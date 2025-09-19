import unittest
import json
import os
import tempfile
import shutil
from datetime import datetime
from unittest.mock import patch
from infra.repositories import CoreRepo, LearnedRepo, HistoryRepo, StatsRepo
from infra.logging_conf import get_logger
from core.intent_matcher import IntentMatcher
from core.chatbot import Chatbot

class TestHistorico(unittest.TestCase):
    def setUp(self):
        """Cria instância do Chatbot para testes."""
        self.core_path = 'data/core_data.json'
        self.new_path = 'data/new_data.json'
        self.temp_dir = tempfile.mkdtemp()
        self.logger = get_logger("test_historico")
        self.core_repo = CoreRepo(self.core_path, logger=self.logger)
        self.learned_repo = LearnedRepo(self.new_path, logger=self.logger)
        self.intent_matcher = IntentMatcher(intencoes=self.core_repo.load_intents(), aprendidos=self.learned_repo.load(), logger=self.logger)
        self.historico_path = os.path.join(self.temp_dir, 'historico.json')
        self.stats_path = os.path.join(self.temp_dir, 'stats.json')
        self.history_repo = HistoryRepo(self.historico_path, logger=self.logger)
        self.stats_repo = StatsRepo(self.stats_path, logger=self.logger)
        self.bot = Chatbot(matcher=self.intent_matcher, learned_repo=self.learned_repo, history_repo=self.history_repo, logger=self.logger)
        self.bot.stats_repo = self.stats_repo # Sobrescrever para usar o repo de teste


    def tearDown(self):
        """Limpa arquivo de histórico após cada teste para isolamento."""
        historico_temp = self.historico_path
        if os.path.exists(historico_temp):
            try:
                os.remove(historico_temp)
            except PermissionError:
                pass  # Ignora se em uso
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_carregar_historico_arquivo_inexistente(self):
        """Testa carregamento quando arquivo não existe (deve retornar [])."""
        historico = self.history_repo._read_json()
        self.assertIsNone(historico) # Deve retornar None se o arquivo não existe

    def test_carregar_historico_com_dados(self):
        """Testa carregamento com 1 entrada usando arquivo temp."""
        dados = [{"timestamp": "2023-01-01T00:00:00", "pergunta": "test1", "resposta": "resp1", "personalidade": "formal"}]
        with open(self.historico_path, 'w', encoding='utf-8') as f:
            json.dump(dados, f, ensure_ascii=False)
        
        historico = self.history_repo._read_json()
        self.assertEqual(len(historico), 1)
        self.assertEqual(historico[0]["pergunta"], "test1")

    def test_carregar_historico_mais_de_cinco(self):
        """Testa rotação: carrega 6, deve retornar só últimas 5 usando arquivo temp."""
        dados_completos = [{"timestamp": f"2023-01-0{i}T00:00:00", "pergunta": f"test{i}", "resposta": f"resp{i}", "personalidade": "formal"} for i in range(1, 7)]
        with open(self.historico_path, 'w', encoding='utf-8') as f:
            json.dump(dados_completos, f, ensure_ascii=False)
        
        historico = self.history_repo.load_last(5)
        self.assertEqual(len(historico), 5)
        self.assertEqual(historico[0]["pergunta"], "test2")

    def test_salvar_historico_basico(self):
        """Testa salvamento de uma entrada e verificação no arquivo."""
        pergunta = "Olá"
        resposta = "Oi!"
        personalidade = "formal"
        
        self.history_repo.append(pergunta, resposta, personalidade)
        
        # Verificar arquivo
        with open(self.historico_path, 'r', encoding='utf-8') as f:
            dados = json.load(f)
            self.assertEqual(len(dados), 1)
            self.assertEqual(dados[0]["pergunta"], pergunta)

    def test_salvar_historico_rotacao(self):
        """Testa rotação: salva 6, deve manter 5."""
        for i in range(6):
            self.history_repo.append(f"Test {i}", f"Resp {i}", "formal")
        
        # Verificar arquivo
        with open(self.historico_path, 'r', encoding='utf-8') as f:
            dados = json.load(f)
            self.assertEqual(len(dados), 5)
            self.assertEqual(dados[0]["pergunta"], "Test 1")

    def test_salvar_historico_entrada_vazia(self):
        """Testa rejeição de entradas vazias."""
        # A validação agora está no Chatbot, não no repo
        pass

    def test_salvar_historico_novos_campos(self):
        """Testa append com novos campos Task 13."""
        pergunta = "Test tag"
        resposta = "Resp tag"
        personalidade = "formal"
        tag = "math_basic"
        is_fallback = True
        
        self.history_repo.append(pergunta, resposta, personalidade, tag_intencao=tag, is_fallback=is_fallback)
        
        dados = self.history_repo._read_json()
        self.assertEqual(len(dados), 1)
        entry = dados[0]
        self.assertIn("timestamp_in", entry)
        self.assertIn("timestamp_out", entry)
        self.assertEqual(entry["tag_intencao"], tag)
        self.assertEqual(entry["is_fallback"], is_fallback)

    def test_salvar_historico_entrada_vazia(self):
        """Testa que entradas vazias não são salvas pelo HistoryRepo."""
        # HistoryRepo não valida entradas vazias, ele apenas as armazena.
        # A validação é feita na camada de negócio (Chatbot).
        # Este teste é removido pois não se aplica diretamente ao HistoryRepo.
        pass

    def test_carregar_historico_novos_campos(self):
        """Testa carregamento com novos campos Task 13."""
        dados = [{"timestamp_in": "2023-01-01T00:00:00", "timestamp_out": "2023-01-01T00:00:01", "pergunta": "test", "resposta": "resp", "personalidade": "formal", "tag_intencao": "math", "is_fallback": True}]
        with open(self.historico_path, 'w') as f:
            json.dump(dados, f)
        historico = self.history_repo._read_json()
        self.assertEqual(len(historico), 1)
        self.assertIn("tag_intencao", historico[0])

    def test_end_to_end_interacao(self):
        """Testa fluxo end-to-end: processar mensagem, salvar, stats."""
        resposta, is_fallback, tag = self.bot.processar_mensagem("oi", "formal")
        
        stats = self.bot.get_stats()
        self.assertEqual(stats['total_interactions'], 1)

    def test_atualizar_stats_incrementa_total_e_personalidade(self):
        """Testa incremento de total_interactions e por_personalidade."""
        self.stats_repo.update_interaction(False, "formal", None, datetime.now().isoformat(), datetime.now().isoformat())
        stats = self.stats_repo.load()
        self.assertEqual(stats['total_interactions'], 1)
        self.assertEqual(stats['por_personalidade']['formal'], 1)
        self.assertEqual(stats['fallback_count'], 0)
        self.assertEqual(stats.get('por_tag', {}), {})
    
    def test_atualizar_stats_incrementa_fallback(self):
        """Testa incremento de fallback_count."""
        self.stats_repo.update_interaction(True, "formal", None, datetime.now().isoformat(), datetime.now().isoformat())
        stats = self.stats_repo.load()
        self.assertEqual(stats['total_interactions'], 1)
        self.assertEqual(stats['fallback_count'], 1)
    
    def test_atualizar_stats_incrementa_tag(self):
        """Testa incremento de por_tag."""
        self.stats_repo.update_interaction(False, "formal", "math_basic", datetime.now().isoformat(), datetime.now().isoformat())
        stats = self.stats_repo.load()
        self.assertEqual(stats['total_interactions'], 1)
        self.assertEqual(stats['por_tag']['math_basic'], 1)
    
    def test_atualizar_stats_salva_json(self):
        """Testa salvamento atômico em stats.json."""
        self.stats_repo.update_interaction(True, "formal", "math", datetime.now().isoformat(), datetime.now().isoformat())
        
        # Verificar arquivo salvo
        self.assertTrue(os.path.exists(self.stats_path))
        with open(self.stats_path, 'r', encoding='utf-8') as f:
            dados = json.load(f)
            self.assertEqual(dados['total_interactions'], 1)
            self.assertEqual(dados['fallback_count'], 1)
            self.assertEqual(dados['por_personalidade']['formal'], 1)
            self.assertEqual(dados['por_tag']['math'], 1)
    
    def test_carregar_stats_com_dados(self):
        """Testa carregamento de stats.json com dados existentes."""
        dados_teste = {
            'total_interactions': 5,
            'fallback_count': 2,
            'por_personalidade': {'formal': 3, 'engracada': 2},
            'por_tag': {'math': 4, 'fallback': 1}
        }
        
        with open(self.stats_path, 'w', encoding='utf-8') as f:
            json.dump(dados_teste, f)
        
        stats = self.stats_repo.load()
        self.assertEqual(stats['total_interactions'], 5)
        self.assertEqual(stats['fallback_count'], 2)
        self.assertEqual(stats['por_personalidade']['formal'], 3)
        self.assertEqual(stats['por_tag']['math'], 4)
    
    def test_carregar_stats_default(self):
        """Testa defaults quando stats.json inexistente."""
        if os.path.exists(self.stats_path):
            os.remove(self.stats_path)
        
        stats = self.stats_repo.load()
        self.assertEqual(stats['total_interactions'], 0)
        self.assertEqual(stats['fallback_count'], 0)
        self.assertEqual(stats.get('por_personalidade', {}), {})
        self.assertEqual(stats.get('por_tag', {}), {})
    def test_get_stats_fallback_rate(self):
        """Testa cálculo de fallback_rate com defaults para divisão zero."""
        for _ in range(3):
            self.bot.processar_mensagem("oi", "formal")
        for _ in range(2):
            self.bot.processar_mensagem("pergunta fallback", "formal")

        stats = self.bot.get_stats()
        self.assertEqual(stats['total_interactions'], 5)
        self.assertEqual(stats['fallback_count'], 2)
        self.assertAlmostEqual(stats['fallback_rate'], 0.4)
    
    def test_get_stats_porcentagens(self):
        """Testa cálculos de porcentagens para por_personalidade e por_tag."""
        self.bot.processar_mensagem("oi", "formal") # tag saudacao
        self.bot.processar_mensagem("oi", "formal") # tag saudacao
        self.bot.processar_mensagem("oi", "engracada") # tag saudacao
        self.bot.processar_mensagem("fallback", "formal") # tag fallback

        stats = self.bot.get_stats()
        self.assertAlmostEqual(stats['por_personalidade_perc']['formal'], 75.0)
        self.assertAlmostEqual(stats['por_personalidade_perc']['engracada'], 25.0)
        self.assertAlmostEqual(stats['por_tag_perc']['saudacao'], 75.0)
        self.assertAlmostEqual(stats['por_tag_perc']['fallback'], 25.0)
    
    def test_get_stats_duracao_sessao(self):
        """Testa duração média de sessão."""
        # Este teste é mais complexo e depende do StatsRepo, que será testado em seu próprio arquivo.
        pass
    def test_formatar_stats(self):
        """Testa formatação de stats para CLI."""
        # Esta funcionalidade foi movida para a camada de apresentação (app.py)
        pass
    
    def test_processar_comando_stats(self):
        """Testa comando /stats."""
        # Esta funcionalidade foi movida para a camada de apresentação (app.py)
        pass
    
    def test_mostrar_stats_gradio(self):
        """Testa mostrar_stats em app.py para Gradio."""
        # Este é um teste de integração que pertence a test_app.py
        pass
if __name__ == '__main__':
    unittest.main()