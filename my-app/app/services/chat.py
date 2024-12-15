from langchain_community.llms import HuggingFaceHub
from langchain.schema import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
import os
from dotenv import load_dotenv
from fastapi import APIRouter,HTTPException
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
    

    #Criando template para chat. Usei como base uma explicação que o professor Fernando deu em aula.
    template = ChatPromptTemplate([
        ("system", "Você é um criador de textos de até dois parágrafos sobre os dados do enem 2023. Caso você não tenha informações, avise ao usuário."),
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
