# MY APP FILE
import pandas as pd
import streamlit as st

import os
os.system('pip install fastparquet')


st.set_page_config(
    page_title="Insights ENEM",  
    page_icon="📈",                      
    layout="wide",                    
)

st.title("Insights ENEM")
st.write("Hoje, a maior parte das pessoas que trabalham com educação no Brasil não conseguem acessar informações sobre o ENEM de forma fácil e rápida. Visando curar essa dor surgiu o Enem Insights, uma aplicação que permite a qualquer pessoa acessar informações sobre o ENEM de forma fácil e rápida.")

st.write("Amostra dos dados:")
df_enem_amostra = pd.read_csv("my-app/data/treated/df_enem_amostra.csv", sep=';')
#df_enem_amostra = pd.read_csv("C:/Users/Marcela Beatriz/Documents/GitHub/ENEM_Insights-Projeto_de_Bloco_2024S2/my-app/data/treated/df_enem_amostra.csv", sep=';')

st.write(df_enem_amostra.head(20))

st.subheader('Dicionário de dados:')
st.markdown("Aqui você encontra o significado de cada coluna do dataset: [Dicionário](https://docs.google.com/spreadsheets/d/1p56xjEUy2MyGt4uuweztZZ2erjhO7CxI/edit?usp=sharing&ouid=102518780984891267084&rtpof=true&sd=true)")

st.subheader('Links úteis e Fontes de Ispiração:')
st.markdown("1. [Sinopses Estatísticas](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/sinopses-estatisticas/enem/)")	