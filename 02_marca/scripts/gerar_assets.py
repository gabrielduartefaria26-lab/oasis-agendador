import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from brand import *

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "Castelo_Polimeros_Kit")
for d in ["logo", "instagram/posts", "instagram/destaques", "instagram/perfil"]:
    os.makedirs(os.path.join(OUT, d), exist_ok=True)
P = lambda *a: os.path.join(OUT, *a)
only = sys.argv[1:]  # opcional: renderizar só alguns itens

def want(k):
    return not only or k in only

# ---------------- LOGOS ----------------
if want("logo"):
    for nome, svg in [("simbolo.svg", simbolo()), ("simbolo-branco.svg", simbolo(BRANCO, AMBAR)),
                      ("logo-horizontal.svg", logo_svg()), ("logo-horizontal-branco.svg", logo_svg(BRANCO, BRANCO, AMBAR))]:
        open(P("logo", nome), "w").write(svg)
    render(f'<div style="padding:40px">{logo_html(escala=2)}</div>', P("logo", "logo-horizontal.png"), 760, 230, True)
    render(f'<div style="padding:40px">{logo_html(BRANCO, BRANCO, AMBAR, 2)}</div>', P("logo", "logo-horizontal-branco.png"), 760, 230, True)
    render(f'<div style="padding:40px">{simbolo(size=432)}</div>', P("logo", "simbolo.png"), 512, 512, True)

# ---------------- PERFIL ----------------
if want("perfil"):
    render(f'<div style="width:1080px;height:1080px;background:{AZUL};display:grid;place-items:center">'
           f'{simbolo(BRANCO, AMBAR, 600)}</div>', P("instagram", "perfil", "foto-perfil.png"), 1080, 1080)

# ---------------- POSTS (1080x1350) ----------------
CSS = f"""
<style>
.post{{width:1080px;height:1350px;position:relative;overflow:hidden;font-family:Barlow,Arial,sans-serif}}
.navy{{background:{AZUL};color:{BRANCO}}} .conc{{background:{CONCRETO};color:{GRAFITE}}} .amb{{background:{AMBAR};color:{AZUL_ESC}}}
.pad{{position:absolute;inset:88px 88px 170px}}
.eb{{font:600 30px 'IBM Plex Mono',monospace;letter-spacing:2px;text-transform:uppercase}}
.navy .eb{{color:{AMBAR}}} .conc .eb{{color:{AZUL}}} .amb .eb{{color:{AZUL}}}
.h{{font:800 132px/0.9 'Barlow Condensed',sans-serif;text-transform:uppercase;letter-spacing:1px;margin:36px 0 0}}
.h2{{font:800 104px/0.92 'Barlow Condensed',sans-serif;text-transform:uppercase;margin:30px 0 0}}
.p{{font:500 40px/1.35 Barlow,sans-serif;margin-top:40px;max-width:860px}}
.mono{{font-family:'IBM Plex Mono',monospace}}
.foot{{position:absolute;left:88px;right:88px;bottom:62px;display:flex;justify-content:space-between;align-items:center}}
.handle{{font:600 28px 'IBM Plex Mono',monospace;opacity:.8}}
.faixa{{position:absolute;left:0;right:0;height:34px;background:{FAIXA_CSS}}}
.hl{{color:{AMBAR}}} .conc .hl, .amb .hl{{color:{AZUL}}}
</style>"""

def foot(tema):
    if tema == "navy":
        lg = logo_html(BRANCO, BRANCO, AMBAR, 1.0)
    elif tema == "amb":
        lg = logo_html(AZUL_ESC, AZUL_ESC, BRANCO, 1.0)
    else:
        lg = logo_html(AZUL, AZUL, AMBAR, 1.0)
    return f'<div class="foot">{lg}<div class="handle">{HANDLE}</div></div>'

def post(tema, corpo, n, faixa="top"):
    fx = '<div class="faixa" style="top:0"></div>' if faixa == "top" else ('<div class="faixa" style="bottom:0;height:22px"></div>' if faixa == "bottom" else "")
    html = f'{CSS}<div class="post {tema}">{fx}<div class="pad">{corpo}</div>{foot(tema)}</div>'
    render(html, P("instagram", "posts", f"post-{n:02d}.png"), 1080, 1350)

def strip(cor, w=300, h=26, curva=False):
    return f'<div style="width:{w}px;height:{h}px;background:{cor};border-radius:3px"></div>'

posts = {}
posts[1] = ("navy", f"""
<div class="eb">Boituva-SP · Castello Branco</div>
<div class="h">Sua apara<br>de fita vira<br><span class="hl" style="white-space:nowrap">matéria-prima.</span></div>
<div class="p">Chegou a Castelo Polímeros: moagem de fita de arquear, ráfia e plástico flexível para a indústria da região.</div>
<div style="position:absolute;right:-30px;bottom:-60px;opacity:.16">{simbolo(BRANCO, AMBAR, 420)}</div>""")

def item(cor_a, cor_b, titulo, sub):
    return (f'<div style="display:flex;gap:40px;align-items:center;padding:30px 0;border-top:3px solid {AZUL}22">'
            f'<div style="width:150px;display:grid;gap:10px">{strip(cor_a,150,20)}{strip(cor_b,150,20)}{strip(cor_a,150,20)}</div>'
            f'<div><div style="font:800 64px/1 \'Barlow Condensed\';text-transform:uppercase;color:{AZUL}">{titulo}</div>'
            f'<div style="font:500 32px Barlow;margin-top:6px">{sub}</div></div></div>')
posts[2] = ("conc", f"""
<div class="eb">O que a gente mói</div>
<div class="h2" style="color:{AZUL}">Especialistas em<br>material flexível</div>
<div style="margin-top:46px">
{item(AMBAR, AZUL, "Fita de arquear", "PP e PET, em lotes separados")}
{item("#C9B48A", "#A8946A", "Ráfia e big bag", "Sacaria e tecido de PP")}
{item("#CFE3F0", "#9DBBD0", "Filme stretch", "Stretch, shrink e sacos de PE")}
{item(VERDE, "#5FA483", "Fio de PP", "Multifilamento e borra de fiação")}
</div>""")

posts[3] = ("amb", f"""
<div class="eb">Capacidade</div>
<div style="font:700 300px/0.85 'Barlow Condensed';margin-top:40px;letter-spacing:-4px">4 t<span style="font-size:120px;letter-spacing:0">/dia</span></div>
<div style="display:grid;gap:26px;margin-top:70px">
 <div style="display:flex;justify-content:space-between;border-top:4px solid {AZUL_ESC};padding-top:22px"><span class="mono" style="font-size:36px">GRANULOMETRIA</span><b style="font:800 60px 'Barlow Condensed'">ATÉ 2 MM</b></div>
 <div style="display:flex;justify-content:space-between;border-top:4px solid {AZUL_ESC};padding-top:22px"><span class="mono" style="font-size:36px">RESINAS</span><b style="font:800 60px 'Barlow Condensed'">PP · PE · PET</b></div>
 <div style="display:flex;justify-content:space-between;border-top:4px solid {AZUL_ESC};padding-top:22px"><span class="mono" style="font-size:36px">ENTREGA</span><b style="font:800 60px 'Barlow Condensed'">BIG BAG POR LOTE</b></div>
</div>""", "none")

def passo(n, t, d):
    return (f'<div style="display:flex;gap:36px;align-items:flex-start;padding:26px 0;border-top:2px solid #ffffff30">'
            f'<div style="font:700 92px/0.8 \'Barlow Condensed\';color:{AMBAR};width:70px">{n}</div>'
            f'<div><div style="font:800 58px/1 \'Barlow Condensed\';text-transform:uppercase">{t}</div>'
            f'<div style="font:500 32px/1.3 Barlow;opacity:.88;margin-top:8px">{d}</div></div></div>')
posts[4] = ("navy", f"""
<div class="eb">Como funciona</div>
<div class="h2">Do fardo<br>ao big bag</div>
<div style="margin-top:40px">
{passo(1,"Avaliação","Você conta o material, o volume e a granulometria.")}
{passo(2,"Lote-piloto","Moemos um teste para você aprovar a qualidade.")}
{passo(3,"Programação","Entrada e saída agendadas, com pesagem nas duas pontas.")}
{passo(4,"Entrega","Moído em big bag identificado, com nota de retorno.")}
</div>""")

agua = f"""
<div style="position:relative;height:430px;margin-top:50px;border-radius:10px;overflow:hidden;background:#fff">
 <div style="position:absolute;left:0;right:0;top:140px;bottom:0;background:linear-gradient(#BFDCEC,#8FBFD8)"></div>
 <div style="position:absolute;left:0;right:0;top:136px;height:8px;background:#7FB2CF"></div>
 <div style="position:absolute;left:120px;top:96px;width:290px;height:46px;background:#2B2B2B;border-radius:4px"></div>
 <div style="position:absolute;left:120px;top:20px;font:800 54px 'Barlow Condensed';color:{AZUL}">PP · BOIA</div>
 <div style="position:absolute;right:120px;bottom:30px;width:290px;height:46px;background:{VERDE};border-radius:4px"></div>
 <div style="position:absolute;right:120px;bottom:96px;font:800 54px 'Barlow Condensed';color:{AZUL_ESC}">PET · AFUNDA</div>
</div>"""
posts[5] = ("conc", f"""
<div class="eb">Dica de chão de fábrica</div>
<div class="h2" style="color:{AZUL}">Fita PP ou PET?<br>Faça o teste da água</div>
{agua}
<div class="p" style="font-size:36px">O PP é mais leve que a água (densidade ~0,9) e boia. O PET é mais pesado (~1,38) e afunda. A fita PET também costuma ser verde e mais rígida.</div>""")

posts[6] = ("navy", f"""
<div class="eb">Por que separar resinas</div>
<div class="h2">Misturou,<br><span class="hl">perdeu valor.</span></div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:36px;margin-top:70px">
 <div style="border:3px solid {AMBAR};padding:36px;border-radius:8px"><div class="mono" style="font-size:30px;color:{AMBAR}">PP derrete a</div><div style="font:700 112px/1 'Barlow Condensed';white-space:nowrap">~165 °C</div></div>
 <div style="border:3px solid #ffffff60;padding:36px;border-radius:8px"><div class="mono" style="font-size:30px;opacity:.8">PET derrete a</div><div style="font:700 112px/1 'Barlow Condensed';white-space:nowrap">~250 °C</div></div>
</div>
<div class="p">Na extrusora, o PET não derrete junto com o PP e vira impureza. Por isso cada resina e cada cliente tem o seu big bag.</div>""")

def lista(titulo, itens, cor, sim):
    lis = "".join(f'<div style="display:flex;gap:22px;align-items:center;font:600 42px Barlow;padding:14px 0">'
                  f'<span style="width:52px;height:52px;border-radius:50%;background:{cor};color:#fff;display:grid;place-items:center;font:800 34px Barlow">{sim}</span>{i}</div>' for i in itens)
    return f'<div><div style="font:800 60px \'Barlow Condensed\';text-transform:uppercase;color:{AZUL};margin-bottom:10px">{titulo}</div>{lis}</div>'
posts[7] = ("conc", f"""
<div class="eb">Antes de mandar seu material</div>
<div class="h2" style="color:{AZUL}">O que entra<br>no picador</div>
<div style="display:grid;gap:50px;margin-top:56px">
{lista("Aceitamos", ["Fita de arquear PP e PET", "Ráfia, sacaria e big bag", "Filme stretch e shrink (PE)", "Fio e borra de fiação PP"], VERDE, "✓")}
{lista("Não aceitamos", ["PVC", "Fita adesiva com cola", "Material sujo ou misturado"], "#B23B3B", "✕")}
</div>""")

cidades = [("Cerquilho", 15), ("Tietê", 25), ("Porto Feliz", 25), ("Tatuí", 30), ("Sorocaba", 45), ("Itu", 50),
           ("Salto", 55), ("Indaiatuba", 70), ("Monte Mor", 80), ("Piracicaba", 85), ("Campinas", 95)]
bars = "".join(f'<div style="display:grid;grid-template-columns:230px 1fr 110px;align-items:center;gap:20px;padding:9px 0">'
               f'<span style="font:700 38px \'Barlow Condensed\';text-transform:uppercase">{c}</span>'
               f'<span style="height:22px;width:{km/100*100:.0f}%;background:{AMBAR};border-radius:2px"></span>'
               f'<span class="mono" style="font-size:28px;text-align:right">{km} km</span></div>' for c, km in cidades)
posts[8] = ("navy", f"""
<div class="eb">Região atendida</div>
<div class="h2">No meio do<br>caminho da indústria</div>
<div style="margin-top:44px">{bars}</div>
<div class="mono" style="font-size:24px;opacity:.7;margin-top:14px">Distância aproximada por estrada a partir de Boituva</div>""")

posts[9] = ("amb", f"""
<div class="eb">Para começar</div>
<div class="h" style="font-size:150px">Teste antes<br>de fechar.</div>
<div style="margin-top:60px;background:{AZUL_ESC};color:#fff;border-radius:10px;padding:46px 50px">
 <div class="mono" style="font-size:30px;color:{AMBAR}">LOTE-PILOTO</div>
 <div style="font:800 96px/1 'Barlow Condensed';margin-top:10px">ATÉ 500 KG</div>
 <div style="font:500 36px/1.35 Barlow;margin-top:16px;opacity:.9">Moemos um lote do seu material para você aprovar a qualidade.</div>
</div>
<div style="font:800 64px 'Barlow Condensed';margin-top:56px;text-transform:uppercase">Orçamento no WhatsApp → link na bio</div>""", "none")

if want("posts"):
    for n, v in posts.items():
        tema, corpo = v[0], v[1]
        post(tema, corpo, n, v[2] if len(v) > 2 else "top")

# ---------------- DESTAQUES (1080x1920) ----------------
ICONES = {
    "servicos": simbolo(AMBAR, BRANCO, 380),
    "materiais": '<div style="display:grid;gap:34px">' + "".join(strip(c, 420, 52) for c in [AMBAR, BRANCO, AMBAR, BRANCO]) + "</div>",
    "processo": f'<svg width="420" height="420" viewBox="0 0 24 24" fill="none" stroke="{AMBAR}" stroke-width="2.2" stroke-linecap="square"><path d="M3 7h13M12 3l4 4-4 4"/><path d="M21 17H8M12 13l-4 4 4 4"/></svg>',
    "regiao": f'<svg width="380" height="380" viewBox="0 0 24 24"><path fill="{AMBAR}" d="M12 2a7 7 0 0 0-7 7c0 5 7 13 7 13s7-8 7-13a7 7 0 0 0-7-7zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5z"/></svg>',
    "contato": f'<svg width="400" height="400" viewBox="0 0 24 24"><path fill="{AMBAR}" d="M4 3h16a2 2 0 0 1 2 2v11a2 2 0 0 1-2 2H9l-5 4v-4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2z"/><rect x="7" y="8" width="10" height="1.8" fill="{AZUL}"/><rect x="7" y="11.5" width="6" height="1.8" fill="{AZUL}"/></svg>',
}
if want("destaques"):
    for k, ic in ICONES.items():
        render(f'<div style="width:1080px;height:1920px;background:{AZUL};display:grid;place-items:center">{ic}</div>',
               P("instagram", "destaques", f"destaque-{k}.png"), 1080, 1920)
print("ok")
