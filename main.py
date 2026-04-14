from suap_api import SuapClient

with SuapClient() as client:
    dados = client.comum.get_my_data()                                                                                                        
    diarios = client.edu.get_diaries('2025.1')                                                                                                  
    diario = client.edu.get_diary_classes(54401)                                                                                                
    materiais = client.edu.get_diary_materials(54401)                                                                                    
    material = client.edu.get_material(109248)                                                                                           
    materialpdf = client.edu.get_material_pdf(63895, 96840)  

print(materialpdf)