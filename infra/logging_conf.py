import logging

_DEF_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
_initialized = False

def get_logger(name: str = 'chatbot') -> logging.Logger:
    """Configura logging global (console + arquivo UTF-8) uma única vez."""
    global _initialized
    if not _initialized:
        # Console
        logging.basicConfig(level=logging.INFO, format=_DEF_FORMAT)

        # Arquivo
        fh = logging.FileHandler('chatbot.log', encoding='utf-8')
        fh.setLevel(logging.INFO)
        fh.setFormatter(logging.Formatter(_DEF_FORMAT))
        logging.getLogger().addHandler(fh)

        _initialized = True
    return logging.getLogger(name)