import streamlit as st
from utils import load_data, dash_nacionaly, dash_pie, dash_bar_race

st.set_page_config(
    page_title="ENEM Insights",  
    page_icon="📈",                      
    layout="wide",                    
)

st.sidebar.image("my-app/docs/logo_infnet.png", width=200, caption="by Marcela Mariano")    

df, df_uf_region_full = load_data()

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
    