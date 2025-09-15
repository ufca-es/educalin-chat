# Plano de Teste de Aceitação do Usuário (UAT)
## Correções Críticas UAT-009 e UAT-015 - Sistema de Segurança e Correspondência

**Preparado por:** Engenheiro de QA Sênior  
**Data:** 2025-01-15  
**Versão:** 1.0  
**Objetivo:** Validar as correções implementadas para as issues críticas UAT-009 (Sistema de Escrita Atômica e Segura) e UAT-015 (Algoritmo de Correspondência Rigoroso)  

---

## 📋 **Resumo Executivo**

Este plano de UAT valida as correções implementadas para resolver dois problemas críticos que impediam a aprovação para produção:

- **UAT-009**: Corrupção de dados no arquivo [`new_data.json`](new_data.json) com caracteres especiais
- **UAT-015**: Correspondência fuzzy incorreta retornando mesma resposta para perguntas diferentes

### **Escopo de Teste:**
- ✅ Sistema de escrita atômica e backup automático
- ✅ Validação robusta de entrada e caracteres de controle
- ✅ Algoritmo de correspondência com thresholds rigorosos
- ✅ Busca exata prioritária sobre busca fuzzy
- ✅ Interface CLI e Gradio
- ✅ Ciclo completo de aprendizado com persistência
- ✅ Testes de regressão abrangentes

---

## 🧪 **Casos de Teste UAT**

### **🔒 GRUPO A: VALIDAÇÃO UAT-009 - Sistema de Escrita Atômica e Segura**

| **ID** | **Objetivo** | **Interface** | **Passos para Reprodução** | **Dados de Entrada** | **Resultado Esperado** |
|--------|--------------|---------------|----------------------------|---------------------|------------------------|
| **UAT-009-01** | Validar persistência de caracteres especiais portugueses | Gradio | 1. Abrir interface Gradio<br>2. Selecionar personalidade "formal"<br>3. Enviar pergunta inexistente com acentos<br>4. Ensinar resposta com acentos<br>5. Reenviar mesma pergunta<br>6. Verificar resposta exata | **Entrada 1:** "Como calcular equações com acentuação: çãõáéíóúÇÃÕÁÉÍÓÚ?"<br><br>**Entrada 2 (Ensino):** "Resposta também com acentos: não, coração, educação matemática"<br><br>**Entrada 3:** "Como calcular equações com acentuação: çãõáéíóúÇÃÕÁÉÍÓÚ?" | **Esperado:**<br>**Passo 3:** Fallback ativado, campo ensino aparece<br>**Passo 4:** "Obrigada! Aprendi uma nova resposta."<br>**Passo 5:** Sistema retorna: "Resposta também com acentos: não, coração, educação matemática"<br>**Verificação:** Arquivo [`new_data.json`](new_data.json) contém caracteres especiais íntegros |
| **UAT-009-02** | Validar recuperação de arquivo JSON corrompido | CLI | 1. Fechar sistema completamente<br>2. Editar [`new_data.json`](new_data.json) manualmente para corromper<br>3. Executar `python main.py`<br>4. Tentar ensinar nova resposta<br>5. Verificar recuperação automática | **Entrada 1:** Corromper arquivo removendo `]` final<br><br>**Entrada 2:** "Como resolver integrais por partes?"<br><br>**Entrada 3 (Ensino):** "Use a fórmula: ∫u dv = uv - ∫v du" | **Esperado:**<br>**Passo 3:** Sistema inicia normalmente<br>**Passo 4:** Ensino funciona sem erros<br>**Passo 5:** Arquivo [`new_data.json`](new_data.json) recriado corretamente com nova entrada apenas |
| **UAT-009-03** | Validar rejeição de caracteres de controle maliciosos | Gradio | 1. Abrir interface Gradio<br>2. Tentar ensinar resposta com caracteres perigosos<br>3. Observar rejeição do sistema<br>4. Verificar logs de segurança | **Entrada 1:** "Pergunta normal?"<br><br>**Entrada 2 (Ensino):** "Resposta com \x00 null byte malicioso"<br><br>**Entrada 3 (Ensino):** "Resposta com \x1b[31m ANSI escape" | **Esperado:**<br>**Passo 2:** Sistema rejeita entrada<br>**Passo 3:** Mensagem "Erro ao salvar a nova resposta"<br>**Passo 4:** Arquivo [`new_data.json`](new_data.json) não é modificado<br>**Verificação:** Logs mostram "Entrada com caracteres de controle rejeitada" |
| **UAT-009-04** | Validar proteção contra ataques DoS com entradas longas | Gradio | 1. Tentar ensinar resposta extremamente longa<br>2. Verificar rejeição automática<br>3. Confirmar sistema permanece estável | **Entrada 1:** "Pergunta de teste DoS?"<br><br>**Entrada 2 (Ensino):** String com 1001 caracteres: "a" repetido 1001 vezes | **Esperado:**<br>**Passo 1:** Fallback ativado normalmente<br>**Passo 2:** Sistema rejeita entrada longa<br>**Mensagem:** "Erro ao salvar a nova resposta"<br>**Passo 3:** Interface permanece responsiva, sem travamentos |
| **UAT-009-05** | Validar sistema de backup/rollback automático | CLI + Manual | 1. Ensinar resposta válida<br>2. Simular falha durante escrita (desconectar HD/alterar permissões)<br>3. Tentar ensinar nova resposta<br>4. Reconectar/restaurar permissões<br>5. Verificar dados originais preservados | **Entrada 1:** "Pergunta backup teste"<br>**Resposta 1:** "Resposta backup teste"<br><br>**Entrada 2:** "Pergunta durante falha"<br>**Resposta 2:** "Resposta durante falha" | **Esperado:**<br>**Passo 1:** Salvamento bem-sucedido<br>**Passo 3:** Sistema falha graciosamente sem corromper dados<br>**Passo 5:** [`new_data.json`](new_data.json) contém apenas entrada original, sem corrupção |

### **🎯 GRUPO B: VALIDAÇÃO UAT-015 - Algoritmo de Correspondência Rigoroso**

| **ID** | **Objetivo** | **Interface** | **Passos para Reprodução** | **Dados de Entrada** | **Resultado Esperado** |
|--------|--------------|---------------|----------------------------|---------------------|------------------------|
| **UAT-015-01** | Reproduzir cenário exato da falha original UAT-015 | Gradio | 1. Ensinar resposta específica<br>2. Testar 4 perguntas similares mas diferentes<br>3. Verificar que cada uma ativa fallback<br>4. Confirmar que não retornam resposta incorreta | **Entrada 1:** "Como calcular derivadas complexas método 1?"<br>**Resposta 1:** "Use a regra da cadeia para derivadas complexas"<br><br>**Testes:** <br>- "Como calcular derivadas complexas método 2?"<br>- "Como calcular derivadas simples método 1?"<br>- "Como resolver derivadas complexas técnica 1?"<br>- "Qual método derivadas complexas usar?" | **Esperado:**<br>**Entrada 1:** Ensino bem-sucedido<br>**Cada teste:** <br>• Fallback ativado (campo ensino aparece)<br>• NÃO retorna "Use a regra da cadeia para derivadas complexas"<br>• Retorna fallback da personalidade selecionada<br>**Verificação:** Threshold 0.9 impede correspondências incorretas |
| **UAT-015-02** | Validar threshold rigoroso (0.8) para intenções base | Gradio | 1. Enviar perguntas com similaridade ~0.7 com intenções conhecidas<br>2. Verificar que fallback é ativado<br>3. Confirmar que não retornam respostas base incorretas | **Testes com [`core_data.json`](core_data.json):**<br>- Pergunta base: "oi"<br>- Teste 1: "olá pessoal" (~0.7 similaridade)<br>- Teste 2: "oi gente" (~0.6 similaridade)<br>- Teste 3: "ei aí" (~0.5 similaridade) | **Esperado:**<br>**Todos os testes:**<br>• Fallback ativado<br>• NÃO retornam saudação padrão<br>• Campo ensino aparece<br>**Verificação:** Apenas correspondências ≥0.8 retornam respostas base |
| **UAT-015-03** | Validar busca exata tem prioridade sobre fuzzy | Gradio | 1. Ensinar resposta com pergunta específica<br>2. Enviar pergunta exatamente igual<br>3. Verificar correspondência exata<br>4. Enviar pergunta similar (não exata)<br>5. Verificar fallback para pergunta similar | **Entrada 1:** "pergunta exata especial teste"<br>**Resposta 1:** "resposta exata especial teste"<br><br>**Teste 1:** "pergunta exata especial teste"<br>**Teste 2:** "pergunta exata especial novo" | **Esperado:**<br>**Teste 1:** <br>• Retorna "resposta exata especial teste"<br>• NÃO ativa fallback<br>**Teste 2:**<br>• Ativa fallback<br>• Campo ensino aparece<br>• NÃO retorna resposta do Teste 1 |
| **UAT-015-04** | Validar threshold muito rigoroso (0.9) para dados aprendidos | Gradio | 1. Ensinar resposta específica<br>2. Testar perguntas com similaridade 0.7-0.8<br>3. Verificar que fallback é ativado<br>4. Confirmar não retornam resposta aprendida | **Entrada 1:** "método integral substituição trigonométrica"<br>**Resposta 1:** "Use identidades sen²+cos²=1 para substituir"<br><br>**Testes:**<br>- "método integral substituição algébrica" (~0.8)<br>- "técnica integral substituição trigonométrica" (~0.8)<br>- "processo integral substituição diferente" (~0.7) | **Esperado:**<br>**Entrada 1:** Ensino bem-sucedido<br>**Todos os testes:**<br>• Fallback ativado<br>• NÃO retornam "Use identidades sen²+cos²=1 para substituir"<br>• Campo ensino aparece<br>**Verificação:** Threshold 0.9 é rigorosamente aplicado |
| **UAT-015-05** | Validar correspondência case-insensitive exata | Gradio | 1. Ensinar resposta com capitalização específica<br>2. Testar mesma pergunta em diferentes capitalizações<br>3. Verificar correspondência exata sempre funciona | **Entrada 1:** "Como Calcular MDC"<br>**Resposta 1:** "MDC é o maior divisor comum"<br><br>**Testes:**<br>- "como calcular mdc"<br>- "COMO CALCULAR MDC"<br>- "Como calcular MDC"<br>- "CoMo CaLcUlAr MdC" | **Esperado:**<br>**Entrada 1:** Ensino bem-sucedido<br>**Todos os testes:**<br>• Retornam "MDC é o maior divisor comum"<br>• NÃO ativam fallback<br>• Correspondência exata case-insensitive funciona 100% |

### **⚡ GRUPO C: TESTES DE EDGE CASES E CENÁRIOS EXTREMOS**

| **ID** | **Objetivo** | **Interface** | **Passos para Reprodução** | **Dados de Entrada** | **Resultado Esperado** |
|--------|--------------|---------------|----------------------------|---------------------|------------------------|
| **UAT-EDGE-01** | Validar comportamento com arquivo new_data.json vazio/inexistente | Gradio | 1. Deletar arquivo [`new_data.json`](new_data.json)<br>2. Abrir interface Gradio<br>3. Tentar ensinar primeira resposta<br>4. Verificar criação automática do arquivo | **Entrada 1:** "primeira pergunta no sistema vazio"<br>**Ensino:** "primeira resposta no sistema vazio" | **Esperado:**<br>• Sistema inicia normalmente sem arquivo<br>• Ensino cria [`new_data.json`](new_data.json) automaticamente<br>• Arquivo criado com estrutura JSON válida<br>• Primeira entrada salva corretamente |
| **UAT-EDGE-02** | Validar limite exato de 1000 caracteres (boundary testing) | Gradio | 1. Enviar pergunta com exatamente 1000 chars<br>2. Ensinar resposta com exatamente 1000 chars<br>3. Tentar 1001 chars<br>4. Verificar limite rigoroso | **Entrada 1:** String com exatos 1000 chars: "a"×999 + "?"<br>**Ensino 1:** String com exatos 1000 chars: "b"×1000<br>**Entrada 2:** String com 1001 chars: "c"×1001 | **Esperado:**<br>**1000 chars:** Aceito normalmente<br>**1001 chars:** Rejeitado com log "Entrada muito longa rejeitada"<br>**Verificação:** Boundary exato de 1000 respeitado |
| **UAT-EDGE-03** | Validar threshold exato 0.8 e 0.9 (boundary testing) | Gradio | 1. Criar perguntas com similaridade exata nos limites<br>2. Testar correspondências nos boundaries<br>3. Verificar comportamento preciso | **Base:** "pergunta teste threshold boundary"<br>**Teste 0.79:** "pergunta novo threshold different" (~0.79)<br>**Teste 0.80:** "pergunta teste threshold modified" (~0.80)<br>**Teste 0.89:** "pergunta teste threshold bound" (~0.89)<br>**Teste 0.90:** "pergunta teste threshold boundary" (exata) | **Esperado:**<br>**<0.8:** Fallback ativado<br>**≥0.8:** Match encontrado<br>**<0.9 (aprendidos):** Fallback<br>**≥0.9 (aprendidos):** Match<br>**Precisão absoluta nos boundaries** |
| **UAT-EDGE-04** | Validar caracteres Unicode extremos e emojis | Gradio | 1. Ensinar com caracteres Unicode diversos<br>2. Testar persistência e recuperação<br>3. Verificar integridade UTF-8 completa | **Entrada 1:** "Pergunta com símbolos: ∑∏∆∇∂∫√∞≠≤≥±÷×∈∉∀∃ e emojis: 📊📈📉💯🔢🧮"<br>**Ensino:** "Resposta com Unicode: α, β, γ, δ, ε, ζ, η, θ e símbolos matemáticos: ∀x∈ℝ, ∃y∈ℕ" | **Esperado:**<br>• Todos os caracteres Unicode aceitos<br>• Persistência perfeita em [`new_data.json`](new_data.json)<br>• Recuperação idêntica após reinício<br>• Zero corrupção ou alteração |
| **UAT-EDGE-05** | Validar múltiplas tentativas de ensino simultâneas | Gradio | 1. Ativar fallback para pergunta<br>2. Tentar ensinar resposta vazia<br>3. Tentar ensinar resposta apenas espaços<br>4. Ensinar resposta válida<br>5. Verificar validação robusta | **Entrada 1:** "pergunta teste multiple attempts"<br>**Ensino 1:** "" (vazio)<br>**Ensino 2:** "   " (apenas espaços)<br>**Ensino 3:** "resposta válida finalmente" | **Esperado:**<br>**Ensino 1 e 2:** Rejeitados silenciosamente<br>**Ensino 3:** Aceito e salvo<br>**Estado:** Sistema mantém consistência<br>**Validação:** [`_validar_entrada()`](main.py) funciona perfeitamente |
| **UAT-EDGE-06** | Validar comportamento com arquivo corrompido de múltiplas formas | CLI | 1. Corromper arquivo de formas diferentes<br>2. Tentar operações normais<br>3. Verificar recuperação robusta | **Corrupções testadas:**<br>- JSON inválido: `{malformed`<br>- Array não fechado: `[{}`<br>- Encoding incorreto: bytes inválidos<br>- Arquivo binário: dados não-UTF8<br>- Arquivo gigante: >100MB | **Esperado:**<br>**Todos os casos:** Sistema recupera graciosamente<br>**Comportamento:** Arquivo recriado automaticamente<br>**Logs:** Registram tentativa de recuperação<br>**Zero crashes ou travamentos** |
| **UAT-EDGE-07** | Validar correspondência com caracteres especiais idênticos | Gradio | 1. Ensinar pergunta com acentos<br>2. Testar variações de acentuação<br>3. Verificar normalização correta | **Entrada 1:** "equação diferencial não-linear"<br>**Ensino:** "método específico para não-lineares"<br>**Testes:**<br>- "equacao diferencial nao-linear" (sem acentos)<br>- "EQUAÇÃO DIFERENCIAL NÃO-LINEAR" (maiúsculo)<br>- "equação diferencial não-linear" (exata) | **Esperado:**<br>**Sem acentos:** Fallback (não é correspondência exata)<br>**Maiúsculo:** Correspondência exata case-insensitive<br>**Exata:** Correspondência exata<br>**Normalização:** UTF-8 preservado perfeitamente |
| **UAT-EDGE-08** | Validar comportamento com volume alto de dados aprendidos | Gradio | 1. Ensinar 100+ respostas diferentes<br>2. Testar performance de busca<br>3. Verificar integridade do arquivo grande | **Dados:** Gerar programaticamente 150 pares pergunta-resposta únicos<br>**Formato:** "pergunta_teste_N" → "resposta_teste_N" (N=1 a 150)<br>**Teste:** Buscar perguntas aleatórias do conjunto | **Esperado:**<br>**Performance:** <200ms para qualquer busca<br>**Arquivo:** [`new_data.json`](new_data.json) mantém estrutura válida<br>**Busca:** Todas as 150 perguntas encontradas corretamente<br>**Escalabilidade:** Sistema robusto com volume alto |

### **🔄 GRUPO D: TESTES DE REGRESSÃO E CICLO COMPLETO**

| **ID** | **Objetivo** | **Interface** | **Passos para Reprodução** | **Dados de Entrada** | **Resultado Esperado** |
|--------|--------------|---------------|----------------------------|---------------------|------------------------|
| **UAT-REG-01** | Validar que todas as intenções base continuam funcionando | Gradio | 1. Testar pergunta de cada tag em [`core_data.json`](core_data.json)<br>2. Verificar resposta específica da personalidade<br>3. Confirmar que ensino NÃO é ativado | **Testes sistemáticos:**<br>- "oi" (saudacao)<br>- "estou com dificuldades nos estudos" (dificuldade_estudos)<br>- "o que é mdc?" (conceito_mdc)<br>- "como calcular 15% de 200?" (porcentagem)<br>- "me explique função quadrática" (funcao_quadratica)<br>- "preciso de ajuda" (pedido_ajuda)<br>- "obrigada" (agradecimento) | **Esperado para cada teste:**<br>• Resposta específica da personalidade selecionada<br>• Campo ensino NÃO aparece<br>• Resposta conforme [`core_data.json`](core_data.json)<br>• Zero regressões detectadas |
| **UAT-REG-02** | Validar compatibilidade completa CLI após correções | CLI | 1. Executar [`main.py`](main.py)<br>2. Testar ensino via CLI<br>3. Verificar comandos especiais<br>4. Confirmar funcionalidade preservada | **Entrada 1:** "pergunta CLI teste especial"<br>**Resposta:** "s"<br>**Ensino:** "resposta CLI teste especial"<br><br>**Comando:** "/personalidade empatica"<br>**Teste:** "oi" | **Esperado:**<br>**CLI funcionando 100%:**<br>• Sistema de ensino via CLI operacional<br>• Comando `/personalidade` funciona<br>• Respostas específicas por personalidade<br>• Interface CLI não afetada pelas correções |
| **UAT-REG-03** | Validar persistência entre sessões após correções | Gradio | 1. Ensinar múltiplas respostas<br>2. Fechar interface Gradio<br>3. Reabrir interface<br>4. Testar todas as respostas ensinadas<br>5. Verificar integridade do arquivo | **Sessão 1 - Ensinar:**<br>- "pergunta persistência 1" → "resposta persistência 1"<br>- "pergunta persistência 2" → "resposta persistência 2"<br>- "pergunta persistência 3" → "resposta persistência 3"<br><br>**Sessão 2 - Validar:**<br>Todas as 3 perguntas | **Esperado:**<br>**Sessão 1:** Todos os ensinos bem-sucedidos<br>**Sessão 2:**<br>• Todas as 3 perguntas retornam respostas corretas<br>• NÃO ativam fallback<br>• [`new_data.json`](new_data.json) íntegro e válido<br>• Encoding UTF-8 preservado |
| **UAT-CIC-01** | Teste completo do ciclo de aprendizado com ambas correções | Gradio | 1. Enviar pergunta com caracteres especiais<br>2. Ensinar resposta com caracteres especiais<br>3. Testar perguntas similares (devem dar fallback)<br>4. Testar pergunta exata (deve retornar resposta)<br>5. Verificar logs e arquivo final | **Entrada 1:** "Como resolver equações diferenciais com coeficientes não-lineares em português: ação, não, coração?"<br><br>**Ensino:** "Métodos de solução incluem: série de potências, transformação de variáveis, aproximação numérica"<br><br>**Teste Similar:** "Como resolver equações diferenciais com coeficientes lineares?"<br><br>**Teste Exato:** "Como resolver equações diferenciais com coeficientes não-lineares em português: ação, não, coração?" | **Esperado:**<br>**Entrada 1:** Fallback ativado<br>**Ensino:** Sucesso com caracteres especiais<br>**Teste Similar:** Fallback (threshold rigoroso)<br>**Teste Exato:** Retorna resposta ensinada<br>**Verificação Final:**<br>• [`new_data.json`](new_data.json) íntegro<br>• Logs mostram operações seguras<br>• Sistema robusto end-to-end |

---

## 🎯 **Critérios de Aceitação**

### **Critérios Obrigatórios UAT-009 (Todos devem passar):**

1. **✅ Zero Corrupção de Dados**
   - Caracteres especiais portugueses (çãõáéíóúÇÃÕÁÉÍÓÚ) DEVEM ser persistidos corretamente
   - Arquivo [`new_data.json`](new_data.json) DEVE manter integridade UTF-8 sempre

2. **✅ Segurança Robusta**
   - Caracteres de controle (\x00, \x01, \x02, \x03, \x04, \x1b) DEVEM ser rejeitados
   - Entradas >1000 caracteres DEVEM ser rejeitadas
   - Sistema DEVE resistir a tentativas de corrupção

3. **✅ Recuperação Automática**
   - Sistema DEVE se recuperar de arquivos JSON corrompidos
   - Backup/rollback DEVE funcionar em falhas de I/O
   - Operações de escrita DEVEM ser atômicas

### **Critérios Obrigatórios UAT-015 (Todos devem passar):**

1. **✅ Correspondência Precisa**
   - Threshold 0.8 para intenções base DEVE ser rigorosamente aplicado
   - Threshold 0.9 para dados aprendidos DEVE ser rigorosamente aplicado
   - Perguntas similares mas diferentes DEVEM ativar fallback

2. **✅ Prioridade de Busca Exata**
   - Correspondência exata SEMPRE tem prioridade sobre fuzzy
   - Busca case-insensitive DEVE funcionar perfeitamente
   - Sistema NUNCA deve retornar resposta incorreta

3. **✅ Zero Falsos Positivos**
   - Cenário original UAT-015 DEVE ser completamente resolvido
   - Sistema DEVE distinguir entre perguntas genuinamente diferentes
   - Correspondência fuzzy DEVE ser muito mais rigorosa

### **Critérios de Regressão:**

- **100% das funcionalidades existentes** DEVEM continuar operando
- **Interface CLI** DEVE permanecer totalmente funcional
- **Todas as intenções base** DEVEM retornar respostas corretas
- **Comandos especiais** (`/personalidade`) DEVEM funcionar normalmente

### **Critérios de Performance:**

- Tempo de resposta < 200ms para qualquer operação
- Sistema DEVE permanecer responsivo durante validações de segurança
- Operações de backup/rollback DEVEM ser transparentes ao usuário

---

## 📊 **Matriz de Rastreabilidade**

| **Correção** | **Casos de Teste Relacionados** | **Cobertura** | **Status** |
|--------------|----------------------------------|---------------|------------|
| **UAT-009: Escrita Atômica** | UAT-009-01, UAT-009-02, UAT-009-05 | Funcionalidade Core | ✅ PASSOU |
| **UAT-009: Validação Segurança** | UAT-009-03, UAT-009-04 | Ataques Maliciosos | ⚠️ PARCIAL |
| **UAT-015: Thresholds Rigorosos** | UAT-015-01, UAT-015-02, UAT-015-04 | Correspondência Fuzzy | ⚠️ PARCIAL |
| **UAT-015: Busca Exata** | UAT-015-03, UAT-015-05 | Prioridade Exata | ✅ PASSOU |
| **Edge Cases Críticos** | UAT-EDGE-01 a UAT-EDGE-08 | Cenários Extremos | ⏳ Aguardando |
| **Regressão Completa** | UAT-REG-01, UAT-REG-02, UAT-REG-03 | Funcionalidades Existentes | ⏳ Aguardando |
| **Ciclo End-to-End** | UAT-CIC-01 | Integração Completa | ⏳ Aguardando |

---

## 🚀 **Ambiente de Teste**

### **Pré-requisitos:**
- Python 3.8+
- Gradio instalado (`pip install gradio`)
- Arquivos: [`main.py`](main.py), [`app.py`](app.py), [`core_data.json`](core_data.json)
- Arquivo [`new_data.json`](new_data.json) limpo para cada teste
- Logs habilitados para auditoria

### **Configuração de Dados:**
- **Backup de [`new_data.json`](new_data.json):** Criar cópia antes dos testes
- **Dados de intenções:** Usar [`core_data.json`](core_data.json) original
- **Ambiente isolado:** Usar diretório temporário para testes críticos

### **Comandos de Inicialização:**
```bash
# Teste CLI
python main.py

# Teste Gradio (terminal separado)
python app.py

# Verificar logs (se necessário)
tail -f sistema.log
```

---

## 📋 **Procedimento de Execução**

### **Fase 1: Validação UAT-009 - Segurança e Integridade (40min)**
**Objetivo:** Provar que corrupção de dados foi 100% eliminada
**Casos:** UAT-009-01 a UAT-009-05
**Critério:** Zero falhas, sistema robusto contra ataques

### **Fase 2: Validação UAT-015 - Correspondência Rigorosa (35min)**
**Objetivo:** Provar que correspondências incorretas foram eliminadas
**Casos:** UAT-015-01 a UAT-015-05
**Critério:** Thresholds rigorosos aplicados, busca exata prioritária

### **Fase 3: Testes de Edge Cases - Cenários Extremos (45min)**
**Objetivo:** Validar robustez em condições limites e casos extremos
**Casos:** UAT-EDGE-01 a UAT-EDGE-08
**Critério:** Sistema resiliente em todos os cenários boundary e extremos

### **Fase 4: Testes de Regressão (30min)**
**Objetivo:** Garantir zero impacto em funcionalidades existentes
**Casos:** UAT-REG-01 a UAT-REG-03
**Critério:** 100% das funcionalidades preservadas

### **Fase 5: Teste de Ciclo Completo (20min)**
**Objetivo:** Validação end-to-end das duas correções juntas
**Casos:** UAT-CIC-01
**Critério:** Sistema robusto com ambas correções ativas

**Tempo total estimado:** 170 minutos

---

## 📝 **Relatório de Resultados**

### **Template de Resultado por Teste:**

| Campo | Descrição |
|-------|-----------|
| **ID do Teste** | UAT-XXX-XX |
| **Status** | ✅ PASSOU / ❌ FALHOU / ⚠️ PARCIAL |
| **UAT-009 Validado** | ✅ Segurança OK / ❌ Vulnerabilidade |
| **UAT-015 Validado** | ✅ Correspondência OK / ❌ Falso Positivo |
| **Evidências** | Screenshots + arquivos de log |
| **Observações** | Notas técnicas específicas |

### **Critério de Aprovação Final:**

- ✅ **100% dos testes UAT-009** passaram (segurança crítica)
- ✅ **100% dos testes UAT-015** passaram (correspondência crítica)  
- ✅ **Zero regressões** detectadas
- ✅ **Taxa de aprovação projetada ≥ 95%** alcançada

---

## 🎯 **Métricas de Sucesso Esperadas**

### **Comparação Antes vs Depois das Correções:**

| Métrica | Antes (UAT Falhado) | Depois (Esperado) | Meta |
|---------|---------------------|-------------------|------|
| **Corrupção de Dados UAT-009** | 100% dos casos | 0% dos casos | **0%** |
| **Correspondência Incorreta UAT-015** | 80% dos casos | <5% dos casos | **<5%** |
| **Taxa Aprovação UAT Geral** | 73.3% | ≥95% | **≥95%** |
| **Falhas Críticas** | 2 (UAT-009, UAT-015) | 0 | **0** |
| **Tempo Resposta** | <200ms | <200ms | **Mantido** |

### **Indicadores de Qualidade:**

- **Robustez:** Sistema resiste a 100% dos ataques testados
- **Precisão:** Zero falsos positivos em correspondência
- **Integridade:** 100% dos dados persistidos corretamente  
- **Segurança:** 100% dos ataques maliciosos bloqueados

---

## ✅ **Conclusão**

Este plano de UAT fornece validação **completa e rigorosa** das correções críticas UAT-009 e UAT-015, cobrindo:

- **🔒 Segurança Total:** Validação robusta contra corrupção e ataques
- **🎯 Precisão Absoluta:** Correspondência rigorosa sem falsos positivos
- **⚡ Robustez Extrema:** 8 casos de edge cases para cenários limites
- **🔄 Zero Regressões:** Preservação completa de funcionalidades existentes
- **📊 Métricas Claras:** Critérios objetivos de aprovação
- **🚀 Preparação Produção:** Validação para deploy seguro

**Total de 21 casos de teste abrangentes** cobrindo desde funcionalidades básicas até cenários extremos e boundary conditions.

**A execução bem-sucedida deste plano confirmará que o sistema está pronto para produção com taxa de aprovação ≥ 95% e zero vulnerabilidades críticas.**

---

*Plano de UAT elaborado para validação completa das correções UAT-009 e UAT-015.*  
*Referência: [`RELATORIO_FINAL_CORRECOES_UAT.md`](RELATORIO_FINAL_CORRECOES_UAT.md)*