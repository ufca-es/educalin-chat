import json
from difflib import get_close_matches
from typing import Optional, Dict, List, Any

class Chatbot: # Classe que irá representar o chatbot Aline, gerencia os dados, a lógica da conversa e a aprendizagem da própria.

    def __init__(self, core_data_path: str, new_data_path: str): # Inicialização e definição de caminhos de arquivo.

        self.core_data_path = core_data_path
        self.new_data_path = new_data_path
        self.intencoes: List[Dict[str, Any]] = self._carregar_base_conhecimento()
        self.aprendidos: List[Dict[str, str]] = self._carregar_dados_aprendidos()
        self.personalidade: Optional[str] = None
        self.nome_personalidade: Optional[str] = None

    def _carregar_base_conhecimento(self) -> List[Dict[str, Any]]: # Carregamento de arquivo e correspondência a erros.
    
        try:
            with open(self.core_data_path, 'r', encoding="utf-8") as file:
                data = json.load(file)
                return data.get("intencoes", [])
        except FileNotFoundError:
            print(f"ERRO: O arquivo de conhecimento '{self.core_data_path}' não foi encontrado.")
            return []
        except json.JSONDecodeError:
            print(f"ERRO: O arquivo '{self.core_data_path}' contém um erro de sintaxe JSON.")
            return []

    def _salvar_dados_aprendidos(self, nova_pergunta: str, nova_resposta: str): # Salvar e guardar novos conhecimentos, sem sobreescrever os já existentes.

        dados_aprendidos = []
        try:
            with open(self.new_data_path, 'r', encoding='utf-8') as f:
                dados_carregados = json.load(f)
                if isinstance(dados_carregados, list):
                    dados_aprendidos = dados_carregados
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        
        dados_aprendidos.append({"pergunta": nova_pergunta, "resposta_ensinada": nova_resposta})
        with open(self.new_data_path, 'w', encoding="utf-8") as file:
            json.dump(dados_aprendidos, file, indent=2, ensure_ascii=False)

        self.aprendidos = dados_aprendidos

    def _carregar_dados_aprendidos(self) -> List[Dict[str, str]]: # Utilizar-se dos dados aprendidos
        try:
            with open(self.new_data_path, 'r', encoding="utf-8") as file:
                dados = json.load(file)
                return dados if isinstance(dados, list) else []
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _achar_melhor_intencao(self, pergunta_usuario: str) -> Optional[Dict[str, Any]]: # Encontrar a melhor intenção para o usuário.

        todas_perguntas = [p for intencao in self.intencoes for p in intencao.get("perguntas", [])]
        
        matches: List[str] = get_close_matches(pergunta_usuario, todas_perguntas, n=1, cutoff=0.6)
        
        if matches:
            melhor_pergunta = matches[0]
            for intencao in self.intencoes:
                if melhor_pergunta in intencao.get("perguntas", []):
                    return intencao
        perguntas_aprendidas = [d["pergunta"] for d in self.aprendidos]
        matches_aprendidos = get_close_matches(pergunta_usuario, perguntas_aprendidas, n=1, cutoff=0.7)

        if matches_aprendidos:
            melhor_pergunta_aprendida = matches_aprendidos[0]
            for dado in self.aprendidos:
                if dado["pergunta"] == melhor_pergunta_aprendida:
                    return {"tag": "aprendido", "resposta": dado["resposta_ensinada"]}
                
        return None

    def processar_mensagem(self, pergunta: str, personalidade: str) -> str:
        """
        Método web-friendly para processar uma mensagem sem interface CLI.
        Retorna a resposta do chatbot para a pergunta dada.
        """
        melhor_intencao = self._achar_melhor_intencao(pergunta.lower())
        
        if melhor_intencao and melhor_intencao.get("tag") != "aprendido":
            resposta = melhor_intencao.get("respostas", {}).get(personalidade, "Desculpe, não tenho uma resposta para essa personalidade.")
            return resposta
        
        elif melhor_intencao and melhor_intencao.get("tag") == "aprendido":
            return melhor_intencao["resposta"]
        
        else:
            # Busca fallback
            fallback_intencao = next((i for i in self.intencoes if i.get("tag") == "fallback"), None)
            if fallback_intencao:
                return fallback_intencao.get("respostas", {}).get(personalidade, "Desculpe, não entendi.")
            else:
                return "Eu não sei a resposta para essa pergunta."

    def ensinar_nova_resposta(self, pergunta: str, resposta: str) -> bool:
        """
        Método web-friendly para ensinar uma nova resposta ao chatbot.
        Retorna True se a operação foi bem-sucedida.
        """
        try:
            self._salvar_dados_aprendidos(pergunta, resposta)
            return True
        except Exception as e:
            print(f"Erro ao salvar dados aprendidos: {e}")
            return False

    def _validar_personalidade(self, personalidade: str) -> bool:
        """
        Valida se a personalidade fornecida é válida.
        Retorna True se válida, False caso contrário.
        """
        personalidades_validas = ["formal", "engracada", "desafiadora", "empatica"]
        return personalidade.lower() in personalidades_validas

    def _processar_comando_especial(self, entrada: str) -> tuple[bool, str]:
        """
        Processa comandos especiais que começam com '/'.
        Retorna (is_comando, resposta_ou_mensagem).
        """
        if not entrada.startswith('/'):
            return False, ""
        
        partes = entrada[1:].split()
        if not partes:
            return True, "Comando inválido. Use '/help' para ver os comandos disponíveis."
        
        comando = partes[0].lower()
        
        if comando == "help":
            return True, self.mostrar_help_personalidades()
        
        elif comando == "personalidade":
            if len(partes) < 2:
                return True, "Uso: /personalidade [formal|engracada|desafiadora|empatica]"
            
            nova_personalidade = partes[1].lower()
            if self.trocar_personalidade(nova_personalidade):
                return True, f"Personalidade alterada para {self.nome_personalidade}!"
            else:
                return True, f"Personalidade '{nova_personalidade}' não encontrada. Use '/help' para ver as opções."
        
        else:
            return True, f"Comando '/{comando}' não reconhecido. Use '/help' para ver os comandos disponíveis."

    def trocar_personalidade(self, nova_personalidade: str) -> bool:
        """
        Troca a personalidade atual para uma nova personalidade válida.
        Retorna True se a troca foi bem-sucedida, False caso contrário.
        """
        if not self._validar_personalidade(nova_personalidade):
            return False
        
        self.personalidade = nova_personalidade.lower()
        # Mapear nome da personalidade para exibição
        nomes = {
            "formal": "Formal",
            "engracada": "Engraçada",
            "desafiadora": "Desafiadora",
            "empatica": "Empática"
        }
        self.nome_personalidade = nomes.get(self.personalidade, self.personalidade.capitalize())
        return True

    def mostrar_help_personalidades(self) -> str:
        """
        Retorna string com informações sobre personalidades disponíveis.
        """
        help_text = "\n" + "="*50
        help_text += "\n         COMANDOS E PERSONALIDADES         "
        help_text += "\n" + "="*50
        help_text += "\n\nComandos disponíveis:"
        help_text += "\n• /personalidade [nome] - Troca a personalidade"
        help_text += "\n• /help - Mostra esta ajuda"
        help_text += "\n\nPersonalidades disponíveis:"
        help_text += "\n• formal      - A Professora Profissional"
        help_text += "\n• engracada   - A Coach Descontraída"
        help_text += "\n• desafiadora - A Professora Exigente"
        help_text += "\n• empatica    - A Mentora Gentil"
        help_text += "\n\nExemplo: /personalidade empatica"
        help_text += "\n" + "-"*50
        return help_text

    def selecionar_personalidade(self): # Exibição de menu de escolha para a personalidade.
        
        print("\n" + "="*50)
        print("           ESCOLHA SUA ALINE           ")
        print("="*50)
        print("\nCom qual personalidade da Aline você gostaria de conversar?\n")
        print("[ 1 ] Aline Formal      - A Professora Profissional")
        print("[ 2 ] Aline Engraçada   - A Coach Descontraída")
        print("[ 3 ] Aline Desafiadora - A Professora Exigente")
        print("[ 4 ] Aline Empática    - A Mentora Gentil")
        print("\n" + "-"*50)

        mapa = {"1": "formal", "2": "engracada", "3": "desafiadora", "4": "empatica"}
        
        while True:
            escolha = input("\nDigite o número da sua escolha (1-4): ").strip()
            if escolha in mapa:
                self.personalidade = mapa[escolha]
                self.nome_personalidade = self.personalidade.capitalize()
                print("\nÓtima escolha! Iniciando conversa...\n")
                return
            print("Opção inválida. Por favor, escolha um número de 1 a 4.")
            
    def aprender(self, pergunta_usuario: str): # Fluxo para aprendizagem.

        print(f'Aline ({self.nome_personalidade}): Você poderia me ensinar qual seria a resposta ideal?')
        nova_resposta = input("Digite a resposta ou 'pular' para não ensinar: ").strip()

        if nova_resposta.lower() != 'pular':
            self._salvar_dados_aprendidos(pergunta_usuario, nova_resposta)
            print(f'Aline ({self.nome_personalidade}): Obrigada! Aprendi uma nova resposta.')

    def iniciar_conversa(self): # Loop do chatbot.

        if not self.intencoes:
            print("O chatbot não pode iniciar pois a base de conhecimento está vazia ou com erro. Encerrando.")
            return

        self.selecionar_personalidade()
        
        print(f"Você está conversando com Aline {self.nome_personalidade}. Digite 'quit' para sair ou '/help' para ver comandos.")

        while True:
            entrada_usuario = input('Você: ').strip()

            if entrada_usuario.lower() in ['quit', 'sair', 'tchau', 'até mais', 'até logo']:
                print("Até a próxima!")
                break

            # Verificar se é um comando especial
            is_comando, resposta_comando = self._processar_comando_especial(entrada_usuario)
            if is_comando:
                print(resposta_comando)
                continue

            # Processar como mensagem normal (converter para lowercase para análise)
            melhor_intencao = self._achar_melhor_intencao(entrada_usuario.lower())

            if melhor_intencao and melhor_intencao.get("tag") != "aprendido": 
                resposta = melhor_intencao.get("respostas", {}).get(self.personalidade, "Desculpe, não tenho uma resposta para essa personalidade.")
                print(f'Aline ({self.nome_personalidade}): {resposta}')
            
            elif melhor_intencao and melhor_intencao.get("tag") == "aprendido":
                print(f'Aline ({self.nome_personalidade}): {melhor_intencao["resposta"]}')
            
            else:
                fallback_intencao = next((i for i in self.intencoes if i.get("tag") == "fallback"), None)
                if fallback_intencao:
                    resposta_fallback = fallback_intencao.get("respostas", {}).get(self.personalidade, "Desculpe, não entendi.")
                    print(f'Aline ({self.nome_personalidade}): {resposta_fallback}')
                else:
                    print(f'Aline ({self.nome_personalidade}): Eu não sei a resposta para essa pergunta.')
                
                quer_ensinar = input(f'Aline ({self.nome_personalidade}): Deseja me ensinar a resposta correta? (s/n) ').lower().strip()

                if quer_ensinar == 's':
                    self.aprender(entrada_usuario)

if __name__ == "__main__": # Execução do chatbot.
    CORE_DATA_FILE = 'core_data.json'
    NEW_DATA_FILE = 'new_data.json'
    
    aline_bot = Chatbot(core_data_path=CORE_DATA_FILE, new_data_path=NEW_DATA_FILE)
    
    aline_bot.iniciar_conversa()