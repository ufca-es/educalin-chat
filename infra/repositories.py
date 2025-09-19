import os
import json
from datetime import datetime, timedelta, timezone
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
        if not isinstance(data, dict):
            data = {}

        # Garante que as chaves principais existam
        data.setdefault("total_interactions", 0)
        data.setdefault("fallback_count", 0)
        data.setdefault("por_personalidade", {})
        data.setdefault("por_tag", {})
        data.setdefault("sessoes", {})
        data.setdefault("total_duracao_sessoes_seg", 0)
        return data

    def update_interaction(
        self,
        is_fallback: bool,
        personalidade: str,
        tag: Optional[str],
        timestamp_in: str,
        timestamp_out: str,
        session_timeout_min: int = 30,
    ) -> bool:
        if self.logger:
            self.logger.info(f"Atualizando stats: fallback={is_fallback}, pers={personalidade}, tag={tag}")

        data = self.load()

        # Atualiza métricas básicas
        data["total_interactions"] += 1
        if is_fallback:
            data["fallback_count"] += 1
        data["por_personalidade"][personalidade] = data["por_personalidade"].get(personalidade, 0) + 1
        if tag:
            data["por_tag"][tag] = data["por_tag"].get(tag, 0) + 1

        # Lógica de Sessão
        try:
            ts_in = datetime.fromisoformat(timestamp_in)
            ts_out = datetime.fromisoformat(timestamp_out)
            duracao_interacao = (ts_out - ts_in).total_seconds()

            sessoes = data.get("sessoes", {})
            ultima_sessao_id = max(sessoes.keys()) if sessoes else None

            if ultima_sessao_id:
                ultima_sessao = sessoes[ultima_sessao_id]
                ultimo_ts_out = datetime.fromisoformat(ultima_sessao["fim"])
                
                if (ts_in - ultimo_ts_out) < timedelta(minutes=session_timeout_min):
                    # Continua sessão existente
                    sessoes[ultima_sessao_id]["fim"] = ts_out.isoformat()
                    sessoes[ultima_sessao_id]["duracao_seg"] += duracao_interacao
                    sessoes[ultima_sessao_id]["num_interacoes"] += 1
                else:
                    # Nova sessão
                    nova_sessao_id = str(int(ultima_sessao_id) + 1)
                    sessoes[nova_sessao_id] = {
                        "inicio": ts_in.isoformat(),
                        "fim": ts_out.isoformat(),
                        "duracao_seg": duracao_interacao,
                        "num_interacoes": 1,
                    }
            else:
                # Primeira sessão
                sessoes["1"] = {
                    "inicio": ts_in.isoformat(),
                    "fim": ts_out.isoformat(),
                    "duracao_seg": duracao_interacao,
                    "num_interacoes": 1,
                }
            
            data["sessoes"] = sessoes
            # Atualiza a duração total agregada para cálculo de média
            data["total_duracao_sessoes_seg"] = sum(s["duracao_seg"] for s in sessoes.values())

        except (ValueError, TypeError) as e:
            if self.logger:
                self.logger.error(f"Erro ao processar timestamps para sessão: {e}")

        success = self.atomic.write_json_atomic(self.path, data, ensure_ascii=False, indent=2)

        # Opcional: manter o relatório de texto
        self._write_to_report(data, personalidade, tag)

        if self.logger:
            self.logger.info(f"Stats salvo: {success}")
        return success

    def _write_to_report(self, data: Dict[str, Any], personalidade: str, tag: Optional[str]):
        relatorio_path = "relatório.txt"
        try:
            if not os.path.exists(relatorio_path):
                with open(relatorio_path, "w", encoding="utf-8") as f:
                    f.write("==== Relatório de Interações do Chatbot ====\n\n")
            
            with open(relatorio_path, "a", encoding="utf-8") as f:
                timestamp = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
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