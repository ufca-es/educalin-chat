import unittest
import os
import json
from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock

# Adiciona o diretório raiz ao sys.path para permitir importações de módulos do projeto
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from infra.repositories import StatsRepo
from core.chatbot import Chatbot

class TestStatsAndSessions(unittest.TestCase):

    def setUp(self):
        """Configura um ambiente de teste limpo antes de cada teste."""
        self.stats_file = "data/test_stats.json"
        self.history_file = "data/test_history.json"
        self.logger = MagicMock()
        
        # Garante que os arquivos de teste não existam no início
        if os.path.exists(self.stats_file):
            os.remove(self.stats_file)
        if os.path.exists(self.history_file):
            os.remove(self.history_file)

    def tearDown(self):
        """Limpa o ambiente de teste após cada teste."""
        if os.path.exists(self.stats_file):
            os.remove(self.stats_file)
        if os.path.exists(self.history_file):
            os.remove(self.history_file)

    def test_01_primeira_interacao_cria_sessao(self):
        """Verifica se a primeira interação cria corretamente a primeira sessão."""
        stats_repo = StatsRepo(self.stats_file, logger=self.logger)
        
        ts_in = datetime.now(timezone.utc)
        ts_out = ts_in + timedelta(seconds=10)
        
        stats_repo.update_interaction(
            is_fallback=False,
            personalidade="formal",
            tag="saudacao",
            timestamp_in=ts_in.isoformat(),
            timestamp_out=ts_out.isoformat()
        )
        
        data = stats_repo.load()
        self.assertEqual(len(data["sessoes"]), 1)
        self.assertIn("1", data["sessoes"])
        self.assertAlmostEqual(data["sessoes"]["1"]["duracao_seg"], 10, delta=0.1)
        self.assertEqual(data["sessoes"]["1"]["num_interacoes"], 1)
        self.assertEqual(data["total_interactions"], 1)

    def test_02_interacao_curta_continua_sessao(self):
        """Verifica se uma interação dentro do timeout continua a mesma sessão."""
        stats_repo = StatsRepo(self.stats_file, logger=self.logger)
        
        # Primeira interação
        ts1_in = datetime.now(timezone.utc)
        ts1_out = ts1_in + timedelta(seconds=15)
        stats_repo.update_interaction(False, "formal", "saudacao", ts1_in.isoformat(), ts1_out.isoformat())
        
        # Segunda interação (5 minutos depois)
        ts2_in = ts1_out + timedelta(minutes=5)
        ts2_out = ts2_in + timedelta(seconds=20)
        stats_repo.update_interaction(False, "formal", "despedida", ts2_in.isoformat(), ts2_out.isoformat())
        
        data = stats_repo.load()
        self.assertEqual(len(data["sessoes"]), 1)
        self.assertEqual(data["sessoes"]["1"]["num_interacoes"], 2)
        self.assertAlmostEqual(data["sessoes"]["1"]["duracao_seg"], 35, delta=0.1) # 15 + 20
        self.assertEqual(data["total_interactions"], 2)

    def test_03_interacao_longa_cria_nova_sessao(self):
        """Verifica se uma interação após o timeout cria uma nova sessão."""
        stats_repo = StatsRepo(self.stats_file, logger=self.logger)
        
        # Primeira interação
        ts1_in = datetime.now(timezone.utc)
        ts1_out = ts1_in + timedelta(seconds=10)
        stats_repo.update_interaction(False, "formal", "saudacao", ts1_in.isoformat(), ts1_out.isoformat())
        
        # Segunda interação (45 minutos depois - timeout é 30)
        ts2_in = ts1_out + timedelta(minutes=45)
        ts2_out = ts2_in + timedelta(seconds=5)
        stats_repo.update_interaction(True, "engracada", "fallback", ts2_in.isoformat(), ts2_out.isoformat())
        
        data = stats_repo.load()
        self.assertEqual(len(data["sessoes"]), 2)
        self.assertIn("1", data["sessoes"])
        self.assertIn("2", data["sessoes"])
        self.assertEqual(data["sessoes"]["1"]["num_interacoes"], 1)
        self.assertEqual(data["sessoes"]["2"]["num_interacoes"], 1)
        self.assertAlmostEqual(data["sessoes"]["2"]["duracao_seg"], 5, delta=0.1)
        self.assertEqual(data["total_interactions"], 2)
        self.assertEqual(data["fallback_count"], 1)

    def test_04_integracao_chatbot_get_stats(self):
        """Testa a integração completa e o cálculo da média de duração no Chatbot."""
        # Mocks para as dependências do Chatbot
        matcher_mock = MagicMock()
        learned_repo_mock = MagicMock()
        history_repo_mock = MagicMock()
        
        # Configura o matcher para retornar uma intenção válida
        matcher_mock.match.return_value = {
            "tipo": "intent",
            "intencao": {
                "tag": "teste_intencao",
                "respostas": {"formal": ["resposta de teste"]}
            }
        }

        chatbot = Chatbot(
            matcher=matcher_mock,
            learned_repo=learned_repo_mock,
            history_repo=history_repo_mock,
            logger=self.logger
        )
        # Substitui o stats_repo padrão por um que usa nosso arquivo de teste
        chatbot.stats_repo = StatsRepo(self.stats_file, logger=self.logger)

        # Simula 3 interações em 2 sessões
        # Sessão 1
        chatbot.processar_mensagem("pergunta 1", "formal")
        # Sessão 2 (simulando que o tempo passou)
        # Para simular, vamos manipular o arquivo de stats diretamente
        stats_data = chatbot.stats_repo.load()
        last_ts_out_str = stats_data["sessoes"]["1"]["fim"]
        last_ts_out = datetime.fromisoformat(last_ts_out_str)
        new_ts_in = last_ts_out + timedelta(minutes=40)
        new_ts_out = new_ts_in + timedelta(seconds=5)
        
        # Atualizamos a interação manualmente para forçar o timestamp
        chatbot.stats_repo.update_interaction(False, "formal", "teste_intencao", new_ts_in.isoformat(), new_ts_out.isoformat())

        stats = chatbot.get_stats()
        
        self.assertEqual(stats["num_sessoes"], 2)
        self.assertGreater(stats["media_duracao_sessao_min"], 0)
        
        # Validação do cálculo da média
        final_data = chatbot.stats_repo.load()
        duracao_total = final_data["total_duracao_sessoes_seg"]
        media_esperada_min = (duracao_total / 2) / 60
        self.assertAlmostEqual(stats["media_duracao_sessao_min"], media_esperada_min, places=5)

if __name__ == '__main__':
    unittest.main()