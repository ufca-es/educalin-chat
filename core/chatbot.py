from typing import Optional, Tuple, Dict, Any
import random
import re
import codecs
from datetime import datetime
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
        # Validação robusta de entrada (portada do original main.py)
        CONTROL_CHAR_REGEX = re.compile(r'[\x00-\x1f\x7f-\x9f]')
        if not pergunta or len(pergunta.strip()) == 0:
            self.logger.warning("Entrada vazia rejeitada")
            return "Entrada inválida. Tente novamente.", True, None
        if len(pergunta) > 1000:
            self.logger.warning(f"Entrada muito longa rejeitada: {len(pergunta)} caracteres")
            return "Entrada muito longa. Limite: 1000 caracteres.", True, None
        try:
            texto_decodificado = codecs.decode(pergunta, 'unicode_escape')
        except UnicodeDecodeError:
            self.logger.warning("Entrada com sequência de escape inválida rejeitada.")
            return "Entrada com caracteres inválidos. Tente novamente.", True, None
        if CONTROL_CHAR_REGEX.search(texto_decodificado):
            self.logger.warning("Entrada com caracteres de controle rejeitada")
            return "Entrada contém caracteres não permitidos. Tente novamente.", True, None

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