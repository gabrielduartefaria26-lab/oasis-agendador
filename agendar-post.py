#!/usr/bin/env python3
"""Leva um carrossel pronto da pasta do post ate a fila de publicacao.

    python3 agendar-post.py ~/oasis-system/posts/carrosseis/carrossel-x \
        --prefixo brasil-eua --quando "2026-09-24T09:00:00-03:00"

Faz o caminho inteiro: converte os PNG em JPG (a API do Instagram recusa PNG),
sobe no Release, insere na agenda na ordem certa e commita. Com --ensaio nao
escreve nada, so mostra o que faria.

Regras que ele checa antes de deixar passar, porque cada uma ja deu problema:
  - legenda com mais de 2200 caracteres (o Instagram corta)
  - legenda comecando com cabecalho interno ("LEGENDA", "COPY", "##")
  - carrossel fora da faixa de 2 a 10 slides
  - id repetido na agenda
  - travessao na legenda
"""
import argparse, json, pathlib, re, subprocess, sys

REPO = "gabrielduartefaria26-lab/oasis-agendador"
TAG = "videos-v1"
RAIZ = pathlib.Path(__file__).resolve().parent
LIMITE_LEGENDA = 2200


def rodar(cmd, **kw):
    return subprocess.run(cmd, check=True, text=True, capture_output=True, **kw).stdout.strip()


def gh():
    for c in ("gh", str(pathlib.Path.home() / "bin/gh")):
        try:
            subprocess.run([c, "--version"], check=True, capture_output=True)
            return c
        except Exception:
            continue
    sys.exit("nao achei o gh")


CHECADOR = pathlib.Path.home() / ".claude/skills/carrossel-viral/scripts/checar-legenda.py"


def conferir(legenda, slides, prefixo, agenda, arquivo_legenda):
    problemas = []
    # o checador da skill e a regua oficial da legenda (teto de 600, blocos, hashtags).
    # Aqui so repetimos o teto duro do Instagram, que e outro limite.
    if CHECADOR.exists():
        r = subprocess.run([sys.executable, str(CHECADOR), str(arquivo_legenda)],
                           text=True, capture_output=True)
        if r.returncode != 0:
            problemas.append("reprovou no checar-legenda da skill:\n     " +
                             "\n     ".join((r.stdout + r.stderr).strip().splitlines()[:6]))
    if len(legenda) > LIMITE_LEGENDA:
        problemas.append(f"legenda com {len(legenda)} caracteres, o teto do Instagram e {LIMITE_LEGENDA}")
    primeira = legenda.splitlines()[0] if legenda else ""
    if re.match(r"^\s*(LEGENDA|COPY|#{1,6}\s)", primeira, re.I):
        problemas.append(f"a legenda comeca com cabecalho interno: {primeira[:50]!r}")
    if not 2 <= len(slides) <= 10:
        problemas.append(f"{len(slides)} slides; o carrossel vai de 2 a 10")
    if any(i["id"] == prefixo for i in agenda):
        problemas.append(f"ja existe um item com id {prefixo} na agenda")
    if "—" in legenda or "–" in legenda:
        problemas.append("tem travessao na legenda")
    return problemas


def main():
    p = argparse.ArgumentParser()
    p.add_argument("pasta", help="pasta do post, a que tem slides/ e legenda.txt")
    p.add_argument("--prefixo", required=True, help="id do post e prefixo dos arquivos")
    p.add_argument("--quando", required=True, help="2026-09-24T09:00:00-03:00")
    p.add_argument("--ensaio", action="store_true", help="mostra o que faria e para")
    a = p.parse_args()

    pasta = pathlib.Path(a.pasta).expanduser()
    slides = sorted((pasta / "slides").glob("slide-*.png"),
                    key=lambda f: int(re.search(r"(\d+)", f.stem).group(1)))
    legenda_arq = pasta / "legenda.txt"
    if not slides:
        sys.exit(f"nenhum slide em {pasta}/slides")
    if not legenda_arq.exists():
        sys.exit(f"falta {legenda_arq}")
    legenda = legenda_arq.read_text().strip()
    agenda = json.loads((RAIZ / "agenda.json").read_text())

    problemas = conferir(legenda, slides, a.prefixo, agenda, legenda_arq)
    print(f"{len(slides)} slides · legenda com {len(legenda)} caracteres")
    print("ordem:", ", ".join(s.stem for s in slides))
    if problemas:
        print("\nNAO VAI SUBIR:")
        for x in problemas:
            print(" -", x)
        sys.exit(1)
    print("conferencia: ok")

    destino = RAIZ / "videos"
    destino.mkdir(exist_ok=True)
    jpgs = []
    for i, s in enumerate(slides, 1):
        j = destino / f"{a.prefixo}-slide-{i}.jpg"
        if not a.ensaio:
            rodar(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "92",
                   str(s), "--out", str(j)])
        jpgs.append(j)

    item = {"id": a.prefixo, "arquivos": [j.name for j in jpgs],
            "quando": a.quando, "legenda": legenda}

    if a.ensaio:
        print("\nensaio: nada foi escrito. Item que entraria:")
        print(json.dumps({**item, "legenda": legenda[:60] + "..."}, ensure_ascii=False, indent=2))
        return 0

    g = gh()
    rodar([g, "release", "upload", TAG, *[str(j) for j in jpgs], "--repo", REPO, "--clobber"])
    print(f"{len(jpgs)} arquivos no Release")

    agenda.append(item)
    agenda.sort(key=lambda i: i["quando"])
    (RAIZ / "agenda.json").write_text(json.dumps(agenda, ensure_ascii=False, indent=2) + "\n")
    rodar(["git", "add", "agenda.json"], cwd=RAIZ)
    rodar(["git", "-c", "user.name=Gabriel D. Faria",
           "-c", "user.email=gabrieldfaria777@gmail.com",
           "commit", "-m", f"agenda: {a.prefixo} em {a.quando[:10]}"], cwd=RAIZ)
    rodar(["git", "push", "origin", "main"], cwd=RAIZ)
    print(f"agendado: {a.prefixo} para {a.quando[:16].replace('T', ' as ')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
