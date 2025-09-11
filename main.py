import json
from difflib import get_close_matches
from typing import Optional, Dict, List

# --- FUNÇÕES DE MANIPULAÇÃO DE ARQUIVOS ---

def carregar_base_conhecimento(file_path: str) -> Dict:
    """Carrega a base de conhecimento principal do arquivo core_data.json."""
    try:
        with open(file_path, 'r', encoding="utf-8") as file:
            data: Dict = json.load(file)
    except FileNotFoundError:
        print(f"ERRO: O arquivo de conhecimento '{file_path}' não foi encontrado.")
        data = {"intencoes": []}
    except json.JSONDecodeError:
        print(f"ERRO: O arquivo '{file_path}' contém um erro de sintaxe JSON.")
        data = {"intencoes": []}
    return data

def salvar_dados_aprendidos(file_path: str, data: List[Dict]):
    """Salva as perguntas e respostas aprendidas no arquivo new_data.json."""
    with open(file_path, 'w', encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

# --- FUNÇÕES DE LÓGICA DO CHATBOT ---

def achar_melhor_intencao(pergunta_usuario: str, intencoes: List[Dict]) -> Optional[Dict]:
    """Encontra a intenção que melhor corresponde à pergunta do usuário."""
    todas_perguntas = [pergunta for intencao in intencoes for pergunta in intencao.get("perguntas", [])]
    matches: List[str] = get_close_matches(pergunta_usuario, todas_perguntas, n=1, cutoff=0.8)
    if matches:
        melhor_pergunta = matches[0]
        for intencao in intencoes:
            if melhor_pergunta in intencao.get("perguntas", []):
                return intencao
    return None

def selecionar_personalidade() -> str:
    """Permite ao usuário escolher a personalidade do chatbot."""
    print("\n" + "="*50)
    print("           ESCOLHA SUA ALINE VIRTUAL           ")
    print("="*50)
    print("\nCom qual personalidade da Aline você gostaria de conversar?\n")
    print("[ 1 ] Aline Formal    - A Professora Profissional")
    print("[ 2 ] Aline Engraçada - A Coach Descontraída")
    print("[ 3 ] Aline Desafiadora - A Professora Exigente")
    print("[ 4 ] Aline Empática    - A Mentora Gentil")
    print("\n" + "-"*50)

    mapa_personalidades = {
        "1": "formal", "2": "engracada", "3": "desafiadora", "4": "empatica"
    }
    
    while True:
        escolha = input("\nDigite o número da sua escolha (1-4): ").strip()
        if escolha in mapa_personalidades:
            print("\nÓtima escolha! Iniciando conversa...\n")
            return mapa_personalidades[escolha]
        print("❌ Opção inválida. Por favor, escolha um número de 1 a 4.")

# --- FUNÇÃO PRINCIPAL ---

def chat_bot():
    """Função principal que executa o loop do chatbot."""
    base_conhecimento = carregar_base_conhecimento('core_data.json')
    intencoes = base_conhecimento.get("intencoes", [])

    if not intencoes:
        print("O chatbot não pode iniciar pois a base de conhecimento está vazia. Encerrando.")
        return

    personalidade = selecionar_personalidade()
    nome_personalidade = personalidade.capitalize()
    
    print(f"\nVocê está conversando com Aline {nome_personalidade}. Digite 'quit' para sair.")

    while True:
        entrada_usuario = input('Você: ').lower()

        if entrada_usuario == 'quit':
            break

        melhor_intencao = achar_melhor_intencao(entrada_usuario, intencoes)

        if melhor_intencao:
            # <<<----------- A CORREÇÃO ESTÁ NESTA LINHA ----------->>>
            resposta = melhor_intencao["respostas"].get(personalidade, "Desculpe, não tenho uma resposta para essa personalidade.")
            print(f'Aline ({nome_personalidade}): {resposta}')
        else:
            # Lógica de fallback e aprendizado
            fallback_intencao = next((i for i in intencoes if i.get("tag") == "fallback"), None)
            if fallback_intencao:
                resposta_fallback = fallback_intencao["respostas"].get(personalidade, "Desculpe, não entendi.")
                print(f'Aline ({nome_personalidade}): {resposta_fallback}')
            else:
                print('Aline: Eu não sei a resposta para essa pergunta.')
            
            print(f'Aline ({nome_personalidade}): Você poderia me ensinar qual seria a resposta ideal?')
            nova_resposta = input("Digite a resposta ou 'pular' para não ensinar: ")

            if nova_resposta.lower() != 'pular':
                dados_aprendidos = []
                try:
                    with open('new_data.json', 'r', encoding='utf-8') as f:
                        dados_carregados = json.load(f)
                        if isinstance(dados_carregados, list):
                            dados_aprendidos = dados_carregados
                        else:
                            print("[Aviso] O arquivo 'new_data.json' não continha uma lista. O formato será corrigido.")
                except (FileNotFoundError, json.JSONDecodeError):
                    pass
                
                dados_aprendidos.append({"pergunta": entrada_usuario, "resposta_ensinada": nova_resposta})
                salvar_dados_aprendidos('new_data.json', dados_aprendidos)
                print(f'Aline ({nome_personalidade}): Obrigada! Aprendi uma nova resposta.')

if __name__ == "__main__":
    chat_bot()