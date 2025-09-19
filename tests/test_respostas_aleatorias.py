import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.chatbot import Chatbot
from core.personalities import canonicalize
import random

from infra.repositories import CoreRepo, LearnedRepo, HistoryRepo
from infra.logging_conf import get_logger
from core.intent_matcher import IntentMatcher

# Fix seed for reproducible testing
random.seed(42)

def test_aleatoriedade():
    # Já importado no topo
    
    logger = get_logger("test")
    core_repo = CoreRepo('data/core_data.json', logger=logger)
    learned_repo = LearnedRepo('data/new_data.json', logger=logger)
    history_repo = HistoryRepo('data/historico.json', logger=logger)
    
    intencoes = core_repo.load_intents()
    aprendidos = learned_repo.load()
    matcher = IntentMatcher(intencoes=intencoes, aprendidos=aprendidos, logger=logger)
    bot = Chatbot(matcher=matcher, learned_repo=learned_repo, history_repo=history_repo, logger=logger)
    bot.set_personalidade(canonicalize('formal'), 'Formal')
    
    pergunta_teste = "oi"
    
    respostas = []
    for i in range(5):
        resposta, is_fallback, tag = bot.processar_mensagem(pergunta_teste, 'formal')
        respostas.append(resposta)
        print(f"Run {i+1}: {resposta} (tag: {tag})")
    
    # Check for variability
    unique_respostas = set(respostas)
    print(f"\nRespostas únicas: {len(unique_respostas)}/5")
    if len(unique_respostas) > 1:
        print("✅ Variabilidade confirmada!")
    else:
        print("❌ Sem variabilidade detectada.")
    
    # Test fallback
    pergunta_fallback = "pergunta desconhecida"
    respostas_fallback = []
    for i in range(3):
        resposta, is_fallback, tag = bot.processar_mensagem(pergunta_fallback, 'engracada')
        respostas_fallback.append(resposta)
        print(f"Fallback Run {i+1}: {resposta} (is_fallback: {is_fallback}, tag: {tag})")
    
    unique_fallback = set(respostas_fallback)
    print(f"Fallback únicas: {len(unique_fallback)}/3")
    if len(unique_fallback) > 1:
        print("✅ Fallback variabilidade confirmada!")
    else:
        print("❌ Fallback sem variabilidade.")

if __name__ == "__main__":
    test_aleatoriedade()