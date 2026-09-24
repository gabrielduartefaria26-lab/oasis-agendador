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


os.makedirs("out", exist_ok=True)
for linha in os.environ["ALVOS"].strip().splitlines():
    usuario, link = linha.split()
    campos = f"business_discovery.username({usuario}){{media.limit(50){{permalink,media_url,caption}}}}"
    try:
        posts = chamar({"fields": campos})["business_discovery"]["media"]["data"]
    except Exception as e:
        print(f"{usuario}: erro {str(e).replace(TOKEN, '***')[:200]}")
        continue
    alvo = next((p for p in posts if p.get("permalink", "").rstrip("/") == link.rstrip("/")), None)
    if not alvo or not alvo.get("media_url"):
        print(f"{usuario}: {'sem media_url' if alvo else 'post não achado'}")
        continue
    nome = f"out/{usuario}"
    urllib.request.urlretrieve(alvo["media_url"], nome + ".mp4")
    open(nome + ".txt", "w").write(alvo.get("caption") or "")
    print(f"{usuario}: ok")
