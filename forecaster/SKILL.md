---
name: forecaster
description: >-
  Forecaster (previsão). Diz quanto você vai fechar este mês. Lê cada negócio aberto do quadro com etapa,
  valor e data de fechamento e dá três números: garantido (contratos enviados), provável (cada negócio
  ponderado pela chance da etapa) e melhor cenário, negócio por negócio, além do que você já fechou, em
  reais. Mostra sua taxa de conversão real e quanto tempo os negócios levam quando já tiver histórico, e
  aponta o que deixa a previsão errada: datas de fechamento vencidas, negócios sem data, negócios parados.
  Use quando o usuário disser "previsão", "quanto vou fechar esse mês", "como está o mês", "projeção de
  faturamento", "taxa de conversão", "valor do funil", ou no começo de cada semana.
argument-hint: "[month YYYY-MM | rates | health]"
---

# forecaster

O Forecaster responde a pergunta que todo dono de negócio faz na segunda-feira: quanto dinheiro entra de
verdade este mês? Ele mostra a conta, pra o número poder ser confiado ou questionado.

Responda sempre em português do Brasil.

`${CLAUDE_SKILL_DIR}` abaixo é a pasta desta skill (onde fica este SKILL.md).

```bash
python3 "${CLAUDE_SKILL_DIR}/forecast.py" month --month 2026-11 --today 2026-10-29
python3 "${CLAUDE_SKILL_DIR}/forecast.py" rates
python3 "${CLAUDE_SKILL_DIR}/forecast.py" health --today 2026-10-29
```

## Os três números

- **Garantido:** negócios em contract-sent com data de fechamento neste mês. É esse número que você diz
  quando alguém pergunta quanto vai fechar.
- **Provável:** cada negócio aberto que fecha neste mês, vezes a chance da etapa dele.
- **Melhor cenário:** cada negócio aberto que fecha neste mês, se todos assinarem.

Chances por etapa pra começar: lead 5%, contacted 10%, replied 20%, call-booked 30%, proposal 50%,
contract-sent 80%. Quando o usuário tiver 10 ou mais negócios fechados, elas são ajustadas pela taxa de
conversão real dele, e a saída avisa. Quem pediu pra sair de uma mensagem fria não conta como venda perdida.

## Passos, toda segunda-feira

1. `/record-keeper sync` antes, pra o quadro estar atualizado.
2. `forecast.py health`. Resolva o que ele apontar antes de prever: peça ao usuário uma data real pra
   negócio sem data, e mova ou feche negócios com data vencida (`/pipeline move`).
3. `forecast.py month`. Leia os três números, depois os negócios que mais pesam, os maiores ponderados primeiro.
4. Diga o que mexeria no número: "A call do Estúdio Jasmim na terça vale R$ 1.436 do provável; prepare
   com o /researcher."
5. `forecast.py rates` uma vez por mês: taxa de conversão e dias pra fechar.

## Exemplo

Pra novembro de 2026, em 29 de outubro: Garantido R$ 4.788 (Clínica Sorriso Leve, contrato enviado).
Provável R$ 6.474: Sorriso Leve R$ 4.788 x 80%, Estúdio Jasmim Yoga R$ 4.788 x 30%, Bem-te-vi Pet Spa
R$ 4.788 x 20%, Academia Pulso Forte R$ 2.500 x 10%. Melhor cenário R$ 16.864. Base: chances padrão por
etapa (menos de 10 negócios fechados ainda). (Ilustrativo: o quadro é `../pipeline/pipeline.example.json`,
todos os negócios nele são fictícios.)

## O que ela nunca faz

- Nunca chama uma previsão de promessa, e nunca esconde em que ela se baseia.
- Nunca muda sozinha o valor ou a data de fechamento de um negócio: pergunta ao usuário.

## Consentimento e verdade

- Nada é enviado, marcado ou assinado sem o "sim" explícito do usuário pra aquela mensagem, convite ou
  documento exato. Esta skill só lê o quadro.
- Nunca invente um número, um resultado, um cliente ou um prazo. Preencha só o que é verdade e pergunte
  quando faltar algo.
- Previsões são estimativas, não orientação financeira.
