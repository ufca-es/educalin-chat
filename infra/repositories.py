import os
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
    Suporta tag_intencao, is_fallback, timestamp_in/out opcionais para compatibilidade com stats.
    """
    def load_last(self, n: int = 5) -> List[Dict[str, Any]]:
        data = self._read_json()
        if isinstance(data, list):
            return data[-n:]
        return []

    def append(self, pergunta: str, resposta: str, personalidade: str, max_len: int = 5, tag_intencao: Optional[str] = None, is_fallback: bool = False, timestamp_in: Optional[str] = None, timestamp_out: Optional[str] = None) -> bool:
        historico = self._read_json()
        if not isinstance(historico, list):
            historico = []

        now_in = timestamp_in or datetime.now().isoformat()
        now_out = timestamp_out or datetime.now().isoformat()

        historico.append({
            "timestamp_in": now_in,
            "timestamp_out": now_out,
            "pergunta": pergunta,
            "resposta": resposta,
            "personalidade": personalidade,
            "tag_intencao": tag_intencao,
            "is_fallback": is_fallback
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

        # Carrega dados existentes
        data = self.load()

        # Atualiza métricas
        data["total_interactions"] += 1
        if is_fallback:
            data["fallback_count"] += 1
        data["por_personalidade"][personalidade] = data["por_personalidade"].get(personalidade, 0) + 1
        if tag:
            data["por_tag"][tag] = data["por_tag"].get(tag, 0) + 1

        # Salva no JSON
        success = self.atomic.write_json_atomic(self.path, data, ensure_ascii=False, indent=2)

        # Garante que relatório.txt exista
        relatorio_path = "relatório.txt"
        if not os.path.exists(relatorio_path):
            with open(relatorio_path, "w", encoding="utf-8") as f:
                f.write("==== Relatório de Interações do Chatbot ====\n\n")

        # Registra a nova interação no relatório
        try:
            with open(relatorio_path, "a", encoding="utf-8") as f:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"[{timestamp}] Interação registrada\n")
                f.write(f"  - Total: {data['total_interactions']}\n")
                f.write(f"  - Fallbacks: {data['fallback_count']}\n")
                f.write(f"  - Personalidade usada: {personalidade}\n")
                if tag:
                    f.write(f"  - Tag: {tag}\n")
                f.write("-" * 40 + "\n")
        except Exception as e:
            if self.logger:
                self.logger.error(f"Erro ao salvar no relatório.txt: {e}")

        if self.logger:
            self.logger.info(f"Stats salvo: {success}")
        return success