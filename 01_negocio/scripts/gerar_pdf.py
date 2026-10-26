import sys, os, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dados_ligar import LIGAR
from dados_concorrentes import CONCORRENTES, OPORTUNIDADES

DIR = os.path.dirname(os.path.abspath(__file__))
e = html.escape

def ul(items):
    return "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"

def table(headers, rows, cls=""):
    h = "".join(f"<th>{x}</th>" for x in headers)
    b = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<table class="{cls}"><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table>'

order = {"REF": 0, "A": 1, "B": 2, "C": 3}
ligar = sorted(LIGAR, key=lambda x: (order[x[0]], x[3]))

def ligar_rows(prio):
    out = []
    for i, r in enumerate(ligar, 1):
        p, emp, cid, km, tipo, oque, tel, wpp, site, conf, porque, fonte = r
        if p != prio:
            continue
        contato = e(tel) + (f"<br><b>WhatsApp:</b> {e(wpp)}" if wpp else "")
        out.append([str(i), f"<b>{e(emp)}</b><br><span class='muted'>{e(tipo)}</span>",
                    f"{e(cid)}<br><span class='muted'>~{km} km</span>", contato,
                    e(site), e(oque) + "<br><i>→ " + e(porque) + "</i>", e(conf)])
    return out

LH = ["Nº", "Empresa", "Cidade", "Telefone / WhatsApp", "E-mail / site", "O que fazem → por que ligar", "Confiança"]

conc_rows = [[f"<b>{e(c[1])}</b><br><span class='muted'>{e(c[4])}</span>",
              f"{e(c[2])}<br><span class='muted'>~{c[3]} km</span>",
              e(c[5]) + f"<br><span class='muted'>{e(c[6])}</span>",
              e(c[7]) + f"<br><span class='muted'>{e(c[8])}</span>",
              e(c[9]), "<b>+</b> " + e(c[10]) + "<br><b>−</b> " + e(c[11])] for c in CONCORRENTES]
CH = ["Empresa / perfil", "Cidade", "Serviços / materiais", "Contato / presença online", "Como vendem", "Forte / fraco"]

oport = "".join(f"<h3>{e(t)}</h3>" + ul([e(i) for i in its]) for t, its in OPORTUNIDADES)

fontes = sorted({r[11] for r in LIGAR if r[11].startswith("http")} | {c[12] for c in CONCORRENTES if c[12].startswith("http")} | {
    "https://www.mfrural.com.br/busca/pp-moido",
    "https://www.mfrural.com.br/busca/plasticos-reciclados",
    "https://www.spglobal.com/energy/en/news-research/latest-news/chemicals/053025-brazils-r-pet-flake-to-virgin-spread-turns-negative-prompts-recyclers-to-raise-june-rates",
    "https://www.afipol.org.br/afipol_associados.php",
    "https://www.enfplastic.com",
})

HTML = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Empresa de Polímeros: Resumo do Projeto</title>
<style>
@page {{ size: A4; margin: 16mm 14mm 16mm 14mm; }}
@page wide {{ size: A4 landscape; margin: 12mm 10mm; }}
.wide {{ page: wide; }}
body {{ font-family: Arial, Helvetica, sans-serif; font-size: 10.5pt; color: #1a1a1a; line-height: 1.42; }}
h1 {{ color: #1F4E78; font-size: 24pt; margin: 0 0 6px; }}
h2 {{ color: #fff; background: #1F4E78; padding: 6px 10px; font-size: 14pt; margin: 22px 0 10px; break-after: avoid; }}
h3 {{ color: #1F4E78; font-size: 11.5pt; margin: 14px 0 6px; break-after: avoid; }}
p {{ margin: 6px 0; }}
ul {{ margin: 4px 0 8px 18px; padding: 0; }} li {{ margin: 2px 0; }}
table {{ border-collapse: collapse; width: 100%; margin: 6px 0 12px; font-size: 9.5pt; }}
th {{ background: #DDEBF7; color: #1F4E78; text-align: left; padding: 5px; border: 1px solid #BFBFBF; }}
td {{ padding: 4px 5px; border: 1px solid #D0D0D0; vertical-align: top; }}
tr {{ break-inside: avoid; }}
table.small {{ font-size: 8pt; }}
.muted {{ color: #666; font-size: 90%; }}
.box {{ border: 2px solid #1F4E78; background: #F3F8FC; padding: 10px 14px; margin: 10px 0; }}
.warn {{ border-left: 4px solid #C00000; background: #FDF0F0; padding: 8px 12px; margin: 8px 0; }}
.cover {{ border-bottom: 3px solid #1F4E78; padding-bottom: 10px; margin-bottom: 10px; }}
.toc li {{ margin: 1px 0; }}
.break {{ break-before: page; }}
code {{ background: #eee; padding: 1px 4px; }}
</style></head><body>

<div class="cover">
<h1>Empresa de Polímeros: Resumo do Projeto</h1>
<p><b>Moagem de aparas plásticas (fita de embalagem) · Boituva-SP</b><br>
<span class="muted">Compilado de toda a conversa com o Claude · outubro de 2026</span></p>
</div>

<div class="box">
<h3 style="margin-top:0">📌 Para o Claude (nova conversa): contexto do projeto</h3>
<ul>
<li><b>Quem:</b> Gabriel quer abrir uma empresa de moagem de plástico com o pai, em <b>Boituva-SP</b>. O papel do Gabriel é <b>comercial: fazer contato com empresas</b> que contratariam o serviço.</li>
<li><b>Ativo:</b> o pai já tem um <b>pré-picador + picador de esteira</b> (joga o fardo inteiro → túnel → pré-pica → segundo picador → até 2 mm → big bag). Capacidade: <b>até 4 t/dia</b>.</li>
<li><b>Oportunidade inicial:</b> o pai tem contato com uma empresa que gera <b>~100 t/mês de fita</b> e procura alguém para cortar/picar.</li>
<li><b>Plano:</b> 1º ano só <b>prestando serviço de moagem</b>; depois avaliar comprar apara e vender moído/granulado.</li>
<li><b>Já feito:</b> estudo de materiais, custos, equipe, parte legal; lista de 48 empresas para ligar; mapeamento de 17 concorrentes; roteiro de ligação; planilha Excel de prospecção.</li>
<li><b>Em aberto:</b> confirmar o nome exato da "MM Plást" (Indaiatuba) e da "empresa de Monte Mor"; descobrir preço de mercado do serviço (R$/kg); confirmar a capacidade real da máquina com fita; começar as ligações.</li>
</ul>
</div>

<h3>Sumário</h3>
<ol class="toc">
<li>Anotações originais da ideia</li>
<li>Que fita é essa? Materiais e siglas</li>
<li>Outros materiais que podem ser processados</li>
<li>Capacidade e equipe</li>
<li>Custos estimados e preço</li>
<li>Parte legal e contrato</li>
<li>Perfil do cliente ideal</li>
<li>Lista de empresas para ligar (48)</li>
<li>Concorrentes (17)</li>
<li>Oportunidades e diferenciação</li>
<li>Roteiro de ligação</li>
<li>Próximos passos e pendências</li>
<li>Como continuar no Mac</li>
<li>Fontes</li>
</ol>

<h2>1. Anotações originais da ideia</h2>
<ul>
<li>Montar uma empresa de polímeros com o pai: matéria-prima = <b>fita de embalagem</b>, picada e trabalhada.</li>
<li>O pai tem o contato de uma empresa que gera <b>100 toneladas de fita por mês</b>; eles querem alguém para cortar as fitas.</li>
<li>O pai tem a máquina: <b>pré-picador + picador de esteira</b>. Joga o pacote inteiro, entra num túnel, pré-pica e cai em outro picador para finalizar em <b>2 mm</b>.</li>
<li>Fluxo: fardo → 1º picador → 2ª boca corta → <b>big bag</b> → empilhadeira → estoque.</li>
<li>Equipe pensada: <b>4 pessoas</b>. Funções citadas: um atende a máquina; um carrega/descarrega caminhão e manuseia bag.</li>
<li>Materiais citados: "PPL, PPE, PED" (interpretado como PP, PE, PEAD/PEBD). Todo plástico é polímero.</li>
<li>Plano: <b>1 ano prestando serviço</b> para quem só quer que pique as fitas.</li>
</ul>

<h2>2. Que fita é essa? Materiais e siglas</h2>
<p>"Fita de embalagem" pode ser três materiais bem diferentes. <b>Isso muda tudo.</b></p>
{table(["Tipo de fita", "Material", "Reciclagem"], [
 ["<b>Fita de arquear</b> (amarra fardos/paletes)", "PP, às vezes PET", "✅ Ótima: material limpo e de um tipo só"],
 ["<b>Ráfia / fita tecida</b> (sacaria, big bag)", "PP", "✅ Boa"],
 ["<b>Fita adesiva</b> (durex, fita marrom)", "BOPP + cola", "⚠️ Difícil: a cola contamina e pouca gente compra"],
])}
<p>Também perguntar: é <b>apara de fábrica</b> (sobra limpa, o melhor caso) ou <b>material já usado</b> (sujo, misturado)?</p>
{table(["Código", "Sigla", "Onde aparece"], [
 ["1", "<b>PET</b>", "Garrafas, fita de arquear PET, bandejas"],
 ["2", "<b>PEAD</b> (polietileno de alta densidade)", "Galões, bombonas, caixas, tampas"],
 ["4", "<b>PEBD / PELBD</b> (baixa densidade)", "Filme stretch, sacolas, filme encolhível"],
 ["5", "<b>PP</b> (polipropileno)", "Fita de arquear, ráfia, big bag, potes, para-choques"],
 ["6", "PS / EPS", "Isopor, copinhos"],
 ["3", "PVC", "Tubos, mangueiras (<b>evitar</b>: contamina os outros e solta cloro)"],
 ["7", "Outros", "ABS, PC (policarbonato), PA (nylon)"],
])}

<h2>3. Outros materiais que podem ser processados</h2>
<h3>Combinam com o maquinário atual (material flexível e longo)</h3>
<ul>
<li><b>Filme stretch de PEBD/PELBD</b>: o melhor vizinho da fita. Toda empresa que recebe palete gera. Muito volume e limpo.</li>
<li><b>Big bags e sacaria de ráfia PP</b>: mesma resina da fita.</li>
<li><b>Filme encolhível e sacos industriais de PE.</b></li>
<li><b>Fita de arquear PET</b>: vale mais, mas <b>nunca misturar com PP</b>; lote separado.</li>
<li><b>Fio / multifilamento de PP</b> (borra de fiação).</li>
</ul>
<h3>Precisariam de um moinho de facas (material rígido)</h3>
<ul><li>Bombonas e caixas de PEAD, paletes plásticos, peças de PP, borra/purga de injetoras, ABS e PC de eletrônicos.</li></ul>
<p><b>Regra de ouro:</b> cada resina num bag separado e etiquetado. Material misturado perde quase todo o valor.</p>

<h2>4. Capacidade e equipe</h2>
<ul>
<li>Máquina: <b>até 4 t/dia</b> → ~<b>88 t/mês</b> em 22 dias úteis.</li>
<li>A empresa do contato gera <b>100 t/mês</b>: a máquina sozinha <b>não cobre tudo</b>. Saídas: alguns sábados, turno estendido ou fechar um volume menor.</li>
<li>Um único cliente tomaria quase toda a capacidade → a lista de prospecção serve para <b>não depender de um só</b>.</li>
<li><b>Testar o 2 mm</b>: é fino para um picador (normal é 8–20 mm). Mais fino = mais energia e mais desgaste de faca. Confirmar com o cliente se 8–10 mm basta.</li>
</ul>
<h3>Equipe proposta (4 pessoas)</h3>
<ol>
<li><b>Alimentador</b>: abre o fardo e alimenta o pré-picador.</li>
<li><b>Operador da saída</b>: segundo picador, troca o bag cheio, pesa e etiqueta.</li>
<li><b>Empilhadeirista</b>: carga e descarga do caminhão, bag para o estoque, fardo para a máquina.</li>
<li><b>Líder de turno</b>: qualidade, manutenção (faca), controle de peso, cobre folgas.</li>
</ol>
<div class="warn"><b>Obrigatório:</b> <b>NR-12</b> (proteções, botão de emergência e intertravamento: picador é das máquinas que mais amputam no Brasil), <b>NR-11</b> (curso de empilhadeira) e EPIs (protetor auricular, luva anticorte, óculos).</div>

<h2>5. Custos estimados e preço</h2>
<p class="muted">Estimativas para ponto de partida: substituir pelos valores reais da região.</p>
{table(["Item", "Premissa", "R$/t (100 t/mês)"], [
 ["Mão de obra", "4 pessoas × ~R$ 4.000 de custo total", "~160"],
 ["Energia", "~100 kWh/t × R$ 0,80", "~80"],
 ["Galpão", "~R$ 10 mil/mês", "~100"],
 ["Empilhadeira (aluguel)", "~R$ 6 mil/mês", "~60"],
 ["Facas e manutenção", "-", "~40"],
 ["Big bags", "~2 bags/t (se o cliente não fornecer)", "~60"],
 ["Contador, seguros, outros", "-", "~50"],
 ["<b>Total</b>", "", "<b>~R$ 550/t ≈ R$ 0,55/kg</b>"],
])}
<ul>
<li>O serviço precisa ser cobrado <b>acima de ~R$ 0,55–0,60/kg</b> para dar lucro.</li>
<li><b>Nenhum concorrente publica preço de serviço por kg</b>: todos trabalham sob orçamento. Pedir orçamento como cliente comum (Nicoplas, Flex Ambiental, Gedel, Barrichello, Plasticosp, Alassia).</li>
<li>Referência de valor do material: <b>PP moído R$ 4–7/kg</b> em classificados; <b>flake PET ~R$ 6,90/kg</b> (SP, mai/2025); PET moído ~R$ 8,90/kg em anúncio.</li>
<li><b>Fase 2:</b> quem compra a apara e vende o moído (ou granula) ganha muito mais por kg. O ano de serviço serve para aprender e juntar caixa.</li>
</ul>

<h2>6. Parte legal e contrato</h2>
<ul>
<li><b>CNPJ</b> com CNAE <b>3832-7/00 – Recuperação de materiais plásticos</b>.</li>
<li><b>Licença ambiental</b> (CETESB em SP) e alvará da prefeitura.</li>
<li><b>AVCB dos Bombeiros</b>: estoque de plástico tem carga de incêndio alta.</li>
<li><b>MTR</b> (Manifesto de Transporte de Resíduos) no SINIR/SIGOR. Emitir <b>CDF (Certificado de Destinação Final)</b> é argumento de venda: o gerador precisa desse papel.</li>
<li><b>Nota fiscal:</b> serviço sobre material do cliente = <b>industrialização por encomenda</b>. No retorno: insumo volta com <b>CFOP 5.902</b> e o serviço é cobrado com <b>CFOP 5.124</b>, na mesma nota (SEFAZ-SP, RC 25345/2022). <b>Acertar com contador.</b></li>
</ul>
<h3>Contrato com a empresa das 100 t</h3>
<ul>
<li>Prazo de 12 meses e <b>volume mínimo</b> mensal.</li>
<li>Preço por kg e <b>como se pesa</b> (balança de quem?).</li>
<li>Quem paga o frete; quem fornece os bags; granulometria exigida.</li>
<li>Tolerância de <b>perda no processo</b> (normalmente 1–3%).</li>
<li>De quem é o material e quem responde em caso de incêndio no galpão.</li>
</ul>

<h2>7. Perfil do cliente ideal</h2>
<ul>
<li><b>Arqplast (Boituva)</b> não fabrica fita: é uma <b>recicladora grande</b> (Toyplast Plásticos Ltda). Compra fardos de PP/PE e faz baldes, bacias e caixas com 100% de reciclado; ~250 funcionários, +30 mil t/ano, triagem ótica própria. Tel. (15) 3268-9191.</li>
<li><b>MM Plást (Indaiatuba)</b>: não encontrada com esse nome. No polo de recicladoras do bairro Recreio Campestre Jóia há duas com nome parecido: <b>Megplast</b> e <b>Making Plast</b>. <i>Confirmar com o pai.</i></li>
<li><b>Empresa de Monte Mor</b>: há um anúncio no MF Rural de alguém em Monte Mor que mói exatamente sucata de <b>fita de arquear PET verde e PP branca</b>. Pode ser essa.</li>
<li><b>Conclusão:</b> o cliente ideal é <b>recicladora/granuladora de PP, PE e PET</b> (prioridade A). Depois: fábricas que geram apara de fita, ráfia, filme e fio (B) e aparistas/gestoras de resíduo (C).</li>
</ul>
<p><b>Por onde começar:</b> Mastrapet (Iperó), Odin Plast (Porto Feliz), Reciclagem Tietê, BCS (Sorocaba) e Dannaplas (Piracicaba, WhatsApp de Compras).</p>

<div class="wide">
<h2>8. Lista de empresas para ligar</h2>
<p class="muted">Telefones de sites e diretórios públicos (out/2026). "não verificado" = conferir no Google Maps. Distâncias aproximadas por estrada a partir de Boituva.</p>
<h3>Referências citadas</h3>
{table(LH, ligar_rows("REF"), "small")}
<h3>Prioridade A: recicladoras / granuladoras (mesmo perfil do cliente ideal)</h3>
{table(LH, ligar_rows("A"), "small")}
<h3>Prioridade B: fábricas que geram apara (fita, ráfia, filme, fio)</h3>
{table(LH, ligar_rows("B"), "small")}
<h3>Prioridade C: aparistas e gestoras de resíduo</h3>
{table(LH, ligar_rows("C"), "small")}

<h2>9. Concorrentes</h2>
<p>Quase ninguém na região vende <b>moagem pura por kg</b> como produto principal. Perfis: recicladores que compram apara; gestoras de resíduo (coleta + certificado); industrialização por encomenda (cliente manda apara, recebe granulado); moagem de nicho.</p>
{table(CH, conc_rows, "small")}
</div>

<h2>10. Oportunidades e diferenciação</h2>
{oport}
<div class="box"><b>Posicionamento sugerido:</b> "Especialistas em moagem de fita de arquear, ráfia e plástico flexível (PP, PE, PET) · moído padronizado até 2 mm · 4 t/dia · MTR + CDF · Boituva, no meio da região de Sorocaba." Criar Google Meu Negócio e WhatsApp comercial.</div>

<h2>11. Roteiro de ligação</h2>
<h3>Abertura (30 s)</h3>
<ul><li>"Bom dia, meu nome é ___, sou da ___, de Boituva. Com quem eu falo sobre aparas, resíduos ou compra de material reciclado?"</li>
<li>"Somos especializados em moagem de fita de arquear, ráfia e plástico flexível (PP, PE e PET). Moemos até 4 toneladas por dia, até 2 mm, entregamos em big bag."</li></ul>
<h3>Perguntas</h3>
<ul><li>Vocês geram ou compram apara de fita, ráfia ou filme? Quantas toneladas por mês?</li>
<li>Hoje quem mói? Fazem internamente ou terceirizam? A moagem está no limite?</li>
<li>Que granulometria, material (PP/PE/PET) e cor precisam?</li>
<li>Como vem o material (fardo, bobina, solto)? Quem faz o frete?</li>
<li>Precisam de MTR ou certificado de destinação (CDF)?</li></ul>
<h3>Proposta</h3>
<ul><li>Opção 1: mandam a apara e recebem o moído de volta (cobrança por kg).</li>
<li>Opção 2 (gerador): compramos ou retiramos a apara.</li>
<li>Oferecer <b>teste grátis</b> com lote pequeno (ex.: 500 kg).</li></ul>
<h3>Fechamento e dicas</h3>
<ul><li>"Posso mandar uma proposta por e-mail ou WhatsApp? Qual o melhor contato?" Anotar nome, cargo, volume e próximo passo.</li>
<li>Ligar 9h–11h30 ou 14h–16h30. Fábricas: pedir "resíduos" ou "meio ambiente". Recicladoras: "compras" ou "produção".</li>
<li>Sem interesse? "Conhece alguém que gera ou compra esse tipo de apara?"</li></ul>

<h2>12. Próximos passos e pendências</h2>
<h3>Perguntar à empresa das 100 t</h3>
<ol><li>Que fita é: arquear, ráfia ou adesiva? PP ou PET?</li><li>Apara de produção ou material usado?</li><li>Vem enfardada? Peso do fardo?</li><li>Por que querem picar e para onde vai o picado?</li><li>Quanto pagam hoje pelo serviço ou pelo descarte?</li></ol>
<h3>Confirmar com o pai</h3>
<ol><li>Quantos kg/h as máquinas fazem <b>com fita</b>.</li><li>Potência dos motores (energia).</li><li>Se as máquinas têm as proteções da NR-12.</li><li>Nome exato/CNPJ da "MM Plást" e da empresa de Monte Mor.</li></ol>
<h3>Comercial</h3>
<ol><li>Pedir orçamento a 3–5 concorrentes para descobrir o preço por kg.</li><li>Começar as ligações pela prioridade A mais próxima.</li><li>Montar planilha de viabilidade (custos × preço × volume) quando houver números reais.</li><li>Criar Google Meu Negócio + WhatsApp comercial.</li></ol>

<h2>13. Como continuar no Mac</h2>
<ul><li>Começar uma conversa nova no Claude e <b>anexar este PDF</b> (e a planilha <code>Lista_Prospeccao_Moagem_Boituva.xlsx</code>, se quiser editar a lista).</li>
<li>Alternativa: no terminal do Mac, clonar o repositório da sessão e rodar <code>claude --teleport</code> (traz o histórico, mas não os arquivos temporários).</li></ul>

<h2>14. Fontes</h2>
<ul class="small" style="font-size:8.5pt">{"".join(f"<li>{e(u)}</li>" for u in fontes)}</ul>
<p class="muted">Pesquisa feita com buscas na web e sites das empresas em outubro de 2026. Diretórios como Econodata, Solutudo e cnpj.biz bloquearam o acesso; podem existir empresas menores que não entraram na lista.</p>
</body></html>"""

with open(os.path.join(DIR, "resumo.html"), "w", encoding="utf-8") as f:
    f.write(HTML)
print("ok")
