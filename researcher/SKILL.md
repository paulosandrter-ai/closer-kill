---
name: researcher
description: >-
  Researcher (pesquisa). Estuda cada cliente antes da call. Lê o site público do próprio negócio
  (início, sobre, serviços, equipe, contato), tira os fatos (como eles se descrevem, o que oferecem, desde
  quando existem, nota, telefone, redes sociais, quais ferramentas de agendamento, pedido online,
  WhatsApp, Google Ads e pixel da Meta eles usam e quais não) e escreve um briefing de uma página em
  closer/research/ com pontos pra puxar e perguntas pra fazer, cada fato com a fonte. Use quando o
  usuário disser "pesquisa o X", "me prepara pra call", "o que a gente sabe do X", "dá uma olhada nesse
  lead", "me dá um briefing", ou antes de qualquer call marcada.
argument-hint: "<contato>"
---

# researcher

Cinco minutos de leitura transformam uma call fria numa conversa. O Researcher lê o que o negócio diz
sobre si mesmo e dá pro usuário três coisas verdadeiras pra comentar e as perguntas certas pra fazer.

Responda sempre em português do Brasil.

`${CLAUDE_SKILL_DIR}` abaixo é a pasta desta skill (onde fica este SKILL.md).

```bash
python3 "${CLAUDE_SKILL_DIR}/brief.py" build --contact dani-sorriso-leve
python3 "${CLAUDE_SKILL_DIR}/brief.py" facts --url https://sorrisoleve.com.br
```

## Passos

1. `brief.py build --contact <id>`. Ele lê no máximo 4 páginas públicas do site do contato, uma de cada
   vez, e grava `closer/research/<id>.md`.
2. Leia o briefing. Depois, se for útil, olhe fontes públicas do negócio (o Perfil da Empresa no Google,
   o Instagram comercial, o Reclame Aqui, notícias locais) com uma pesquisa na web. Acrescente só fatos
   do negócio, cada um com o link.
3. Preencha as linhas `[Claude: ...]`: três pontos específicos e verdadeiros ("Vocês estão na Aldeota
   desde 2009", "As avaliações falam da demora pra conseguir falar no telefone"), e mais duas perguntas
   pra esse negócio.
4. Ligue isso à lacuna que o `/prospector` achou, como pergunta, não como acusação: "O que acontece quando
   alguém quer marcar às 21h?"
5. Mostre o briefing pronto pro usuário antes da call. O `/sales-coach` usa ele durante a call.

## O que entra no briefing

- **O negócio:** a descrição deles, desde quando existem, nota e quantidade de avaliações no site,
  telefone, redes sociais.
- **O que oferecem:** os títulos das páginas deles, nas palavras deles.
- **O que a gente notou:** ferramentas vistas no site e não vistas (agendamento online, pedido online,
  botão de WhatsApp, tag do Google Ads, pixel da Meta, chat). Não visto é pista, não prova: pergunte.
- **Pontos pra puxar** e **perguntas pra fazer.**
- **Fontes:** toda página usada.

## Exemplo

Antes da call de quinta com a Daniela Rocha, o briefing da Clínica Sorriso Leve: uma clínica odontológica
familiar em Fortaleza; o site lista os tratamentos e um telefone; nenhuma ferramenta de agendamento online
em nenhuma página (a lacuna que o Prospector achou); perguntas: "Hoje, como a maioria dos pacientes novos
chega até vocês?" e "O que acontece quando alguém quer marcar fora do horário?" (Ilustrativo: a Clínica
Sorriso Leve é fictícia.)

## O que ela nunca faz

- Nunca pesquisa a vida pessoal de alguém: nada de endereço de casa, família, perfil pessoal, idade,
  saúde ou qualquer coisa que a pessoa não publicou como parte do negócio.
- Nunca lê nada atrás de login ou paywall, e nunca mais de 4 páginas de um site por briefing.
- Nunca afirma um palpite como fato. "Não visto" continua "não visto".

## Consentimento e verdade

- Só informação pública do negócio na pesquisa: o site, o perfil comercial e listas públicas. Nunca a
  vida pessoal de alguém, casa ou família, e nada atrás de login. Isso também é o que a LGPD pede.
- Nada é enviado, marcado ou assinado sem o "sim" explícito do usuário pra aquela mensagem, convite ou
  documento exato. Esta skill só lê e escreve anotações.
- Nunca invente um número, um resultado, um cliente ou uma avaliação. Todo fato tem a fonte.
