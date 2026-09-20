#!/bin/bash
# Roda a esteira de conteudo sem ninguem por perto. Chamado pelo launchd.
# Cada execucao deixa log em esteira/log/, inclusive quando da errado.
set -u
export PATH="$HOME/.local/npm-global/bin:$HOME/bin:/opt/homebrew/bin:/usr/local/bin:$PATH"

# O claude headless usa credencial propria, separada da do app. O token de longa
# duracao sai de `claude setup-token` e mora aqui, com permissao 600.
# Só usa o arquivo se ele tiver cara de token de verdade. Um arquivo com lixo
# sobrescreve a credencial boa do `claude login` e derruba tudo com "Invalid bearer
# token", que foi exatamente o que aconteceu na estreia.
TOKEN_ARQ="$HOME/.config/claude/oauth-token"
if [ -r "$TOKEN_ARQ" ]; then
  TOKEN="$(tr -d '[:space:]' < "$TOKEN_ARQ")"
  case "$TOKEN" in
    sk-ant-oat*) export CLAUDE_CODE_OAUTH_TOKEN="$TOKEN" ;;
    *) echo "aviso: $TOKEN_ARQ nao parece um token, ignorando e usando o login do CLI" ;;
  esac
fi
# variaveis do app confundem o CLI filho; fora daqui
unset ANTHROPIC_BASE_URL CLAUDECODE CLAUDE_CODE_SESSION_ID CLAUDE_CODE_CHILD_SESSION \
      CLAUDE_CODE_ENTRYPOINT CLAUDE_CODE_MESSAGING_SOCKET CLAUDE_CODE_MESSAGING_TOKEN 2>/dev/null || true

DIA=$(date +%Y-%m-%d)
LOG="$HOME/oasis-agendador/esteira/log/$DIA-execucao.log"
mkdir -p "$(dirname "$LOG")"

{
  echo "===== $(date '+%Y-%m-%d %H:%M:%S') ====="
  # trazer a agenda mais recente, sem deixar mudanca local travar a execucao
  cd "$HOME/oasis-agendador" || exit 1
  git stash --quiet --include-untracked 2>/dev/null
  git pull --quiet --rebase origin main 2>&1 || echo "aviso: nao consegui atualizar o repo, seguindo com o que tem em disco"
  git stash pop --quiet 2>/dev/null || true

  claude -p "Rode a esteira de conteudo do @system.oasis de hoje seguindo a skill esteira-oasis, do comeco ao fim, sem me perguntar nada. Se a fila estiver cheia ou se nenhuma pauta passar da regua, pare e me avise o motivo." \
    --permission-mode acceptEdits 2>&1

  echo "codigo de saida: $?"
} >> "$LOG" 2>&1

# rede de seguranca: se o claude morrer no meio, o Mac avisa mesmo assim
if ! tail -40 "$LOG" | grep -qi "fila\|pauta\|agendado\|geladeira"; then
  osascript -e 'display notification "A esteira rodou e nao deixou rastro. Confere o log." with title "Esteira Oasis" sound name "Basso"' 2>/dev/null
fi
