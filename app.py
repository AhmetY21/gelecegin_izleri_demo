__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
import os
#from utils import history_teller  # Not needed now since we'll define a similar function inline

load_dotenv(override=True)
api_key = os.getenv("OPENAI_API_KEY")
vectorstore = Chroma(
    embedding_function=OpenAIEmbeddings(api_key=api_key),
    persist_directory="vectorstore_data"
)
# Assuming vectorstore is already defined and contains embeddings from Çatalhöyük PDF
# For example: vectorstore = Chroma.from_documents([...], embedding=OpenAIEmbeddings())
retriever = vectorstore.as_retriever()

# Define the catalhoyuk_info function
def catalhoyuk_info(question):
    """Retrieve detailed information about Çatalhöyük based on user's question."""
    # Retrieve relevant context from the vector database
    retrieved_context = retriever.get_relevant_documents(question)
    
    # Concatenate retrieved contexts
    context_text = "\n".join(doc.page_content for doc in retrieved_context)

    # System-level prompt tailored for Çatalhöyük
    system_prompt = (
        "Sen, Çatalhöyük hakkında detaylı bilgi veren bir yardımcı asistansın. Aşağıdaki soruya dayanarak "
        "Çatalhöyük ile ilgili arkeolojik, tarihi, kültürel ve yapısal özellikleri anlat. "
        "Lütfen bilgileri başlıklar, madde işaretleri ve uygun yerlerde emoji kullanarak ve Markdown formatında sun.\n\n"
        "İşte Çatalhöyük hakkında bağlam:\n\n{context}"
    )

    # Prepare messages for the OpenAI chat completion
    messages = [
        {"role": "system", "content": system_prompt.format(context=context_text)},
        {"role": "user", "content": question}
    ]
    
    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=messages
    )
    
    return response.choices[0].message.content

api_key = os.getenv("OPENAI_API_KEY")

# Set page configuration
st.set_page_config(page_title="Çatalhöyük Rehberi", page_icon="🏺", layout="centered")

# Title
st.title("Çatalhöyük'e Sanal Tur Rehberi 🏺")

# Display embedded PDF about Çatalhöyük (ensure catalhoyuk.pdf is in the directory)
pdf_file = "catalhoyuk.pdf"
st.markdown("### Tur Rehberi")

st.markdown("---")

st.markdown("### Merak Ettiğiniz Soruyu Sorun:")
user_question = st.text_input("Çatalhöyük hakkında merak ettiğiniz herhangi bir şeyi sorun...")

if user_question.strip():
    with st.spinner("Bilgi alınıyor..."):
        output = catalhoyuk_info(user_question)
    #st.markdown("#### Cevap:")
    st.markdown(output, unsafe_allow_html=True)
else:
    st.info("Çatalhöyük hakkında bir soru girin ve Enter'a basın.")

# Footer
st.markdown("---")


