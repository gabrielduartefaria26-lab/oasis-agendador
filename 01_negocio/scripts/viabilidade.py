import os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.comments import Comment
from openpyxl.formatting.rule import CellIsRule

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Viabilidade_Moagem_Castelo_Polimeros.xlsx")
F = "Arial"
BLUE = Font(name=F, size=10, color="0000FF")
BLK = Font(name=F, size=10)
BOLD = Font(name=F, size=10, bold=True)
GREEN = Font(name=F, size=10, color="008000")
TITLE = Font(name=F, size=14, bold=True, color="1F4E78")
SEC = Font(name=F, size=11, bold=True, color="FFFFFF")
SEC_FILL = PatternFill("solid", fgColor="1F4E78")
YEL = PatternFill("solid", fgColor="FFFF00")
OUT_FILL = PatternFill("solid", fgColor="E2EFDA")
thin = Side(style="thin", color="BFBFBF")
BRD = Border(left=thin, right=thin, top=thin, bottom=thin)
BRL = '"R$" #,##0;[Red]-"R$" #,##0;"-"'
BRL2 = '"R$" #,##0.00;[Red]-"R$" #,##0.00;"-"'
NUM = '#,##0;[Red]-#,##0;"-"'
NUM1 = '#,##0.0;[Red]-#,##0.0;"-"'
PCT = '0.0%;[Red]-0.0%;"-"'

wb = Workbook()
ws = wb.active
ws.title = "Premissas e Resultado"
ws.column_dimensions["A"].width = 46
ws.column_dimensions["B"].width = 16
ws.column_dimensions["C"].width = 70
ws["A1"] = "Viabilidade: serviço de moagem de aparas (Boituva-SP)"
ws["A1"].font = TITLE
ws["A2"] = "Altere só as células AMARELAS com texto AZUL. O resto é calculado. Valores iniciais são estimativas para ponto de partida."
ws["A2"].font = Font(name=F, size=9, italic=True)

names = {}
r = 4
def section(t):
    global r
    for c in range(1, 4):
        ws.cell(r, c).fill = SEC_FILL
    ws.cell(r, 1, t).font = SEC
    r += 1

def inp(key, label, val, fmt, note):
    global r
    ws.cell(r, 1, label).font = BLK
    c = ws.cell(r, 2, val); c.font = BLUE; c.fill = YEL; c.number_format = fmt; c.border = BRD
    ws.cell(r, 3, note).font = Font(name=F, size=9, color="595959")
    ws.cell(r, 3).alignment = Alignment(wrap_text=True)
    names[key] = f"$B${r}"
    r += 1

def calc(key, label, formula, fmt, note="", bold=False, hi=False):
    global r
    ws.cell(r, 1, label).font = BOLD if bold else BLK
    c = ws.cell(r, 2, formula.format(**names)); c.font = BOLD if bold else BLK; c.number_format = fmt; c.border = BRD
    if hi:
        c.fill = OUT_FILL
    ws.cell(r, 3, note).font = Font(name=F, size=9, color="595959")
    ws.cell(r, 3).alignment = Alignment(wrap_text=True)
    names[key] = f"$B${r}"
    r += 1

section("1. Volume e preço")
inp("cap_dia", "Capacidade da máquina (t/dia)", 4, NUM1, "Informado pelo usuário: até 4 t/dia.")
inp("dias", "Dias úteis por mês", 22, NUM, "Sábados extras aumentam a capacidade.")
calc("cap_mes", "Capacidade máxima (t/mês)", "={cap_dia}*{dias}", NUM1)
inp("vol", "Volume contratado (t/mês)", 80, NUM1, "Quanto os clientes mandam por mês. O contato do pai fala em 100 t/mês.")
calc("vol_ef", "Volume processado (t/mês)", "=MIN({vol},{cap_mes})", NUM1, "Limitado à capacidade da máquina.")
calc("ocup", "Ocupação da máquina", "=IF({cap_mes}>0,{vol_ef}/{cap_mes},0)", PCT)
inp("preco", "Preço do serviço (R$/kg)", 0.80, BRL2, "A DEFINIR: nenhum concorrente publica. Pedir orçamentos (Nicoplas, Flex, Gedel, Alassia).")
inp("imp", "Impostos sobre faturamento (%)", 0.10, PCT, "Estimativa (Simples Nacional, faixa inicial). Confirmar com contador.")
r += 1

section("2. Custos variáveis (por tonelada)")
inp("kwh_t", "Energia consumida (kWh/t)", 100, NUM, "Estimativa. Medir com a potência real dos motores do pai.")
inp("tarifa", "Tarifa de energia (R$/kWh)", 0.80, BRL2, "Conferir na conta de luz industrial (CPFL/Elektro).")
calc("energia_t", "Energia (R$/t)", "={kwh_t}*{tarifa}", BRL)
inp("facas_t", "Facas e manutenção (R$/t)", 40, BRL, "Estimativa. Fita e filme desgastam menos que rígido.")
inp("bags_t", "Big bags por tonelada", 2, NUM1, "Fita picada é leve (volumosa): ~400–600 kg por bag.")
inp("bag_preco", "Preço do big bag (R$)", 30, BRL, "Zere se o cliente fornecer o bag.")
calc("bag_t", "Big bags (R$/t)", "={bags_t}*{bag_preco}", BRL)
calc("var_t", "Custo variável total (R$/t)", "={energia_t}+{facas_t}+{bag_t}", BRL, "", True)
r += 1

section("3. Custos fixos (por mês)")
inp("func", "Número de funcionários", 4, NUM, "Alimentador, operador de saída, empilhadeirista, líder.")
inp("custo_func", "Custo por funcionário (R$/mês)", 4000, BRL, "Salário + encargos + benefícios. Estimativa.")
calc("mo", "Mão de obra (R$/mês)", "={func}*{custo_func}", BRL)
inp("aluguel", "Galpão (R$/mês)", 10000, BRL, "Zere se o galpão for próprio.")
inp("empilh", "Empilhadeira (R$/mês)", 6000, BRL, "Aluguel. Se comprar usada, zere aqui e coloque no investimento.")
inp("outros", "Contador, seguro, licenças, internet etc. (R$/mês)", 5000, BRL, "Estimativa.")
inp("prolabore", "Pró-labore dos sócios (R$/mês)", 0, BRL, "Quanto vocês dois vão tirar. Começa em zero.")
calc("fixos", "Custo fixo total (R$/mês)", "={mo}+{aluguel}+{empilh}+{outros}+{prolabore}", BRL, "", True)
r += 1

section("4. Investimento inicial")
inp("inv_nr12", "Adequação NR-12 das máquinas (R$)", 25000, BRL, "Proteções, intertravamento, emergência, laudo. Estimativa: cotar.")
inp("inv_legal", "Licenças, CETESB, AVCB, abertura (R$)", 15000, BRL, "Estimativa: cotar com despachante/consultoria ambiental.")
inp("inv_balanca", "Balança e instalação elétrica (R$)", 20000, BRL, "Estimativa.")
inp("inv_capital", "Capital de giro (R$)", 40000, BRL, "Para pagar ~2 meses de custos antes de receber.")
calc("inv", "Investimento total (R$)", "={inv_nr12}+{inv_legal}+{inv_balanca}+{inv_capital}", BRL, "Máquinas do pai não entram (já existem).", True)
r += 1

section("5. Resultado mensal")
calc("fat", "Faturamento bruto (R$/mês)", "={vol_ef}*1000*{preco}", BRL)
calc("imp_v", "(-) Impostos (R$/mês)", "={fat}*{imp}", BRL)
calc("var_v", "(-) Custos variáveis (R$/mês)", "={vol_ef}*{var_t}", BRL)
calc("fix_v", "(-) Custos fixos (R$/mês)", "={fixos}", BRL)
calc("lucro", "LUCRO MENSAL (R$)", "={fat}-{imp_v}-{var_v}-{fix_v}", BRL, "", True, True)
calc("margem", "Margem sobre faturamento", "=IF({fat}>0,{lucro}/{fat},0)", PCT, "", False, True)
calc("custo_kg", "Custo total por kg (R$/kg)", "=IF({vol_ef}>0,({var_v}+{fix_v})/({vol_ef}*1000),0)", BRL2,
     "Preço precisa ficar acima disto + impostos.", False, True)
calc("pe_t", "Ponto de equilíbrio (t/mês)", "=IF({preco}*1000*(1-{imp})-{var_t}>0,{fixos}/({preco}*1000*(1-{imp})-{var_t}),0)", NUM1,
     "Volume mínimo por mês para não ter prejuízo.", True, True)
calc("pe_preco", "Preço mínimo no volume atual (R$/kg)", "=IF({vol_ef}>0,({fixos}/{vol_ef}+{var_t})/1000/(1-{imp}),0)", BRL2,
     "Abaixo disto, dá prejuízo no volume informado.", True, True)
calc("payback", "Retorno do investimento (meses)", "=IF({lucro}>0,{inv}/{lucro},0)", NUM1, "Zero = não se paga (lucro negativo).", False, True)
ws.conditional_formatting.add(names["lucro"].replace("$", ""), CellIsRule(operator="lessThan", formula=["0"], fill=PatternFill("solid", fgColor="F8CBAD")))
ws.freeze_panes = "A4"

# ---------- Sensibilidade ----------
s = wb.create_sheet("Sensibilidade")
s["A1"] = "Lucro mensal (R$) por preço × volume"
s["A1"].font = TITLE
s["A2"] = "Usa custos da aba 'Premissas e Resultado'. Vermelho = prejuízo. Volume acima da capacidade é limitado à capacidade."
s["A2"].font = Font(name=F, size=9, italic=True)
precos = [0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00, 1.20]
vols = [20, 30, 40, 50, 60, 70, 80, 88, 100]
s.cell(4, 1, "Volume (t/mês) ↓   Preço (R$/kg) →").font = BOLD
for j, p in enumerate(precos, 2):
    c = s.cell(4, j, p); c.font = BLUE; c.fill = YEL; c.number_format = BRL2; c.border = BRD
for i, v in enumerate(vols, 5):
    c = s.cell(i, 1, v); c.font = BLUE; c.fill = YEL; c.number_format = NUM; c.border = BRD
    for j in range(2, 2 + len(precos)):
        col = s.cell(4, j).column_letter
        P = "'Premissas e Resultado'!"
        f = (f"=MIN($A{i},{P}{names['cap_mes']})*1000*{col}$4*(1-{P}{names['imp']})"
             f"-MIN($A{i},{P}{names['cap_mes']})*{P}{names['var_t']}-{P}{names['fixos']}")
        c = s.cell(i, j, f); c.number_format = BRL; c.font = GREEN; c.border = BRD
last_r = 4 + len(vols); last_c = s.cell(4, 1 + len(precos)).column_letter
s.conditional_formatting.add(f"B5:{last_c}{last_r}", CellIsRule(operator="lessThan", formula=["0"], fill=PatternFill("solid", fgColor="F8CBAD")))
s.conditional_formatting.add(f"B5:{last_c}{last_r}", CellIsRule(operator="greaterThanOrEqual", formula=["0"], fill=PatternFill("solid", fgColor="E2EFDA")))
s.column_dimensions["A"].width = 32
for j in range(2, 2 + len(precos)):
    s.column_dimensions[s.cell(4, j).column_letter].width = 13

# ---------- 12 meses ----------
m = wb.create_sheet("12 meses")
m["A1"] = "Projeção de 12 meses (ano de prestação de serviço)"
m["A1"].font = TITLE
m["A2"] = "Linha amarela = volume esperado em cada mês (rampa de clientes). Preço e custos vêm da aba de premissas."
m["A2"].font = Font(name=F, size=9, italic=True)
P = "'Premissas e Resultado'!"
m.cell(4, 1, "Mês").font = BOLD
rampa = [30, 45, 60, 70, 80, 80, 85, 88, 88, 88, 88, 88]
labels = ["Volume (t/mês)", "Volume processado (t)", "Faturamento (R$)", "(-) Impostos", "(-) Variáveis", "(-) Fixos",
          "Lucro do mês (R$)", "Caixa acumulado (R$)"]
for k, lab in enumerate(labels, 5):
    m.cell(k, 1, lab).font = BOLD if "Lucro" in lab or "Caixa" in lab else BLK
for j in range(12):
    col = m.cell(4, j + 2).column_letter
    m.cell(4, j + 2, j + 1).font = BOLD
    c = m.cell(5, j + 2, rampa[j]); c.font = BLUE; c.fill = YEL; c.number_format = NUM
    m.cell(6, j + 2, f"=MIN({col}5,{P}{names['cap_mes']})").number_format = NUM1
    m.cell(7, j + 2, f"={col}6*1000*{P}{names['preco']}").number_format = BRL
    m.cell(8, j + 2, f"=-{col}7*{P}{names['imp']}").number_format = BRL
    m.cell(9, j + 2, f"=-{col}6*{P}{names['var_t']}").number_format = BRL
    m.cell(10, j + 2, f"=-{P}{names['fixos']}").number_format = BRL
    m.cell(11, j + 2, f"=SUM({col}7:{col}10)").number_format = BRL
    prev = f"-{P}{names['inv']}" if j == 0 else f"{m.cell(12, j + 1).column_letter}12"
    m.cell(12, j + 2, f"={prev}+{col}11").number_format = BRL
    for k in range(5, 13):
        m.cell(k, j + 2).border = BRD
        if k > 5:
            m.cell(k, j + 2).font = BOLD if k >= 11 else BLK
m.cell(12, 1).comment = Comment("Começa com o investimento inicial negativo (mês 0) e soma o lucro de cada mês.", "Claude")
m.cell(14, 1, "Total do ano").font = BOLD
m.cell(14, 2, "=SUM(B11:M11)").number_format = BRL
m.cell(14, 2).font = BOLD
m.conditional_formatting.add("B11:M12", CellIsRule(operator="lessThan", formula=["0"], fill=PatternFill("solid", fgColor="F8CBAD")))
m.column_dimensions["A"].width = 24
for j in range(2, 14):
    m.column_dimensions[m.cell(4, j).column_letter].width = 12

for sh in wb.worksheets:
    for row in sh.iter_rows():
        for c in row:
            if c.font and c.font.name != F:
                c.font = Font(name=F, size=c.font.size, bold=c.font.bold, color=c.font.color, italic=c.font.italic)
wb.save(OUT)
print(OUT)
