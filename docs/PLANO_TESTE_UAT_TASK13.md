# Plano de Teste de Aceitação do Usuário (UAT) para Task 13 - Sistema de Estatísticas

**Preparado por:** Arquiteto Técnico (Roo/Sonoma)  
**Data:** 2025-09-17  
**Versão:** 1.0  
**Objetivo:** Validar o sistema de estatísticas da Task 13, garantindo coleta precisa, persistência segura, exibição legível e robustez em cenários reais. Inspirado nos formatos de `docs/PLANO_TESTE_UAT_ISSUE_CRITICA_01.md` e `docs/PLANO_TESTE_UAT_CORRECOES_CRITICAS_009_015.md`, prioriza testes críticos (coleta/exibição), erros, usabilidade e performance para sistemas analíticos (alinhado a QA best practices: ISTQB, foco em dados agregados).

## 📋 Resumo Executivo
Este plano UAT valida a Task 13 (coleta de stats: interações, personalidades, fallbacks, tags, duração), cobrindo fluxos principais (CLI/Gradio), erros (arquivos corrompidos, zero dados), usabilidade (formatação intuitiva) e performance (<1s response). Escopo: Integração com histórico/aprendizado; sem ML avançado (Task 15).

- **Escopo:** CLI (`python main.py`), Gradio (`python app.py`); 18 casos (12 principais, 4 erros, 2 usabilidade/performance).
- **Prioridades:** Críticos (coleta precisa, persistência); alinha com ISO 25010 (funcionalidade, usabilidade, performance).
- **Tempo Estimado:** 120 minutos.

## 🧪 Casos de Teste UAT
Casos em tabela: ID, Descrição, Passos, Dados Entrada, Critérios Sucesso/Falha, Evidências Esperadas. Cobrem fluxos (coleta/exibição), erros (I/O, edges), usabilidade (legibilidade), performance (tempo).

| **ID** | **Descrição** | **Interface** | **Passos de Execução** | **Dados de Entrada** | **Critérios de Sucesso/Falha** | **Evidências Esperadas** |
|--------|---------------|---------------|------------------------|----------------------|-------------------------------|--------------------------|
| **UAT-13-01** | Validar coleta básica: Interação conhecida (non-fallback) | Gradio | 1. Abrir Gradio (`python app.py`).<br>2. Selecionar "formal".<br>3. Enviar pergunta conhecida (ex. "oi").<br>4. Clicar "Ver Stats".<br>5. Verificar textbox. | Entrada: "oi" (saudação, tag="saudacao"). | Sucesso: total_interactions=1, fallback_rate=0%, por_personalidade['formal']=1 (100%), por_tag['saudacao']=1, duração~0.1min.<br>Falha: Contadores=0 ou erro. | Screenshot textbox: "Total:1, Formal:1 (100%), Saudacao:1 (100%)"; stats.json diff (total=1). |
| **UAT-13-02** | Validar coleta fallback + tag | CLI | 1. Executar `python main.py`.<br>2. Selecionar personalidade 1 (formal).<br>3. Enviar pergunta inexistente.<br>4. Digitar /stats. | Entrada: "Pergunta inventada sobre física quântica?" (fallback, tag=None). | Sucesso: total=1, fallback_count=1 (100%), por_personalidade['formal']=1, por_tag={}, duração~0min.<br>Falha: Fallback não contado. | Console output: "Total:1, Taxa Fallback:100.0%, Formal:1 (100%)"; stats.json (fallback_count=1). |
| **UAT-13-03** | Validar múltiplas interações por personalidade | Gradio | 1. Abrir Gradio.<br>2. Trocar para "engracada".<br>3. Enviar 3 perguntas conhecidas.<br>4. Clicar "Ver Stats". | Entradas: "o que é mdc?", "como calcular 15% de 200?", "oi". | Sucesso: total=3, por_personalidade['engracada']=3 (100% se só ela), fallback=0, tags variadas (mdc, porcentagem, saudacao).<br>Falha: Contadores errados. | Textbox: "Engracada:3 (100%), mdc:1 (33.3%)"; stats.json atualizado. |
| **UAT-13-04** | Validar duração de sessão <5min | CLI | 1. `python main.py`, personalidade formal.<br>2. Enviar 2 perguntas rápidas (<1min).<br>3. /stats. | Entradas: "oi", "o que é mdc?" (intervalo <5min). | Sucesso: total=2, media_duracao~0.5-1min, fallback=0.<br>Falha: Duração=0 ou >5min. | Output: "Duração Média: 0.8 minutos"; stats.json (indireto via get_stats). |
| **UAT-13-05** | Validar duração múltiplas sessões (>5min gap) | Gradio | 1. Abrir Gradio.<br>2. Enviar 2 msgs (<5min).<br>3. Aguardar >5min (simular).<br>4. Enviar 1 msg.<br>5. "Ver Stats". | Sessão1: "oi", "mdc" (gap 1min).<br>Sessão2: "porcentagem" (gap 6min). | Sucesso: total=3, media_duracao~(d1 + d2)/2 ~1-2min (2 sessões).<br>Falha: Uma sessão única. | Textbox: "Duração Média: 1.5 min"; log timestamps confirmam gaps. |
| **UAT-13-06** | Validar rotação histórico não afeta stats | CLI | 1. `python main.py`.<br>2. Enviar 6 perguntas (conhecidas).<br>3. /stats (deve total=6, histórico=5). | 6 entradas variadas (tags diferentes). | Sucesso: total=6, histórico len=5 (mostrar_historico), stats agregados intactos.<br>Falha: total=5. | Output /stats: "Total:6"; comando /historico: 5 entradas. |
| **UAT-13-07** | Validar exibição CLI formatada | CLI | 1. Após 3 interações mistas.<br>2. /stats. | Mistura: 2 formal (1 fallback), 1 engracada. | Sucesso: Output com 📊, = separadores, % arredondados (ex. "Formal:2 (66.7%)").<br>Falha: Formato quebrado. | Console: "📊 ESTATÍSTICAS... Total:3, Taxa:33.3%". |
| **UAT-13-08** | Validar exibição Gradio (botão) | Gradio | 1. Após interações.<br>2. Trocar personalidade.<br>3. "Ver Stats". | Após UAT-13-01. | Sucesso: Textbox: "ESTATÍSTICAS ATUAIS (Formal)... Total:1, Formal:1 (100%)".<br>Falha: Erro ou vazio. | Screenshot textbox; chat não interrompido. |
| **UAT-13-09** | Cenário erro: Stats.json corrompido | CLI + Manual | 1. Corromper stats.json (remover ]).<br>2. Reiniciar `python main.py`.<br>3. Enviar 1 msg.<br>4. /stats. | Corrupção: JSON inválido. | Sucesso: Carrega defaults (total=0), atualiza para 1, salva válido.<br>Falha: Crash. | Log: "stats.json inválido, usando defaults"; stats.json recriado válido. |
| **UAT-13-10** | Cenário borda: Zero interações | Gradio | 1. Abrir Gradio.<br>2. "Ver Stats" imediato. | Nenhuma entrada. | Sucesso: total=0, fallback_rate=0%, %=0 ou {}, duração=0.<br>Falha: Erro divisão zero. | Textbox: "Total:0, Taxa:0.0%, Duração:0.0 min". |
| **UAT-13-11** | Usabilidade: Formatação legível multi-linha | CLI | 1. 5 interações (todas personalidades/tags).<br>2. /stats. | Variar: formal/math, engracada/fallback, etc. | Sucesso: Output indentado, emojis, % claros; <80 chars/linha.<br>Falha: Quebrado ou confuso. | Console legível; usuário entende sem scroll excessivo. |
| **UAT-13-12** | Performance: Tempo response <1s | Gradio | 1. Enviar 10 msgs rápidas.<br>2. "Ver Stats".<br>3. Medir tempo (timer). | 10 entradas variadas. | Sucesso: <1s para save + get_stats.<br>Falha: >2s ou lag UI. | Timer: "0.5s"; UI responsiva (sem freeze). |
| **UAT-13-13** | Integração aprendizado: Stats contam aprendido | Gradio | 1. Enviar inexistente (fallback).<br>2. Ensinar resposta.<br>3. Reenviar (non-fallback, tag=None? ou aprendido).<br>4. "Ver Stats". | Inexistente: "Nova pergunta?"; Ensino: "Resposta nova". | Sucesso: total=2, fallback=1 (50%), segunda non-fallback. | Textbox: "Total:2, Taxa:50.0%"; new_data.json +1. |
| **UAT-13-14** | Erro: Timestamp inválido (simular) | CLI + Manual | 1. Editar histórico com timestamp malformado.<br>2. Reiniciar, enviar msg.<br>3. /stats. | Histórico: timestamp="invalid". | Sucesso: Ignora inválido na duração (média sem ele), total intacto.<br>Falha: Crash parse. | Log: "Erro timestamp, pulando"; duração=0 se todos inválidos. |
| **UAT-13-15** | Usabilidade: Troca personalidade mid-sessão | Gradio | 1. 2 msgs formal.<br>2. Trocar para "empatica".<br>3. 1 msg.<br>4. "Ver Stats". | Msgs: "oi" (formal), "ajuda" (empatica). | Sucesso: por_personalidade atualiza (formal:2? wait, por interação; total=3). | Textbox: Distribuição por pers; UI dropdown funcional. |
| **UAT-13-16** | Performance: 20 interações seguidas | CLI | 1. Script ou manual: 20 msgs.<br>2. /stats após cada 5.<br>3. Medir cumulativo. | 20 entradas mistas. | Sucesso: <0.5s/save, total=20, sem lag.<br>Falha: Degradação >2s. | Tempo total <10s; stats precisos. |
| **UAT-13-17** | Borda: Fallback 100% (alta taxa) | Gradio | 1. 5 perguntas inexistentes.<br>2. "Ver Stats". | 5 inventadas (fallback=True, tag=None). | Sucesso: fallback_rate=100%, por_tag={}, duração média baixa. | Textbox: "Taxa:100.0% (5 casos)". |
| **UAT-13-18** | Regressão: Stats não quebra histórico | CLI | 1. 3 interações.<br>2. /historico (ver len=3).<br>3. /stats.<br>4. Limpar histórico (/limpar).<br>5. /stats (total mantido). | Mistura conhecida/fallback. | Sucesso: Histórico limpo (len=0), stats total=3 intacto. | Output /historico: "Não há..."; /stats: "Total:3". |

## 🎯 Critérios de Aceitação
### Obrigatórios (Todos Devem Passar):
1. **Coleta Precisa (100%):** Contadores exatos; fallback_rate/tag % corretos; duração agrupa <5min.
2. **Persistência Segura:** stats.json atômico; recuperação de corrompido com defaults.
3. **Exibição Correta:** Formatação legível (📊, %); CLI/Gradio sem erros.
4. **Integração:** Não quebra histórico/aprendizado; rotação ok.
5. **Robustez:** Edges (zero, inválido) handled; sem crashes.

### Performance:
- Response <1s (save/compute); UI responsiva (Gradio).

### Usabilidade:
- Output intuitivo (emojis, indentação); acessível via botões/comandos.

### Geral:
- Zero regressões em Tasks 08-12; logs auditáveis.

## 📊 Matriz de Rastreabilidade aos Requisitos da Task 13
| **Requisito (plano_task13.md)** | **Casos de Teste Relacionados** | **Status** |
|---------------------------------|---------------------------------|------------|
| Coleta automática (passo 1-2) | UAT-13-01,02,03,13,17 | ⏳ Aguardando |
| Persistência stats.json (passo 2) | UAT-13-06,09,14,18 | ⏳ Aguardando |
| Exposição CLI/Gradio (passo 3-4) | UAT-13-07,08,11,15 | ⏳ Aguardando |
| Duração sessão (passo 2) | UAT-13-04,05 | ⏳ Aguardando |
| Otimização/Edges (passo 5) | UAT-13-10,12,16 | ⏳ Aguardando |
| Riscos (I/O, privacidade) | UAT-13-09,14 | ⏳ Aguardando |

## 🚀 Ambiente de Teste
### Pré-Condições:
- Python 3.8+; Gradio (`pip install gradio` via requirements.txt).
- Arquivos: main.py, app.py, core_data.json, historico.json limpo ([]), stats.json deletado (defaults).
- Ambiente: Local (Windows 11, cmd.exe); timer para performance; editor para corromper JSONs.
- Dados: Perguntas de core_data.json; inventadas para fallback.

### Configuração:
```bash
# CLI
cd c:/workspace/educalin-chat
python main.py

# Gradio (terminal separado)
python app.py  # Acessar http://127.0.0.1:7860
```

## 📋 Procedimentos de Execução, Relatórios e Critérios de Aprovação
### Procedimentos de Execução:
- **Fase 1: Fluxos Principais (UAT-13-01 a 08, 45min):** Executar em ordem; verificar stats.json diff (git ou manual).
- **Fase 2: Erros/Borda (UAT-13-09,10,14,17,18, 30min):** Corromper arquivos; reiniciar.
- **Fase 3: Usabilidade/Performance (UAT-13-11 a 12,15,16, 30min):** Medir tempos; validar legibilidade.
- **Fase 4: Regressão/Integração (UAT-13-13, 15min):** Combinar com aprendizado.
- **Execução:** 1 testador; registrar em planilha/template abaixo. Rodar pytest antes (confirmar automação).

### Relatórios de Resultados:
**Template por Teste:**
| Campo | Descrição |
|-------|-----------|
| **ID** | UAT-13-XXX |
| **Status** | ✅ PASSOU / ❌ FALHOU / ⚠️ PARCIAL |
| **Resultado Obtido** | [Detalhes: ex. total=1, screenshot descrito] |
| **Desvios** | [Diferenças do esperado] |
| **Evidências** | [Screenshots, logs, stats.json diff] |
| **Observações** | [Notas QA] |

**Relatório Final:** Sumário % aprovação; anexar logs/chatbot.log; matriz atualizada.

### Critérios de Aprovação para UAT:
- **100% Casos Críticos (01-08,13):** Passam (coleta/exibição/persistência).
- **≥90% Geral:** Máx 2 falhas não-críticas (corrigir antes deploy).
- **Zero Crashes/Regressões:** Sem impacto em histórico/aprendizado.
- **Performance:** Todos <1s; usabilidade: Output legível sem erros.
- **Aprovação:** Se ≥95%, aprovar para Tasks 14-15; senão, retestar pós-correção.

## 🎯 Conclusão
Este plano garante validação executável e abrangente da Task 13, alinhado a best practices QA para analíticos (cobertura fluxos/erros, rastreabilidade, métricas objetivas). Total 18 casos priorizam críticos, preparando rollout seguro. Execução confirmará aderência 100% e robustez para produção educacional.