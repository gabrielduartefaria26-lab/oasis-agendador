"""Monta o item de carrossel para colar na agenda, com os slides na ordem certa.

    python3 montar-carrossel.py ~/oasis-system/posts/1-manifesto/out \
        --quando "2026-09-25T09:00:00-03:00" --id manifesto-01

Ordena pelo numero que aparece no nome, nao por ordem alfabetica: e o que impede
o slide-10 de entrar logo depois do slide-1 e baguncar o carrossel.
"""
import argparse, json, os, re, sys

EXTENSOES = (".jpg", ".jpeg", ".png")


def chave(nome):
    # ("slide-10.jpg") -> ("slide-", 10). Numero vira numero, resto fica texto.
    return [int(p) if p.isdigit() else p.lower() for p in re.split(r"(\d+)", nome)]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("pasta")
    p.add_argument("--quando", required=True, help="2026-09-25T09:00:00-03:00")
    p.add_argument("--id", required=True)
    p.add_argument("--legenda", default="")
    a = p.parse_args()

    slides = sorted((f for f in os.listdir(a.pasta) if f.lower().endswith(EXTENSOES)),
                    key=chave)
    if not slides:
        sys.exit(f"nenhuma imagem em {a.pasta}")
    if len(slides) > 10:
        sys.exit(f"{len(slides)} slides: o carrossel do Instagram vai ate 10")

    png = [f for f in slides if f.lower().endswith(".png")]
    if png:
        print(f"AVISO: {len(png)} PNG na lista. Converta para .jpg antes de subir "
              "no Release, a API do Instagram recusa PNG.\n", file=sys.stderr)

    print("confira a ordem:", file=sys.stderr)
    for i, f in enumerate(slides, 1):
        print(f"  {i:>2}. {f}", file=sys.stderr)
    print(file=sys.stderr)

    item = {"id": a.id,
            "arquivos": [os.path.splitext(f)[0] + ".jpg" for f in slides],
            "quando": a.quando,
            "legenda": a.legenda or "ESCREVA A LEGENDA"}
    print(json.dumps(item, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
