#!/usr/bin/env python3
"""Simulação do grid do @gabrielfaria.ia com tudo que já saiu e tudo que está na fila.

    python3 feed-simulado.py [saida.png]

Fontes: agenda.json (posts do agendador, com capa_ms/capa), estado.json (o que já saiu) e
metricas.csv (posts feitos à mão pelo app, que não estão na agenda). Capa de cada peça:
1º slide do carrossel, capa.jpg do Reel ou o quadro de capa_ms do vídeo em videos/;
post feito à mão usa a og:image pública do link. Borda laranja = ainda vai sair.
"""
import csv, html, json, pathlib, re, subprocess, sys, urllib.request
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageOps

RAIZ = pathlib.Path(__file__).resolve().parent
VID = RAIZ / "videos"
CACHE = RAIZ / "videos" / "_capas"
TW, TH, GAP, COLS = 356, 474, 6, 3
FONTE = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
LAR = (217, 119, 87)


def quadro(video, seg):
    CACHE.mkdir(exist_ok=True)
    out = CACHE / f"{video.stem}-{int(seg*1000)}.jpg"
    if not out.exists() or out.stat().st_mtime < video.stat().st_mtime:
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(seg), "-i", str(video), "-frames:v", "1", str(out)], check=True)
    return Image.open(out)


def og_image(link):
    CACHE.mkdir(exist_ok=True)
    out = CACHE / (re.sub(r"\W", "", link)[-24:] + ".jpg")
    if not out.exists():
        req = urllib.request.Request(link, headers={"User-Agent": "Mozilla/5.0"})
        pag = urllib.request.urlopen(req, timeout=20).read().decode("utf8", "ignore")
        m = re.search(r'og:image" content="([^"]+)', pag)
        if not m:
            return None
        out.write_bytes(urllib.request.urlopen(html.unescape(m.group(1)), timeout=20).read())
    return Image.open(out)


def capa(item):
    if item.get("arquivos"):
        return Image.open(VID / item["arquivos"][0])
    if item.get("capa") and (VID / item["capa"]).exists():
        return Image.open(VID / item["capa"])
    v = VID / item["arquivo"]
    if v.exists():
        return quadro(v, item.get("capa_ms", 500) / 1000)
    return None


def main(saida):
    agenda = json.loads((RAIZ / "agenda.json").read_text())
    estado = json.loads((RAIZ / "estado.json").read_text())
    pecas, ids_media = [], set()
    for i in agenda:
        pub = estado.get(i["id"], {}).get("status") == "publicado"
        if pub: ids_media.add(str(estado[i["id"]].get("media_id")))
        pecas.append(dict(quando=datetime.fromisoformat(i["quando"]), pub=pub, img=lambda i=i: capa(i)))
    for r in csv.DictReader(open(RAIZ / "metricas.csv")):
        if r["media_id"] in ids_media or r["data_postagem"][6:10] != "2026" or r["data_postagem"][3:5] < "09":
            continue
        q = datetime.strptime(r["data_postagem"], "%d/%m/%Y %H:%M")
        pecas.append(dict(quando=q.astimezone(), pub=True, img=lambda l=r["link"]: og_image(l)))
    pecas.sort(key=lambda p: p["quando"], reverse=True)

    linhas = -(-len(pecas) // COLS)
    W = COLS * TW + (COLS + 1) * GAP; TOPO = 150
    tela = Image.new("RGB", (W, TOPO + linhas * (TH + GAP) + GAP), "white")
    d = ImageDraw.Draw(tela)
    f1, f2, f3 = ImageFont.truetype(FONTE, 40), ImageFont.truetype(FONTE, 22), ImageFont.truetype(FONTE, 20)
    ult = pecas[0]["quando"].strftime("%d/%m")
    d.text((GAP * 3, 36), "gabrielfaria.ia", font=f1, fill=(20, 20, 20))
    d.text((GAP * 3, 92), f"Simulação do feed em {ult} · {len(pecas)} posts · borda laranja = ainda vai sair", font=f2, fill=(110, 110, 110))
    for n, p in enumerate(pecas):
        x = GAP + (n % COLS) * (TW + GAP); y = TOPO + (n // COLS) * (TH + GAP)
        try:
            im = p["img"]()
        except Exception:
            im = None
        if im is None:
            d.rectangle([x, y, x + TW, y + TH], fill=(235, 235, 235))
        else:
            tela.paste(ImageOps.fit(im.convert("RGB"), (TW, TH), Image.LANCZOS), (x, y))
        if not p["pub"]:
            d.rectangle([x, y, x + TW - 1, y + TH - 1], outline=LAR, width=6)
        rot = p["quando"].strftime("%d/%m %Hh")
        d.rounded_rectangle([x + 10, y + TH - 42, x + 20 + d.textlength(rot, font=f3), y + TH - 12], 8, fill=(0, 0, 0))
        d.text((x + 15, y + TH - 39), rot, font=f3, fill="white")
    tela.save(saida)
    print(saida, tela.size, len(pecas), "posts")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else str(RAIZ / "feed-simulado.png"))
