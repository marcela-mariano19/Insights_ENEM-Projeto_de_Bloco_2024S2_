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
    df_ufs.set_index('UF', inplace=True)
    
    return st.bar_chart(df_ufs,)

def dash_Uf_MH(df_uf_region_full):

    return st.bar_chart(df_uf_region_full,x='UF',y=['Total Homens Inscritos','Total Mulheres Inscritas','Total Homens Presentes','Total Mulheres Presentes'],stack=False)

def dash_Uf_selected_MH(df_send,seletions):
    df_send = df_send[df_send['UF'].isin(seletions)]

    return st.bar_chart(df_send,x='UF',y=['Total Homens Inscritos','Total Mulheres Inscritas','Total Homens Presentes','Total Mulheres Presentes'],stack=False)

@st.cache_data
def load_data():
    df  = pd.read_parquet("my-app/data/analysis/df_metrics_inscription.parquet")
    df_uf_region_full = pd.read_parquet("my-app/data/analysis/df_uf_region_full.parquet")

    return df,df_uf_region_full


def main ():
    menu = ['Home','Dados Gerais 2023', ' Visão Inscritos','Visão Concluintes','Visão Desempenho','Fatores de Contexto','Personalizado', 'Criadora','TP1']

    st.title("Insights ENEM")
    choice = st.sidebar.selectbox('Menu', menu)

    df, df_uf_region_full  = load_data()

    if choice == 'Home':
        st.subheader('O que é o ENEM Insights?')
        st.write("Hoje, a maior parte das pessoas que trabalham com educação no Brasil não conseguem acessar informações sobre o ENEM de forma fácil e rápida. Visando curar essa dor surgiu o Enem Insights, uma aplicação que permite a qualquer pessoa acessar informações sobre o ENEM de forma fácil e prática.")

        st.subheader('Por que o ENEM Insights foi criado?')
        st.markdown("O [Instituto INFNET](https://www.infnet.edu.br/infnet/home/) propôs que os alunos do curso de Ciência de Dados criassem um projeto de bloco ligado aos Objetivos de Desenvolvimento Sustentável no Brasil, então a aluna Marcela Mariano propôs o projeto Enem Insights, que une seu amor pela educação e pela análise de dados.") 

        st.subheader("Esta aplicação tem ligação com qual Objetivos de Desenvolvimento Sustentável?")
        st.markdown("Este projeto está ligado ao ODS 4 - Educação de Qualidade, pois visa facilitar o acesso a informações sobre o ENEM, que é uma das principais formas de acesso ao ensino superior no Brasil. Esses dados ajudam a entender melhor o cenário educacional do país e a identificar possíveis melhorias. Quer saber mais sobre as metas do ODS 4? [Clique aqui](https://brasil.un.org/pt-br/sdgs/4)")
    
        st.subheader("De onde vêm os dados?")
        st.markdown("Os dados utilizados nesta aplicação são públicos e foram disponibilizados pelo [INEP](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enem). Legal, né? O governo brasileiro oferece esses e outros dados devido a lei de Dados Abertos. ")
        
    elif choice == 'Dados Gerais 2023':

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
        
        #Total de Provas Aplicadas por UF
        dash_Uf(df['Total de Provas Aplicadas por UF'][0])

        #Total de Mulheres e Homens iscritos vs Presentes por UF
        st.subheader('Total de Mulheres e Homens Inscritos vs Presentes por UF')
        dash_Uf_MH(df_uf_region_full)

        if 'ufs_selected' not in st.session_state:
            st.session_state['ufs_selected'] = []

        st.write("Quer exibir somente alguns UF's? Selecione abaixo:")
        ufs_selected = st.multiselect('UFs', df_uf_region_full['UF'].sort_values(), default=st.session_state['ufs_selected'])

        st.session_state['ufs_selected'] = ufs_selected

        if ufs_selected:
            dash_Uf_selected_MH(df_uf_region_full,ufs_selected)


        st.subheader('Dados Gerais para Download:')

        st.dataframe(df_uf_region_full)
        


        
        
    elif choice == ' Visão Inscritos':
        st.write('EM DESENVOLVIMENTO')

    elif choice == 'Visão Concluintes':
        st.write('EM DESENVOLVIMENTO')
    
    elif choice == 'Visão Desempenho':
        st.write('EM DESENVOLVIMENTO')
    
    elif choice == 'Fatores de Contexto':
        st.write('EM DESENVOLVIMENTO')

    elif choice == 'Personalizado':
        st.write('EM DESENVOLVIMENTO')
    
    elif choice == 'Criadora':
        st.subheader('Marcela Mariano')
        st.write('Aluna do curso de Ciência de Dados do Instituto INFNET')
        st.write('Linkedin: [Marcela Mariano](https://www.linkedin.com/in/marcela-mariano-8a0b6a1b4/)')


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