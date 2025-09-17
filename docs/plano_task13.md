# Plano de Implementação: Task 13 - Implementação da Coleta de Estatísticas

## Visão Geral da Task
**Objetivos Principais:**
- Implementar um sistema de coleta e agregação de estatísticas de uso do chatbot EducAlin, baseado no histórico de interações (historico.json).
- Preparar dados para Tasks dependentes: Geração de relatório (Task 14) e sugestões de FAQs (Task 15).
- Rastrear métricas chave: total de interações, interações por personalidade, taxa de fallback (respostas desconhecidas), frequência por tag de intenção (ex.: matemática básica), duração média de sessão (se aplicável).

**Requisitos:**
- Coleta automática após cada interação (CLI e Gradio).
- Persistência em arquivo JSON (stats.json) para agregados, além de histórico detalhado.
- Exposição via comandos (/stats) e interface Gradio (botão ou chat).
- Manter compatibilidade com rotação de histórico (últimas 5, mas stats agregadas totais).
- Sem impacto em performance (histórico limitado).

**Escopo:** Foco em coleta básica; análise avançada (ex.: ML para FAQs) para Tasks 15+.

## Análise de Impactos na Base de Código Atual
- **Módulos Afetados:**
  - `main.py` (Classe Chatbot): Adicionar métodos `_atualizar_stats()` (chamado em `_salvar_historico`), `get_stats()` (retorna dict com métricas).
  - `app.py` (Gradio): Integrar exibição de stats em chat ou novo componente (ex.: textbox para stats).
  - `historico.json`: Expandir entradas com campos: 'tag_intencao' (da melhor_intencao), 'is_fallback' (bool), 'timestamp_out' (para duração).
  - Novo: `stats.json` para agregados (total_interactions, por_personalidade: dict, fallback_rate: float).
- **Integrações Necessárias:**
  - Em `processar_mensagem()`: Retornar também tag_intencao para passar ao histórico.
  - Em `_salvar_historico()`: Incrementar contadores e salvar agregados atomicamente.
  - Comandos CLI: Novo /stats em `_processar_comando_especial()`.
  - Gradio: Função `mostrar_stats()` similar a `enviar_mensagem`.
- **Padrões Atuais Mantidos:** Salvamento atômico (backup/tmp), validação de entrada, logging. Evitar duplicação (Chatbot central).

## Dependências Técnicas
- **Bibliotecas:** Python stdlib (json, datetime, collections.Counter para contagens). Gradio (existente para GUI). Sem novas installs (requirements.txt inalterado).
- **APIs/Serviços Externos:** Nenhum. Tudo local (JSON files).
- **Arquivos Existentes:** historico.json (fonte primária), core_data.json (para tags de intenção). Novo: stats.json.
- **Dependências de Tasks:** Tasks 11-12 (histórico funcional). Bloqueia Tasks 14-15.

## Passos Sequenciais de Implementação
1. **Preparar Estrutura de Dados (2-3h, Responsável: Dev Principal)**
   - Editar `_achar_melhor_intencao()` para retornar tag se encontrada.
   - Expandir `processar_mensagem()`: Retornar (resposta, is_fallback, tag_intencao ou None).
   - Atualizar `_salvar_historico()`: Incluir 'tag_intencao', 'is_fallback', timestamp_out = datetime.now().
   - Estimativa: Testar localmente com mocks.

2. **Implementar Coleta e Agregação de Stats (4-6h, Responsável: Dev Principal)**
   - Adicionar self.stats = {} no __init__ (carregar de stats.json se existir).
   - Novo método `_atualizar_stats()`: Usar Counter para por_personalidade, total_interactions +=1, fallback_count se is_fallback.
   - Chamar em `_salvar_historico()` após append.
   - Salvar stats.json atomicamente (similar a histórico).
   - Estimativa: Incluir duração (timestamp_out - in).

3. **Integrar em Interfaces (3-4h, Responsável: Dev Frontend/Backend)**
   - CLI: Em `_processar_comando_especial()`, /stats -> formatar self.get_stats() como str (ex.: "Total: X, Formal: Y%").
   - Gradio: Nova função `mostrar_stats(personalidade, chat_history, state)`: Adicionar stats ao chat. Botão "Ver Stats".
   - Atualizar `enviar_mensagem()`: Passar tag/is_fallback para histórico.
   - Estimativa: Testar fluxo end-to-end.

4. **Criar Método de Exposição de Stats (2h, Responsável: Dev Principal)**
   - `get_stats()`: Computar on-demand (fallback_rate = fallback_count / total, por_tag via loop histórico).
   - Formatação legível (JSON dump indentado ou str formatada).
   - Estimativa: Integrar logging para debug.

5. **Otimizar e Refatorar (1-2h, Responsável: Dev Sênior)**
   - Garantir rotação histórico não afete stats agregados.
   - Adicionar validação em stats.json load/save.
   - Estimativa: Review código.

Total Estimado: 12-17h.

## Estratégias de Teste e Critérios de Aceitação
- **Unitários (pytest):** Novo test_stats.py: Testar _atualizar_stats() com mocks (ex.: assert total==5 após 5 saves). Cobrir edge: histórico vazio, fallback 100%.
  - Critério: 100% pass, cobertura >80% (usar coverage.py).
- **Integração:** Estender test_historico.py: Simular saves, assert stats.json atualizado corretamente (ex.: por_personalidade['formal'] == 3).
  - Critério: Sem regressão em histórico; stats refletem entradas.
- **End-to-End:** Simular sessões CLI (iniciar_conversa com inputs mock) e Gradio (demo.launch, interagir via script). Verificar /stats exibe corretos.
  - Critério: Stats precisos em cenários reais; fallback_rate calculada right; UI mostra sem erros.
- **Geral:** Rodar suite existente (test_historico, etc.) pós-mudanças. UAT: Usuários testam 10+ interações, verificam stats.

## Riscos Potenciais, Desafios e Mitigações
- **Risco: Overhead I/O em saves atômicos (alta frequência).** Desafio: Histórico salva a cada msg. Mitigação: Batch saves (salvar stats a cada 5 interações); monitor logging; limite histórico a 5 ok para low volume.
- **Risco: Privacidade/Dados Sensíveis no histórico (perguntas usuário).** Desafio: Stats incluem tags, mas perguntas raw. Mitigação: Anonimizar (hash perguntas ou remover em stats); aviso em README; GDPR-like (não aplica, mas boa prática).
- **Risco: Edge Cases em Computação (ex.: divisão zero em rates).** Desafio: Stats vazios. Mitigação: Defaults (0.0), testes comprehensivos.
- **Risco: Regressão em Histórico/Processamento.** Desafio: Mudanças em processar_mensagem. Mitigação: Tests first, CI GitHub Actions se setup.
- **Desafio Geral: Definição de Métricas (sem spec detalhada).** Mitigação: Basear em histórico fields; iterar com user feedback.

## Métricas de Sucesso e Plano de Rollout/Deploy
- **Métricas:**
  - Funcional: interacoes_count == len(historico) + agregados; fallback_rate precisa (ex.: 20% em testes).
  - Qualidade: Zero crashes em 100+ simulações; cobertura testes >90%; tempo response <1s.
  - Uso: Após rollout, monitor logs para 10+ interações reais sem issues.
- **Plano de Rollout:**
  1. Commit Git: Branch 'feature/task13-stats', merge main após review.
  2. Update: README.md (seção Stats), requirements.txt (se new lib, mas none).
  3. Deploy Local: Rodar python main.py / python app.py; share Gradio se test.
  4. Monitor: Logs em chatbot.log; UAT via GitHub issues.
  5. Pós-Rollout: Update STATUS_REQUISITOS.md (Task 13 ✅), prepare Task 14.

```mermaid
flowchart TD
    A[Início Interação] --> B[processar_mensagem: Get tag, fallback]
    B --> C[_salvar_historico: Add entry com timestamp_in/out, tag, fallback]
    C --> D[_atualizar_stats: Counter++ por pers/tag/fallback]
    D --> E[Salvar stats.json atômico]
    F[Comando /stats ou Botão GUI] --> G[get_stats: Compute rates, format]
    G --> H[Exibir em CLI/Chat]
    style A fill:#f9f
    style H fill:#bbf