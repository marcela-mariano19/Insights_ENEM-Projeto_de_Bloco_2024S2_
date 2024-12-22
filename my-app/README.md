# Projeto de Bloco - Enem Insights
Este repositório foi criado para armazenar o projeto de bloco de 2024S2. Ele foi criado com o objetivo de trazer um novo ponto de vista para os microdados dados do ENEM 2023.

## Como executar o projeto localmente?
- Crie uma env para ter certeza que o ambiente está controlado;
- Inicie a env criada;
- Instale os componente usando como base o arquivo requiments.txt que está na pasta raiz;
- Abra dois terminais no VSCode;
- Dentro da pasta raiz, rode streamlit run "./my-app/app/Home.py" para iniciar o front-end;
- No segundo terminal já dentro do da pasta my-app, execute  uvicorn app.Home:app --reload para iniciar o back-end;
- Configue na variável de ambiente no caminho "my-app/.env" para que o modelo funcione. A chave deve ser o Gemini. 

## 
