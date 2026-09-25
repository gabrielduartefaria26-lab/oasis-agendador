"""Corrige a cor de vídeo gravado à noite antes de subir: pele branca demais, fria, sem cor e com ruído.

Mede o próprio vídeo e decide sozinho quanto corrigir, sem valor fixo chutado:

1. HDR vira SDR. O iPhone grava em HDR (HLG) por padrão. Fora do app da Apple esse vídeo
   aparece lavado e com a pele estourada, que é o "branco estranho" mais comum.
2. Mede a pele. Pega a parte mais clara de cada quadro (à noite, é o rosto iluminado)
   e vê o quanto ela está clara, fria e sem cor.
3. Corrige só o que a medição pediu: baixa as altas luzes, esquenta, devolve cor à
   pele com vibrance (mexe mais no que tem pouca cor e poupa o que já tem), levanta
   um pouco as sombras e tira o ruído da noite.

Uso:
  python3 tratar-video.py corte.mp4                  # corte-tratado.mp4 + corte-antes-depois.jpg
  python3 tratar-video.py corte.mp4 --provas         # só a folha com leve, médio e forte, para escolher
  python3 tratar-video.py corte.mp4 --forca forte    # aplica a força escolhida na folha

Precisa só do ffmpeg (brew install ffmpeg).
"""
import argparse, json, os, subprocess, sys

FORCAS = {"leve": 0.6, "medio": 1.0, "forte": 1.4}
LARG, ALT = 48, 84  # quadro reduzido para medir: sobra informação e custa nada


def sonda(video):
    s = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                        "stream=color_transfer,color_primaries,width,height:format=duration",
                        "-of", "json", video], capture_output=True, text=True, check=True)
    d = json.loads(s.stdout)
    return d["streams"][0], float(d["format"].get("duration") or 0)


def para_sdr(info):
    """Filtro que traz HDR para SDR. Vazio se o vídeo já é SDR."""
    if info.get("color_transfer") not in ("arib-std-b67", "smpte2084"):
        return ""
    pin = "2020" if "2020" in (info.get("color_primaries") or "bt2020") else "709"
    return (f"zscale=tin={info['color_transfer']}:pin={pin}:min=2020_ncl:t=linear:npl=100,"
            "format=gbrpf32le,zscale=p=709,tonemap=tonemap=mobius:desat=0,"
            "zscale=t=709:m=709:r=tv,format=yuv420p,")


def e_pele(r, g, b):
    """Pele de qualquer tom tem vermelho acima de verde e azul. Parede de LED azul, roupa preta
    e cabelo ficam de fora; pele pálida sob luz neutra também, e aí vale o plano B."""
    return r > 45 and r >= g and r >= b and r - min(g, b) >= 12


def medir(video, prefixo, duracao):
    """Mede a pele (pixels com cor de pele) e o quadro inteiro."""
    fps = min(4, max(1, 40 / max(duracao, 1)))
    bruto = subprocess.run(["ffmpeg", "-v", "error", "-i", video, "-vf",
                            f"{prefixo}fps={fps:.3f},scale={LARG}:{ALT},format=rgb24",
                            "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    px = LARG * ALT
    quadros = [bruto[i:i + px * 3] for i in range(0, len(bruto) - px * 3 + 1, px * 3)]
    lum_geral, estourado, pele, claros = [], 0, [], []
    for q in quadros:
        pontos = []
        for i in range(0, len(q), 3):
            r, g, b = q[i], q[i + 1], q[i + 2]
            p = (0.2126 * r + 0.7152 * g + 0.0722 * b, r, g, b)
            pontos.append(p)
            estourado += p[0] >= 250
            if e_pele(r, g, b):
                pele.append(p)
        lum_geral.append(sum(p[0] for p in pontos) / px)
        claros += sorted(pontos, reverse=True)[:px // 6]
    total = max(len(quadros) * px, 1)
    achou = len(pele) / total >= 0.02
    amostra = pele if achou else claros  # plano B: sem pele reconhecível, o rosto é o mais claro
    n = len(amostra) or 1
    lums = sorted(p[0] for p in amostra) or [0]
    return {
        "achou_pele": achou,
        "quadro": sum(lum_geral) / max(len(lum_geral), 1),
        "pele": sum(lums) / n,
        "brilho_max": lums[int(len(lums) * 0.9)],     # os 10% mais claros: testa, nariz, reflexo
        "calor": sum(p[1] - p[3] for p in amostra) / n,  # vermelho menos azul: pele saudável 40 a 80
        "amarelo": sum(p[2] - p[3] for p in amostra) / n,  # verde menos azul: pele saudável 18 a 35
        "cor": sum((max(p[1:]) - min(p[1:])) / max(max(p[1:]), 1) for p in amostra) / n,
        "estourado": estourado / total,
    }


def receita(m, f):
    """Transforma a medição em filtros. f é a força (0,6 leve, 1 médio, 1,4 forte)."""
    filtros, notas = [], []
    if m["quadro"] < 90:
        filtros.append(f"hqdn3d={1.5 * f:.2f}:{1.2 * f:.2f}:{4 * f:.2f}:{3 * f:.2f}")
        notas.append("tira ruído de pouca luz")
    desce = min(0.14, max(0.0, (m["brilho_max"] - 205) / 255 * 1.3)) * f
    # Nada de clarear: rosto mais claro à noite lê como pele mais branca, e levantar sombra
    # lava o fundo. Só desce o que estourou e firma um pouco o contraste.
    if desce:
        filtros.append("curves=all='0/0 0.5/{:.3f} 0.8/{:.3f} 1/{:.3f}'".format(
            0.5 - desce * 0.3, 0.8 - desce, 1 - desce * 0.6))
        notas.append(f"baixa as altas luzes em {desce * 100:.0f}%")
    if m["achou_pele"]:
        # Só nos tons de pele: devolve o amarelo que a luz fria roubou e tira o magenta.
        # O resto da cena, inclusive fundo de LED, fica como está.
        falta = max(0.0, 24 - m["amarelo"])
        if falta:
            y = min(0.40, falta / 100 * 2.2) * f
            filtros.append(f"selectivecolor=reds='0 {-y * 0.35:.3f} {y:.3f} {y * 0.15:.3f}':"
                           f"yellows='0 {-y * 0.25:.3f} {y * 0.8:.3f} {y * 0.1:.3f}'")
            notas.append(f"devolve o amarelo da pele (+{y * 100:.0f}%), sem mexer no fundo")
    elif m["calor"] < 45:
        temp = max(5000, 6500 - (45 - m["calor"]) * 35 * f)
        filtros.append(f"colortemperature=temperature={temp:.0f}:pl=0.6")
        notas.append(f"esquenta a imagem ({temp:.0f}K)")
    if m["cor"] < 0.30 and not m["achou_pele"]:  # com pele achada o selectivecolor já devolve a cor
        filtros.append(f"vibrance=intensity={min(0.45, (0.32 - m['cor']) * 2.5) * f:.2f}")
        notas.append("devolve cor à pele")
    filtros.append(f"unsharp=5:5:{0.35 * f:.2f}:5:5:0")
    return ",".join(filtros), notas


def folha(video, prefixo, cadeias, nomes, saida, duracao):
    """Um quadro do meio do vídeo, lado a lado: original e cada versão tratada."""
    meio = f"{duracao / 2:.2f}"
    ramos = [f"[v{i}]{c or 'null'},scale=-2:960,drawtext=text='{n}':x=20:y=20:fontsize=40:"
             f"fontcolor=white:box=1:boxcolor=black@0.6:boxborderw=10[s{i}]"
             for i, (c, n) in enumerate(zip(cadeias, nomes))]
    fc = (f"[0:v]{prefixo}split={len(cadeias)}" + "".join(f"[v{i}]" for i in range(len(cadeias)))
          + ";" + ";".join(ramos) + ";" + "".join(f"[s{i}]" for i in range(len(cadeias)))
          + f"hstack=inputs={len(cadeias)}")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", meio, "-i", video, "-filter_complex", fc,
                    "-frames:v", "1", "-q:v", "3", saida], check=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("video")
    ap.add_argument("--forca", choices=FORCAS, default="medio")
    ap.add_argument("--provas", action="store_true", help="só gera a folha leve/médio/forte")
    a = ap.parse_args()

    info, duracao = sonda(a.video)
    prefixo = para_sdr(info)
    m = medir(a.video, prefixo, duracao)
    base = os.path.splitext(a.video)[0]

    print(f"vídeo: {info['width']}x{info['height']}, {duracao:.1f}s, "
          f"{'HDR, vai virar SDR' if prefixo else 'SDR'}")
    print(f"pele{'' if m['achou_pele'] else ' (não reconhecida, usei a parte mais clara)'}: "
          f"brilho {m['pele']:.0f}/255, amarelo {m['amarelo']:.0f}, calor {m['calor']:.0f}, "
          f"cor {m['cor']:.2f}  |  "
          f"quadro: brilho {m['quadro']:.0f}/255")
    if m["estourado"] > 0.02:
        print(f"aviso: {m['estourado'] * 100:.0f}% da imagem está branco puro. Isso não volta na "
              "edição, só na gravação (luz mais longe do rosto ou exposição mais baixa).")

    if a.provas:
        cadeias = [""] + [receita(m, f)[0] for f in FORCAS.values()]
        saida = base + "-provas.jpg"
        folha(a.video, prefixo, cadeias, ["original", *FORCAS], saida, duracao)
        print(f"folha: {saida}\nescolha e rode de novo com --forca leve|medio|forte")
        return

    cadeia, notas = receita(m, FORCAS[a.forca])
    print("correções: " + "; ".join(notas))
    saida = base + "-tratado.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a.video, "-vf", prefixo + cadeia,
                    "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p",
                    "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
                    "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", saida], check=True)
    folha(a.video, prefixo, ["", cadeia], ["antes", "depois"], base + "-antes-depois.jpg", duracao)
    print(f"pronto: {saida}\ncompare: {base}-antes-depois.jpg")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as e:
        sys.exit(f"o ffmpeg falhou: {(e.stderr or b'').decode(errors='ignore')[-400:]}")
