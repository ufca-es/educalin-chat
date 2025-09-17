import gradio as gr

# --- imports da arquitetura modular ---
from infra.logging_conf import get_logger
from infra.repositories import CoreRepo, LearnedRepo, HistoryRepo
from core.intent_matcher import IntentMatcher
from core.chatbot import Chatbot
from core.personalities import canonicalize, display_name, is_valid

# -------------------------
# Inicialização do Chatbot
# -------------------------

CORE_FILE = 'core_data.json'
NEW_DATA_FILE = 'new_data.json'
HIST_FILE = 'historico.json'

logger = get_logger("chatbot")

# Repositórios de dados
core_repo = CoreRepo(CORE_FILE, logger=logger)
learned_repo = LearnedRepo(NEW_DATA_FILE, logger=logger)
history_repo = HistoryRepo(HIST_FILE, logger=logger)

# Carrega dados
intencoes = core_repo.load_intents()
aprendidos = learned_repo.load()

# Matcher + Chatbot
matcher = IntentMatcher(intencoes=intencoes, aprendidos=aprendidos, logger=logger)
aline_bot = Chatbot(matcher=matcher, learned_repo=learned_repo, history_repo=history_repo, logger=logger)

# -------------------------
# Funções conectadas ao Gradio
# -------------------------

def load_initial_history():
    """Carrega histórico inicial automaticamente para Gradio."""
    bot_name = "Aline"
    welcome = f"Olá! Eu sou a {bot_name}. Escolha uma personalidade e escreva sua mensagem abaixo."

    chat_history = [(bot_name, welcome)]

    # Usa a API pública do Chatbot para obter as últimas mensagens
    historico = aline_bot.carregar_historico_inicial(n=5)
    if historico:
        for entry in historico:
            ts = entry.get("timestamp", "")[:16]  # YYYY-MM-DD HH:MM
            pers = entry.get("personalidade", "formal")
            pers_exibe = display_name(pers)
            hist_msg_user = f"[{ts}] Você: {entry.get('pergunta','')}"
            hist_msg_bot = f"Aline ({pers_exibe}): {entry.get('resposta','')}"
            chat_history.append((hist_msg_user, hist_msg_bot))
        chat_history.append((bot_name, "📜 Histórico anterior carregado. Continuando a conversa..."))

    return chat_history

def reset_chat():
    """Reseta o chat para histórico inicial."""
    return load_initial_history(), {"awaiting_teach": False, "last_question": None}

def enviar_mensagem(user_message: str, personalidade: str, chat_history, internal_state):
    """
    Função disparada quando o usuário envia uma mensagem.
    Retorna chat atualizado e estado interno.
    """
    if internal_state is None:
        internal_state = {"awaiting_teach": False, "last_question": None}

    # Normaliza/valida personalidade
    pers = canonicalize(personalidade) or "formal"
    pers_exibe = display_name(pers)

    # adiciona a mensagem do usuário ao histórico local do componente
    chat = list(chat_history) if chat_history else []
    chat.append(("Você", user_message))

    # Pede resposta ao Chatbot (ele mesmo registra o histórico via HistoryRepo)
    resposta_bot, is_fallback = aline_bot.processar_mensagem(user_message, pers)

    if is_fallback:
        chat.append((f"Aline ({pers_exibe})", resposta_bot + " Você pode me ensinar a resposta ideal?"))
        internal_state["awaiting_teach"] = True
        internal_state["last_question"] = user_message
    else:
        chat.append((f"Aline ({pers_exibe})", resposta_bot))
        internal_state["awaiting_teach"] = False
        internal_state["last_question"] = None

    # ❌ NÃO chamamos métodos privados nem salvamos histórico aqui:
    # o próprio Chatbot já persistiu via HistoryRepo na chamada acima.

    return chat, internal_state, ""  # limpa o input

def ensinar_resposta(resposta_ensinada: str, personalidade: str, chat_history, internal_state):
    """
    Quando o usuário ensina uma resposta para a última pergunta desconhecida.
    Salva em new_data.json via LearnedRepo (encapsulado em Chatbot.ensinar_nova_resposta).
    """
    chat = list(chat_history) if chat_history else []
    if not internal_state or not internal_state.get("awaiting_teach") or not internal_state.get("last_question"):
        chat.append(("Aline", "Não há pergunta pendente para ensinar. Envie uma nova pergunta primeiro."))
        return chat, {"awaiting_teach": False, "last_question": None}, ""

    pergunta = internal_state["last_question"]

    sucesso = aline_bot.ensinar_nova_resposta(pergunta, resposta_ensinada)

    pers = canonicalize(personalidade) or "formal"
    pers_exibe = display_name(pers)

    if sucesso:
        chat.append(("Você", f"(ensinou) {resposta_ensinada}"))
        chat.append((f"Aline ({pers_exibe})", "Obrigada! Aprendi uma nova resposta."))
    else:
        chat.append(("Aline", "Erro ao salvar a nova resposta. Tente novamente."))

    return chat, {"awaiting_teach": False, "last_question": None}, ""  # limpa o campo de ensino

def pular_ensino(chat_history, internal_state, personalidade):
    chat = list(chat_history) if chat_history else []
    pers = canonicalize(personalidade) or "formal"
    pers_exibe = display_name(pers)

    if internal_state and internal_state.get("awaiting_teach"):
        chat.append((f"Aline ({pers_exibe})", "Tudo bem, podemos deixar para depois."))
    else:
        chat.append((f"Aline ({pers_exibe})", "Não há nada para pular no momento."))
    return chat, {"awaiting_teach": False, "last_question": None}, ""

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

    chatbot = gr.Chatbot(value=load_initial_history(), label="Conversa")
    user_input = gr.Textbox(label="Sua mensagem", placeholder="Digite aqui e pressione Enter")
    enviar_btn = gr.Button("Enviar")

    gr.Markdown("### Ensinar resposta (quando o bot não souber)")
    teach_input = gr.Textbox(label="Resposta que você quer ensinar", placeholder="Escreva a resposta que o bot deve aprender")
    ensinar_btn = gr.Button("Ensinar")
    pular_btn = gr.Button("Pular Ensino")

    # estado interno: (flag de ensino pendente, última pergunta)
    estado_interno = gr.State({"awaiting_teach": False, "last_question": None})

    # Reset chat
    reset_btn = gr.Button("Resetar Chat")
    reset_btn.click(fn=reset_chat, inputs=[], outputs=[chatbot, estado_interno])

    # enviar mensagem (botão)
    enviar_btn.click(
        fn=enviar_mensagem,
        inputs=[user_input, personalidade_dropdown, chatbot, estado_interno],
        outputs=[chatbot, estado_interno, user_input]
    )
    # enviar mensagem (enter)
    user_input.submit(
        fn=enviar_mensagem,
        inputs=[user_input, personalidade_dropdown, chatbot, estado_interno],
        outputs=[chatbot, estado_interno, user_input]
    )

    # ensinar resposta
    ensinar_btn.click(
        fn=ensinar_resposta,
        inputs=[teach_input, personalidade_dropdown, chatbot, estado_interno],
        outputs=[chatbot, estado_interno, teach_input]
    )

    # pular ensino
    pular_btn.click(
        fn=pular_ensino,
        inputs=[chatbot, estado_interno, personalidade_dropdown],
        outputs=[chatbot, estado_interno, teach_input]
    )

    # limpar chat (só limpa a UI; o histórico persistido continua salvo)
    def limpar(chat_history, internal_state):
        return [], {"awaiting_teach": False, "last_question": None}
    limpar_btn.click(fn=limpar, inputs=[chatbot, estado_interno], outputs=[chatbot, estado_interno])

# -------------------------
# Run
# -------------------------
if __name__ == "__main__":
    demo.launch(share=False)