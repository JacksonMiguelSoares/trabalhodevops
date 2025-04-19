import unittest
import tempfile
import os
import shutil
import fitz  # PyMuPDF
from src.main import pdf_to_jpg_pymupdf, convert_pdfs_recursively



class TestConversaoPDF(unittest.TestCase):

    def setUp(self):
        # Criar pastas temporárias
        self.test_dir = tempfile.mkdtemp()
        self.output_dir = tempfile.mkdtemp()

        # Criar PDF simples
        self.pdf_path = os.path.join(self.test_dir, "exemplo.pdf")
        self.criar_pdf_simples(self.pdf_path, "Página de teste")

        # Criar PDF ignorado (começa com "Modelo")
        self.modelo_path = os.path.join(self.test_dir, "Modelo_exemplo.pdf")
        self.criar_pdf_simples(self.modelo_path, "Ignorado")

    def tearDown(self):
        shutil.rmtree(self.test_dir)
        shutil.rmtree(self.output_dir)

    def criar_pdf_simples(self, path, texto="Página"):
        doc = fitz.open()
        page = doc.new_page()
        page.insert_text((72, 72), texto)
        doc.save(path)
        doc.close()

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
        for root, _, files in os.walk(self.output_dir):
            for file in files:
                self.assertFalse(file.startswith("Modelo"), "Arquivo 'Modelo' não deveria ter sido convertido")

    def test_pdf_vazio_nao_cria_imagem(self):
        pdf_vazio_path = os.path.join(self.test_dir, "vazio.pdf")
        fitz.open().save(pdf_vazio_path)  # Cria PDF vazio
        convert_pdfs_recursively(self.test_dir, self.output_dir)
        arquivos_gerados = os.listdir(self.output_dir)
        self.assertFalse(any(f.endswith(".jpg") for f in arquivos_gerados), "Imagem não deveria ser gerada para PDF vazio")

    def test_nome_do_arquivo_convertido(self):
        convert_pdfs_recursively(self.test_dir, self.output_dir)
        arquivos_gerados = os.listdir(self.output_dir)
        nomes_sem_extensao = [os.path.splitext(f)[0] for f in arquivos_gerados if f.endswith(".jpg")]
        self.assertIn("exemplo", "".join(nomes_sem_extensao), "Nome do arquivo convertido está incorreto")

    def test_conversao_em_diretorio_com_arquivos_existentes(self):
        pdf_path = os.path.join(self.test_dir, "existente.pdf")
        self.criar_pdf_simples(pdf_path, texto="Página única")

        imagem_falsa = os.path.join(self.test_dir, "existente_page_0.jpg")
        with open(imagem_falsa, "w") as f:
            f.write("imagem falsa")

        imagens = pdf_para_jpg(pdf_path, self.test_dir)

        self.assertEqual(len(imagens), 1)
        self.assertTrue(os.path.exists(imagens[0]))

    def test_nome_de_arquivo_com_espacos(self):
        pdf_path = os.path.join(self.test_dir, "arquivo com espacos.pdf")
        self.criar_pdf_simples(pdf_path, texto="Com espaços no nome")

        imagens = pdf_para_jpg(pdf_path, self.test_dir)

        self.assertEqual(len(imagens), 1)
        self.assertTrue(imagens[0].endswith(".jpg"))
        self.assertTrue(os.path.exists(imagens[0]))


if __name__ == '__main__':
    unittest.main()
