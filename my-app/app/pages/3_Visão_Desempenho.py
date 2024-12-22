import streamlit as st
from utils import load_data, dash_pie, dash_uf, dash_Uf_MH, dash_subs_uf
import plotly.express as px

st.set_page_config(
    page_title="ENEM Insights",  
    page_icon="📈",                      
    layout="wide",                    
)

df, df_uf_region_full = load_data()

st.sidebar.image("my-app/docs/logo_infnet.png", width=200, caption="by Marcela Mariano")    

st.subheader("Desempenho por Região")

df_sum = df_uf_region_full[['Regiao','Nota Média  Ciências da Natureza','Nota Média  Ciências Humanas','Nota Média  Linguagens e Códigos','Nota Média  Matemática','Nota Média Redação']].groupby('Regiao', as_index=False).mean()

# Gráfico de Ciências da Natureza
fig_cn = px.line(
    df_sum,
    x='Regiao',
    y='Nota Média  Ciências da Natureza',
    markers=True,
    title='Nota Média de Ciências da Natureza por Região',
)

# Gráfico de Ciências Humanas
fig_ch = px.line(
    df_sum,
    x='Regiao',
    y='Nota Média  Ciências Humanas',
    markers=True,
    title='Nota Média de Ciências Humanas por Região',
)

# Criar gráfico de linha para Linguagens e Códigos
fig_lc = px.line(
    df_sum,
    x='Regiao',
    y='Nota Média  Linguagens e Códigos',
    markers=True,
    title='Nota Média de Linguagens e Códigos por Região'
)

# Criar gráfico de linha para Matemática
fig_mt = px.line(
    df_sum,
    x='Regiao',
    y='Nota Média  Matemática',
    markers=True,
    title='Nota Média de Matemática por Região',
    range_y=[0, None]
)

# Cria layout com duas colunas
col1, col2 = st.columns(2)

# Exibir gráficos lado a lado
with col1:
    st.plotly_chart(fig_cn, use_container_width=True)  
    st.plotly_chart(fig_mt, use_container_width=True)  

with col2:
    st.plotly_chart(fig_ch, use_container_width=True)  
    st.plotly_chart(fig_lc, use_container_width=True)  


# Cria gráfico de linha para Redação. Deixei separado, porque esteticamente ficou melhor.
fig_rd = px.line(
    df_sum,
    x='Regiao',
    y='Nota Média Redação',
    markers=True,
    title='Nota Média de Redação por Região',
)

# Exibir o gráfico de Redação

st.plotly_chart(fig_rd)

st.subheader('Desempenho por UF')

# Os Gráficos ficaram ruins em conjunto, então vamos exibir separadamente. 

#Comparação entre Médias de escolas rural e urbana

fig_r_u = px.bar(
    df_uf_region_full,
    x='UF',
    y=['Nota Média Redação Escola Urbana', 'Nota Média Redação Escola Rural'],
    title='Média de Notas da Redação por Tipo de Escola e UF',
    barmode='group',
)

st.plotly_chart(fig_r_u)


#Gráfico de barra de média de notas de  Ciências da Natureza por UF
fig_uf_cn = px.bar(
    df_uf_region_full,
    x='UF',
    y='Nota Média  Ciências da Natureza',
    title='Nota Média de Ciências da Natureza por UF',
)
                
#Gráfico de barra de média de notas de  Ciências Humanas por UF
fig_uf_ch = px.bar(
    df_uf_region_full,
    x='UF',
    y='Nota Média  Ciências Humanas',
    title='Nota Média de Ciências Humanas por UF',
)

#Gráfico de barra de média de notas de  Linguagens e Códigos por UF
fig_uf_lc = px.bar(
    df_uf_region_full,
    x='UF',
    y='Nota Média  Linguagens e Códigos',
    title='Nota Média de Linguagens e Códigos por UF',
)

#Gráfico de barra de média de notas de  Matemática por UF

fig_uf_mt = px.bar(
    df_uf_region_full,
    x='UF',
    y='Nota Média  Matemática',
    title='Nota Média de Matemática por UF',
)


# Cria layout com duas colunas
col3, col4 = st.columns(2)

# Exibir gráficos lado a lado
with col3:
    st.plotly_chart(fig_uf_cn, use_container_width=True)  
    st.plotly_chart(fig_uf_mt, use_container_width=True)  

with col4:
    st.plotly_chart(fig_uf_ch, use_container_width=True)  
    st.plotly_chart(fig_uf_lc, use_container_width=True)  