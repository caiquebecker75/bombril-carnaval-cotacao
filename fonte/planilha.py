#!/usr/bin/env python3
"""Gera assets/BOM003-planilha-cotacao.xlsx a partir de fonte/dados.py (mesmos números do deck).
Rodar da raiz: python3 fonte/planilha.py"""
import pathlib, sys
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

R = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(R / 'fonte'))
import dados as D

AM = PatternFill('solid', fgColor='FFD200')
VM = PatternFill('solid', fgColor='E30613')
PR = PatternFill('solid', fgColor='17110D')
ED = PatternFill('solid', fgColor='FFF7CC')
fino = Side(style='thin', color='C9C2B0')
B = Border(left=fino, right=fino, top=fino, bottom=fino)
H = Font(bold=True, color='FFD200', name='Arial', size=10)
N = Font(name='Arial', size=10)
NB = Font(name='Arial', size=10, bold=True)
WR = Alignment(wrap_text=True, vertical='top')
BRL = 'R$ #,##0.00'
INT = '#,##0'


def cabec(ws, linha, cols):
    for i, c in enumerate(cols, 1):
        cel = ws.cell(linha, i, c)
        cel.font = H; cel.fill = PR; cel.alignment = Alignment(wrap_text=True, vertical='center'); cel.border = B


def titulo(ws, txt, sub):
    ws['A1'] = txt; ws['A1'].font = Font(name='Arial', size=15, bold=True, color='E30613')
    ws['A2'] = sub; ws['A2'].font = Font(name='Arial', size=10, italic=True)


wb = Workbook()

# ---- aba 1: cotação
ws = wb.active; ws.title = 'Cotação'
titulo(ws, 'BOM003 · Bombril Carnaval 2027 · Planilha de cotação · 75 LAB',
       'Preencha só as células amarelas. Preço com impostos destacados. Medidas e materiais: aba Especificação.')
ws['A3'] = 'Fornecedor:'; ws['C3'].fill = ED
ws['E3'] = 'CNPJ:'; ws['F3'].fill = ED
ws['A4'] = 'Validade da proposta (dias):'; ws['C4'].fill = ED
ws['E4'] = 'Condição de pagamento:'; ws['F4'].fill = ED
for c in ('A3', 'E3', 'A4', 'E4'):
    ws[c].font = NB
cols = ['Cód.', 'Peça', 'Unid.', 'Qtd. total', 'Qtd. por loja × lojas/PDVs', 'Preço unitário c/ impostos (R$)', 'Total (R$)',
        'ICMS %', 'IPI %', 'Prazo de produção (dias úteis)', 'Preço unitário do lote extra de 5% (R$)', 'Alternativa mais barata (opcional)', 'Observações']
L0 = 6
cabec(ws, L0, cols)
lin = D.linhas()
for k, l in enumerate(lin):
    r = L0 + 1 + k
    vals = [l['cod'], l['nome'], l['un'], l['total'], l['porloja_txt'] + ' × ' + l['pdvs'] + (' · ' + l['obs'] if l['obs'] else ''), None, f'=D{r}*F{r}', None, None, None, None, None, None]
    for i, v in enumerate(vals, 1):
        c = ws.cell(r, i, v); c.font = N; c.border = B; c.alignment = WR
    ws.cell(r, 4).number_format = INT
    for col in (6, 8, 9, 10, 11, 12, 13):
        ws.cell(r, col).fill = ED
    ws.cell(r, 6).number_format = BRL; ws.cell(r, 7).number_format = BRL; ws.cell(r, 11).number_format = BRL
    ws.cell(r, 1).font = Font(name='Arial', size=10, bold=True, color='E30613')
rT = L0 + 1 + len(lin)
ws.cell(rT, 2, 'TOTAL DA PROPOSTA').font = NB
ws.cell(rT, 7, f'=SUM(G{L0+1}:G{rT-1})').number_format = BRL
ws.cell(rT, 7).font = NB; ws.cell(rT, 7).fill = AM
r13 = next(L0 + 1 + k for k, l in enumerate(lin) if l['cod'] == 'P13')
ws.cell(rT + 2, 2, 'P13 com 800 camisetas: preço unitário (R$)').font = NB
ws.cell(rT + 2, 6).fill = ED; ws.cell(rT + 2, 6).number_format = BRL
for i, w in enumerate([10, 34, 7, 11, 46, 16, 16, 8, 8, 14, 18, 30, 30], 1):
    ws.column_dimensions[get_column_letter(i)].width = w
ws.row_dimensions[L0].height = 44
ws.freeze_panes = f'C{L0+1}'

# ---- aba 2: entrega por regional
w2 = wb.create_sheet('Entrega por regional')
titulo(w2, 'Quantidades por regional (para o frete opcional)', 'Base de lojas do briefing Bombril. Preencha o frete por regional na última linha, se cotar entrega descentralizada.')
cabec(w2, 4, ['Cód.', 'Peça'] + D.REGIONAIS + ['Total'])
for k, l in enumerate(lin):
    r = 5 + k
    w2.cell(r, 1, l['cod']).font = Font(name='Arial', size=10, bold=True, color='E30613')
    w2.cell(r, 2, l['nome']).font = N
    if any(l['regional']):
        for i, x in enumerate(l['regional']):
            w2.cell(r, 3 + i, x).number_format = INT
        w2.cell(r, 3 + len(D.REGIONAIS), f'=SUM(C{r}:{get_column_letter(2+len(D.REGIONAIS))}{r})').number_format = INT
    else:
        w2.cell(r, 3, 'entrega nacional única (Grande São Paulo)').font = Font(name='Arial', size=10, italic=True)
        w2.cell(r, 3 + len(D.REGIONAIS), l['total']).number_format = INT
    for i in range(1, 4 + len(D.REGIONAIS)):
        w2.cell(r, i).border = B
rf = 6 + len(lin)
w2.cell(rf, 2, 'Frete por regional (R$), opcional').font = NB
for i in range(len(D.REGIONAIS)):
    c = w2.cell(rf, 3 + i); c.fill = ED; c.number_format = BRL; c.border = B
w2.cell(rf, 3 + len(D.REGIONAIS), f'=SUM(C{rf}:{get_column_letter(2+len(D.REGIONAIS))}{rf})').number_format = BRL
w2.column_dimensions['A'].width = 10; w2.column_dimensions['B'].width = 34
for i in range(len(D.REGIONAIS) + 1):
    w2.column_dimensions[get_column_letter(3 + i)].width = 11

# ---- aba 3: especificação
w3 = wb.create_sheet('Especificação')
titulo(w3, 'Especificação de cada peça (cotar esta versão)', 'Medidas em cm, tolerância ± 0,5, confirmar em prova física. Encaixes e fixações: proposta do fornecedor, sem ferramenta na loja.')
cabec(w3, 4, ['Cód.', '#', 'Componente', 'Qtd. por kit', 'Medida (cm)', 'Material e acabamento'])
r = 5
for cod, comps in D.SPEC.items():
    for k, (peca, q, med, mat) in enumerate(comps, 1):
        for i, v in enumerate([cod, k, peca, q, med, mat], 1):
            c = w3.cell(r, i, v); c.font = N; c.border = B; c.alignment = WR
        w3.cell(r, 1).font = Font(name='Arial', size=10, bold=True, color='E30613')
        r += 1
for i, w in enumerate([10, 5, 38, 12, 46, 70], 1):
    w3.column_dimensions[get_column_letter(i)].width = w

# ---- aba 4: ajustes
w4 = wb.create_sheet('Ajustes')
titulo(w4, 'O que mudou do caderno original para esta versão', 'Revisão 75 LAB: material mais barato que cumpre a função e informações fechadas.')
cabec(w4, 4, ['Peça', 'Antes', 'Agora', 'Por quê', 'Tipo'])
for k, (pc, a, d, pq, t) in enumerate(D.DE_PARA):
    for i, v in enumerate([pc, a, d, pq, 'barateia' if t == 'custo' else 'fecha a conta'], 1):
        c = w4.cell(5 + k, i, v); c.font = N; c.border = B; c.alignment = WR
for i, w in enumerate([16, 34, 40, 70, 14], 1):
    w4.column_dimensions[get_column_letter(i)].width = w

out = R / 'assets' / 'BOM003-planilha-cotacao.xlsx'
wb.save(out)
print('ok', out.name, len(lin), 'itens')
