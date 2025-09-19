import re
import codecs
from typing import Optional

CONTROL_CHAR_REGEX = re.compile(r'[\x00-\x1f\x7f-\x9f]')

MAX_INPUT_LEN = 1000

def validate_input(texto: Optional[str], logger=None) -> bool:
    """
    Validação robusta de entrada para prevenir abusos/ataques.
    Regras (iguais às do código original):
      1) Não aceitar vazio/whitespace
      2) Rejeitar textos com mais de MAX_INPUT_LEN caracteres
      3) Decodificar escapes (unicode_escape); se falhar, rejeita
      4) Rejeitar se houver caracteres de controle após a decodificação
    """
    if not texto or len(texto.strip()) == 0:
        return False

    if len(texto) > MAX_INPUT_LEN:
        if logger:
            logger.warning(f"Entrada muito longa rejeitada: {len(texto)} caracteres")
        return False

    try:
        texto_decodificado = codecs.decode(texto, 'unicode_escape')
    except UnicodeDecodeError:
        if logger:
            logger.warning("Entrada com sequência de escape inválida rejeitada.")
        return False

    # Verifica caracteres de controle
    if CONTROL_CHAR_REGEX.search(texto_decodificado):
        if logger:
            logger.warning("Entrada com caracteres de controle rejeitada")
        return False

    return True