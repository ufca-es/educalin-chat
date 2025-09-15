**UNIVERSIDADE FEDERAL DO CARIRI \- UFCA**  
**PRÓ-REITORIA DE GRADUAÇÃO \- PROGRAD**  
**CENTRO DE CIÊNCIA E TECNOLOGIA \- CCT**  
**CURSO DE BACHARELADO EM ENGENHARIA DE SOFTWARE**  
    
**ESPECIFICAÇÃO TRABALHO FINAL DA DISCIPLINA DE FUNDAMENTOS DE PROGRAMAÇÃO**

1. **Objetivo Geral**

Desenvolver, em grupos, um chatbot temático utilizando a linguagem Python, integrando conceitos fundamentais de programação, listas, funções, dicionários, manipulação de arquivos e organização modular com uso de classes. O projeto deve simular um atendimento interativo voltado a um domínio específico, como Educação, Saúde, Turismo, Atendimento ao Cliente, Sustentabilidade, entre outros.

2. **Objetivos de Aprendizagem**  
* Consolidar o uso de listas, dicionários, estruturas condicionais e de repetição.  
* Praticar a modularização de códigos com uso de funções e classes.  
* Aprender a separar lógica de negócio da interface com o usuário.  
* Ler e gravar dados em arquivos textos.  
* Utilizar Git e GitHub para documentação e controle de versão do projeto.  
* Desenvolver habilidades de projeto em equipe e resolução de problemas reais.

**3\. Requisitos Educacionais Obrigatórios do Projeto**  
O chatbot deve:

* Ser implementado com uso de classes (no mínimo classes de domínio);  
* Ter interface interfaces gráficas de usuário  (GUI) em Python;  
* Ter fluxo de atendimento com tomada de decisão (condicionais);  
* Utilizar listas para armazenar dados temporários;  
* Utilizar dicionários para representar entidades ou mapeamentos;  
* Ler dados de um arquivo .txt (como base de perguntas, dados de usuários etc.);  
* Gerar um relatório (arquivo texto) com o resumo da interação;  
* Possuir código modularizado: organização em funções e classes;  
* Fazer uso de docstrings (strings de documentação) para descrever módulos, classes, funções e métodos.  
* Ser documentado em um repositório público no GitHub.

**4\. Requisitos Funcionais do Projeto**

* **Conversação básica com dicionário**  
  * O chatbot deve responder perguntas com base em um dicionário de perguntas e respostas.  
  * Deve verificar se a entrada do usuário contém palavras-chave.  
* **Histórico de conversas**  
  * Registrar todas as interações (pergunta e resposta) em um arquivo `.txt`.  
  * Ao iniciar, exibir as **últimas 5 interações anteriores** (se existirem).  
* **Modo de aprendizagem**  
* Caso não saiba responder:  
  * Solicitar ao usuário uma resposta apropriada;  
  * Salvar essa nova pergunta e resposta em um arquivo separado (ex: `aprendizado.txt`);  
* **Personalidades**  
  * Deve haver ao menos **3 estilos de resposta**:  
    * **formal** – que fornece respostas educadas e formais.  
    * **engraçado** – que fornece respostas com humor ou gírias.  
    * **rude** – que fornece respostas diretas e impacientes.  
    * outras: os desenvolvedores podem pensar em outros estilos de respostas que o chatbot pode fornecer.  
  * Observações:  
    * A personalidade afeta **o modo de responder**, mas **não o conteúdo**.  
    * O usuário escolhe a personalidade ao iniciar o sistema e pode trocá-la durante a execução.  
    * O sistema deve manter um **contador de quantas vezes cada personalidade foi usada** (com persistência em arquivo).  
* **Respostas variadas**  
  * Para perguntas conhecidas, o chatbot deve oferecer respostas aleatórias entre múltiplas variações salvas para a mesma pergunta.  
* **Estatísticas e recomendações**  
  * Ao final da execução, o chatbot deve exibir:  
    * Número total de interações;  
    * A pergunta mais frequente da sessão;  
    * Sugestões de perguntas com base nas mais feitas;  
* Quantas vezes cada personalidade foi usada (acumulado).

**5\. Questão de Pesquisa** 

**Como um chatbot pode auxiliar as pessoas a interagirem melhor com sua cidade, sociedade ou comunidade?**

**6\. Grupos**  
O trabalho deve ser realizado em grupos de no máximo quatro estudantes, sendo que os grupos devem ser mantidos em todas as demais etapas deste trabalho prático. Caso haja problema na formação dos grupos, contatem os professores para discutir a solução.

**7\. Entrega**  
O trabalho deverá ser constantemente atualizado na Wiki do projeto no repositório Git. A entrega final será realizada via Tarefa “Submissão Entrega Trabalho Prático” a ser publicada no Classroom de Fundamentos de Programação, em que um integrante do grupo deverá submeter a Tag do Git com a indicação do último Commit realizado. Além disso, cada grupo deverá preparar uma apresentação para expor o funcionamento do software, bem como resumindo os principais pontos do trabalho desenvolvido. Todos os integrantes do grupo devem participar da apresentação. O tempo máximo da apresentação é 20 minutos (15 min explanação \+ 5 min de perguntas).

**8\. Avaliação**  
A nota considerará:

* Entregas parciais nos encontros (comprometimento e progresso);  
* Corretude e robustez do chatbot final;  
* Uso adequado dos recursos obrigatórios;  
* Criatividade e adequação do tema escolhido;  
* Documentação e organização do repositório GitHub.

**10\. Entregas e Acompanhamento**:

| Encontros | Objetivos de Aprendizagem | Entregas Obrigatórias |
| ----- | ----- | ----- |
| **Entrega 01 \- Planejamento (05/09/2025) 20% da Nota Final do Trabalho. Avaliação de 0 a 10** | Compreender o escopo do projeto; Aplicar organização modular; Utilizar listas e dicionários na base de conhecimento; Planejar classes e métodos. | **Task 01:** Definição do **tema do chatbot** (ex: saúde, educação, turismo, atendimento ao cliente, etc). **Task 02:** Definição das **personalidades do bot** (pelo menos 3: formal, engraçada, rude, etc). \-  **Task 03:** Rascunho do **fluxo básico de conversa** (mínimo 3 tipos de pergunta por personalidade). \- tok **Task 04:** Esboço das **classes de domínio** e **módulos do projeto** (ex: `ChatBot`, `Historico`, `Personalidade`, etc.). \-  **Task 05:** Configuração do **repositório no GitHub** (com estrutura básica e README inicial). **Task 06:** Criação do **arquivo de perguntas/respostas** (formato `.txt` ou `.json`). \-  **Task 07:** Início da implementação da **interface principal** (loop de conversação simples via terminal).  |
| **Entrega 02 \- Funcionalidades intermediárias (10/09/2025) 20% da Nota Final do Trabalho. Avaliação de 0 a 10** | Usar leitura/escrita em arquivos (`open`, `read`, `write`); Modularizar funcionalidades com funções e classes; Trabalhar com estruturas condicionais e de repetição em fluxos reais.  | **Task 08:** Implementação da **mudança de personalidade** durante a execução. **Task 09:** Uso de **respostas aleatórias** para a mesma pergunta. **Task 10:** Implementação da **persistência de aprendizado** (arquivo separado para novas perguntas). **Task 11:** Leitura do **histórico anterior ao iniciar o programa** (últimas 5 interações). **Task 12:** Armazenamento do **histórico de conversas da sessão** em arquivo `.txt`. |
| **Entrega 03 \- Estatísticas, relatórios e refinamentos (12/09/2025) 20% da Nota Final do Trabalho. Avaliação de 0 a 10** | Compreender escopo de funções utilitárias; Realizar análise de dados simples (ex: contagem, ranking); Trabalhar com geração de relatórios automatizados.  | **Task 13:** Implementação da **coleta de estatísticas**: Número total de interações; Pergunta mais feita da sessão; Quantas vezes cada personalidade foi usada; **Task 14:** Geração de **relatório legível ao usuário final** (`relatorio.txt`); **Task 15:** Exibição de **sugestões de perguntas frequentes**; **Task 16:** Organização final das **classes e arquivos** em módulos distintos. |
| **Entrega Final – Apresentação e Documentação 40% da Nota Final do Trabalho. Avaliação de 0 a 10** |  | Repositório completo no GitHub com: **Task 17:** Código-fonte organizado por módulos; **Task 18:** Arquivos de dados (`.txt` ou `.json`); **Task 19:** Relatório final (`relatorio.txt`); **Task 20:** Histórico (`historico.txt`); **Task 21:** Arquivo de aprendizado (`aprendizado.txt`); **Task 22:** README.md completo com: Descrição do projeto; Como executar; Integrantes e funções de cada um; Demonstrações (prints ou vídeos). **Task 23:** Apresentação breve (15 min) explicando: Tema e público-alvo do bot; Funcionalidades implementadas; Principais dificuldades e aprendizados. |