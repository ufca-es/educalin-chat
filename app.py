import json
import random
from difflib import get_close_matches
from typing import Optional, Dict, List

import gradio as gr

# -------------------------
# Funções de I/O (arquivos)
# -------------------------

CORE_FILE = 'core_data.json'
NEW_DATA_FILE = 'new_data.json'

def carregar_base_conhecimento(file_path: str) -> Dict:
    try:
        with open(file_path, 'r', encoding="utf-8") as file:
            data: Dict = json.load(file)
    except FileNotFoundError:
        print(f"[WARN] O arquivo '{file_path}' não foi encontrado. Iniciando com base vazia.")
        data = {"intencoes": []}
    except json.JSONDecodeError:
        print(f"[WARN] O arquivo '{file_path}' contém JSON inválido. Iniciando com base vazia.")
        data = {"intencoes": []}
    return data

def salvar_dados_aprendidos(file_path: str, data: List[Dict]):
    with open(file_path, 'w', encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

def carregar_novos_dados(file_path: str) -> List[Dict]:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            dados = json.load(f)
            if isinstance(dados, list):
                return dados
            else:
                print("[WARN] new_data.json não contém lista; retornando lista vazia")
                return []
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# -------------------------
# Lógica do Chatbot
# -------------------------

def achar_melhor_intencao(pergunta_usuario: str, intencoes: List[Dict]) -> Optional[Dict]:
    todas_perguntas = [pergunta for intencao in intencoes for pergunta in intencao.get("perguntas", [])]
    # usar cutoff baixo para permitir correspondências mais flexíveis na interface
    matches: List[str] = get_close_matches(pergunta_usuario, todas_perguntas, n=1, cutoff=0.6)
    if matches:
        melhor_pergunta = matches[0]
        for intencao in intencoes:
            if melhor_pergunta in intencao.get("perguntas", []):
                return intencao
    return None

def gerar_resposta_para_intencao(intencao: Dict, personalidade: str) -> str:
    respostas = intencao.get("respostas", [])
    # suporte tanto dict por personalidade quanto lista
    if isinstance(respostas, dict):
        return respostas.get(personalidade, next(iter(respostas.values())) if respostas else "Desculpe, sem resposta.")
    elif isinstance(respostas, list):
        return random.choice(respostas) if respostas else "Desculpe, sem resposta."
    else:
        return "Desculpe, sem resposta válida configurada."

# -------------------------
# Carregamento inicial
# -------------------------

base_conhecimento = carregar_base_conhecimento(CORE_FILE)
intencoes_globais = base_conhecimento.get("intencoes", [])
novos_dados = carregar_novos_dados(NEW_DATA_FILE)

# -------------------------
# Funções conectadas ao Gradio
# -------------------------

def iniciar_chat():
    """Retorna estado inicial do chat (lista de mensagens) e estado interno."""
    bot_name = "Aline"
    welcome = f"Olá! Eu sou a {bot_name}. Escolha uma personalidade e escreva sua mensagem abaixo."
    return [(bot_name, welcome)], {"awaiting_teach": False, "last_question": None}

def enviar_mensagem(user_message: str, personalidade: str, chat_history, internal_state):
    """
    Função disparada quando o usuário envia uma mensagem.
    Retorna chat atualizado e estado interno.
    """
    if internal_state is None:
        internal_state = {"awaiting_teach": False, "last_question": None}

    # adiciona a mensagem do usuário ao histórico
    chat = list(chat_history) if chat_history else []
    chat.append(("Você", user_message))

    # busca intenção
    melhor_intencao = achar_melhor_intencao(user_message.lower(), intencoes_globais)

    if melhor_intencao:
        resposta_bot = gerar_resposta_para_intencao(melhor_intencao, personalidade)
        chat.append((f"Aline ({personalidade.capitalize()})", resposta_bot))
        internal_state["awaiting_teach"] = False
        internal_state["last_question"] = None
    else:
        # usa fallback se existir
        fallback_intencao = next((i for i in intencoes_globais if i.get("tag") == "fallback"), None)
        if fallback_intencao:
            resposta_fallback = gerar_resposta_para_intencao(fallback_intencao, personalidade)
        else:
            resposta_fallback = "Desculpe, não entendi. Você pode me ensinar a resposta ideal?"
        chat.append((f"Aline ({personalidade.capitalize()})", resposta_fallback))

        # estado para ensinar
        internal_state["awaiting_teach"] = True
        internal_state["last_question"] = user_message

    return chat, internal_state

def ensinar_resposta(resposta_ensinada: str, personalidade: str, chat_history, internal_state):
    """
    Função disparada quando o usuário ensina uma resposta para a última pergunta desconhecida.
    Salva em new_data.json.
    """
    chat = list(chat_history) if chat_history else []
    if not internal_state or not internal_state.get("awaiting_teach") or not internal_state.get("last_question"):
        chat.append(("Aline", "Não há pergunta pendente para ensinar. Envie uma nova pergunta primeiro."))
        return chat, {"awaiting_teach": False, "last_question": None}

    pergunta = internal_state["last_question"]
    # carregar existentes
    dados_aprendidos = carregar_novos_dados(NEW_DATA_FILE)
    dados_aprendidos.append({
        "pergunta": pergunta,
        "resposta_ensinada": resposta_ensinada,
        "personalidade": personalidade
    })
    salvar_dados_aprendidos(NEW_DATA_FILE, dados_aprendidos)

    chat.append(("Você", f"(ensinou) {resposta_ensinada}"))
    chat.append((f"Aline ({personalidade.capitalize()})", "Obrigada! Aprendi uma nova resposta."))
    # resetar estado de ensino
    return chat, {"awaiting_teach": False, "last_question": None}

def pular_ensino(chat_history, internal_state, personalidade):
    chat = list(chat_history) if chat_history else []
    if internal_state and internal_state.get("awaiting_teach"):
        chat.append((f"Aline ({personalidade.capitalize()})", "Tudo bem, podemos deixar para depois."))
    else:
        chat.append((f"Aline ({personalidade.capitalize()})", "Não há nada para pular no momento."))
    return chat, {"awaiting_teach": False, "last_question": None}

# -------------------------
# Construção da interface Gradio
# -------------------------

with gr.Blocks(title="Aline Chatbot (Gradio)") as demo:
    gr.Markdown("# Aline: Seu chatbot de matemática")
    gr.Markdown("Escolha uma personalidade e converse. Se o bot não souber responder, você poderá **ensinar** a resposta.")

    with gr.Row():
        personalidade_dropdown = gr.Dropdown(
            label="Personalidade",
            choices=["formal", "engracada", "desafiadora", "empatica"],
            value="formal"
        )
        limpar_btn = gr.Button("Limpar Chat")

    chatbot = gr.Chatbot(label="Conversa")
    user_input = gr.Textbox(label="Sua mensagem", placeholder="Digite aqui e pressione Enter")
    enviar_btn = gr.Button("Enviar")

    gr.Markdown("### Ensinar resposta (quando o bot não souber)")
    teach_input = gr.Textbox(label="Resposta que você quer ensinar", placeholder="Escreva a resposta que o bot deve aprender")
    ensinar_btn = gr.Button("Ensinar")
    pular_btn = gr.Button("Pular")

    # estados internos: (waiting flag, last_question)
    estado_interno = gr.State({"awaiting_teach": False, "last_question": None})

    # inicializa chat
    init_chat_btn = gr.Button("Iniciar/Resetar chat")
    init_chat_btn.click(fn=iniciar_chat, inputs=[], outputs=[chatbot, estado_interno])

    # enviar mensagem
    enviar_btn.click(
        fn=enviar_mensagem,
        inputs=[user_input, personalidade_dropdown, chatbot, estado_interno],
        outputs=[chatbot, estado_interno]
    )
    # permitir enviar também ao pressionar enter
    user_input.submit(
        fn=enviar_mensagem,
        inputs=[user_input, personalidade_dropdown, chatbot, estado_interno],
        outputs=[chatbot, estado_interno]
    )

    # ensinar resposta
    ensinar_btn.click(
        fn=ensinar_resposta,
        inputs=[teach_input, personalidade_dropdown, chatbot, estado_interno],
        outputs=[chatbot, estado_interno]
    )

    # pular
    pular_btn.click(
        fn=pular_ensino,
        inputs=[chatbot, estado_interno, personalidade_dropdown],
        outputs=[chatbot, estado_interno]
    )

    # limpar chat
    def limpar(chat_history, internal_state):
        return [], {"awaiting_teach": False, "last_question": None}
    limpar_btn.click(fn=limpar, inputs=[chatbot, estado_interno], outputs=[chatbot, estado_interno])

# -------------------------
# Run
# -------------------------
if __name__ == "__main__":
    demo.launch(share=False)
