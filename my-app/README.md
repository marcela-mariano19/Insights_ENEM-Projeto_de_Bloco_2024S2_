# Projeto de Bloco - Enem Insights

## Como executar o projeto localmente?
- Crie uma env para ter certeza que o ambiente está controlado;
- Inicie a env criada;
- Instale os componente usando como base o arquivo requiments.txt que está na pasta raiz;
- Abra dois terminais no VSCode;
- Escolha um dos terminais e rod streamlit run "./my-app/app/main.py" para iniciar o front-end;
- No segundo terminal já dentro do da pasta my-app, execute  uvicorn app.main:app --reload para iniciar o back-end;
- Configue na variável de ambiente no caminho "my-app/.env" para que o modelo funcione. A chave deve ser o Gemini. 

## 
