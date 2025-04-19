import unittest
import tempfile
import os
import shutil
import fitz
from src.main import pdf_to_jpg_pymupdf, convert_pdfs_recursively  # Corrigido para importar do src.main

class TestConversaoPDF(unittest.TestCase):

    def setUp(self):
        # Criar pastas temporárias
        self.test_dir = tempfile.mkdtemp()
        self.output_dir = tempfile.mkdtemp()

        # Criar PDF simples
        self.pdf_path = os.path.join(self.test_dir, "exemplo.pdf")
        doc = fitz.open()
        page = doc.new_page()
        page.insert_text((72, 72), "Página de teste")
        doc.save(self.pdf_path)
        doc.close()

        # Criar PDF ignorado (começa com "Modelo")
        self.modelo_path = os.path.join(self.test_dir, "Modelo_exemplo.pdf")
        doc = fitz.open()
        doc.new_page()
        doc.save(self.modelo_path)
        doc.close()

    def tearDown(self):
        shutil.rmtree(self.test_dir)
        shutil.rmtree(self.output_dir)

    def test_pdf_to_jpg_pymupdf_gera_imagem(self):
        output_file = os.path.join(self.output_dir, "teste_img")
        pdf_to_jpg_pymupdf(self.pdf_path, output_file)
        self.assertTrue(os.path.exists(output_file + ".jpg"))

    def test_convert_pdfs_recursively_cria_imagem(self):
        convert_pdfs_recursively(self.test_dir, self.output_dir)
        arquivos_gerados = os.listdir(self.output_dir)
        encontrou = any(f.endswith(".jpg") for f in arquivos_gerados)
        self.assertTrue(encontrou, "Nenhuma imagem JPG foi gerada")

    def test_convert_pdfs_recursively_ignora_modelo(self):
        convert_pdfs_recursively(self.test_dir, self.output_dir)
        # Verificar que a imagem do PDF "Modelo..." não foi gerada
        for root, _, files in os.walk(self.output_dir):
            for file in files:
                self.assertFalse(file.startswith("Modelo"), "Arquivo 'Modelo' não deveria ter sido convertido")

if __name__ == '__main__':
    unittest.main()
