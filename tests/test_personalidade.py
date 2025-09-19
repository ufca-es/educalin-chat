#!/usr/bin/env python3
"""
Script de teste para validar a funcionalidade de troca dinâmica de personalidade
Testa todos os casos de uso implementados na Task 08
"""

import sys
import json
from infra.repositories import CoreRepo, LearnedRepo, HistoryRepo
from infra.logging_conf import get_logger
from core.intent_matcher import IntentMatcher
from core.chatbot import Chatbot

def test_chatbot_personalidade():
    """Testa todas as funcionalidades de personalidade implementadas"""
    
    print("🧪 INICIANDO TESTES DE PERSONALIDADE")
    print("="*50)
    
    # Inicializar chatbot
    CORE_DATA_FILE = 'data/core_data.json'
    NEW_DATA_FILE = 'data/new_data.json'
    
    try:
        logger = get_logger("test_personalidade")
        core_repo = CoreRepo(CORE_DATA_FILE, logger=logger)
        learned_repo = LearnedRepo(NEW_DATA_FILE, logger=logger)
        history_repo = HistoryRepo('data/historico.json', logger=logger) # Usar um arquivo de histórico temporário ou mock
        matcher = IntentMatcher(intencoes=core_repo.load_intents(), aprendidos=learned_repo.load(), logger=logger)
        bot = Chatbot(matcher=matcher, learned_repo=learned_repo, history_repo=history_repo, logger=logger)
        print("✅ Chatbot inicializado com sucesso")
    except Exception as e:
        print(f"❌ Erro ao inicializar chatbot: {e}")
        return False
    
    # Teste 1: Validação de personalidades
    print("\n📋 Teste 1: Validação de Personalidades")
    personalidades_validas = ["formal", "engracada", "desafiadora", "empatica"]
    personalidades_invalidas = ["xyz", "informal", ""]
    
    for p in personalidades_validas:
        resultado = bot._validar_personalidade(p)
        print(f"  ✅ '{p}': {resultado}")
        assert resultado == True, f"Personalidade válida '{p}' falhou"
    
    for p in personalidades_invalidas:
        resultado = bot._validar_personalidade(p)
        print(f"  ❌ '{p}': {resultado}")
        assert resultado == False, f"Personalidade inválida '{p}' passou"
    
    # Teste 2: Troca de personalidade
    print("\n🔄 Teste 2: Troca de Personalidade")
    for personalidade in personalidades_validas:
        resultado = bot.trocar_personalidade(personalidade)
        print(f"  ✅ Trocar para '{personalidade}': {resultado}")
        print(f"     Personalidade atual: {bot.personalidade}")
        print(f"     Nome: {bot.nome_personalidade}")
        assert resultado == True, f"Falha ao trocar para '{personalidade}'"
        assert bot.personalidade == personalidade, f"Personalidade não foi definida corretamente"
    
    # Teste 3: Comandos especiais
    print("\n⚡ Teste 3: Processamento de Comandos Especiais")
    
    comandos_teste = [
        ("/help", True, "help"),
        ("/personalidade formal", True, "personalidade"),
        ("/personalidade xyz", True, "personalidade inválida"),
        ("/personalidade", True, "uso incorreto"),
        ("/comando_inexistente", True, "comando desconhecido"),
        ("olá", False, "não é comando")
    ]
    
    for comando, esperado_comando, descricao in comandos_teste:
        is_comando, resposta = bot._processar_comando_especial(comando)
        print(f"  📝 '{comando}': {is_comando} - {descricao}")
        assert is_comando == esperado_comando, f"Falha no comando '{comando}'"
    
    # Teste 4: Processamento de mensagens com personalidades
    print("\n💬 Teste 4: Processamento de Mensagens")
    bot.trocar_personalidade("formal")
    resposta_formal, _, _ = bot.processar_mensagem("oi", "formal")
    
    bot.trocar_personalidade("engracada")
    resposta_engracada, _, _ = bot.processar_mensagem("oi", "engracada")
    
    print(f"  📝 Resposta Formal: {resposta_formal[:50]}...")
    print(f"  📝 Resposta Engraçada: {resposta_engracada[:50]}...")
    
    assert resposta_formal != resposta_engracada, "Respostas devem ser diferentes por personalidade"
    
    # Teste 5: Help de personalidades
    print("\n❓ Teste 5: Help de Personalidades")
    help_text = bot.mostrar_help_personalidades()
    print(f"  📋 Help gerado: {len(help_text)} caracteres")
    
    for personalidade in personalidades_validas:
        assert personalidade in help_text, f"Personalidade '{personalidade}' não está no help"
    
    print("\n🎉 TODOS OS TESTES PASSARAM!")
    return True

def test_compatibilidade_gradio():
    """Testa se as mudanças não afetaram a compatibilidade com Gradio"""
    print("\n🌐 Teste de Compatibilidade com Gradio")
    
    try:
        from app import aline_bot
        resposta, _, _ = aline_bot.processar_mensagem("oi", "formal")
        print(f"  ✅ Método processar_mensagem funciona: {resposta[:50]}...")
        
        resultado = aline_bot.ensinar_nova_resposta("teste", "resposta teste")
        print(f"  ✅ Método ensinar_nova_resposta funciona: {resultado}")
        
        return True
    except Exception as e:
        print(f"  ❌ Erro na compatibilidade com Gradio: {e}")
        return False

if __name__ == "__main__":
    print("🚀 EXECUTANDO TESTES DE VALIDAÇÃO")
    print("=" * 50)
    
    try:
        # Executar testes
        teste1 = test_chatbot_personalidade()
        teste2 = test_compatibilidade_gradio()
        
        if teste1 and teste2:
            print("\n🎊 TODOS OS TESTES FORAM APROVADOS!")
            print("✅ Task 08 implementada com sucesso")
            print("✅ Issues críticas corrigidas")
            print("✅ Compatibilidade mantida")
            sys.exit(0)
        else:
            print("\n❌ ALGUNS TESTES FALHARAM")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n💥 ERRO DURANTE EXECUÇÃO DOS TESTES: {e}")
        sys.exit(1)