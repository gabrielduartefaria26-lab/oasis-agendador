#!/bin/bash
# Roda a esteira de conteudo sem ninguem por perto. Chamado pelo launchd.
# Cada execucao deixa log em esteira/log/, inclusive quando da errado.
set -u
export PATH="$HOME/.local/npm-global/bin:$HOME/bin:/opt/homebrew/bin:/usr/local/bin:$PATH"

DIA=$(date +%Y-%m-%d)
LOG="$HOME/oasis-agendador/esteira/log/$DIA-execucao.log"
mkdir -p "$(dirname "$LOG")"

{
  echo "===== $(date '+%Y-%m-%d %H:%M:%S') ====="
  cd "$HOME/oasis-agendador" && git pull --quiet --rebase origin main 2>&1

  claude -p "Rode a esteira de conteudo do @system.oasis de hoje seguindo a skill esteira-oasis, do comeco ao fim, sem me perguntar nada. Se a fila estiver cheia ou se nenhuma pauta passar da regua, pare e me avise o motivo." \
    --permission-mode acceptEdits 2>&1

  echo "codigo de saida: $?"
} >> "$LOG" 2>&1

# rede de seguranca: se o claude morrer no meio, o Mac avisa mesmo assim
if ! tail -40 "$LOG" | grep -qi "fila\|pauta\|agendado\|geladeira"; then
  osascript -e 'display notification "A esteira rodou e nao deixou rastro. Confere o log." with title "Esteira Oasis" sound name "Basso"' 2>/dev/null
fi
