---
name: record-keeper
description: >-
  Record Keeper (registro). Registra cada e-mail, WhatsApp e call pra você, pra nunca mais atualizar CRM
  na mão. Lê sua caixa de entrada pelo conector do Gmail, liga cada mensagem a um contato do quadro e
  registra (primeira mensagem, follow-up ou resposta) no closer/pipeline.json; registra conversas de
  WhatsApp que você colar ou exportar; registra calls com as anotações salvas em closer/calls/; mostra o
  histórico completo com qualquer pessoa; e lista endereços novos escrevendo que ainda não são contatos.
  Use quando o usuário disser "registra isso", "registra meus e-mails", "sincroniza a caixa",
  "atualiza o CRM", "qual meu histórico com X", "salva as anotações da call", no fim de cada call e
  toda manhã.
argument-hint: "[sync | timeline <contato> | call <contato>]"
---

# record-keeper

O Record Keeper mantém o quadro verdadeiro sem ninguém digitar nele. Cada e-mail e mensagem que entra e
sai, e cada call, vai parar no `closer/pipeline.json` (o formato que o `/pipeline` define), uma vez só.

Responda sempre em português do Brasil.

`${CLAUDE_SKILL_DIR}` abaixo é a pasta desta skill (onde fica este SKILL.md).

```bash
python3 "${CLAUDE_SKILL_DIR}/log.py" sync --emails closer/inbox-2026-10-27.json
python3 "${CLAUDE_SKILL_DIR}/log.py" unknown --emails closer/inbox-2026-10-27.json
python3 "${CLAUDE_SKILL_DIR}/log.py" log --contact dani-sorriso-leve --channel email --direction in \
    --subject "Re: Ideia rápida pra Clínica Sorriso Leve" --text "Desculpa, semana corrida! Quinta às 14h pode ser." \
    --at 2026-10-27T11:48
python3 "${CLAUDE_SKILL_DIR}/log.py" log --contact priscila-bemtevi --channel whatsapp --direction in \
    --text "Talvez! Pode me mandar os valores?" --at 2026-10-22T16:10
python3 "${CLAUDE_SKILL_DIR}/log.py" call --contact dani-sorriso-leve --minutes 24 \
    --notes-file /tmp/sorriso-leve-notas.md --at 2026-10-29T14:00
python3 "${CLAUDE_SKILL_DIR}/log.py" timeline --contact dani-sorriso-leve
```

## Sincronizando e-mail

1. Com o conector do Gmail, busque na caixa do usuário, desde a última sincronização, mensagens de ou
   para o endereço de algum contato (`from:daniela@sorrisoleve.com.br OR to:daniela@sorrisoleve.com.br ...`).
   Leia só esses fios. Nunca leia outros e-mails pra isso.
2. Escreva o que achou num arquivo de sincronização: uma lista JSON de
   `{"date": "YYYY-MM-DDTHH:MM", "from": "...", "to": ["..."], "subject": "...", "text": "..."}`
   com o texto cortado só na parte nova de cada mensagem (sem o histórico citado).
3. `log.py sync --emails <arquivo>`. Ele pula o que já foi registrado, então rodar duas vezes é seguro.
   E-mail que o usuário mandou da própria caixa é registrado com a aprovação "sent by you from your inbox".
4. Se uma resposta diz não ou pede pra parar, avise o usuário e rode o `reply` do `/follow-up` pra essa
   pessoa, pra todas as skills pararem. Não só registre.
5. `log.py unknown` lista endereços que escreveram mas não são contatos. Pergunte ao usuário antes de
   adicionar qualquer um.

Sem conector do Gmail? O usuário pode colar ou encaminhar os e-mails, e você registra com `log.py log`.

## Registrando WhatsApp e Instagram

Não existe conector que leia o WhatsApp do usuário. Ele cola as mensagens (ou exporta a conversa em
"Mais > Exportar conversa > Sem mídia") e você registra cada mensagem nova com
`log.py log --channel whatsapp` (ou `instagram`), `--direction in` pro que o contato mandou e
`--direction out --approval "<o sim>"` pro que o usuário mandou. Leia só as conversas com contatos do quadro.

## Registrando uma call

Depois de cada call, escreva as anotações em linhas simples: o que a pessoa precisa, o que disse sobre
preço, o que foi combinado, o próximo passo e a data. Depois `log.py call`. O arquivo de anotações vai pra
`closer/calls/<data>-<empresa>.md` e um resumo de uma linha vai pro quadro. Se o `/sales-coach` rodou na
call, use a saída do `review` como parte das anotações.

## Exemplo

O fio da Daniela, registrado sem digitar nada: a primeira mensagem na seg 19/out às 9:02, follow-ups em
21, 23 e 27/out, a resposta dela na ter 27/out às 11:48 ("Desculpa, semana corrida! Quinta às 14h pode
ser."), e a call na qui 29/out: "Call, 24 min. Adorou o site. Objeção de preço nos R$ 2.500; topou o plano
de R$ 399/mês, sem taxa de implantação. Quer começar segunda." `timeline --contact dani-sorriso-leve`
mostra tudo. (Ilustrativo: a Daniela e a Clínica Sorriso Leve são fictícias.)

## O que ela nunca faz

- Nunca registra uma mensagem enviada que o usuário não mandou ou não aprovou.
- Nunca lê e-mail ou conversa além das que são com contatos conhecidos, e nunca guarda anexos.
- Nunca edita nem apaga o que já foi registrado: uma correção é uma nota nova.

## Consentimento e verdade

- Nada é enviado, marcado ou assinado sem o "sim" explícito do usuário pra aquela mensagem, convite ou
  documento exato. Esta skill só registra; nunca envia nada.
- Calls: avise todo mundo na call que a legenda ou as anotações estão ligadas, antes de começar. Gravar
  ou transcrever uma conversa usa dados pessoais (LGPD), então a pessoa precisa saber.
- Pare no primeiro "não" ou em qualquer sinal de desinteresse. Um pedido pra parar vale pra sempre, em
  todas as skills.
- Nunca invente o que foi dito. As anotações são o que aconteceu, em palavras simples.
