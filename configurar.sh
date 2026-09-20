#!/bin/bash
# Grava o token do Instagram da Oasis nos segredos do repositorio. O token e digitado
# aqui e vai direto para o GitHub: nao aparece na tela, nao fica no historico do shell.
set -e

REPO="gabrielduartefaria26-lab/oasis-agendador"
GH=$(command -v gh || echo "$HOME/bin/gh")
if [ ! -x "$GH" ]; then
  echo "Nao achei o gh. Procure com: ls ~/bin/gh /opt/homebrew/bin/gh /usr/local/bin/gh"
  exit 1
fi

echo "Cole o token do usuario do sistema e tecle Enter (nao vai aparecer na tela):"
read -rs TOKEN
echo

"$GH" secret set IG_TOKEN --body "$TOKEN" --repo "$REPO"
echo
echo "Pronto. Segredos do repositorio:"
"$GH" secret list --repo "$REPO"
