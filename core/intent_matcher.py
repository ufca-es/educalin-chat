from difflib import get_close_matches, SequenceMatcher
from typing import List, Dict, Any, Optional

class IntentMatcher:
    """
    Responsável por encontrar a melhor correspondência para a pergunta do usuário:
    - Busca EXATA e FUZZY nas intenções base
    - Busca EXATA e FUZZY nos aprendizados
    - Fornece respostas de fallback por personalidade
    Não acessa disco nem faz I/O de terminal.
    """

    def __init__(self, intencoes: List[Dict[str, Any]], aprendidos: List[Dict[str, str]], logger=None):
        self.logger = logger
        self.intencoes = intencoes or []
        self.aprendidos = aprendidos or []

        self._mapa_pergunta_intencao: Dict[str, Dict[str, Any]] = {}
        self._todas_perguntas: List[str] = []
        self._fallback_intencao: Optional[Dict[str, Any]] = None

        self._reindex()

    # -------- infra interna --------
    def _log(self, msg: str):
        if self.logger:
            self.logger.info(msg)

    def _reindex(self):
        self._mapa_pergunta_intencao.clear()
        self._todas_perguntas.clear()
        self._fallback_intencao = None

        for intencao in self.intencoes:
            if intencao.get("tag") == "fallback":
                self._fallback_intencao = intencao
            for pergunta in intencao.get("perguntas", []):
                self._todas_perguntas.append(pergunta)
                self._mapa_pergunta_intencao[pergunta.lower()] = intencao

    def refresh_intents(self, intencoes: List[Dict[str, Any]]):
        self.intencoes = intencoes or []
        self._reindex()

    def refresh_learned(self, aprendidos: List[Dict[str, str]]):
        self.aprendidos = aprendidos or []

    # -------- helpers de similaridade --------
    @staticmethod
    def _sim(a: str, b: str) -> float:
        return SequenceMatcher(None, a, b).ratio()

    @staticmethod
    def _jaccard(a: str, b: str) -> float:
        sa, sb = set(a.split()), set(b.split())
        uniao = len(sa.union(sb))
        return (len(sa.intersection(sb)) / uniao) if uniao > 0 else 0.0

    # -------- API principal --------
    def match(self, pergunta_usuario: str) -> Optional[Dict[str, Any]]:
        """
        Retorna:
          - {"tipo": "intent", "intencao": <dict da intenção>}  OU
          - {"tipo": "aprendido", "resposta": <str>}            OU
          - None (sem correspondência -> usar fallback)
        """
        pergunta_norm = (pergunta_usuario or "").lower().strip()
        self._log(f"Iniciando busca por correspondência: '{pergunta_usuario}'")

        # 1) EXATA nas intenções base
        if pergunta_norm in self._mapa_pergunta_intencao:
            intencao = self._mapa_pergunta_intencao[pergunta_norm]
            self._log(f"✅ EXATA base -> tag '{intencao.get('tag')}'")
            return {"tipo": "intent", "intencao": intencao}

        # 2) FUZZY nas intenções base (thresholds originais: cutoff 0.8, sim>=0.92, jac>=0.9)
        matches = get_close_matches(pergunta_norm, self._todas_perguntas, n=1, cutoff=0.8)
        if matches:
            cand = matches[0]
            sim = self._sim(pergunta_norm, cand.lower())
            self._log(f"✅ FUZZY base: '{cand}' (sim: {sim:.2f})")

            if sim >= 0.92:
                for i in self.intencoes:
                    if cand in i.get("perguntas", []):
                        return {"tipo": "intent", "intencao": i}
            elif sim >= 0.8:
                jac = self._jaccard(pergunta_norm, cand.lower())
                self._log(f"Jaccard: {jac:.2f}")
                if jac >= 0.9:
                    for i in self.intencoes:
                        if cand in i.get("perguntas", []):
                            return {"tipo": "intent", "intencao": i}

        # 3) EXATA nos aprendidos (CS e CI)
        mapa_aprendidos_cs = {d.get("pergunta", ""): d for d in self.aprendidos}
        mapa_aprendidos_ci = {k.lower(): v for k, v in mapa_aprendidos_cs.items()}

        if pergunta_usuario in mapa_aprendidos_cs:
            d = mapa_aprendidos_cs[pergunta_usuario]
            self._log("✅ EXATA aprendido (CS)")
            return {"tipo": "aprendido", "resposta": d.get("resposta_ensinada", "")}

        if pergunta_norm in mapa_aprendidos_ci:
            d = mapa_aprendidos_ci[pergunta_norm]
            self._log("✅ EXATA aprendido (CI)")
            return {"tipo": "aprendido", "resposta": d.get("resposta_ensinada", "")}

        # 4) FUZZY nos aprendidos (thresholds originais: cutoff 0.9, sim>=0.92, jac>=0.95)
        perguntas_aprendidas = list(mapa_aprendidos_cs.keys())
        matches_apr = get_close_matches(pergunta_norm, perguntas_aprendidas, n=1, cutoff=0.9)
        if matches_apr:
            cand_apr = matches_apr[0]
            sim_apr = self._sim(pergunta_norm, cand_apr.lower())
            self._log(f"✅ FUZZY aprendido: '{cand_apr}' (sim: {sim_apr:.2f})")

            if sim_apr >= 0.92:
                d = mapa_aprendidos_cs[cand_apr]
                return {"tipo": "aprendido", "resposta": d.get("resposta_ensinada", "")}
            elif sim_apr >= 0.9:
                jac_apr = self._jaccard(pergunta_norm, cand_apr.lower())
                self._log(f"Jaccard apr: {jac_apr:.2f}")
                if jac_apr >= 0.95:
                    d = mapa_aprendidos_cs[cand_apr]
                    return {"tipo": "aprendido", "resposta": d.get("resposta_ensinada", "")}

        self._log(f"❌ Nenhuma correspondência para: '{pergunta_usuario}'")
        return None

    def get_fallback_respostas(self, personalidade: str):
        if not self._fallback_intencao:
            return [
                "Eu não sei a resposta para essa pergunta.",
                "Desculpe, não consegui processar isso."
            ]
        return self._fallback_intencao.get("respostas", {}).get(personalidade, [
            "Desculpe, não entendi."
        ])