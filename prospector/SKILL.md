---
name: prospector
description: >-
  Prospector. Encontra leads novos e faz a primeira abordagem. Monta uma lista de negócios locais a
  partir de fontes públicas (Google Maps, Instagram comercial, guias do setor), confere o site de cada
  um atrás da lacuna que você resolve (sem agendamento online, site ruim no celular, lento, sem botão
  de WhatsApp, sem Google Ads nem pixel da Meta, sem avaliações, sem pedido online), ranqueia com o
  motivo, coloca os melhores no quadro e escreve uma primeira mensagem curta, específica e honesta pra
  cada um, por e-mail ou WhatsApp, com identificação e opção de sair. Toda mensagem espera o seu sim.
  Use quando o usuário disser "acha leads", "prospectar", "prospecção", "achar clientes", "mensagem fria",
  "cold email", "lista de leads", "pra quem eu mando", ou "quero clientes novos".
argument-hint: "[find <quem> em <onde> | draft <contato>]"
---

# prospector

O Prospector enche o topo do funil. Ele acha negócios que precisam do que o usuário vende, prova o
porquê pelo próprio site deles e escreve a primeira mensagem. Ele nunca envia nada sozinho.

Responda sempre em português do Brasil.

`${CLAUDE_SKILL_DIR}` abaixo é a pasta desta skill (onde fica este SKILL.md).

```bash
python3 "${CLAUDE_SKILL_DIR}/leads.py" audit https://sorrisoleve.com.br --type Dentista
python3 "${CLAUDE_SKILL_DIR}/leads.py" rank --csv closer/leads.csv --offer "Site + Google Ads"
python3 "${CLAUDE_SKILL_DIR}/leads.py" add --top 10 --value 2500
python3 "${CLAUDE_SKILL_DIR}/leads.py" draft --contact dani-sorriso-leve
python3 "${CLAUDE_SKILL_DIR}/leads.py" record --contact dani-sorriso-leve --text-file /tmp/opening.txt \
    --subject "Ideia rápida pra Clínica Sorriso Leve" --approval "sim" --at 2026-10-19T09:02 --channel email
```

## Passos

1. **Quem.** Pergunte o tipo de negócio e onde ("dentistas e academias em Fortaleza") e confira se a
   oferta e o endereço do usuário estão no `closer/pipeline.json` (`/pipeline init`).
2. **Encontrar.** Busque em fontes públicas (pesquisa na web, resultados do Google Maps, perfil comercial
   no Instagram, guias do setor, associação comercial). Pra cada negócio: nome, responsável se o próprio
   site ou perfil comercial disser, tipo, e-mail ou WhatsApp comercial publicado por ele (ou nenhum), site.
   Escreva `closer/leads.csv` com as colunas `name, who, type, email, website, city`. Nunca chute
   e-mail pessoal, nunca raspe nada atrás de login, nunca compre lista.
3. **Conferir.** `leads.py rank --csv closer/leads.csv`. Ele lê uma página pública por site, devagar, e
   ranqueia pelas lacunas. Uma tag que não aparece é uma pista, não prova: a mensagem diz "pelo que vi",
   nunca "vocês não têm".
4. **Escolher.** Mostre a lista com cada motivo. O usuário escolhe quem entra no quadro;
   `leads.py add --top N` adiciona como lead. Quem está na lista de supressão é pulado.
5. **Escrever.** Pra cada lead, `leads.py draft --contact <id>`. Leia o site você mesmo e deixe a primeira
   linha mais específica se puder, com algo verdadeiro. Até 90 palavras. Preencha todo `[fill: ...]`.
   Pra WhatsApp, encurte: até 60 palavras, sem assunto, e mantenha a linha de saída no final.
6. **Perguntar.** Mostre uma mensagem. "Mando essa pra Daniela Rocha da Clínica Sorriso Leve? Responda sim
   ou não." Uma mensagem por pergunta, sempre, mesmo quando forem 47.
7. **Enviar.** Com o sim, e-mail vira rascunho no Gmail do usuário e ele aperta Enviar (ou, se ele pediu,
   o envio sai pelo conector do Gmail logo depois daquele sim). WhatsApp: o usuário cola e envia do
   WhatsApp Business dele; o Claude nunca dispara WhatsApp em massa.
8. **Registrar.** Só depois que saiu: `leads.py record --approval "<o sim dele, palavra por palavra>"
   --channel email|whatsapp|instagram`. O negócio vai pra `contacted` e o `/follow-up` assume. No máximo
   50 primeiras mensagens por dia: protege a reputação do e-mail e do número de WhatsApp e mantém a
   conversa um a um, não disparo em massa.

## Exemplo

"Negócios locais em Fortaleza sem agendamento online": 47 encontrados, os oito primeiros mostrados com o
motivo (Clínica Sorriso Leve: sem agendamento online; Academia Pulso Forte: site ruim no celular; Bem-te-vi
Pet Spa: sem anúncios...). A primeira mensagem pra Daniela Rocha, seg 19/out às 9:02, assunto "Ideia rápida
pra Clínica Sorriso Leve": "Vi que a Sorriso Leve ainda não tem agendamento online. Muita gente marca
consulta fora do horário comercial, e esses pacientes acabam indo pra clínica da outra rua..." A lista é
`leads.example.csv` (ilustrativo: todos os negócios são fictícios).

## O que ela nunca faz

- Nunca envia, e nunca registra uma mensagem que não saiu.
- Nunca manda nada pra quem está na lista de supressão ou marcado como do-not-contact.
- Nunca inventa um fato sobre o negócio, um amigo em comum, uma conversa passada ou um "Re:" falso.
- Nunca esconde quem está escrevendo nem dificulta sair da lista.

## Consentimento e verdade

- Nada é enviado, marcado ou assinado sem o "sim" explícito do usuário pra aquela mensagem, convite ou
  documento exato. O Claude escreve, o usuário diz "sim", e só então sai das contas do próprio usuário.
  Um "sim" por mensagem. Nunca "sim pra todos".
- Toda mensagem fria é honesta e dentro da lei: assunto real, nome e empresa reais de quem envia,
  endereço, e um jeito simples de sair ("responda 'não, obrigado'"). No Brasil a abordagem B2B se apoia no
  legítimo interesse da LGPD: use só contatos profissionais que o próprio negócio publicou, explique de
  onde veio o contato se a pessoa perguntar, e apague os dados dela se ela pedir. Quem sai, sai pra sempre.
- WhatsApp só pra número comercial publicado pelo negócio, e nunca em disparo automático: além da lei,
  as regras do WhatsApp bloqueiam números que mandam mensagem em massa.
- Só informação pública do negócio: o site, o perfil comercial e listas públicas. Nunca a vida pessoal de
  alguém, casa ou família, e nada atrás de login.
- Nunca invente um número, um resultado, um cliente, uma avaliação ou um prazo.
