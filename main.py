import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import os

# Definir o caminho da variável TESSDATA_PREFIX (se necessário)
os.environ['TESSDATA_PREFIX'] = '/usr/share/tessdata'

def process_pdf(pdf_path):
    # Converte o PDF em uma lista de imagens
    pages = convert_from_path(pdf_path)

    # Variável para armazenar o texto extraído
    extracted_text = ""

    # Itera sobre cada página
    for page_number, page in enumerate(pages, start=1):
        # Usa OCR na imagem da página
        text = pytesseract.image_to_string(page, lang='por')  # Define o idioma como 'por' para português
        # Adiciona o texto extraído ao conteúdo
        extracted_text += f"\n\n--- Página {page_number} ---\n\n{text}"

    return extracted_text

def process_image(image_path):
    # Abre a imagem
    img = Image.open(image_path)
    # Usa OCR na imagem
    text = pytesseract.image_to_string(img, lang='por')  # Define o idioma como 'por' para português
    return text

def process_files_in_folder(folder_path):
    # Itera sobre todos os arquivos da pasta
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        # Verifica se é um arquivo
        if os.path.isfile(file_path):
            # Extrai a extensão do arquivo
            ext = filename.lower().split('.')[-1]

            # Variável para armazenar o texto extraído
            extracted_text = ""

            # Verifica se é PDF
            if ext == 'pdf':
                print(f"Processando PDF: {filename}")
                extracted_text = process_pdf(file_path)
            # Verifica se é imagem (PNG, JPEG, etc.)
            elif ext in ['png', 'jpg', 'jpeg']:
                print(f"Processando Imagem: {filename}")
                extracted_text = process_image(file_path)
            else:
                print(f"Formato não suportado: {filename}")
                continue  # Pula arquivos que não são suportados

            # Define o nome do arquivo de texto de saída
            output_text_file = os.path.join(folder_path, f"{filename}.txt")

            # Salva o texto extraído em um arquivo de texto
            with open(output_text_file, 'w', encoding='utf-8') as f:
                f.write(extracted_text)

            print(f"Texto extraído e salvo em: {output_text_file}")

# Defina o caminho da pasta onde os arquivos estão localizados
folder_to_scan = './docs_to_scan'

# Processa todos os arquivos na pasta
process_files_in_folder(folder_to_scan)
