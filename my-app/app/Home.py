# MY APP FILE
import pandas as pd
import streamlit as st
from fastapi import FastAPI
import sys
import os

#Usado para que o app consiga importar os arquivos de outras pastas
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.chat import router as chat_router  # Importação correta


st.set_page_config(
    page_title="ENEM Insights",  
    page_icon="📈",                      
    layout="wide",                    
)

app = FastAPI()


app.include_router(chat_router)

def main ():
    st.sidebar.image("my-app/docs/logo_infnet.png", width=200, caption="by Marcela Mariano")    
    st.title("ENEM Insights")
    st.subheader('O que é o ENEM Insights?')
    st.write("Hoje, a maior parte das pessoas que trabalham com educação no Brasil não conseguem acessar informações sobre o ENEM de forma fácil e rápida. Visando curar essa dor surgiu o Enem Insights, uma aplicação que permite a qualquer pessoa acessar informações sobre o ENEM de forma fácil e prática.")

    st.subheader('Por que o ENEM Insights foi criado?')
    st.markdown("O [Instituto INFNET](https://www.infnet.edu.br/infnet/home/) propôs que os alunos do curso de Ciência de Dados criassem um projeto de bloco ligado aos Objetivos de Desenvolvimento Sustentável no Brasil, então a aluna Marcela Mariano propôs o projeto Enem Insights, que une seu amor pela educação e pela análise de dados.") 

    st.subheader("Esta aplicação tem ligação com quais Objetivos de Desenvolvimento Sustentável?")
    st.markdown("Este projeto está ligado ao ODS 4 - Educação de Qualidade, pois visa facilitar o acesso a informações sobre o ENEM, que é uma das principais formas de acesso ao ensino superior no Brasil. Esses dados ajudam a entender melhor o cenário educacional do país e a identificar possíveis melhorias. Quer saber mais sobre as metas do ODS 4? [Clique aqui](https://brasil.un.org/pt-br/sdgs/4)")

    st.subheader("De onde vêm os dados?")
    st.markdown("Os dados utilizados nesta aplicação são públicos e foram disponibilizados pelo [INEP](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enem). Legal, né? O governo brasileiro oferece esses e outros dados devido a lei de Dados Abertos. ")
    

###############################################################################################################################################################


if __name__ == '__main__':
    main()