import streamlit as st
from openai import OpenAI
import fitz  # PyMuPDF
import io
import os

# Configurar a chave da API
client = OpenAI(
    api_key=os.environ["open_api_key"] ,
)

# Função para carregar o arquivo
def load_file(file):
    if file.type == "application/pdf":
        return load_pdf(file)
    elif file.type == "text/plain":
        return load_txt(file)
    return None

# Função para carregar PDF
def load_pdf(file):
    pdf_document = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    return text

# Função para carregar TXT
def load_txt(file):
    return file.read().decode('utf-8')

# Função para fazer perguntas ao ChatGPT
def ask_question(content, question):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Você é um assistente útil."},
            {"role": "user", "content": f"Baseado no seguinte conteúdo:\n\n{content}\n\nResponda a seguinte pergunta:\n\n{question}"}
        ],
        max_tokens=150,
        temperature=0.7,
    )
    return response.choices[0].message.content

# Configurar o layout do Streamlit
st.title("Pergunte ao Documento")
uploaded_file = st.file_uploader("Faça o upload do seu arquivo de texto ou PDF", type=["pdf", "txt"])

if uploaded_file is not None:
    content = load_file(uploaded_file)
    st.text_area("Conteúdo do Arquivo", content, height=250)
    
    question = st.text_input("Faça uma pergunta sobre o conteúdo do arquivo:")
    
    if st.button("Perguntar"):
        if content and question:
            answer = ask_question(content, question)
            st.write("Resposta:")
            st.write(answer)
        else:
            st.write("Por favor, carregue um arquivo e faça uma pergunta.")
