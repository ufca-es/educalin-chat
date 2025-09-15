# Plano de Teste de Aceitação do Usuário (UAT)
## Issue Crítica #01 - Sistema de Fallback e Aprendizado

**Preparado por:** Engenheiro de QA Sênior  
**Data:** 2025-01-15  
**Versão:** 1.0  
**Objetivo:** Validar a correção da Issue Crítica #01 relacionada ao string matching frágil no sistema de fallback e aprendizado  

---

## 📋 **Resumo Executivo**

Este plano de UAT valida a correção implementada para resolver o problema de detecção de fallback que tornava o sistema de aprendizado **100% inoperante** na interface Gradio. A correção substituiu o string matching frágil por uma flag robusta de detecção.

### **Escopo de Teste:**
- ✅ Interface CLI (Command Line Interface)
- ✅ Interface Web Gradio
- ✅ Sistema de fallback para todas as personalidades
- ✅ Ciclo completo de aprendizado
- ✅ Testes de regressão

---

## 🧪 **Casos de Teste UAT**

| **ID** | **Objetivo** | **Interface** | **Passos para Reprodução** | **Dados de Entrada** | **Resultado Esperado** |
|--------|--------------|---------------|----------------------------|---------------------|------------------------|
| **UAT-001** | Validar detecção de fallback - Personalidade Formal | Gradio | 1. Abrir interface Gradio<br>2. Selecionar personalidade "formal"<br>3. Enviar pergunta inexistente<br>4. Observar resposta e interface | **Entrada:** "Como calcular a raiz cúbica de números complexos usando logaritmos neperianos?" | **Esperado:**<br>• Resposta: "Não compreendi a sua solicitação. Poderia, por favor, reformular a pergunta utilizando outros termos?"<br>• Interface mostra: "Você pode me ensinar a resposta ideal?"<br>• Campo de ensino aparece<br>• Botões "Ensinar" e "Pular Ensino" habilitados |
| **UAT-002** | Validar detecção de fallback - Personalidade Engraçada | Gradio | 1. Abrir interface Gradio<br>2. Selecionar personalidade "engracada"<br>3. Enviar pergunta inexistente<br>4. Observar resposta e interface | **Entrada:** "Qual é a fórmula da transformada de Fourier aplicada à teoria dos jogos?" | **Esperado:**<br>• Resposta: "Opa, essa aí passou batido pelo meu radar! Tenta me perguntar de outro jeito, quem sabe a gente não se entende?"<br>• Interface mostra: "Você pode me ensinar a resposta ideal?"<br>• Campo de ensino aparece<br>• Botões "Ensinar" e "Pular Ensino" habilitados |
| **UAT-003** | Validar detecção de fallback - Personalidade Desafiadora | Gradio | 1. Abrir interface Gradio<br>2. Selecionar personalidade "desafiadora"<br>3. Enviar pergunta inexistente<br>4. Observar resposta e interface | **Entrada:** "Como resolver equações diferenciais parciais com condições de contorno móveis?" | **Esperado:**<br>• Resposta: "Sua pergunta não está clara para mim. Tente quebrá-la em partes menores. Qual é o conceito central da sua dúvida?"<br>• Interface mostra: "Você pode me ensinar a resposta ideal?"<br>• Campo de ensino aparece<br>• Botões "Ensinar" e "Pular Ensino" habilitados |
| **UAT-004** | Validar detecção de fallback - Personalidade Empática | Gradio | 1. Abrir interface Gradio<br>2. Selecionar personalidade "empatica"<br>3. Enviar pergunta inexistente<br>4. Observar resposta e interface | **Entrada:** "Pode me explicar a aplicação de matrizes esparsas em algoritmos de machine learning?" | **Esperado:**<br>• Resposta: "Desculpe, não entendi bem o que você quis dizer. Não se preocupe, acontece! Podemos tentar de outra forma? Me explique com suas palavras qual é a sua dificuldade."<br>• Interface mostra: "Você pode me ensinar a resposta ideal?"<br>• Campo de ensino aparece<br>• Botões "Ensinar" e "Pular Ensino" habilitados |
| **UAT-005** | Validar resposta conhecida - Saudação | Gradio | 1. Abrir interface Gradio<br>2. Selecionar personalidade "formal"<br>3. Enviar saudação conhecida<br>4. Verificar que modo ensino NÃO é ativado | **Entrada:** "oi" | **Esperado:**<br>• Resposta: "Olá. Sou Aline, sua assistente de matemática. Qual tópico gostaria de abordar hoje?"<br>• Campo de ensino NÃO aparece<br>• Botões "Ensinar" e "Pular Ensino" NÃO aparecem<br>• Interface normal de conversa |
| **UAT-006** | Validar resposta conhecida - Conceito MDC | Gradio | 1. Abrir interface Gradio<br>2. Selecionar personalidade "engracada"<br>3. Enviar pergunta sobre MDC<br>4. Verificar resposta específica da personalidade | **Entrada:** "o que é mdc?" | **Esperado:**<br>• Resposta: "MDC é o 'amigão em comum' dos números! Pensa assim: qual é o maior número que consegue dividir o 12 e o 18 sem deixar ninguém de fora (resto)? É o 6! Ele é o 'Máximo' do rolê."<br>• Campo de ensino NÃO aparece<br>• Interface normal de conversa |
| **UAT-007** | Ciclo completo de aprendizado - Ensinar nova resposta | Gradio | 1. Abrir interface Gradio<br>2. Selecionar personalidade "formal"<br>3. Enviar pergunta inexistente<br>4. Aguardar ativação do ensino<br>5. Inserir resposta no campo de ensino<br>6. Clicar "Ensinar"<br>7. Enviar a mesma pergunta novamente | **Entrada 1:** "Como calcular juros compostos com inflação?"<br><br>**Entrada 2 (Ensino):** "Para calcular juros compostos com inflação, use a fórmula: Montante = Capital × [(1 + taxa_real)^tempo], onde taxa_real = (1 + taxa_nominal)/(1 + inflação) - 1"<br><br>**Entrada 3:** "Como calcular juros compostos com inflação?" | **Esperado:**<br>**Passo 3:** Fallback ativado, campo ensino aparece<br>**Passo 6:** Mensagem "Obrigada! Aprendi uma nova resposta."<br>**Passo 7:** Sistema retorna resposta ensinada exata, SEM ativar modo ensino |
| **UAT-008** | Ciclo completo de aprendizado - Pular ensino | Gradio | 1. Abrir interface Gradio<br>2. Selecionar personalidade "empatica"<br>3. Enviar pergunta inexistente<br>4. Aguardar ativação do ensino<br>5. Clicar "Pular Ensino"<br>6. Verificar retorno ao estado normal | **Entrada:** "Qual é a derivada da função logarítmica natural de x ao quadrado?" | **Esperado:**<br>**Passo 4:** Campo ensino ativado<br>**Passo 5:** Mensagem "Tudo bem, podemos deixar para depois."<br>**Passo 6:** Campo ensino desaparece, chat retorna ao normal |
| **UAT-009** | Validar fallback CLI - Personalidade Formal | CLI | 1. Executar `python main.py`<br>2. Selecionar personalidade 1 (formal)<br>3. Enviar pergunta inexistente<br>4. Observar pergunta sobre ensino<br>5. Responder 's' para ensinar<br>6. Inserir resposta de ensino | **Entrada 1:** "Como resolver integrais triplas em coordenadas esféricas?"<br><br>**Entrada 2:** "s"<br><br>**Entrada 3:** "Para resolver integrais triplas em coordenadas esféricas, use dV = ρ²sin(φ)dρdφdθ" | **Esperado:**<br>**Passo 3:** "Não compreendi a sua solicitação..."<br>**Passo 4:** "Deseja me ensinar a resposta correta? (s/n)"<br>**Passo 6:** "Obrigada! Aprendi uma nova resposta." |
| **UAT-010** | Validar fallback CLI - Personalidade Engraçada | CLI | 1. Executar `python main.py`<br>2. Selecionar personalidade 2 (engracada)<br>3. Enviar pergunta inexistente<br>4. Observar pergunta sobre ensino<br>5. Responder 'n' para não ensinar | **Entrada 1:** "Como aplicar teorema de Bayes em redes neurais profundas?"<br><br>**Entrada 2:** "n" | **Esperado:**<br>**Passo 3:** "Opa, essa aí passou batido pelo meu radar!..."<br>**Passo 4:** "Deseja me ensinar a resposta correta? (s/n)"<br>**Passo 5:** Retorna ao prompt normal sem salvar |
| **UAT-011** | Validar comandos especiais CLI - Troca de personalidade | CLI | 1. Executar `python main.py`<br>2. Selecionar personalidade inicial<br>3. Usar comando `/personalidade empatica`<br>4. Enviar pergunta conhecida<br>5. Verificar resposta da nova personalidade | **Entrada 1:** "/personalidade empatica"<br><br>**Entrada 2:** "oi" | **Esperado:**<br>**Passo 3:** "Personalidade alterada para Empática!"<br>**Passo 5:** "Oi, tudo bem? Que bom que você veio estudar..." |
| **UAT-012** | Teste de regressão - Múltiplas personalidades | Gradio | 1. Testar pergunta conhecida em cada personalidade<br>2. Verificar respostas específicas<br>3. Confirmar que nenhuma ativa ensino | **Entrada:** "estou com dificuldades nos estudos"<br><br>**Testar em:** formal, engracada, desafiadora, empatica | **Esperado:**<br>**Formal:** "Dificuldades de aprendizado podem ser superadas..."<br>**Engraçada:** "Relaxa, todo super-herói tem sua criptonita!..."<br>**Desafiadora:** "A dificuldade faz parte do processo..."<br>**Empática:** "Eu entendo completamente como é se sentir assim..."<br>**Todas:** Campo ensino NÃO aparece |
| **UAT-013** | Teste de regressão - Sistema de persistência | Gradio | 1. Ensinar nova resposta<br>2. Fechar interface Gradio<br>3. Reabrir interface<br>4. Enviar mesma pergunta<br>5. Verificar se resposta foi persistida | **Entrada 1:** "O que são números imaginários puros?"<br><br>**Entrada 2 (Ensino):** "Números imaginários puros são números da forma bi, onde b é real e i é a unidade imaginária."<br><br>**Entrada 3:** "O que são números imaginários puros?" | **Esperado:**<br>**Passo 1:** Fallback ativado<br>**Passo 4:** Resposta ensinada retornada<br>**Passo 5:** Sistema NÃO ativa modo ensino |
| **UAT-014** | Validar cenário da falha original - String matching | Gradio | 1. Enviar pergunta que geraria fallback<br>2. Verificar que a resposta NÃO contém strings "não sei a resposta" ou "não entendi" exatas<br>3. Confirmar que ensino é ativado mesmo assim | **Entrada:** "Como calcular a área de um polígono irregular de 17 lados usando apenas régua e compasso?" | **Esperado:**<br>• Resposta de fallback específica da personalidade (sem strings exatas do código original)<br>• Campo ensino DEVE ser ativado<br>• Isso prova que a correção funciona independente do texto |
| **UAT-015** | Teste de stress - Múltiplas interações seguidas | Gradio | 1. Enviar 5 perguntas inexistentes seguidas<br>2. Ensinar resposta para 3 delas<br>3. Pular ensino para 2<br>4. Reenviar todas as 5 perguntas<br>5. Verificar comportamento correto | **Perguntas:** "pergunta1_UAT015", "pergunta2_UAT015", "pergunta3_UAT015", "pergunta4_UAT015", "pergunta5_UAT015" | **Esperado:**<br>• Primeiras 5: Todas ativam fallback<br>• 3 ensinadas: Retornam respostas aprendidas<br>• 2 puladas: Ainda ativam fallback<br>• Estado interno sempre consistente |

---

## 🎯 **Critérios de Aceitação**

### **Critérios Obrigatórios (Todos devem passar):**

1. **✅ Detecção de Fallback 100%**
   - Todas as perguntas inexistentes DEVEM ativar o modo ensino
   - TODAS as personalidades devem funcionar corretamente

2. **✅ Sistema de Aprendizado Funcional**
   - Ensino via Gradio DEVE funcionar em 100% dos casos
   - Respostas ensinadas DEVEM ser persistidas e recuperadas

3. **✅ Compatibilidade CLI Preservada**
   - Interface CLI DEVE continuar funcionando exatamente como antes
   - Sistema de ensino CLI DEVE permanecer operacional

4. **✅ Zero Regressões**
   - Todas as funcionalidades existentes DEVEM continuar operando
   - Perguntas conhecidas NUNCA devem ativar modo ensino

5. **✅ Robustez da Solução**
   - Sistema DEVE funcionar independente do texto das mensagens de fallback
   - Mudanças futuras nas mensagens NÃO devem quebrar a detecção

### **Critérios de Performance:**
- Tempo de resposta < 200ms para qualquer interação
- Interface deve permanecer responsiva durante o processo de ensino

### **Critérios de Usabilidade:**
- Mensagens claras sobre quando o modo ensino é ativado
- Feedback imediato ao ensinar nova resposta
- Interface intuitiva para pular ensino

---

## 📊 **Matriz de Rastreabilidade**

| **Requisito** | **Casos de Teste Relacionados** | **Status** |
|---------------|----------------------------------|------------|
| Detecção de fallback por personalidade | UAT-001, UAT-002, UAT-003, UAT-004 | ⏳ Aguardando |
| Sistema de aprendizado Gradio | UAT-007, UAT-008, UAT-013 | ⏳ Aguardando |
| Compatibilidade CLI | UAT-009, UAT-010, UAT-011 | ⏳ Aguardando |
| Teste de regressão | UAT-005, UAT-006, UAT-012 | ⏳ Aguardando |
| Validação da correção | UAT-014, UAT-015 | ⏳ Aguardando |

---

## 🚀 **Ambiente de Teste**

### **Pré-requisitos:**
- Python 3.8+
- Gradio instalado (`pip install gradio`)
- Arquivos do sistema: `main.py`, `app.py`, `core_data.json`
- Interface CLI acessível via `python main.py`
- Interface Gradio acessível via `python app.py`

### **Dados de Teste:**
- **Perguntas conhecidas:** Usar exatas do [`core_data.json`](core_data.json)
- **Perguntas inexistentes:** Usar perguntas técnicas específicas listadas
- **Personalidades:** formal, engracada, desafiadora, empatica

### **Configuração:**
```bash
# Executar interface CLI
python main.py

# Executar interface Gradio (em terminal separado)
python app.py
```

---

## 📋 **Procedimento de Execução**

### **Fase 1: Testes de Fallback (UAT-001 a UAT-004)**
**Objetivo:** Validar que a detecção de fallback funciona para todas as personalidades  
**Tempo estimado:** 20 minutos  
**Critério de sucesso:** 100% dos casos devem ativar modo ensino  

### **Fase 2: Testes de Regressão (UAT-005, UAT-006, UAT-012)**
**Objetivo:** Garantir que funcionalidades existentes não foram afetadas  
**Tempo estimado:** 15 minutos  
**Critério de sucesso:** Nenhuma pergunta conhecida deve ativar ensino  

### **Fase 3: Testes de Aprendizado (UAT-007, UAT-008, UAT-013)**
**Objetivo:** Validar ciclo completo de aprendizado  
**Tempo estimado:** 25 minutos  
**Critério de sucesso:** Ensino e recuperação devem funcionar 100%  

### **Fase 4: Testes CLI (UAT-009, UAT-010, UAT-011)**
**Objetivo:** Verificar compatibilidade com interface CLI  
**Tempo estimado:** 20 minutos  
**Critério de sucesso:** CLI deve funcionar exatamente como antes  

### **Fase 5: Testes de Validação da Correção (UAT-014, UAT-015)**
**Objetivo:** Provar que a correção original funciona  
**Tempo estimado:** 15 minutos  
**Critério de sucesso:** Sistema deve funcionar independente de strings específicas  

**Tempo total estimado:** 95 minutos

---

## 📝 **Relatório de Resultados**

### **Template de Resultado por Teste:**

| Campo | Descrição |
|-------|-----------|
| **ID do Teste** | UAT-XXX |
| **Status** | ✅ PASSOU / ❌ FALHOU / ⚠️ PARCIAL |
| **Resultado Obtido** | [Descrição detalhada do que aconteceu] |
| **Desvios** | [Qualquer diferença do resultado esperado] |
| **Screenshots** | [Evidências visuais quando aplicável] |
| **Observações** | [Notas adicionais do testador] |

### **Critério de Aprovação Final:**
- ✅ **100% dos testes obrigatórios** devem passar
- ✅ **Zero regressões** detectadas
- ✅ **Funcionalidade crítica restaurada** completamente

---

## 🎯 **Conclusão**

Este plano de UAT garante validação completa da correção da Issue Crítica #01, cobrindo:

- **✅ Todas as interfaces** (CLI e Gradio)
- **✅ Todas as personalidades** (formal, engraçada, desafiadora, empática)
- **✅ Cenários de fallback** com dados reais
- **✅ Ciclo completo de aprendizado** 
- **✅ Testes de regressão** abrangentes
- **✅ Validação da robustez** da solução implementada

**A execução deste plano confirmará que o sistema de aprendizado via Gradio foi 100% restaurado e que nenhuma funcionalidade existente foi comprometida.**

---

*Plano de UAT elaborado para validação completa da correção implementada.*