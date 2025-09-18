from typing import Optional, Tuple, Dict, Any
import random
from datetime import datetime
from infra.repositories import StatsRepo
from core.faq_suggestions import FAQSuggestions
from core.validation import validate_input

class Chatbot:
    def __init__(self, matcher, learned_repo, history_repo, logger):
        self.matcher = matcher
        self.learned_repo = learned_repo
        self.history_repo = history_repo
        self.stats_repo = StatsRepo('stats.json', logger=logger)
        self.logger = logger
        self.faq_suggestions = FAQSuggestions(history_repo=history_repo, intent_matcher=matcher, logger=logger)
        self.personalidade: Optional[str] = None
        self.nome_personalidade: Optional[str] = None

    def set_personalidade(self, personalidade: str, nome_exibicao: str):
        self.personalidade = personalidade
        self.nome_personalidade = nome_exibicao

    def processar_mensagem(self, pergunta: str, personalidade: str) -> Tuple[str, bool, Optional[str]]:
        if not validate_input(pergunta, self.logger):
            return "Entrada inválida. Tente novamente.", True, None

        now_in = datetime.now().isoformat()
        match = self.matcher.match(pergunta)

        if match is None:
            respostas_fallback = self.matcher.get_fallback_respostas(personalidade)
            resposta = random.choice(respostas_fallback) if isinstance(respostas_fallback, list) else respostas_fallback
            now_out = datetime.now().isoformat()
            self.history_repo.append(pergunta, resposta, personalidade, tag_intencao="fallback", is_fallback=True, timestamp_in=now_in, timestamp_out=now_out)
            self.update_stats(True, personalidade, "fallback")
            return resposta, True, "fallback"

        if match["tipo"] == "intent":
            intencao = match["intencao"]
            respostas = intencao.get("respostas", {}).get(personalidade, ["Desculpe, não tenho uma resposta para essa personalidade."])
            resposta = random.choice(respostas) if isinstance(respostas, list) else respostas
            tag = intencao.get("tag")
            now_out = datetime.now().isoformat()
            self.history_repo.append(pergunta, resposta, personalidade, tag_intencao=tag, is_fallback=False, timestamp_in=now_in, timestamp_out=now_out)
            self.update_stats(False, personalidade, tag)
            return resposta, False, tag

        if match["tipo"] == "aprendido":
            resposta = match["resposta"]
            now_out = datetime.now().isoformat()
            self.history_repo.append(pergunta, resposta, personalidade, tag_intencao="aprendido", is_fallback=False, timestamp_in=now_in, timestamp_out=now_out)
            self.update_stats(False, personalidade, "aprendido")
            return resposta, False, "aprendido"

        respostas_fallback = self.matcher.get_fallback_respostas(personalidade)
        resposta = random.choice(respostas_fallback) if isinstance(respostas_fallback, list) else respostas_fallback
        now_out = datetime.now().isoformat()
        self.history_repo.append(pergunta, resposta, personalidade, tag_intencao="fallback", is_fallback=True, timestamp_in=now_in, timestamp_out=now_out)
        self.update_stats(True, personalidade, "fallback")
        return resposta, True, "fallback"

    def ensinar_nova_resposta(self, pergunta: str, resposta: str) -> bool:
        ok = self.learned_repo.append(pergunta, resposta)
        if ok:
            aprendidos = self.learned_repo.load()
            self.matcher.refresh_learned(aprendidos)
        return ok

    def carregar_historico_inicial(self, n: int = 5):
        return self.history_repo.load_last(n)

    def update_stats(self, is_fallback: bool, personalidade: str, tag: Optional[str]):
        self.stats_repo.update_interaction(is_fallback, personalidade, tag)

    def get_stats(self) -> Dict[str, Any]:
        data = self.stats_repo.load()
        total = data["total_interactions"]
        fallback_count = data["fallback_count"]
        fallback_rate = fallback_count / total if total > 0 else 0.0

        por_personalidade_perc = {}
        for pers, count in data["por_personalidade"].items():
            perc = (count / total * 100) if total > 0 else 0.0
            por_personalidade_perc[pers] = perc

        por_tag_perc = {}
        for t, count in data["por_tag"].items():
            perc = (count / total * 100) if total > 0 else 0.0
            por_tag_perc[t] = perc

        # Duração média: placeholder, pois não temos sessões definidas
        media_duracao = 0.0

        return {
            "total_interactions": total,
            "fallback_rate": fallback_rate,
            "fallback_count": fallback_count,
            "por_personalidade": data["por_personalidade"],
            "por_personalidade_perc": por_personalidade_perc,
            "por_tag": data["por_tag"],
            "por_tag_perc": por_tag_perc,
            "media_duracao_sessao_min": media_duracao
        }

    def get_faq_suggestions(self, n_total: int = 3) -> list[str]:
        """
        Retorna uma lista de sugestões de perguntas para o usuário.
        """
        return self.faq_suggestions.get_combined_suggestions(n_total=n_total)