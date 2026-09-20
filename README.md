# Agendador da Oasis

Publica sozinho os Reels, carrosséis e imagens do `@system.oasis`, na hora marcada. Roda no GitHub Actions,
com o seu computador desligado. É o gêmeo do `cortes-agendador`, que cuida do
`@gabrieldfaria_`: código igual, agenda, token e histórico separados. Um não enxerga
nem atrapalha o outro.

## Como funciona

A cada 15 minutos a Action acorda, lê `agenda.json` e verifica se algum item já venceu
sem ter sido publicado. Se venceu, cria o container na API do Instagram, espera
o processamento terminar e publica. O resultado fica registrado em `estado.json`.

Publica no máximo um por execução. Se dois vencerem juntos por causa de atraso, o segundo
sai no ciclo seguinte.

## Arquivos

| Arquivo | O que é |
|---|---|
| `agenda.json` | Os itens: arquivo, data e hora, legenda |
| `videos/` | Os MP4 e JPG. Não vão para o Git, vão para o Release |
| `publicar.py` | Conversa com a API do Instagram |
| `montar-carrossel.py` | Monta o item do carrossel com os slides na ordem certa |
| `estado.json` | O que já foi publicado, com o id de cada post |

## Os três formatos

O formato sai do próprio item, sem campo de configuração:

```json
[
  { "id": "reel-01",  "arquivo":  "corte.mp4",                       "quando": "...", "legenda": "..." },
  { "id": "foto-01",  "arquivo":  "post.jpg",                        "quando": "...", "legenda": "..." },
  { "id": "carro-01", "arquivos": ["s1.jpg", "s2.jpg", "s3.jpg"],    "quando": "...", "legenda": "..." }
]
```

`arquivos` é carrossel, de 2 a 10 imagens, na ordem escrita. `arquivo` sozinho é Reel
quando for `.mp4` e imagem quando for `.jpg`.

A ordem do carrossel é a ordem literal da lista: o primeiro nome é a capa. Para não
depender de digitação, monte a lista a partir da pasta dos slides:

```bash
python3 montar-carrossel.py ~/oasis-system/posts/1-manifesto/out \
    --quando "2026-09-25T09:00:00-03:00" --id manifesto-01
```

Ele ordena pelo número do nome, não por ordem alfabética, imprime a sequência para você
conferir e devolve o item pronto para colar na agenda. Ordenação alfabética colocaria o
`slide-10` logo depois do `slide-1`.

**A API só aceita JPEG.** Os slides saem do render em PNG, então converta antes de subir:

```bash
cd videos && for f in *.png; do sips -s format jpeg -s formatOptions 90 "$f" --out "${f%.png}.jpg"; done && rm *.png
```

Proporção entre 4:5 e 1.91:1. Os carrosséis da Oasis já saem em 1080x1350, que é 4:5.

Carrossel com vídeo dentro usa outro caminho na API e não está implementado aqui: o
agendador recusa com mensagem clara em vez de publicar errado.

## Os três segredos

Em Settings, Secrets and variables, Actions:

| Nome | Valor |
|---|---|
| `IG_TOKEN` | O token do usuário do sistema que enxerga a Oasis |
| `IG_USER_ID` | `17841432343967660` |
| `VIDEOS_BASE_URL` | `https://github.com/gabrielduartefaria26-lab/oasis-agendador/releases/download/videos-v1` (serve para MP4 e JPG) |

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

## Colocar um post novo na fila

Um comando, da pasta do post até a fila:

```bash
python3 agendar-post.py ~/oasis-system/posts/carrosseis/carrossel-x \
    --prefixo brasil-eua --quando "2026-09-24T09:00:00-03:00"
```

Ele converte os PNG em JPG, sobe no Release, insere na agenda na ordem certa e commita.
Use `--ensaio` para ver o que ele faria sem escrever nada.

**Quando não passar `--quando`, ele empilha no fim da fila**, um dia depois do último post
agendado. É o modo normal: produzir em lote com antecedência e deixar a fila correr na
frente da publicação.

```bash
python3 agendar-post.py <pasta> --prefixo x              # entra no fim da fila
python3 agendar-post.py <pasta> --prefixo x --urgente    # entra amanhã e empurra o resto
python3 agendar-post.py --fila                           # mostra o que está programado
```

**`--urgente` é para assunto quente**, o que perde valor se esperar. Ele entra no slot de
amanhã e empurra um dia cada post ainda não publicado. Nada se perde, tudo anda.

**Antes de subir, ele trava a entrega se:** a legenda reprovar no `checar-legenda.py` da
skill de carrossel, passar dos 2.200 caracteres do Instagram, começar com cabeçalho
interno, tiver travessão, o carrossel sair da faixa de 2 a 10 slides, ou o id já existir
na agenda.

**Se você editar uma legenda no disco depois de agendar**, a agenda fica com a versão
velha, porque ela guarda uma cópia do texto. Nesse caso é preciso ressincronizar.

## Subir os vídeos

```bash
gh release create videos-v1 videos/*.mp4 videos/*.jpg --title "Oasis" --notes "Lote 1"
```

O repositório precisa ser público para o Instagram conseguir baixar os arquivos.
Nenhum segredo fica no código: os tokens vivem nos Secrets, que não são expostos.

## Testar antes de confiar

Aba Actions, Run workflow com **Ensaio** marcado. Ele monta o container na Meta e para
antes de publicar: valida token, permissão e download do vídeo sem postar nada no perfil.

## Limites

- 50 publicações por conta a cada 24 horas.
- O vídeo precisa estar em URL pública no momento da publicação.
- Carrossel conta como uma publicação só, não como uma por slide.
- A API não agenda nada: quem decide a hora é o cron daqui.
