import streamlit as st
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import tempfile
import os
import shutil

# Detecta automaticamente o caminho do executável do Tesseract
tesseract_path = shutil.which('tesseract')
if tesseract_path is not None:
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
else:
    st.error('O Tesseract OCR não foi encontrado em seu sistema. Por favor, instale o Tesseract e certifique-se de que ele está no PATH do sistema.')
    st.stop()

# Configuração da página
st.set_page_config(page_title="Extração de Texto via OCR",
                   page_icon="📄", layout="wide")

# Título e descrição
st.title("📄 Extração de Texto via OCR")
st.markdown("""
Bem-vindo à aplicação de extração de texto via OCR! Faça upload de imagens ou PDFs, e o sistema irá extrair o texto contido neles.
""")

# Seleção de idioma para o OCR
st.sidebar.header("Configurações")
languages = {'Português': 'por', 'Inglês': 'eng',
             'Espanhol': 'spa', 'Francês': 'fra', 'Alemão': 'deu'}
language = st.sidebar.selectbox(
    "Selecione o idioma para OCR", list(languages.keys()), index=0)
lang_code = languages[language]

# Upload de arquivos
st.sidebar.header("Upload de Arquivos")
uploaded_files = st.sidebar.file_uploader(
    "Carregue suas imagens ou PDFs",
    type=['png', 'jpg', 'jpeg', 'pdf'],
    accept_multiple_files=True
)

# Função para processar PDFs


def process_pdf(file_path):
    images = convert_from_path(file_path)
    text = ""
    for i, image in enumerate(images):
        page_text = pytesseract.image_to_string(image, lang=lang_code)
        text += f"--- Página {i+1} ---\n{page_text}\n"
    return text

# Função para processar imagens


def process_image(image):
    text = pytesseract.image_to_string(image, lang=lang_code)
    return text


# Processamento dos arquivos carregados
if uploaded_files:
    for uploaded_file in uploaded_files:
        st.subheader(f"Arquivo: {uploaded_file.name}")
        # Salva o arquivo temporariamente
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(uploaded_file.read())
            temp_filename = temp_file.name

        file_ext = os.path.splitext(uploaded_file.name)[1].lower()

        if file_ext == '.pdf':
            try:
                with st.spinner('Processando PDF...'):
                    text = process_pdf(temp_filename)
                st.success('Processamento concluído!')
                with st.expander("Visualizar Texto Extraído"):
                    st.text_area("Texto Extraído", text, height=300)
                st.download_button(
                    label="📥 Baixar Texto",
                    data=text,
                    file_name=f"{uploaded_file.name}.txt",
                    mime="text/plain"
                )
            except Exception as e:
                st.error(f"Erro ao processar o PDF: {e}")
        elif file_ext in ['.png', '.jpg', '.jpeg']:
            try:
                image = Image.open(temp_filename)
                col1, col2 = st.columns(2)
                with col1:
                    st.image(image, caption='Imagem Carregada',
                             use_container_width=True)
                with col2:
                    with st.spinner('Processando Imagem...'):
                        text = process_image(image)
                    st.success('Processamento concluído!')
                    st.text_area("Texto Extraído", text, height=300)
                    st.download_button(
                        label="📥 Baixar Texto",
                        data=text,
                        file_name=f"{uploaded_file.name}.txt",
                        mime="text/plain"
                    )
            except Exception as e:
                st.error(f"Erro ao processar a imagem: {e}")
        else:
            st.warning("Formato de arquivo não suportado.")

        # Remove o arquivo temporário
        os.unlink(temp_filename)
