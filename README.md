# Agendador da Oasis

Publica sozinho os Reels do `@system.oasis`, na hora marcada. Roda no GitHub Actions,
com o seu computador desligado. É o gêmeo do `cortes-agendador`, que cuida do
`@gabrieldfaria_`: código igual, agenda, token e histórico separados. Um não enxerga
nem atrapalha o outro.

## Como funciona

A cada 15 minutos a Action acorda, lê `agenda.json` e verifica se algum item já venceu
sem ter sido publicado. Se venceu, cria o container do Reel na API do Instagram, espera
o processamento terminar e publica. O resultado fica registrado em `estado.json`.

Publica no máximo um por execução. Se dois vencerem juntos por causa de atraso, o segundo
sai no ciclo seguinte.

## Arquivos

| Arquivo | O que é |
|---|---|
| `agenda.json` | Os itens: arquivo, data e hora, legenda |
| `videos/` | Os MP4. Não vão para o Git, vão para o Release |
| `publicar.py` | Conversa com a API do Instagram |
| `estado.json` | O que já foi publicado, com o id de cada post |

## Os três segredos

Em Settings, Secrets and variables, Actions:

| Nome | Valor |
|---|---|
| `IG_TOKEN` | O token do usuário do sistema que enxerga a Oasis |
| `IG_USER_ID` | `17841432343967660` |
| `VIDEOS_BASE_URL` | `https://github.com/gabrielduartefaria26-lab/oasis-agendador/releases/download/videos-v1` |

Cole os valores direto na tela do GitHub, ou rode `./configurar.sh` para o token.
Não passe token por mensagem, e-mail ou arquivo.

## O token, uma vez só

A conta `@system.oasis` é propriedade do Business **Money Machine**, e o usuário do
sistema `agendador` mora no Business **Gabriel D. Faria**. Token de usuário do sistema
não atravessa Business, então escolha um dos dois caminhos:

**Caminho A, reaproveitar o token que já existe.** No Money Machine, Configurações do
Negócio, Contas do Instagram, `@system.oasis`, botão **Atribuir parceiro**, ID
`477821146615870` com controle total. Depois, no Business Gabriel D. Faria, Usuários do
sistema, `agendador`, Adicionar ativos, marcar a conta com controle total. O mesmo token
do outro repo passa a servir aqui.

**Caminho B, token próprio da Oasis.** No Money Machine, Usuários do sistema, criar
`agendador-oasis`, dar a conta do Instagram como ativo com controle total e gerar token
pelo app, com `instagram_basic`, `instagram_content_publish`, `pages_show_list`,
`pages_read_engagement` e `business_management`. Mais independente, mais um token para
administrar.

Nos dois casos a conta do Instagram precisa estar vinculada a uma **Página do Facebook**.
Sem Página, a API de publicação não existe para ela.

## Subir os vídeos

```bash
gh release create videos-v1 videos/*.mp4 --title "Oasis" --notes "Lote 1"
```

O repositório precisa ser público para o Instagram conseguir baixar os arquivos.
Nenhum segredo fica no código: os tokens vivem nos Secrets, que não são expostos.

## Testar antes de confiar

Aba Actions, Run workflow com **Ensaio** marcado. Ele monta o container na Meta e para
antes de publicar: valida token, permissão e download do vídeo sem postar nada no perfil.

## Limites

- 50 publicações por conta a cada 24 horas.
- O vídeo precisa estar em URL pública no momento da publicação.
- Só Reel. Carrossel e imagem estática usam outro endpoint e hoje não estão aqui.
- A API não agenda nada: quem decide a hora é o cron daqui.
