"""Baixa os vídeos de Reels de referência para dissecar (duração, texto na tela, fala).

Roda sob demanda pelo GitHub Actions, porque o token só existe lá. Recebe em ALVOS uma
linha por Reel no formato "usuario permalink". Procura o permalink entre os últimos posts
do perfil via business_discovery e baixa o media_url para out/. O resultado sai como
artefato da execução, não entra no repositório.
"""
import json, os, urllib.parse, urllib.request

API = "https://graph.facebook.com/v21.0"
TOKEN = os.environ["IG_TOKEN"]
IG_ID = os.environ["IG_USER_ID"]


def chamar(params):
    url = f"{API}/{IG_ID}?{urllib.parse.urlencode({**params, 'access_token': TOKEN})}"
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.load(r)


def codigo(link):
    """Shortcode do post: /p/X/ e /reel/X/ são o mesmo vídeo."""
    partes = [x for x in link.split("?")[0].split("/") if x]
    return partes[-1]


def perfis_dele():
    lista, grupo = [], ""
    for l in open("referencias.txt", encoding="utf-8"):
        l = l.strip()
        if l.startswith("## "):
            grupo = l[3:].strip()
        elif l and not l.startswith("#") and grupo == "gabriel":
            lista.append(l.lstrip("@"))
    return lista


def posts_de(usuario):
    campos = f"business_discovery.username({usuario}){{media.limit(100){{permalink,media_url,caption}}}}"
    return chamar({"fields": campos})["business_discovery"]["media"]["data"]


os.makedirs("out", exist_ok=True)
cache = {}
for linha in os.environ["ALVOS"].strip().splitlines():
    partes = linha.split()
    link = partes[-1]
    candidatos = partes[:1] if len(partes) > 1 else perfis_dele()   # só o link: procura nos perfis dele
    alvo = usuario = None
    for u in candidatos:
        if u not in cache:
            try:
                cache[u] = posts_de(u)
                print(f"{u}: {len(cache[u])} posts lidos")
            except Exception as e:
                print(f"{u}: erro {str(e).replace(TOKEN, '***')[:200]}")
                cache[u] = []
        alvo = next((p for p in cache[u] if codigo(p.get("permalink", "")) == codigo(link)), None)
        if alvo:
            usuario = u
            break
    if not alvo or not alvo.get("media_url"):
        print(f"{codigo(link)}: {'sem media_url' if alvo else 'post não achado nos perfis'}")
        continue
    nome = f"out/{usuario}__{codigo(link)}"
    urllib.request.urlretrieve(alvo["media_url"], nome + ".mp4")
    open(nome + ".txt", "w").write(alvo.get("caption") or "")
    print(f"{codigo(link)}: ok ({usuario})")
