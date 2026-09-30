"""Aviso de notícia quente (30/09/2026).

Ele reclamou: saiu o Sonnet 5.5 e os agentes do ChatGPT e ninguém avisou. Roda 3x por dia
(07h, 15h e 21h) no GitHub Actions, lê só os canais OFICIAIS e grava em quentes.json o que é
lançamento novo. O quadro mostra no topo: "🔥 Saiu X · gravar hoje". Nada de crédito, nada de Mac.

Novidade = link que não estava em vistos.json. Some do aviso depois de 48 h.
"""
import json, os, re, urllib.request, xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone

UA = {"User-Agent": "Mozilla/5.0 (Macintosh) Chrome/124"}
FEEDS = [
    ("OpenAI", "https://openai.com/news/rss.xml"),
    ("Google", "https://blog.google/technology/ai/rss/"),
    ("Google DeepMind", "https://deepmind.google/blog/rss.xml"),
    ("Meta", "https://about.fb.com/news/feed/"),
]
# lançamento de produto ou modelo; política, parceria e pesquisa acadêmica ficam de fora
LANCAMENTO = re.compile(r"introduc|launch|announc|now available|rolling out|new model|release|meet |"
                        r"gpt|codex|chatgpt|claude|sonnet|opus|haiku|gemini|veo|imagen|llama|meta ai|agent",
                        re.I)
SO_IA = re.compile(r"\bai\b|llama|meta ai|gemini|agent|model", re.I)   # Meta e Google postam de tudo
VISTOS, QUENTES = "vistos.json", "quentes.json"


def ler(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read().decode("utf-8", "ignore")


def dos_feeds():
    for fonte, url in FEEDS:
        try:
            raiz = ET.fromstring(ler(url))
        except Exception as e:
            print("falhou", fonte, str(e)[:80]); continue
        for it in raiz.iter("item"):
            titulo = (it.findtext("title") or "").strip()
            link = (it.findtext("link") or "").strip()
            if not (titulo and link and LANCAMENTO.search(titulo)): continue
            if fonte in ("Meta", "Google") and not SO_IA.search(titulo): continue
            yield fonte, titulo, link


def da_anthropic():
    """A Anthropic não tem feed: página de modelo (/claude-*) é sempre lançamento; notícia passa no filtro."""
    try:
        s = ler("https://www.anthropic.com/news")
    except Exception as e:
        print("falhou Anthropic", str(e)[:80]); return
    for caminho in dict.fromkeys(re.findall(r'href="(/(?:claude-[a-z0-9-]+|news/[a-z0-9-]+))"', s)):
        nome = re.sub(r"(\d) (\d)", r"\1.\2", caminho.rsplit("/", 1)[-1].replace("-", " ")).title()
        if caminho.startswith("/claude-") or LANCAMENTO.search(nome):
            yield "Anthropic", nome, "https://www.anthropic.com" + caminho


def main():
    agora = datetime.now(timezone.utc)
    primeira = not os.path.exists(VISTOS)
    vistos = set(json.load(open(VISTOS))) if not primeira else set()
    quentes = json.load(open(QUENTES)) if os.path.exists(QUENTES) else []
    novos = []
    for fonte, titulo, link in [*dos_feeds(), *da_anthropic()]:
        if link in vistos: continue
        vistos.add(link)
        if not primeira:        # 1ª rodada só aprende o que já existia, não avisa o passado inteiro
            novos.append({"fonte": fonte, "titulo": titulo, "link": link, "visto_em": agora.isoformat(timespec="minutes")})
    corte = (agora - timedelta(days=7)).isoformat()
    quentes = [q for q in novos + quentes if q["visto_em"] >= corte]
    json.dump(sorted(vistos), open(VISTOS, "w"), ensure_ascii=False, indent=0)
    json.dump(quentes, open(QUENTES, "w"), ensure_ascii=False, indent=1)
    print(f"{len(novos)} novidade(s)" + ("" if not primeira else " (1ª rodada: só aprendi o que já existia)"))
    for q in novos: print(" 🔥", q["fonte"], "|", q["titulo"], "|", q["link"])


if __name__ == "__main__":
    main()
