from langchain_community.llms import HuggingFaceHub
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
from fastapi import APIRouter,HTTPException,Path
from ..model.chat import ChatModel
import pandas as pd



path_env = "my-app/.env"
load_dotenv()

router = APIRouter()

def gerar_texto_uf(uf, df):
    # Filtrar os dados do estado
    dic_uf = { #Criado para que o app suporte o nome por extenso dos estados
        "ACRE": "AC",
        "ALAGOAS": "AL",
        "AMAPÁ": "AP",
        "AMAZONAS": "AM",
        "BAHIA": "BA",
        "CEARÁ": "CE",
        "DISTRITO FEDERAL": "DF",
        "ESPÍRITO SANTO": "ES",
        "GOIÁS": "GO",
        "MARANHÃO": "MA",
        "MATO GROSSO": "MT",
        "MATO GROSSO DO SUL": "MS",
        "MINAS GERAIS": "MG",
        "PARÁ": "PA",
        "PARAÍBA": "PB",
        "PARANÁ": "PR",
        "PERNAMBUCO": "PE",
        "PIAUÍ": "PI",
        "RIO DE JANEIRO": "RJ",
        "RIO GRANDE DO NORTE": "RN",
        "RIO GRANDE DO SUL": "RS",
        "RONDÔNIA": "RO",
        "RORAIMA": "RR",
        "SANTA CATARINA": "SC",
        "SÃO PAULO": "SP",
        "SERGIPE": "SE",
        "TOCANTINS": "TO"
    }
    if (uf).upper() in dic_uf:
        uf = dic_uf[(uf).upper()]
    
    elif (uf).upper() in dic_uf.values():
        uf = (uf).upper()
    else:
        return "Não foi possível encontrar informações sobre o estado informado. Por favor, tente novamente com um estado válido"
    
    df_uf = df[df['UF'] == (uf).upper()].iloc[0]
    
    # Gerar o contexto com base nas informações do dataframe.
    contexto = f"Dados do ENEM 2023 para o estado de {uf} em até 2 parágrafos:\n"
    contexto += f" - Total de inscritos {df_uf['Total Inscritos']}\n"
    contexto += f" - Total de mulheres inscritas {df_uf['Total Mulheres Inscritas']}\n"
    contexto += f" - Total de mulheres presentes {df_uf['Total Mulheres Presentes']}\n"
    contexto += f" - Total de homens inscritos {df_uf['Total Homens Inscritos']}\n"
    contexto += f" - Total de homens presentes {df_uf['Total Homens Presentes']}\n"
    contexto += f" - Nota média de Ciências da Natureza {df_uf['Nota Média  Ciências da Natureza']}\n"
    contexto += f" - Nota média de Ciências Humanas {df_uf['Nota Média  Ciências Humanas']}\n"
    contexto += f" - Nota média de Linguagens e Códigos {df_uf['Nota Média  Linguagens e Códigos']}\n"
    contexto += f" - Nota média de Matemática {df_uf['Nota Média  Matemática']}\n"
    contexto += f" - Nota média de Redação {df_uf['Nota Média Redação']}\n"
    contexto += f" - Nota máxima de Ciências da Natureza {df_uf['Nota Máxima  Ciências da Natureza']}\n"
    contexto += f" - Nota máxima de Ciências Humanas {df_uf['Nota Máxima  Ciências Humanas']}\n"
    contexto += f" - Nota máxima de Linguagens e Códigos {df_uf['Nota Máxima  Linguagens e Códigos']}\n"
    contexto += f" - Nota máxima de Matemática {df_uf['Nota Máxima  Matemática']}\n"
    contexto += f" - Nota máxima de Redação {df_uf['Nota Máxima Redação']}\n"
    

    #Criando template para chat. Usei como base uma explicação que o professor Fernando deu em aula.
    template = ChatPromptTemplate([
        ("system", "Você é um cientista de dados que está recebendo dados do ENEM 2023. Crie uma análise com base no contexto. Caso você não tenha informações, avise ao usuário."),
        ("user", " {contexto}")
    ])

    KEY = os.getenv('GOOGLE_API_KEY')

    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.5)
    response = llm.invoke(template.format_messages(contexto=contexto))
    return response.content

@router.post("/chat")
async def gerar_texto(body: ChatModel):
    try:
        # Carregar o dataframe
        df = pd.read_parquet("data/analysis/df_uf_region_full.parquet")
        response = gerar_texto_uf(body.text, df)
        return {"message": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro inesperado no back-end str(e)")

@router.get(
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
async def get_dados():
    result = pd.read_parquet("my-app/data/analysis/df_uf_region_full.parquet").to_dict(orient="records")
    return result

@router.get("/dados/{uf}",
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
    if len(result) == 0:
        raise HTTPException(status_code=404, detail="UF não encontrada")
    
    return result