from typing import List, Optional
from collections import Counter
import random

from infra.repositories import HistoryRepo
from core.intent_matcher import IntentMatcher

class FAQSuggestions:
    """
    Gera sugestões de perguntas com base no histórico e nas intenções principais.
    """
    def __init__(self, history_repo: HistoryRepo, intent_matcher: IntentMatcher, logger: Optional[object] = None):
        self.history_repo = history_repo
        self.intent_matcher = intent_matcher
        self.logger = logger

    def _log(self, msg: str):
        if self.logger:
            self.logger.info(msg)

    def _get_from_history(self, n: int = 3) -> List[str]:
        """
        Obtém sugestões de perguntas baseadas na frequência do histórico recente.
        """
        self._log("Obtendo sugestões do histórico...")
        historico = self.history_repo.load_last(n=10)  # Carrega um histórico maior para análise
        if not historico:
            return []

        perguntas = [entrada.get('pergunta', '') for entrada in historico]
        contador = Counter(perguntas)
        mais_frequentes = contador.most_common(n)
        sugestoes = [pergunta for pergunta, _ in mais_frequentes]
        self._log(f"Sugestões do histórico encontradas: {sugestoes}")
        return sugestoes

    def _get_from_core(self, n: int = 3) -> List[str]:
        """
        Obtém sugestões aleatórias das intenções principais.
        """
        self._log("Obtendo sugestões do core...")
        todas_perguntas = []
        for intencao in self.intent_matcher.intencoes:
            if intencao.get("tag") not in ["fallback", "saudacao"]:
                perguntas = intencao.get("perguntas", [])
                todas_perguntas.extend(perguntas)
        
        num_sugestoes = min(n, len(todas_perguntas))
        if num_sugestoes > 0:
            sugestoes = random.sample(todas_perguntas, num_sugestoes)
            self._log(f"Sugestões do core encontradas: {sugestoes}")
            return sugestoes
        
        self._log("Nenhuma sugestão do core encontrada.")
        return []

    def get_combined_suggestions(self, n_total: int = 3, n_history: int = 2, n_core: int = 3) -> List[str]:
        """
        Combina sugestões do histórico e do core, evitando duplicatas.
        """
        sugestoes_hist = self._get_from_history(n=n_history)
        sugestoes_core = self._get_from_core(n=n_core)

        combinadas = sugestoes_hist
        for s in sugestoes_core:
            if s not in combinadas:
                combinadas.append(s)
        
        return combinadas[:n_total]