# Castelo Polímeros: passagem de contexto

Resumo de tudo o que foi feito na conversa anterior com o Claude, para continuar o trabalho daqui.

## O negócio
- **Quem:** Gabriel e o pai vão abrir uma empresa de moagem de plástico em **Boituva-SP**. O papel do Gabriel é o comercial (contato com empresas).
- **Máquina (do pai):** pré-picador + picador de esteira em linha. Recebe o fardo inteiro, sai até **2 mm**, direto no big bag. Capacidade: **até 4 t/dia** (~88 t/mês).
- **Oportunidade inicial:** um contato do pai gera ~100 t/mês de fita e quer terceirizar o corte.
- **Plano:** 1º ano só prestando serviço de moagem; depois avaliar comprar apara e vender moído/granulado.
- **Cliente ideal (ICP):** recicladoras/granuladoras de PP, PE e PET (ex.: Arqplast, Boituva, que é recicladora, não fábrica de fita; "MM Plást", Indaiatuba, nome a confirmar: talvez Megplast ou Making Plast). Depois: fábricas que geram apara de fita, ráfia, filme e fio; e aparistas/gestoras de resíduo.
- **Números da viabilidade (estimativas):** custo ~R$ 0,64/kg com 88 t/mês; com R$ 0,80/kg e 80 t/mês o lucro fica em ~R$ 6,2 mil/mês; ponto de equilíbrio ~69 t/mês; caixa chega a ~-R$ 138 mil no 3º mês. **Preço de mercado do serviço ainda desconhecido** (nenhum concorrente publica).

## A marca
- **Nome:** Castelo Polímeros (da Rodovia Castello Branco). Domínio castelopolimeros.com.br estava livre em out/2026. **Falta checar no INPI.**
- **Logo:** torre de castelo feita de faixas (fitas) que se desfazem em grãos (o moído). Aprovado pelo Gabriel ("excelente").
- **Cores:** Azul Castelo #12385A · Azul Noite #0B2238 · fundo noturno #071629 · Âmbar Fita #F2A900 (+ âmbar claro #FFC93C nos gradientes) · Concreto #EEF1F4/#F3F6F9 · Grafite #17232D · Verde Ciclo #2F7D5B.
- **Fontes:** Barlow Condensed (títulos, maiúsculas), Barlow (texto), IBM Plex Mono (dados e rótulos). Todas do Google Fonts.
- **Elemento gráfico:** faixa listrada diagonal âmbar/azul (fita de arquear + faixa de segurança).
- **Preferências do Gabriel:** visual sofisticado no nível de https://cargobooking.com.br/novo/ (gradientes, fotos, cards de vidro, selos), **mas com a nossa identidade**; prefere **muito branco/respiro** (o site ficou pesado quando era todo escuro); header fixo **sólido** azul-noite; margens laterais generosas; mobile bem cuidado.

## O que existe nesta pasta
| Pasta | Conteúdo |
|---|---|
| `01_negocio/` | PDF-resumo completo da conversa, lista de 48 empresas para ligar + 17 concorrentes (xlsx), planilha de viabilidade (xlsx), apresentação comercial de 2 páginas (PDF) e os scripts que geram tudo |
| `02_marca/kit/` | Logos (SVG/PNG), Instagram (foto de perfil, 9 posts 1080×1350 com legendas em `legendas.txt`, 5 capas de destaque), manual da marca (PDF), site (`site/index.html`), vídeo mudo |
| `02_marca/fotos/` | 3 fotos geradas por IA no Gamma (esteira, mão com o moído, fardos de fita): **provisórias**, trocar por fotos reais da máquina |
| `02_marca/scripts/` | Geradores dos logos, posts, destaques e manual (Python + Chromium headless) |
| `03_video/` | Animação do processo em código (`castelo_anim.js` + `.css`), `video.html` (palco 1920×1080 para render), `render.js` (exporta MP4 com Playwright + ffmpeg), `castelo_mudo.mp4`, `roteiro_narracao_elevenlabs.txt` |
| `04_site/` | `site_fonte.html` (fonte com marcadores IMG_HERO, IMG_BALES, IMG_HAND e NARRACAO_SRC a substituir pelas fotos/áudio em base64) e `site_publicado_artifact.html` (versão completa publicada) |

**Site publicado (Artifact privado do Gabriel):** https://claude.ai/artifact/T3i2S22onev1ypBbBdaMtp

Seções do site, nesta ordem: header fixo → hero com foto → **vídeo animado (2ª dobra)** → serviços → "Faça a conta" (moagem interna × Castelo) → materiais → como funciona + ficha técnica (faixa escura) → região (barras de distância) → orçamento (formulário que monta mensagem de WhatsApp) → quem somos (história, card branco com logo, missão/visão/propósito, 4 valores, marcos) → FAQ (8 perguntas) → rodapé completo. Dados de contato, endereço, CNPJ, história e FAQ são **inventados/provisórios**.

## O vídeo animado
- 12 cenas em código (estilo inspirado no VSL de konesales.com.br: tipografia cinética com marca-texto, cenas escuras/claras, diagramas). Tudo é função do tempo (`CasteloAnim.mount(el)` → `renderAt(t)`), então o mesmo código toca no site e exporta MP4.
- Última versão: **narração reescrita "à prova de idiotas"** (explica o porquê de cada etapa), **legendas na tela** (campo `cap` de cada cena) e card explicativo por etapa na cena do processo. Duração ~2:30 com tempos estimados.
- A narração com voz Microsoft (Edge TTS) foi **reprovada** pelo Gabriel e removida. Ele quer **ElevenLabs, voz "Spuds Oxley - Grandpa"**, sem tom muito idoso (Stability ~50%, Speed ~1.05, modelo v3 com tags).

## Próximo passo (onde paramos)
1. **Gerar as 12 falas no ElevenLabs** com `03_video/roteiro_narracao_elevenlabs.txt` (uma por fala: 01.mp3 … 12.mp3). A sessão anterior rodava na nuvem e não alcançava o navegador do Gabriel. Se esta sessão tiver Claude no Chrome / computador do Gabriel, fazer direto no ElevenLabs aberto; senão, pedir para ele gerar e anexar, ou configurar `ELEVENLABS_API_KEY` no ambiente.
2. **Sincronizar:** cortar silêncio das pontas, duração de cada cena = max(duração atual, 0,35 + fala + 0,6), atualizar os `d:` em `castelo_anim.js`, montar a trilha com `adelay` + `loudnorm` (ffmpeg).
3. **Site:** embutir a trilha em base64 no lugar de `NARRACAO_SRC`, trocar `HAS_AUDIO = false` para `true` (o player usa o áudio como relógio e mostra o botão de som), embutir o JS/CSS novos e republicar o Artifact no mesmo link.
4. **MP4 final narrado** 1080p (`node render.js saida.mp4` + mux do áudio). Depois, oferecer versão vertical 9:16 para Reels/Status.

## Outras pendências do negócio
- Confirmar nome no INPI e registrar domínio + @castelopolimeros.
- Pedir orçamento a concorrentes (Nicoplas, Flex Ambiental, Gedel, Alassia, Barrichello) para descobrir o preço por kg.
- Começar as ligações pela prioridade A (Mastrapet, Odin Plast, Reciclagem Tietê, BCS, Dannaplas).
- Abertura: CNPJ (CNAE 3832-7/00 + 4687-7/03), CETESB, AVCB, NR-12, contador (industrialização por encomenda, CFOP 5.124/5.902).
- Mensagens prontas de WhatsApp para os clientes (ainda não feitas).

## Observações técnicas
- Renderização: Chromium headless (`/opt/pw-browsers/chromium_headless_shell-*/chrome-linux/headless_shell`) para PNG/PDF exatos; Playwright global em `/opt/node22/lib/node_modules/playwright`; ffmpeg no sistema. Caminhos absolutos nos scripts apontavam para o scratchpad da sessão anterior: ajustar para esta pasta.
- Ao tirar print com o Chromium "normal", ~87 px somem embaixo. Usar o `headless_shell`.
