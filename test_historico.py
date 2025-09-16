import unittest
import json
import os
import tempfile
import shutil
from datetime import datetime
from unittest.mock import patch
from main import Chatbot

class TestHistorico(unittest.TestCase):
    def setUp(self):
        """Cria instância do Chatbot para testes."""
        self.core_path = 'core_data.json'
        self.new_path = 'new_data.json'
        self.bot = Chatbot(self.core_path, self.new_path)
        self.historico_path = 'historico.json'
        self.temp_dir = tempfile.mkdtemp()
        self.bot.historico_path = os.path.join(self.temp_dir, 'historico.json')  # Usar temp para evitar conflitos
        self.bot.historico = []  # Reset para testes isolados
        self.bot.interacoes_count = 0

    def tearDown(self):
        """Limpa arquivo de histórico após cada teste para isolamento."""
        historico_temp = self.bot.historico_path
        if os.path.exists(historico_temp):
            try:
                os.remove(historico_temp)
            except PermissionError:
                pass  # Ignora se em uso
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_carregar_historico_arquivo_inexistente(self):
        """Testa carregamento quando arquivo não existe (deve retornar [])."""
        self.bot.historico = []  # Reset
        historico = self.bot._carregar_historico()
        self.assertEqual(historico, [])
        # Count setado em init, mas para teste isolado, checar len
        self.assertEqual(len(historico), 0)

    def test_carregar_historico_com_dados(self):
        """Testa carregamento com 1 entrada usando arquivo temp."""
        dados = [{"timestamp": "2023-01-01T00:00:00", "pergunta": "test1", "resposta": "resp1", "personalidade": "formal"}]
        historico_path = self.bot.historico_path
        
        # Criar arquivo temp
        with open(historico_path, 'w', encoding='utf-8') as f:
            json.dump(dados, f, ensure_ascii=False)
        
        historico = self.bot._carregar_historico()
        self.assertEqual(len(historico), 1)
        self.assertEqual(historico[0]["pergunta"], "test1")
        # Simular set count como em init
        self.bot.interacoes_count = len(historico)
        self.assertEqual(self.bot.interacoes_count, 1)

    def test_carregar_historico_mais_de_cinco(self):
        """Testa rotação: carrega 6, deve retornar só últimas 5 usando arquivo temp."""
        dados_completos = [{"timestamp": f"2023-01-0{i}T00:00:00", "pergunta": f"test{i}", "resposta": f"resp{i}", "personalidade": "formal"} for i in range(1, 7)]
        historico_path = self.bot.historico_path
        
        # Criar arquivo com 6 entradas
        with open(historico_path, 'w', encoding='utf-8') as f:
            json.dump(dados_completos, f, ensure_ascii=False)
        
        historico = self.bot._carregar_historico()
        self.assertEqual(len(historico), 5)
        self.assertEqual(historico[0]["pergunta"], "test2")  # Índice 1 (test2)
        self.bot.interacoes_count = len(historico)
        self.assertEqual(self.bot.interacoes_count, 5)

    def test_salvar_historico_basico(self):
        """Testa salvamento de uma entrada e verificação no arquivo."""
        pergunta = "Olá"
        resposta = "Oi!"
        personalidade = "formal"
        
        success = self.bot._salvar_historico(pergunta, resposta, personalidade)
        self.assertTrue(success)
        self.assertEqual(len(self.bot.historico), 1)
        self.assertEqual(self.bot.interacoes_count, 1)
        
        # Verificar arquivo
        historico_path = self.bot.historico_path
        with open(historico_path, 'r', encoding='utf-8') as f:
            dados = json.load(f)
            self.assertEqual(len(dados), 1)
            self.assertEqual(dados[0]["pergunta"], pergunta)

    def test_salvar_historico_rotacao(self):
        """Testa rotação: salva 6, deve manter 5."""
        for i in range(6):
            self.bot._salvar_historico(f"Test {i}", f"Resp {i}", "formal")
        
        self.assertEqual(len(self.bot.historico), 5)
        self.assertEqual(self.bot.interacoes_count, 5)
        self.assertEqual(self.bot.historico[0]["pergunta"], "Test 1")  # Após rotação, começa com Test1 (índice 1 de 0-5)

        # Verificar arquivo
        historico_path = self.bot.historico_path
        with open(historico_path, 'r', encoding='utf-8') as f:
            dados = json.load(f)
            self.assertEqual(len(dados), 5)
            self.assertEqual(dados[0]["pergunta"], "Test 1")

    def test_salvar_historico_entrada_vazia(self):
        """Testa rejeição de entradas vazias."""
        success = self.bot._salvar_historico("", "resp", "formal")
        self.assertFalse(success)
        self.assertEqual(len(self.bot.historico), 0)
        self.assertEqual(self.bot.interacoes_count, 0)

if __name__ == '__main__':
    unittest.main()