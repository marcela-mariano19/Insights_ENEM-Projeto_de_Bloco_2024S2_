import streamlit as st
import requests   

from app.services.chat import router as chat_router
from fastapi import FastAPI


st.set_page_config(
    page_title="ENEM Insights",  
    page_icon="📈",                      
    layout="wide",                    
)

st.sidebar.image("my-app/docs/logo_infnet.png", width=200, caption="by Marcela Mariano")    

app = FastAPI()
app.include_router(chat_router)


st.title("Insights IA")

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
        
