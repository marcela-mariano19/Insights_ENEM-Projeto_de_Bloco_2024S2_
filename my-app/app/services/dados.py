from fastapi import FastAPI,Path,HTTPException
import pandas as pd

router_data = FastAPI()

@router_data.get(
    "/dados/",
    description="Retorna os dados da análise dos microdados do ENEM 2023. Ela pode ser usada para por pessoas que construir as próprias visualizações.",
    responses={
        200: {
            "description": "Sucesso",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "UF": "DF",
                            "Total Inscritos": 72975,
                            "Regiao": "Centro-Oeste",
                            "Total Presentes": 50267,
                            "Total Homens Inscritos": 28782,
                            "Total Mulheres Inscritas": 44193,
                            "Total Homens Presentes": 19719,
                            "Total Mulheres Presentes": 30548,
                            "Percentual de Presentes": 68.88,
                            "Total Inscritos Raça Não Declarada": 1171,
                            "Total Inscritos Raça Branca": 29224,
                            "Total Inscritos Raça Preta": 10126,
                            "Total Inscritos Raça Parda": 30989,
                            "Total Inscritos Raça Amarela": 1230,
                            "Total Inscritos Raça Indígena": 235,
                            "Inscritos menores de 17 anos": 5511,
                            "Inscritos com 17 anos": 13132,
                            "Inscritos com 18 anos": 16435,
                            "Inscritos com 19 anos": 7789,
                            "Inscritos com 20 anos": 4993,
                            "Inscritos com 21 anos": 3398,
                            "Inscritos com 22 anos": 2492,
                            "Inscritos com 23 anos": 2023,
                            "Inscritos com 24 anos": 1655,
                            "Inscritos com 25 anos": 1437,
                            "Inscritos entre 26 e 30 anos": 4776,
                            "Inscritos entre 31 e 35 anos": 2821,
                            "Inscritos entre 36 e 40 anos": 2224,
                            "Inscritos entre 41 e 45 anos": 1753,
                            "Inscritos entre 46 e 50 anos": 1181,
                            "Inscritos entre 51 e 55 anos": 708,
                            "Inscritos entre 56 e 60 anos": 402,
                            "Inscritos entre 61 e 65 anos": 151,
                            "Inscritos entre 66 e 70 anos": 65,
                            "Inscritos maiores de 70 anos": 29,
                            "Inscritos Não Declarados": 32,
                            "Inscritos Brasileiros": 71637,
                            "Inscritos Brasileiros Naturalizados": 1083,
                            "Inscritos Estrangeiros": 104,
                            "Inscritos Brasileiros Natos Nascidos no Exterior": 119
                        }
                    ]
                }
            }
        }
    }
)


def get_dados():
    result = pd.read_parquet("my-app/data/analysis/df_uf_region_full.parquet").to_dict(orient="records")
    return result

@app.get("/dados/{uf}",
          description="Retorna os dados da análise dos microdados do ENEM 2023 para um estado específico.",
           responses={
        200: {
            "description": "Sucesso",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "UF": "RJ",
                            "Total Inscritos": 72975,
                            "Regiao": "Centro-Oeste",
                            "Total Presentes": 50267,
                            "Total Homens Inscritos": 28782,
                            "Total Mulheres Inscritas": 44193,
                            "Total Homens Presentes": 19719,
                            "Total Mulheres Presentes": 30548,
                            "Percentual de Presentes": 68.88,
                            "Total Inscritos Raça Não Declarada": 1171,
                            "Total Inscritos Raça Branca": 29224,
                            "Total Inscritos Raça Preta": 10126,
                            "Total Inscritos Raça Parda": 30989,
                            "Total Inscritos Raça Amarela": 1230,
                            "Total Inscritos Raça Indígena": 235,
                            "Inscritos menores de 17 anos": 5511,
                            "Inscritos com 17 anos": 13132,
                            "Inscritos com 18 anos": 16435,
                            "Inscritos com 19 anos": 7789,
                            "Inscritos com 20 anos": 4993,
                            "Inscritos com 21 anos": 3398,
                            "Inscritos com 22 anos": 2492,
                            "Inscritos com 23 anos": 2023,
                            "Inscritos com 24 anos": 1655,
                            "Inscritos com 25 anos": 1437,
                            "Inscritos entre 26 e 30 anos": 4776,
                            "Inscritos entre 31 e 35 anos": 2821,
                            "Inscritos entre 36 e 40 anos": 2224,
                            "Inscritos entre 41 e 45 anos": 1753,
                            "Inscritos entre 46 e 50 anos": 1181,
                            "Inscritos entre 51 e 55 anos": 708,
                            "Inscritos entre 56 e 60 anos": 402,
                            "Inscritos entre 61 e 65 anos": 151,
                            "Inscritos entre 66 e 70 anos": 65,
                            "Inscritos maiores de 70 anos": 29,
                            "Inscritos Não Declarados": 32,
                            "Inscritos Brasileiros": 71637,
                            "Inscritos Brasileiros Naturalizados": 1083,
                            "Inscritos Estrangeiros": 104,
                            "Inscritos Brasileiros Natos Nascidos no Exterior": 119
                        }
                    ]
                }
            }
        }
    }
)

def get_uf(uf:str = Path(..., description="Unidade Federativa (UF) para a qual deseja-se obter os dados. Utilize a sigla do estado, por exemplo: 'SP' para São Paulo, 'RJ' para Rio de Janeiro, etc.")):
    
    result = pd.read_parquet("my-app/data/analysis/df_uf_region_full.parquet").query(f"UF == '{uf}'").to_dict(orient="records")

    return result