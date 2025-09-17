# Análise do Erro: ValueError - Unpacking em processar_mensagem

## Descrição do Erro
Ao executar comandos no app.py (via Gradio), ocorre o erro:
```
ValueError: not enough values to unpack (expected 3, got 2)
```
Traceback aponta para linha 80 em [`app.py`](app.py:80):
```python
resposta_bot, is_fallback, tag = aline_bot.processar_mensagem(user_message, pers)
```

## Causa Raiz
- O método `processar_mensagem` em [`core/chatbot.py`](core/chatbot.py:18) retorna apenas 2 valores: `Tuple[str, bool]` (resposta, is_fallback).
- No entanto, o unpacking espera 3 valores (resposta, is_fallback, tag).
- Isso é uma incompatibilidade introduzida na Task 13, onde o retorno foi expandido na expectativa de propagar a tag para stats/histórico, mas o método não foi atualizado.

## Evidências nos Logs
- Log: "✅ EXATA base -> tag 'saudacao'" indica que o matcher encontrou uma intenção com tag.
- Mas a tag não é retornada para app.py, causando falha no unpacking.
- O matcher em [`core/intent_matcher.py`](core/intent_matcher.py:60) retorna dict com "tipo": "intent" e "intencao" (que tem "tag"), ou "aprendido" (sem tag), ou None (fallback, sem tag).

## Dependências Afetadas
- Linha 95 em app.py: `# aline_bot.update_stats(is_fallback, tag)` (comentada, mas planeja usar tag para estatísticas por tag).
- `get_stats()` em Chatbot é chamado (linha 140), mas não implementa uso de tag ainda (código atual não mostra detalhes de stats.json).
- Histórico é salvo sem tag explicitamente, mas poderia ser estendido.

## Solução Proposta
1. Modificar `processar_mensagem` em core/chatbot.py para retornar 3 valores:
   - Se match["tipo"] == "intent": retornar resposta, False, match["intencao"]["tag"]
   - Se match["tipo"] == "aprendido": retornar resposta, False, None (ou "aprendido")
   - Se None/fallback: retornar resposta, True, None
2. Atualizar assinatura: `-> Tuple[str, bool, Optional[str]]`
3. Descomentar/atualizar update_stats se necessário para coletar tags.
4. Testar com input "oi" (deve retornar tag 'saudacao', is_fallback=False).

## Impacto
- Correção mínima, cirúrgica (usar apply_diff).
- Mantém compatibilidade com histórico existente.
- Prepara para stats por tag em futuras tasks.