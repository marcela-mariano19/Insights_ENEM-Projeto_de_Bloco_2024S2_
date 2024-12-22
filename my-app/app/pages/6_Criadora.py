import streamlit as st

st.set_page_config(
    page_title="ENEM Insights",  
    page_icon="📈",                      
    layout="wide",                    
)
st.sidebar.image("my-app/docs/logo_infnet.png", width=200, caption="by Marcela Mariano")    

import streamlit as st

# Configurar o título da página
#

col1, col2 = st.columns([1, 2])  

with col1:
    st.image("my-app/docs/marcela_mariano.jpeg", width=200)  

with col2:
    st.title("Marcela Mariano")
    st.write(
        """
        Atualmente, sou aluna do curso de **Ciência de Dados** do Instituto INFNET e estou no **4º período**. Além disso, sou **gestora de N2** na empresa [SPOT Metrics](https://www.spotmetrics.com).
        """
    )
    st.markdown("🔗 **LinkedIn**: [Marcela Mariano](https://www.linkedin.com/in/seu-link)")
    st.markdown("📧 **Email**: marcela.beatriz20info@gmail.com")

# Adicionar uma seção adicional sobre suas habilidades
st.subheader("Habilidades e Interesses")
st.write(
    """
    - 📊 Análise de Dados e Visualização
    - 💻 Python e Machine Learning
    - 🚀 Desenvolvimento de Dashboards Interativos
    - 📈 Business Intelligence
    - 📚 Aprendizado Contínuo
    - 🛒💡 Retail
    """
)


