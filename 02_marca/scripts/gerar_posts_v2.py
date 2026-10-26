import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from brand import *

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "Castelo_Polimeros_Kit", "instagram")
FOTO = lambda n: "file://" + os.path.join(BASE, "fotos", n + "_raw.jpg")
NIGHT = "#071629"; STEEL = "#2C6E9E"; AMB_CLARO = "#FFC93C"; PAPER = "#F4F7FA"

CSS = f"""<style>
.post{{width:1080px;height:1350px;position:relative;overflow:hidden;font-family:Barlow,Arial,sans-serif;color:#EAF1F7}}
.dark{{background:radial-gradient(70% 55% at 100% 0%,rgba(44,110,158,.55),transparent 70%),radial-gradient(60% 45% at 0% 100%,rgba(242,169,0,.20),transparent 70%),linear-gradient(180deg,{NIGHT},{AZUL_ESC})}}
.light{{background:radial-gradient(70% 50% at 100% 0%,rgba(242,169,0,.16),transparent 70%),radial-gradient(60% 45% at 0% 100%,rgba(44,110,158,.14),transparent 70%),{PAPER};color:#0E1E2E}}
.photo-bg{{position:absolute;inset:0;background-size:cover;background-position:center}}
.shade{{position:absolute;inset:0}}
.pad{{position:absolute;inset:84px 84px 180px;display:flex;flex-direction:column}}
.pill{{align-self:flex-start;display:inline-flex;align-items:center;gap:12px;padding:12px 24px;border-radius:999px;background:rgba(242,169,0,.12);border:2px solid rgba(242,169,0,.4);color:{AMB_CLARO};font:600 26px 'IBM Plex Mono',monospace;letter-spacing:3px;text-transform:uppercase}}
.light .pill{{background:rgba(18,56,90,.07);border-color:rgba(18,56,90,.22);color:{AZUL}}}
.h{{font:800 124px/.92 'Barlow Condensed',sans-serif;text-transform:uppercase;margin-top:40px}}
.h2{{font:800 100px/.94 'Barlow Condensed',sans-serif;text-transform:uppercase;margin-top:36px}}
.g{{background:linear-gradient(100deg,#FFE08A 0%,{AMB_CLARO} 35%,{AMBAR} 100%);-webkit-background-clip:text;background-clip:text;color:transparent}}
.light .g{{background:linear-gradient(100deg,{AZUL},{STEEL});-webkit-background-clip:text;background-clip:text}}
.p{{font:500 38px/1.4 Barlow,sans-serif;color:#B4C4D4;margin-top:34px;max-width:860px}}
.light .p{{color:#4A5F72}}
.glass{{background:linear-gradient(180deg,rgba(255,255,255,.10),rgba(255,255,255,.04));border:2px solid rgba(255,255,255,.14);border-radius:30px;backdrop-filter:blur(18px);-webkit-backdrop-filter:blur(18px)}}
.light .glass{{background:#fff;border:2px solid #DCE5ED;box-shadow:0 30px 60px -30px rgba(18,56,90,.30)}}
.mono{{font-family:'IBM Plex Mono',monospace}}
.k{{font:600 24px 'IBM Plex Mono';letter-spacing:3px;text-transform:uppercase;color:#9FB3C6}}
.light .k{{color:#5B7084}}
.foot{{position:absolute;left:84px;right:84px;bottom:56px;padding-top:30px;border-top:2px solid rgba(255,255,255,.12);display:flex;justify-content:space-between;align-items:center}}
.light .foot{{border-top-color:#DCE5ED}}
.handle{{font:600 28px 'IBM Plex Mono';color:#9FB3C6}}
.light .handle{{color:#5B7084}}
.tape{{position:absolute;left:0;right:0;top:0;height:14px;background:repeating-linear-gradient(-45deg,{AMBAR} 0 22px,{AZUL_ESC} 22px 34px)}}
.btn{{display:inline-flex;align-items:center;gap:16px;padding:28px 44px;border-radius:22px;background:linear-gradient(110deg,{AMB_CLARO},{AMBAR});color:#1A1200;font:700 40px Barlow;box-shadow:0 20px 50px -18px rgba(242,169,0,.7)}}
.icon{{width:96px;height:96px;border-radius:26px;display:grid;place-items:center;background:linear-gradient(135deg,rgba(242,169,0,.26),rgba(242,169,0,.06));border:2px solid rgba(242,169,0,.35);color:{AMB_CLARO}}}
.light .icon{{background:linear-gradient(135deg,rgba(18,56,90,.12),rgba(18,56,90,.03));border-color:rgba(18,56,90,.2);color:{AZUL}}}
</style>"""

def foot(light=False):
    lg = logo_html(AZUL, AZUL, AMBAR, 1.0) if light else logo_html(BRANCO, BRANCO, AMBAR, 1.0)
    return f'<div class="foot">{lg}<div class="handle">{HANDLE}</div></div>'

def post(n, cls, corpo, extra_bg="", light=False):
    html = f'{CSS}<div class="post {cls}">{extra_bg}<div class="tape"></div><div class="pad">{corpo}</div>{foot(light)}</div>'
    render(html, os.path.join(OUT, "posts", f"post-{n:02d}.png"), 1080, 1350)

def photo(nome, pos="center", shade="linear-gradient(180deg,rgba(7,22,41,.15) 0%,rgba(7,22,41,.55) 45%,rgba(7,22,41,.97) 78%)"):
    return f'<div class="photo-bg" style="background-image:url({FOTO(nome)});background-position:{pos}"></div><div class="shade" style="background:{shade}"></div>'

ICO = {
    "moagem": '<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M3 7h18M3 12h18"/><path d="M5 17h2M10 17h2M15 17h2M7.5 20.5h1M12.5 20.5h1"/></svg>',
}

# 01 · lançamento (foto da linha)
post(1, "dark", f"""
<div style="flex:1"></div>
<span class="pill">● Boituva-SP · Castello Branco</span>
<div class="h" style="font-size:118px">Sua apara de fita vira <span class="g" style="white-space:nowrap">matéria-prima.</span></div>
<div class="p" style="color:#C9D6E2">Chegou a Castelo Polímeros: moagem de fita de arquear, ráfia e plástico flexível para a indústria da região.</div>""",
     photo("hero", "30% center"))

# 02 · o que a gente mói
def mrow(c1, c2, t, s, tag):
    return (f'<div class="glass" style="display:grid;grid-template-columns:110px 1fr auto;gap:30px;align-items:center;padding:28px 34px">'
            f'<div style="display:grid;gap:9px"><i style="height:14px;border-radius:7px;background:{c1}"></i><i style="height:14px;border-radius:7px;background:{c2}"></i><i style="height:14px;border-radius:7px;background:{c1}"></i></div>'
            f'<div><div style="font:800 54px/1 \'Barlow Condensed\';text-transform:uppercase">{t}</div><div style="font:500 30px Barlow;color:#9FB3C6;margin-top:6px">{s}</div></div>'
            f'<div class="mono" style="font-size:24px;padding:10px 18px;border:2px solid rgba(255,255,255,.16);border-radius:999px;color:#9FB3C6">{tag}</div></div>')
post(2, "dark", f"""
<span class="pill">O que a gente mói</span>
<div class="h2">Especialistas em <span class="g">material flexível</span></div>
<div style="display:grid;gap:20px;margin-top:52px">
{mrow(AMBAR, STEEL, "Fita de arquear", "Lotes sempre separados", "PP · PET")}
{mrow("#D9C59A", "#A8946A", "Ráfia e big bag", "Sacaria e tecido", "PP")}
{mrow("#CFE3F0", "#8FB5D0", "Filme stretch", "Stretch, shrink e sacos", "PE")}
{mrow("#3FA27A", VERDE, "Fio de PP", "Borra de fiação", "PP")}
</div>""")

# 03 · capacidade (foto da mão)
def stat(v, k):
    return f'<div class="glass" style="padding:30px 32px"><div style="font:800 92px/1 \'Barlow Condensed\'">{v}</div><div style="font:500 28px Barlow;color:#B4C4D4;margin-top:8px">{k}</div></div>'
post(3, "dark", f"""
<span class="pill">Ficha técnica</span>
<div class="h2" style="margin-top:28px">Material que volta <span class="g">pronto para a extrusora</span></div>
<div style="flex:1"></div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:20px">
{stat("4 t", "por dia de capacidade")}{stat("2 mm", "granulometria mínima")}
{stat("3", "resinas: PP, PE e PET")}{stat("1 bag", "por lote e por cliente")}
</div>""", photo("hand", "center 60%", "linear-gradient(180deg,rgba(7,22,41,.96) 0%,rgba(7,22,41,.55) 38%,rgba(7,22,41,.35) 55%,rgba(7,22,41,.92) 100%)"))

# 04 · como funciona
def passo(n, t, d):
    return (f'<div class="glass" style="display:grid;grid-template-columns:92px 1fr;gap:30px;align-items:center;padding:28px 32px">'
            f'<div style="width:92px;height:92px;border-radius:24px;background:linear-gradient(110deg,{AMB_CLARO},{AMBAR});color:#1A1200;display:grid;place-items:center;font:800 50px \'Barlow Condensed\'">0{n}</div>'
            f'<div><div style="font:800 52px/1 \'Barlow Condensed\';text-transform:uppercase">{t}</div><div style="font:500 30px/1.3 Barlow;color:#9FB3C6;margin-top:8px">{d}</div></div></div>')
post(4, "dark", f"""
<span class="pill">Como funciona</span>
<div class="h2">Do fardo ao big bag, <span class="g">em 4 etapas</span></div>
<div style="display:grid;gap:18px;margin-top:48px">
{passo(1, "Avaliação", "Material, volume e granulometria.")}
{passo(2, "Lote-piloto", "Um teste para você aprovar.")}
{passo(3, "Programação", "Entrada e saída com pesagem.")}
{passo(4, "Entrega", "Big bag identificado + nota de retorno.")}
</div>""")

# 05 · teste da água (claro)
agua = f"""
<div class="glass" style="margin-top:50px;padding:0;overflow:hidden;position:relative;height:420px">
 <div style="position:absolute;left:0;right:0;top:150px;bottom:0;background:linear-gradient(180deg,#CFE6F4,#8DBFDD)"></div>
 <div style="position:absolute;left:0;right:0;top:146px;height:8px;background:#9CC8E2"></div>
 <div style="position:absolute;left:96px;top:104px;width:300px;height:48px;border-radius:10px;background:linear-gradient(180deg,#3a3a3a,#141414);box-shadow:0 10px 20px -8px rgba(0,0,0,.4)"></div>
 <div style="position:absolute;left:96px;top:36px;font:800 52px 'Barlow Condensed';color:{AZUL}">PP · BOIA</div>
 <div style="position:absolute;right:96px;bottom:34px;width:300px;height:48px;border-radius:10px;background:linear-gradient(180deg,#45B387,{VERDE})"></div>
 <div style="position:absolute;right:96px;bottom:100px;font:800 52px 'Barlow Condensed';color:{AZUL_ESC}">PET · AFUNDA</div>
</div>"""
post(5, "light", f"""
<span class="pill">Dica de chão de fábrica</span>
<div class="h2" style="color:#0E1E2E">Fita PP ou PET? <span class="g">Faça o teste da água</span></div>
{agua}
<div class="p" style="font-size:34px">O PP é mais leve que a água (densidade ~0,9) e boia. O PET (~1,38) afunda. A fita PET também costuma ser verde e mais rígida.</div>""", light=True)

# 06 · não misturar
def temp(res, t, dest):
    borda = f"border-image:none;border:2px solid rgba(242,169,0,.5)" if dest else ""
    return (f'<div class="glass" style="padding:36px;{borda}"><div class="k">{res} derrete a</div>'
            f'<div style="font:800 128px/1 \'Barlow Condensed\';margin-top:10px;white-space:nowrap" class="{"g" if dest else ""}">~{t} °C</div></div>')
post(6, "dark", f"""
<span class="pill">Por que separar resinas</span>
<div class="h">Misturou, <span class="g">perdeu valor.</span></div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:22px;margin-top:60px">{temp("PP", 165, True)}{temp("PET", 250, False)}</div>
<div class="p">Na extrusora, o PET não derrete junto com o PP e vira impureza. Por isso cada resina e cada cliente têm o seu big bag.</div>""")

# 07 · aceitamos (claro)
def item(t, ok):
    cor = VERDE if ok else "#C93542"; bg = "#E3F2EB" if ok else "#FDE8EA"
    return (f'<div style="display:flex;gap:22px;align-items:center;font:600 38px Barlow;padding:12px 0">'
            f'<span style="width:54px;height:54px;border-radius:16px;background:{bg};color:{cor};display:grid;place-items:center;font:800 32px Barlow">{"✓" if ok else "✕"}</span>{t}</div>')
post(7, "light", f"""
<span class="pill">Antes de mandar seu material</span>
<div class="h2" style="color:#0E1E2E">O que entra <span class="g">no picador</span></div>
<div class="glass" style="margin-top:46px;padding:34px 40px;border:3px solid transparent;background:linear-gradient(#fff,#fff) padding-box,linear-gradient(120deg,{AMB_CLARO},{AMBAR},{AZUL}) border-box">
<div class="k" style="margin-bottom:8px">Aceitamos</div>
{item("Fita de arquear PP e PET", True)}{item("Ráfia, sacaria e big bag", True)}{item("Filme stretch e shrink (PE)", True)}{item("Fio e borra de fiação PP", True)}
</div>
<div class="glass" style="margin-top:22px;padding:30px 40px">
<div class="k" style="margin-bottom:8px">Não aceitamos</div>
{item("PVC · fita adesiva com cola", False)}{item("Material sujo ou misturado", False)}
</div>""", light=True)

# 08 · região
cid = [("Cerquilho", 15), ("Tietê", 25), ("Porto Feliz", 25), ("Tatuí", 30), ("Sorocaba", 45), ("Itu", 50), ("Salto", 55),
       ("Indaiatuba", 70), ("Monte Mor", 80), ("Piracicaba", 85), ("Campinas", 95)]
bars = "".join(f'<div style="display:grid;grid-template-columns:220px 1fr 110px;gap:22px;align-items:center;padding:7px 0">'
               f'<span style="font:700 36px \'Barlow Condensed\';text-transform:uppercase">{c}</span>'
               f'<span style="height:16px;border-radius:9px;width:{km}%;background:linear-gradient(90deg,{AMB_CLARO},{AMBAR})"></span>'
               f'<span class="mono" style="font-size:26px;text-align:right;color:#9FB3C6">{km} km</span></div>' for c, km in cid)
post(8, "dark", f"""
<span class="pill">Região atendida</span>
<div class="h2">No meio do caminho <span class="g">da indústria</span></div>
<div class="glass" style="margin-top:46px;padding:30px 40px">{bars}
<div class="mono" style="font-size:22px;color:#9FB3C6;margin-top:12px">Distância aproximada por estrada a partir de Boituva</div></div>""")

# 09 · CTA (foto dos fardos)
post(9, "dark", f"""
<span class="pill">Para começar</span>
<div class="h" style="font-size:140px">Teste antes <span class="g">de fechar.</span></div>
<div style="flex:1"></div>
<div class="glass" style="padding:44px 46px;background:linear-gradient(180deg,rgba(11,34,56,.78),rgba(11,34,56,.6))">
 <div class="k" style="color:{AMB_CLARO}">Lote-piloto</div>
 <div style="font:800 100px/1 'Barlow Condensed';margin-top:8px">ATÉ 500 KG</div>
 <div style="font:500 34px/1.35 Barlow;color:#C9D6E2;margin-top:14px">Moemos um lote do seu material para você aprovar a qualidade antes de qualquer contrato.</div>
 <div style="margin-top:34px"><span class="btn">Orçamento no WhatsApp ↗</span></div>
</div>""", photo("bales", "center", "linear-gradient(180deg,rgba(7,22,41,.92) 0%,rgba(7,22,41,.25) 32%,rgba(7,22,41,.15) 48%,rgba(7,22,41,.85) 78%)"))

# foto de perfil e destaques com o mesmo acabamento
GLOW = (f"radial-gradient(60% 60% at 80% 10%,rgba(44,110,158,.6),transparent 70%),"
        f"radial-gradient(60% 60% at 10% 100%,rgba(242,169,0,.22),transparent 70%),linear-gradient(180deg,{NIGHT},{AZUL_ESC})")
render(f'<div style="width:1080px;height:1080px;background:{GLOW};display:grid;place-items:center">{simbolo(BRANCO, AMBAR, 600)}</div>',
       os.path.join(OUT, "perfil", "foto-perfil.png"), 1080, 1080)
sys.argv = [sys.argv[0], "nada"]  # importar gerar_assets sem re-renderizar a versão antiga
from gerar_assets import ICONES  # reaproveita os ícones dos destaques
for k, ic in ICONES.items():
    render(f'<div style="width:1080px;height:1920px;background:{GLOW};display:grid;place-items:center">'
           f'<div style="width:720px;height:720px;border-radius:50%;display:grid;place-items:center;background:linear-gradient(180deg,rgba(255,255,255,.08),rgba(255,255,255,.02));border:3px solid rgba(255,255,255,.12)">{ic}</div></div>',
           os.path.join(OUT, "destaques", f"destaque-{k}.png"), 1080, 1920)
print("ok")
