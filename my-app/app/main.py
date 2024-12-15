# MY APP FILE
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.services.chat import router as chat_router
from fastapi import FastAPI
import requests


app = FastAPI()


app.include_router(chat_router)


st.set_page_config(
    page_title="Insights ENEM",  
    page_icon="📈",                      
    layout="wide",                    
)

def dash_uf(ufs_dict):
    df_ufs = pd.DataFrame(list(ufs_dict.items()),columns = ['UF','Total de Provas Aplicadas'])
    fig = px.bar(df_ufs, x='UF', y='Total de Provas Aplicadas',text_auto=True)
    fig.update_traces(textposition='outside')
    return st.plotly_chart(fig)

def dash_subs_uf(df_uf_region_full):
    ufs_sorted = df_uf_region_full['UF'].sort_values().tolist()
    fig = px.bar(df_uf_region_full, x='UF', y='Total Inscritos',category_orders={'UF':ufs_sorted}, text_auto=True)
    fig.update_traces(textposition='outside')
    return st.plotly_chart(fig)


def dash_Uf_MH(df_uf_region_full,y_list,seletions=None):
    if seletions is None:
        ufs_sorted = df_uf_region_full['UF'].sort_values().tolist()
        fig = px.bar(df_uf_region_full,
                    x='UF',
                    y=y_list,
                    category_orders={'UF':ufs_sorted},
                    barmode='group',
                    )
        return st.plotly_chart(fig)
    else:
        df_selected = df_uf_region_full[df_uf_region_full['UF'].isin(seletions)]
        ufs_sorted = df_selected['UF'].sort_values().tolist()
        fig = px.bar(df_selected,
                    x='UF',
                    y=y_list,
                    category_orders={'UF':ufs_sorted},
                    barmode='group',
                    )
        return st.plotly_chart(fig)
    
def dash_nacionaly(df_uf_region_full):
    fig = px.line(df_uf_region_full, 
                 x='UF', 
                 y=['Inscritos Não Declarados',
       'Inscritos Brasileiros', 'Inscritos Brasileiros Naturalizados',
       'Inscritos Estrangeiros',
       'Inscritos Brasileiros Natos Nascidos no Exterior'],
            log_y=True,
                 )
    return st.plotly_chart(fig)


def dash_pie(df_send,info_name,info_value):
    fig = px.pie(df_send,
                values=info_value,
                names=info_name,
                width=500,  # ajusta a largura
                height=400  # ajusta a altura)
    )
    fig.add_annotation(text='Considerando dados extraídos no dia 21/10/24',
                        x=0.5,
                        y=-0.1,
                        showarrow=False)
    return st.plotly_chart(fig)

def dash_bar_race(df_send_):
    df_filtered = df_send_[['Total Inscritos Raça Não Declarada',
       'Total Inscritos Raça Branca', 'Total Inscritos Raça Preta',
       'Total Inscritos Raça Parda', 'Total Inscritos Raça Amarela',
       'Total Inscritos Raça Indígena']].sum()
    fig = px.bar(df_filtered, x=df_filtered.index,
                y=df_filtered.values,
                text_auto=True)
    return st.plotly_chart(fig)


@st.cache_data
def load_data():
    df  = pd.read_parquet("my-app/data/analysis/df_metrics_inscription.parquet")
    df_uf_region_full = pd.read_parquet("my-app/data/analysis/df_uf_region_full.parquet")

    return df,df_uf_region_full


def main ():
    menu = ['Home','Dados Gerais 2023', ' Visão Inscritos','Visão Desempenho','Fatores de Contexto','Insights IA', 'Criadora','TP1']

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
            col4.metric(label="Total de Treineiros Inscritos", value=df['Total de treineiros inscritos'].apply(lambda x: f"{x:,.0f}".replace(',', '.')).iloc[0])
            col5.metric(label="Total de Mulheres Presentes", value=f"{df_uf_region_full['Total Mulheres Presentes'].sum():,.0f}".replace(',', '.'))
            col6.metric(label="Total de Homens Presentes", value=f"{df_uf_region_full['Total Homens Presentes'].sum():,.0f}".replace(',', '.'))

        col7,col8 = st.columns([1,2])

        with col7:
            st.subheader('Total de Inscritos por Região')
            dash_pie(df_uf_region_full,'Regiao','Total Inscritos')

        with col8:
            st.subheader('Inscritos por UF')
            dash_subs_uf(df_uf_region_full)

        st.subheader('Provas Aplicadas por UF')
        
        #Total de Provas Aplicadas por UF
        dash_uf(df['Total de Provas Aplicadas por UF'][0])


        st.subheader('Total de Inscrições vs Presença - Homens')
        dash_Uf_MH(df_uf_region_full,['Total Homens Inscritos','Total Homens Presentes'])

        if 'ufs_selected_men' not in st.session_state:
            st.session_state.ufs_selected_men = []

        st.write("Quer exibir somente alguns UF's? Selecione abaixo:")
        ufs_selected_men = st.multiselect('UFs', df_uf_region_full['UF'].sort_values(), key='ufs_selected_men')

        if ufs_selected_men:
            dash_Uf_MH(df_uf_region_full=df_uf_region_full, seletions=ufs_selected_men,y_list=['Total Homens Inscritos','Total Homens Presentes'])
        
        if ufs_selected_men != st.session_state['ufs_selected_men']:
            st.session_state.ufs_selected_men = ufs_selected_men

###############################################################################################################################################################

        st.subheader('Total de Inscrições vs Presença - Mulheres')
        dash_Uf_MH(df_uf_region_full,['Total Mulheres Inscritas','Total Mulheres Presentes'])

        def woman_selected():
            st.write(st.session_state.ufs_selected_woman)

        if 'ufs_selected_woman' not in st.session_state:
            st.session_state.ufs_selected_woman = []

        st.write("Quer exibir somente alguns UF's? Selecione abaixo:")
        ufs_selected_woman = st.multiselect('UFs', df_uf_region_full['UF'].sort_values(), key='ufs_selected_woman')

        if ufs_selected_woman != st.session_state['ufs_selected_woman']:
            st.session_state.ufs_selected_woman = ufs_selected_woman

        if ufs_selected_woman:
            dash_Uf_MH(df_uf_region_full=df_uf_region_full, seletions=ufs_selected_woman,y_list=['Total Mulheres Inscritas','Total Mulheres Presentes'])
        

        st.subheader('Dados Gerais para Download:')

        st.dataframe(df_uf_region_full)
        
        
        
    elif choice == ' Visão Inscritos':

        st.subheader('Inscritos por Nacionalidade')
        dash_nacionaly(df_uf_region_full)

        st.subheader('Inscritos por Cor/Raça')
        dash_bar_race(df_uf_region_full)


        with st.container():
            col9,col10,col11 = st.columns(3)
            with col9:
                st.subheader('Inscritos por Região e Cor/Raça Não Declarada')
                dash_pie(df_uf_region_full,'Regiao','Total Inscritos Raça Não Declarada')

            with col10:
                st.subheader('Inscritos por Região e Cor/Raça Branca')
                dash_pie(df_uf_region_full,'Regiao','Total Inscritos Raça Branca')

            with col11:
                st.subheader('Inscritos por Região e Cor/Raça Parda')
                dash_pie(df_uf_region_full,'Regiao','Total Inscritos Raça Parda')
        
        with st.container():
            col12,col13,col14 = st.columns(3)
            with col12:
                st.subheader('Inscritos por Região e Cor/Raça Amarela')
                dash_pie(df_uf_region_full,'Regiao','Total Inscritos Raça Amarela')

            with col13:
                st.subheader('Inscritos por Região e Cor/Raça Preta')
                dash_pie(df_uf_region_full,'Regiao','Total Inscritos Raça Preta')

            with col14:
                st.subheader('Inscritos por Região e Cor/Raça Indígena')
                dash_pie(df_uf_region_full,'Regiao','Total Inscritos Raça Indígena')


        st.subheader('Inscritos por Faixa Etária')
        df_group_age = df_uf_region_full[['UF','Inscritos menores de 17 anos',
       'Inscritos com 17 anos', 'Inscritos com 18 anos',
       'Inscritos com 19 anos', 'Inscritos com 20 anos',
       'Inscritos com 21 anos', 'Inscritos com 22 anos',
       'Inscritos com 23 anos', 'Inscritos com 24 anos',
       'Inscritos com 25 anos', 'Inscritos entre 26 e 30 anos',
       'Inscritos entre 31 e 35 anos', 'Inscritos entre 36 e 40 anos',
       'Inscritos entre 41 e 45 anos', 'Inscritos entre 46 e 50 anos',
       'Inscritos entre 51 e 55 anos', 'Inscritos entre 56 e 60 anos',
       'Inscritos entre 61 e 65 anos', 'Inscritos entre 66 e 70 anos',
       'Inscritos maiores de 70 anos']].sort_values(by='UF')
        
        st.dataframe(df_group_age)
    
    elif choice == 'Visão Desempenho':
        st.write('EM DESENVOLVIMENTO')
    
    elif choice == 'Fatores de Contexto':
        st.write('EM DESENVOLVIMENTO')

    elif choice == 'Insights IA':
        st.markdown('**Oi, eu sou a especialista do ENEM Insights. Informe o estado para que gerar um texto com o que está "escondido" nos dados do ENEM 2023.**')
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        
        for message in st.session_state.messages:
            with st.chat_message(message['role']):
                st.markdown(message['content'])

        if chat_uf := st.chat_input("Digite a UF que deseja gerar um texto sobre o desempenho no ENEM 2023:", key='chat_uf'):
            st.session_state.messages.append({"role": "user", "content":chat_uf }) #Adicionando a mensagem do usuário ao histórico de mensagens
            with st.chat_message("user"):
                st.markdown(chat_uf)
            
            with st.chat_message("assistant"):
                with st.spinner("Gerando texto..."):
                    req = requests.post("http://localhost:8000/chat", #Não achei forma de subir do df ou deixat ele pré-carregado
                                        json={"text": chat_uf})
                    response = req.json()
                    st.markdown(response['message'])
            st.session_state.messages.append({"role": "assistant", "content":response['message']}) #Adicionando a mensagem do assistente ao histórico de mensagens
                
    
    elif choice == 'Criadora':
        st.subheader('Marcela Mariano')
        st.write('Atualmente, sou aluna do curso de Ciência de Dados do Instituto INFNET e estou no 4º período. Além disso, sou gestora de N2 na empresa [SPOT Metrics](https://spotmetrics.com/)')
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