"""Puxa os numeros de todos os posts do @system.oasis e grava em metricas.csv.

Roda uma vez por dia pelo GitHub Actions. Pega TODOS os posts da conta, inclusive os
publicados a mao pelo app (meme, tutorial), e nao so os que sairam pelo agendador.

O que cada post e (formato, fonte, palavra do CTA, versao do teste) vem da agenda:
post que saiu pelo agendador ja nasce classificado; post manual entra como "manual" e o
Gabriel marca o formato na propria planilha.

Precisa da permissao instagram_manage_insights no token. Sem ela a lista de posts sai,
mas as colunas de alcance, salvamento e compartilhamento ficam vazias.
"""
import csv, json, os, sys, urllib.error, urllib.parse, urllib.request
from datetime import datetime, timezone

API = "https://graph.facebook.com/v21.0"
TOKEN = os.environ["IG_TOKEN"]
IG_ID = os.environ["IG_USER_ID"]
SAIDA = "metricas.csv"

# o que a planilha mostra, nessa ordem
COLUNAS = ["data", "formato", "fonte", "cta", "versao", "tipo", "alcance", "views",
           "curtidas", "comentarios", "salvamentos", "compartilhamentos", "interacoes",
           "taxa_salvamento", "gancho", "link", "media_id", "atualizado"]


def chamar(caminho, params=None):
    params = {**(params or {}), "access_token": TOKEN}
    url = f"{API}/{caminho}?{urllib.parse.urlencode(params)}"
    try:
        with urllib.request.urlopen(url, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        corpo = e.read().decode("utf-8", "replace").replace(TOKEN, "***")
        raise RuntimeError(f"{e.code}: {corpo[:240]}") from None


def todos_os_posts():
    campos = "id,caption,media_type,media_product_type,timestamp,permalink,like_count,comments_count"
    posts, pagina = [], chamar(f"{IG_ID}/media", {"fields": campos, "limit": 50})
    while True:
        posts += pagina.get("data", [])
        prox = pagina.get("paging", {}).get("next")
        if not prox:
            return posts
        with urllib.request.urlopen(prox, timeout=60) as r:
            pagina = json.load(r)


def insights(media_id, produto):
    # Reel e carrossel aceitam conjuntos diferentes; pede um por um para que uma
    # metrica recusada nao derrube as outras.
    pedidas = ["reach", "saved", "shares", "total_interactions", "views"]
    achou = {}
    for m in pedidas:
        try:
            d = chamar(f"{media_id}/insights", {"metric": m})
            valor = d["data"][0].get("values", [{}])[0].get("value")
            if valor is None:
                valor = d["data"][0].get("total_value", {}).get("value")
            achou[m] = valor
        except RuntimeError as e:
            if "(#10)" in str(e) or "permission" in str(e).lower():
                return None  # sem a permissao de insights: nao adianta insistir
            achou[m] = ""
    return achou


def catalogo():
    """O que se sabe de cada post que saiu pelo agendador, indexado pelo media_id."""
    try:
        estado = json.load(open("estado.json"))
        agenda = {i["id"]: i for i in json.load(open("agenda.json"))}
    except FileNotFoundError:
        return {}
    saida = {}
    for pid, e in estado.items():
        if e.get("status") != "publicado" or not e.get("media_id"):
            continue
        item = agenda.get(pid, {})
        saida[e["media_id"]] = {
            "formato": item.get("formato") or ("ferramenta" if pid.startswith("repos") else "case"),
            "fonte": "agendador",
            "cta": item.get("cta", ""),
            "versao": item.get("versao", ""),
        }
    return saida


def main():
    agora = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
    cat = catalogo()
    linhas, sem_permissao = [], False
    for p in todos_os_posts():
        ins = None if sem_permissao else insights(p["id"], p.get("media_product_type"))
        if ins is None:
            sem_permissao = True
            ins = {}
        c = cat.get(p["id"], {"formato": "manual", "fonte": "app", "cta": "", "versao": ""})
        alcance = ins.get("reach") or 0
        salvos = ins.get("saved") or 0
        linhas.append({
            "data": p["timestamp"][:10],
            **c,
            "tipo": (p.get("media_product_type") or p.get("media_type") or "").lower(),
            "alcance": ins.get("reach", ""), "views": ins.get("views", ""),
            "curtidas": p.get("like_count", ""), "comentarios": p.get("comments_count", ""),
            "salvamentos": ins.get("saved", ""), "compartilhamentos": ins.get("shares", ""),
            "interacoes": ins.get("total_interactions", ""),
            "taxa_salvamento": f"{salvos / alcance:.3f}" if alcance else "",
            "gancho": ((p.get("caption") or "").split("\n")[0])[:120],
            "link": p.get("permalink", ""), "media_id": p["id"], "atualizado": agora,
        })

    linhas.sort(key=lambda x: x["data"], reverse=True)
    with open(SAIDA, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUNAS)
        w.writeheader()
        w.writerows(linhas)
    print(f"{len(linhas)} posts gravados em {SAIDA}")
    if sem_permissao:
        print("AVISO: o token nao tem instagram_manage_insights. Lista saiu, numeros nao.",
              file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
