#!/usr/bin/env python3
"""
Teste específico para validar a correção da Issue Crítica #01
String matching frágil no app.py

Este teste verifica se:
1. A detecção de fallback funciona corretamente para todas as personalidades
2. O sistema de aprendizado é ativado quando deveria
3. A interface CLI continua funcionando
4. A funcionalidade de ensino via Gradio funciona
"""

import unittest
import sys
import os

# Adicionar diretório raiz ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from infra.repositories import CoreRepo, LearnedRepo, HistoryRepo
from infra.logging_conf import get_logger
from core.intent_matcher import IntentMatcher
from core.chatbot import Chatbot
from app import enviar_mensagem, ensinar_resposta

class TestIssueCorrecao(unittest.TestCase):
    """Testes para validar a correção da Issue Crítica #01"""
    
    def setUp(self):
        """Configuração inicial dos testes"""
        self.logger = get_logger("test_issue_critica_01")
        self.core_repo = CoreRepo('data/core_data.json', logger=self.logger)
        self.learned_repo = LearnedRepo('data/new_data.json', logger=self.logger)
        self.history_repo = HistoryRepo('data/historico.json', logger=self.logger)
        self.intent_matcher = IntentMatcher(intencoes=self.core_repo.load_intents(), aprendidos=self.learned_repo.load(), logger=self.logger)
        self.bot = Chatbot(matcher=self.intent_matcher, learned_repo=self.learned_repo, history_repo=self.history_repo, logger=self.logger)
    
    def test_fallback_detection_todas_personalidades(self):
        """Verifica detecção de fallback para todas as personalidades"""
        personalities = ["formal", "engracada", "desafiadora", "empatica"]
        pergunta_inexistente = "pergunta totalmente inexistente para teste"
        
        for personality in personalities:
            with self.subTest(personality=personality):
                resposta, is_fallback, _ = self.bot.processar_mensagem(pergunta_inexistente, personality)
                
                # Verifica que fallback foi detectado
                self.assertTrue(is_fallback, f"Fallback não foi detectado para personalidade {personality}")
                
                # Verifica que resposta não está vazia
                self.assertTrue(len(resposta) > 0, f"Resposta vazia para personalidade {personality}")
                
                # Verifica que resposta é apropriada para a personalidade
                if personality == "formal":
                    self.assertIn("Não compreendi", resposta)
                elif personality == "engracada":
                    self.assertIn("passou batido", resposta)
                elif personality == "desafiadora":
                    self.assertIn("não está clara", resposta)
                elif personality == "empatica":
                    self.assertIn("não entendi bem", resposta)

    def test_resposta_normal_nao_eh_fallback(self):
        """Verifica que respostas normais não são detectadas como fallback"""
        personalities = ["formal", "engracada", "desafiadora", "empatica"]
        
        for personality in personalities:
            with self.subTest(personality=personality):
                resposta, is_fallback, _ = self.bot.processar_mensagem("oi", personality)
                
                # Resposta normal não deve ser fallback
                self.assertFalse(is_fallback, f"Resposta normal detectada como fallback para {personality}")
                
                # Deve conter saudação (diferentes formatos por personalidade)
                saudacoes_validas = ["olá", "oi", "e aí"]
                tem_saudacao = any(saudacao in resposta.lower() for saudacao in saudacoes_validas)
                self.assertTrue(tem_saudacao, f"Nenhuma saudação encontrada na resposta para {personality}: {resposta}")

    def test_gradio_learning_flow_completo(self):
        """Verifica fluxo completo de aprendizado via Gradio"""
        import time
        # Usar timestamp para garantir pergunta única
        pergunta_nova = f"pergunta única para teste {int(time.time() * 1000)}"
        personalidade = "formal"
        
        # 1. Enviar pergunta inexistente
        chat, state, _ = enviar_mensagem(pergunta_nova, personalidade, [], None)
        
        # 2. Verificar se modo de ensino foi ativado (FALHA ANTES DA CORREÇÃO!)
        self.assertTrue(state["awaiting_teach"], "Modo de ensino não foi ativado!")
        self.assertEqual(state["last_question"], pergunta_nova, "Pergunta não foi salva corretamente")
        
        # 3. Verificar se mensagem de ensino foi adicionada
        last_message = chat[-1]["content"]
        self.assertIn("Você pode me ensinar", last_message, "Mensagem de ensino não foi adicionada")
        
        # 4. Ensinar resposta
        resposta_ensinada = "Esta é uma resposta de teste ensinada"
        chat, state, _ = ensinar_resposta(resposta_ensinada, personalidade, chat, state)
        
        # 5. Verificar se resposta foi aceita
        self.assertFalse(state["awaiting_teach"], "Modo de ensino não foi desativado")
        self.assertIsNone(state["last_question"], "Pergunta não foi limpa após ensino")
        
        # 6. Testar se resposta é retornada em nova consulta
        chat_novo, state_novo, _ = enviar_mensagem(pergunta_nova, personalidade, [], None)
        ultima_resposta = chat_novo[-1]["content"]
        
        # A resposta ensinada deve aparecer
        self.assertIn(resposta_ensinada, ultima_resposta, "Resposta ensinada não foi salva/recuperada")
        
        # E não deve ser fallback
        self.assertFalse(state_novo["awaiting_teach"], "Resposta aprendida sendo tratada como fallback")

    def test_compatibilidade_cli(self):
        """Verifica que a interface CLI continua funcionando após correção"""
        # Teste resposta normal
        resposta_normal, _, _ = self.bot.processar_mensagem("oi", "formal")
        self.assertIn("Olá", resposta_normal)
        
        # Teste fallback 
        resposta_fallback, _, _ = self.bot.processar_mensagem("pergunta inexistente", "formal")
        self.assertTrue(len(resposta_fallback) > 0)

    def test_string_matching_original_nao_funcionaria(self):
        """
        Demonstra que o string matching original estava quebrado
        """
        pergunta_inexistente = "pergunta que nao existe"
        
        for personality in ["formal", "engracada", "desafiadora"]:  # Excluir empática que contém "não entendi"
            resposta, is_fallback, _ = self.bot.processar_mensagem(pergunta_inexistente, personality)
            
            # Verifica que é fallback
            self.assertTrue(is_fallback)
            
            # Verifica que a string exata "não sei a resposta" NÃO está na resposta
            # Isso prova que o string matching original nunca funcionaria
            self.assertNotIn("não sei a resposta", resposta,
                            f"String 'não sei a resposta' encontrada na resposta para {personality}")
        
        # Teste específico para empática (que contém variação de "não entendi")
        resposta_empatica, is_fallback_empatica, _ = self.bot.processar_mensagem(pergunta_inexistente, "empatica")
        self.assertTrue(is_fallback_empatica)
        # A string exata "não entendi" (sem "bem") não deveria estar
        self.assertNotIn("não sei a resposta", resposta_empatica)

class TestRegressao(unittest.TestCase):
    """Testes de regressão para verificar que não quebramos nada"""
    
    def setUp(self):
        self.logger = get_logger("test_issue_critica_01")
        self.core_repo = CoreRepo('data/core_data.json', logger=self.logger)
        self.learned_repo = LearnedRepo('data/new_data.json', logger=self.logger)
        self.history_repo = HistoryRepo('data/historico.json', logger=self.logger)
        self.intent_matcher = IntentMatcher(intencoes=self.core_repo.load_intents(), aprendidos=self.learned_repo.load(), logger=self.logger)
        self.bot = Chatbot(matcher=self.intent_matcher, learned_repo=self.learned_repo, history_repo=self.history_repo, logger=self.logger)
    
    def test_todas_intencoes_funcionam(self):
        """Verifica que todas as intenções conhecidas ainda funcionam"""
        test_cases = [
            ("oi", "formal", False),
            ("o que é mdc", "engracada", False),
            ("como somar", "desafiadora", False),
            ("estou com dificuldades nos estudos", "empatica", False),
        ]
        
        for pergunta, personalidade, expected_fallback in test_cases:
            with self.subTest(pergunta=pergunta, personalidade=personalidade):
                resposta, is_fallback, _ = self.bot.processar_mensagem(pergunta, personalidade)
                self.assertEqual(is_fallback, expected_fallback, 
                               f"Fallback incorreto para '{pergunta}' com {personalidade}")
                self.assertTrue(len(resposta) > 0, f"Resposta vazia para '{pergunta}'")

def main():
    """Executa todos os testes com relatório detalhado"""
    print("🧪 Executando testes da correção da Issue Crítica #01")
    print("=" * 60)
    
    # Criar suite de testes
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Adicionar testes específicos da issue
    suite.addTests(loader.loadTestsFromTestCase(TestIssueCorrecao))
    suite.addTests(loader.loadTestsFromTestCase(TestRegressao))
    
    # Executar com verbosidade máxima
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("=" * 60)
    if result.wasSuccessful():
        print("✅ TODOS OS TESTES PASSARAM!")
        print("🎯 Issue Crítica #01 foi resolvida com sucesso!")
        print("\n📋 Resultados:")
        print(f"   • Testes executados: {result.testsRun}")
        print(f"   • Falhas: {len(result.failures)}")
        print(f"   • Erros: {len(result.errors)}")
        print("\n🚀 Sistema de aprendizado agora funciona 100% na interface Gradio!")
    else:
        print("❌ ALGUNS TESTES FALHARAM!")
        print(f"   • Testes executados: {result.testsRun}")
        print(f"   • Falhas: {len(result.failures)}")
        print(f"   • Erros: {len(result.errors)}")
        
        if result.failures:
            print("\n💥 FALHAS:")
            for test, traceback in result.failures:
                print(f"   • {test}: {traceback}")
        
        if result.errors:
            print("\n🔥 ERROS:")
            for test, traceback in result.errors:
                print(f"   • {test}: {traceback}")
    
    return result.wasSuccessful()

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)