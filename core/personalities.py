from typing import Dict, List, Optional, Tuple

# Chaves canônicas
FORMAL = "formal"
ENGRACADA = "engracada"     # (armazenamos sem acento como chave)
DESAFIADORA = "desafiadora"
EMPATICA = "empatica"

# Conjunto válido
PERSONALIDADES_VALIDAS = {FORMAL, ENGRACADA, DESAFIADORA, EMPATICA}

# Nomes de exibição (com acentos)
NOMES_EXIBICAO: Dict[str, str] = {
    FORMAL: "Formal",
    ENGRACADA: "Engraçada",
    DESAFIADORA: "Desafiadora",
    EMPATICA: "Empática",
}

# Descrições curtas (úteis para montar /help e menus na UI)
DESCRICOES: Dict[str, str] = {
    FORMAL: "A Professora Profissional",
    ENGRACADA: "A Coach Descontraída",
    DESAFIADORA: "A Professora Exigente",
    EMPATICA: "A Mentora Gentil",
}

# Aliases aceitos para entradas do usuário (com/sem acento, variações)
ALIASES: Dict[str, str] = {
    "formal": FORMAL,
    "FORMAL": FORMAL,

    "engracada": ENGRACADA,
    "engraçada": ENGRACADA,
    "ENGRACADA": ENGRACADA,
    "ENGRAÇADA": ENGRACADA,

    "desafiadora": DESAFIADORA,
    "DESAFIADORA": DESAFIADORA,

    "empatica": EMPATICA,
    "empática": EMPATICA,
    "EMPATICA": EMPATICA,
    "EMPÁTICA": EMPATICA,
}

# Mapa útil para menus numéricos (CLI)
CHOICE_MAP: Dict[str, str] = {
    "1": FORMAL,
    "2": ENGRACADA,
    "3": DESAFIADORA,
    "4": EMPATICA,
}

def is_valid(personalidade: Optional[str]) -> bool:
    """Retorna True se a string (após canonicalizar) é uma personalidade válida."""
    return canonicalize(personalidade) is not None

def canonicalize(personalidade: Optional[str]) -> Optional[str]:
    """
    Normaliza a entrada do usuário para a chave canônica.
    Aceita variações com acento/maiúsculas e devolve ex.: 'engracada'.
    """
    if not personalidade:
        return None
    key = ALIASES.get(personalidade, None)
    if key:
        return key
    # fallback: lower simples (caso alguém passe 'Formal', etc.)
    low = personalidade.lower()
    return low if low in PERSONALIDADES_VALIDAS else None

def display_name(personalidade: str) -> str:
    """Nome bonito para exibição (com acentos)."""
    return NOMES_EXIBICAO.get(personalidade, personalidade.capitalize())

def description(personalidade: str) -> str:
    """Descrição curta da personalidade."""
    return DESCRICOES.get(personalidade, "")

def list_all() -> List[Tuple[str, str, str]]:
    """
    Lista [(chave, nome_exibicao, descricao)] em ordem recomendada para montar menus.
    """
    ordem = [FORMAL, ENGRACADA, DESAFIADORA, EMPATICA]
    return [(p, NOMES_EXIBICAO[p], DESCRICOES[p]) for p in ordem]