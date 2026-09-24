"""Caça os Reels fora da curva dos perfis de referência e grava em outliers.csv.

Roda uma vez por semana pelo GitHub Actions. Fora da curva não é viral: é o Reel que fez
pelo menos 3 vezes a mediana de interação do PRÓPRIO perfil nos últimos posts. Assim um
perfil de 800 mil não esmaga um de 8 mil, e o que sobra é formato e tema que venceram, não
audiência que o perfil já tinha.

Usa business_discovery da API do Instagram: só funciona com perfil comercial ou de criador,
e devolve curtida e comentário, não visualização. Perfil pessoal ou que esconde curtida
aparece como pulado no log.

A lista de perfis mora em referencias.txt, um @ por linha (linha com # é comentário).
"""
import csv, json, os, statistics, sys, urllib.error, urllib.parse, urllib.request
from datetime import datetime, timedelta, timezone

API = "https://graph.facebook.com/v21.0"
TOKEN = os.environ["IG_TOKEN"]
IG_ID = os.environ["IG_USER_ID"]
SAIDA = "outliers.csv"
VEZES = 3.0          # quantas vezes a mediana do perfil para contar como fora da curva
JANELA_DIAS = 60     # formato mais velho que isso provavelmente já saturou
POSTS_POR_PERFIL = 40
MINIMO_PARA_MEDIANA = 8

COLUNAS = ["vezes_acima", "perfil", "seguidores", "data", "interacoes", "curtidas",
           "comentarios", "mediana_perfil", "legenda", "link", "coletado"]


def chamar(caminho, params=None):
    params = {**(params or {}), "access_token": TOKEN}
    url = f"{API}/{caminho}?{urllib.parse.urlencode(params)}"
    try:
        with urllib.request.urlopen(url, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        corpo = e.read().decode("utf-8", "replace").replace(TOKEN, "***")
        raise RuntimeError(f"{e.code}: {corpo[:240]}") from None


def perfis():
    with open("referencias.txt", encoding="utf-8") as f:
        return [l.strip().lstrip("@") for l in f if l.strip() and not l.startswith("#")]


def posts_de(usuario):
    campos = (f"business_discovery.username({usuario}){{followers_count,"
              f"media.limit({POSTS_POR_PERFIL}){{caption,like_count,comments_count,"
              f"media_product_type,timestamp,permalink}}}}")
    bd = chamar(IG_ID, {"fields": campos})["business_discovery"]
    return bd.get("followers_count", 0), bd.get("media", {}).get("data", [])


def main():
    agora = datetime.now(timezone.utc)
    corte = agora - timedelta(days=JANELA_DIAS)
    achados, pulados = [], []
    for u in perfis():
        try:
            seg, posts = posts_de(u)
        except Exception as e:
            pulados.append(f"{u}: {e}")
            continue
        reels = [p for p in posts if p.get("media_product_type") == "REELS" and "like_count" in p]
        if len(reels) < MINIMO_PARA_MEDIANA:
            pulados.append(f"{u}: só {len(reels)} Reels com curtida visível")
            continue
        inter = lambda p: p.get("like_count", 0) + p.get("comments_count", 0)
        mediana = statistics.median(inter(p) for p in reels) or 1
        for p in reels:
            quando = datetime.fromisoformat(p["timestamp"].replace("+0000", "+00:00"))
            vezes = inter(p) / mediana
            if quando >= corte and vezes >= VEZES:
                achados.append({
                    "vezes_acima": f"{vezes:.1f}", "perfil": u, "seguidores": seg,
                    "data": quando.astimezone(timezone(timedelta(hours=-3))).strftime("%d/%m/%Y"),
                    "interacoes": inter(p), "curtidas": p.get("like_count", 0),
                    "comentarios": p.get("comments_count", 0), "mediana_perfil": int(mediana),
                    "legenda": " ".join((p.get("caption") or "").split())[:220],
                    "link": p.get("permalink", ""), "coletado": agora.strftime("%Y-%m-%d %H:%M"),
                })
    achados.sort(key=lambda a: float(a["vezes_acima"]), reverse=True)
    with open(SAIDA, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUNAS)
        w.writeheader()
        w.writerows(achados)
    print(f"{len(achados)} Reels fora da curva em {len(perfis()) - len(pulados)} perfis lidos")
    for p in pulados:
        print("pulado:", p)
    if len(pulados) == len(perfis()):
        sys.exit("nenhum perfil lido: confira a permissão do token para business_discovery")


if __name__ == "__main__":
    main()
