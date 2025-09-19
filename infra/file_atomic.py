import os
import json
import shutil
from typing import Any, Optional

class AtomicWriter:
    """Escrita atômica com backup/rollback para JSON (UTF-8)."""
    def __init__(self, logger: Optional[object] = None):
        self.logger = logger

    def _log(self, level: str, msg: str):
        if self.logger:
            getattr(self.logger, level)(msg)

    def write_json_atomic(self, path: str, data: Any, ensure_ascii: bool = False, indent: int = 2) -> bool:
        """Escrita atômica com backup/rollback para JSON (UTF-8)."""
        backup = f"{path}.backup"
        tmp = f"{path}.tmp"

        try:
            if os.path.exists(path):
                shutil.copy2(path, backup)
                self._log('info', f"Backup criado: {backup}")

            json_string = json.dumps(data, ensure_ascii=ensure_ascii, indent=indent)
            json.loads(json_string)  # valida parsing

            with open(tmp, 'w', encoding='utf-8') as f:
                f.write(json_string)

            with open(tmp, 'r', encoding='utf-8') as f:
                json.load(f)  # valida integridade

            os.replace(tmp, path)

            if os.path.exists(backup):
                os.remove(backup)

            self._log('info', f"Arquivo salvo com sucesso: {path}")
            return True

        except Exception as e:
            self._log('error', f"Erro na escrita atômica: {e}")

            if os.path.exists(backup):
                if os.path.exists(path):
                    try:
                        os.remove(path)
                    except Exception:
                        pass
                shutil.copy2(backup, path)
                try:
                    os.remove(backup)
                except Exception:
                    pass
                self._log('info', "Rollback executado")

            if os.path.exists(tmp):
                try:
                    os.remove(tmp)
                except Exception:
                    pass

            return False