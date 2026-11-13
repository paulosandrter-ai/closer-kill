---
name: follow-up
description: >-
  Follow-Up. Continua fazendo follow-up até a call ser marcada, e aí para. Toda manhã lê o
  closer/pipeline.json e diz quem precisa de follow-up hoje, quem respondeu e está esperando você,
  quem já marcou e quem está parado e por quê. Escreve cada follow-up (um lembrete, depois algo útil,
  depois uma última mensagem educada), por e-mail ou WhatsApp, espera o seu sim, registra, e para no
  primeiro "não", na hora que a call é marcada, depois de 3 follow-ups ou de 30 dias. Use quando o
  usuário disser "follow-up", "faz o follow", "quem eu preciso cobrar", "não me responderam", "dar um
  toque", "lembrar fulano", "responderam", ou toda manhã.
argument-hint: "[due | draft <contato> | reply <contato>]"
---

# follow-up

A maioria das vendas se perde no silêncio, não no "não". Esta skill garante que ninguém seja esquecido
e ninguém seja incomodado. Ela escreve; nunca envia sozinha.

Responda sempre em português do Brasil.

`${CLAUDE_SKILL_DIR}` abaixo é a pasta desta skill (onde fica este SKILL.md).

```bash
python3 "${CLAUDE_SKILL_DIR}/followup.py" due --today 2026-10-21
python3 "${CLAUDE_SKILL_DIR}/followup.py" draft --contact dani-sorriso-leve --today 2026-10-21
python3 "${CLAUDE_SKILL_DIR}/followup.py" draft --contact dani-sorriso-leve --today 2026-10-23 \
    --hook "fiz uma prévia de 1 minuto de como ficaria o agendamento online da Sorriso Leve."
python3 "${CLAUDE_SKILL_DIR}/followup.py" record --contact dani-sorriso-leve --text-file /tmp/f.txt \
    --approval "sim" --at 2026-10-21T09:00 --channel email
python3 "${CLAUDE_SKILL_DIR}/followup.py" reply --contact dani-sorriso-leve \
    --text "Desculpa, semana corrida! Quinta às 14h pode ser." --at 2026-10-27T11:48 --channel email
python3 "${CLAUDE_SKILL_DIR}/followup.py" stop --contact <id> --said "Por favor, me tire da sua lista."
```

## As regras (por pessoa, em todos os canais)

1. **Pare no primeiro "não"** ou em qualquer sinal de desinteresse ("não tenho interesse", "não,
   obrigado", "já fechamos com outra agência", "me tira da lista"). Um pedido pra sair vai pra lista de
   supressão, e nenhuma skill manda mensagem de novo.
2. **Pare na hora que a call é marcada.** Esse é o objetivo. `/scheduler` e `/sales-coach` assumem.
3. **Resposta é a sua vez.** Responder é conversa, nunca "follow-up".
4. **No máximo 3 follow-ups** depois da primeira mensagem, e o terceiro avisa que é o último.
5. **Nada depois de 30 dias** da primeira mensagem sem resposta. O `/win-back` pode tentar uma vez,
   bem depois.

O `draft` se recusa a escrever e o `record` se recusa a registrar qualquer coisa que quebre uma regra.
As frases de "não" e de "sair da lista" são reconhecidas em português e em inglês, com ou sem acento.

## A cadência

Follow-up 1 dois dias depois da primeira mensagem, follow-up 2 dois dias depois, follow-up 3 quatro dias
depois. Data em fim de semana passa pra segunda. No exemplo: seg 19/out (primeira mensagem), qua 21/out,
sex 23/out, ter 27/out.

1. **Follow-up 1, o lembrete.** Uma linha: "só subindo essa mensagem caso tenha se perdido."
2. **Follow-up 2, entregue algo.** Uma prévia, um número, uma ideia curta pra eles. `--hook` é essa coisa
   nova, verdadeira e específica. Sem gancho não tem follow-up 2.
3. **Follow-up 3, a última.** Ofereça um dia pra call e diga que é a última mensagem. Qualquer resposta serve.

## Passos, toda manhã

1. Rode `/record-keeper sync` antes, pra as respostas estarem no quadro.
2. `followup.py due`. Leia pro usuário agrupado como aparece: DUE NOW (vence hoje), YOUR TURN (responderam),
   WAITING (aguardando), BOOKED (marcado), STOPPED (parado).
3. Pra cada DUE NOW, `followup.py draft`. Preencha todo `[fill: ...]`. Mostre: "Mando esse follow-up pra
   Daniela? Responda sim ou não." Uma mensagem por pergunta.
4. Com o sim: e-mail vira rascunho no mesmo fio, no Gmail do usuário, e ele envia (ou sai pelo conector do
   Gmail logo depois daquele sim). WhatsApp: o usuário cola e envia na mesma conversa. Depois,
   `followup.py record --approval "<o sim dele, palavra por palavra>" --channel <canal>`.
5. Pra cada YOUR TURN: se deram um horário, passe pro `/scheduler` (`slots.py parse`), confirme com o
   modelo `confirm-time` e marque. Se disseram não, `followup.py reply` com as palavras deles: isso para
   tudo e marca o negócio como perdido.

Uma rotina agendada de manhã pode listar e escrever. Nunca envia: não tem ninguém ali pra dizer sim.

## Exemplo

A Daniela Rocha não respondeu a primeira mensagem. Follow-up 1 na qua 21/out: "só subindo essa mensagem
caso tenha se perdido." Follow-up 2 na sex 23/out: a prévia de 1 minuto. Follow-up 3 na ter 27/out: "posso
encerrar por aqui, ou quinta fica bom pra uma call rápida?" Às 11:48 ela respondeu: "Desculpa, semana
corrida! Quinta às 14h pode ser." O `reply` passou ela pra YOUR TURN; a call foi marcada e ela não recebeu
mais nenhum follow-up. (Ilustrativo: a Daniela e a Clínica Sorriso Leve são fictícias.)

## O que ela nunca faz

- Nunca envia, e nunca registra uma mensagem que não saiu.
- Nunca faz follow-up depois de um não, de uma call marcada, de 3 follow-ups ou de 30 dias.
- Nunca usa culpa, urgência falsa, "Re:" falso ou um motivo inventado pra escrever.

## Consentimento e verdade

- Nada é enviado, marcado ou assinado sem o "sim" explícito do usuário pra aquela mensagem, convite ou
  documento exato. O Claude escreve, o usuário diz "sim", e só então sai das contas do próprio usuário.
  Um "sim" por mensagem. Nunca "sim pra todos".
- Pare no primeiro "não" ou em qualquer sinal de desinteresse. Um pedido pra parar vale pra sempre, em
  todas as skills.
- Toda mensagem mantém a linha de saída da primeira conversa. Quem sai, sai pra sempre.
- Nunca invente um número, um resultado, um cliente, uma avaliação ou um prazo.
