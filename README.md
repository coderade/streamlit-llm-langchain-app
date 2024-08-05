# streamlit-llm-langchain-app

Aplicação desenvolvida utilizando Streamlit, LLM e LangChain. 

Essa aplicação foi criada para o curso de MiT em Inteligencia Artificial, é uma applicação interativa com uso de LLMs para resolver um problema específico.

## Sobre a Aplicação

A aplicação é desenvolvida em Python, onde é usado o Streamlit para a criação do cliente (interface do usuario) da aplicação, 
o LangChain é responsável por estruturar a interação entre o modelo de linguagem (LLM) e as solicitações dos usuários e 
no projeto o modelo de linguagem generativa fornecido pelo Google `gemini-1.5-flash` é utilizado para gerar recomendações 
de jogos com base nas solicitações dos usuários.

## Como Usar

Esse projeto usa o modelo `gemini-1.5-flash` da Google para geração de texto, dessa forma é necessário criar uma API Key no Google AI Studio.
Para fazer isso use esse link: [Get AI Studio API Key](https://aistudio.google.com/app/apikey)

Após criar a API Key exporte a mesma no seu terminal usando o seguinte comando:

    export GOOGLE_API_KEY="<API_KEY>"

Após isso, você pode executar a aplicação usando o seguinte comando:

    streamlit run main.py



