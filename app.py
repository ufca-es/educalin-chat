import gradio as gr
from main import Chatbot

# -------------------------
# Inicialização do Chatbot
# -------------------------

CORE_FILE = 'core_data.json'
NEW_DATA_FILE = 'new_data.json'

# Instância global do chatbot
aline_bot = Chatbot(core_data_path=CORE_FILE, new_data_path=NEW_DATA_FILE)

# -------------------------
# Funções conectadas ao Gradio
# -------------------------

def load_initial_history():
    """Carrega histórico inicial automaticamente para Gradio."""
    bot_name = "Aline"
    welcome = f"Olá! Eu sou a {bot_name}. Escolha uma personalidade e escreva sua mensagem abaixo."
    
    # Task 11: Carregar e exibir histórico anterior no Gradio automaticamente
    chat_history = [(bot_name, welcome)]
    if aline_bot.historico:
        for entry in aline_bot.historico:
            ts = entry["timestamp"][:16]  # Formato legível
            pers = entry["personalidade"].capitalize()
            hist_msg_user = f"[{ts}] Você: {entry['pergunta']}"
            hist_msg_bot = f"Aline ({pers}): {entry['resposta']}"
            chat_history.append((hist_msg_user, hist_msg_bot))
        chat_history.append((bot_name, "📜 Histórico anterior carregado. Continuando a conversa..."))
    
    return chat_history

def reset_chat():
    """Reseta o chat para histórico inicial."""
    return load_initial_history(), {"awaiting_teach": False, "last_question": None}

def enviar_mensagem(user_message: str, personalidade: str, chat_history, internal_state):
    """
    🚀 FUNÇÃO CORRIGIDA - Solução para Issue Crítica #01
    
    Função disparada quando o usuário envia uma mensagem.
    Retorna chat atualizado e estado interno.
    """
    if internal_state is None:
        internal_state = {"awaiting_teach": False, "last_question": None}

    # adiciona a mensagem do usuário ao histórico
    chat = list(chat_history) if chat_history else []
    chat.append(("Você", user_message))

    # 🚨 CORREÇÃO: Usa o método corrigido que retorna tupla (resposta, is_fallback)
    resposta_bot, is_fallback = aline_bot.processar_mensagem(user_message, personalidade)
    
    # 🚨 CORREÇÃO: Verifica fallback usando flag robusta ao invés de string matching
    if is_fallback:
        chat.append((f"Aline ({personalidade.capitalize()})", resposta_bot + " Você pode me ensinar a resposta ideal?"))
        # estado para ensinar
        internal_state["awaiting_teach"] = True
        internal_state["last_question"] = user_message
    else:
        chat.append((f"Aline ({personalidade.capitalize()})", resposta_bot))
        internal_state["awaiting_teach"] = False
        internal_state["last_question"] = None

    # Task 12: Salvar interação no histórico para Gradio
    aline_bot._salvar_historico(user_message, resposta_bot, personalidade)

    return chat, internal_state, ""  # Limpa input

def ensinar_resposta(resposta_ensinada: str, personalidade: str, chat_history, internal_state):
    """
    Função disparada quando o usuário ensina uma resposta para a última pergunta desconhecida.
    Salva em new_data.json.
    """
    chat = list(chat_history) if chat_history else []
    if not internal_state or not internal_state.get("awaiting_teach") or not internal_state.get("last_question"):
        chat.append(("Aline", "Não há pergunta pendente para ensinar. Envie uma nova pergunta primeiro."))
        return chat, {"awaiting_teach": False, "last_question": None}, ""

    pergunta = internal_state["last_question"]
    
    # usa o método da classe Chatbot para ensinar nova resposta
    sucesso = aline_bot.ensinar_nova_resposta(pergunta, resposta_ensinada)
    
    if sucesso:
        chat.append(("Você", f"(ensinou) {resposta_ensinada}"))
        chat.append((f"Aline ({personalidade.capitalize()})", "Obrigada! Aprendi uma nova resposta."))
    else:
        chat.append(("Aline", "Erro ao salvar a nova resposta. Tente novamente."))
    
    # resetar estado de ensino
    return chat, {"awaiting_teach": False, "last_question": None}, ""

def pular_ensino(chat_history, internal_state, personalidade):
    chat = list(chat_history) if chat_history else []
    if internal_state and internal_state.get("awaiting_teach"):
        chat.append((f"Aline ({personalidade.capitalize()})", "Tudo bem, podemos deixar para depois."))
    else:
        chat.append((f"Aline ({personalidade.capitalize()})", "Não há nada para pular no momento."))
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

    chatbot = gr.Chatbot(value=load_initial_history(), label="Conversa")  # Auto-carregamento inicial
    user_input = gr.Textbox(label="Sua mensagem", placeholder="Digite aqui e pressione Enter")
    enviar_btn = gr.Button("Enviar")

    gr.Markdown("### Ensinar resposta (quando o bot não souber)")
    teach_input = gr.Textbox(label="Resposta que você quer ensinar", placeholder="Escreva a resposta que o bot deve aprender")
    ensinar_btn = gr.Button("Ensinar")
    pular_btn = gr.Button("Pular Ensino")

    # estados internos: (waiting flag, last_question)
    estado_interno = gr.State({"awaiting_teach": False, "last_question": None})

    # Reset chat (antigo init)
    reset_btn = gr.Button("Resetar Chat")
    reset_btn.click(fn=reset_chat, inputs=[], outputs=[chatbot, estado_interno])

    # enviar mensagem
    enviar_btn.click(
        fn=enviar_mensagem,
        inputs=[user_input, personalidade_dropdown, chatbot, estado_interno],
        outputs=[chatbot, estado_interno, user_input]
    )
    # permitir enviar também ao pressionar enter
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

    # pular
    pular_btn.click(
        fn=pular_ensino,
        inputs=[chatbot, estado_interno, personalidade_dropdown],
        outputs=[chatbot, estado_interno, teach_input]
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
