#!/usr/bin/env python3
"""Gera a pasta de um cliente no vault do Obsidian: notas de cada etapa + fluxograma (.canvas).

Uso:
    python3 novo-cliente.py "Nome do Cliente" [--hub URL] [--vault CAMINHO] [--pasta Clientes]

Por padrão o vault é a pasta onde este script está.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

STATUS = "não iniciado"  # não iniciado | em andamento | aguardando cliente | concluído | bloqueado

# Cores do Canvas: 1 vermelho, 2 laranja, 3 amarelo, 4 verde, 5 ciano, 6 roxo
COR_GATE = "6"
COR_SIM = "4"
COR_NAO = "1"

ETAPAS = [
    {
        "id": "onb", "arquivo": "00 Onboarding", "fase": "0 · Entrada",
        "depende": [],
        "objetivo": "Receber o cliente, entender o negócio e garantir tudo que o time precisa para começar.",
        "entregavel": "Briefing preenchido + acessos liberados",
        "checklist": [
            "Contrato assinado e pagamento confirmado",
            "Reunião de kickoff realizada",
            "Formulário de briefing respondido",
            "Acessos recebidos (Instagram, Meta Ads, Google, site, CRM)",
            "Materiais existentes recebidos (logo, fotos, apresentações)",
            "Grupo de comunicação criado",
            "Cronograma do projeto enviado ao cliente",
        ],
    },
    {
        "id": "pub", "arquivo": "01 Pesquisa de Público", "fase": "1 · Diagnóstico",
        "depende": ["onb"],
        "objetivo": "Entender quem compra, por que compra e o que impede a compra.",
        "entregavel": "Documento de persona / ICP",
        "checklist": [
            "Entrevistas ou formulário com clientes atuais",
            "Dores, desejos, objeções e gatilhos de compra mapeados",
            "Linguagem do público coletada (frases reais)",
            "Persona / ICP definido",
        ],
    },
    {
        "id": "mer", "arquivo": "02 Pesquisa de Mercado", "fase": "1 · Diagnóstico",
        "depende": ["onb"],
        "objetivo": "Dimensionar o mercado e identificar tendências e oportunidades.",
        "entregavel": "Relatório de mercado",
        "checklist": [
            "Tamanho e momento do mercado",
            "Tendências e sazonalidade",
            "Oportunidades e ameaças",
        ],
    },
    {
        "id": "con", "arquivo": "03 Pesquisa de Concorrentes", "fase": "1 · Diagnóstico",
        "depende": ["onb"],
        "objetivo": "Mapear como os concorrentes se posicionam, vendem e comunicam.",
        "entregavel": "Matriz de concorrentes",
        "checklist": [
            "Lista de concorrentes diretos e indiretos",
            "Oferta, preço e posicionamento de cada um",
            "Análise de conteúdo e anúncios (Biblioteca de Anúncios)",
            "Brechas de posicionamento identificadas",
        ],
    },
    {
        "id": "hub", "arquivo": "04 HUB", "fase": "2 · Fundação",
        "depende": ["pub", "mer", "con"],
        "objetivo": "Portal central do cliente: consolida as pesquisas e recebe cada entregável do projeto.",
        "entregavel": "HUB publicado (link)",
        "checklist": [
            "Página inicial do HUB (logo, frase da marca, versão)",
            "Pesquisas de público, mercado e concorrentes publicadas",
            "Um card por documento (Manual, Plano, Materiais Comerciais, Reuniões)",
            "Link do HUB enviado ao cliente",
            "Rotina: cada nova entrega e cada reunião é publicada no HUB",
        ],
    },
    {
        "id": "man", "arquivo": "05 Manual da Marca", "fase": "2 · Fundação",
        "depende": ["hub"],
        "objetivo": "Definir posicionamento, voz e identidade visual da marca.",
        "entregavel": "Manual da Marca",
        "checklist": [
            "Essência e posicionamento",
            "Inimigo declarado",
            "Público (a partir da pesquisa)",
            "Arquitetura de marca (marca principal e frentes pessoais)",
            "Logotipo, cores e tipografia",
            "Tom de voz",
            "Aplicações",
            "Limites legais da comunicação",
        ],
    },
    {
        "id": "pla", "arquivo": "06 Plano de Crescimento", "fase": "2 · Fundação",
        "depende": ["hub"],
        "objetivo": "Definir metas, canais e prioridades para o crescimento.",
        "entregavel": "Plano de Crescimento",
        "checklist": [
            "Onde estamos: números atuais (faturamento, ticket, origem das vendas, equipe)",
            "Diagnóstico principal em uma frase",
            "Alavancas de crescimento",
            "Primeiras ações, em ordem",
            "O que cabe à agência × o que cabe ao cliente",
            "Metas e preços validados pelo cliente",
        ],
    },
    {
        "id": "pro", "arquivo": "07 Produto e Funis de Vendas", "fase": "3 · Oferta",
        "depende": ["man", "pla"],
        "objetivo": "Estruturar a oferta e o caminho do lead até a compra.",
        "entregavel": "Oferta + desenho dos funis",
        "checklist": [
            "Produto / oferta principal definida",
            "Esteira de produtos (entrada, principal, recorrência)",
            "Funis desenhados etapa por etapa",
            "Precificação validada",
        ],
    },
    {
        "id": "lp", "arquivo": "08 Site - LP", "fase": "4 · Conversão",
        "depende": ["pro"],
        "objetivo": "Criar as páginas que convertem o tráfego em leads ou vendas.",
        "entregavel": "Site / LP no ar",
        "checklist": [
            "Copy da página",
            "Design aprovado",
            "Desenvolvimento e versão mobile",
            "Pixel, GA4 e eventos de conversão instalados",
            "Formulário / checkout testado",
        ],
    },
    {
        "id": "pb", "arquivo": "09 Playbooks Comerciais", "fase": "4 · Conversão",
        "depende": ["pro"],
        "objetivo": "Padronizar como o time comercial atende e fecha.",
        "entregavel": "Materiais Comerciais (scripts, playbooks, protocolo, planilha)",
        "checklist": [
            "Script de Atendimento (WhatsApp, até o agendamento)",
            "Script de Ligação",
            "Script de Reunião (do diagnóstico ao fechamento)",
            "Playbook de Social Selling",
            "Playbook de Rotina Comercial",
            "Protocolo de pós-venda (ex.: Conexão 30)",
            "Planilha de acompanhamento de leads (pasta no Drive)",
            "Treinamento do time comercial",
        ],
    },
    {
        "id": "est", "arquivo": "10 Estratégia de Conteúdo", "fase": "5 · Tração",
        "depende": ["lp", "pb"],
        "objetivo": "Definir o que comunicar, para quem e em qual canal.",
        "entregavel": "Estratégia de conteúdo",
        "checklist": [
            "Pilares de conteúdo",
            "Divisão orgânico × anúncios",
            "Calendário editorial",
        ],
    },
    {
        "id": "org", "arquivo": "10.1 Orgânico", "fase": "5 · Tração",
        "depende": ["est"],
        "objetivo": "Produzir e publicar o conteúdo orgânico.",
        "entregavel": "Conteúdos publicados",
        "checklist": [
            "Linha editorial aprovada",
            "Produção do mês",
            "Publicação agendada",
        ],
    },
    {
        "id": "ads", "arquivo": "10.2 Anúncios", "fase": "5 · Tração",
        "depende": ["est"],
        "objetivo": "Rodar campanhas pagas ligadas aos funis.",
        "entregavel": "Campanhas ativas",
        "checklist": [
            "Estrutura de campanhas",
            "Criativos produzidos",
            "Públicos configurados",
            "Campanhas no ar",
        ],
    },
    {
        "id": "met", "arquivo": "11 Métricas e Revisão", "fase": "6 · Loop",
        "depende": ["org", "ads"],
        "objetivo": "Medir os resultados e devolver os aprendizados para o Plano de Crescimento.",
        "entregavel": "Relatório mensal",
        "checklist": [
            "Relatório de resultados do mês",
            "Reunião de revisão com o cliente (apresentação publicada no HUB)",
            "Ajustes levados ao Plano de Crescimento",
        ],
    },
]

# Pontos de aprovação: (id, texto, depois de, segue para, se "Não" volta para o grupo)
GATES = [
    ("g1", "Briefing e acessos completos?", ["onb"], ["pub", "mer", "con"], "G0"),
    ("g2", "Cliente validou as pesquisas?", ["pub", "mer", "con"], ["hub"], "G1"),
    ("g3", "Manual e Plano aprovados?", ["man", "pla"], ["pro"], "G2"),
    ("g4", "Oferta e funis aprovados?", ["pro"], ["lp", "pb"], "G3"),
    ("g5", "LP e Playbooks aprovados?", ["lp", "pb"], ["est"], "G4"),
]

W, H = 360, 240          # tamanho dos cards de etapa
GW, GH = 240, 130        # tamanho dos cards de decisão
POS = {                  # posição (x, y) de cada card
    "onb": (0, -120),
    "g1": (440, -65),
    "pub": (760, -420), "mer": (760, -120), "con": (760, 180),
    "g2": (1200, -65),
    "hub": (1520, -120), "man": (1960, -270), "pla": (1960, 30),
    "g3": (2400, -65),
    "pro": (2720, -120),
    "g4": (3160, -65),
    "lp": (3480, -270), "pb": (3480, 30),
    "g5": (3920, -65),
    "est": (4240, -120), "org": (4680, -270), "ads": (4680, 30),
    "met": (5120, -120),
}
GRUPOS = [  # (id, rótulo, etapas dentro)
    ("G0", "0 · Entrada", ["onb"]),
    ("G1", "1 · Diagnóstico", ["pub", "mer", "con"]),
    ("G2", "2 · Fundação", ["hub", "man", "pla"]),
    ("G3", "3 · Oferta", ["pro"]),
    ("G4", "4 · Conversão", ["lp", "pb"]),
    ("G5", "5 · Tração", ["est", "org", "ads"]),
    ("G6", "6 · Loop", ["met"]),
]


def nid(*partes):
    return hashlib.md5("|".join(partes).encode()).hexdigest()[:16]


def caminho_nota(pasta_cliente, etapa):
    return f"{pasta_cliente}/{etapa['arquivo']}.md"


def link(pasta_cliente, etapa):
    return f"[[{pasta_cliente}/{etapa['arquivo']}|{etapa['arquivo']}]]"


def nota(cliente, pasta_cliente, etapa, por_id):
    deps = "\n".join(f"- {link(pasta_cliente, por_id[d])}" for d in etapa["depende"]) or "- (início do fluxo)"
    checklist = list(etapa["checklist"])
    if etapa["id"] not in ("onb", "hub"):
        checklist.append("Publicado no HUB")
    checklist = "\n".join(f"- [ ] {c}" for c in checklist)
    return f"""---
cliente: "{cliente}"
etapa: "{etapa['arquivo']}"
fase: "{etapa['fase']}"
status: {STATUS}
responsavel:
inicio:
prazo:
concluido:
entregavel:
retrabalho: 0
tags:
  - fluxo-cliente
---
# {etapa['arquivo']}

> **Objetivo:** {etapa['objetivo']}
> **Entregável:** {etapa['entregavel']}

## Depende de
{deps}

## Checklist
{checklist}

## Falhas e aprendizados
<!-- Anote o que travou ou deu errado. A cada "Não" num ponto de aprovação, some 1 em `retrabalho`. -->
-
"""


def canvas(cliente, pasta_cliente, hub_url, por_id):
    nodes, edges = [], []
    pad = 40

    for gid, rotulo, membros in GRUPOS:
        xs = [POS[m][0] for m in membros]
        ys = [POS[m][1] for m in membros]
        nodes.append({
            "id": nid(cliente, gid), "type": "group", "label": rotulo,
            "x": min(xs) - pad, "y": min(ys) - pad - 20,
            "width": max(xs) - min(xs) + W + 2 * pad,
            "height": max(ys) - min(ys) + H + 2 * pad + 20,
        })

    for e in ETAPAS:
        x, y = POS[e["id"]]
        nodes.append({
            "id": nid(cliente, e["id"]), "type": "file", "file": caminho_nota(pasta_cliente, e),
            "x": x, "y": y, "width": W, "height": H, "color": "5",
        })

    for gid, texto, _, _, _ in GATES:
        x, y = POS[gid]
        nodes.append({
            "id": nid(cliente, gid), "type": "text", "text": f"◆ **{texto}**",
            "x": x, "y": y, "width": GW, "height": GH, "color": COR_GATE,
        })

    hub = f"[{hub_url}]({hub_url})" if hub_url else "_(adicionar link)_"
    nodes.append({
        "id": nid(cliente, "cabecalho"), "type": "text",
        "text": f"# {cliente}\n\n**HUB:** {hub}\n\n"
                f"Clique em um card para abrir a etapa. Atualize o `status` na nota **e** a cor do card.",
        "x": 0, "y": -820, "width": 720, "height": 220,
    })
    nodes.append({
        "id": nid(cliente, "legenda"), "type": "text",
        "text": "### Legenda\n"
                "🔵 Não iniciado\n🟡 Em andamento\n🟠 Aguardando cliente\n"
                "🟢 Concluído\n🔴 Bloqueado / com erro\n🟣 ◆ Aprovação do cliente",
        "x": 760, "y": -820, "width": 360, "height": 260,
    })

    def edge(a, b, fs="right", ts="left", **extra):
        edges.append({"id": nid(cliente, "e", a, b), "fromNode": nid(cliente, a), "fromSide": fs,
                      "toNode": nid(cliente, b), "toSide": ts, **extra})

    # Ligações diretas entre etapas (sem ponto de aprovação no meio)
    for a, b in [("hub", "man"), ("hub", "pla"), ("est", "org"), ("est", "ads"), ("org", "met"), ("ads", "met")]:
        edge(a, b)

    # Pontos de aprovação: entrada, "Sim" e "Não"
    for gid, _, antes, depois, volta in GATES:
        for a in antes:
            edge(a, gid)
        for b in depois:
            edge(gid, b, label="Sim", color=COR_SIM)
        edge(gid, volta, fs="bottom", ts="bottom", label="Não → ajustar", color=COR_NAO)

    # Loop: métricas voltam para o plano
    edge("met", "pla", fs="top", ts="top", label="Revisão mensal → ajustar plano", color="3")

    return {"nodes": nodes, "edges": edges}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cliente")
    ap.add_argument("--hub", default="", help="link do HUB do cliente")
    ap.add_argument("--vault", default=str(Path(__file__).resolve().parent), help="pasta raiz do vault")
    ap.add_argument("--pasta", default="Clientes", help="pasta dos clientes dentro do vault")
    args = ap.parse_args()

    vault = Path(args.vault)
    pasta_cliente = f"{args.pasta}/{args.cliente}"
    destino = vault / pasta_cliente
    if destino.exists():
        sys.exit(f"Já existe: {destino} (nada foi alterado)")
    destino.mkdir(parents=True)

    por_id = {e["id"]: e for e in ETAPAS}
    for e in ETAPAS:
        (vault / caminho_nota(pasta_cliente, e)).write_text(nota(args.cliente, pasta_cliente, e, por_id), encoding="utf-8")

    dados = canvas(args.cliente, pasta_cliente, args.hub, por_id)
    (destino / f"{args.cliente} - Fluxo.canvas").write_text(
        json.dumps(dados, ensure_ascii=False, indent="\t"), encoding="utf-8")

    print(f"Criado: {destino}")


if __name__ == "__main__":
    main()
