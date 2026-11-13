---
name: win-back
description: >-
  Win-Back (reconquista). Traz de volta os negócios que esfriaram. Acha negócios perdidos que valem mais
  uma tentativa (momento ruim, orçamento, "vou pensar", sem decisão) depois de tempo suficiente ou na data
  que a pessoa pediu pra você voltar, além de negócios abertos que ficaram em silêncio depois de todos os
  follow-ups, e escreve uma mensagem curta e honesta a partir do motivo da perda. Uma reconquista por
  negócio, nunca pra quem disse não ou pediu pra sair. Use quando o usuário disser "reconquistar",
  "reativar negócios antigos", "follow-up dos perdidos", "quem sumiu", "reengajar", "leads mortos",
  "clientes que esfriaram", ou uma vez por semana.
argument-hint: "[list | draft <negócio>]"
---

# win-back

"Agora não" não é "não". O Win-Back lembra quem disse agora não e volta uma vez, na hora certa, com um
motivo pra conversar. Ele nunca corre atrás de quem disse não.

Responda sempre em português do Brasil.

`${CLAUDE_SKILL_DIR}` abaixo é a pasta desta skill (onde fica este SKILL.md).

```bash
python3 "${CLAUDE_SKILL_DIR}/winback.py" list --today 2026-10-29
python3 "${CLAUDE_SKILL_DIR}/winback.py" draft --deal serra-azul-site --today 2026-10-29
python3 "${CLAUDE_SKILL_DIR}/winback.py" record --deal serra-azul-site --text-file /tmp/w.txt \
    --approval "sim" --at 2026-10-29T10:00
```

## Quem ele tenta, e quando

- **Perdido por momento, orçamento, "vou pensar" ou sem decisão:** 60 dias depois da perda, ou na data
  `revisit` do próprio negócio se a pessoa deu uma ("me procura depois do carnaval": coloque `revisit` no
  negócio).
- **Perdido pra outra agência:** nunca antes de 180 dias, e só um "como estão as coisas?" simpático.
- **Aberto mas em silêncio:** 30 dias sem atividade depois que o `/follow-up` usou os 3 follow-ups.
- **Nunca:** quem disse não, pediu pra sair ou está como do-not-contact. Nunca duas vezes: uma reconquista
  por negócio, e se não tiver resposta, acabou. Outra tentativa só depois que a pessoa responder, e 90
  dias depois.

Os motivos de perda são lidos em português e em inglês ("alta temporada", "tá caro", "fechou com outra
agência", "sumiu").

## Passos, uma vez por semana

1. `winback.py list`. Leia os READY pro usuário com o porquê, os maiores primeiro. Cite os LATER com a data.
2. Pra cada um que o usuário quiser, `winback.py draft`. Deixe mais específico com uma coisa nova e
   verdadeira se tiver (um plano novo, um resultado de um negócio parecido). Até 60 palavras, e mantenha a
   saída fácil: "Se não, sem problema nenhum, é só me falar que eu deixo quieto."
3. Pergunte: "Mando essa pro Tomás da Telhados Serra Azul? Responda sim ou não."
4. Com o sim: rascunho no Gmail do usuário, e ele envia (ou sai pelo conector do Gmail logo depois daquele
   sim), ou o usuário manda pelo WhatsApp. Depois `winback.py record --approval "<o sim dele>"`. O negócio
   reabre.
5. Se a pessoa responder, é conversa: `/follow-up reply`, depois `/scheduler`.

## Exemplo

O Tomás Becker da Telhados Serra Azul gostou da ideia em julho, mas disse que era alta temporada e pediu
pra procurar de novo em novembro. Perdido em 10/ago por momento. Em 29/out o `list` mostra READY, e a
mensagem fica: "Oi Tomás, quando a gente conversou você disse que não era o momento e pediu pra eu voltar em
novembro. Agora ficou melhor pra site + avaliações no site? Se não, sem problema nenhum, é só me falar que
eu deixo quieto." A Elena Ruiz da Mesa Verde Estética pediu pra sair da lista, então aparece como NEVER.
(Ilustrativo: as duas empresas são fictícias.)

## O que ela nunca faz

- Nunca manda mensagem pra quem disse não, pediu pra sair ou está como do-not-contact.
- Nunca manda uma segunda reconquista depois de uma primeira sem resposta.
- Nunca inventa um motivo pra escrever ("acabei de ver seu post", "um colega falou de você") que não é verdade.

## Consentimento e verdade

- Nada é enviado, marcado ou assinado sem o "sim" explícito do usuário pra aquela mensagem, convite ou
  documento exato. O Claude escreve, o usuário diz "sim", e só então sai das contas do próprio usuário.
  Um "sim" por mensagem. Nunca "sim pra todos".
- Pare no primeiro "não" ou em qualquer sinal de desinteresse. Um pedido pra parar vale pra sempre, em
  todas as skills.
- Toda mensagem é honesta sobre quem está escrevendo e mantém um jeito simples de sair. Quem sai, sai pra
  sempre.
- Nunca invente um número, um resultado, um cliente, uma avaliação ou um prazo.
