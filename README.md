# Bombril Carnaval 2027 · Caderno de cotação BOM003 · 75 LAB

Versão HTML do caderno técnico BOM003 para os fornecedores cotarem o MPDV do Carnaval 2027 da Bombril.

- Apresentação: https://projetos.75lab.com.br/bombril-carnaval-cotacao/
- PDF: `bombril-carnaval-2027-cotacao.pdf` (capa com link e QR, uma página por aba)
- Planilha de resposta: `assets/BOM003-planilha-cotacao.xlsx` (Cotação, Entrega por regional, Especificação, Ajustes)
- Fontes: `briefing/` (caderno original de 12 páginas e briefing da Bombril; fora do Git)

## O que a revisão mudou
- Material mais barato que cumpre a função: sem LED nas 2.995 pontas; papelão ondulado BC no lugar de polionda (P04, P06); PS e PVC cristal no lugar de PETG; faca no contorno no lugar de borda transparente; 2 apliques laterais na ponta em vez de 3.
- Informação redonda: faixa P01 com um tamanho só (32,0 × 4,9 + aba 5); forração em 4 painéis que fecham a volta do PBR (440, não 432); costas do display em 140 + cabeçote; uma especificação por peça; ilha com estrutura única e só testeiras e plumas por praça; quantidades fechadas.

## Quantidades (regra enxuta)
Base: tabela "Verba e cobertura" do briefing (1.906 lojas do canal direto, 2.995 PDVs com ponta, 7.536 PDVs com ilha) e 4 praças prioritárias.
Kit linear (canal direto): 6 faixas, 15 gargaleiras, 2 wobblers, 1 display = 24 peças. Kit ponta: 1 ponta + 9 faixas. Kit ponto extra: 1 forração. Kit praça: ilha + comunicação regional + motoboy.

## Como editar
- Números e especificações: só em `fonte/dados.py`. O build e a planilha leem dali.
- Telas em `src/sNN-*.html`; estilos em `src/base.css`, `src/tema.css`, `src/telas.css`, `src/celular.css`; motor em `src/deck.js`.
- Montar: `python3 fonte/build.py` e `python3 fonte/planilha.py`.
- Conferir (Playwright de `ariuno-videos`, base `file://…/index.html`): `node fonte/miniaturas.mjs`, `node fonte/sobreposicao.mjs`, `node fonte/celular.mjs`, `node fonte/abas.mjs`.
- PDF: `LINK=https://projetos.75lab.com.br/bombril-carnaval-cotacao/ PAGINA=index.html node fonte/gerar-pdf.mjs file:///…/bombril-carnaval-cotacao/ bombril-carnaval-2027-cotacao.pdf`.
- Teclas: setas navegam, M abre o sumário, N mostra o roteiro de fala.

## Pontos a confirmar com o Caique
- Camisetas: 1.000 pelo briefing; a reunião falou em 800 (a planilha pede os dois preços).
- Mapa dos códigos regionais: P08 Salvador, P09 São Paulo/Vai-Vai, P10 Rio, P11 Olinda.
