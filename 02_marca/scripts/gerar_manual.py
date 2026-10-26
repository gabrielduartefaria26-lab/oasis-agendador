import os, sys, subprocess, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from brand import *

BASE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.join(BASE, "Castelo_Polimeros_Kit")
IMG = lambda p: "file://" + os.path.join(KIT, p)

LEGENDAS = [
    ("01", "Seg · semana 1", "Chegou a Castelo Polímeros. 🏭\n\nSomos uma empresa familiar de Boituva, às margens da Castello Branco, especializada em moagem de fita de arquear, ráfia e plástico flexível.\n\nSua apara vira matéria-prima padronizada, sem você investir em máquina nem parar a produção.\n\n📲 Orçamento pelo WhatsApp: link na bio."),
    ("02", "Qua · semana 1", "O que a gente mói:\n\n▪ Fita de arquear PP e PET\n▪ Ráfia, sacaria e big bag\n▪ Filme stretch, shrink e sacos de PE\n▪ Fio e borra de fiação de PP\n\nNosso equipamento recebe o fardo inteiro. Fita e filme enrolados, que travam moinho comum, são o nosso dia a dia."),
    ("03", "Sex · semana 1", "Capacidade de 4 toneladas por dia, granulometria até 2 mm e entrega em big bag identificado por lote.\n\nPP, PE e PET sempre separados. Seu material volta do jeito que entrou, só que moído."),
    ("04", "Seg · semana 2", "Como funciona, do fardo ao big bag:\n\n1. Avaliação: você conta material, volume e granulometria.\n2. Lote-piloto: moemos um teste para você aprovar.\n3. Programação: entrada e saída agendadas, com pesagem.\n4. Entrega: moído em big bag identificado, com nota de retorno."),
    ("05", "Qua · semana 2", "Dica de chão de fábrica: fita PP ou PET? 💧\n\nColoque um pedaço na água. O PP é mais leve que a água (densidade ~0,9) e boia. O PET (~1,38) afunda. A fita PET também costuma ser verde e mais rígida.\n\nSalve para mostrar para a equipe."),
    ("06", "Sex · semana 2", "Por que a gente nunca mistura resinas?\n\nO PP derrete por volta de 165 °C e o PET por volta de 250 °C. Na extrusora, o PET não derrete junto e vira impureza no produto.\n\nPor isso cada resina e cada cliente têm o próprio big bag."),
    ("07", "Seg · semana 3", "Antes de mandar seu material:\n\n✅ Aceitamos: fita de arquear PP e PET, ráfia e big bag, filme stretch e shrink, fio de PP.\n❌ Não aceitamos: PVC, fita adesiva com cola, material sujo ou misturado.\n\nFicou em dúvida? Manda uma foto no WhatsApp."),
    ("08", "Qua · semana 3", "Boituva fica no meio do caminho da indústria: 15 km de Cerquilho, 45 km de Sorocaba, 50 km de Itu, 70 km de Indaiatuba e menos de 100 km de Campinas e Piracicaba.\n\nFrete curto é custo menor para você."),
    ("09", "Sex · semana 3", "Teste antes de fechar. 🤝\n\nMoemos um lote-piloto de até 500 kg do seu material para você aprovar a qualidade antes de qualquer contrato.\n\n📲 Chama no WhatsApp: link na bio."),
]
HASHTAGS = ("#reciclagem #reciclagemdeplastico #moagemdeplastico #fitadearquear #rafia #filmestretch "
            "#polipropileno #economiacircular #industria #boituva #sorocaba #regiaodesorocaba")

# legendas também em .txt no kit
with open(os.path.join(KIT, "instagram", "legendas.txt"), "w", encoding="utf-8") as f:
    for n, quando, txt in LEGENDAS:
        f.write(f"===== POST {n} ({quando}) =====\n{txt}\n\n{HASHTAGS}\n\n")

e = lambda s: s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

posts_html = "".join(
    f'<div class="pc"><img src="{IMG(f"instagram/posts/post-{n}.png")}"><div><div class="mono">POST {n} · {quando}</div>'
    f'<div class="cap">{e(txt).replace(chr(10), "<br>")}</div></div></div>' for n, quando, txt in LEGENDAS)

destaques = "".join(
    f'<div class="hl"><div class="circ"><img src="{IMG(f"instagram/destaques/destaque-{k}.png")}"></div><span>{t}</span></div>'
    for k, t in [("servicos", "Serviços"), ("materiais", "Materiais"), ("processo", "Como funciona"), ("regiao", "Região"), ("contato", "Contato")])

def fase(titulo, quando, itens):
    lis = "".join(f'<li><span class="box"></span><div><b>{a}</b>{" · " + b if b else ""}</div></li>' for a, b in itens)
    return f'<div class="fase"><div class="fh"><h3>{titulo}</h3><span class="mono">{quando}</span></div><ul class="chk">{lis}</ul></div>'

checklist = "".join([
    fase("1. Decisões da família", "Semana 1–2", [
        ("Nome final", "pesquisar no INPI (busca.inpi.gov.br) e na Junta Comercial antes de imprimir qualquer coisa"),
        ("Sociedade pai + filho", "percentual de cada um, quem é administrador, pró-labore"),
        ("Galpão", "confirmar com a prefeitura se o zoneamento permite indústria de reciclagem (consulta de viabilidade)"),
        ("Contador", "de preferência com experiência em indústria e reciclagem"),
        ("Orçamento de abertura", "usar a planilha de viabilidade com números reais"),
    ]),
    fase("2. Formalização", "Semana 2–4", [
        ("CNPJ", "pela Junta Comercial / REDESIM, com contrato social"),
        ("CNAE principal 3832-7/00", "Recuperação de materiais plásticos"),
        ("CNAE secundário 4687-7/03", "Comércio atacadista de resíduos e sucatas não metálicos (para comprar e vender apara)"),
        ("Inscrição estadual (ICMS)", "necessária para a nota de industrialização por encomenda (CFOP 5.124 / 5.902)"),
        ("Regime tributário", "Simples Nacional ou outro, decidir com o contador"),
        ("Conta PJ", ""),
        ("Pedido de registro da marca no INPI", "logo + nome; classe de serviços de tratamento de materiais"),
    ]),
    fase("3. Licenças e segurança", "Mês 1–3", [
        ("Licença ambiental CETESB", "licença prévia, de instalação e de operação para a atividade de reciclagem"),
        ("AVCB ou CLCB do Corpo de Bombeiros", "estoque de plástico tem alta carga de incêndio"),
        ("Alvará de funcionamento da prefeitura", ""),
        ("Laudo NR-12 das máquinas", "proteções, intertravamento e botão de emergência"),
        ("PGR e PCMSO", "programas de segurança e saúde do trabalho; ASO dos funcionários"),
        ("Curso NR-11", "para o operador de empilhadeira"),
        ("Cadastro no SIGOR / MTR", "para emitir manifesto de transporte e certificado de destinação"),
        ("Seguro do galpão e do estoque", ""),
    ]),
    fase("4. Presença digital", "Pode começar já", [
        ("Domínio castelopolimeros.com.br", "registro.br, ~R$ 40/ano"),
        ("E-mail profissional", "contato@ e comercial@ (Google Workspace ou Zoho)"),
        ("WhatsApp Business", "foto, descrição, horário, catálogo com os 3 serviços, mensagem de saudação"),
        ("Instagram @castelopolimeros", "criar já para reservar o nome; publicar os posts só perto da operação"),
        ("Site no ar", "arquivo pronto na pasta site/; hospedagem grátis em Netlify ou GitHub Pages, ou Hostinger"),
        ("Google Meu Negócio", "depende de endereço; é o que coloca vocês no mapa de Boituva e região"),
        ("Página no LinkedIn", "compradores e gestores industriais estão lá"),
        ("Cadastros em vitrines do setor", "B2Blue, MF Rural, ENF Recycling"),
    ]),
    fase("5. Material físico", "Antes do 1º cliente", [
        ("Etiqueta de big bag", "modelo neste manual: cliente, resina, lote, peso, data"),
        ("Cartão de visita", "modelo neste manual"),
        ("Uniforme e EPI com logo", "camiseta, colete refletivo"),
        ("Placa da fachada", ""),
        ("Modelo de proposta comercial", "usar a apresentação de 2 páginas como base"),
        ("Modelo de contrato", "volume mínimo, preço/kg, pesagem, perda, frete, responsabilidade"),
    ]),
    fase("6. Lançamento comercial", "Com licença em mãos", [
        ("Ligações", "planilha com 48 empresas, começar pela prioridade A"),
        ("Pedir orçamento aos concorrentes", "descobrir o preço de mercado por kg"),
        ("Lote-piloto com o primeiro cliente", "foto e vídeo da máquina viram conteúdo"),
        ("Publicar os 9 posts", "3 por semana, na ordem 01 → 09"),
    ]),
])

HTML = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Castelo Polímeros: Manual da Marca</title>{FONTS}
<style>
@page {{ size: A4; margin: 0; }}
* {{ box-sizing: border-box; }}
body {{ margin: 0; font: 400 10.5pt/1.5 Barlow, Arial, sans-serif; color: {GRAFITE}; }}
.pg {{ width: 210mm; min-height: 297mm; padding: 16mm 16mm 14mm; position: relative; break-after: page; }}
.pg:last-child {{ break-after: auto; }}
.mono {{ font: 600 8pt 'IBM Plex Mono', monospace; letter-spacing: .1em; text-transform: uppercase; color: #5b6b78; }}
h1 {{ font: 800 54pt/0.9 'Barlow Condensed'; text-transform: uppercase; margin: 0; }}
h2 {{ font: 800 26pt/1 'Barlow Condensed'; text-transform: uppercase; color: {AZUL}; margin: 2mm 0 5mm; }}
h3 {{ font: 700 14pt/1.1 'Barlow Condensed'; text-transform: uppercase; color: {AZUL}; margin: 0; }}
p {{ margin: 0 0 3mm; max-width: 165mm; }}
.tape {{ height: 7mm; background: repeating-linear-gradient(-45deg,{AMBAR} 0 16px,{AZUL_ESC} 16px 26px); }}
.cover {{ background: {AZUL}; color: #fff; padding: 0; display: flex; flex-direction: column; }}
.cover .in {{ padding: 24mm 18mm; flex: 1; display: flex; flex-direction: column; justify-content: space-between; }}
.cover .mono {{ color: {AMBAR}; }}
.grid2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 6mm; }}
.grid3 {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 5mm; }}
.tile {{ border-radius: 3mm; padding: 6mm; display: grid; place-items: center; min-height: 42mm; }}
.sw {{ border-radius: 2mm; overflow: hidden; border: 1px solid #dde3e8; }}
.sw div:first-child {{ height: 26mm; }}
.sw div:last-child {{ padding: 3mm; font-size: 9pt; }}
.sw b {{ display: block; font: 700 12pt 'Barlow Condensed'; text-transform: uppercase; }}
table {{ width: 100%; border-collapse: collapse; font-size: 9.5pt; }}
td, th {{ text-align: left; padding: 2mm; border-bottom: 1px solid #dde3e8; vertical-align: top; }}
th {{ font: 600 8pt 'IBM Plex Mono'; text-transform: uppercase; color: #5b6b78; }}
.do li::marker {{ content: "✓  "; color: {VERDE}; }} .dont li::marker {{ content: "✕  "; color: #B23B3B; }}
ul {{ margin: 0; padding-left: 5mm; }} li {{ margin: 1mm 0; }}
.pc {{ display: grid; grid-template-columns: 34mm 1fr; gap: 5mm; padding: 3mm 0; border-bottom: 1px solid #dde3e8; break-inside: avoid; }}
.pc img {{ width: 34mm; border-radius: 1mm; }}
.cap {{ font-size: 8.8pt; line-height: 1.4; margin-top: 1mm; }}
.hls {{ display: flex; gap: 7mm; }}
.hl {{ display: grid; justify-items: center; gap: 2mm; font-size: 9pt; }}
.circ {{ width: 22mm; height: 22mm; border-radius: 50%; overflow: hidden; border: 2px solid #dde3e8; }}
.circ img {{ width: 100%; height: 100%; object-fit: cover; }}
.phone {{ border: 2px solid {GRAFITE}; border-radius: 6mm; padding: 6mm 5mm; width: 78mm; }}
.fase {{ break-inside: avoid; margin-bottom: 5mm; }}
.fh {{ display: flex; justify-content: space-between; align-items: baseline; border-bottom: 2px solid {AMBAR}; padding-bottom: 1mm; margin-bottom: 1.5mm; }}
.chk {{ list-style: none; padding: 0; margin: 0; }}
.chk li {{ display: grid; grid-template-columns: 6mm 1fr; gap: 2mm; font-size: 9.5pt; margin: 1.3mm 0; }}
.box {{ width: 3.6mm; height: 3.6mm; border: 1.5px solid {AZUL}; border-radius: 1px; margin-top: 1mm; }}
.card {{ width: 85mm; height: 55mm; border-radius: 2mm; position: relative; overflow: hidden; box-shadow: 0 0 0 1px #dde3e8; }}
.label {{ border: 2px solid {GRAFITE}; width: 100%; font-size: 10pt; }}
.label td {{ border: 1px solid {GRAFITE}; padding: 2.5mm 3mm; }}
.label .k {{ font: 600 7.5pt 'IBM Plex Mono'; text-transform: uppercase; color: #5b6b78; display: block; }}
.label .v {{ font: 700 15pt 'Barlow Condensed'; text-transform: uppercase; min-height: 7mm; display: block; }}
.note {{ background: {CONCRETO}; padding: 4mm 5mm; border-radius: 2mm; font-size: 9.5pt; }}
.warn {{ border-left: 3px solid #B23B3B; background: #FBEFEF; padding: 3mm 4mm; font-size: 9.5pt; margin: 3mm 0; }}
</style></head><body>

<section class="pg cover">
  <div class="tape"></div>
  <div class="in">
    <div>{logo_html(BRANCO, BRANCO, AMBAR, 1.8)}</div>
    <div>
      <div class="mono">Manual da marca · plano de lançamento</div>
      <h1 style="margin-top:6mm">Montando o<br><span style="color:{AMBAR}">negócio.</span></h1>
      <p style="font-size:13pt;margin-top:8mm;opacity:.9;max-width:140mm">Identidade visual, Instagram, site e o checklist de tudo o que precisa existir antes do primeiro cliente.</p>
    </div>
    <div class="mono" style="color:#ffffffaa">Boituva-SP · outubro 2026 · versão 1</div>
  </div>
</section>

<section class="pg">
  <div class="mono">01 · Conceito</div>
  <h2>Por que Castelo Polímeros</h2>
  <p><b>Castelo</b> vem da Rodovia Castello Branco: Boituva está nela, e a maioria dos clientes da região (Sorocaba, Itu, Porto Feliz, Tatuí) também. O nome diz onde a empresa fica sem precisar explicar. <b>Polímeros</b> mostra que é indústria, não ferro-velho.</p>
  <p>O símbolo é uma torre de castelo feita de <b>faixas</b>, como fitas de arquear empilhadas, que se desfazem em <b>grãos</b> embaixo. É o serviço desenhado: a fita entra, o moído sai.</p>
  <div class="grid2" style="margin-top:8mm">
    <div class="tile" style="background:{CONCRETO}">{simbolo(AZUL, AMBAR, 150)}</div>
    <div class="tile" style="background:{AZUL}">{simbolo(BRANCO, AMBAR, 150)}</div>
  </div>
  <h3 style="margin-top:9mm">Posicionamento</h3>
  <div class="note" style="margin-top:2mm;font-size:12pt"><b>Especialistas em moagem de fita de arquear, ráfia e plástico flexível</b> (PP, PE, PET) · moído padronizado até 2 mm · 4 t/dia · Boituva, no meio da região industrial de Sorocaba.</div>
  <h3 style="margin-top:8mm">Para quem falamos</h3>
  <p style="margin-top:2mm">Comprador, gerente de produção e responsável por resíduos de recicladoras, granuladoras e fábricas que geram apara. Gente prática, que quer preço por kg, prazo e material sem contaminação.</p>
  <h3 style="margin-top:6mm">Tom de voz</h3>
  <div class="grid2" style="margin-top:2mm">
    <ul class="do"><li>Direto e técnico: kg, mm, t/dia, resina</li><li>Linguagem de chão de fábrica, sem enrolação</li><li>Prova concreta: pesagem, lote, teste</li><li>Educativo: dicas que o cliente usa no dia a dia</li></ul>
    <ul class="dont"><li>Prometer o que ainda não tem (licença, certificação)</li><li>"Sustentabilidade" genérica sem número</li><li>Gíria e excesso de emoji</li><li>Falar mal de concorrente</li></ul>
  </div>
</section>

<section class="pg">
  <div class="mono">02 · Logo</div>
  <h2>Versões do logo</h2>
  <div class="grid2">
    <div class="tile" style="background:#fff;box-shadow:0 0 0 1px #dde3e8">{logo_html(AZUL, AZUL, AMBAR, 1.15)}</div>
    <div class="tile" style="background:{AZUL}">{logo_html(BRANCO, BRANCO, AMBAR, 1.15)}</div>
    <div class="tile" style="background:{AMBAR}">{logo_html(AZUL_ESC, AZUL_ESC, BRANCO, 1.15)}</div>
    <div class="tile" style="background:{CONCRETO}">{logo_html(AZUL, AZUL, AMBAR, 1.15)}</div>
  </div>
  <table style="margin-top:6mm">
    <tr><th>Uso</th><th>Versão</th></tr>
    <tr><td>Fundo claro (padrão)</td><td>Azul com grãos âmbar · <span class="mono">logo/logo-horizontal.svg</span></td></tr>
    <tr><td>Fundo azul ou foto escura</td><td>Branco com grãos âmbar · <span class="mono">logo/logo-horizontal-branco.svg</span></td></tr>
    <tr><td>Fundo âmbar</td><td>Azul noite com grãos brancos</td></tr>
    <tr><td>Espaço pequeno (perfil, favicon, carimbo)</td><td>Só o símbolo · <span class="mono">logo/simbolo.svg</span></td></tr>
  </table>
  <h3 style="margin-top:7mm">Regras</h3>
  <div class="grid2" style="margin-top:2mm">
    <ul class="do"><li>Deixar em volta do logo um espaço livre do tamanho de uma "ameia" (o quadradinho do topo da torre)</li><li>Tamanho mínimo: 25 mm de largura no impresso, 120 px na tela</li></ul>
    <ul class="dont"><li>Esticar, inclinar ou mudar as cores</li><li>Colocar sobre foto poluída sem tarja</li><li>Trocar a fonte do nome</li></ul>
  </div>
</section>

<section class="pg">
  <div class="mono">03 · Cores e tipografia</div>
  <h2>Paleta</h2>
  <div class="grid3">
    <div class="sw"><div style="background:{AZUL}"></div><div><b>Azul Castelo</b>{AZUL} · principal</div></div>
    <div class="sw"><div style="background:{AMBAR}"></div><div><b>Âmbar Fita</b>{AMBAR} · destaque</div></div>
    <div class="sw"><div style="background:{AZUL_ESC}"></div><div><b>Azul Noite</b>{AZUL_ESC} · fundos escuros</div></div>
    <div class="sw"><div style="background:{CONCRETO}"></div><div><b>Concreto</b>{CONCRETO} · fundos claros</div></div>
    <div class="sw"><div style="background:{GRAFITE}"></div><div><b>Grafite</b>{GRAFITE} · texto</div></div>
    <div class="sw"><div style="background:{VERDE}"></div><div><b>Verde Ciclo</b>{VERDE} · "aceitamos", PET</div></div>
  </div>
  <p style="margin-top:4mm;font-size:9.5pt">O âmbar vem da fita de arquear e da faixa de sinalização da fábrica. Use como destaque (uma palavra, um número, a faixa listrada), nunca como fundo de texto longo.</p>
  <h2 style="margin-top:8mm">Fontes</h2>
  <table>
    <tr><th>Papel</th><th>Fonte</th><th>Exemplo</th></tr>
    <tr><td>Títulos</td><td>Barlow Condensed ExtraBold, maiúsculas</td><td style="font:800 22pt 'Barlow Condensed';color:{AZUL}">DO FARDO AO BIG BAG</td></tr>
    <tr><td>Texto</td><td>Barlow Regular / Medium</td><td>Moemos um lote-piloto para você aprovar a qualidade.</td></tr>
    <tr><td>Dados e rótulos</td><td>IBM Plex Mono</td><td style="font:600 11pt 'IBM Plex Mono'">4 t/dia · até 2 mm · PP/PE/PET</td></tr>
  </table>
  <p style="margin-top:3mm;font-size:9.5pt">As três são gratuitas no Google Fonts (fonts.google.com). No Canva, procure pelos mesmos nomes.</p>
  <h2 style="margin-top:8mm">Elemento gráfico: a faixa</h2>
  <div class="tape" style="height:10mm;border-radius:1mm"></div>
  <p style="margin-top:3mm">Listras diagonais âmbar e azul, como fita de arquear e faixa de segurança. Use no topo de posts, em placas, uniforme e na etiqueta do big bag.</p>
</section>

<section class="pg">
  <div class="mono">04 · Aplicações</div>
  <h2>Cartão de visita</h2>
  <div style="display:flex;gap:6mm;flex-wrap:wrap">
    <div class="card" style="background:{AZUL};color:#fff;display:grid;place-items:center">{logo_html(BRANCO, BRANCO, AMBAR, 1.0)}<div class="tape" style="position:absolute;left:0;right:0;bottom:0;height:4mm"></div></div>
    <div class="card" style="background:#fff;padding:6mm">
      <div style="font:800 15pt 'Barlow Condensed';color:{AZUL};text-transform:uppercase">Gabriel Faria</div>
      <div class="mono" style="margin-top:.5mm">Comercial</div>
      <div style="margin-top:6mm;font-size:9pt;line-height:1.55">(15) 9XXXX-XXXX · WhatsApp<br>gabriel@castelopolimeros.com.br<br>castelopolimeros.com.br · @castelopolimeros<br>Boituva-SP</div>
      <div style="position:absolute;right:5mm;top:5mm">{simbolo(AZUL, AMBAR, 34)}</div>
    </div>
  </div>
  <h2 style="margin-top:9mm">Etiqueta de big bag (A5)</h2>
  <p>Vai em todo bag que sai. É a prova de que o material não mistura e facilita a pesagem e a nota.</p>
  <div style="width:148mm;border:2px solid {GRAFITE}">
    <div style="display:flex;justify-content:space-between;align-items:center;padding:3mm 4mm;background:{AZUL}">{logo_html(BRANCO, BRANCO, AMBAR, .7)}<span style="font:800 20pt 'Barlow Condensed';color:{AMBAR}">LOTE Nº ______</span></div>
    <div class="tape" style="height:3mm"></div>
    <table class="label" style="border:0">
      <tr><td colspan="2"><span class="k">Cliente</span><span class="v"></span></td></tr>
      <tr><td><span class="k">Resina</span><span class="v">☐ PP &nbsp; ☐ PE &nbsp; ☐ PET</span></td><td><span class="k">Cor</span><span class="v"></span></td></tr>
      <tr><td><span class="k">Granulometria</span><span class="v">______ mm</span></td><td><span class="k">Peso líquido</span><span class="v">______ kg</span></td></tr>
      <tr><td><span class="k">Data da moagem</span><span class="v">___/___/____</span></td><td><span class="k">NF de retorno</span><span class="v"></span></td></tr>
    </table>
  </div>
  <h2 style="margin-top:9mm">Outros usos</h2>
  <ul><li><b>Uniforme:</b> camiseta azul com símbolo branco no peito e "CASTELO POLÍMEROS" nas costas; colete refletivo para o pátio.</li>
  <li><b>Fachada:</b> placa com logo branco sobre azul e a faixa listrada embaixo.</li>
  <li><b>Caminhão ou carro:</b> logo na porta e WhatsApp em letras grandes.</li>
  <li><b>Assinatura de e-mail:</b> nome, cargo, WhatsApp, site e o símbolo pequeno.</li></ul>
</section>

<section class="pg">
  <div class="mono">05 · Instagram</div>
  <h2>Perfil</h2>
  <div class="grid2" style="grid-template-columns:80mm 1fr;align-items:start">
    <div class="phone">
      <div style="display:flex;gap:4mm;align-items:center">
        <img src="{IMG('instagram/perfil/foto-perfil.png')}" style="width:20mm;height:20mm;border-radius:50%">
        <div><b style="font-size:11pt">castelopolimeros</b><div style="font-size:8.5pt;color:#5b6b78">Serviço de reciclagem</div></div>
      </div>
      <div style="font-size:9.3pt;line-height:1.45;margin-top:3mm"><b>Castelo Polímeros</b><br>♻️ Moagem de fita de arquear, ráfia e filme<br>⚙️ PP · PE · PET · até 2 mm · 4 t/dia<br>📍 Boituva-SP · Castello Branco<br>👇 Orçamento no WhatsApp<br><span style="color:#1a5fa8">castelopolimeros.com.br</span></div>
      <div class="hls" style="gap:3mm;margin-top:4mm;transform:scale(.62);transform-origin:left top;width:160%">{destaques}</div>
    </div>
    <div>
      <table>
        <tr><th>Item</th><th>O que colocar</th></tr>
        <tr><td>@ (usuário)</td><td><b>@castelopolimeros</b>. Reserve já. Alternativas: @castelo.polimeros, @castelopolimeros.sp</td></tr>
        <tr><td>Tipo de conta</td><td>Profissional · categoria "Serviço de reciclagem" ou "Empresa industrial"</td></tr>
        <tr><td>Foto</td><td><span class="mono">instagram/perfil/foto-perfil.png</span></td></tr>
        <tr><td>Bio</td><td>O texto ao lado (cabe nos 150 caracteres)</td></tr>
        <tr><td>Botões</td><td>WhatsApp + e-mail + endereço quando tiver</td></tr>
        <tr><td>Link</td><td>Site; ou link direto do WhatsApp até o site estar no ar</td></tr>
        <tr><td>Destaques</td><td>Serviços · Materiais · Como funciona · Região · Contato (capas em <span class="mono">instagram/destaques/</span>)</td></tr>
      </table>
      <div class="warn">Crie o perfil agora para reservar o nome, mas só publique quando a operação estiver perto de começar. Não anuncie licença ou certificado que ainda não existe.</div>
    </div>
  </div>
  <div style="display:grid;grid-template-columns:1fr 68mm;gap:8mm;margin-top:6mm;align-items:start">
   <div><h2 style="margin-top:0">Os 9 primeiros posts</h2>
   <p>Publique na ordem 01 → 09, três por semana (seg, qua, sex). Assim o post 09 (oferta) fica no topo do perfil e o grid fecha alternando as cores.</p>
   <p>Os posts estão prontos em <span class="mono">instagram/posts/</span>. Para criar novos, use as mesmas fontes, cores e a faixa listrada (dá para montar modelos no Canva).</p></div>
   <div><img src="file://{os.path.join(BASE, 'grid_preview.png')}" style="width:68mm;display:block;border:1px solid #dde3e8">
   <p class="mono" style="text-align:center;margin-top:2mm">Grid depois do post 09</p></div>
  </div>
</section>

<section class="pg">
  <div class="mono">05 · Instagram</div>
  <h2>Legendas e calendário</h2>
  <p style="font-size:9.5pt">Hashtags para todos os posts: <span class="mono" style="text-transform:none;letter-spacing:0">{HASHTAGS}</span>. Todas as legendas estão também em <span class="mono">instagram/legendas.txt</span> para copiar e colar.</p>
  {posts_html}
</section>

<section class="pg">
  <div class="mono">05 · Instagram</div>
  <h2>Depois dos 9 posts</h2>
  <table>
    <tr><th>Formato</th><th>Ideia</th><th>Frequência</th></tr>
    <tr><td><b>Reels</b></td><td>Vídeo do fardo entrando no pré-picador e saindo em grão no big bag (15–30 s, sem cortes). É o conteúdo mais forte que vocês têm: ninguém mostra isso.</td><td>1 por semana</td></tr>
    <tr><td><b>Reels</b></td><td>Antes e depois: foto do material do cliente (sem marca dele) e do moído na mão.</td><td>A cada lote novo</td></tr>
    <tr><td><b>Stories</b></td><td>Bastidores: chegada de caminhão, troca de faca, pesagem, equipe de EPI.</td><td>3–4 por semana</td></tr>
    <tr><td><b>Carrossel</b></td><td>Dicas técnicas: como enfardar fita para frete mais barato; PEAD x PEBD; por que a umidade atrapalha.</td><td>1 a cada 2 semanas</td></tr>
    <tr><td><b>Post</b></td><td>Números do mês: toneladas moídas, clientes atendidos (só com autorização).</td><td>Mensal</td></tr>
  </table>
  <div class="note" style="margin-top:5mm"><b>Regras de foto e vídeo:</b> sempre com EPI e proteções da máquina no lugar; nunca mostrar marca ou nome de cliente sem autorização; filmar na horizontal só para o site, para Instagram sempre na vertical.</div>

  <div class="mono" style="margin-top:10mm">06 · Site</div>
  <h2>Site</h2>
  <p>Página única com: ficha técnica, serviços, materiais aceitos e não aceitos, como funciona, diferenciais, região atendida e um formulário que monta a mensagem de orçamento e abre no WhatsApp.</p>
  <table>
    <tr><th>Passo</th><th>Como</th></tr>
    <tr><td>1. Registrar o domínio</td><td>registro.br → castelopolimeros.com.br (precisa de CPF ou CNPJ)</td></tr>
    <tr><td>2. Trocar os dados provisórios</td><td>No arquivo <span class="mono">site/index.html</span>: o número do WhatsApp (linha <span class="mono">const WHATSAPP</span>), o telefone, o e-mail e o endereço no rodapé</td></tr>
    <tr><td>3. Publicar</td><td>Grátis: arrastar a pasta <span class="mono">site/</span> em app.netlify.com/drop. Ou hospedagem paga (Hostinger, Locaweb)</td></tr>
    <tr><td>4. Ligar o domínio</td><td>Nas configurações da hospedagem, seguindo o passo a passo dela</td></tr>
    <tr><td>5. Google</td><td>Cadastrar no Google Meu Negócio e no Google Search Console</td></tr>
  </table>
</section>

<section class="pg">
  <div class="mono">07 · Checklist</div>
  <h2>Montando o negócio</h2>
  <p style="font-size:9.5pt">Na ordem em que as coisas dependem umas das outras. Prazos são estimativas e variam com a prefeitura e a CETESB. Confirmar os itens fiscais e de licença com o contador.</p>
  {checklist}
</section>

<section class="pg">
  <div class="mono">08 · Arquivos</div>
  <h2>O que tem no kit</h2>
  <table>
    <tr><th>Pasta</th><th>Arquivos</th><th>Para quê</th></tr>
    <tr><td class="mono">logo/</td><td>logo-horizontal (svg/png), versão branca, símbolo</td><td>Site, documentos, gráfica (SVG é o arquivo que a gráfica quer)</td></tr>
    <tr><td class="mono">instagram/perfil/</td><td>foto-perfil.png</td><td>Foto do Instagram, WhatsApp Business e Google</td></tr>
    <tr><td class="mono">instagram/posts/</td><td>post-01 a post-09 (1080×1350)</td><td>Os 9 posts de lançamento</td></tr>
    <tr><td class="mono">instagram/destaques/</td><td>5 capas (1080×1920)</td><td>Capas dos destaques</td></tr>
    <tr><td class="mono">instagram/legendas.txt</td><td>Legendas + hashtags</td><td>Copiar e colar</td></tr>
    <tr><td class="mono">site/index.html</td><td>Site completo em um arquivo</td><td>Publicar na hospedagem</td></tr>
  </table>
  <div class="note" style="margin-top:6mm"><b>Pendências antes de usar:</b> confirmar o nome no INPI · trocar WhatsApp, e-mail e endereço provisórios · revisar distâncias · só divulgar documentação ambiental (MTR/CDF) depois da licença CETESB.</div>
  <div style="position:absolute;left:16mm;right:16mm;bottom:16mm;display:flex;justify-content:space-between;align-items:center">{logo_html(AZUL, AZUL, AMBAR, .9)}<span class="mono">@castelopolimeros</span></div>
</section>
</body></html>"""

html_path = os.path.join(BASE, "manual.html")
with open(html_path, "w", encoding="utf-8") as f:
    f.write(HTML)
out = os.path.join(KIT, "Manual_da_Marca_Castelo_Polimeros.pdf")
subprocess.run([CHROME, "--no-sandbox", "--disable-gpu", "--virtual-time-budget=8000", "--no-pdf-header-footer",
                f"--print-to-pdf={out}", "file://" + html_path], capture_output=True, timeout=120)
print(out, os.path.exists(out))
