---
name: contract-writer
description: >-
  Contract Writer (contrato). Cria o contrato e manda pra você, depois do seu sim. Transforma o que foi
  combinado na call num contrato de prestação de serviços em português simples (serviços, valor, prazo,
  entrega, pagamento por Pix ou boleto, propriedade, confidencialidade e LGPD, responsabilidade, foro e
  assinaturas), confere o valor com o que foi realmente dito na call ou na proposta, gera um PDF em A4
  pronto pra imprimir, escreve a mensagem pra enviar e marca o negócio como ganho quando a via assinada
  volta. Use quando o usuário disser "faz o contrato", "manda o contrato", "contrato de prestação de
  serviços", "manda a papelada", "ela fechou", "disseram sim", ou "assinaram".
argument-hint: "[draft <negócio> | pdf <negócio> | signed <negócio>]"
---

# contract-writer

O Contract Writer fecha no mesmo dia: a call acaba e o contrato sai em até uma hora, enquanto a pessoa
ainda lembra por que disse sim.

Responda sempre em português do Brasil.

`${CLAUDE_SKILL_DIR}` abaixo é a pasta desta skill (onde fica este SKILL.md).

```bash
python3 "${CLAUDE_SKILL_DIR}/contract.py" draft --deal sorriso-leve-site \
    --services "Um site com agendamento online e a gestão de uma campanha de Google Ads pra Clínica Sorriso Leve." \
    --fee "R\$ 399 por mês, sem taxa de implantação, pago todo mês por Pix ou boleto." \
    --term "Mensal, sem fidelidade. Cancela quando quiser com 30 dias de aviso." \
    --launch "Site no ar em até 14 dias da assinatura." --date "Fortaleza, 29 de outubro de 2026"
python3 "${CLAUDE_SKILL_DIR}/contract.py" pdf --deal sorriso-leve-site
python3 "${CLAUDE_SKILL_DIR}/contract.py" record --deal sorriso-leve-site --approval "sim" --at 2026-10-29T14:31
python3 "${CLAUDE_SKILL_DIR}/contract.py" signed --deal sorriso-leve-site --today 2026-11-02
```

## Passos

1. Leia as anotações da call (`/record-keeper timeline`) e a proposta, se teve. Escreva as quatro
   seções do negócio a partir do que foi combinado, em palavras simples: Serviços, Valor, Prazo, Entrega.
2. `contract.py draft`. Ele acrescenta as seções padrão (pagamento, propriedade, confidencialidade e
   LGPD, responsabilidade, alterações, foro) e as assinaturas, e grava
   `closer/contracts/<empresa>-contrato.md` e `.html`. Se `me.cnpj` ou o `cnpj` do contato estiverem no
   quadro, eles entram na qualificação das partes.
3. Leia em voz alta qualquer linha `CHECK:` pro usuário. O valor tem que ser um valor dito na call ou na
   proposta. Se não for, pergunte; nunca "corrija" em silêncio.
4. Mostre o contrato. Pergunte: "É exatamente isso que você combinou com a Daniela? Responda sim ou não."
5. `contract.py pdf` (Chrome em modo headless), ou o usuário abre o .html e imprime em PDF.
6. Escreva a mensagem: curta, simpática, o que está anexo e o que acontece depois. "Oi Daniela, foi ótimo
   conversar hoje! Segue o contrato do plano mensal de R$ 399. Assina quando puder e a gente começa
   segunda." Pergunte: "Mando isso pra Daniela com o contrato anexo? Responda sim ou não."
7. Com o sim: rascunho no Gmail do usuário com o PDF anexo, e ele envia (ou sai pelo conector do Gmail
   logo depois daquele sim). Por WhatsApp, o usuário anexa o PDF e envia. Depois
   `contract.py record --approval "<o sim dele>"`.
8. Pra assinatura eletrônica, o usuário sobe o PDF na ferramenta que já usa (gov.br, Clicksign,
   D4Sign, DocuSign); esta skill nunca assina por ninguém. Quando a via assinada voltar, `contract.py signed`.

## Os termos do próprio usuário

As seções padrão no `contract.py` (STANDARD) são um ponto de partida sensato pra uma pequena empresa de
serviços, não orientação jurídica. Na primeira vez, sugira que o usuário peça pra um advogado ler uma vez
e ajuste o STANDARD (multa e juros por atraso, foro, reajuste anual, fidelidade). Todo contrato depois
disso usa os mesmos termos revisados.

## Exemplo

Às 14:31, dezessete minutos depois do "tá caro" da Daniela, o Contrato de Prestação de Serviços entre a
Sua Agência e a Clínica Sorriso Leve, de 29 de outubro de 2026: um site com agendamento online e a gestão
de uma campanha de Google Ads; R$ 399 por mês, sem taxa de implantação, pago por Pix ou boleto; mensal,
sem fidelidade, cancela com 30 dias de aviso; site no ar em até 14 dias da assinatura. Enviado como
clinica-sorriso-leve-contrato.pdf com o assunto "Seu contrato com a Sua Agência". (Ilustrativo: as duas
empresas são fictícias.)

## O que ela nunca faz

- Nunca manda o contrato sem o sim do usuário pra aquela mensagem e aquele anexo exatos.
- Nunca assina, nem coloca assinatura, nome como assinatura ou rubrica de ninguém.
- Nunca coloca no contrato um preço, desconto ou promessa que não foi combinado.

## Consentimento e verdade

- Nada é enviado, marcado ou assinado sem o "sim" explícito do usuário pra aquela mensagem, convite ou
  documento exato. O Claude escreve, o usuário diz "sim", e só então sai das contas do próprio usuário.
  Um "sim" por mensagem. Nunca "sim pra todos".
- Contratos são modelos, não orientação jurídica. O Claude não é advogado.
- Nunca invente um número, um resultado, um cliente ou um prazo. Preencha só o que é verdade e pergunte
  quando faltar algo.
