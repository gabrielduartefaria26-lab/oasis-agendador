"""Varredura diária · transcrição só do que presta (30/09/2026).

Regra dele: "transcrever apenas vídeos falados, e redobrar o critério antes de transcrever".
Pega as referências que ele marcou como "→ Vídeo falado" no quadro e, para cada uma ainda sem
análise, só gasta crédito do Supadata se o Reel passar na MESMA régua do caçador de outliers:

  1. perfil comercial ou de criador (senão não dá para medir: barrada)
  2. publicado há no máximo 60 dias
  3. pelo menos 3x a mediana de interação dos Reels do PRÓPRIO perfil
  4. pelo menos 100 interações e mediana do perfil de pelo menos 30 (senão a razão é ruído)

Passou: transcreve pelo Supadata e grava a fala na referência. Não passou: grava o motivo e
não gasta crédito. Roda no GitHub Actions (varredura.yml), sem o Mac.
"""
import html, json, os, re, statistics, time, urllib.error, urllib.parse, urllib.request
from datetime import datetime, timedelta, timezone

from outliers import VEZES, JANELA_DIAS, MINIMO_INTERACOES, MEDIANA_MINIMA, MINIMO_PARA_MEDIANA, posts_de

REFS = "https://oasis-dm.vercel.app/api/referencias"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh) Chrome/124"}
SUPADATA = os.environ["SUPADATA_KEY"]
ROBO = os.environ["ROBO_SECRET"]
MAX_POR_RODADA = 10


def http(url, dados=None, cab=None, metodo=None):
    req = urllib.request.Request(url, data=json.dumps(dados).encode() if dados is not None else None,
                                 headers={**UA, **(cab or {})}, method=metodo)
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.status, json.load(r)


def autor_do(link):
    """@ do autor pela página pública de incorporação (sem login)."""
    cod = re.search(r"/(reel|p)/([^/?]+)", link).group(2)
    s = urllib.request.urlopen(urllib.request.Request(f"https://www.instagram.com/reel/{cod}/embed/captioned/", headers=UA),
                               timeout=20).read().decode("utf-8", "ignore")
    u = re.search(r'class="UsernameText"[^>]*>([^<]+)', s)
    return cod, (html.unescape(u.group(1)).strip() if u else "")


def medir(link):
    """(passou, motivo, dados) contra a régua do caçador."""
    cod, autor = autor_do(link)
    if not autor:
        return False, "não achei o autor (post privado ou apagado)", {}
    try:
        _, posts = posts_de(autor)
    except Exception:
        return False, f"@{autor} é perfil pessoal: sem métrica pública, não dá para medir", {"autor": autor}
    inter = lambda p: p.get("like_count", 0) + p.get("comments_count", 0)
    reels = [p for p in posts if p.get("media_product_type") == "REELS" and "like_count" in p]
    este = next((p for p in posts if cod in (p.get("permalink") or "")), None)
    d = {"autor": autor}
    if not este:
        return False, f"o Reel não está entre os últimos 40 posts de @{autor} (antigo demais)", d
    if len(reels) < MINIMO_PARA_MEDIANA:
        return False, f"@{autor} tem só {len(reels)} Reels com curtida visível", d
    mediana = statistics.median(inter(p) for p in reels) or 1
    vezes = inter(este) / mediana
    dias = (datetime.now(timezone.utc) - datetime.fromisoformat(este["timestamp"].replace("+0000", "+00:00"))).days
    d.update(vezes=round(vezes, 1), interacoes=inter(este), mediana=int(mediana), dias=dias)
    if dias > JANELA_DIAS:
        return False, f"publicado há {dias} dias (máximo {JANELA_DIAS})", d
    if mediana < MEDIANA_MINIMA:
        return False, f"mediana de @{autor} é {mediana:.0f} interações: pequena demais para comparar", d
    if inter(este) < MINIMO_INTERACOES:
        return False, f"só {inter(este)} interações (mínimo {MINIMO_INTERACOES})", d
    if vezes < VEZES:
        return False, f"{vezes:.1f}x a mediana de @{autor} (precisa de {VEZES:.0f}x)", d
    return True, f"{vezes:.1f}x a mediana de @{autor}, {inter(este)} interações, há {dias} dias", d


def transcrever(link):
    """Fala pelo Supadata: os 10 primeiros segundos (o gancho) e o texto inteiro."""
    q = urllib.parse.urlencode({"url": link, "mode": "auto"})
    cab = {"x-api-key": SUPADATA}
    st, d = http(f"https://api.supadata.ai/v1/transcript?{q}", cab=cab)
    if st == 202 and d.get("jobId"):          # vídeo longo: o Supadata responde depois
        for _ in range(20):
            time.sleep(6)
            _, d = http(f"https://api.supadata.ai/v1/transcript/{d['jobId']}", cab=cab)
            if d.get("status") in ("completed", None) and "content" in d: break
            if d.get("status") == "failed": return "", ""
    partes = d.get("content") or []
    if isinstance(partes, str): return partes[:300], partes
    gancho = " ".join(p["text"] for p in partes if p.get("offset", 0) < 10_000).strip()
    return gancho, " ".join(p["text"] for p in partes).strip()


def main():
    _, lista = http(REFS)
    fila = [r for r in lista if r.get("status") == "video" and r.get("link") and not r.get("analise", {}).get("criterio")]
    print(f"{len(fila)} marcadas como vídeo falado sem análise; faço até {MAX_POR_RODADA}")
    for r in fila[:MAX_POR_RODADA]:
        try:
            passou, motivo, d = medir(r["link"])
            an = {"autor": d.get("autor", ""), "criterio": ("APROVADA: " if passou else "BARRADA: ") + motivo}
            if passou:
                gancho, tudo = transcrever(r["link"])
                an["fala"] = gancho
                an["formato"] = "falado" if len(tudo) > 40 else "sem fala (confira: pode ser lofi ou meme)"
                an["legenda"] = tudo[:600]
            http(REFS, {"id": r["id"], "analise": an}, {"Content-Type": "application/json", "Authorization": f"Bearer {ROBO}"}, "POST")
            print(("✓" if passou else "✗"), r["link"], "|", an["criterio"], "|", an.get("fala", "")[:80])
        except Exception as e:
            print("falhou", r["link"], str(e)[:150])


if __name__ == "__main__":
    main()
