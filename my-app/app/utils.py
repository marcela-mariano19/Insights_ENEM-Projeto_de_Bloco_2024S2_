import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px

@st.cache_data
def load_data():
    """
    Carrega e retorna os DataFrames para o aplicativo Streamlit. Fiz dessa forma para evitar que os DataFrames sejam carregados a cada interação do usuário.
    """
    df = pd.read_parquet("my-app/data/analysis/df_metrics_inscription.parquet")
    df_uf_region_full = pd.read_parquet("my-app/data/analysis/df_uf_region_full.parquet")
    
    return df,df_uf_region_full
   

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