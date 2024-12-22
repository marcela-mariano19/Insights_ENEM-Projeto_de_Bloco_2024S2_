import streamlit as st
from utils import load_data, dash_pie, dash_uf, dash_Uf_MH, dash_subs_uf
import locale

st.set_page_config(
    page_title="ENEM Insights",  
    page_icon="📈",                      
    layout="wide",                    
)

st.sidebar.image("my-app/docs/logo_infnet.png", width=200, caption="by Marcela Mariano")    

st.title("Dados Gerais 2023")

df, df_uf_region_full = load_data()

st.subheader("Métricas de Inscrição")
col1, col2, col3 = st.columns(3)


# Configurar locale para formato brasileiro
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

with st.container():
    col1.metric("Total de Inscritos", f"{df['Total de inscritos'].iloc[0]:n}")
    col2.metric("Total de Inscritos Presentes", f"{df['Total de inscritos presentes'].iloc[0]:n}")
    col3.metric("Total de Inscritos Ausentes", f"{df['Total de inscritos ausentes'].iloc[0]:n}")

col4, col5, col6 = st.columns(3)
with st.container():
    col4.metric("Total de Treineiros Inscritos", f"{df['Total de treineiros inscritos'].iloc[0]:n}")
    col5.metric("Total de Mulheres Presentes", f"{df_uf_region_full['Total Mulheres Presentes'].sum():n}")
    col6.metric("Total de Homens Presentes", f"{df_uf_region_full['Total Homens Presentes'].sum():n}")


st.subheader("Total de Inscritos por Região")
dash_pie(df_uf_region_full, 'Regiao', 'Total Inscritos')

st.subheader("Inscritos por UF")
dash_subs_uf(df_uf_region_full)

st.subheader("Provas Aplicadas por UF")
dash_uf(df['Total de Provas Aplicadas por UF'][0])

st.subheader("Total de Inscrições vs Presença - Homens")
dash_Uf_MH(df_uf_region_full, ['Total Homens Inscritos', 'Total Homens Presentes'])

if 'ufs_selected_men' not in st.session_state:
    st.session_state.ufs_selected_men = []

st.write("Quer exibir somente alguns UF's? Selecione abaixo:")
ufs_selected_men = st.multiselect('UFs', df_uf_region_full['UF'].sort_values(), key='ufs_selected_men')

if ufs_selected_men:
    dash_Uf_MH(df_uf_region_full=df_uf_region_full, seletions=ufs_selected_men,y_list=['Total Homens Inscritos','Total Homens Presentes'])

if ufs_selected_men != st.session_state['ufs_selected_men']:
    st.session_state.ufs_selected_men = ufs_selected_men


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
