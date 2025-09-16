import json
import re
import os
import shutil
import logging
import codecs
import random
from difflib import get_close_matches, SequenceMatcher
from typing import Optional, Dict, List, Any

CONTROL_CHAR_REGEX = re.compile(r'[\x00-\x1f\x7f-\x9f]')

class Chatbot: # Classe que irá representar o chatbot Aline, gerencia os dados, a lógica da conversa e a aprendizagem da própria.

    def __init__(self, core_data_path: str, new_data_path: str): # Inicialização e definição de caminhos de arquivo.

        self.core_data_path = core_data_path
        self.new_data_path = new_data_path
        self.logger = self._setup_logging()
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

    def _setup_logging(self):
        """Configuração de logging para debugging e monitoramento"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('chatbot.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger('chatbot')

    def _validar_entrada(self, texto: str) -> bool:
        """Validação robusta de entrada para prevenir ataques"""
        if not texto or len(texto.strip()) == 0:
            return False
        
        if len(texto) > 1000:  # Limite razoável
            self.logger.warning(f"Entrada muito longa rejeitada: {len(texto)} caracteres")
            return False
        
        # Decodificar escapes para garantir que a validação pegue caracteres como \x00
        try:
            texto_decodificado = codecs.decode(texto, 'unicode_escape')
        except UnicodeDecodeError:
            self.logger.warning("Entrada com sequência de escape inválida rejeitada.")
            return False # Rejeita entradas com escapes malformados

        # Verificação robusta de caracteres de controle usando regex no texto decodificado
        if CONTROL_CHAR_REGEX.search(texto_decodificado):
            self.logger.warning("Entrada com caracteres de controle rejeitada")
            return False
        
        return True

    def _salvar_dados_aprendidos(self, nova_pergunta: str, nova_resposta: str) -> bool:
        """
        🚀 MÉTODO CORRIGIDO - Versão robusta com tratamento UTF-8, rollback e integridade
        
        Args:
            nova_pergunta: Pergunta a ser aprendida
            nova_resposta: Resposta correspondente
            
        Returns:
            bool: True se salvamento foi bem-sucedido, False caso contrário
        """
        # Validação de entrada
        if not self._validar_entrada(nova_pergunta) or not self._validar_entrada(nova_resposta):
            self.logger.error("Entrada inválida rejeitada")
            return False
            
        backup_file = f"{self.new_data_path}.backup"
        temp_file = f"{self.new_data_path}.tmp"
        
        try:
            # 1. Backup do arquivo atual se existir
            if os.path.exists(self.new_data_path):
                shutil.copy2(self.new_data_path, backup_file)
                self.logger.info("Backup criado com sucesso")
            
            # 2. Carregamento seguro dos dados existentes
            dados_aprendidos = []
            try:
                with open(self.new_data_path, 'r', encoding='utf-8') as f:
                    dados_carregados = json.load(f)
                    if isinstance(dados_carregados, list):
                        dados_aprendidos = dados_carregados
            except (FileNotFoundError, json.JSONDecodeError, UnicodeDecodeError, Exception) as e:
                self.logger.error(f"Erro crítico no arquivo: {str(e)} - Recriando arquivo válido")
                # Cria arquivo vazio com estrutura JSON válida
                with open(self.new_data_path, 'w', encoding='utf-8') as f:
                    json.dump([], f)
                dados_aprendidos = []
            
            # 3. Adicionar nova entrada
            nova_entrada = {
                "pergunta": nova_pergunta,
                "resposta_ensinada": nova_resposta
            }
            dados_aprendidos.append(nova_entrada)
            
            # 4. Validação antes de escrever
            json_string = json.dumps(dados_aprendidos, indent=2, ensure_ascii=False)
            json.loads(json_string)  # Validação de parsing
            
            # 5. Escrita atômica usando arquivo temporário
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(json_string)
            
            # 6. Verificação pós-escrita
            with open(temp_file, 'r', encoding='utf-8') as f:
                json.load(f)  # Verificação de integridade
            
            # 7. Commit atômico (renomear arquivo temporário)
            os.replace(temp_file, self.new_data_path)
            
            # 8. Cleanup backup se tudo deu certo
            if os.path.exists(backup_file):
                os.remove(backup_file)
                
            # 9. Atualizar dados em memória
            self.aprendidos = dados_aprendidos
            self.logger.info(f"Dados salvos com sucesso: '{nova_pergunta}' -> '{nova_resposta}'")
            return True
            
        except Exception as e:
            # Rollback em caso de falha
            self.logger.error(f"ERRO CRÍTICO ao salvar dados: {e}")
            if os.path.exists(backup_file) and os.path.exists(self.new_data_path):
                shutil.copy2(backup_file, self.new_data_path)
                os.remove(backup_file)
                self.logger.info("Rollback executado com sucesso")
            
            # Cleanup arquivo temporário
            if os.path.exists(temp_file):
                os.remove(temp_file)
            
            return False

    def _carregar_dados_aprendidos(self) -> List[Dict[str, str]]: # Utilizar-se dos dados aprendidos
        try:
            with open(self.new_data_path, 'r', encoding="utf-8") as file:
                dados = json.load(file)
                return dados if isinstance(dados, list) else []
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _achar_melhor_intencao(self, pergunta_usuario: str) -> Optional[Dict[str, Any]]:
        """
        🚀 MÉTODO CORRIGIDO - Versão com threshold mais rigoroso e busca exata primeiro
        
        Args:
            pergunta_usuario: Pergunta do usuário para buscar correspondência
            
        Returns:
            Dict com intenção correspondente ou None se não encontrar
        """
        pergunta_normalizada = pergunta_usuario.lower().strip()
        self.logger.info(f"Iniciando busca por correspondência: '{pergunta_usuario}'")
        
        # 1. Busca EXATA primeiro nas intenções base
        todas_perguntas = []
        mapa_pergunta_intencao = {}
        
        for intencao in self.intencoes:
            for pergunta in intencao.get("perguntas", []):
                todas_perguntas.append(pergunta)
                mapa_pergunta_intencao[pergunta.lower()] = intencao
        
        # Verificar correspondência exata (case-insensitive)
        if pergunta_normalizada in mapa_pergunta_intencao:
            intencao_encontrada = mapa_pergunta_intencao[pergunta_normalizada]
            self.logger.info(f"✅ Correspondência EXATA encontrada nas intenções base: '{pergunta_usuario}' -> tag '{intencao_encontrada.get('tag')}'")
            return intencao_encontrada
        
        # 2. Busca fuzzy nas intenções base (threshold MAIS RIGOROSO)
        matches = get_close_matches(pergunta_normalizada, todas_perguntas, n=1, cutoff=0.8)
        
        if matches:
            melhor_pergunta = matches[0]
            similaridade = SequenceMatcher(None, pergunta_normalizada, melhor_pergunta.lower()).ratio()
            self.logger.info(f"✅ Correspondência FUZZY encontrada nas intenções base: '{pergunta_usuario}' -> '{melhor_pergunta}' (similaridade: {similaridade:.2f})")
            
            # Lógica Condicional de Confiança
            self.logger.info(f"Similaridade SequenceMatcher: {similaridade:.2f}")

            # 1. Alta Confiança (>=0.92): Aceita como erro de digitação, sem verificação Jaccard.
            if similaridade >= 0.92:
                self.logger.info("Alta confiança, aceitando correspondência.")
                for intencao in self.intencoes:
                    if melhor_pergunta in intencao.get("perguntas", []):
                        return intencao
            
            # 2. Confiança Média (>=0.8): Requer verificação Jaccard para desambiguação.
            elif similaridade >= 0.8:
                tokens_usuario = set(pergunta_normalizada.split())
                tokens_candidata = set(melhor_pergunta.lower().split())
                intersecao = len(tokens_usuario.intersection(tokens_candidata))
                uniao = len(tokens_usuario.union(tokens_candidata))
                jaccard_similarity = intersecao / uniao if uniao > 0 else 0
                self.logger.info(f"Confiança média, verificando Jaccard: {jaccard_similarity:.2f}")
                
                if jaccard_similarity >= 0.9:
                    self.logger.info("Jaccard alto, confirmando correspondência.")
                    for intencao in self.intencoes:
                        if melhor_pergunta in intencao.get("perguntas", []):
                            return intencao
        
        # 3. Busca EXATA primeiro nos dados aprendidos
        perguntas_aprendidas = [d["pergunta"] for d in self.aprendidos]
        mapa_aprendidos = {d["pergunta"]: d for d in self.aprendidos}
        mapa_aprendidos_lower = {d["pergunta"].lower(): d for d in self.aprendidos}
        
        # Verificar correspondência exata nos aprendidos (case-sensitive primeiro)
        if pergunta_usuario in mapa_aprendidos:
            dado_encontrado = mapa_aprendidos[pergunta_usuario]
            self.logger.info(f"✅ Correspondência EXATA encontrada nos dados aprendidos: '{pergunta_usuario}'")
            return {"tag": "aprendido", "resposta": dado_encontrado["resposta_ensinada"]}
        
        # Verificar correspondência exata case-insensitive
        if pergunta_normalizada in mapa_aprendidos_lower:
            dado_encontrado = mapa_aprendidos_lower[pergunta_normalizada]
            self.logger.info(f"✅ Correspondência EXATA (case-insensitive) encontrada nos dados aprendidos: '{pergunta_usuario}'")
            return {"tag": "aprendido", "resposta": dado_encontrado["resposta_ensinada"]}
        
        # 4. Busca fuzzy nos aprendidos com threshold MUITO RIGOROSO
        matches_aprendidos = get_close_matches(pergunta_normalizada, perguntas_aprendidas, n=1, cutoff=0.9)

        if matches_aprendidos:
            melhor_pergunta_aprendida = matches_aprendidos[0]
            similaridade_aprendida = SequenceMatcher(None, pergunta_normalizada, melhor_pergunta_aprendida.lower()).ratio()
            self.logger.info(f"✅ Correspondência FUZZY encontrada nos dados aprendidos: '{pergunta_usuario}' -> '{melhor_pergunta_aprendida}' (similaridade: {similaridade_aprendida:.2f})")

            # Lógica Condicional de Confiança para dados aprendidos
            self.logger.info(f"Similaridade SequenceMatcher (aprendido): {similaridade_aprendida:.2f}")

            # 1. Alta Confiança (>=0.92): Aceita como erro de digitação.
            if similaridade_aprendida >= 0.92:
                self.logger.info("Alta confiança (aprendido), aceitando correspondência.")
                for dado in self.aprendidos:
                    if dado["pergunta"] == melhor_pergunta_aprendida:
                        return {"tag": "aprendido", "resposta": dado["resposta_ensinada"]}
            
            # 2. Confiança Média (>=0.9): Requer verificação Jaccard.
            elif similaridade_aprendida >= 0.9:
                tokens_usuario_aprendido = set(pergunta_normalizada.split())
                tokens_candidata_aprendido = set(melhor_pergunta_aprendida.lower().split())
                intersecao_aprendido = len(tokens_usuario_aprendido.intersection(tokens_candidata_aprendido))
                uniao_aprendido = len(tokens_usuario_aprendido.union(tokens_candidata_aprendido))
                jaccard_similarity_aprendido = intersecao_aprendido / uniao_aprendido if uniao_aprendido > 0 else 0
                self.logger.info(f"Confiança média (aprendido), verificando Jaccard: {jaccard_similarity_aprendido:.2f}")
                
                if jaccard_similarity_aprendido >= 0.95:
                    self.logger.info("Jaccard alto (aprendido), confirmando correspondência.")
                    for dado in self.aprendidos:
                        if dado["pergunta"] == melhor_pergunta_aprendida:
                            return {"tag": "aprendido", "resposta": dado["resposta_ensinada"]}
                
        self.logger.info(f"❌ Nenhuma correspondência encontrada para: '{pergunta_usuario}' - ativando fallback")
        return None

    def processar_mensagem(self, pergunta: str, personalidade: str) -> tuple[str, bool]:
        """
        🚀 MÉTODO CORRIGIDO - Solução para Issue Crítica #01
        🚀 ATUALIZADO - Suporte a respostas aleatórias (Task 09)
        
        Retorna a resposta do chatbot e uma flag indicando se é fallback.
        
        Args:
            pergunta: A pergunta do usuário
            personalidade: A personalidade a ser usada
            
        Returns:
            tuple[str, bool]: (resposta, is_fallback)
                - resposta: A resposta gerada pelo chatbot
                - is_fallback: True se for resposta de fallback, False caso contrário
        """
        melhor_intencao = self._achar_melhor_intencao(pergunta.lower())
        
        if melhor_intencao and melhor_intencao.get("tag") != "aprendido":
            respostas_pers = melhor_intencao.get("respostas", {}).get(personalidade, ["Desculpe, não tenho uma resposta para essa personalidade."])
            if isinstance(respostas_pers, list):
                resposta = random.choice(respostas_pers)
            else:
                resposta = respostas_pers
            return resposta, False
        
        elif melhor_intencao and melhor_intencao.get("tag") == "aprendido":
            return melhor_intencao["resposta"], False
        
        else:
            # Busca fallback
            fallback_intencao = next((i for i in self.intencoes if i.get("tag") == "fallback"), None)
            if fallback_intencao:
                respostas_fallback = fallback_intencao.get("respostas", {}).get(personalidade, ["Desculpe, não entendi."])
                if isinstance(respostas_fallback, list):
                    resposta = random.choice(respostas_fallback)
                else:
                    resposta = respostas_fallback
                return resposta, True  # 🚨 CORREÇÃO: Retorna True para indicar fallback
            else:
                fallback_respostas = ["Eu não sei a resposta para essa pergunta.", "Desculpe, não consegui processar isso."]
                return random.choice(fallback_respostas), True  # 🚨 CORREÇÃO: Retorna True para indicar fallback

    def processar_mensagem_cli(self, pergunta: str, personalidade: str) -> str:
        """
        Método de compatibilidade para interface CLI.
        Mantém a assinatura original para não quebrar o código CLI existente.
        
        Args:
            pergunta: A pergunta do usuário
            personalidade: A personalidade a ser usada
            
        Returns:
            str: A resposta do chatbot (sem flag de fallback)
        """
        resposta, _ = self.processar_mensagem(pergunta, personalidade)
        return resposta
    def ensinar_nova_resposta(self, pergunta: str, resposta: str) -> bool:
        """
        🚀 MÉTODO CORRIGIDO - Usa novo método de salvamento seguro
        """
        # Validação básica antes de chamar método seguro
        if not pergunta.strip() or not resposta.strip():
            self.logger.error("Pergunta ou resposta vazia rejeitada")
            return False
            
        return self._salvar_dados_aprendidos(pergunta, resposta)

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

            # Processar como mensagem normal usando método corrigido
            resposta, is_fallback = self.processar_mensagem(entrada_usuario, self.personalidade)
            print(f'Aline ({self.nome_personalidade}): {resposta}')
            
            # Se for fallback, perguntar se quer ensinar
            if is_fallback:
                quer_ensinar = input(f'Aline ({self.nome_personalidade}): Deseja me ensinar a resposta correta? (s/n) ').lower().strip()
                if quer_ensinar == 's':
                    self.aprender(entrada_usuario)

if __name__ == "__main__": # Execução do chatbot.
    CORE_DATA_FILE = 'core_data.json'
    NEW_DATA_FILE = 'new_data.json'
    
    aline_bot = Chatbot(core_data_path=CORE_DATA_FILE, new_data_path=NEW_DATA_FILE)
    
    aline_bot.iniciar_conversa()