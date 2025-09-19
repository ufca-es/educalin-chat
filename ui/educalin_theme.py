import gradio as gr

tema_aline = gr.themes.Base(
    primary_hue="teal",      # melhor aproximação para --color-primary: #1ABC9C
    secondary_hue="blue",
    neutral_hue="slate",
    font=gr.themes.utils.fonts.GoogleFont("Inter")
).set(
    # Paleta principal baseada nas suas variáveis root:
    body_background_fill="#F4F3F2",           # Fundo principal
    background_fill_primary="#F4F3F2",           # Fundo principal
    background_fill_secondary="#FFFFFF",         # Fundo card/bloco

    button_primary_background_fill_hover="#17a085",              # Tom escurecido para hover
    button_primary_text_color="#FFFFFF",
    button_primary_border_color="#1ABC9C",
    button_secondary_background_fill="transparent",
    button_secondary_text_color="#1ABC9C",
    button_secondary_border_color="#1ABC9C",
    block_background_fill="#FFFFFF",
    block_shadow="0 2px 8px rgba(15, 23, 42, 0.06)",
    input_background_fill="#FFFFFF",
)
