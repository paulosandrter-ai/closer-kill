# Closer Kill

Onze skills do Claude que tocam todo o seu comercial. Grátis, MIT, sem cadastro, sem chave de API, sem
licença de CRM. Feito pra agências e prestadores de serviço no Brasil: português, reais, WhatsApp, Pix e LGPD.

`record-keeper` `prospector` `follow-up` `sales-coach` `contract-writer` `researcher`
`scheduler` `pipeline` `proposal-writer` `win-back` `forecaster`

Uma registra cada e-mail, WhatsApp e call pra você. Outra acha leads novos e faz a primeira abordagem. Uma
faz follow-up até a call ser marcada. E a mais legal é o coach: ele escuta sua call de vendas e diz o que
falar em seguida. Quando o cliente fala "tá caro", a resposta certa já está na sua tela. Depois ele escreve
o contrato e manda.

Então, em vez de pagar CRM, ferramenta de lead, automação de e-mail e coach de call, você roda tudo dentro
do Claude, a partir de um arquivo no seu projeto.

Nada é enviado, marcado ou assinado sem o seu "sim". O Claude escreve, você aprova, e sai das suas
próprias contas.

## Instalar

Cole o link deste repositório no Claude e diga `instala essa skill`:

```
https://github.com/paulosandrter-ai/closer-kill

instala essa skill
```

Ou como plugin, no Claude Code:

```
/plugin marketplace add paulosandrter-ai/closer-kill
/plugin install closer-kill@closer-kill
```

O Claude Code coloca o nome do plugin na frente das skills, então instaladas como plugin elas aparecem como
`/closer-kill:prospector` e assim por diante. Copie as pastas se quiser só `/prospector`:

```bash
git clone https://github.com/paulosandrter-ai/closer-kill.git
cd closer-kill && cp -r record-keeper prospector follow-up sales-coach contract-writer researcher \
    scheduler pipeline proposal-writer win-back forecaster ~/.claude/skills/
```

Mantenha as onze juntas: todas usam o `pipeline/deals.py`. Sem Claude Code? Cole qualquer `SKILL.md` no
começo de uma conversa e ela funciona como um modo. Você perde as ferramentas em Python, mas o método
funciona. As ferramentas precisam de Python 3.8 ou mais novo. Nada pra instalar com pip.

Funciona melhor com os conectores do Gmail e do Google Agenda (e-mails e convites saem das suas contas) e
com o Claude in Chrome (o coach lê a legenda ao vivo do Google Meet). WhatsApp não tem conector: o Claude
escreve, você cola e envia do seu WhatsApp Business.

## As onze

| skill | função | o que faz |
| --- | --- | --- |
| `record-keeper` | Registro | Registra cada e-mail, WhatsApp e call: sincroniza a caixa de entrada com cada contato, salva as anotações das calls, mostra o histórico de qualquer pessoa. |
| `prospector` | Prospecção | Acha negócios locais em fontes públicas, confere no site a lacuna que você resolve (sem agendamento, ruim no celular, lento, sem WhatsApp, sem anúncios, sem avaliações) e escreve a primeira mensagem. |
| `follow-up` | Follow-up | Faz follow-up até a call ser marcada: um lembrete, algo útil, uma última mensagem. Para no primeiro não. |
| `sales-coach` | Coach de vendas | Escuta sua call pela legenda ao vivo e diz o que falar quando vem uma objeção. Revisa a call depois. |
| `contract-writer` | Contrato | Transforma o combinado num contrato de prestação de serviços em PDF, confere o valor com a call e envia com o seu sim. |
| `researcher` | Pesquisa | Lê o site do cliente antes da call e escreve um briefing de uma página com pontos pra puxar e perguntas. |
| `scheduler` | Agenda | Transforma "quinta às 14h pode ser" num convite com link do Meet, sem marcar por cima de nada. |
| `pipeline` | Funil (CRM) | Um quadro pra todos os negócios, de lead a ganho: o CRM, em `closer/pipeline.json`. |
| `proposal-writer` | Proposta | Transforma a call numa proposta com duas ou três opções claras, nas palavras do cliente. |
| `win-back` | Reconquista | Traz de volta os negócios que esfriaram, uma vez, na hora certa. |
| `forecaster` | Previsão | Diz quanto você vai fechar este mês: garantido, provável e melhor cenário, negócio por negócio. |

## Como usar

Tudo vai pra uma pasta `closer/` no seu projeto, e cada skill lê o que a anterior escreveu.

Um exemplo: uma agência pequena em Fortaleza que vende site com agendamento online e tráfego pago.

1. **`pipeline`** monta o quadro com a sua oferta: R$ 2.500, ou um plano mensal de R$ 399, e uma frase
   verdadeira sobre o retorno.
2. **`prospector`** acha 47 negócios locais sem agendamento online, ranqueia com o motivo e escreve a
   primeira mensagem pra Daniela Rocha da Clínica Sorriso Leve. Você diz sim. Sai segunda às 9:02.
3. **`follow-up`** manda um lembrete na quarta, uma prévia de 1 minuto na sexta e uma última mensagem na
   terça, cada uma com o seu sim. A Daniela responde às 11:48: "Desculpa, semana corrida! Quinta às 14h pode ser."
4. **`scheduler`** marca quinta, 29 de outubro, 14:00 na sua agenda com link do Meet.
5. **`researcher`** escreve o briefing da Clínica Sorriso Leve antes da call.
6. **`sales-coach`** lê a legenda. A Daniela fala: "Ficou lindo, mas sinceramente, tá caro pra gente
   agora." Na sua tela: "Faz sentido. A maioria das clínicas recupera o investimento com 2 pacientes novos
   por mês. Quer começar pelo plano mensal de R$ 399, sem taxa de implantação?"
7. **`contract-writer`** manda o contrato de R$ 399 por mês às 14:31, com o seu sim.
8. **`record-keeper`** registrou cada mensagem e a call. **`forecaster`** coloca no garantido de novembro.
   **`proposal-writer`** e **`win-back`** cuidam dos negócios que pediram orçamento ou esfriaram.

(A agência, a Daniela, a Clínica Sorriso Leve e todos os leads são fictícios.)

## As ferramentas

Tudo em Python só com a biblioteca padrão. As duas que leem sites leem só páginas públicas, se identificam
e vão devagar. Elas entendem português e inglês: "sim" e "não", "tá caro", "quinta às 14h", R$ e sites
brasileiros (Doctoralia, iFood, botão de WhatsApp, pixel da Meta).

```bash
python3 pipeline/deals.py board                                   # o quadro
python3 record-keeper/log.py sync --emails closer/inbox.json      # registra cada e-mail
python3 prospector/leads.py rank --csv closer/leads.csv           # leads ranqueados -> closer/leads.json
python3 follow-up/followup.py due                                 # quem precisa de follow-up hoje
python3 sales-coach/coach.py listen --captions closer/calls/live.txt --follow
python3 contract-writer/contract.py draft --help
python3 researcher/brief.py build --contact <id>
python3 scheduler/slots.py parse --text "quinta às 14h pode ser"
python3 proposal-writer/proposal.py draft --help
python3 win-back/winback.py list
python3 forecaster/forecast.py month
```

Teste qualquer uma no quadro de exemplo com `--file pipeline/pipeline.example.json`.
Os testes ficam ao lado de cada ferramenta:

```bash
for d in */; do python3 -m unittest discover -s "$d" -p "test_*.py"; done
```

## Letras miúdas

**Nada sai sem o seu sim.** Cada e-mail, WhatsApp, follow-up, convite, proposta e contrato é rascunho até
você aprovar aquele exato. Um "sim" por mensagem, nunca "sim pra todos". "Ok", "beleza" e "manda" não
contam. E-mail sai da sua caixa, convite da sua agenda, WhatsApp do seu número.

**Prospecção dentro da lei.** Toda primeira mensagem tem assunto real, seu nome e empresa reais, seu
endereço e um jeito simples de sair. A abordagem B2B se apoia no legítimo interesse da LGPD: só contatos
profissionais que o próprio negócio publicou, e os dados saem do quadro se a pessoa pedir. No máximo 50
primeiras mensagens por dia, e nunca disparo em massa no WhatsApp.

**Regras de parada.** No primeiro "não" para tudo, em todo lugar, pra sempre. Follow-ups param na hora que
a call é marcada, depois de 3 follow-ups ou 30 dias depois da primeira mensagem. Uma reconquista por
negócio. Quem pede pra sair vai pra uma lista de supressão que nenhuma skill usa.

**Calls.** Avise todo mundo na call que a legenda ou as anotações estão ligadas. O coach lê a legenda como
texto, não guarda áudio e só mostra os cartões pra você. Ele nunca fala na call.

**Nunca inventa nada.** Nada de fato inventado sobre um cliente, número, resultado, case, avaliação ou
prazo. As respostas e propostas são preenchidas com a sua oferta e com o que foi dito de verdade.

**Só informação pública do negócio.** O researcher e o prospector leem o site do negócio e fontes
públicas, nunca a vida pessoal de alguém e nada atrás de login.

**Não é orientação jurídica nem financeira.** Contratos e propostas são modelos: peça pra um advogado ler
seus termos padrão uma vez. Previsões são estimativas.

## Arquivos

```
pipeline/          SKILL.md, deals.py, pipeline.example.json
record-keeper/     SKILL.md, log.py
prospector/        SKILL.md, leads.py, openers.json, leads.example.csv
follow-up/         SKILL.md, followup.py, templates.json
sales-coach/       SKILL.md, coach.py, objections.json, call.example.txt
contract-writer/   SKILL.md, contract.py
researcher/        SKILL.md, brief.py
scheduler/         SKILL.md, slots.py
proposal-writer/   SKILL.md, proposal.py, options.example.json
win-back/          SKILL.md, winback.py
forecaster/        SKILL.md, forecast.py
*/test_*.py        testes unittest, offline
```

## Créditos

Adaptado do [Closer skill](https://github.com/Jakeschincariol/closer-skill) de Jake Schincariol (MIT).
Versão brasileira por Paulo / Vora Marketing & Digital. MIT.
