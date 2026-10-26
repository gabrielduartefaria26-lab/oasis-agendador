# Identidade visual Castelo Polímeros: tokens, símbolo e helpers de renderização.
import os, subprocess

AZUL = "#12385A"      # Azul Castelo
AZUL_ESC = "#0B2238"  # Azul Noite
AMBAR = "#F2A900"     # Âmbar Fita
CONCRETO = "#EEF1F4"  # Concreto
GRAFITE = "#17232D"   # Grafite
VERDE = "#2F7D5B"     # Verde Ciclo
BRANCO = "#FFFFFF"

FONTS = ('<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700;800'
         '&family=Barlow:wght@400;500;600;700&family=IBM+Plex+Mono:wght@500;600&display=swap" rel="stylesheet">')
HANDLE = "@castelopolimeros"
CHROME = "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell"


def simbolo(torre=AZUL, pellet=AMBAR, size=None):
    """Torre de castelo cujas faixas (fitas) se desfazem em grãos (o moído)."""
    s = f' width="{size}" height="{size}"' if size else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"{s}>'
            f'<g fill="{torre}">'
            '<rect x="8" y="4" width="8" height="8"/><rect x="20" y="4" width="8" height="8"/><rect x="32" y="4" width="8" height="8"/>'
            '<rect x="8" y="12" width="32" height="6"/>'
            '<rect x="8" y="20.5" width="32" height="3.5"/><rect x="8" y="26.5" width="32" height="3.5"/></g>'
            f'<g fill="{pellet}">'
            '<rect x="8" y="33" width="4" height="4"/><rect x="15" y="33" width="4" height="4"/><rect x="22" y="33" width="4" height="4"/>'
            '<rect x="29" y="33" width="4" height="4"/><rect x="36" y="33" width="4" height="4"/>'
            '<rect x="11.5" y="40" width="3" height="3"/><rect x="18.5" y="40" width="3" height="3"/>'
            '<rect x="25.5" y="40" width="3" height="3"/><rect x="32.5" y="40" width="3" height="3"/></g></svg>')


def logo_html(cor_texto=AZUL, torre=AZUL, pellet=AMBAR, escala=1.0):
    t = escala
    return (f'<div style="display:flex;align-items:center;gap:{14*t}px">'
            f'{simbolo(torre, pellet, int(64*t))}'
            f'<div style="line-height:.86;color:{cor_texto}">'
            f'<div style="font:800 {46*t}px \'Barlow Condensed\',\'Arial Narrow\',sans-serif;letter-spacing:{1.5*t}px">CASTELO</div>'
            f'<div style="font:600 {18.5*t}px \'Barlow Condensed\',\'Arial Narrow\',sans-serif;letter-spacing:{6.6*t}px;margin-top:{3*t}px">POLÍMEROS</div>'
            '</div></div>')


def logo_svg(cor_texto=AZUL, torre=AZUL, pellet=AMBAR):
    inner = simbolo(torre, pellet).replace('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48">', "").replace("</svg>", "")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 250 64" width="500" height="128">'
            f'<g transform="scale(1.3333)">{inner}</g>'
            f'<text x="78" y="38" fill="{cor_texto}" font-family="Barlow Condensed, Arial Narrow, sans-serif" font-weight="800" font-size="46" letter-spacing="1.5">CASTELO</text>'
            f'<text x="79" y="58" fill="{cor_texto}" font-family="Barlow Condensed, Arial Narrow, sans-serif" font-weight="600" font-size="18.5" letter-spacing="6.6">POLÍMEROS</text>'
            '</svg>')


FAIXA_CSS = f"repeating-linear-gradient(-45deg,{AMBAR} 0 26px,{AZUL_ESC} 26px 40px)"


def render(html, out_png, w, h, transparent=False):
    tmp = out_png.replace(".png", ".tmp.html")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(f'<!doctype html><html><head><meta charset="utf-8">{FONTS}'
                f'<style>*{{box-sizing:border-box}}html,body{{margin:0;width:{w}px;height:{h}px;overflow:hidden;'
                f'{"background:transparent" if transparent else ""}}}</style></head><body>{html}</body></html>')
    cmd = [CHROME, "--no-sandbox", "--disable-gpu", "--hide-scrollbars", "--virtual-time-budget=6000",
           f"--window-size={w},{h}", f"--screenshot={out_png}"]
    if transparent:
        cmd.append("--default-background-color=00000000")
    subprocess.run(cmd + ["file://" + tmp], capture_output=True, timeout=90)
    os.remove(tmp)
    assert os.path.exists(out_png), out_png
