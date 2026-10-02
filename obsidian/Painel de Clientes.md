# Painel de Clientes

> Precisa do plugin **Dataview** (Configurações → Plugins da comunidade → Dataview).
> Lê o `status`, `prazo` e `retrabalho` de todas as notas com a tag `#fluxo-cliente`.

## Progresso por cliente
```dataview
TABLE WITHOUT ID
  key AS "Cliente",
  length(filter(rows.status, (s) => s = "concluído")) + " / " + length(rows) AS "Etapas concluídas",
  join(map(filter(rows, (r) => r.status = "em andamento"), (r) => r.file.link), ", ") AS "Em andamento"
FROM #fluxo-cliente
GROUP BY cliente
SORT key ASC
```

## 🔴 Bloqueado ou 🟠 aguardando cliente
```dataview
TABLE WITHOUT ID cliente AS "Cliente", file.link AS "Etapa", status AS "Status", responsavel AS "Responsável", prazo AS "Prazo"
FROM #fluxo-cliente
WHERE status = "bloqueado" OR status = "aguardando cliente"
SORT prazo ASC
```

## ⏰ Atrasadas
```dataview
TABLE WITHOUT ID cliente AS "Cliente", file.link AS "Etapa", status AS "Status", responsavel AS "Responsável", prazo AS "Prazo"
FROM #fluxo-cliente
WHERE prazo AND prazo < date(today) AND status != "concluído"
SORT prazo ASC
```

## 🔁 Onde o processo mais volta (retrabalho)
Soma dos "Não" nos pontos de aprovação, por etapa, somando todos os clientes.
```dataview
TABLE WITHOUT ID key AS "Etapa", sum(rows.retrabalho) AS "Retrabalhos", length(rows) AS "Clientes"
FROM #fluxo-cliente
GROUP BY etapa
SORT sum(rows.retrabalho) DESC
```
