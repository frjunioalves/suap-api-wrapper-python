import stat

import pytest

from suap_api.config import clear_config, normalize_url, save_config, load_config
from suap_api.exceptions import SuapNotLoggedInError


class TestNormalizeUrl:
    def test_returns_base_domain(self) -> None:
        assert normalize_url("https://suap.ifpi.edu.br") == "https://suap.ifpi.edu.br"

    def test_strips_trailing_slash(self) -> None:
        assert normalize_url("https://suap.ifpi.edu.br/") == "https://suap.ifpi.edu.br"

    def test_adds_https_when_no_scheme(self) -> None:
        assert normalize_url("suap.ifpi.edu.br") == "https://suap.ifpi.edu.br"

    def test_strips_whitespace(self) -> None:
        assert normalize_url("  https://suap.ifpi.edu.br  ") == "https://suap.ifpi.edu.br"

    def test_removes_api_v2_suffix(self) -> None:
        assert normalize_url("https://suap.ifpi.edu.br/api/v2") == "https://suap.ifpi.edu.br"

    def test_removes_api_v2_suffix_with_slash(self) -> None:
        assert normalize_url("https://suap.ifpi.edu.br/api/v2/") == "https://suap.ifpi.edu.br"


class TestSaveAndLoadConfig:
    def test_round_trip(self, tmp_path, monkeypatch) -> None:
        monkeypatch.setattr("suap_api.config.CONFIG_DIR", tmp_path / ".suap")
        monkeypatch.setattr("suap_api.config.CONFIG_FILE", tmp_path / ".suap" / "config.json")

        save_config("https://suap.ifpi.edu.br", "20221234")
        config = load_config()

        assert config["base_url"] == "https://suap.ifpi.edu.br"
        assert config["username"] == "20221234"

    def test_file_permissions(self, tmp_path, monkeypatch) -> None:
        config_file = tmp_path / ".suap" / "config.json"
        monkeypatch.setattr("suap_api.config.CONFIG_DIR", tmp_path / ".suap")
        monkeypatch.setattr("suap_api.config.CONFIG_FILE", config_file)

        save_config("https://suap.ifpi.edu.br", "20221234")

        mode = stat.S_IMODE(config_file.stat().st_mode)
        assert mode == 0o600

    def test_load_raises_when_no_config(self, tmp_path, monkeypatch) -> None:
        monkeypatch.setattr("suap_api.config.CONFIG_FILE", tmp_path / "nonexistent.json")

        with pytest.raises(SuapNotLoggedInError):
            load_config()


class TestClearConfig:
    def test_removes_file(self, tmp_path, monkeypatch) -> None:
        config_file = tmp_path / "config.json"
        config_file.write_text("{}")
        monkeypatch.setattr("suap_api.config.CONFIG_FILE", config_file)

        clear_config()

        assert not config_file.exists()

    def test_no_error_when_file_missing(self, tmp_path, monkeypatch) -> None:
        monkeypatch.setattr("suap_api.config.CONFIG_FILE", tmp_path / "nonexistent.json")
        clear_config()
