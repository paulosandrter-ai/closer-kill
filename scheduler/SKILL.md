---
name: scheduler
description: >-
  Scheduler (agenda). Coloca cada call marcada na sua agenda. Lê uma resposta como "quinta às 14h pode
  ser", "amanhã 10h30" ou "30/10 às 15:00" e transforma na data e hora certas, confere se você já tem
  compromisso, oferece horários livres quando perguntam "qual horário você tem?", cria o convite com link
  do Google Meet na sua própria agenda depois do seu sim, confirma por e-mail ou WhatsApp e move o
  negócio pra call-booked pra os follow-ups pararem. Use quando o usuário disser "marca", "agenda uma
  call", "coloca na minha agenda", "manda o convite", "que horário eu tenho livre", "ela disse que quinta
  pode", ou quando o /follow-up mostrar uma resposta com horário.
argument-hint: "[parse <resposta> | free | book <contato> <horário>]"
---

# scheduler

Na hora que alguém aceita uma call, o Scheduler coloca ela nas duas agendas antes que o momento passe.
Uma call marcada vale mais que dez follow-ups.

Responda sempre em português do Brasil.

`${CLAUDE_SKILL_DIR}` abaixo é a pasta desta skill (onde fica este SKILL.md).

```bash
python3 "${CLAUDE_SKILL_DIR}/slots.py" parse --text "Desculpa, semana corrida! Quinta às 14h pode ser." --today 2026-10-27
python3 "${CLAUDE_SKILL_DIR}/slots.py" free --busy closer/busy.json --from 2026-10-28 --days 3 --length 30
python3 "${CLAUDE_SKILL_DIR}/slots.py" invite --contact dani-sorriso-leve --start 2026-10-29T14:00 --minutes 30
python3 "${CLAUDE_SKILL_DIR}/slots.py" book --contact dani-sorriso-leve --start 2026-10-29T14:00 \
    --minutes 30 --approval "sim" --busy closer/busy.json
```

## Passos

1. **Quando.** `slots.py parse` na resposta. Ele entende português ("quinta às 14h", "amanhã 10h30",
   "segunda que vem às 9", "30/10 às 15:00", "sexta ao meio-dia", "terça às 3 da tarde") e inglês. "às 2"
   sem "da manhã" vira 14h (de 1 a 7 é tarde, de 8 a 12 é manhã). Se aparecer "No clear time", peça um
   horário; nunca chute o dia. Repita a data completa pro usuário: "Quinta, 29 de outubro, às 14:00 no
   seu horário. Certo?"
2. **Conflito.** Com o conector de agenda, leia os compromissos do usuário naquele dia e grave em
   `closer/busy.json` como `[{"start": "...", "end": "..."}]`. Se pediram opções, `slots.py free` lista
   horários livres no horário comercial; ofereça dois ou três.
3. **Perguntar.** "Marco Clínica Sorriso Leve x Sua Agência, quinta 29 de outubro, das 14:00 às 14:30,
   Google Meet, com a Daniela Rocha convidada? Responda sim ou não."
4. **Marcar.** Com o sim, crie o evento na agenda do usuário pelo conector (título, horário, Google Meet,
   a Daniela como convidada). Sem conector de agenda: `slots.py invite` gera um .ics que o usuário abre ou
   anexa.
5. **Registrar.** `slots.py book --approval "<o sim dele>"`. O negócio vai pra call-booked e o
   `/follow-up` para.
6. **Confirmar.** Escreva a resposta com o modelo confirm-time do `/follow-up` ("Quinta às 14h fechado,
   Daniela. Já te mando o convite."), por e-mail ou WhatsApp, e envie só com o sim dela.
7. **Preparar.** Lembre o usuário de rodar o `/researcher` antes da call.

## Exemplo

Ter 27/out, 11:48: "Desculpa, semana corrida! Quinta às 14h pode ser." O `parse` dá quinta, 29 de outubro,
14:00. O usuário está livre, diz sim, e a agenda mostra "Clínica Sorriso Leve x Sua Agência, quinta, 29 de
outubro, 14:00 às 14:30, Google Meet, convidados Daniela Rocha e Ana". (Ilustrativo: a Daniela e a Clínica
Sorriso Leve são fictícias.)

## O que ela nunca faz

- Nunca marca, move ou cancela um evento sem o sim do usuário pra aquele evento exato.
- Nunca marca por cima de algo que já está na agenda do usuário.
- Nunca lê detalhes da agenda além de livre e ocupado pra achar um horário.

## Consentimento e verdade

- Nada é enviado, marcado ou assinado sem o "sim" explícito do usuário pra aquela mensagem, convite ou
  documento exato. O Claude escreve, o usuário diz "sim", e só então sai das contas do próprio usuário:
  convites pela agenda do próprio usuário. Um "sim" por mensagem. Nunca "sim pra todos".
- Pare no primeiro "não" ou em qualquer sinal de desinteresse. Um pedido pra parar vale pra sempre, em
  todas as skills.
- Nunca invente um horário que alguém aceitou. Quando não estiver claro, pergunte.
