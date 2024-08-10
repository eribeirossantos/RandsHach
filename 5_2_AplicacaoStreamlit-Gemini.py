import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
import os
import yaml

# Carregar configurações do arquivo config.yaml
try:
    with open('config.yaml', 'r') as config_file:
        config = yaml.safe_load(config_file)
except FileNotFoundError:
    st.error("Arquivo de configuração não encontrado.")
    st.stop()
except yaml.YAMLError:
    st.error("Erro ao ler o arquivo de configuração.")
    st.stop()

# Definir variável de ambiente para a API key
os.environ['GOOGLE_API_KEY'] = config.get('GOOGLE_API_KEY', '')

# Verificar se a chave da API está presente
if not os.environ['GOOGLE_API_KEY']:
    st.error("Chave da API do Google não encontrada no arquivo de configuração.")
    st.stop()

# Instanciar o ChatGoogleGenerativeAI com o modelo apropriado
googleai = ChatGoogleGenerativeAI(model='gemini-pro') 

# Template de prompt
template = '''
Você é um analista financeiro.
Escreva um relatório financeiro detalhado para a empresa "{empresa}" para o período {periodo}.

O relatório deve ser escrito em {idioma} e incluir a seguinte análise:
{analise}

Certifique-se de fornecer insights e conclusões para esta seção.
Formate o relatório utilizando Markdown.
'''

# Criar o template do prompt
prompt_template = PromptTemplate.from_template(template=template)

# Listas de seleção
empresas = ['Randstad Brasil','Randstad Argentina', 'Randstad Chile', 'Randstad Uruguai', 'Randstad Holanda']
trimestres = ['Q1', 'Q2', 'Q3', 'Q4']
anos = [2021, 2022, 2023, 2024, 2025]
idiomas = ['Português', 'Inglês', 'Espanhol', 'Francês', 'Alemão']
analises = [
    "Análise do Balanço Patrimonial",
    "Análise do Fluxo de Caixa",
    "Análise de Tendências",
    "Análise de Receita e Lucro",
    "Análise de Posição de Mercado",
    "Análise de Rentabilidade",
    "Análise de Liquidez",
    "Análise de Solvência",
    "Análise de Eficiência",
    "Análise de Valor Econômico Adicionado (EVA)",
    "Análise de Retorno sobre o Investimento (ROI)",
    "Análise de Valor de Mercado",
    "Análise de Capital de Giro"
]

# Interface do usuário com Streamlit
st.title('Gerador de Relatório Financeiro:')

empresa = st.sidebar.selectbox('Selecione a empresa:', empresas)
trimestre = st.sidebar.selectbox('Selecione o trimestre:', trimestres)
ano = st.sidebar.selectbox('Selecione o ano:', anos)
periodo = f"{trimestre} {ano}"
idioma = st.sidebar.selectbox('Selecione o idioma:', idiomas)
analise = st.sidebar.selectbox('Selecione a análise:', analises)

# Gerar o relatório
if st.sidebar.button('Gerar Relatório'):
    prompt = prompt_template.format(
        empresa=empresa,
        periodo=periodo,
        idioma=idioma,
        analise=analise
    )

    with st.spinner('Gerando relatório...'):
        try:
            response = googleai.invoke(prompt)
            st.subheader('Relatório Gerado:')
            st.write(response.content)
        except Exception as e:
            st.error(f"Ocorreu um erro ao gerar o relatório: {str(e)}")
