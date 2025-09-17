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
        # Reset stats para isolamento em cada teste
        self.bot.stats = {
            'total_interactions': 0,
            'fallback_count': 0,
            'por_personalidade': {},
            'por_tag': {}
        }
        # Reset stats para isolamento em cada teste
        self.bot.stats = {
            'total_interactions': 0,
            'fallback_count': 0,
            'por_personalidade': {},
            'por_tag': {}
        }

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

    def test_salvar_historico_novos_campos(self):
        """Testa _salvar_historico com novos campos Task 13."""
        pergunta = "Test tag"
        resposta = "Resp tag"
        personalidade = "formal"
        tag = "math_basic"
        is_fallback = True
        success = self.bot._salvar_historico(pergunta, resposta, personalidade, tag, is_fallback)
        self.assertTrue(success)
        self.assertEqual(len(self.bot.historico), 1)
        entry = self.bot.historico[0]
        self.assertIn("timestamp_in", entry)
        self.assertIn("timestamp_out", entry)
        self.assertEqual(entry["tag_intencao"], tag)
        self.assertEqual(entry["is_fallback"], is_fallback)

    def test_limpar_historico_mantem_stats(self):
        """Testa limpar histórico não afeta stats agregados."""
        # Salvar 3 interações
        for i in range(3):
            self.bot._salvar_historico(f"test{i}", f"resp{i}", "formal", None, False)
        self.assertEqual(self.bot.stats['total_interactions'], 3)
        # Limpar
        self.bot._limpar_historico()
        self.assertEqual(len(self.bot.historico), 0)
        self.assertEqual(self.bot.interacoes_count, 0)
        self.assertEqual(self.bot.stats['total_interactions'], 3)  # Agregado mantido

    def test_carregar_historico_novos_campos(self):
        """Testa carregamento com novos campos Task 13."""
        dados = [{"timestamp_in": "2023-01-01T00:00:00", "timestamp_out": "2023-01-01T00:00:01", "pergunta": "test", "resposta": "resp", "personalidade": "formal", "tag_intencao": "math", "is_fallback": True}]
        with open(self.bot.historico_path, 'w') as f:
            json.dump(dados, f)
        historico = self.bot._carregar_historico()
        self.assertEqual(len(historico), 1)
        self.assertIn("tag_intencao", historico[0])

    def test_end_to_end_interacao(self):
        """Testa fluxo end-to-end: processar mensagem, salvar, stats."""
        # Mock datetime for reproducible duration
        with patch('main.datetime', wraps=datetime) as mock_dt:
            mock_dt.now.return_value = datetime(2023,1,1,10,0)
            resposta, is_fallback, tag = self.bot.processar_mensagem("oi", "formal")
            # Para _salvar_historico: in=10:0, out=10:1
            mock_dt.now.side_effect = [datetime(2023,1,1,10,0), datetime(2023,1,1,10,1)]
            self.bot._salvar_historico("oi", resposta, "formal", tag, False)
        
        stats = self.bot.get_stats()
        self.assertEqual(stats['total_interactions'], 1)
        self.assertAlmostEqual(stats['media_duracao_sessao_min'], 1.0)

    def test_atualizar_stats_incrementa_total_e_personalidade(self):
        """Testa incremento de total_interactions e por_personalidade."""
        # Reset stats para defaults
        self.bot.stats = {
            'total_interactions': 0,
            'fallback_count': 0,
            'por_personalidade': {},
            'por_tag': {}
        }
        
        entry = {
            "personalidade": "formal",
            "is_fallback": False,
            "tag_intencao": None
        }
        
        success = self.bot._atualizar_stats(entry)
        self.assertTrue(success)
        self.assertEqual(self.bot.stats['total_interactions'], 1)
        self.assertEqual(self.bot.stats['por_personalidade']['formal'], 1)
        self.assertEqual(self.bot.stats['fallback_count'], 0)
        self.assertEqual(self.bot.stats['por_tag'], {})
    
    def test_atualizar_stats_incrementa_fallback(self):
        """Testa incremento de fallback_count."""
        self.bot.stats = {
            'total_interactions': 0,
            'fallback_count': 0,
            'por_personalidade': {},
            'por_tag': {}
        }
        
        entry = {
            "personalidade": "formal",
            "is_fallback": True,
            "tag_intencao": None
        }
        
        success = self.bot._atualizar_stats(entry)
        self.assertTrue(success)
        self.assertEqual(self.bot.stats['total_interactions'], 1)
        self.assertEqual(self.bot.stats['fallback_count'], 1)
    
    def test_atualizar_stats_incrementa_tag(self):
        """Testa incremento de por_tag."""
        self.bot.stats = {
            'total_interactions': 0,
            'fallback_count': 0,
            'por_personalidade': {},
            'por_tag': {}
        }
        
        entry = {
            "personalidade": "formal",
            "is_fallback": False,
            "tag_intencao": "math_basic"
        }
        
        success = self.bot._atualizar_stats(entry)
        self.assertTrue(success)
        self.assertEqual(self.bot.stats['total_interactions'], 1)
        self.assertEqual(self.bot.stats['por_tag']['math_basic'], 1)
    
    def test_atualizar_stats_salva_json(self):
        """Testa salvamento atômico em stats.json."""
        # Usar temp para stats_path
        original_stats_path = self.bot.stats_path
        temp_stats_path = os.path.join(self.temp_dir, 'stats_temp.json')
        self.bot.stats_path = temp_stats_path
        
        self.bot.stats = {
            'total_interactions': 0,
            'fallback_count': 0,
            'por_personalidade': {},
            'por_tag': {}
        }
        
        entry = {
            "personalidade": "formal",
            "is_fallback": True,
            "tag_intencao": "math"
        }
        
        success = self.bot._atualizar_stats(entry)
        self.assertTrue(success)
        
        # Verificar arquivo salvo
        self.assertTrue(os.path.exists(temp_stats_path))
        with open(temp_stats_path, 'r', encoding='utf-8') as f:
            dados = json.load(f)
            self.assertEqual(dados['total_interactions'], 1)
            self.assertEqual(dados['fallback_count'], 1)
            self.assertEqual(dados['por_personalidade']['formal'], 1)
            self.assertEqual(dados['por_tag']['math'], 1)
        
        # Cleanup
        if os.path.exists(temp_stats_path):
            os.remove(temp_stats_path)
        self.bot.stats_path = original_stats_path
    
    def test_carregar_stats_com_dados(self):
        """Testa carregamento de stats.json com dados existentes."""
        # Criar arquivo temp com dados
        temp_stats_path = os.path.join(self.temp_dir, 'stats_temp.json')
        dados_teste = {
            'total_interactions': 5,
            'fallback_count': 2,
            'por_personalidade': {'formal': 3, 'engracada': 2},
            'por_tag': {'math': 4, 'fallback': 1}
        }
        
        with open(temp_stats_path, 'w', encoding='utf-8') as f:
            json.dump(dados_teste, f)
        
        original_stats_path = self.bot.stats_path
        self.bot.stats_path = temp_stats_path
        
        stats = self.bot._carregar_stats()
        self.assertEqual(stats['total_interactions'], 5)
        self.assertEqual(stats['fallback_count'], 2)
        self.assertEqual(stats['por_personalidade']['formal'], 3)
        self.assertEqual(stats['por_tag']['math'], 4)
        
        # Cleanup
        if os.path.exists(temp_stats_path):
            os.remove(temp_stats_path)
        self.bot.stats_path = original_stats_path
    
    def test_carregar_stats_default(self):
        """Testa defaults quando stats.json inexistente."""
        # Remover se existir
        if os.path.exists(self.bot.stats_path):
            os.remove(self.bot.stats_path)
        
        stats = self.bot._carregar_stats()
        self.assertEqual(stats['total_interactions'], 0)
        self.assertEqual(stats['fallback_count'], 0)
        self.assertEqual(stats['por_personalidade'], {})
        self.assertEqual(stats['por_tag'], {})
    def test_get_stats_fallback_rate(self):
        """Testa cálculo de fallback_rate com defaults para divisão zero."""
        # Setup com 5 interações, 2 fallbacks
        self.bot.stats = {
            'total_interactions': 5,
            'fallback_count': 2,
            'por_personalidade': {},
            'por_tag': {}
        }
        
        stats = self.bot.get_stats()
        self.assertEqual(stats['total_interactions'], 5)
        self.assertEqual(stats['fallback_count'], 2)
        self.assertEqual(stats['fallback_rate'], 0.4)
        
        # Edge: total=0, fallback=0
        self.bot.stats['total_interactions'] = 0
        self.bot.stats['fallback_count'] = 0
        stats = self.bot.get_stats()
        self.assertEqual(stats['fallback_rate'], 0.0)
    
    def test_get_stats_porcentagens(self):
        """Testa cálculos de porcentagens para por_personalidade e por_tag, com edge totais 0."""
        self.bot.stats = {
            'total_interactions': 4,
            'fallback_count': 0,
            'por_personalidade': {'formal': 2, 'engracada': 2},
            'por_tag': {'math': 3, 'fallback': 1}
        }
        
        stats = self.bot.get_stats()
        self.assertEqual(stats['por_personalidade_perc']['formal'], 50.0)
        self.assertEqual(stats['por_personalidade_perc']['engracada'], 50.0)
        self.assertEqual(stats['por_tag_perc']['math'], 75.0)
        self.assertEqual(stats['por_tag_perc']['fallback'], 25.0)
        
        # Edge: por_personalidade vazio
        self.bot.stats['por_personalidade'] = {}
        stats = self.bot.get_stats()
        self.assertEqual(stats['por_personalidade_perc'], {})
    
    def test_get_stats_duracao_sessao(self):
        """Testa duração média de sessão: agrupa <5min, média (out_last - in_first)/60."""
        # Reset histórico
        self.bot.historico = []
        
        # Mock times: sessão1 (3 interações <5min total 2min), sessão2 (1 interação 1min)
        mock_times_in = [
            datetime(2023, 1, 1, 10, 0, 0),   # in1
            datetime(2023, 1, 1, 10, 0, 30),  # in2 (<5min)
            datetime(2023, 1, 1, 10, 1, 30),  # in3 (<5min)
            datetime(2023, 1, 1, 10, 8, 0)    # in4 (>5min from out3 10:2:30)
        ]
        mock_times_out = [
            datetime(2023, 1, 1, 10, 0, 30),  # out1
            datetime(2023, 1, 1, 10, 1, 30),  # out2
            datetime(2023, 1, 1, 10, 2, 30),  # out3 (delta to in4 10:8:0 =5.5min >5)
            datetime(2023, 1, 1, 10, 9, 0)    # out4 (1min session)
        ]
        
        with patch('main.datetime') as mock_dt:
            # Sequence for 4 saves: in, out for each (8 calls)
            times_sequence = [
                mock_times_in[0], mock_times_out[0],  # save1
                mock_times_in[1], mock_times_out[1],  # save2
                mock_times_in[2], mock_times_out[2],  # save3
                mock_times_in[3], mock_times_out[3]   # save4
            ]
            mock_dt.now.side_effect = times_sequence
            
            # Salvar 4 interações
            self.bot._salvar_historico("p1", "r1", "formal", "math", False)
            self.bot._salvar_historico("p2", "r2", "formal", "math", False)
            self.bot._salvar_historico("p3", "r3", "formal", None, False)
            self.bot._salvar_historico("p4", "r4", "engracada", None, True)
        
        stats = self.bot.get_stats()
        # Sessão1: in1 10:00 to out3 10:02:30 = 2.5min
        # Sessão2: in4 10:08 to out4 10:09 = 1min
        # Média: (2.5 + 1)/2 = 1.75min
        self.assertAlmostEqual(stats['media_duracao_sessao_min'], 1.75)
        
        # Histórico vazio
        self.bot.historico = []
        stats = self.bot.get_stats()
        self.assertEqual(stats['media_duracao_sessao_min'], 0.0)
    def test_formatar_stats(self):
        """Testa formatação de _formatar_stats para CLI."""
        # Setup stats simples
        self.bot.stats = {
            'total_interactions': 5,
            'fallback_count': 2,
            'por_personalidade': {'formal': 3, 'engracada': 2},
            'por_tag': {'math': 4, 'fallback': 1}
        }
        
        # Mock get_stats para retornar valores computados fixos (evita dependência de histórico/duração)
        mock_stats = {
            'total_interactions': 5,
            'fallback_count': 2,
            'fallback_rate': 0.4,
            'por_personalidade': {'formal': 3, 'engracada': 2},
            'por_personalidade_perc': {'formal': 60.0, 'engracada': 40.0},
            'por_tag': {'math': 4, 'fallback': 1},
            'por_tag_perc': {'math': 80.0, 'fallback': 20.0},
            'media_duracao_sessao_min': 2.5
        }
        with patch.object(self.bot, 'get_stats', return_value=mock_stats):
            formatted = self.bot._formatar_stats()
        
        self.assertIn("📊 ESTATÍSTICAS DO CHATBOT 📊", formatted)
        self.assertIn("Total de Interações: 5", formatted)
        self.assertIn("Taxa de Fallback: 40.0%", formatted)
        self.assertIn("Duração Média de Sessão: 2.5 minutos", formatted)
        self.assertIn("Por Personalidade:", formatted)
        self.assertIn("Formal: 3 (60.0%)", formatted)
        self.assertIn("Engracada: 2 (40.0%)", formatted)
        self.assertIn("Por Tag de Intenção:", formatted)
        self.assertIn("math: 4 (80.0%)", formatted)
        self.assertIn("fallback: 1 (20.0%)", formatted)
        self.assertIn("=", formatted)  # Verifica separadores
    
    def test_processar_comando_stats(self):
        """Testa comando /stats em _processar_comando_especial."""
        # Mock get_stats para ambos testes
        mock_stats = {
            'total_interactions': 5,
            'fallback_count': 2,
            'fallback_rate': 0.4,
            'por_personalidade': {'formal': 3, 'engracada': 2},
            'por_personalidade_perc': {'formal': 60.0, 'engracada': 40.0},
            'por_tag': {'math': 4, 'fallback': 1},
            'por_tag_perc': {'math': 80.0, 'fallback': 20.0},
            'media_duracao_sessao_min': 2.5
        }
        with patch.object(self.bot, 'get_stats', return_value=mock_stats):
            is_comando, response = self.bot._processar_comando_especial("/stats")
        
            self.assertTrue(is_comando)
            self.assertIn("📊 ESTATÍSTICAS DO CHATBOT 📊", response)
            self.assertIn("Total de Interações: 5", response)
            self.assertIn("Taxa de Fallback: 40.0%", response)
            
            # Edge: /stats com args extras (deve ignorar e retornar mesmo)
            is_comando, response = self.bot._processar_comando_especial("/stats extra")
            self.assertTrue(is_comando)
            self.assertIn("Total de Interações: 5", response)
    
    def test_mostrar_stats_gradio(self):
        """Testa mostrar_stats em app.py para Gradio, formatação básica."""
        from app import mostrar_stats, aline_bot
        personalidade = "formal"
        
        mock_stats = {
            'total_interactions': 5,
            'fallback_count': 2,
            'fallback_rate': 0.4,
            'por_personalidade': {'formal': 3},
            'por_personalidade_perc': {'formal': 60.0},
            'por_tag': {'math': 4},
            'por_tag_perc': {'math': 80.0},
            'media_duracao_sessao_min': 2.5
        }
        with patch.object(aline_bot, 'get_stats', return_value=mock_stats):
            output = mostrar_stats(personalidade, [], {})
        
        self.assertIn("📊 ESTATÍSTICAS ATUAIS (Personalidade: Formal)", output)
        self.assertIn("Total de Interações: 5", output)
        self.assertIn("Taxa de Fallback: 40.0%", output)
        self.assertIn("Duração Média de Sessão: 2.5 min", output)
        self.assertIn("Por Personalidade:", output)
        self.assertIn("Por Tag:", output)
if __name__ == '__main__':
    unittest.main()