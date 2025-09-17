from typing import Optional, Tuple, Dict, Any
import random
from infra.repositories import StatsRepo

class Chatbot:
    def __init__(self, matcher, learned_repo, history_repo, logger):
        self.matcher = matcher
        self.learned_repo = learned_repo
        self.history_repo = history_repo
        self.stats_repo = StatsRepo('stats.json', logger=logger)
        self.logger = logger
        self.personalidade: Optional[str] = None
        self.nome_personalidade: Optional[str] = None

    def set_personalidade(self, personalidade: str, nome_exibicao: str):
        self.personalidade = personalidade
        self.nome_personalidade = nome_exibicao

    def processar_mensagem(self, pergunta: str, personalidade: str) -> Tuple[str, bool, Optional[str]]:
        match = self.matcher.match(pergunta)

        if match is None:
            respostas_fallback = self.matcher.get_fallback_respostas(personalidade)
            resposta = random.choice(respostas_fallback) if isinstance(respostas_fallback, list) else respostas_fallback
            self.history_repo.append(pergunta, resposta, personalidade)
            return resposta, True, None

        if match["tipo"] == "intent":
            intencao = match["intencao"]
            respostas = intencao.get("respostas", {}).get(personalidade, ["Desculpe, não tenho uma resposta para essa personalidade."])
            resposta = random.choice(respostas) if isinstance(respostas, list) else respostas
            tag = intencao.get("tag")
            self.history_repo.append(pergunta, resposta, personalidade)
            return resposta, False, tag

        if match["tipo"] == "aprendido":
            resposta = match["resposta"]
            self.history_repo.append(pergunta, resposta, personalidade)
            return resposta, False, None

        respostas_fallback = self.matcher.get_fallback_respostas(personalidade)
        resposta = random.choice(respostas_fallback) if isinstance(respostas_fallback, list) else respostas_fallback
        self.history_repo.append(pergunta, resposta, personalidade)
        return resposta, True, None

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