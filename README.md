# EducAlin - Aline Chat 🤖📚

> Um chatbot educacional inteligente em Python que auxilia estudantes de matemática básica com diferentes personalidades pedagógicas.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow.svg)](STATUS_REQUISITOS.md)

---

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Funcionalidades](#-funcionalidades)
- [Personalidades](#-personalidades)
- [Como Executar](#-como-executar)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Exemplo de Uso](#-exemplo-de-uso)
- [Tecnologias Utilizadas](#%EF%B8%8F-tecnologias-utilizadas)
- [Contribuição](#-contribuição)
- [Equipe](#-equipe)
- [Links Úteis](#-links-úteis)

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
- **🧠 Sistema de Aprendizado**: Capaz de aprender novas respostas através da interação
- **📚 Base de Conhecimento**: Conhecimento pré-programado em matemática básica
- **🔍 Busca Inteligente**: Correspondência fuzzy para entender variações de perguntas
- **💾 Persistência de Dados**: Salva novos aprendizados em arquivo JSON

### 📊 Tópicos Cobertos

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

- Python 3.8 ou superior
- Sistema operacional: Windows, macOS ou Linux

### Passo a Passo

1. **Clone o repositório**
   ```bash
   git clone https://github.com/ufca-es/educalin-chat.git
   cd educalin-chat
   ```

2. **Execute o chatbot**
   ```bash
   python main.py
   ```

3. **Escolha uma personalidade**
   - Digite um número de 1 a 4 quando solicitado
   - Comece a conversar com a Aline!

4. **Para sair**
   - Digite `quit` a qualquer momento

### 🔧 Sem Dependências Externas

O projeto foi desenvolvido usando apenas bibliotecas nativas do Python, não sendo necessário instalar dependências adicionais.

---

## 📁 Estrutura do Projeto

```
educalin-chat/
├── main.py                 # Arquivo principal do chatbot
├── core_data.json          # Base de conhecimento principal
├── new_data.json          # Dados aprendidos durante execução (gerado automaticamente)
├── README.md              # Este arquivo
├── STATUS_REQUISITOS.md   # Relatório de progresso do projeto
├── espec_trabalho.md      # Especificação completa do projeto
└── .gitignore            # Arquivos ignorados pelo Git
```

### 📄 Arquivos Principais

- **[`main.py`](main.py:1)**: Contém toda a lógica do chatbot, incluindo processamento de linguagem natural, seleção de personalidades e sistema de aprendizado
- **[`core_data.json`](core_data.json:1)**: Base de conhecimento estruturada com intenções, perguntas e respostas por personalidade
- **`new_data.json`**: Arquivo gerado automaticamente para armazenar novos aprendizados

---

## 💬 Exemplo de Uso

### Conversação com Aline Engraçada

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

Você está conversando com Aline Engraçada. Digite 'quit' para sair.

Você: oi
Aline (Engraçada): E aí, tudo pronto pra gente detonar nesses números? Pode mandar a dúvida que eu tô aqui pra ajudar!

Você: como funcionam as frações equivalentes?
Aline (Engraçada): Pense numa pizza: cortar 1 fatia de uma pizza de 2 (1/2) te dá a mesma quantidade de comida que pegar 2 fatias de uma pizza de 4 (2/4). Só muda o jeito de cortar, mas a barriga fica igualmente feliz!

Você: quit
```

### Sistema de Aprendizado

```
Você: como calcular raiz quadrada?
Aline (Engraçada): Opa, essa aí passou batido pelo meu radar! Tenta me perguntar de outro jeito, quem sabe a gente não se entende?
Aline (Engraçada): Você poderia me ensinar qual seria a resposta ideal?
Digite a resposta ou 'pular' para não ensinar: A raiz quadrada é um número que multiplicado por ele mesmo resulta no número original.
Aline (Engraçada): Obrigada! Aprendi uma nova resposta.
```

---

## ⚙️ Tecnologias Utilizadas

- **Python 3.8+**: Linguagem principal
- **JSON**: Armazenamento de dados estruturados
- **difflib**: Correspondência fuzzy para processamento de linguagem natural
- **typing**: Anotações de tipo para melhor código

### 🎨 Bibliotecas Nativas Utilizadas

- `json`: Manipulação de dados JSON
- `difflib.get_close_matches`: Busca de correspondência aproximada
- `typing`: Tipagem estática para melhor manutenibilidade

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

- Siga o padrão PEP 8 para código Python
- Adicione novos tópicos em [`core_data.json`](core_data.json:1) seguindo a estrutura existente
- Teste todas as personalidades ao adicionar novas respostas
- Documente mudanças significativas

---

## 👥 Equipe

| Nome | GitHub | Papel |
|------|--------|-------|
| Davi Maia Soares | [@davimso](https://github.com/davimso) | Desenvolvedor |
| Elder Rayan Oliveira Silva | [@eldrayan](https://github.com/eldrayan) | Desenvolvedor |
| Pedro Yan Alcantara Palácio | [@pedropalacioo](https://github.com/pedropalacioo) | Desenvolvedor |
| Samuel Wagner Tiburi Silveira | [@samsilveira](https://github.com/samsilveira) | Desenvolvedor |

---

## 🔗 Links Úteis

- 📊 [Relatório de Progresso](STATUS_REQUISITOS.md) - Status atual dos requisitos
- 📋 [Especificação Completa](espec_trabalho.md) - Documento de especificação
- 🐛 [Reportar Bug](https://github.com/ufca-es/educalin-chat/issues/new?assignees=&labels=bug&template=bug_report.md) - Encontrou um problema?
- 💡 [Sugerir Feature](https://github.com/ufca-es/educalin-chat/issues/new?assignees=&labels=feature&template=feature_request.md) - Tem uma ideia?
- 📈 [Painel de Issues](https://github.com/ufca-es/educalin-chat/issues) - Acompanhe o desenvolvimento


---

<div align="center">

**Desenvolvido com ❤️ pela equipe EducAlin**

*Transformando o aprendizado de matemática através da tecnologia*

</div>
