# Fluxo de Clientes — como usar

## Instalação (uma vez)
1. Copie o conteúdo desta pasta `obsidian/` para a raiz do seu vault.
2. Instale o plugin **Dataview** para o `Painel de Clientes` funcionar.

## Criar um cliente novo
No terminal, dentro do vault:
```
python3 novo-cliente.py "Nome do Cliente" --hub https://link-do-hub
```
Isso cria `Clientes/Nome do Cliente/` com uma nota por etapa + `Nome do Cliente - Fluxo.canvas`.
Se a pasta de clientes tiver outro nome: `--pasta "Projetos"`.

## No dia a dia
- **Abra o `.canvas`** do cliente para navegar pelo fluxo. Cada card é uma nota.
- **Mudou de status?** Troque o `status` na nota *e* a cor do card (botão direito → cor):
  - 🔵 não iniciado · 🟡 em andamento · 🟠 aguardando cliente · 🟢 concluído · 🔴 bloqueado
- **◆ Cards roxos** são aprovações do cliente. Se o cliente disse **Não**, siga a seta vermelha de volta,
  some 1 em `retrabalho` na nota da etapa e anote o motivo em *Falhas e aprendizados*.
- **Toda entrega** tem o item "Publicado no HUB" no checklist.
- O **Painel de Clientes** mostra o que está travado, atrasado e onde o processo mais volta.

## Ordem do fluxo
Onboarding → ◆ → Pesquisas (Público, Mercado, Concorrentes em paralelo) → ◆ → HUB →
Manual da Marca + Plano de Crescimento (em paralelo) → ◆ → Produto e Funis → ◆ →
Site/LP + Playbooks (em paralelo) → ◆ → Estratégia de Conteúdo → Orgânico + Anúncios →
Métricas e Revisão → volta para o Plano de Crescimento.
