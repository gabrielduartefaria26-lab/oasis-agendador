#!/bin/bash
# Roda a esteira de conteudo sem ninguem por perto. Chamado pelo launchd.
# Cada execucao deixa log em esteira/log/, inclusive quando da errado.
set -u

# Carrossel pausado desde 23/09/2026 (4 posts somaram 17 de alcance com 17 seguidores).
# A esteira so produz carrossel, entao ela fica parada enquanto este arquivo existir.
# Para voltar: rm ~/oasis-agendador/esteira/PAUSADA
if [ -e "$HOME/oasis-agendador/esteira/PAUSADA" ]; then
  mkdir -p "$HOME/oasis-agendador/esteira/log"
  echo "$(date '+%Y-%m-%d %H:%M:%S') esteira pausada (esteira/PAUSADA existe), nada produzido" \
    >> "$HOME/oasis-agendador/esteira/log/$(date +%Y-%m-%d)-execucao.log"
  exit 0
fi
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

# Duas execucoes ao mesmo tempo brigam pelo mesmo agenda.json e pelo mesmo commit,
# e podem gerar post duplicado. A segunda desiste.
TRANCA="/tmp/oasis-esteira.lock"
if ! mkdir "$TRANCA" 2>/dev/null; then
  echo "$(date '+%H:%M:%S') ja existe uma esteira rodando, este disparo foi ignorado" >> "$LOG"
  osascript -e 'display notification "Ja tem uma esteira rodando. Este disparo foi ignorado." with title "Esteira Oasis"' 2>/dev/null
  exit 0
fi
trap 'rmdir "$TRANCA" 2>/dev/null' EXIT

{
  echo "===== $(date '+%Y-%m-%d %H:%M:%S') ====="
  # trazer a agenda mais recente, sem deixar mudanca local travar a execucao
  cd "$HOME/oasis-agendador" || exit 1
  git stash --quiet --include-untracked 2>/dev/null
  git pull --quiet --rebase origin main 2>&1 || echo "aviso: nao consegui atualizar o repo, seguindo com o que tem em disco"
  git stash pop --quiet 2>/dev/null || true

  # A esteira precisa das skills e da pasta de posts, que ficam fora do repo, e de
  # rodar python3 e node (regua, checadores, render, agendar-post). Sem isso ela para
  # no passo 2, que foi o que aconteceu na estreia.
  claude -p "Rode a esteira de conteudo do @system.oasis de hoje seguindo a skill esteira-oasis, do comeco ao fim, sem me perguntar nada. Se a fila estiver cheia ou se nenhuma pauta passar da regua, pare e me avise o motivo." \
    --add-dir "$HOME/.claude/skills" \
    --add-dir "$HOME/oasis-system" \
    --permission-mode acceptEdits 2>&1

  echo "codigo de saida: $?"
} >> "$LOG" 2>&1

# rede de seguranca: se o claude morrer no meio, o Mac avisa mesmo assim
if ! tail -40 "$LOG" | grep -qi "fila\|pauta\|agendado\|geladeira"; then
  osascript -e 'display notification "A esteira rodou e nao deixou rastro. Confere o log." with title "Esteira Oasis" sound name "Basso"' 2>/dev/null
fi
