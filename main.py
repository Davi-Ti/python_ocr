import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import os

# Define explicitamente o caminho para o executável do Tesseract
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"


def process_pdf(pdf_path):
    """
    Extrai texto de um PDF usando OCR.
    """
    try:
        pages = convert_from_path(pdf_path)
        return "\n".join(
            f"--- Página {i +
                          1} ---\n{pytesseract.image_to_string(page, lang='por')}"
            for i, page in enumerate(pages)
        )
    except Exception as e:
        print(f"Erro ao processar PDF {pdf_path}: {e}")
        return ""


def process_image(image_path):
    """
    Extrai texto de uma imagem usando OCR.
    """
    try:
        img = Image.open(image_path)
        return pytesseract.image_to_string(img, lang='por')
    except Exception as e:
        print(f"Erro ao processar imagem {image_path}: {e}")
        return ""


def process_files_in_folder(folder_path):
    """
    Itera sobre todos os arquivos da pasta, processa PDFs e imagens,
    e salva os textos extraídos em arquivos separados.
    """
    if not os.path.exists(folder_path):
        print(f"Pasta '{folder_path}' não encontrada!")
        return

    output_folder = os.path.join(folder_path, "extracted_text")
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        if os.path.isfile(file_path):
            print(f"Processando arquivo: {filename}")
            ext = filename.lower().split('.')[-1]

            if ext in ['pdf', 'png', 'jpg', 'jpeg']:
                try:
                    if ext == 'pdf':
                        text = process_pdf(file_path)
                    else:
                        text = process_image(file_path)

                    output_file = os.path.join(
                        output_folder, f"{filename}.txt")
                    with open(output_file, "w", encoding="utf-8") as f:
                        f.write(text)
                    print(f"Texto extraído salvo em: {output_file}")

                except Exception as e:
                    print(f"Erro ao processar {filename}: {e}")
            else:
                print(f"Formato não suportado: {filename}")


# Defina o caminho da pasta com os arquivos
folder_to_scan = './docs_to_scan'

# Processa os arquivos na pasta
process_files_in_folder(folder_to_scan)
