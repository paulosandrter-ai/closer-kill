---
name: proposal-writer
description: >-
  Proposal Writer (proposta). Transforma a call numa proposta com preço no mesmo dia. Usa as palavras do
  próprio cliente nas anotações da call e nas respostas, mostra o que você vai fazer, dá duas ou três
  opções com preço claro (um projeto fechado, um plano mensal) e o total do primeiro ano, diz numa frase
  verdadeira o retorno que o serviço dá, recomenda uma e termina com um único próximo passo. Escreve a
  mensagem; ela sai com o seu sim. Use quando o usuário disser "faz uma proposta", "manda os valores",
  "monta um orçamento", "pediram preço", "manda as opções", ou depois de uma boa call.
argument-hint: "<negócio>"
---

# proposal-writer

Uma proposta que chega na mesma tarde, com as palavras do cliente, um preço claro e uma opção
recomendada, é assinada. Uma que chega semana que vem com cinco opções, não.

Responda sempre em português do Brasil.

`${CLAUDE_SKILL_DIR}` abaixo é a pasta desta skill (onde fica este SKILL.md).

```bash
python3 "${CLAUDE_SKILL_DIR}/proposal.py" draft --deal bemtevi-anuncios \
    --options "${CLAUDE_SKILL_DIR}/options.example.json" --today 2026-10-29
python3 "${CLAUDE_SKILL_DIR}/proposal.py" record --deal bemtevi-anuncios --approval "sim" --at 2026-10-29T16:00
```

## Passos

1. Leia o histórico do negócio (`/record-keeper timeline`) e as anotações da call em `closer/calls/`.
2. Escreva o arquivo de opções: de 1 a 3 opções, cada uma `{"name", "setup", "monthly", "includes",
   "recommended"}`. `setup` é a taxa de implantação, `monthly` a mensalidade, em reais. Os preços vêm do
   usuário, nunca de você. Recomende no máximo uma.
3. `proposal.py draft`. Ele grava `closer/proposals/<empresa>.md` com as palavras deles, uma tabela de
   opções com o total do primeiro ano, a frase de retorno do `me.value_line`, um próximo passo e a
   validade de 14 dias.
4. Preencha todo `[Claude: ...]`: "O que a gente vai fazer" em 3 a 5 linhas simples, com datas. Use as
   palavras deles pro problema deles. O `record` recusa enquanto sobrar qualquer marcador.
5. Mostre. Pergunte: "Mando essa proposta pra Priscila? Responda sim ou não."
6. Com o sim: rascunho no Gmail do usuário com a proposta (no corpo, ou anexa em PDF), e ele envia (ou sai
   pelo conector do Gmail logo depois daquele sim). Se a conversa está no WhatsApp, o usuário manda o PDF
   por lá. Depois `proposal.py record --approval "<o sim dele>"`.
7. Quando escolherem uma opção, `/contract-writer`.

## Exemplo

A Priscila Santos do Bem-te-vi Pet Spa respondeu no WhatsApp: "Talvez! Pode me mandar os valores?" A
proposta abre com essa frase e mostra duas opções do `options.example.json`: Projeto completo, R$ 2.500 de
implantação, R$ 2.500 no primeiro ano; Plano mensal (recomendado), R$ 399/mês, R$ 4.788 no primeiro ano,
sem taxa de implantação, cancela quando quiser. Fecha com "Me responde com a opção que você quer e eu te
mando o contrato no mesmo dia." (Ilustrativo: o Bem-te-vi Pet Spa é fictício.)

## O que ela nunca faz

- Nunca inventa um preço, um desconto, um resultado ou um case de cliente.
- Nunca envia sem o sim do usuário pra aquela proposta exata.
- Nunca dá mais de 3 opções nem esconde uma taxa.

## Consentimento e verdade

- Nada é enviado, marcado ou assinado sem o "sim" explícito do usuário pra aquela mensagem, convite ou
  documento exato. O Claude escreve, o usuário diz "sim", e só então sai das contas do próprio usuário.
  Um "sim" por mensagem. Nunca "sim pra todos".
- Propostas são modelos, não orientação jurídica ou financeira.
- Nunca invente um número, um resultado, um cliente, uma avaliação ou um prazo. Preencha só o que é
  verdade e pergunte quando faltar algo.
