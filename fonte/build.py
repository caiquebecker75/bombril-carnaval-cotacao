#!/usr/bin/env python3
# Monta index.html e assets/deck.css e deck.js a partir de src/ e de fonte/dados.py. Rodar da raiz: python3 fonte/build.py
import pathlib, time, re, sys, html as H
R = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(R / 'fonte'))
import dados as D
S = R / 'src'
v = time.strftime('%Y%m%d%H%M%S')
br = D.br
LIN = {l['cod']: l for l in D.linhas()}


def spec(cod):
    rows = []
    for k, (peca, q, med, mat) in enumerate(D.SPEC[cod], 1):
        ref = ' class="ref"' if mat.startswith('Ver P01') else ''
        rows.append(f'<tr{ref}><td>{k:02d}</td><td class="p">{H.escape(peca)}</td><td class="q">{q}</td><td>{H.escape(med)}</td><td>{H.escape(mat)}</td></tr>')
    return ('<table class="ficha"><thead><tr><th>#</th><th>Peça</th><th>Qtd.</th><th>Medida (cm)</th><th>Material e acabamento</th></tr></thead><tbody>'
            + ''.join(rows) + '</tbody></table>')


def qtd(cod):
    l = LIN[cod]
    regra = next(r for c, n, r, u, o in D.ITENS if c == cod)
    cel = []
    for uni, q in regra:
        u = D.UNIVERSO[uni]
        cel.append(f'<div><span>{u["curto"]}</span><b>{q} × {br(u["total"])}</b><i>{q} por PDV · {br(u["total"])} PDVs</i></div>')
    un = 'kits' if l['un'] == 'kit' else 'unidades'
    cel.append(f'<div><span>Total a produzir</span><b data-conta="{l["total"]}">{br(l["total"])}</b><i>{un}</i></div>')
    return '<div class="qtd">' + ''.join(cel) + '</div>'


def kits():
    out = []
    for k in D.KITS:
        u = D.UNIVERSO[k['id']]
        n = sum(q for _, _, q in k['itens'])
        itens = ''.join(f'<li><b>{q}</b><span><em>{c}</em>{H.escape(nm)}</span></li>' for c, nm, q in k['itens'])
        out.append(f'<div class="kit k-{k["id"]}"><div class="kit-cab"><span>{H.escape(k["onde"])}</span><b data-conta="{u["total"]}">{br(u["total"])}</b></div>'
                   f'<h3>{H.escape(k["nome"])}</h3><ul>{itens}</ul>'
                   f'<div class="kit-tot"><span>Total no PDV</span><b>{n}</b><i>{"peça" if n == 1 else "peças"}</i></div>'
                   f'<p>{H.escape(k["porque"])}</p></div>')
    return ''.join(out)


def totais():
    rows = []
    for l in D.linhas():
        rows.append(f'<tr><td>{l["cod"]}</td><td class="p">{H.escape(l["nome"])}</td><td class="c">{l["conta"]}</td>'
                    f'<td class="t">{br(l["total"])}</td><td class="o">{H.escape(l["obs"])}</td></tr>')
    t1 = ('<table class="tot"><thead><tr><th>Cód.</th><th>Peça</th><th>Conta (por PDV × PDVs)</th><th>Total</th><th>Observação</th></tr></thead><tbody>'
          + ''.join(rows) + '</tbody></table>')
    cab = ''.join(f'<th>{r}</th>' for r in D.REGIONAIS)
    rows2 = []
    for l in D.linhas():
        if not any(l['regional']):
            cel = f'<td colspan="{len(D.REGIONAIS)}" class="nac">entrega nacional única</td>'
        else:
            cel = ''.join(f'<td>{br(x) if x else "·"}</td>' for x in l['regional'])
        rows2.append(f'<tr><td>{l["cod"]}</td><td class="p">{H.escape(l["nome"])}</td>{cel}<td class="t">{br(l["total"])}</td></tr>')
    t2 = (f'<table class="tot reg"><thead><tr><th>Cód.</th><th>Peça</th>{cab}<th>Total</th></tr></thead><tbody>'
          + ''.join(rows2) + '</tbody></table>')
    return t1, t2


def regional(uni):
    u = D.UNIVERSO[uni]
    mx = max(u['por'])
    bars = ''.join(f'<div class="rb"><b>{br(n)}</b><i style="--h:{n / mx * 100:.1f}%"></i><span>{r}</span></div>' for r, n in zip(D.REGIONAIS, u['por']))
    return f'<div class="regbar">{bars}</div>'


def depara(tipo):
    out = []
    for pc, antes, depois, pq, t in D.DE_PARA:
        if t != tipo:
            continue
        out.append(f'<div class="dp"><span class="dp-pc">{pc}</span><s>{H.escape(antes)}</s><svg class="dp-s"><use href="#i-seta"/></svg>'
                   f'<b>{H.escape(depois)}</b><p>{H.escape(pq)}</p></div>')
    return ''.join(out)


telas = ''.join((S / f).read_text() for f in sorted(p.name for p in S.glob('s[0-9]*.html')))
t1, t2 = totais()
def unif():
    rows = []
    for cod in ['P12', 'P13', 'P14', 'P15', 'P16', 'P17']:
        peca, q, med, mat = D.SPEC[cod][0]
        rows.append(f'<tr><td>{cod}</td><td class="p">{H.escape(peca)}</td><td class="q">{br(LIN[cod]["total"])}</td><td>{H.escape(LIN[cod]["obs"])}</td><td>{H.escape(med)}</td><td>{H.escape(mat)}</td></tr>')
    return ('<table class="ficha"><thead><tr><th>Cód.</th><th>Peça</th><th>Total</th><th>Regra</th><th>Medida</th><th>Material e acabamento</th></tr></thead><tbody>'
            + ''.join(rows) + '</tbody></table>')


telas = telas.replace('<!--UNIF-->', unif())
telas = telas.replace('<!--TOTAIS-->', t1).replace('<!--REGIONAIS-->', t2).replace('<!--KITS-->', kits())
telas = re.sub(r'<!--SPEC:([^>]+?)-->', lambda m: spec(m.group(1)), telas)
telas = re.sub(r'<!--QTD:([^>]+?)-->', lambda m: qtd(m.group(1)), telas)
telas = re.sub(r'<!--REG:(\w+)-->', lambda m: regional(m.group(1)), telas)
telas = re.sub(r'<!--DEPARA:(\w+)-->', lambda m: depara(m.group(1)), telas)
telas = re.sub(r'<!--N:(\w+)-->', lambda m: br(D.UNIVERSO[m.group(1)]['total']), telas)
telas = re.sub(r'<!--T:([^>]+?)-->', lambda m: br(LIN[m.group(1)]['total']), telas)
(R / 'versao.txt').write_text(v + '\n')
shell = (S / 'shell.html').read_text()
html = shell.replace('__TELAS__', telas).replace('__VERSAO__', v)
(R / 'index.html').write_text(html)
(R / 'assets').mkdir(exist_ok=True)
css = ''.join((S / f).read_text() for f in ['base.css', 'tema.css', 'telas.css', 'celular.css'] if (S / f).exists())
(R / 'assets/deck.css').write_text(css)
(R / 'assets/deck.js').write_text((S / 'deck.js').read_text())
tudo = html + css + (R / 'assets/deck.js').read_text()
bad = [x for x in ('—', '–') if x in tudo]
n = html.count('<section class="tela')
rot = html.count('<aside class="roteiro"')
print('telas', n, '· roteiros', rot, '· versão', v, '· TRAVESSÃO!' if bad else '· sem travessão')
for m in re.finditer(r'(?:a definir|lorem|TBD|XXX|\[__|<!--[A-Z]+:)', html, re.I):
    print('TEXTO PROVISÓRIO:', html[max(0, m.start() - 40):m.end() + 40].replace('\n', ' '))
