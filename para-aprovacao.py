#!/usr/bin/env python3
"""Troca o vídeo de um post que já está na agenda e manda para "Em aprovação" no quadro.

    python3 para-aprovacao.py <id-do-post> <video-novo.mp4>

Converte o vídeo como o agendar-post.py faz, sobe no Release com o mesmo nome (o item da
agenda não muda de arquivo), gera a prévia leve no Blob e marca `aprovacao: true` com a
`previa`. O publicar.py não solta o post até o Gabriel aprovar no quadro.
"""
import importlib.util, json, pathlib, subprocess, sys

RAIZ = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("ap", RAIZ / "agendar-post.py")
ap = importlib.util.module_from_spec(spec)
sys.argv, args = sys.argv[:1], sys.argv[1:]
spec.loader.exec_module(ap)


def main(pid, video):
    video = pathlib.Path(video).expanduser()
    subprocess.run(["git", "pull", "-q", "--rebase"], cwd=RAIZ, check=True)
    agenda = json.loads((RAIZ / "agenda.json").read_text())
    item = next((i for i in agenda if i["id"] == pid), None)
    if not item or not item.get("arquivo", "").endswith(".mp4"):
        sys.exit(f"{pid} não é um vídeo na agenda")
    destino = RAIZ / "videos" / item["arquivo"]
    ap.converter(video, destino)
    ap.rodar([ap.gh(), "release", "upload", ap.TAG, str(destino), "--repo", ap.REPO, "--clobber"])
    leve = RAIZ / "videos" / f"{pid}-previa.mp4"
    ap.rodar(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", str(destino), "-vf", "scale=-2:960",
              "-c:v", "libx264", "-preset", "veryfast", "-crf", "28", "-c:a", "aac", "-b:a", "96k",
              "-movflags", "+faststart", str(leve)])
    item["aprovacao"] = True
    import time
    item["previa"] = ap.subir_previa(leve, "video/mp4") + f"?v={int(time.time())}"   # fura o cache do Blob e sempre muda a agenda
    item.pop("ajuste", None)
    (RAIZ / "agenda.json").write_text(json.dumps(agenda, ensure_ascii=False, indent=2) + "\n")
    ap.rodar(["git", "add", "agenda.json"], cwd=RAIZ)
    ap.rodar(["git", "-c", "user.name=Gabriel D. Faria", "-c", "user.email=gabrieldfaria777@gmail.com",
              "commit", "-m", f"aprovacao: {pid} com video novo"], cwd=RAIZ)
    try:
        ap.rodar(["git", "push", "origin", "main"], cwd=RAIZ)
    except subprocess.CalledProcessError:
        ap.rodar(["git", "pull", "--rebase"], cwd=RAIZ); ap.rodar(["git", "push", "origin", "main"], cwd=RAIZ)
    print(f"{pid}: vídeo trocado e esperando aprovação no quadro ({item['quando'][:16]})")


if __name__ == "__main__":
    if len(args) != 2:
        sys.exit(__doc__)
    main(*args)
