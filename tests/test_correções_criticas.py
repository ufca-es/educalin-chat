#!/usr/bin/env python3
"""
Testes unitários específicos para validar correções UAT-009 e UAT-015
Foco em casos extremos e cenários de falha identificados no UAT
"""

import unittest
import tempfile
import os
import json
import shutil
from unittest.mock import patch, mock_open
from infra.repositories import CoreRepo, LearnedRepo, HistoryRepo
from infra.logging_conf import get_logger
from core.intent_matcher import IntentMatcher
from infra.repositories import CoreRepo, LearnedRepo, HistoryRepo
from infra.logging_conf import get_logger
from core.intent_matcher import IntentMatcher
from core.chatbot import Chatbot

class TestUAT009CorrecaoEncoding(unittest.TestCase):
    """Testes específicos para correção da Issue UAT-009"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.core_data_file = os.path.join(self.temp_dir, 'core_test.json')
        self.new_data_file = os.path.join(self.temp_dir, 'new_test.json')
        
        # Criar arquivo core_data mínimo
        core_data = {
            "intencoes": [
                {"tag": "fallback", "perguntas": [], "respostas": {"formal": "Não entendi"}}
            ]
        }
        
        with open(self.core_data_file, 'w', encoding='utf-8') as f:
            json.dump(core_data, f, ensure_ascii=False)
            
        self.logger = get_logger("test_correcoes_criticas")
        self.core_repo = CoreRepo(self.core_data_file, logger=self.logger)
        self.learned_repo = LearnedRepo(self.new_data_file, logger=self.logger)
        self.history_repo = HistoryRepo(os.path.join(self.temp_dir, 'history_test.json'), logger=self.logger)
        self.intent_matcher = IntentMatcher(intencoes=self.core_repo.load_intents(), aprendidos=self.learned_repo.load(), logger=self.logger)
        self.bot = Chatbot(matcher=self.intent_matcher, learned_repo=self.learned_repo, history_repo=self.history_repo, logger=self.logger)
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_caracteres_especiais_portugues(self):
        """🚨 TESTE CRÍTICO: Salvar caracteres especiais do português"""
        pergunta = "Equação com acentuação: çãõáéíóúÇÃÕÁÉÍÓÚ"
        resposta = "Resposta também com acentos: não, coração, educação"
        
        resultado = self.bot.ensinar_nova_resposta(pergunta, resposta)
        self.assertTrue(resultado, "Falha ao salvar caracteres especiais portugueses")
        
        # Verificar integridade completa do arquivo
        with open(self.new_data_file, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        
        self.assertEqual(len(dados), 1)
        self.assertEqual(dados[0]["pergunta"], pergunta)
        self.assertEqual(dados[0]["resposta_ensinada"], resposta)
    
    def test_arquivo_corrompido_sem_colchete_fechamento(self):
        """🚨 TESTE CRÍTICO: Simular exatamente o problema do UAT-009"""
        # Criar arquivo corrompido exatamente como no UAT-009
        conteudo_corrompido = '''[
  {
    "pergunta": "teste anterior",
    "resposta_ensinada": "resposta anterior"
  },
  {
    "pergunta": "pergunta sem fechamento"'''
        
        with open(self.new_data_file, 'w', encoding='utf-8') as f:
            f.write(conteudo_corrompido)
        
        # Tentar salvar nova entrada
        resultado = self.bot.ensinar_nova_resposta("nova pergunta", "nova resposta")
        self.assertTrue(resultado, "Sistema não conseguiu se recuperar de arquivo corrompido")
        
        # Verificar que arquivo foi recriado corretamente
        with open(self.new_data_file, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        
        # Deve ter apenas a nova entrada (arquivo foi recriado)
        self.assertEqual(len(dados), 1)
        self.assertEqual(dados[0]["pergunta"], "nova pergunta")
    
    def test_simulacao_interrupcao_escrita(self):
        """🚨 TESTE CRÍTICO: Simular falha durante escrita"""
        # Primeiro, estabelecer estado inicial válido
        self.bot.ensinar_nova_resposta("pergunta inicial", "resposta inicial")
        
        # Simular falha durante escrita usando mock
        with patch('builtins.open', side_effect=IOError("Disco cheio simulado")):
            resultado = self.bot.ensinar_nova_resposta("pergunta problema", "resposta problema")
            self.assertFalse(resultado, "Sistema deveria ter falhado com disco cheio")
        
        # Verificar que dados originais foram preservados
        with open(self.new_data_file, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        
        self.assertEqual(len(dados), 1)
        self.assertEqual(dados[0]["pergunta"], "pergunta inicial")
    
    def test_validacao_caracteres_controle_maliciosos(self):
        """🚨 TESTE CRÍTICO: Rejeitar caracteres que podem corromper JSON"""
        caracteres_perigosos = [
            "pergunta com \x00 null byte",
            "pergunta com \x01 start of heading", 
            "pergunta com \x02 start of text",
            "pergunta com \x1b[31m ANSI escape",
            "\x00\x01\x02pergunta toda corrompida"
        ]
        
        for pergunta_perigosa in caracteres_perigosos:
            resultado = self.bot.ensinar_nova_resposta(pergunta_perigosa, "resposta")
            self.assertFalse(resultado, f"Sistema aceitou entrada perigosa: {repr(pergunta_perigosa)}")
    
    def test_entrada_muito_longa_dos_attack(self):
        """🚨 TESTE CRÍTICO: Prevenir ataques DoS com entradas muito longas"""
        pergunta_gigante = "a" * 1001  # Acima do limite de 1000
        resposta_gigante = "b" * 1001
        
        resultado_pergunta = self.bot.ensinar_nova_resposta(pergunta_gigante, "resposta normal")
        resultado_resposta = self.bot.ensinar_nova_resposta("pergunta normal", resposta_gigante)
        
        self.assertFalse(resultado_pergunta, "Sistema aceitou pergunta muito longa")
        self.assertFalse(resultado_resposta, "Sistema aceitou resposta muito longa")

class TestUAT015CorrecaoThreshold(unittest.TestCase):
    """Testes específicos para correção da Issue UAT-015"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.core_data_file = os.path.join(self.temp_dir, 'core_test.json')
        self.new_data_file = os.path.join(self.temp_dir, 'new_test.json')
        
        # Core data com intenção de teste
        core_data = {
            "intencoes": [
                {
                    "tag": "teste", 
                    "perguntas": ["pergunta teste base"], 
                    "respostas": {"formal": "resposta base"}
                },
                {
                    "tag": "fallback", 
                    "perguntas": [], 
                    "respostas": {"formal": "Não entendi"}
                }
            ]
        }
        
        with open(self.core_data_file, 'w', encoding='utf-8') as f:
            json.dump(core_data, f, ensure_ascii=False)
            
        self.logger = get_logger("test_correcoes_criticas")
        self.core_repo = CoreRepo(self.core_data_file, logger=self.logger)
        self.learned_repo = LearnedRepo(self.new_data_file, logger=self.logger)
        self.history_repo = HistoryRepo(os.path.join(self.temp_dir, 'history_test.json'), logger=self.logger)
        self.intent_matcher = IntentMatcher(intencoes=self.core_repo.load_intents(), aprendidos=self.learned_repo.load(), logger=self.logger)
        self.bot = Chatbot(matcher=self.intent_matcher, learned_repo=self.learned_repo, history_repo=self.history_repo, logger=self.logger)
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_cenario_exato_uat015(self):
        """🚨 TESTE CRÍTICO: Reproduzir exatamente o cenário UAT-015"""
        # Ensinar resposta específica
        self.bot.ensinar_nova_resposta("pergunta1_UAT015", "resposta1_UAT015")
        
        # Testar as outras 4 perguntas que estavam retornando incorretamente a mesma resposta
        perguntas_diferentes = [
            "pergunta2_UAT015",
            "pergunta3_UAT015", 
            "pergunta4_UAT015",
            "pergunta5_UAT015"
        ]
        
        for pergunta in perguntas_diferentes:
            resposta, is_fallback, _ = self.bot.processar_mensagem(pergunta, "formal")
            
            # Com threshold corrigido, deve ativar fallback
            self.assertTrue(is_fallback, f"Pergunta '{pergunta}' não ativou fallback como deveria")
            self.assertNotIn("resposta1_UAT015", resposta, f"Pergunta '{pergunta}' retornou resposta incorreta")
            self.assertTrue(len(resposta) > 0, f"Pergunta '{pergunta}' não retornou fallback apropriado")
    
    def test_threshold_rigoroso_intenções_base(self):
        """🚨 TESTE CRÍTICO: Verificar threshold 0.8 para intenções base"""
        # Pergunta base: "pergunta teste base"
        perguntas_similares_mas_diferentes = [
            "pergunta teste diferente",     # ~0.7 similaridade - deve dar fallback
            "pergunta nova base",           # ~0.6 similaridade - deve dar fallback  
            "questão teste base",           # ~0.7 similaridade - deve dar fallback
        ]
        
        for pergunta in perguntas_similares_mas_diferentes:
            resposta, is_fallback, _ = self.bot.processar_mensagem(pergunta, "formal")
            self.assertTrue(is_fallback, f"Pergunta '{pergunta}' não ativou fallback com threshold 0.8")
    
    def test_busca_exata_tem_prioridade(self):
        """🚨 TESTE CRÍTICO: Busca exata deve ter prioridade sobre fuzzy"""
        # Ensinar resposta exata
        self.bot.ensinar_nova_resposta("pergunta exata especial", "resposta exata especial")
        
        # Busca exata deve sempre retornar a resposta correta
        resposta, is_fallback, _ = self.bot.processar_mensagem("pergunta exata especial", "formal")
        
        self.assertFalse(is_fallback, "Correspondência exata foi incorretamente tratada como fallback")
        self.assertIn("resposta exata especial", resposta, "Busca exata não retornou resposta correta")
    
    def test_threshold_muito_rigoroso_aprendidos(self):
        """🚨 TESTE CRÍTICO: Threshold 0.9 para dados aprendidos"""
        # Ensinar resposta específica
        self.bot.ensinar_nova_resposta("pergunta aprendida especifica", "resposta aprendida especifica")
        
        # Perguntas com similaridade entre 0.7-0.8 que antes dariam match
        perguntas_quase_similares = [
            "pergunta aprendida diferente",   # ~0.8 similaridade
            "questão aprendida especifica",   # ~0.8 similaridade
            "pergunta nova especifica",       # ~0.7 similaridade
        ]
        
        for pergunta in perguntas_quase_similares:
            resposta, is_fallback, _ = self.bot.processar_mensagem(pergunta, "formal")
            
            # Com threshold 0.9, deve ativar fallback
            self.assertTrue(is_fallback, f"Pergunta '{pergunta}' não ativou fallback com threshold 0.9")
            self.assertNotIn("resposta aprendida especifica", resposta, f"Pergunta '{pergunta}' retornou resposta incorreta")

class TestValidacaoCompleta(unittest.TestCase):
    """Testes de validação completa das correções"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.core_data_file = os.path.join(self.temp_dir, 'core_test.json')
        self.new_data_file = os.path.join(self.temp_dir, 'new_test.json')
        
        # Core data completo para testes
        core_data = {
            "intencoes": [
                {
                    "tag": "saudacao",
                    "perguntas": ["oi", "olá", "bom dia"],
                    "respostas": {"formal": "Olá. Como posso ajudar?"}
                },
                {
                    "tag": "fallback",
                    "perguntas": [],
                    "respostas": {"formal": "Não compreendi a sua solicitação."}
                }
            ]
        }
        
        with open(self.core_data_file, 'w', encoding='utf-8') as f:
            json.dump(core_data, f, ensure_ascii=False)
            
        self.logger = get_logger("test_correcoes_criticas")
        self.core_repo = CoreRepo(self.core_data_file, logger=self.logger)
        self.learned_repo = LearnedRepo(self.new_data_file, logger=self.logger)
        self.history_repo = HistoryRepo(os.path.join(self.temp_dir, 'history_test.json'), logger=self.logger)
        self.intent_matcher = IntentMatcher(intencoes=self.core_repo.load_intents(), aprendidos=self.learned_repo.load(), logger=self.logger)
        self.bot = Chatbot(matcher=self.intent_matcher, learned_repo=self.learned_repo, history_repo=self.history_repo, logger=self.logger)
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_fluxo_completo_sem_regressao(self):
        """🚨 TESTE CRÍTICO: Verificar que correções não quebram funcionalidade existente"""
        # 1. Teste saudação normal
        resposta, is_fallback, _ = self.bot.processar_mensagem("oi", "formal")
        self.assertFalse(is_fallback, "Saudação normal não deveria ser fallback")
        self.assertIn("Olá", resposta, "Saudação não retornou resposta correta")
        
        # 2. Teste aprendizado
        resultado = self.bot.ensinar_nova_resposta("como calcular MDC", "Use fatoração em números primos")
        self.assertTrue(resultado, "Aprendizado não funcionou")
        
        # 3. Teste recuperação de resposta aprendida
        resposta_aprendida, is_fallback_aprendida, _ = self.bot.processar_mensagem("como calcular MDC", "formal")
        self.assertFalse(is_fallback_aprendida, "Resposta aprendida não foi reconhecida")
        self.assertIn("fatoração", resposta_aprendida, "Resposta aprendida não foi retornada")
        
        # 4. Teste fallback para pergunta desconhecida
        resposta_fallback, is_fallback_real, _ = self.bot.processar_mensagem("pergunta totalmente aleatória", "formal")
        self.assertTrue(is_fallback_real, "Fallback não foi ativado para pergunta desconhecida")
        self.assertTrue(len(resposta_fallback) > 0, "Mensagem de fallback incorreta")

if __name__ == '__main__':
    # Executar apenas testes críticos relacionados às correções
    suite = unittest.TestSuite()
    
    # Adicionar testes UAT-009
    suite.addTest(TestUAT009CorrecaoEncoding('test_caracteres_especiais_portugues'))
    suite.addTest(TestUAT009CorrecaoEncoding('test_arquivo_corrompido_sem_colchete_fechamento'))
    suite.addTest(TestUAT009CorrecaoEncoding('test_simulacao_interrupcao_escrita'))
    suite.addTest(TestUAT009CorrecaoEncoding('test_validacao_caracteres_controle_maliciosos'))
    suite.addTest(TestUAT009CorrecaoEncoding('test_entrada_muito_longa_dos_attack'))
    
    # Adicionar testes UAT-015
    suite.addTest(TestUAT015CorrecaoThreshold('test_cenario_exato_uat015'))
    suite.addTest(TestUAT015CorrecaoThreshold('test_threshold_rigoroso_intenções_base'))
    suite.addTest(TestUAT015CorrecaoThreshold('test_busca_exata_tem_prioridade'))
    suite.addTest(TestUAT015CorrecaoThreshold('test_threshold_muito_rigoroso_aprendidos'))
    
    # Adicionar teste de validação completa
    suite.addTest(TestValidacaoCompleta('test_fluxo_completo_sem_regressao'))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "="*60)
    if result.wasSuccessful():
        print("✅ TODAS AS CORREÇÕES VALIDADAS COM SUCESSO!")
        print("🎯 Issues UAT-009 e UAT-015 foram resolvidas completamente")
        print(f"📊 Testes executados: {result.testsRun}")
        print(f"📊 Falhas: {len(result.failures)}")
        print(f"📊 Erros: {len(result.errors)}")
        print("\n🚀 Sistema pronto para novo UAT com expectativa de ≥95% aprovação!")
    else:
        print("❌ ALGUMAS CORREÇÕES FALHARAM!")
        print("📋 Revisar implementação antes de submeter para novo UAT")
        print(f"📊 Testes executados: {result.testsRun}")
        print(f"📊 Falhas: {len(result.failures)}")
        print(f"📊 Erros: {len(result.errors)}")
        
        if result.failures:
            print("\n💥 FALHAS:")
            for test, traceback in result.failures:
                print(f"   • {test}: {traceback}")
        
        if result.errors:
            print("\n🔥 ERROS:")
            for test, traceback in result.errors:
                print(f"   • {test}: {traceback}")