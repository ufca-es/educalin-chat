from typing import Optional, Tuple, Dict, Any
import random
from datetime import datetime, timezone
from infra.repositories import StatsRepo
from core.faq_suggestions import FAQSuggestions
from core.validation import validate_input

class Chatbot:
    def __init__(self, matcher, learned_repo, history_repo, logger):
        self.matcher = matcher
        self.learned_repo = learned_repo
        self.history_repo = history_repo
        self.stats_repo = StatsRepo('data/stats.json', logger=logger)
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

        now_in = datetime.now(timezone.utc).isoformat()
        match = self.matcher.match(pergunta)

        is_fallback = False
        tag = None
        resposta = ""

        if match is None:
            is_fallback = True
            tag = "fallback"
            respostas_fallback = self.matcher.get_fallback_respostas(personalidade)
            resposta = random.choice(respostas_fallback) if isinstance(respostas_fallback, list) else respostas_fallback
        
        elif match["tipo"] == "intent":
            is_fallback = False
            intencao = match["intencao"]
            tag = intencao.get("tag")
            respostas = intencao.get("respostas", {}).get(personalidade, ["Desculpe, não tenho uma resposta para essa personalidade."])
            resposta = random.choice(respostas) if isinstance(respostas, list) else respostas

        elif match["tipo"] == "aprendido":
            is_fallback = False
            tag = "aprendido"
            resposta = match["resposta"]
        
        else: # Fallback de segurança
            is_fallback = True
            tag = "fallback"
            respostas_fallback = self.matcher.get_fallback_respostas(personalidade)
            resposta = random.choice(respostas_fallback) if isinstance(respostas_fallback, list) else respostas_fallback

        now_out = datetime.now(timezone.utc).isoformat()
        
        self.history_repo.append(
            pergunta, resposta, personalidade,
            tag_intencao=tag, is_fallback=is_fallback,
            timestamp_in=now_in, timestamp_out=now_out
        )
        
        self.update_stats(is_fallback, personalidade, tag, now_in, now_out)
        
        return resposta, is_fallback, tag

    def ensinar_nova_resposta(self, pergunta: str, resposta: str) -> bool:
        if not validate_input(pergunta, self.logger):
            self.logger.warning("Pergunta inválida rejeitada no ensino")
            return False
        if not validate_input(resposta, self.logger):
            self.logger.warning("Resposta inválida rejeitada no ensino")
            return False
        ok = self.learned_repo.append(pergunta, resposta)
        if ok:
            aprendidos = self.learned_repo.load()
            self.matcher.refresh_learned(aprendidos)
        return ok

    def carregar_historico_inicial(self, n: int = 5):
        return self.history_repo.load_last(n)

    def update_stats(self, is_fallback: bool, personalidade: str, tag: Optional[str], timestamp_in: str, timestamp_out: str):
        self.stats_repo.update_interaction(is_fallback, personalidade, tag, timestamp_in, timestamp_out)

    def get_stats(self) -> Dict[str, Any]:
        data = self.stats_repo.load()
        total = data.get("total_interactions", 0)
        fallback_count = data.get("fallback_count", 0)
        fallback_rate = fallback_count / total if total > 0 else 0.0

        por_personalidade = data.get("por_personalidade", {})
        por_personalidade_perc = {pers: (count / total * 100) if total > 0 else 0.0 for pers, count in por_personalidade.items()}

        por_tag = data.get("por_tag", {})
        por_tag_perc = {t: (count / total * 100) if total > 0 else 0.0 for t, count in por_tag.items()}

        # Calcula a duração média da sessão
        sessoes = data.get("sessoes", {})
        total_duracao_seg = data.get("total_duracao_sessoes_seg", 0)
        num_sessoes = len(sessoes)
        
        media_duracao_seg = total_duracao_seg / num_sessoes if num_sessoes > 0 else 0.0
        media_duracao_min = media_duracao_seg / 60.0

        return {
            "total_interactions": total,
            "fallback_rate": fallback_rate,
            "fallback_count": fallback_count,
            "por_personalidade": por_personalidade,
            "por_personalidade_perc": por_personalidade_perc,
            "por_tag": por_tag,
            "por_tag_perc": por_tag_perc,
            "media_duracao_sessao_min": media_duracao_min,
            "num_sessoes": num_sessoes,
        }

    def get_faq_suggestions(self, n_total: int = 3) -> list[str]:
        """
        Retorna uma lista de sugestões de perguntas para o usuário.
        """
        return self.faq_suggestions.get_combined_suggestions(n_total=n_total)