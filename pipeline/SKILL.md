---
name: pipeline
description: >-
  Pipeline (CRM). Mantém todos os negócios andando num quadro só, o CRM que as outras dez skills do
  Closer Kill compartilham: contatos, negócios, etapas (lead, contacted, replied, call-booked, proposal,
  contract-sent, won, lost), cada e-mail, WhatsApp e call, próximos passos e uma lista de quem nunca mais
  deve ser contatado, tudo num arquivo simples closer/pipeline.json no seu projeto. Mostra o quadro, o
  histórico de um negócio, move negócios entre etapas e valida o arquivo depois de cada mudança. Use
  quando o usuário disser "pipeline", "funil", "quadro", "meus negócios", "CRM", "como está o X",
  "move o X pra proposta", "fechamos o X", "perdemos o X", "configura o closer kill", ou quiser trocar
  RD Station, Pipedrive, HubSpot ou planilha.
argument-hint: "[board | show <negócio> | move <negócio> <etapa>]"
---

# pipeline

O quadro que todas as outras skills do Closer Kill leem e escrevem. Ele substitui o CRM: um arquivo
JSON no projeto do usuário, sem conta, sem licença por usuário, sem mensalidade.

Responda sempre em português do Brasil. Os comandos e nomes de etapa ficam em inglês porque são o
formato do arquivo.

`${CLAUDE_SKILL_DIR}` abaixo é a pasta desta skill (onde fica este SKILL.md).

```bash
python3 "${CLAUDE_SKILL_DIR}/deals.py" init --name "Ana" --company "Sua Agência" \
    --email contato@suaagencia.com.br --phone "+55 85 99999-0000" \
    --address "Av. Santos Dumont, 1000, sala 400, Fortaleza - CE, 60150-160" --timezone America/Fortaleza \
    --offer "sites com agendamento online e tráfego pago (Google e Meta Ads)" --price "R\$ 2.500" \
    --plan_b "plano mensal de R\$ 399, sem taxa de implantação" \
    --value_line "A maioria das clínicas recupera o investimento com 2 pacientes novos por mês."
python3 "${CLAUDE_SKILL_DIR}/deals.py" board --today 2026-10-29
python3 "${CLAUDE_SKILL_DIR}/deals.py" show --deal sorriso-leve-site
python3 "${CLAUDE_SKILL_DIR}/deals.py" move --deal serra-azul-site --stage lost \
    --reason "timing: alta temporada, pediu pra procurar de novo em novembro"
python3 "${CLAUDE_SKILL_DIR}/deals.py" validate
```

Todo comando aceita `--file` (padrão `closer/pipeline.json`).

## Primeira vez

1. Pergunte ao usuário: nome, nome da empresa, e-mail e WhatsApp de onde ele vende, endereço comercial
   (toda mensagem comercial diz quem está mandando e de onde), fuso horário, o que vende, o preço, uma
   segunda opção menor e uma frase verdadeira sobre o retorno que o serviço dá. Não chute nada disso.
2. `deals.py init` com essas respostas. CNPJ é opcional: se o usuário quiser no contrato, adicione
   `"cnpj"` dentro de `me` no arquivo.
3. Se ele vier do RD Station, Pipedrive, HubSpot ou de uma planilha, peça a exportação de contatos e
   negócios abertos em CSV e adicione cada um com `deals.py contact` e `deals.py deal`. Mapeie as etapas
   dele para as oito abaixo e mostre o mapeamento antes de gravar qualquer coisa.

## O arquivo

```
me          quem você é e o que vende (offer, price, plan_b, value_line, proof, address, cnpj)
contacts    id, name, title, company, email, phone, website, source, notes, do_not_contact
deals       id, contact_id, title, stage, value, currency, close_date, created, next_step, lost_reason
activities  id, date, contact_id, deal_id, channel, type, direction, subject, text, approval
suppression e-mails que nunca mais podem receber mensagem
```

Etapas, em ordem: `lead, contacted, replied, call-booked, proposal, contract-sent, won, lost`.
Canais: `email, whatsapp, instagram, call, meeting, linkedin, sms, note`.
O valor é quanto o negócio vale no primeiro ano (um plano de R$ 399/mês vale 4788). A moeda padrão é BRL.
Toda mensagem que sai (e-mail, WhatsApp, Instagram, LinkedIn ou SMS) precisa ter `approval`: o "sim" do
usuário, palavra por palavra. O `validate` falha sem isso, então nada pode ser registrado como enviado
sem aprovação. Um negócio perdido precisa de `lost_reason`: é o que o `/win-back` lê depois.

## Passos, toda manhã

1. `deals.py board`. Leia pro usuário etapa por etapa, os maiores negócios primeiro, com cada próximo passo.
2. Aponte tudo que estiver marcado `[quiet N days]` e diga qual skill resolve: `/follow-up` pra quem não
   respondeu, `/scheduler` quando responderam com um horário, `/proposal-writer` depois de uma call,
   `/contract-writer` quando escolheram uma opção.
3. Quando o usuário contar uma mudança ("perdemos a Serra Azul, momento ruim"), `deals.py move` com o
   motivo nas palavras dele.

## Exemplo

Na quinta, 29 de outubro de 2026, depois da call com a Daniela Rocha da Clínica Sorriso Leve, o quadro
mostra `CONTRACT-SENT (1, R$ 4.788)  Site + Google Ads, mensal  Clínica Sorriso Leve  next: Daniela
assinar o contrato`. `show --deal sorriso-leve-site` lista a primeira mensagem em 19/out, três
follow-ups, a resposta dela em 27/out, a call marcada, a call de 24 minutos e o contrato às 14:31. O
estado completo está em `pipeline.example.json` ao lado deste arquivo (ilustrativo: a agência, a Daniela
e todos os negócios são fictícios).

## O que ela nunca faz

- Nunca apaga um contato ou uma atividade: o histórico é o registro. Quem pediu pra parar continua no
  arquivo como do-not-contact, pra nenhuma skill mandar mensagem de novo.
- Nunca marca como enviado o que não foi, nem como ganho o que não foi assinado.

## Consentimento e verdade

- Nada é enviado, marcado ou assinado sem o "sim" explícito do usuário pra aquela mensagem, convite ou
  documento exato. O Claude escreve, o usuário diz "sim", e só então sai das contas do próprio usuário.
  Um "sim" por mensagem. Nunca "sim pra todos".
- Pare no primeiro "não" ou em qualquer sinal de desinteresse. Um pedido pra parar vale pra sempre, em
  todas as skills.
- Dados pessoais seguem a LGPD: só dados profissionais públicos, usados pra esta venda, e apagados do
  contato se a pessoa pedir.
- Nunca invente um número, um resultado, um cliente ou um prazo. Preencha só o que é verdade e pergunte
  quando faltar algo.
