# MY APP FILE
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

import os
os.system('pip install fastparquet')


st.set_page_config(
    page_title="Insights ENEM",  
    page_icon="📈",                      
    layout="wide",                    
)

def dash_Uf(ufs_dict):
    df_ufs = pd.DataFrame(list(ufs_dict.items()),columns = ['UF','Total de Provas Aplicadas'])
    fig, ax = plt.subplots( figsize=(7,3))
    ax.bar(df_ufs['UF'], df_ufs['Total de Provas Aplicadas'])
    ax.tick_params(axis='x', rotation=45)
    #ax.legend()
    return fig





def main ():
    menu = ['Home', 'Nevegando nos Dados', 'Criadora','TP1']

    st.title("Insights ENEM")
    choice = st.sidebar.selectbox('Menu', menu)

    if choice == 'Home':
        st.subheader('O que é o ENEM Insights?')
        st.write("Hoje, a maior parte das pessoas que trabalham com educação no Brasil não conseguem acessar informações sobre o ENEM de forma fácil e rápida. Visando curar essa dor surgiu o Enem Insights, uma aplicação que permite a qualquer pessoa acessar informações sobre o ENEM de forma fácil e prática.")
        df  = pd.read_parquet("my-app/data/analysis/df_metrics_inscription.parquet")

        st.subheader('Métricas de Inscrição:')
        col1,col2,col3 = st.columns(3)
        with st.container():
            #Foi necessário usar o apply para formatar os valores e como esse format usa string tive que usar f-string, usar replace para trocar a virgula por ponto e usar iloc para pegar o primeiro valor da série pandas que retorna 
            col1.metric(label="Total de Inscritos", value=df['Total de inscritos'].apply(lambda x: f"{x:,.0f}".replace(',', '.')).iloc[0])
            col2.metric(label="Total de Inscritos Presentes", value=df['Total de inscritos presentes'].apply(lambda x: f"{x:,.0f}".replace(',', '.')).iloc[0])
            col3.metric(label="Total de Inscritos Ausentes", value=df['Total de inscritos ausentes'].apply(lambda x: f"{x:,.0f}".replace(',', '.')).iloc[0])

        col4, col5, col6 = st.columns(3)
        with st.container():
            col4.metric(label="Total de Treineiros Presentes", value=df['Total de treineiros inscritos'].apply(lambda x: f"{x:,.0f}".replace(',', '.')).iloc[0])
            col5.metric(label="Total de Mulheres Presentes", value=df['Total de Mulheres inscritas'].apply(lambda x: f"{x:,.0f}".replace(',', '.')).iloc[0])
            col6.metric(label="Total de Homens Presentes", value=df['Total de Homens inscritos'].apply(lambda x: f"{x:,.0f}".replace(',', '.')).iloc[0])

        st.subheader('Provas Aplicadas por UF')

        st.pyplot(dash_Uf(df['Total de Provas Aplicadas por UF'][0]))
        



    elif choice == 'TP1':
        st.write('Criado apenas para o professor ter noção da evolução')
        st.write("Amostra dos dados:")
        df_enem_amostra = pd.read_csv("my-app/data/treated/df_enem_amostra.csv", sep=';')
        #df_enem_amostra = pd.read_csv("C:/Users/Marcela Beatriz/Documents/GitHub/ENEM_Insights-Projeto_de_Bloco_2024S2/my-app/data/treated/df_enem_amostra.csv", sep=';')

        st.write(df_enem_amostra.head(20))

        st.subheader('Dicionário de dados:')
        st.markdown("Aqui você encontra o significado de cada coluna do dataset: [Dicionário](https://docs.google.com/spreadsheets/d/1p56xjEUy2MyGt4uuweztZZ2erjhO7CxI/edit?usp=sharing&ouid=102518780984891267084&rtpof=true&sd=true)")

        st.subheader('Links úteis e Fontes de Ispiração:')
        st.markdown("1. [Sinopses Estatísticas](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/sinopses-estatisticas/enem/)")	


if __name__ == '__main__':
    main()