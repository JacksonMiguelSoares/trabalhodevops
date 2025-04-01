import fitz  # PyMuPDF
import os

def pdf_to_jpg_pymupdf(pdf_path, output_path, zoom=2, page_number=0):
    """Converte uma página específica de um PDF em uma imagem JPG."""
    try:
        pdf_document = fitz.open(pdf_path)
        page = pdf_document.load_page(page_number)
        mat = fitz.Matrix(zoom, zoom)  # Aumenta a resolução
        pix = page.get_pixmap(matrix=mat)
        output_file = f"{output_path}.jpg"
        pix.save(output_file)
        pdf_document.close()
        print(f"Página {page_number + 1} do PDF '{pdf_path}' convertida para JPG com sucesso!")
    except Exception as e:
        print(f"Erro ao converter página {page_number + 1} do PDF '{pdf_path}': {e}")

def convert_pdfs_recursively(root_folder, output_folder, zoom=2):
    """Converte todos os PDFs em uma pasta e suas subpastas recursivamente,
       EXCLUINDO arquivos que começam com 'Modelo'."""
    print(f"Analisando pasta raiz: {root_folder}")

    for dirpath, dirnames, filenames in os.walk(root_folder):
        print(f"Entrando na pasta: {dirpath}")

        for filename in filenames:
            if filename.endswith(".pdf"):
                # Ignora arquivos que começam com "Modelo"
                if filename.startswith("Modelo"):
                    print(f"Arquivo '{filename}' começa com 'Modelo'. Ignorando.")
                    continue  # Pula para o próximo arquivo

                pdf_path = os.path.join(dirpath, filename)
                print(f"Arquivo PDF encontrado: {pdf_path}")

                # Remove a extensão .pdf do nome do arquivo
                base_name = os.path.splitext(filename)[0]

                # Caminho para salvar as imagens JPG na mesma pasta do PDF
                relative_path = os.path.relpath(dirpath, root_folder)
                output_subfolder = os.path.join(output_folder, relative_path)
                os.makedirs(output_subfolder, exist_ok=True)  # Cria a pasta, se não existir

                try:
                    pdf_document = fitz.open(pdf_path)
                    num_pages = pdf_document.page_count
                    pdf_document.close()

                    if num_pages > 1:
                        # Se o PDF tem mais de uma página, converte cada página com um sufixo
                        for page_number in range(num_pages):
                            output_path = os.path.join(output_subfolder, f"{base_name}_{page_number + 1}")
                            pdf_to_jpg_pymupdf(pdf_path, output_path, zoom, page_number)
                    else:
                        # Se o PDF tem apenas uma página, converte sem sufixo
                        output_path = os.path.join(output_subfolder, base_name)
                        pdf_to_jpg_pymupdf(pdf_path, output_path, zoom, 0)  # Converte a primeira página
                except Exception as e:
                    print(f"Erro ao processar o número de páginas do PDF '{pdf_path}': {e}")
            else:
                print(f"Arquivo '{filename}' não é um PDF. Ignorando.")

# Exemplo de uso:
root_folder = "C:/Users/OTY8513/Downloads/ATIVORE - Automação dos reports"  # Substitua pelo caminho da sua pasta raiz
output_folder = "C:/Users/OTY8513/Downloads/ATIVORE - Automação dos reports"  # Substitua pelo caminho da pasta de saída
zoom = 2  # Fator de zoom (opcional)

convert_pdfs_recursively(root_folder, output_folder, zoom)