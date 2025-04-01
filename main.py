import fitz
import os
import tkinter as tk
from tkinter import messagebox, filedialog

def pdf_to_jpg(pdf_path, output_path, zoom=2, page_number=0):
    try:
        with fitz.open(pdf_path) as pdf_document:
            page = pdf_document.load_page(page_number)
            mat = fitz.Matrix(zoom, zoom)  # Aumenta a resolução
            pix = page.get_pixmap(matrix=mat)
            output_file = f"{output_path}.jpg"
            pix.save(output_file)
            print(f"Página {page_number + 1} do PDF '{pdf_path}' convertida para JPG com sucesso!")
    except Exception as e:
        print(f"Erro ao converter página {page_number + 1} do PDF '{pdf_path}': {e}")

def convert_pdfs_recursively(root_folder, output_folder, zoom=2):

    print(f"Analisando pasta raiz: {root_folder}")

    for dirpath, dirnames, filenames in os.walk(root_folder):
        print(f"Entrando na pasta: {dirpath}")

        for filename in filenames:
            if not filename.lower().endswith(".pdf"):
                print(f"Ignorado (não é PDF): {filename}")
                continue

            if filename.lower().startswith("modelo"):
                print(f"Ignorado (começa com 'Modelo'): {filename}")
                continue

            pdf_path = os.path.join(dirpath, filename)
            base_name = os.path.splitext(filename)[0]
            relative_path = os.path.relpath(dirpath, root_folder)
            output_subfolder = os.path.join(output_folder, relative_path)
            os.makedirs(output_subfolder, exist_ok=True)

            try:
                with fitz.open(pdf_path) as pdf_document:
                    num_pages = pdf_document.page_count

                for page_number in range(num_pages):
                    output_path = os.path.join(output_subfolder, f"{base_name}_{page_number + 1}")
                    pdf_to_jpg(pdf_path, output_path, zoom, page_number)
            except Exception as e:
                print(f"Erro ao processar '{pdf_path}': {e}")

# Abrir o explorador de arquivos para selecionar a pasta
root = tk.Tk()
root.withdraw()
root_folder = filedialog.askdirectory(title="Selecione a pasta de entrada")
output_folder = filedialog.askdirectory(title="Selecione a pasta de saída")

if root_folder and output_folder:
    zoom = 2
    convert_pdfs_recursively(root_folder, output_folder, zoom)
else:
    print("Operação cancelada pelo usuário.")

print("Conversão concluída!")
 # Exibir mensagem ao concluir
root = tk.Tk()
root.withdraw()
messagebox.showinfo("Conversão Concluída", "Todos os PDFs foram convertidos com sucesso!")