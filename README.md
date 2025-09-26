# EducAlin - Aline Chat 🤖📚

> Um chatbot educacional inteligente em Python que auxilia estudantes de matemática básica com diferentes personalidades pedagógicas.

<div align="center">
  
  [![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
  [![Gradio](https://img.shields.io/badge/Gradio-Interface%20Web-orange.svg)](https://gradio.app/)
  [![Status](https://img.shields.io/badge/Status-95%25%20Concluído-green.svg)](docs/STATUS_REQUISITOS.md)
  [![Issues Críticas](https://img.shields.io/badge/Issues%20Críticas-0-brightgreen.svg)](docs/STATUS_REQUISITOS.md#-issues-críticas-de-código-identificadas)

</div>

---

## 📋 Índice

- [EducAlin - Aline Chat 🤖📚](#educalin---aline-chat-)
  - [📋 Índice](#-índice)
  - [📖 Sobre o Projeto](#-sobre-o-projeto)
    - [🎯 Objetivos](#-objetivos)
  - [✨ Funcionalidades](#-funcionalidades)
    - [🔥 Principais Features](#-principais-features)
  - [🖥️ Interfaces Disponíveis](#️-interfaces-disponíveis)
    - [🌐 Interface Web (Gradio)](#-interface-web-gradio)
    - [Tópicos Cobertos](#tópicos-cobertos)
  - [🎭 Personalidades](#-personalidades)
    - [👩‍🏫 Aline Formal (Professora)](#-aline-formal-professora)
    - [😄 Aline Engraçada (Coach Leve)](#-aline-engraçada-coach-leve)
    - [🎯 Aline Desafiadora (Professora Exigente)](#-aline-desafiadora-professora-exigente)
    - [💝 Aline Empática (Mentora Gentil)](#-aline-empática-mentora-gentil)
  - [🚀 Como Executar](#-como-executar)
    - [Pré-requisitos](#pré-requisitos)
    - [📦 Instalação](#-instalação)
    - [🌐 Interface Web (Gradio)](#-interface-web-gradio-1)
    - [🧪 Testes](#-testes)
    - [🔧 Dependências](#-dependências)
      - [Processamento](#processamento)
      - [Interface Web (app.py)](#interface-web-apppy)
  - [📁 Estrutura do Projeto](#-estrutura-do-projeto)
    - [📄 Arquivos Principais](#-arquivos-principais)
      - [🔧 **Código Fonte**](#-código-fonte)
      - [📊 **Dados**](#-dados)
      - [📋 **Documentação**](#-documentação)
      - [🧪 **Testes**](#-testes-1)
      - [🎨 **Interface do Usuário (UI)**](#-interface-do-usuário-ui)
      - [📄 **Relatórios**](#-relatórios)
  - [💬 Exemplo de Uso](#-exemplo-de-uso)
    - [🌐 Interface Web (Gradio)](#-interface-web-gradio-2)
    - [🧠 Sistema de Aprendizado](#-sistema-de-aprendizado)
  - [⚙️ Tecnologias Utilizadas](#️-tecnologias-utilizadas)
    - [🐍 **Core**](#-core)
    - [🌐 **Interface Web**](#-interface-web)
    - [📚 **Bibliotecas Utilizadas**](#-bibliotecas-utilizadas)
      - [Nativas do Python](#nativas-do-python)
      - [Externas](#externas)
  - [⚠️ Limitações Conhecidas](#️-limitações-conhecidas)
    - [🚨 **Issues Críticas de Código**](#-issues-críticas-de-código)
  - [📈 Progresso do Projeto](#-progresso-do-projeto)
    - [📊 **Status Atual: 95% Concluído** (Task 23 em andamento)](#-status-atual-95-concluído-task-23-em-andamento)
    - [🎯 **Principais Conquistas**](#-principais-conquistas)
    - [🔜 **Próximas Prioridades**](#-próximas-prioridades)
  - [🤝 Contribuição](#-contribuição)
    - [Como Contribuir](#como-contribuir)
    - [📝 Diretrizes](#-diretrizes)
      - [🔧 **Código**](#-código)
      - [📊 **Conteúdo**](#-conteúdo)
      - [🚨 **Prioridades Atuais**](#-prioridades-atuais)
      - [📋 **Documentação**](#-documentação-1)
  - [👥 Equipe](#-equipe)
  - [🔗 Links Úteis](#-links-úteis)

---

## 📖 Sobre o Projeto

O **EducAlin - Aline** é um chatbot educacional desenvolvido como projeto acadêmico que visa auxiliar estudantes no aprendizado de matemática básica. O sistema utiliza processamento de linguagem natural simples e oferece diferentes personalidades pedagógicas para se adaptar ao estilo de aprendizagem de cada aluno.

### 🎯 Objetivos

- Fornecer suporte educacional personalizado em matemática básica
- Oferecer diferentes abordagens pedagógicas através de personalidades distintas
- Criar uma experiência de aprendizado interativa e envolvente
- Manter histórico de aprendizado e permitir evolução do conhecimento

---

## ✨ Funcionalidades

### 🔥 Principais Features

- **🎭 4 Personalidades Distintas**: Formal, Engraçada, Desafiadora e Empática
- **🌐 Interface Web (Gradio)**
- **🧠 Sistema de Aprendizado**: Capaz de aprender novas respostas através da interação
- **📚 Base de Conhecimento**: Conhecimento pré-programado em matemática básica
- **🔍 Busca Inteligente**: Correspondência fuzzy para entender variações de perguntas
- **💾 Persistência de Dados**: Salva novos aprendizados em arquivo JSON
- **📜 Sistema de Histórico**: Carregamento e salvamento das últimas 5 interações com timestamps, preparando para estatísticas
- **Troca Dinâmica de Personalidade**: Mudança durante a conversa via dropdown interativo
- **🎲 Respostas Aleatórias**: Variabilidade nas respostas para a mesma pergunta, melhorando engajamento
- **🛡️ Correções de Segurança**: Issues críticas resolvidas para maior robustez
- **🎯 Arquitetura Limpa**: Separação clara entre lógica e apresentação

## 🖥️ Interfaces Disponíveis

### 🌐 Interface Web (Gradio)
- **Arquivo**: [`app.py`](app.py)
- **Recursos**: Troca dinâmica de personalidade, interface gráfica intuitiva, histórico visual
- **Ideal para**: Usuários finais, demonstrações, uso educacional
- **Acesso**: Interface web local com compartilhamento opcional

###  Tópicos Cobertos

- Máximo Divisor Comum (MDC)
- Mínimo Múltiplo Comum (MMC)
- Frações Equivalentes
- Operações Básicas (Soma, Subtração)
- Ordem das Operações (PEMDAS)
- Suporte motivacional para dificuldades de aprendizado

---

## 🎭 Personalidades

O bot adapta sua forma de comunicação através de 4 personalidades distintas:

### 👩‍🏫 Aline Formal (Professora)
- **Perfil**: Direta, objetiva e focada no conteúdo
- **Estilo**: Linguagem técnica e explicações estruturadas
- **Ideal para**: Estudantes que preferem abordagem tradicional

### 😄 Aline Engraçada (Coach Leve)
- **Perfil**: Usa analogias criativas e tom descontraído
- **Estilo**: Metáforas divertidas e linguagem coloquial
- **Ideal para**: Estudantes que aprendem melhor com humor

### 🎯 Aline Desafiadora (Professora Exigente)
- **Perfil**: Instiga o aluno a construir o próprio raciocínio
- **Estilo**: Perguntas socráticas e desafios progressivos
- **Ideal para**: Estudantes que gostam de pensar ativamente

### 💝 Aline Empática (Mentora Gentil)
- **Perfil**: Usa linguagem amigável e suporte emocional
- **Estilo**: Encorajamento e abordagem passo a passo
- **Ideal para**: Estudantes com ansiedade ou baixa autoestima

---

## 🚀 Como Executar

### Pré-requisitos

- Python 3.9 ou superior
- Sistema operacional: Windows, macOS ou Linux

### 📦 Instalação

1. **Clone o repositório**
   ```bash
   git clone https://github.com/ufca-es/educalin-chat.git
   cd educalin-chat
   ```

2. **Instale as dependências** (apenas para interface web)
   ```bash
   pip install -r requirements.txt
   ```


### 🌐 Interface Web (Gradio)

```bash
python app.py
```

**Funcionalidades:**
- Interface gráfica intuitiva
- Troca dinâmica de personalidade via dropdown
- Histórico visual de conversas
- Sistema de ensino com botões dedicados
- Acesso via navegador (normalmente http://localhost:7860)

### 🧪 Testes
O projeto inclui uma suíte de testes abrangente para garantir a qualidade e a funcionalidade do chatbot. Para executar todos os testes, navegue até o diretório `tests/` e execute os arquivos de teste individualmente ou use um executor de testes como `pytest`.

- **[`tests/test_correções_criticas.py`](tests/test_correções_criticas.py)**: Valida correções para issues críticas, como problemas de encoding e thresholds de similaridade.
- **[`tests/test_historico.py`](tests/test_historico.py)**: Testa o sistema de histórico de interações, incluindo carregamento, salvamento e rotação.
- **[`tests/test_issue_critica_01.py`](tests/test_issue_critica_01.py)**: Verifica a correção da Issue Crítica #01, focando na detecção de fallback e no fluxo de aprendizado via Gradio.
- **[`tests/test_personalidade.py`](tests/test_personalidade.py)**: Garante a funcionalidade de troca dinâmica de personalidade e a consistência das respostas.
- **[`tests/test_respostas_aleatorias.py`](tests/test_respostas_aleatorias.py)**: Confirma a variabilidade nas respostas do chatbot e o comportamento de fallback.
- **[`tests/test_stats_and_sessions.py`](tests/test_stats_and_sessions.py)**: Valida a coleta de estatísticas de uso e o gerenciamento de sessões.

### 🔧 Dependências

#### Processamento
- **Pytz**: Biblioteca para conversão de timezones


#### Interface Web (app.py)
- **Gradio** - Para interface web interativa
- Consulte [`requirements.txt`](requirements.txt) para versões específicas

---

## 📁 Estrutura do Projeto

```
educalin-chat/
├── .gitignore
├── app.py                      # Interface Web - Gradio
├── requirements.txt            # Dependências Python
├── core/
│   ├── chatbot.py              # Lógica principal do chatbot
│   ├── faq_suggestions.py      # Sugestões de FAQ
│   ├── intent_matcher.py       # Mapeamento de intenções
│   ├── personalities.py        # Definição das personalidades
│   └── validation.py           # Funções de validação
├── data/
│   ├── core_data.json          # Base de conhecimento principal
│   ├── historico.json          # Histórico de interações (gerado automaticamente)
│   ├── new_data.json           # Dados aprendidos (gerado automaticamente)
│   └── stats.json              # Estatísticas de uso (gerado automaticamente)
├── docs/
│   ├── ANALISE_CRITICA_RESULTOS_UAT.md # Análise de resultados UAT
│   ├── ANALISE_ERRO_UNPACKING.MD       # Análise de erro de unpacking
│   ├── ANALISE_ISSUE_CRITICA_01.MD     # Análise da Issue Crítica #01
│   ├── espec_trabalho.md               # Especificação completa do projeto
│   ├── image-1.png                     # Imagem de documentação
│   ├── image.png                       # Imagem de documentação
│   ├── IMPLEMENTACAO_PRATICA_SOLUCOES.md # Implementação prática de soluções
│   ├── PERSONALIDADE_DINAMICA.md       # Documentação da troca dinâmica de personalidade
│   ├── plano_task13.md                 # Plano da Task 13
│   ├── PLANO_TESTE_UAT_CORRECOES_CRITICAS_009_015.md # Plano de teste UAT
│   ├── PLANO_TESTE_UAT_ISSUE_CRITICA_01.md # Plano de teste UAT
│   ├── PLANO_TESTE_UAT_TASK13.md         # Plano de teste UAT
│   ├── RELATORIO_CORRECAO_IMPLEMENTADA.md # Relatório de correção implementada
│   ├── RELATORIO_FINAL_CORRECOES_UAT.md   # Relatório final de correções UAT
│   ├── RESULTADOS_TESTE_UAT_CORRECOES_CRITICAS.md # Resultados de teste UAT
│   ├── RESULTADOS_TESTE_UAT_ISSUE_CRITICA_01.md # Resultados de teste UAT
│   ├── RESULTADOS_TESTE_UAT_TASK_13.md   # Resultados de teste UAT
│   ├── SOLUCOES_TECNICAS_UAT_CRITICAS.md # Soluções técnicas UAT
│   └── STATUS_REQUISITOS.md            # Relatório de progresso do projeto
├── infra/
│   ├── file_atomic.py          # Operações atômicas de arquivo
│   ├── logging_conf.py         # Configuração de logging
│   └── repositories.py         # Repositórios de dados
├── reports/
│   ├── logs/                   # Logs gerados pelo sistema
│   └── relatório.txt           # Relatório de testes (exemplo)
├── tests/
│   ├── test_correções_criticas.py  # Testes para correções críticas
│   ├── test_historico.py           # Testes para o sistema de histórico
│   ├── test_issue_critica_01.py    # Testes para a Issue Crítica #01
│   ├── test_personalidade.py       # Suite de testes para personalidades
│   ├── test_respostas_aleatorias.py # Teste de variabilidade de respostas
│   └── test_stats_and_sessions.py # Testes para estatísticas e sessões
└── ui/
    ├── educalin_theme.py           # Tema visual personalizado para Gradio
    ├── logo_educalin-chat.svg      # Logo do projeto
    └── style.css                   # Estilos CSS para a interface Gradio
```

### 📄 Arquivos Principais

#### 🔧 **Código Fonte**
- **[`app.py`](app.py)**: Interface web Gradio, integração com a lógica do chatbot.
- **`core/`**: Contém a lógica principal do chatbot.
    - **[`core/chatbot.py`](core/chatbot.py)**: Lógica central do chatbot, processamento de mensagens e integração com repositórios.
    - **[`core/intent_matcher.py`](core/intent_matcher.py)**: Mapeamento de intenções e lógica de correspondência.
    - **[`core/personalities.py`](core/personalities.py)**: Definição e gerenciamento das personalidades.
    - **[`core/validation.py`](core/validation.py)**: Funções de validação de entrada.
    - **[`core/faq_suggestions.py`](core/faq_suggestions.py)**: Lógica para sugestões de FAQ.
- **`infra/`**: Contém a infraestrutura de dados e logging.
    - **[`infra/repositories.py`](infra/repositories.py)**: Repositórios para acesso e persistência de dados (Core, Learned, History, Stats).
    - **[`infra/file_atomic.py`](infra/file_atomic.py)**: Funções para operações atômicas de arquivo.
    - **[`infra/logging_conf.py`](infra/logging_conf.py)**: Configuração de logging.
- **[`requirements.txt`](requirements.txt)**: Dependências Python necessárias.

#### 📊 **Dados**
- **`data/`**: Contém todos os arquivos JSON de dados.
    - **[`data/core_data.json`](data/core_data.json)**: Base de conhecimento principal com intenções e respostas.
    - **[`data/new_data.json`](data/new_data.json)**: Dados aprendidos dinamicamente pelo chatbot.
    - **[`data/historico.json`](data/historico.json)**: Histórico de interações do chatbot.
    - **[`data/stats.json`](data/stats.json)**: Estatísticas de uso do chatbot.

#### 📋 **Documentação**
- **`docs/`**: Contém toda a documentação do projeto.
    - **[`README.md`](README.md)**: Documentação principal (este arquivo).
    - **[`STATUS_REQUISITOS.md`](docs/STATUS_REQUISITOS.md)**: Análise detalhada de progresso.
    - **[`PERSONALIDADE_DINAMICA.md`](docs/PERSONALIDADE_DINAMICA.md)**: Documentação da troca dinâmica de personalidade.
    - **[`espec_trabalho.md`](docs/espec_trabalho.md)**: Especificação técnica completa do projeto.
    - Outros arquivos de documentação e relatórios de teste.

#### 🧪 **Testes**
- **`tests/`**: Contém todos os testes unitários e de integração.
    - **[`tests/test_correções_criticas.py`](tests/test_correções_criticas.py)**: Testes para correções críticas.
    - **[`tests/test_historico.py`](tests/test_historico.py)**: Testes para o sistema de histórico.
    - **[`tests/test_issue_critica_01.py`](tests/test_issue_critica_01.py)**: Testes para a Issue Crítica #01.
    - **[`tests/test_personalidade.py`](tests/test_personalidade.py)**: Suite de testes para funcionalidades de personalidade.
    - **[`tests/test_respostas_aleatorias.py`](tests/test_respostas_aleatorias.py)**: Teste de variabilidade de respostas.
    - **[`tests/test_stats_and_sessions.py`](tests/test_stats_and_sessions.py)**: Testes para estatísticas e sessões.

#### 🎨 **Interface do Usuário (UI)**
- **`ui/`**: Contém arquivos relacionados à interface do usuário.
    - **[`ui/educalin_theme.py`](ui/educalin_theme.py)**: Tema visual personalizado para Gradio.
    - **[`ui/logo_educalin-chat.svg`](ui/educalin-chat.svg)**: Logo do projeto.
    - **[`ui/style.css`](ui/style.css)**: Estilos CSS para a interface Gradio.

#### 📄 **Relatórios**
- **`reports/`**: Contém arquivos de relatórios e logs.
    - **[`reports/relatório.txt`](reports/relatório.txt)**: Exemplo de relatório de testes ou logs.

---

## 💬 Exemplo de Uso

### 🌐 Interface Web (Gradio)

A interface web oferece:
- **Dropdown de Personalidade**: Troca dinâmica entre as 4 personalidades
- **Chat Visual**: Histórico de conversas com interface limpa
- **Botões de Ação**: "Enviar", "Ensinar", "Pular", "Limpar Chat"
- **Sistema de Ensino**: Interface dedicada para ensinar novas respostas
- **Acesso Web**: Disponível em `http://localhost:7860` após executar `python app.py`

### 🧠 Sistema de Aprendizado

```
Você: como calcular raiz quadrada?
Aline (Engraçada): Opa, essa aí passou batido pelo meu radar! Tenta me perguntar de outro jeito, quem sabe a gente não se entende?

# Web: Campo de texto dedicado + botão "Ensinar"
Aline (Engraçada): Obrigada! Aprendi uma nova resposta.
```

---

## ⚙️ Tecnologias Utilizadas

### 🐍 **Core**
- **Python 3.9+**: Linguagem principal
- **JSON**: Armazenamento de dados estruturados
- **difflib**: Correspondência fuzzy para processamento de linguagem natural
- **typing**: Anotações de tipo para melhor código

### 🌐 **Interface Web**
- **Gradio**: Framework para interfaces web interativas
- **HTML/CSS/JS**: Renderização automática via Gradio

### 📚 **Bibliotecas Utilizadas**

#### Nativas do Python
- `json`: Manipulação de dados JSON
- `difflib.get_close_matches`: Busca de correspondência aproximada
- `typing`: Tipagem estática para melhor manutenibilidade

#### Externas
- `gradio`: Interface web interativa e responsiva
- `pytz`: Biblioteca para conversão de timezones

---

## ⚠️ Limitações Conhecidas

### 🚨 **Issues Críticas de Código**
- ✅ **Issue Crítica #01 RESOLVIDA**: String matching frágil corrigido com uso de flag booleana (`is_fallback`)
- ✅ **Issue Crítica #02 RESOLVIDA**: Acesso não seguro a dicionários corrigido ([`app.py`](app.py))

---

## 📈 Progresso do Projeto

### 📊 **Status Atual: 95% Concluído** (Task 23 em andamento)

| Categoria | Progresso | Status |
|-----------|-----------|--------|
| 🎯 **Planejamento e Base** | 100% | ✅ Completo |
| ⚙️ **Funcionalidades Core** | 100% | ✅ Completo |
| 📈 **Estatísticas/Relatórios** | 100% | ✅ Completo |
| 🗂️ **Organização/Modularização** | 100% | ✅ Completo |
| 📄 **Entrega Final** | 100% | ✅ Completo |

### 🎯 **Principais Conquistas**
- ✅ Interface CLI completa e funcional 
- ✅ Interface Web Gradio implementada
- ✅ Troca dinâmica de personalidade em ambas interfaces
- ✅ Sistema de histórico implementado com carregamento das últimas 5 interações, salvamento atômico e preparação para estatísticas
- ✅ Acesso seguro a dicionários implementado
- ✅ Sistema de aprendizado robusto
- ✅ 4 personalidades pedagógicas funcionais
- ✅ Base de conhecimento rica (7 intenções)
- ✅ Arquitetura limpa e bem estruturada

### 🔜 **Próximas Prioridades**
1. 🗂️ **Task 23**: Finalizar documentação e apresentação final

*Para análise completa, consulte [STATUS_REQUISITOS.md](docs/STATUS_REQUISITOS.md)*

---

## 🤝 Contribuição

Quer contribuir com o EducAlin? Ficamos felizes em receber sua ajuda!

### Como Contribuir

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

### 📝 Diretrizes

#### 🔧 **Código**
- Siga o padrão PEP 8 para código Python
- Mantenha a lógica do chatbot em `core/` e a interface em `app.py`.
- Teste a interface Web ao fazer alterações.
- Use type hints para melhor manutenibilidade.

#### 📊 **Conteúdo**
- Adicione novos tópicos em [`data/core_data.json`](data/core_data.json) seguindo a estrutura existente
- Teste todas as 4 personalidades ao adicionar novas respostas
- Mantenha consistência no tom de cada personalidade

#### 🚨 **Prioridades Atuais**
- Implementar sistema de histórico
- Adicionar respostas aleatórias
- Modularização adicional do código
- Melhorar sistema de testes automatizados

#### 📋 **Documentação**
- Documente mudanças significativas no README
- Atualize [`docs/STATUS_REQUISITOS.md`](docs/STATUS_REQUISITOS.md) se aplicável
- Mantenha exemplos de uso atualizados

---

## 👥 Equipe

| Nome | GitHub | Papel |
|------|--------|-------|
| Davi Maia Soares | [@davimso](https://github.com/davimso) | Criação da base de dados core data.json <br> Primeira implementação de troca dinâmica de personalidade na GUI <br> Implementação inicial e final da interface gráfica |
| Elder Rayan Oliveira Silva | [@eldrayan](https://github.com/eldrayan) | Sugestão de perguntas frequentes para o usuário <br> Implementação de histórico e solicitação do mesmo <br> Primeira implementação de troca dinâmica de personalidade na CLI |
| Pedro Yan Alcantara Palácio | [@pedropalacioo](https://github.com/pedropalacioo) | MVP CLI <br> Primeira implementação de troca dinâmica de personalidade na CLI <br>  Modularização <br> Geração de relatórios <br> Alterações na interface com CSS |
| Samuel Wagner Tiburi Silveira | [@samsilveira](https://github.com/samsilveira) | Configuração no GitHub e `README.md` <br> Melhora na implementação de troca dinâmica de personalidade na CLI <br> Respostas aleatórias para a mesma pergunta <br> Melhoria do intent matcher <br> Coleta de estatísticas <br> Testes e integrações |
| Jayr Alencar Pereira | [@jayralencar](https://github.com/jayralencar) | Professor Orientador |

---

## 🔗 Links Úteis

- 📊 [Relatório de Progresso](docs/STATUS_REQUISITOS.md) - Status atual dos requisitos
- 📋 [Especificação Completa](docs/espec_trabalho.md) - Documento de especificação
- 🐛 [Reportar Bug](https://github.com/ufca-es/educalin-chat/issues/new?assignees=&labels=bug&template=bug_report.md) - Encontrou um problema?
- 💡 [Sugerir Feature](https://github.com/ufca-es/educalin-chat/issues/new?assignees=&labels=feature&template=feature_request.md) - Tem uma ideia?
- 📈 [Painel de Issues](https://github.com/ufca-es/educalin-chat/issues) - Acompanhe o desenvolvimento


---

<div align="center">

**Desenvolvido pela equipe EducAlin**

</div>
