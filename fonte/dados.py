#!/usr/bin/env python3
"""Fonte única das quantidades da cotação BOM003 · Bombril Carnaval 2027.

Base de lojas: briefing Bombril (tabela "Verba e cobertura", slide 11).
Regra enxuta: cada peça vai só para o tipo de PDV que precisa dela, sem sobra.
Usado por fonte/telas_qtd.py (telas de quantidade) e fonte/planilha.py (planilha de resposta).
"""

REGIONAIS = ['SPC', 'SPI', 'RJ', 'MG/CO', 'NO', 'NE', 'SUL']

# universos do briefing, por regional
UNIVERSO = {
    'direto': {'nome': 'Lojas do canal direto', 'curto': 'Canal direto',
               'por': [342, 231, 158, 357, 215, 146, 457]},
    'ponta':  {'nome': 'PDVs com ponta de gôndola', 'curto': 'Com ponta',
               'por': [638, 298, 538, 525, 240, 113, 643]},
    'ilha':   {'nome': 'PDVs com ilha (ponto extra)', 'curto': 'Com ilha',
               'por': [1913, 730, 521, 1313, 571, 1195, 1293]},
    # praças prioritárias: São Paulo (SPC), Rio (RJ), Salvador e Olinda (NE)
    'praca':  {'nome': 'Praças prioritárias', 'curto': 'Praças',
               'por': [1, 0, 1, 0, 0, 2, 0]},
    # demonstradoras: 8, uma por regional (MG e CO são duas)
    'demo':   {'nome': 'Demonstradoras', 'curto': 'Demonstradoras',
               'por': [1, 1, 1, 2, 1, 1, 1]},
}
for u in UNIVERSO.values():
    u['total'] = sum(u['por'])

# kits por tipo de PDV: (código, peça, quantidade por PDV)
KITS = [
    {'id': 'direto', 'nome': 'Kit linear', 'onde': 'Lojas do canal direto',
     'porque': 'A equipe própria instala, abastece o display e coloca as gargaleiras.',
     'itens': [('P01', 'Faixa de gôndola em L', 6), ('P02', 'Gargaleira', 15),
               ('P03', 'Wobbler', 2), ('P06', 'Display de chão', 1)]},
    {'id': 'ponta', 'nome': 'Kit ponta', 'onde': 'PDVs com ponta de gôndola',
     'porque': 'A ponta já sai com as 9 faixas das 3 prateleiras.',
     'itens': [('P04', 'Ponta de gôndola retrátil', 1), ('P01', 'Faixa de gôndola em L', 9)]},
    {'id': 'ilha', 'nome': 'Kit ponto extra', 'onde': 'PDVs com ilha (ponto extra)',
     'porque': 'Uma forração no pallet da base, que é o que o shopper vê.',
     'itens': [('P05', 'Forração de ponto extra', 1)]},
    {'id': 'praca', 'nome': 'Kit praça', 'onde': 'Praças prioritárias',
     'porque': 'Uma ilha cenográfica por praça, já com a comunicação da praça, e um motoboy.',
     'itens': [('P07', 'Ilha cenográfica', 1), ('P08 a P11', 'Comunicação regional da ilha', 1),
               ('P14 a P17', 'Kit motoboy', 1)]},
]

# itens da cotação: (código, peça, regra [(universo, qtd por PDV)], unidade, observação)
ITENS = [
    ('P01', 'Faixa de gôndola em L', [('direto', 6), ('ponta', 9)], 'un', '6 no linear + 9 dentro de cada ponta'),
    ('P02', 'Gargaleira', [('direto', 15)], 'un', 'frente do display: 5 frentes × 3 prateleiras'),
    ('P03', 'Wobbler', [('direto', 2)], 'un', '1 na lã de aço e 1 no Limpol'),
    ('P04', 'Ponta de gôndola retrátil', [('ponta', 1)], 'kit', 'kit com 11 componentes + 9 faixas P01 (contadas no P01)'),
    ('P05', 'Forração de ponto extra', [('ilha', 1)], 'kit', 'kit de 4 painéis, 1 por ilha'),
    ('P06', 'Display de chão', [('direto', 1)], 'kit', 'abastece 75 Limpol 500 ml'),
    ('P07', 'Ilha cenográfica (estrutura)', [('praca', 1)], 'kit', '12 displays, 4 testeiras, 2 portais, adesivo de chão'),
    ('P08 a P11', 'Comunicação regional da ilha', [('praca', 1)], 'kit', '1 por praça: Salvador, São Paulo/Vai-Vai, Rio, Olinda'),
    ('P12', 'Abadá das demonstradoras', [('demo', 2)], 'un', '2 por demonstradora (troca para lavar)'),
    ('P13', 'Camiseta do time Bombril', [], 'un', 'nacional, 1 entrega; informar também o preço para 800'),
    ('P14', 'Colete do motoboy com fitilhos', [('praca', 1)], 'un', '1 motoboy por praça'),
    ('P15', 'Aplique de plumas para capacete', [('praca', 1)], 'un', 'sem furar nem colar no casco'),
    ('P16', 'Capa de bag com fitilhos', [('praca', 1)], 'un', 'sobre a bag do motoboy'),
    ('P17', 'Pirulito da bag', [('praca', 1)], 'un', 'estandarte com haste, preso na bag'),
]
CAMISETAS = 1000  # briefing, tabela "Nacional · Camisetas"


def por_regional(regra):
    v = [0] * len(REGIONAIS)
    for uni, q in regra:
        for i, n in enumerate(UNIVERSO[uni]['por']):
            v[i] += n * q
    return v


def linhas():
    out = []
    for cod, nome, regra, un, obs in ITENS:
        v = por_regional(regra) if regra else [0] * len(REGIONAIS)
        tot = sum(v) if regra else CAMISETAS
        porpdv = ' + '.join(f"{q} × {UNIVERSO[u]['total']:,}".replace(',', '.') for u, q in regra) if regra else 'nacional'
        out.append({'cod': cod, 'nome': nome, 'un': un, 'obs': obs, 'regional': v, 'total': tot, 'conta': porpdv})
    return out


def br(n):
    return f'{n:,}'.replace(',', '.')


if __name__ == '__main__':
    for k, u in UNIVERSO.items():
        print(k, u['total'])
    for l in linhas():
        print(f"{l['cod']:10} {l['nome']:34} {br(l['total']):>8}  {l['conta']}  {l['regional']}")
    for k in KITS:
        print(k['nome'], sum(q for _, _, q in k['itens']), 'peças por PDV')


# ===== especificação final para cotação (material mais barato que cumpre a função) =====
# cada componente: (peça, qtd por kit, medida em cm, material e acabamento)
SPEC = {
    'P01': [('Faixa de gôndola em L', '1', 'frente 32,0 × 4,9 + aba 5 (planificado 32,0 × 9,9)',
             'PS 0,5 mm branco, impressão digital UV 4×0, vinco na dobra, corte reto')],
    'P02': [('Gargaleira', '1', '5,6 × 15,6, furo Ø 4,4, vinco abaixo do furo',
             'Cartão triplex 300 g, offset 4×0, verniz de máquina, faca especial')],
    'P03': [('Disco', '1', '14,2 × 14,1', 'PS 0,5 mm branco, digital UV 4×0, faca no contorno da arte'),
            ('Haste com aba', '1', '2,5 × 13 + aba 2,5 × 3', 'PVC cristal 0,3 mm, dupla-face na aba')],
    'P04': [('Canto em L superior (esq. e dir.)', '2', 'lateral 55,9 × 64,2 + frente 55,9 × 19,6; raio 1,2',
             'Papelão ondulado BC, couché 4×0 laminado, vinco múltiplo na dobra curva'),
            ('Canto em L inferior (esq. e dir.)', '2', 'lateral 55,9 × 64,2 + frente 55,9 × 19,6; raio 1,2',
             'Papelão ondulado BC, couché 4×0 laminado, vinco múltiplo na dobra curva'),
            ('Régua de coluna (esq. e dir.)', '2', '45 × 80', 'Papelão ondulado BC kraft, sem impressão (fica por dentro)'),
            ('Aplique lateral direito (campanha)', '1', '50 × 86,9 (faca)', 'PS 0,5 mm, digital UV 4×0, dupla-face'),
            ('Aplique lateral esquerdo (compre e ganhe)', '1', '50 × 86,9 (faca)', 'PS 0,5 mm, digital UV 4×0, dupla-face'),
            ('Testeira com plumas', '1', '110,8 × 61,7', 'Papelão ondulado BC, couché 4×0 laminado, faca no contorno das plumas'),
            ('Logo em relevo', '1', '59,5 × 33,6, afastado 1 da testeira', 'PS 1 mm, digital UV 4×0, espaçador de papelão'),
            ('Aplique da base inferior', '1', '105,6 × 21,1', 'PS 0,5 mm, digital UV 4×0'),
            ('Faixa de gôndola em L (P01)', '9', '3 por prateleira', 'Ver P01 (quantidade somada no P01)')],
    'P05': [('Painel frente e fundo', '2', '125 × 50 (face de 120 + aba de emenda de 5)',
             'Microondulado onda E, couché 4×0 laminado, BOPP brilho, vinco na aba'),
            ('Painel lateral', '2', '105 × 50 (face de 100 + aba de emenda de 5)', 'Microondulado onda E, couché 4×0 laminado, BOPP brilho, vinco na aba'),
            ('Fita dupla-face', '4', 'tiras de 50', 'Fecho das 4 quinas, vai no kit')],
    'P06': [('Lateral', '2', 'perfil 53 × 126, topo inclinado, canto arredondado',
             'Papelão ondulado BC, couché 4×0 laminado por fora, capa branca por dentro'),
            ('Costas', '1', '63,6 × 140', 'Papelão ondulado BC, couché 4×0 laminado'),
            ('Cabeçote com plumas', '1', '70,3 × 45,6, sobrepõe 7 nas costas', 'Papelão ondulado BC, couché 4×0 laminado, faca nas plumas'),
            ('Aplique do logo', '1', '45,6 × 25,8, afastado 1 do cabeçote', 'PS 1 mm, digital UV 4×0'),
            ('Prateleira em bandeja', '3', 'piso 62,8 × 40, abas de 4 em U na frente e no fundo',
             'Papelão ondulado BC capa branca, carga de 15 kg sem flecha visível'),
            ('Faixa frontal da prateleira', '3', '63,6 × 10,5, logo recortado acima da borda', 'Microondulado onda E, couché 4×0 laminado'),
            ('Frente inclinada da base', '1', '63,6 × 36,8', 'Papelão ondulado BC, couché 4×0 laminado'),
            ('Rodapé', '1', '66 × 55,8 × 5,3', 'Polionda 4 mm amarela em massa (resiste ao pano de chão)'),
            ('Pé redondo', '4', 'Ø 5,2 × 1,5', 'Plástico preto')],
    'P07': [('Display de base reta', '12', '63,6 × 41,4 × 157,5', 'Papelão ondulado BC, impressão digital UV direta'),
            ('Fitilhos da base', '12 conj.', '63,6 de largura, caindo sobre a base', 'Fitilho metalizado amarelo e vermelho'),
            ('Portal', '2', '312,6 × 291,3 × 6; colunas de 81,6; passagem 149,4 × 208,9',
             'Metalon 20 × 20 pintado + polionda 4 mm impressa UV nos 2 lados; sapata sem furar o piso'),
            ('Logo iluminado da testeira', '4', '107 × 60,5', 'PS 2 mm, digital UV, fita LED 12 V atrás (luz rebatida)'),
            ('Logo iluminado do portal', '4', '109 × 61,7 (frente e verso)', 'PS 2 mm, digital UV, fita LED 12 V atrás (luz rebatida)'),
            ('Fita de LED do portal', '2 conj.', '12,7 m por portal (contorno externo e interno)', 'Fita LED 12 V em perfil com difusor, fonte bivolt e cabo até a tomada'),
            ('Adesivo de chão', '1', 'Ø 480, em gomos de até 130 de largura', 'Vinil impresso + laminação antiderrapante')],
    'P08 a P11': [('Testeira de grupo com plumas', '4', '199,5 × 111, topo a 244,9 do chão', 'Polionda 4 mm, digital UV, recorte das plumas'),
                  ('Aplique de plumas do portal', '4', '161,9 × 132,4 (frente e verso), topo a 324,9', 'Polionda 4 mm, digital UV, recorte')],
    'P12': [('Abadá das demonstradoras', '16', 'grade P a GG', 'Malha 100% poliéster (dry), sublimação total, 4 artes regionais')],
    'P13': [('Camiseta do time Bombril', '1.000', 'grade P a GG', 'Malha 100% algodão fio 30.1 cardado amarela, silk 3 cores só na frente')],
    'P14': [('Colete com fitilhos', '1', 'tamanho único ajustável', 'Oxford sublimado com fitilhos metalizados costurados na barra')],
    'P15': [('Aplique de plumas', '1', 'sobre capacete padrão', 'Plumas sintéticas em base de EVA com elástico; sem furar nem colar no casco')],
    'P16': [('Capa de bag com fitilhos', '1', 'pela bag do motoboy', 'Oxford sublimado com elástico + fitilhos metalizados')],
    'P17': [('Pirulito da bag', '1', 'estandarte com franja', 'Tecido sublimado + haste de PVC presa na bag')],
}

# o que mudou do caderno original para a versão de cotação: (peça, antes, depois, por quê, tipo)
# tipo: 'custo' (barateia) ou 'acerto' (deixa a informação redonda)
DE_PARA = [
    ('P04', 'Logo com fita de LED em cada ponta', 'Logo em relevo, sem LED',
     'A ponta de gôndola não tem tomada: seriam 2.995 fontes ou baterias para instalar e trocar.', 'custo'),
    ('P04 · P06', 'Polionda 4 mm na estrutura', 'Papelão ondulado BC com impressão offset laminada',
     'Campanha de 4 semanas. Mesmo visual, material bem mais barato. O rodapé segue em polionda por causa do pano de chão.', 'custo'),
    ('P03 · P04 · P06', 'PETG impresso e PETG cristal', 'PS 0,5 a 1 mm e PVC cristal 0,3 mm na haste',
     'PS faz o mesmo papel por uma fração do preço; PVC cristal é a haste padrão de wobbler.', 'custo'),
    ('P04', 'Borda transparente nas plumas', 'Faca no contorno das plumas',
     'Sem chapa cristal e sem branco de base na impressão, igual ao wobbler.', 'custo'),
    ('P04', '3 apliques laterais, 1 de troca', '2 apliques: o esquerdo já sai com o compre e ganhe',
     'Menos 2.995 peças e nenhuma visita de troca.', 'custo'),
    ('P01', 'PS 1 mm', 'PS 0,5 mm', 'Peça pequena e apoiada na prateleira: metade do material e vinco mais limpo.', 'custo'),
    ('P03', 'Disco em PS 1 mm', 'Disco em PS 0,5 mm', 'O disco de 14 cm fica leve e balança melhor na haste.', 'custo'),
    ('P06', 'Amarelo por dentro das laterais', 'Capa branca por dentro, sem impressão', 'Imprimir as duas faces dobra o custo de impressão. Amarelo por dentro entra como opcional.', 'custo'),
    ('P01', 'Dois tamanhos: 39,0 × 4,9 e 38,2 × 4,8', 'Um só: 32,0 × 4,9 + aba 5',
     'Cabem 3 na ponta mais estreita (104) e 3 num módulo de 100 cm. Uma faca e uma tiragem só.', 'acerto'),
    ('P05', 'Faixa contínua de 432 × 50', '4 painéis: 2 de 125 × 50 e 2 de 105 × 50',
     'O pallet PBR 120 × 100 pede 440 de volta, não 432. Em painéis, cabe na folha de impressão e viaja plano.', 'acerto'),
    ('P06', 'Costas + testeira numa peça de 178,6', 'Costas de 140 + cabeçote encaixado',
     'Cada parte cabe na folha de offset; o cabeçote é o padrão de display de papelão.', 'acerto'),
    ('P02 · P05 · P13', 'Duas opções de material ("cartão ou PS")', 'Uma especificação por peça',
     'Todos os fornecedores cotam a mesma coisa e os preços ficam comparáveis.', 'acerto'),
    ('P07 · P08 a P11', 'Ilha nacional + kits regionais por cima', 'Estrutura única + só as peças que trocam',
     'Testeiras e plumas já saem com a arte da praça: nenhuma testeira nacional é jogada fora.', 'acerto'),
    ('P14 · P17', 'Colete com fitilhos e colete com pirulito', 'Um colete; o pirulito vai na bag',
     'O briefing pede mochila pirulito: um colete por motoboy basta.', 'acerto'),
    ('Todas', 'Quantidade "conforme plano"', 'Quantidade por PDV e total fechado',
     'Calculado com a base de lojas do briefing, sem sobra.', 'acerto'),
]
