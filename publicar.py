"""Publica no Instagram da Oasis os posts cuja hora ja chegou.

Le agenda.json, publica o que venceu e ainda nao foi publicado, e registra
o resultado em estado.json. Roda a cada 15 minutos pelo GitHub Actions.

Tres formatos, deduzidos do proprio item da agenda:
  Reel       "arquivo": "corte.mp4"
  Imagem     "arquivo": "post.jpg"
  Carrossel  "arquivos": ["slide-1.jpg", "slide-2.jpg", ...]
"""
import json, os, sys, time, urllib.error, urllib.parse, urllib.request
from datetime import datetime, timezone

API = "https://graph.facebook.com/v21.0"
TOKEN = os.environ["IG_TOKEN"]
IG_ID = os.environ["IG_USER_ID"]
BASE_URL = os.environ["VIDEOS_BASE_URL"].rstrip("/")
# Ensaio: monta o container na Meta e para antes de publicar. Valida token,
# permissoes e download do arquivo sem postar nada no perfil.
ENSAIO = os.environ.get("ENSAIO") == "1"

VIDEO = (".mp4", ".mov")
# A API de publicacao do Instagram so aceita JPEG. PNG e recusado la na frente,
# com erro obscuro, entao e melhor barrar aqui.
IMAGEM = (".jpg", ".jpeg")


def chamar(caminho, dados=None):
    url = f"{API}/{caminho}"
    corpo = None
    if dados is not None:
        dados = {**dados, "access_token": TOKEN}
        corpo = urllib.parse.urlencode(dados).encode()
    else:
        url += f"{'&' if '?' in url else '?'}access_token={TOKEN}"
    try:
        with urllib.request.urlopen(urllib.request.Request(url, data=corpo), timeout=90) as r:
            return json.load(r)
    except urllib.error.HTTPError as erro:
        # Sem o corpo da resposta, um 400 da Meta nao diz nada. O token nunca
        # aparece nele, mas a limpeza abaixo garante que nao vaze pelo log.
        detalhe = erro.read().decode("utf-8", "replace").replace(TOKEN, "***")
        raise RuntimeError(f"{erro.code} em {caminho.split('/')[-1]}: {detalhe}") from None


def criar_container(arquivo, campos):
    """Monta um container de midia. Os campos extras dizem se e peca solta ou filho."""
    url = f"{BASE_URL}/{urllib.parse.quote(arquivo)}"
    extensao = os.path.splitext(arquivo)[1].lower()
    if extensao in VIDEO:
        campos = {"media_type": "REELS", "video_url": url, **campos}
    elif extensao in IMAGEM:
        campos = {"image_url": url, **campos}
    else:
        raise RuntimeError(f"{arquivo}: so vale .mp4 para Reel e .jpg para imagem, "
                           "o Instagram nao aceita PNG")
    print(f"  container: {url}")
    return chamar(f"{IG_ID}/media", campos)["id"]


def esperar(container):
    """O Instagram baixa e processa antes de aceitar a publicacao.

    Imagem costuma sair pronta na primeira conferida; Reel de ate 90s leva de
    um a tres minutos.
    """
    for tentativa in range(40):
        st = chamar(f"{container}?fields=status_code,status")
        if st["status_code"] == "FINISHED":
            return
        if st["status_code"] == "ERROR":
            raise RuntimeError(f"processamento falhou: {st.get('status')}")
        print(f"  {st['status_code']} ({tentativa*15}s)")
        time.sleep(15)
    raise RuntimeError("processamento passou de 10 minutos")


def publicar(item):
    arquivos = item.get("arquivos")
    if arquivos:
        if not 2 <= len(arquivos) <= 10:
            raise RuntimeError(f"carrossel vai de 2 a 10 imagens, vieram {len(arquivos)}")
        if any(os.path.splitext(a)[1].lower() in VIDEO for a in arquivos):
            raise RuntimeError("carrossel aqui e so de imagem; video em carrossel "
                               "usa outro caminho e nao esta implementado")
        filhos = []
        for arquivo in arquivos:
            filho = criar_container(arquivo, {"is_carousel_item": "true"})
            esperar(filho)
            filhos.append(filho)
        container = chamar(f"{IG_ID}/media", {
            "media_type": "CAROUSEL",
            "children": ",".join(filhos),
            "caption": item["legenda"],
        })["id"]
    elif item.get("arquivo"):
        campos = {"caption": item["legenda"]}
        if os.path.splitext(item["arquivo"])[1].lower() in VIDEO:
            campos["share_to_feed"] = "true"
        container = criar_container(item["arquivo"], campos)
    else:
        raise RuntimeError("o item precisa de 'arquivo' ou de 'arquivos'")

    esperar(container)
    if ENSAIO:
        print("  ensaio: container pronto e aceito, nao vou publicar")
        return None
    return chamar(f"{IG_ID}/media_publish", {"creation_id": container})["id"]


def main():
    agenda = json.load(open("agenda.json"))
    estado = json.load(open("estado.json")) if os.path.exists("estado.json") else {}
    agora = datetime.now(timezone.utc)

    pendente = lambda i: estado.get(i["id"], {}).get("status") != "publicado"
    vencidos = [i for i in agenda
                if (ENSAIO or datetime.fromisoformat(i["quando"]) <= agora)
                and pendente(i)]
    if not vencidos:
        print("nada a publicar")
        return 0

    houve_erro = False
    # um por execucao: se dois vencerem juntos, o segundo sai no ciclo seguinte,
    # 15 minutos depois. Evita estourar o limite da API num acumulo de atraso.
    item = vencidos[0]
    print(f"publicando {item['id']} (agendado para {item['quando']})")
    try:
        media_id = publicar(item)
        if ENSAIO:
            print("  ensaio concluido, estado nao foi alterado")
            return 0
        estado[item["id"]] = {"status": "publicado", "media_id": media_id,
                              "em": agora.isoformat(timespec="seconds")}
        print(f"  ok, media {media_id}")
    except Exception as e:
        anterior = estado.get(item["id"], {}).get("tentativas", 0)
        estado[item["id"]] = {"status": "erro", "erro": str(e),
                              "tentativas": anterior + 1,
                              "em": agora.isoformat(timespec="seconds")}
        print(f"  FALHOU: {e}", file=sys.stderr)
        houve_erro = True

    json.dump(estado, open("estado.json", "w"), ensure_ascii=False, indent=2)
    if len(vencidos) > 1:
        print(f"{len(vencidos)-1} ainda na fila, saem nos proximos ciclos")
    return 1 if houve_erro else 0


if __name__ == "__main__":
    sys.exit(main())
