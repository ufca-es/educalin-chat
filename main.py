import json
from difflib import get_close_matches
from typing import Optional

def carregar_base_conhecimento(file_path: str) -> dict:
    try:
        with open(file_path, 'r', encoding="utf-8") as file:
            data: dict = json.load(file)
    except FileNotFoundError:
        data = {"perguntas": []}
        with open(file_path, 'w', encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
    return data

def salvar_base_conhecimento(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def achar_melhor_resposta(pergunta_usuario: str, perguntas: list[str]) -> Optional[str]:
    matches: list = get_close_matches(pergunta_usuario, perguntas, n=1, cutoff=0.6)
    return matches[0] if matches else None

def achar_resposta_de_pergunta(pergunta: str, base_conhecimento: dict) -> Optional[str]:
    for p in base_conhecimento["perguntas"]:
        if p["pergunta"] == pergunta:  
            return p["resposta"]
    return None

def chat_bot():
    base_conhecimento: dict = carregar_base_conhecimento('educalin-chat/base_conhecimento.json')

    while True:
        entrada_usuario: str = input('Sua resposta: ')

        if entrada_usuario.lower() == 'quit':
            break

        melhor_resposta: Optional[str] = achar_melhor_resposta(
            entrada_usuario, [p["pergunta"] for p in base_conhecimento["perguntas"]]
        ) 

        if melhor_resposta:
            resposta: str = achar_resposta_de_pergunta(melhor_resposta, base_conhecimento)
            print(f'Aline: {resposta}')
        else:
            print(f'Aline: Eu não sei a resposta dessa pergunta. Você pode me ensinar?')
            nova_resposta: str = input('Escrever resposta ou "pular" para pular: ')

            if nova_resposta.lower() != 'pular':
                base_conhecimento["perguntas"].append({"pergunta": entrada_usuario, "resposta": nova_resposta})
                salvar_base_conhecimento('base_conhecimento.json', base_conhecimento)
                print('Aline: Obrigado! Aprendi uma nova resposta.')

if __name__ == "__main__":
    chat_bot()