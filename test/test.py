import os
import fitz  # PyMuPDF
import shutil
import pytest
from src.main import pdf_to_jpg_pymupdf, convert_pdfs_recursively  # Corrigido o import

# Pasta temporária para testes
TEST_INPUT_DIR = "test_data/input"
TEST_OUTPUT_DIR = "test_data/output"

@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    # Cria pastas de teste
    os.makedirs(TEST_INPUT_DIR, exist_ok=True)
    os.makedirs(TEST_OUTPUT_DIR, exist_ok=True)

    # Cria um PDF simples com 2 páginas
    doc = fitz.open()
    for i in range(2):
        page = doc.new_page()
        page.insert_text((72, 72), f"Página {i + 1}")
    doc.save(os.path.join(TEST_INPUT_DIR, "teste.pdf"))
    doc.close()

    # Cria um PDF chamado Modelo para teste de exclusão
    doc = fitz.open()
    doc.new_page().insert_text((72, 72), "Este é um modelo")
    doc.save(os.path.join(TEST_INPUT_DIR, "Modelo_Exemplo.pdf"))
    doc.close()

    yield  # Executa os testes

    # Limpa tudo após os testes
    shutil.rmtree("test_data")


def test_pdf_to_jpg_single_page():
    pdf_path = os.path.join(TEST_INPUT_DIR, "teste.pdf")
    output_path = os.path.join(TEST_OUTPUT_DIR, "teste_single")
    pdf_to_jpg_pymupdf(pdf_path, output_path, page_number=0)
    assert os.path.exists(output_path + ".jpg")


def test_pdf_to_jpg_second_page():
    pdf_path = os.path.join(TEST_INPUT_DIR, "teste.pdf")
    output_path = os.path.join(TEST_OUTPUT_DIR, "teste_page2")
    pdf_to_jpg_pymupdf(pdf_path, output_path, page_number=1)
    assert os.path.exists(output_path + ".jpg")


def test_exclude_modelo_file():
    convert_pdfs_recursively(TEST_INPUT_DIR, TEST_OUTPUT_DIR)
    # Nome correto considerando o padrão: base + _1.jpg
    modelo_output_1 = os.path.join(TEST_OUTPUT_DIR, "Modelo_Exemplo_1.jpg")
    modelo_output_2 = os.path.join(TEST_OUTPUT_DIR, "Modelo_Exemplo.jpg")
    assert not os.path.exists(modelo_output_1)
    assert not os.path.exists(modelo_output_2)


def test_multiple_pages_converted():
    convert_pdfs_recursively(TEST_INPUT_DIR, TEST_OUTPUT_DIR)
    page1 = os.path.join(TEST_OUTPUT_DIR, "teste_1.jpg")
    page2 = os.path.join(TEST_OUTPUT_DIR, "teste_2.jpg")
    assert os.path.exists(page1)
    assert os.path.exists(page2)


def test_non_pdf_file_ignored():
    # Cria um arquivo que não é PDF
    txt_path = os.path.join(TEST_INPUT_DIR, "arquivo.txt")
    with open(txt_path, "w") as f:
        f.write("Conteúdo de teste")

    convert_pdfs_recursively(TEST_INPUT_DIR, TEST_OUTPUT_DIR)
    # Garante que esse arquivo não resultou em imagem
    output_files = os.listdir(TEST_OUTPUT_DIR)
    assert all(not file.startswith("arquivo") for file in output_files)
