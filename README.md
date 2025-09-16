# EducAlin - Aline Chat 🤖📚

> Um chatbot educacional inteligente em Python que auxilia estudantes de matemática básica com diferentes personalidades pedagógicas.

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Gradio](https://img.shields.io/badge/Gradio-Interface%20Web-orange.svg)](https://gradio.app/)
[![Status](https://img.shields.io/badge/Status-53.3%25%20Concluído-green.svg)](docs/STATUS_REQUISITOS.md)
[![Issues Críticas](https://img.shields.io/badge/Issues%20Críticas-0-brightgreen.svg)](docs/STATUS_REQUISITOS.md#-issues-críticas-de-código-identificadas)

---

## 📋 Índice

- [EducAlin - Aline Chat 🤖📚](#educalin---aline-chat-)
  - [📋 Índice](#-índice)
  - [📖 Sobre o Projeto](#-sobre-o-projeto)
    - [🎯 Objetivos](#-objetivos)
  - [✨ Funcionalidades](#-funcionalidades)
    - [🔥 Principais Features](#-principais-features)
  - [🖥️ Interfaces Disponíveis](#️-interfaces-disponíveis)
    - [💻 Interface Terminal (CLI)](#-interface-terminal-cli)
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
    - [🖥️ Interface Terminal (CLI)](#️-interface-terminal-cli)
    - [🌐 Interface Web (Gradio)](#-interface-web-gradio-1)
    - [🧪 Testes](#-testes)
    - [🔧 Dependências](#-dependências)
      - [Interface CLI (main.py)](#interface-cli-mainpy)
      - [Interface Web (app.py)](#interface-web-apppy)
  - [📁 Estrutura do Projeto](#-estrutura-do-projeto)
    - [📄 Arquivos Principais](#-arquivos-principais)
      - [🔧 **Código Fonte**](#-código-fonte)
      - [📊 **Dados**](#-dados)
      - [📋 **Documentação**](#-documentação)
  - [💬 Exemplo de Uso](#-exemplo-de-uso)
    - [💻 Interface Terminal (CLI)](#-interface-terminal-cli-1)
    - [🌐 Interface Web (Gradio)](#-interface-web-gradio-2)
    - [🧠 Sistema de Aprendizado (Ambas Interfaces)](#-sistema-de-aprendizado-ambas-interfaces)
  - [⚙️ Tecnologias Utilizadas](#️-tecnologias-utilizadas)
    - [🐍 **Core**](#-core)
    - [🌐 **Interface Web**](#-interface-web)
    - [📚 **Bibliotecas Utilizadas**](#-bibliotecas-utilizadas)
      - [Nativas do Python](#nativas-do-python)
      - [Externas](#externas)
  - [⚠️ Limitações Conhecidas](#️-limitações-conhecidas)
    - [🚨 **Issues Críticas de Código**](#-issues-críticas-de-código)
    - [🔄 **Funcionalidades Pendentes**](#-funcionalidades-pendentes)
    - [📋 **Arquivos de Entrega**](#-arquivos-de-entrega)
  - [📈 Progresso do Projeto](#-progresso-do-projeto)
    - [📊 **Status Atual: 53.3% Concluído** (após Task 09)](#-status-atual-533-concluído-após-task-09)
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
- **🖥️ Dupla Interface**: Terminal (CLI) e Interface Web (Gradio)
- **🧠 Sistema de Aprendizado**: Capaz de aprender novas respostas através da interação
- **📚 Base de Conhecimento**: Conhecimento pré-programado em matemática básica
- **🔍 Busca Inteligente**: Correspondência fuzzy para entender variações de perguntas
- **💾 Persistência de Dados**: Salva novos aprendizados em arquivo JSON
- **🔄 Troca Dinâmica de Personalidade**: Mudança durante a conversa em **ambas interfaces**
  - **CLI**: Comandos especiais `/personalidade [nome]` e `/help`
  - **Web**: Dropdown interativo com troca instantânea
- **🎲 Respostas Aleatórias (Task 09)**: Variabilidade nas respostas para a mesma pergunta, melhorando engajamento - [Issue #10](https://github.com/ufca-es/educalin-chat/issues/10)
- **🛡️ Correções de Segurança**: Issues críticas resolvidas para maior robustez
- **🎯 Arquitetura Limpa**: Separação clara entre lógica e apresentação

## 🖥️ Interfaces Disponíveis

### 💻 Interface Terminal (CLI)
- **Arquivo**: [`main.py`](main.py)
- **Recursos**: Seleção inicial de personalidade, **troca dinâmica via comandos**, chat interativo, sistema de aprendizado
- **Comandos Especiais**: `/personalidade [nome]`, `/help`
- **Ideal para**: Desenvolvimento, testes, uso em servidores
- **📋 Documentação**: Veja [`PERSONALIDADE_DINAMICA.md`](PERSONALIDADE_DINAMICA.md) para detalhes completos

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

### 🖥️ Interface Terminal (CLI)

```bash
python main.py
```

**Funcionalidades:**
- Seleção inicial de personalidade (1-4)
- **Troca dinâmica**: `/personalidade [nome]` durante a conversa
- **Comandos de ajuda**: `/help` para ver opções disponíveis
- Chat interativo no terminal
- Sistema de aprendizado integrado
- Digite `quit` para sair

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
- **Testes Unitários**: Execute `python test_*.py` para validar correções críticas, personalidades e variabilidade de respostas.
- **Teste de Variabilidade (Task 09)**: `python test_respostas_aleatorias.py` - Confirma aleatoriedade em respostas e fallback.

### 🔧 Dependências

#### Interface CLI (main.py)
- **Sem dependências externas** - Usa apenas bibliotecas nativas do Python

#### Interface Web (app.py)
- **Gradio** - Para interface web interativa
- Consulte [`requirements.txt`](requirements.txt) para versões específicas

---

## 📁 Estrutura do Projeto

```
educalin-chat/
├── main.py                     # Interface CLI - Chatbot principal
├── app.py                      # Interface Web - Gradio
├── core_data.json              # Base de conhecimento principal
├── new_data.json              # Dados aprendidos (gerado automaticamente)
├── test_personalidade.py      # Suite de testes para Task 08
├── test_respostas_aleatorias.py # Teste de variabilidade para Task 09
├── PERSONALIDADE_DINAMICA.md  # Documentação da Task 08
├── requirements.txt            # Dependências Python
├── README.md                  # Este arquivo
├── STATUS_REQUISITOS.md       # Relatório de progresso do projeto
├── espec_trabalho.md          # Especificação completa do projeto
└── .gitignore                # Arquivos ignorados pelo Git
```

### 📄 Arquivos Principais

#### 🔧 **Código Fonte**
- **[`main.py`](main.py)**: Interface CLI com classe Chatbot, lógica de processamento NLP e sistema de aprendizado
- **[`app.py`](app.py)**: Interface web Gradio, integração limpa com main.py, UI interativa
- **[`requirements.txt`](requirements.txt)**: Dependências Python necessárias (principalmente Gradio)

#### 📊 **Dados**
- **[`core_data.json`](core_data.json)**: Base de conhecimento estruturada com 7 intenções e 4 personalidades
- **`new_data.json`**: Aprendizados dinâmicos salvos durante execução (gerado automaticamente)

#### 📋 **Documentação**
- **[`README.md`](README.md)**: Documentação principal (este arquivo)
- **[`STATUS_REQUISITOS.md`](STATUS_REQUISITOS.md)**: Análise detalhada de progresso (52.2% concluído)
- **[`PERSONALIDADE_DINAMICA.md`](PERSONALIDADE_DINAMICA.md)**: Documentação completa da Task 08 - Troca Dinâmica de Personalidade
- **[`espec_trabalho.md`](espec_trabalho.md)**: Especificação técnica completa do projeto
- **[`test_personalidade.py`](test_personalidade.py)**: Suite de testes para funcionalidades de personalidade

---

## 💬 Exemplo de Uso

### 💻 Interface Terminal (CLI)

```
====================================
     ESCOLHA SUA ALINE VIRTUAL
====================================

Com qual personalidade da Aline você gostaria de conversar?

[ 1 ] Aline Formal    - A Professora Profissional
[ 2 ] Aline Engraçada - A Coach Descontraída
[ 3 ] Aline Desafiadora - A Professora Exigente
[ 4 ] Aline Empática    - A Mentora Gentil

Digite o número da sua escolha (1-4): 2

Você está conversando com Aline Engraçada. Digite 'quit' para sair ou '/help' para ver comandos.

Você: oi
Aline (Engraçada): E aí, tudo pronto pra gente detonar nesses números? Pode mandar a dúvida que eu tô aqui pra ajudar!

Você: /personalidade empatica
Personalidade alterada para Empática!

Você: oi
Aline (Empática): Oi, tudo bem? Que bom que você veio estudar. Como você está se sentindo hoje?

Você: /help
==================================================
         COMANDOS E PERSONALIDADES
==================================================

Comandos disponíveis:
• /personalidade [nome] - Troca a personalidade
• /help - Mostra esta ajuda

Personalidades disponíveis:
• formal      - A Professora Profissional
• engracada   - A Coach Descontraída
• desafiadora - A Professora Exigente
• empatica    - A Mentora Gentil

Exemplo: /personalidade empatica
--------------------------------------------------

Você: quit
```

### 🌐 Interface Web (Gradio)

A interface web oferece:
- **Dropdown de Personalidade**: Troca dinâmica entre as 4 personalidades
- **Chat Visual**: Histórico de conversas com interface limpa
- **Botões de Ação**: "Enviar", "Ensinar", "Pular", "Limpar Chat"
- **Sistema de Ensino**: Interface dedicada para ensinar novas respostas
- **Acesso Web**: Disponível em `http://localhost:7860` após executar `python app.py`

### 🧠 Sistema de Aprendizado (Ambas Interfaces)

```
Você: como calcular raiz quadrada?
Aline (Engraçada): Opa, essa aí passou batido pelo meu radar! Tenta me perguntar de outro jeito, quem sabe a gente não se entende?

# CLI: Prompt direto
Digite a resposta ou 'pular' para não ensinar: A raiz quadrada é um número que multiplicado por ele mesmo resulta no número original.

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

---

## ⚠️ Limitações Conhecidas

### 🚨 **Issues Críticas de Código**
- ✅ **Issue Crítica #01 RESOLVIDA**: String matching frágil corrigido com uso de flag booleana (`is_fallback`)
- ✅ **Issue Crítica #02 RESOLVIDA**: Acesso não seguro a dicionários corrigido ([`main.py`](main.py))

### 🔄 **Funcionalidades Pendentes**
- **Sistema de Histórico**: Não implementado (bloqueia estatísticas)
- **Respostas Aleatórias**: ✅ Implementado (Task 09)
- **Modularização Completa**: Código ainda em poucos arquivos
- **Estatísticas de Uso**: Dependente do sistema de histórico

### 📋 **Arquivos de Entrega**
- Alguns arquivos específicos da especificação ainda não implementados
- Formato de alguns arquivos diverge da especificação original

---

## 📈 Progresso do Projeto

### 📊 **Status Atual: 53.3% Concluído** (após Task 09)

| Categoria | Progresso | Status |
|-----------|-----------|--------|
| 🎯 **Planejamento e Base** | 100% | ✅ Completo |
| ⚙️ **Funcionalidades Core** | 80% | ⏳ Em Andamento |
| 📈 **Estatísticas/Relatórios** | 0% | 📋 Pendente |
| 🗂️ **Organização/Modularização** | 40% | ⏳ Em Andamento |
| 📄 **Entrega Final** | 35% | 🔄 Parcial |

### 🎯 **Principais Conquistas**
- ✅ Interface CLI completa e funcional
- ✅ Interface Web Gradio implementada
- ✅ **Task 08 CONCLUÍDA**: Troca dinâmica de personalidade em ambas interfaces
- ✅ **Issue Crítica #02 RESOLVIDA**: Acesso seguro a dicionários implementado
- ✅ Sistema de aprendizado robusto
- ✅ 4 personalidades pedagógicas funcionais
- ✅ Base de conhecimento rica (7 intenções)
- ✅ Arquitetura limpa e bem estruturada

### 🔜 **Próximas Prioridades**
1. 🔥 **Implementar sistema de histórico**
2. ⚡ **Adicionar respostas aleatórias**
3. 📊 **Desenvolver estatísticas de uso**
4. 🗂️ **Modularização completa do código**

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
- Mantenha separação entre [`main.py`](main.py) (lógica) e [`app.py`](app.py) (interface)
- Teste ambas as interfaces (CLI e Web) ao fazer alterações
- Use type hints para melhor manutenibilidade

#### 📊 **Conteúdo**
- Adicione novos tópicos em [`core_data.json`](core_data.json) seguindo a estrutura existente
- Teste todas as 4 personalidades ao adicionar novas respostas
- Mantenha consistência no tom de cada personalidade

#### 🚨 **Prioridades Atuais**
- Corrigir issue crítica restante (string matching no app.py)
- Implementar sistema de histórico
- Adicionar respostas aleatórias
- Modularização adicional do código
- Melhorar sistema de testes automatizados

#### 📋 **Documentação**
- Documente mudanças significativas no README
- Atualize [`STATUS_REQUISITOS.md`](STATUS_REQUISITOS.md) se aplicável
- Mantenha exemplos de uso atualizados

---

## 👥 Equipe

| Nome | GitHub | Papel |
|------|--------|-------|
| Davi Maia Soares | [@davimso](https://github.com/davimso) | Desenvolvedor |
| Elder Rayan Oliveira Silva | [@eldrayan](https://github.com/eldrayan) | Desenvolvedor |
| Pedro Yan Alcantara Palácio | [@pedropalacioo](https://github.com/pedropalacioo) | Desenvolvedor |
| Samuel Wagner Tiburi Silveira | [@samsilveira](https://github.com/samsilveira) | Desenvolvedor |
| Jayr Alencar Pereira | [@jayralencar](https://github.com/jayralencar) | Professor Orientador |

---

## 🔗 Links Úteis

- 📊 [Relatório de Progresso](STATUS_REQUISITOS.md) - Status atual dos requisitos
- 📋 [Especificação Completa](espec_trabalho.md) - Documento de especificação
- 🐛 [Reportar Bug](https://github.com/ufca-es/educalin-chat/issues/new?assignees=&labels=bug&template=bug_report.md) - Encontrou um problema?
- 💡 [Sugerir Feature](https://github.com/ufca-es/educalin-chat/issues/new?assignees=&labels=feature&template=feature_request.md) - Tem uma ideia?
- 📈 [Painel de Issues](https://github.com/ufca-es/educalin-chat/issues) - Acompanhe o desenvolvimento


---

<div align="center">

**Desenvolvido pela equipe EducAlin**

</div>
