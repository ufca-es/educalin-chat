import json
from datetime import datetime
from typing import Any, Dict, List, Optional

from .file_atomic import AtomicWriter

class BaseRepo:
    """Base para repositórios que leem/escrevem JSON."""
    def __init__(self, path: str, logger: Optional[object] = None):
        self.path = path
        self.logger = logger
        self.atomic = AtomicWriter(logger=logger)

    def _read_json(self) -> Optional[Any]:
        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            if self.logger:
                self.logger.info(f"Arquivo não encontrado: {self.path}")
            return None
        except json.JSONDecodeError:
            if self.logger:
                self.logger.error(f"JSON inválido em: {self.path}")
            return None
        except Exception as e:
            if self.logger:
                self.logger.error(f"Erro ao ler {self.path}: {e}")
            return None


class CoreRepo(BaseRepo):
    """Lê intenções do core_data.json (chave 'intencoes')."""
    def load_intents(self) -> List[Dict[str, Any]]:
        data = self._read_json()
        if isinstance(data, dict):
            return data.get('intencoes', []) or []
        return []


class LearnedRepo(BaseRepo):
    """
    Lê/adiciona aprendizados em new_data.json.
    Obs.: Validação de entrada deve ser feita na camada de negócio.
    """
    def load(self) -> List[Dict[str, str]]:
        data = self._read_json()
        return data if isinstance(data, list) else []

    def append(self, pergunta: str, resposta: str) -> bool:
        dados = self.load()
        dados.append({
            "pergunta": pergunta,
            "resposta_ensinada": resposta
        })
        return self.atomic.write_json_atomic(self.path, dados, ensure_ascii=False, indent=2)


class HistoryRepo(BaseRepo):
    """
    Persiste o histórico em historico.json.
    Mantém apenas as últimas `max_len` interações (padrão: 5).
    """
    def load_last(self, n: int = 5) -> List[Dict[str, Any]]:
        data = self._read_json()
        if isinstance(data, list):
            return data[-n:]
        return []

    def append(self, pergunta: str, resposta: str, personalidade: str, max_len: int = 5) -> bool:
        historico = self._read_json()
        if not isinstance(historico, list):
            historico = []

        historico.append({
            "timestamp": datetime.now().isoformat(),
            "pergunta": pergunta,
            "resposta": resposta,
            "personalidade": personalidade
        })

        historico = historico[-max_len:]  # rotação
        return self.atomic.write_json_atomic(self.path, historico, ensure_ascii=False, indent=2)

class StatsRepo(BaseRepo):
    def load(self) -> Dict[str, Any]:
        data = self._read_json()
        if isinstance(data, dict):
            return data
        return {
            "total_interactions": 0,
            "fallback_count": 0,
            "por_personalidade": {},
            "por_tag": {}
        }

    def update_interaction(self, is_fallback: bool, personalidade: str, tag: Optional[str]) -> bool:
        if self.logger:
            self.logger.info(f"Atualizando stats: fallback={is_fallback}, pers={personalidade}, tag={tag}")
        data = self.load()
        data["total_interactions"] += 1
        if is_fallback:
            data["fallback_count"] += 1
        data["por_personalidade"][personalidade] = data["por_personalidade"].get(personalidade, 0) + 1
        if tag:
            data["por_tag"][tag] = data["por_tag"].get(tag, 0) + 1
        success = self.atomic.write_json_atomic(self.path, data, ensure_ascii=False, indent=2)
        if self.logger:
            self.logger.info(f"Stats salvo: {success}")
        return success
class StatsRepo(BaseRepo):
    def load(self) -> Dict[str, Any]:
        data = self._read_json()
        if isinstance(data, dict):
            return data
        return {
            "total_interactions": 0,
            "fallback_count": 0,
            "por_personalidade": {},
            "por_tag": {}
        }

    def update_interaction(self, is_fallback: bool, personalidade: str, tag: Optional[str]) -> bool:
        data = self.load()
        data["total_interactions"] += 1
        if is_fallback:
            data["fallback_count"] += 1
        data["por_personalidade"][personalidade] = data["por_personalidade"].get(personalidade, 0) + 1
        if tag:
            data["por_tag"][tag] = data["por_tag"].get(tag, 0) + 1
        return self.atomic.write_json_atomic(self.path, data, ensure_ascii=False, indent=2)