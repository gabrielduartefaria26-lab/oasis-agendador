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
from datetime import datetime, timedelta

REPO = "gabrielduartefaria26-lab/oasis-agendador"
TAG = "videos-v1"
RAIZ = pathlib.Path(__file__).resolve().parent
LIMITE_LEGENDA = 2200
HORA_DO_POST = 9          # um carrossel por dia, sempre no mesmo horario
FUSO = "-03:00"
TETO_DIAS = 28            # nao se programa alem de 4 semanas; o que passa vai para a geladeira


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


def quando_de(item):
    return datetime.fromisoformat(item["quando"])


def slot(dia):
    return f"{dia.strftime('%Y-%m-%d')}T{HORA_DO_POST:02d}:00:00{FUSO}"


def proximo_livre(agenda):
    """Empilha no fim da fila. A producao corre na frente da publicacao de proposito."""
    hoje = datetime.now().date()
    if not agenda:
        return slot(hoje + timedelta(days=1))
    ultimo = max(quando_de(i).date() for i in agenda)
    return slot(max(ultimo, hoje) + timedelta(days=1))


def furar_fila(agenda):
    """Assunto quente nao espera a fila. Entra no primeiro slot e empurra o resto um dia.

    So empurra o que ainda nao foi publicado; o que ja saiu fica onde esta.
    """
    alvo = (datetime.now() + timedelta(days=1)).date()
    ocupados = {quando_de(i).date() for i in agenda}
    if alvo in ocupados:
        for i in agenda:
            if quando_de(i).date() >= alvo:
                i["quando"] = slot(quando_de(i).date() + timedelta(days=1))
    return slot(alvo)


def avisar(titulo, texto):
    """Notificacao do macOS. Barato e ele pediu para ser avisado por todo canal."""
    try:
        subprocess.run(["osascript", "-e",
                        f'display notification "{texto}" with title "{titulo}" sound name "Glass"'],
                       capture_output=True, timeout=10)
    except Exception:
        pass


def aplicar_teto(agenda):
    """Corta o que passa de 28 dias e devolve o que saiu.

    Nada e perdido: o que sai da fila vai para geladeira.json e pode voltar depois.
    """
    limite = datetime.now().date() + timedelta(days=TETO_DIAS)
    dentro = [i for i in agenda if quando_de(i).date() <= limite]
    fora = [i for i in agenda if quando_de(i).date() > limite]
    if fora:
        g = RAIZ / "geladeira.json"
        guardados = json.loads(g.read_text()) if g.exists() else []
        ids = {x["id"] for x in guardados}
        guardados += [x for x in fora if x["id"] not in ids]
        g.write_text(json.dumps(guardados, ensure_ascii=False, indent=2) + "\n")
    return dentro, fora


def mostrar_fila(agenda, estado):
    if not agenda:
        print("fila vazia")
        return
    hoje = datetime.now().date()
    ultimo = max(quando_de(i).date() for i in agenda)
    print(f"{len(agenda)} posts · fila cheia ate {ultimo} "
          f"({(ultimo - hoje).days} de {TETO_DIAS} dias)\n")
    for i in sorted(agenda, key=lambda x: x["quando"]):
        st = estado.get(i["id"], {}).get("status")
        dia = quando_de(i).date()
        marca = "publicado" if st == "publicado" else ("erro" if st == "erro" else
                ("hoje" if dia == hoje else f"em {(dia - hoje).days}d"))
        print(f"{i['quando'][:10]}  {i['id']:<14} {len(i['arquivos']):>2} slides  {marca}")


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
    p.add_argument("pasta", nargs="?", help="pasta do post, a que tem slides/ e legenda.txt")
    p.add_argument("--prefixo", help="id do post e prefixo dos arquivos")
    p.add_argument("--quando", help="data explicita, 2026-09-24T09:00:00-03:00")
    p.add_argument("--urgente", action="store_true",
                   help="assunto quente: entra amanha e empurra a fila um dia")
    p.add_argument("--fila", action="store_true", help="mostra a fila e sai")
    p.add_argument("--ensaio", action="store_true", help="mostra o que faria e para")
    a = p.parse_args()

    agenda_arq = RAIZ / "agenda.json"
    if a.fila:
        estado = json.loads((RAIZ / "estado.json").read_text() or "{}")
        mostrar_fila(json.loads(agenda_arq.read_text()), estado)
        return 0
    if not a.pasta or not a.prefixo:
        sys.exit("faltou a pasta do post ou o --prefixo (use --fila para so ver a fila)")

    pasta = pathlib.Path(a.pasta).expanduser()
    slides = sorted((pasta / "slides").glob("slide-*.png"),
                    key=lambda f: int(re.search(r"(\d+)", f.stem).group(1)))
    legenda_arq = pasta / "legenda.txt"
    if not slides:
        sys.exit(f"nenhum slide em {pasta}/slides")
    if not legenda_arq.exists():
        sys.exit(f"falta {legenda_arq}")
    legenda = legenda_arq.read_text().strip()
    agenda = json.loads(agenda_arq.read_text())
    if a.quando:
        quando = a.quando
    elif a.urgente:
        quando = furar_fila(agenda)
    else:
        quando = proximo_livre(agenda)

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
            "quando": quando, "legenda": legenda}

    if a.ensaio:
        print("\nensaio: nada foi escrito. Item que entraria:")
        print(json.dumps({**item, "legenda": legenda[:60] + "..."}, ensure_ascii=False, indent=2))
        return 0

    g = gh()
    rodar([g, "release", "upload", TAG, *[str(j) for j in jpgs], "--repo", REPO, "--clobber"])
    print(f"{len(jpgs)} arquivos no Release")

    agenda.append(item)
    agenda.sort(key=lambda i: i["quando"])
    agenda, cortados = aplicar_teto(agenda)
    for c in cortados:
        print(f"passou de {TETO_DIAS} dias e foi para a geladeira: {c['id']} ({c['quando'][:10]})")
    agenda_arq.write_text(json.dumps(agenda, ensure_ascii=False, indent=2) + "\n")
    if a.urgente:
        print("fila empurrada um dia para abrir espaco")
    rodar(["git", "add", "agenda.json"], cwd=RAIZ)
    rodar(["git", "-c", "user.name=Gabriel D. Faria",
           "-c", "user.email=gabrieldfaria777@gmail.com",
           "commit", "-m", f"agenda: {a.prefixo} em {quando[:10]}"], cwd=RAIZ)
    rodar(["git", "push", "origin", "main"], cwd=RAIZ)
    dia = quando[:16].replace("T", " as ")
    print(f"agendado: {a.prefixo} para {dia}")
    extra = f", {len(cortados)} foram para a geladeira" if cortados else ""
    avisar("Carrossel na fila", f"{a.prefixo} sai em {dia}{extra}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
