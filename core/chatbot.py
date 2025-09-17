from typing import Optional, Tuple
import random

class Chatbot:
    def __init__(self, matcher, learned_repo, history_repo, logger):
        self.matcher = matcher
        self.learned_repo = learned_repo
        self.history_repo = history_repo
        self.logger = logger
        self.personalidade: Optional[str] = None
        self.nome_personalidade: Optional[str] = None

    def set_personalidade(self, personalidade: str, nome_exibicao: str):
        self.personalidade = personalidade
        self.nome_personalidade = nome_exibicao

    def processar_mensagem(self, pergunta: str, personalidade: str) -> Tuple[str, bool]:
        match = self.matcher.match(pergunta)

        if match is None:
            respostas_fallback = self.matcher.get_fallback_respostas(personalidade)
            resposta = random.choice(respostas_fallback) if isinstance(respostas_fallback, list) else respostas_fallback
            self.history_repo.append(pergunta, resposta, personalidade)
            return resposta, True

        if match["tipo"] == "intent":
            intencao = match["intencao"]
            respostas = intencao.get("respostas", {}).get(personalidade, ["Desculpe, não tenho uma resposta para essa personalidade."])
            resposta = random.choice(respostas) if isinstance(respostas, list) else respostas
            self.history_repo.append(pergunta, resposta, personalidade)
            return resposta, False

        if match["tipo"] == "aprendido":
            resposta = match["resposta"]
            self.history_repo.append(pergunta, resposta, personalidade)
            return resposta, False

        respostas_fallback = self.matcher.get_fallback_respostas(personalidade)
        resposta = random.choice(respostas_fallback) if isinstance(respostas_fallback, list) else respostas_fallback
        self.history_repo.append(pergunta, resposta, personalidade)
        return resposta, True

    def ensinar_nova_resposta(self, pergunta: str, resposta: str) -> bool:
        ok = self.learned_repo.append(pergunta, resposta)
        if ok:
            aprendidos = self.learned_repo.load()
            self.matcher.refresh_learned(aprendidos)
        return ok

    def carregar_historico_inicial(self, n: int = 5):
        return self.history_repo.load_last(n)