/* Vídeo animado Castelo Polímeros. Tudo é função do tempo: CasteloAnim.renderAt(t) desenha o quadro t (segundos).
   Assim o mesmo código toca no site (requestAnimationFrame) e exporta o MP4 quadro a quadro. */
(function () {
  const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
  const prog = (t, a, b) => clamp((t - a) / (b - a));
  const out = (x) => 1 - Math.pow(1 - x, 3);
  const inout = (x) => (x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2);
  const back = (x) => { const c = 1.6; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); };
  const lerp = (a, b, p) => a + (b - a) * p;
  const fmt = (n, dec) => n.toLocaleString("pt-BR", { minimumFractionDigits: dec, maximumFractionDigits: dec });

  const NAVY = "#12385A", NIGHT = "#0B2238", AMBER = "#F2A900", AMBER_L = "#FFC93C", GREEN = "#2F7D5B";

  // título cinético: palavras sobem em sequência; *palavra* ganha marca-texto âmbar; | quebra a linha; _ vira espaço
  function T(str, o) {
    const s0 = o.s ?? 0.15, st = o.st ?? 0.07;
    let i = 0;
    const words = str.split(" ").map((tok) => {
      if (tok === "|") return "<br>";
      const mk = tok.startsWith("*");
      const txt = tok.replace(/\*/g, "").replace(/_/g, " ");
      const s = (s0 + st * i++).toFixed(2);
      if (mk) return `<span class="w cp-mk" data-a="up" data-s="${s}"><i data-a="mark" data-s="${(+s + 0.25).toFixed(2)}" data-d=".45"></i>${txt}</span>`;
      return `<span class="w" data-a="up" data-s="${s}">${txt}</span>`;
    }).join(" ");
    const style = `left:${o.x}px;top:${o.y}px;${o.size ? `font-size:${o.size}px;` : ""}${o.w ? `width:${o.w}px;` : ""}${o.center ? "text-align:center;" : ""}${o.color ? `color:${o.color};` : ""}`;
    return `<div class="cp-t" style="${style}">${words}</div>`;
  }
  const at = (a, s, d, extra = "") => `data-a="${a}" data-s="${s}"${d ? ` data-d="${d}"` : ""} ${extra}`;

  const SYMBOL_RECTS = [
    [8, 4, 8, 8, 0], [20, 4, 8, 8, 0], [32, 4, 8, 8, 0], [8, 12, 32, 6, 0], [8, 20.5, 32, 3.5, 0], [8, 26.5, 32, 3.5, 0],
    [8, 33, 4, 4, 1], [15, 33, 4, 4, 1], [22, 33, 4, 4, 1], [29, 33, 4, 4, 1], [36, 33, 4, 4, 1],
    [11.5, 40, 3, 3, 1], [18.5, 40, 3, 3, 1], [25.5, 40, 3, 3, 1], [32.5, 40, 3, 3, 1],
  ];
  // símbolo montado peça por peça: ameias caem, faixas deslizam, grãos aparecem
  function symbolBuild(cx, cy, size, s0, torre = "#fff") {
    const u = size / 48, x0 = cx - size / 2, y0 = cy - size / 2;
    return SYMBOL_RECTS.map(([x, y, w, h, p], i) => {
      const anim = i < 3 ? "drop" : i < 6 ? "slide" : "pop";
      const s = (s0 + (i < 3 ? i * 0.12 : i < 6 ? 0.45 + (i - 3) * 0.12 : 0.9 + (i - 6) * 0.06)).toFixed(2);
      return `<div ${at(anim, s, ".5")} style="position:absolute;left:${x0 + x * u}px;top:${y0 + y * u}px;width:${w * u}px;height:${h * u}px;background:${p ? AMBER : torre}"></div>`;
    }).join("");
  }
  const bale = (x, y, w = 200, h = 140, extra = "") =>
    `<div ${extra} style="position:absolute;left:${x}px;top:${y}px;width:${w}px;height:${h}px;border-radius:10px;
      background:repeating-linear-gradient(180deg,#1d2b38 0 9px,#3a4a58 9px 13px);box-shadow:0 18px 30px -16px rgba(0,0,0,.5)">
      <i style="position:absolute;top:0;bottom:0;left:22%;width:10px;background:${AMBER}"></i>
      <i style="position:absolute;top:0;bottom:0;right:22%;width:10px;background:${AMBER}"></i></div>`;

  const SCENES = [
    { d: 9.78, cap: "Toda fábrica que usa plástico gera sobra. Fita de arquear, ráfia, filme stretch, fio. No setor, essa sobra tem nome: apara.", cls: "cp-dark", html: () => `
      ${T("Toda indústria | gera *apara.*", { x: 160, y: 270, size: 150 })}
      <div class="cp-chip" ${at("pop", 1.5)} style="left:160px;top:690px">Fita de arquear</div>
      <div class="cp-chip" ${at("pop", 1.7)} style="left:560px;top:690px">Ráfia</div>
      <div class="cp-chip" ${at("pop", 1.9)} style="left:790px;top:690px">Filme stretch</div>
      <div class="cp-chip" ${at("pop", 2.1)} style="left:1150px;top:690px">Fio de PP</div>` },

    { d: 10.2, cap: "E, na maioria das vezes, essa apara fica parada no pátio. Ocupa espaço, junta poeira e vira custo, quando poderia virar dinheiro.", cls: "cp-light", html: () => `
      ${T("E ela fica | *parada* | no pátio.", { x: 160, y: 170, size: 140 })}
      <div class="cp-card" ${at("up", 1.4)} style="left:160px;top:660px;width:560px;padding:34px 40px">
        <div class="cp-k" style="color:#5B7084">Apara acumulada</div>
        <div class="cp-num" style="font-size:120px;color:${NAVY}"><span data-a="count" data-s="1.6" data-d="2.6" data-from="0" data-to="100">0</span> t<span style="font-size:52px;color:#7D90A2">/mês</span></div>
      </div>
      ${[0, 1, 2, 3, 4, 5].map((i) => bale(1060 + (i % 3) * 230, 760 - Math.floor(i / 3) * 165, 210, 150, at("drop", (0.8 + i * 0.3).toFixed(2), ".55"))).join("")}
      ${bale(1175, 430, 210, 150, at("drop", "2.6", ".55"))}
      ${bale(1405, 430, 210, 150, at("drop", "2.9", ".55"))}` },

    { d: 10.13, cap: "Por que ninguém resolve? Porque fita e filme são longos e enrolam. No moinho comum, eles se enroscam nas facas e a máquina para.", cls: "cp-dark", html: () => `
      ${T("Moinho comum | *trava* | com fita.", { x: 160, y: 250, size: 140 })}
      <svg style="position:absolute;left:1100px;top:240px;overflow:visible" width="600" height="600" viewBox="0 0 600 600">
        <circle cx="300" cy="300" r="250" fill="rgba(255,255,255,.04)" stroke="rgba(255,255,255,.18)" stroke-width="4"/>
        <g data-rot="rotor3">${Array.from({ length: 8 }, (_, i) => `<rect x="288" y="80" width="24" height="120" rx="6" fill="#A3B6C8" transform="rotate(${i * 45} 300 300)"/>`).join("")}<circle cx="300" cy="300" r="70" fill="#2C6E9E"/></g>
        <path data-a="draw" data-s="1.0" data-d="1.6" pathLength="1" d="M -60 120 C 120 80, 520 60, 520 300 C 520 520, 80 520, 80 300 C 80 140, 420 140, 420 300 C 420 420, 180 420, 180 300 C 180 230, 330 230, 330 300" fill="none" stroke="${AMBER}" stroke-width="22" stroke-linecap="round"/>
      </svg>
      <div ${at("pop", 2.7)} style="position:absolute;left:1500px;top:230px;width:150px;height:150px;border-radius:50%;background:#C93542;display:grid;place-items:center;font:800 90px Barlow;color:#fff;box-shadow:0 20px 40px -10px rgba(201,53,66,.6)">✕</div>
      <div class="cp-chip" ${at("pop", 3.0)} style="left:1180px;top:840px;background:rgba(201,53,66,.18);border-color:rgba(201,53,66,.6);color:#FFB3BA">Máquina parada</div>`,
      update(lt, r) { const a = r.querySelector('[data-rot="rotor3"]'); const spin = lt < 2.6 ? lt * 140 - Math.pow(prog(lt, 1.6, 2.6), 2) * 60 : 2.6 * 140 - 60; a.setAttribute("transform", `rotate(${spin} 300 300)`); } },

    { d: 7.78, cap: "A Castelo Polímeros nasceu exatamente pra isso: moer fita e plástico flexível, do jeito certo.", cls: "cp-dark", html: () => `
      ${symbolBuild(960, 400, 380, 0.2)}
      <div ${at("up", 1.8)} style="position:absolute;left:0;right:0;top:640px;text-align:center;font:800 120px/1 'Barlow Condensed';letter-spacing:6px">CASTELO <span style="color:${AMBER}">POLÍMEROS</span></div>
      <div class="cp-sub" ${at("fade", 2.3)} style="left:0;right:0;top:790px;text-align:center">Moagem especializada em fita e plástico flexível.</div>` },

    { d: 29.02, cap: "Funciona assim. O fardo entra inteiro, do jeito que sai da sua fábrica, sem precisar desmanchar. O pré-picador quebra o fardo em pedaços grandes. A esteira leva esses pedaços até o picador, que corta fino. Embaixo dele tem uma peneira: só passa o que tem até dois milímetros. O que é maior fica lá dentro até ser cortado de novo. No final, o material cai moído, direto no big bag, pronto pra extrusora.", stretch: true, b: 14, cls: "cp-light", html: () => `
      ${T("Do fardo ao *big_bag*", { x: 120, y: 64, size: 100 })}
      <div class="cp-sub" ${at("fade", 0.6)} style="left:120px;top:178px;font-size:34px">O fardo entra inteiro. Fita e filme não travam a linha.</div>
      <svg style="position:absolute;left:0;top:0" width="1920" height="1080" viewBox="0 0 1920 1080">
        <line x1="60" y1="842" x2="1860" y2="842" stroke="#D6E0E8" stroke-width="4"/>
        <!-- esteira 1 -->
        <line x1="110" y1="800" x2="580" y2="480" stroke="${NAVY}" stroke-width="22" stroke-linecap="round"/>
        ${Array.from({ length: 7 }, (_, i) => `<circle cx="${lerp(130, 560, i / 6)}" cy="${lerp(786, 494, i / 6)}" r="7" fill="${AMBER}"/>`).join("")}
        <line x1="150" y1="800" x2="150" y2="842" stroke="${NAVY}" stroke-width="10"/><line x1="470" y1="580" x2="470" y2="842" stroke="${NAVY}" stroke-width="10"/>
        <!-- pré-picador -->
        <polygon points="530,385 830,385 790,475 570,475" fill="#2C6E9E"/>
        <rect x="560" y="470" width="240" height="250" rx="16" fill="${NAVY}"/>
        <rect x="590" y="520" width="180" height="130" rx="65" fill="${NIGHT}"/>
        <g data-rot="r1">${Array.from({ length: 6 }, (_, i) => `<rect x="639" y="545" width="10" height="34" rx="3" fill="${AMBER}" transform="rotate(${i * 60} 644 585)"/>`).join("")}<circle cx="644" cy="585" r="16" fill="#A3B6C8"/></g>
        <g data-rot="r2">${Array.from({ length: 6 }, (_, i) => `<rect x="711" y="545" width="10" height="34" rx="3" fill="${AMBER}" transform="rotate(${i * 60} 716 585)"/>`).join("")}<circle cx="716" cy="585" r="16" fill="#A3B6C8"/></g>
        <line x1="600" y1="720" x2="600" y2="842" stroke="${NAVY}" stroke-width="12"/><line x1="760" y1="720" x2="760" y2="842" stroke="${NAVY}" stroke-width="12"/>
        <text x="680" y="365" text-anchor="middle" font-family="IBM Plex Mono" font-weight="600" font-size="22" letter-spacing="3" fill="#4E6377">PRÉ-PICADOR</text>
        <!-- calha + esteira 2 -->
        <path d="M 790 690 L 880 760" stroke="${NAVY}" stroke-width="16" stroke-linecap="round"/>
        <line x1="870" y1="772" x2="1250" y2="772" stroke="${NAVY}" stroke-width="16" stroke-linecap="round"/>
        ${Array.from({ length: 6 }, (_, i) => `<circle cx="${890 + i * 70}" cy="772" r="5" fill="${AMBER}"/>`).join("")}
        <g data-strips>${Array.from({ length: 7 }, (_, i) => `<rect data-strip="${i}" x="0" y="744" width="46" height="14" rx="4" fill="${i % 2 ? "#3a4a58" : AMBER}"/>`).join("")}</g>
        <text x="1060" y="730" text-anchor="middle" font-family="IBM Plex Mono" font-weight="600" font-size="22" letter-spacing="3" fill="#4E6377">ESTEIRA</text>
        <!-- picador -->
        <rect x="1250" y="560" width="210" height="250" rx="16" fill="${NAVY}"/>
        <circle cx="1355" cy="660" r="62" fill="${NIGHT}"/>
        <g data-rot="r3">${Array.from({ length: 8 }, (_, i) => `<rect x="1350" y="604" width="10" height="40" rx="3" fill="${AMBER}" transform="rotate(${i * 45} 1355 660)"/>`).join("")}<circle cx="1355" cy="660" r="18" fill="#A3B6C8"/></g>
        <rect x="1280" y="752" width="150" height="22" rx="4" fill="${NIGHT}"/>
        ${Array.from({ length: 12 }, (_, i) => `<circle cx="${1292 + i * 12}" cy="763" r="3" fill="#A3B6C8"/>`).join("")}
        <line x1="1280" y1="810" x2="1280" y2="842" stroke="${NAVY}" stroke-width="12"/><line x1="1430" y1="810" x2="1430" y2="842" stroke="${NAVY}" stroke-width="12"/>
        <text x="1355" y="540" text-anchor="middle" font-family="IBM Plex Mono" font-weight="600" font-size="22" letter-spacing="3" fill="#4E6377">PICADOR · 2 MM</text>
        <path d="M 1460 700 L 1560 720" stroke="${NAVY}" stroke-width="16" stroke-linecap="round"/>
        <!-- big bag -->
        <defs><clipPath id="cpbag"><path d="M 1560 640 L 1800 640 L 1790 838 L 1570 838 Z"/></clipPath>
          <pattern id="cpgr" width="16" height="16" patternUnits="userSpaceOnUse"><rect width="16" height="16" fill="#26313b"/><rect x="2" y="3" width="6" height="5" fill="#e9eef2"/><rect x="10" y="10" width="5" height="4" fill="#9fb0bf"/></pattern></defs>
        <path d="M 1560 640 L 1800 640 L 1790 838 L 1570 838 Z" fill="#fff" stroke="#C9D6E1" stroke-width="4"/>
        <rect data-fill x="1550" y="838" width="260" height="0" fill="url(#cpgr)" clip-path="url(#cpbag)"/>
        <path d="M 1580 640 Q 1590 600 1610 640 M 1750 640 Q 1760 600 1780 640" fill="none" stroke="#C9D6E1" stroke-width="6"/>
        <g data-pellets>${Array.from({ length: 16 }, (_, i) => `<rect data-pel="${i}" width="9" height="8" fill="${i % 3 ? "#26313b" : "#e9eef2"}"/>`).join("")}</g>
      </svg>
      ${bale(0, 0, 170, 120, 'data-bale')}
      <div ${at("fade", 6.5)} class="cp-card" style="left:1570px;top:500px;padding:12px 22px;border-radius:16px;font:800 44px 'Barlow Condensed';color:${NAVY}"><span data-a="count" data-s="7" data-d="6" data-from="0" data-to="985">0</span> kg</div>
      <div class="cp-card" data-explain style="left:1160px;top:250px;width:640px;padding:22px 30px;display:flex;gap:22px;align-items:center">
        <div data-explain-n style="flex:none;width:64px;height:64px;border-radius:18px;background:linear-gradient(110deg,${AMBER_L},${AMBER});display:grid;place-items:center;font:800 40px 'Barlow Condensed';color:#1A1200">1</div>
        <div><div data-explain-t style="font:800 40px/1 'Barlow Condensed';text-transform:uppercase;color:${NAVY}"></div><div data-explain-d style="font:500 28px/1.3 Barlow;color:#4E6377;margin-top:6px"></div></div></div>
      <!-- etapas -->
      <div style="position:absolute;left:250px;top:898px;width:1400px;height:6px;border-radius:4px;background:#DCE5ED"><div data-line style="height:100%;width:0;border-radius:4px;background:linear-gradient(90deg,${AMBER_L},${AMBER})"></div></div>
      ${[["Fardo inteiro", 250], ["Pré-picador", 680], ["Esteira", 1060], ["Picador · 2 mm", 1355], ["Big bag", 1650]].map(([l, x], i) =>
        `<div data-step="${i}" style="position:absolute;left:${x - 150}px;top:870px;width:300px;text-align:center">
          <div class="cp-dot" style="margin:0 auto;width:30px;height:30px;border-radius:50%;background:#DCE5ED;border:5px solid #F3F6F9"></div>
          <div class="lb" style="margin-top:10px;font:700 34px 'Barlow Condensed';text-transform:uppercase;color:#9AACBC">${l}</div></div>`).join("")}`,
      update(lt, r) {
        const STEP_T = [0.6, 3.4, 4.6, 6.2, 7.6];
        r.querySelectorAll("[data-step]").forEach((el, i) => {
          const on = lt >= STEP_T[i];
          el.querySelector(".cp-dot").style.background = on ? AMBER : "#DCE5ED";
          el.querySelector(".cp-dot").style.transform = `scale(${on ? 1 + 0.35 * (1 - prog(lt, STEP_T[i], STEP_T[i] + 0.4)) : 1})`;
          el.querySelector(".lb").style.color = on ? NAVY : "#9AACBC";
        });
        const EXP = [["Fardo inteiro", "Entra do jeito que sai da sua fábrica."], ["Pré-picador", "Quebra o fardo em pedaços grandes."], ["Esteira", "Leva os pedaços até o picador."], ["Picador + peneira", "Corta fino. Só passa o que tem até 2 mm."], ["Big bag", "Moído e pronto pra extrusora."]];
        let si = 0; for (let k = 0; k < 5; k++) if (lt >= STEP_T[k]) si = k;
        const ex = r.querySelector("[data-explain]");
        ex.style.opacity = String(prog(lt, 0.3, 0.7));
        r.querySelector("[data-explain-n]").textContent = si + 1;
        r.querySelector("[data-explain-t]").textContent = EXP[si][0];
        r.querySelector("[data-explain-d]").textContent = EXP[si][1];
        const pulse = 1 - prog(lt, STEP_T[si], STEP_T[si] + 0.35);
        ex.style.transform = `translateY(${pulse * 12}px)`;
        const xs = [0, 430, 810, 1105, 1400];
        let w = 0; for (let i = 0; i < 5; i++) if (lt >= STEP_T[i]) w = i < 4 ? lerp(xs[i], xs[i + 1], out(prog(lt, STEP_T[i], STEP_T[i + 1]))) : 1400;
        r.querySelector("[data-line]").style.width = w + "px";
        // fardo sobe a esteira e cai na tremonha
        const b = r.querySelector("[data-bale]"); const u = inout(prog(lt, 0.8, 3.3));
        const bx = lerp(150, 545, u), by = lerp(668, 368, u) + 18 * Math.pow(prog(lt, 3.3, 3.9), 2) * 6;
        b.style.transform = `translate(${bx - 85}px, ${by - 60}px) rotate(${lt < 3.3 ? -34 : -34 + 34 * prog(lt, 3.3, 3.9)}deg) scale(${1 - 0.5 * prog(lt, 3.3, 3.9)})`;
        b.style.opacity = String(lt < 0.4 ? prog(lt, 0, 0.4) : 1 - prog(lt, 3.5, 3.95));
        // rotores
        const sp1 = lt < 3.3 ? lt * 40 : 3.3 * 40 + (lt - 3.3) * 420;
        r.querySelector('[data-rot="r1"]').setAttribute("transform", `rotate(${sp1} 644 585)`);
        r.querySelector('[data-rot="r2"]').setAttribute("transform", `rotate(${-sp1} 716 585)`);
        const sp3 = lt < 5.6 ? lt * 40 : 5.6 * 40 + (lt - 5.6) * 520;
        r.querySelector('[data-rot="r3"]').setAttribute("transform", `rotate(${sp3} 1355 660)`);
        // tiras na esteira
        const sOn = prog(lt, 4.2, 4.6) * (1 - prog(lt, 12.6, 13));
        r.querySelectorAll("[data-strip]").forEach((el, i) => {
          const x = 880 + ((lt * 150 + i * 56) % 360);
          el.setAttribute("x", x); el.setAttribute("opacity", String(sOn * (x > 1220 ? 0 : 1)));
          el.setAttribute("transform", `rotate(${(i % 2 ? 8 : -6)} ${x + 23} 751)`);
        });
        // grãos caindo no bag
        const fill = out(prog(lt, 7.2, 13.2));
        const surf = 838 - fill * 175;
        r.querySelector("[data-fill]").setAttribute("y", surf); r.querySelector("[data-fill]").setAttribute("height", 838 - surf);
        const pOn = prog(lt, 6.6, 7) * (1 - prog(lt, 13, 13.3));
        r.querySelectorAll("[data-pel]").forEach((el, i) => {
          const ph = (lt * 1.3 + i / 16) % 1;
          const x0 = 1562, y0 = 722, x1 = 1600 + (i * 37) % 160, y1 = surf;
          const x = lerp(x0, x1, ph), y = y0 + (y1 - y0) * ph * ph - 60 * Math.sin(Math.PI * ph) * 0.4;
          el.setAttribute("x", x); el.setAttribute("y", y); el.setAttribute("opacity", String(pOn * (ph < 0.95 ? 1 : 0)));
        });
      } },

    { d: 14.27, cap: "Antes de começar, a gente pesa o seu material. Depois de moído, pesa de novo. Assim você sabe exatamente quanto entrou e quanto voltou. E a perda do processo já fica combinada em contrato.", cls: "cp-dark", html: () => `
      ${T("Pesagem | na entrada | *e na saída.*", { x: 160, y: 230, size: 130 })}
      <div class="cp-card" ${at("left", 1.2)} style="left:1080px;top:230px;width:660px;padding:36px 44px">
        <div class="cp-k" style="color:#A3B6C8">Entrada · fardo</div>
        <div class="cp-num" style="font-size:130px"><span data-a="count" data-s="1.4" data-d="1.4" data-from="0" data-to="1000">0</span> <span style="font-size:60px;color:#A3B6C8">kg</span></div></div>
      <div class="cp-card" ${at("left", 2.0)} style="left:1080px;top:540px;width:660px;padding:36px 44px;border-color:rgba(242,169,0,.5)">
        <div class="cp-k" style="color:${AMBER_L}">Saída · moído</div>
        <div class="cp-num" style="font-size:130px"><span data-a="count" data-s="2.2" data-d="1.4" data-from="0" data-to="985">0</span> <span style="font-size:60px;color:#A3B6C8">kg</span></div></div>
      <div class="cp-sub" ${at("fade", 3.2)} style="left:1080px;top:860px;font-size:34px">Perda de processo combinada em contrato.</div>` },

    { d: 11.23, cap: "Cada big bag sai com uma etiqueta: nome do cliente, tipo de plástico, tamanho do grão, peso e data. Se precisar rastrear um lote, está tudo ali.", cls: "cp-light", html: () => `
      ${T("Cada lote | com sua | *etiqueta.*", { x: 160, y: 250, size: 140 })}
      <div class="cp-card" ${at("up", 0.8)} style="left:980px;top:170px;width:780px;overflow:hidden">
        <div style="background:${NAVY};padding:26px 36px;display:flex;justify-content:space-between;align-items:center">
          <div style="display:flex;align-items:center;gap:14px;color:#fff;font:800 40px/1 'Barlow Condensed';letter-spacing:2px">
            <svg width="54" height="54" viewBox="0 0 48 48">${SYMBOL_RECTS.map(([x, y, w, h, p]) => `<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="${p ? AMBER : "#fff"}"/>`).join("")}</svg>CASTELO</div>
          <div style="font:800 46px 'Barlow Condensed';color:${AMBER_L}">LOTE Nº 0042</div></div>
        <div style="height:10px;background:repeating-linear-gradient(-45deg,${AMBER} 0 18px,${NIGHT} 18px 28px)"></div>
        <div style="padding:20px 36px 30px">
          ${[["Cliente", "Embalagens Exemplo"], ["Resina", "PP · preto"], ["Granulometria", "2 mm"], ["Peso líquido", "985 kg"], ["Data", "18/11/2026"]].map(([k, v], i) =>
            `<div style="display:flex;justify-content:space-between;align-items:baseline;padding:16px 0;border-bottom:2px solid #E2E9EF">
              <span class="cp-k" style="font-size:22px;color:#7D90A2">${k}</span>
              <span data-a="type" data-s="${(1.3 + i * 0.55).toFixed(2)}" data-d=".5" data-text="${v}" style="font:700 42px 'Barlow Condensed';text-transform:uppercase;color:#0E1E2E"></span></div>`).join("")}
        </div></div>` },

    { d: 14.75, cap: "E o mais importante: o seu material nunca se mistura com o de outro cliente. Também não misturamos tipos de plástico, porque PP e PET derretem em temperaturas diferentes, e misturado perde valor.", cls: "cp-dark", html: () => `
      ${T("Um bag por lote. | *Nunca* mistura.", { x: 160, y: 120, size: 120 })}
      ${[["PP", 300, "#26313b"], ["PE", 860, "#9DBBD0"], ["PET", 1420, "#3FA27A"]].map(([lb, x, c], k) => `
        <div class="cp-chip" ${at("pop", (1.2 + k * 0.25).toFixed(2))} style="left:${x + 110}px;top:470px">${lb}</div>
        ${[0, 1].map((j) => `<div ${at("drop", (1.5 + k * 0.25 + j * 0.15).toFixed(2), ".5")} style="position:absolute;left:${x + j * 190}px;top:600px;width:170px;height:210px;border-radius:12px 12px 18px 18px;background:#fff;overflow:hidden;box-shadow:0 24px 40px -20px rgba(0,0,0,.6)">
            <div style="position:absolute;left:0;right:0;bottom:0;height:62%;background:${c}"></div>
            <div style="position:absolute;left:14px;right:14px;top:14px;height:26px;border-radius:4px;background:${AMBER}"></div></div>`).join("")}
        ${k < 2 ? `<div ${at("fade", 1.4)} style="position:absolute;left:${x + 450}px;top:470px;height:360px;border-left:4px dashed rgba(255,255,255,.18)"></div>` : ""}`).join("")}` },

    { d: 11.51, cap: "Ficamos em Boituva, às margens da Castello Branco. Daqui, atendemos um raio de cem quilômetros: Sorocaba, Itu, Tatuí, Indaiatuba, Campinas e região.", cls: "cp-dark", html: () => {
      const C = [960 + 380, 560], R = 380;
      const cities = [["Cerquilho", 15, 340], ["Tietê", 25, 265], ["Porto Feliz", 25, 35], ["Tatuí", 30, 225], ["Sorocaba", 45, 135], ["Itu", 50, 105], ["Salto", 55, 85], ["Indaiatuba", 70, 62], ["Monte Mor", 80, 20], ["Piracicaba", 85, 352], ["Campinas", 95, 50]];
      return `
      ${T("Da Castello | Branco para | *a região.*", { x: 120, y: 300, size: 120 })}
      <div class="cp-sub" ${at("fade", 1.2)} style="left:120px;top:720px;font-size:34px">Distâncias aproximadas a partir de Boituva.</div>
      <svg style="position:absolute;left:0;top:0;overflow:visible" width="1920" height="1080">
        ${[[30, 0.3], [60, 0.55], [100, 0.8]].map(([km, s]) => `<circle data-a="draw" data-s="${s}" data-d="1" pathLength="1" cx="${C[0]}" cy="${C[1]}" r="${(km / 100) * R}" fill="none" stroke="rgba(255,255,255,.22)" stroke-width="3" stroke-dasharray="1" transform="rotate(-90 ${C[0]} ${C[1]})"/>
          <text ${at("fade", s + 0.6)} x="${C[0] + 8}" y="${C[1] - (km / 100) * R - 10}" font-family="IBM Plex Mono" font-size="22" fill="#A3B6C8">${km} km</text>`).join("")}
        ${cities.map(([n, km, ang], i) => { const a = (ang - 90) * Math.PI / 180, rr = (km / 100) * R, x = C[0] + Math.cos(a) * rr, y = C[1] + Math.sin(a) * rr, s = (1.3 + i * 0.16).toFixed(2), left = Math.cos(a) < -0.2;
          return `<g ${at("pop", s, ".4")} style="transform-origin:${x}px ${y}px"><circle cx="${x}" cy="${y}" r="11" fill="${AMBER}"/><circle cx="${x}" cy="${y}" r="22" fill="rgba(242,169,0,.18)"/>
            <text x="${left ? x - 22 : x + 22}" y="${y + 9}" text-anchor="${left ? "end" : "start"}" font-family="Barlow Condensed" font-weight="700" font-size="30" fill="#EAF1F7">${n.toUpperCase()}</text></g>`; }).join("")}
      </svg>
      <div ${at("pop", 0.2)} style="position:absolute;left:${C[0] - 46}px;top:${C[1] - 46}px;width:92px;height:92px;border-radius:24px;background:${NAVY};border:3px solid ${AMBER};display:grid;place-items:center">
        <svg width="56" height="56" viewBox="0 0 48 48">${SYMBOL_RECTS.map(([x, y, w, h, p]) => `<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="${p ? AMBER : "#fff"}"/>`).join("")}</svg></div>
      <div ${at("fade", 0.5)} style="position:absolute;left:${C[0] - 100}px;top:${C[1] + 56}px;width:200px;text-align:center;font:800 32px 'Barlow Condensed';color:${AMBER_L}">BOITUVA</div>`; } },

    { d: 9.51, cap: "Em números: capacidade de quatro toneladas por dia, grão de até dois milímetros e três tipos de plástico: PP, PE e PET.", cls: "cp-light", html: () => `
      ${T("Ficha *técnica*", { x: 160, y: 130, size: 120 })}
      ${[["count", 0, 4, " t", "por dia de capacidade"], ["count", 10, 2, " mm", "granulometria mínima"], ["count", 0, 3, "", "resinas: PP, PE e PET"]].map(([a, f, to, suf, k], i) => `
        <div class="cp-card" ${at("up", (0.7 + i * 0.2).toFixed(2))} style="left:${160 + i * 545}px;top:400px;width:510px;height:400px;padding:46px 48px">
          <div class="cp-num" style="font-size:190px;color:${NAVY}"><span data-a="count" data-s="${(1 + i * 0.2).toFixed(2)}" data-d="1.6" data-from="${f}" data-to="${to}">${f}</span><span style="font-size:90px">${suf}</span></div>
          <div style="margin-top:30px;padding-top:24px;border-top:3px solid #E2E9EF;font:600 38px Barlow;color:#4E6377">${k}</div>
          <div style="position:absolute;left:48px;top:0;width:90px;height:8px;border-radius:0 0 6px 6px;background:linear-gradient(90deg,${AMBER_L},${AMBER})"></div></div>`).join("")}` },

    { d: 11.64, cap: "Quer ver antes de fechar? Você manda até quinhentos quilos, a gente mói, e você testa na sua máquina. Aprovou? Aí sim a gente conversa sobre contrato.", cls: "cp-dark", html: () => `
      ${T("Teste antes | *de fechar.*", { x: 160, y: 280, size: 150 })}
      <div class="cp-card" ${at("left", 1.2)} style="left:1060px;top:240px;width:700px;padding:48px 54px">
        <div class="cp-k" style="color:${AMBER_L}">Lote-piloto</div>
        <div class="cp-num" style="font-size:150px;margin-top:6px">ATÉ 500 KG</div>
        <div style="font:500 36px/1.35 Barlow;color:#A3B6C8;margin-top:12px">Moemos um lote do seu material para você aprovar antes do contrato.</div>
        <div data-btn ${at("pop", 2.2)} style="display:inline-block;margin-top:36px;padding:26px 46px;border-radius:20px;background:linear-gradient(110deg,${AMBER_L},${AMBER});color:#1A1200;font:700 40px Barlow;box-shadow:0 20px 40px -16px rgba(242,169,0,.7)">Peça seu orçamento ↗</div>
      </div>
      <svg data-cursor style="position:absolute;left:0;top:0;opacity:0" width="56" height="56" viewBox="0 0 24 24"><path d="M4 2 L4 20 L9 15 L12.5 22 L15.5 20.5 L12 13.5 L19 13.5 Z" fill="#fff" stroke="#0B2238" stroke-width="1.4"/></svg>
      <div ${at("fade", 3.4)} style="position:absolute;left:160px;top:820px;font:600 40px 'IBM Plex Mono';color:${AMBER_L}">castelopolimeros.com.br</div>`,
      update(lt, r) {
        const c = r.querySelector("[data-cursor]"); const u = inout(prog(lt, 2.6, 3.4));
        c.style.opacity = String(prog(lt, 2.5, 2.7)); c.style.transform = `translate(${lerp(1800, 1330, u)}px, ${lerp(1000, 800, u)}px)`;
        const k = prog(lt, 3.45, 3.6) - prog(lt, 3.6, 3.8);
        const b = r.querySelector("[data-btn]"); if (lt > 3.4) b.style.transform = `scale(${1 - 0.06 * k})`;
      } },

    { d: 10.82, cap: "Pra pedir orçamento, é só acessar castelopolimeros.com.br ou chamar no WhatsApp. Castelo Polímeros: sua apara de volta como matéria-prima.", cls: "cp-dark", html: () => `
      <svg style="position:absolute;left:0;top:0" width="1920" height="1080"><circle data-a="draw" data-s="0.1" data-d="1.4" pathLength="1" cx="960" cy="420" r="250" fill="none" stroke="${AMBER}" stroke-width="5" stroke-dasharray="1" transform="rotate(-90 960 420)"/>
        <circle cx="960" cy="420" r="250" fill="rgba(255,255,255,.03)"/></svg>
      ${symbolBuild(960, 420, 280, 0.4)}
      <div ${at("up", 1.5)} style="position:absolute;left:0;right:0;top:720px;text-align:center;line-height:.9;color:#fff">
        <div style="font:800 110px 'Barlow Condensed';letter-spacing:5px">CASTELO</div>
        <div style="font:600 44px 'Barlow Condensed';letter-spacing:22px;margin-top:6px">POLÍMEROS</div></div>
      <div class="cp-k" ${at("fade", 2.2)} style="position:absolute;left:0;right:0;top:905px;text-align:center;color:#A3B6C8">Boituva-SP · moagem de fita e plástico flexível</div>
      <div class="cp-tape" ${at("fade", 2.0)}></div>` },
  ];

  function splitCap(str) {
    const parts = str.match(/[^.?!:]+[.?!:]?/g) || [];
    const out = [];
    parts.forEach((p) => { p = p.trim(); if (!p) return; const w = p.split(" ");
      if (w.length <= 11) out.push(p); else { const n = Math.ceil(w.length / 10), k = Math.ceil(w.length / n); for (let j = 0; j < w.length; j += k) out.push(w.slice(j, j + k).join(" ")); } });
    return out.map((c) => c.charAt(0).toUpperCase() + c.slice(1));
  }
  let starts = [], TOTAL = 0;
  SCENES.forEach((s) => { starts.push(TOTAL); TOTAL += s.d; });
  const FADE = 0.4;

  function animEl(el, lt) {
    const a = el.dataset.a, s = +el.dataset.s || 0, d = +(el.dataset.d || 0.6);
    const p = prog(lt, s, s + d);
    switch (a) {
      case "up": el.style.opacity = p; el.style.transform = `translateY(${(1 - out(p)) * 60}px)`; break;
      case "fade": el.style.opacity = p; break;
      case "left": el.style.opacity = p; el.style.transform = `translateX(${(1 - out(p)) * 120}px)`; break;
      case "pop": el.style.opacity = clamp(p * 2); el.style.transform = `scale(${0.6 + 0.4 * back(p)})`; break;
      case "drop": el.style.opacity = clamp(p * 3); el.style.transform = `translateY(${-(1 - out(p)) * 260}px)`; break;
      case "slide": el.style.opacity = clamp(p * 2); el.style.transform = `translateX(${-(1 - out(p)) * 320}px)`; break;
      case "mark": el.style.transform = `scaleX(${out(p)})`; break;
      case "draw": el.style.strokeDasharray = "1"; el.style.strokeDashoffset = String(1 - inout(p)); break;
      case "count": { const f = +el.dataset.from, t = +el.dataset.to; const v = lerp(f, t, out(p)); el.textContent = fmt(Math.round(v), 0); break; }
      case "type": { const txt = el.dataset.text; el.textContent = txt.slice(0, Math.round(txt.length * p)); break; }
    }
  }

  function mount(stage) {
    stage.classList.add("cp-stage");
    stage.innerHTML = SCENES.map((s, i) => `<div class="cp-scene ${s.cls}" data-i="${i}">${s.html()}</div>`).join("");
    stage.insertAdjacentHTML("beforeend", '<div class="cp-cap"><span></span></div>');
    const capEl = stage.querySelector(".cp-cap"), capTxt = capEl.firstChild;
    const chunks = SCENES.map((sc) => splitCap(sc.cap || ""));
    const roots = [...stage.querySelectorAll(".cp-scene")];
    const anims = roots.map((r) => [...r.querySelectorAll("[data-a]")]);
    return function renderAt(t) {
      t = clamp(t, 0, TOTAL);
      // legenda: a fala da cena atual dividida em trechos curtos, cada um pelo tempo proporcional ao tamanho
      let ci = 0; while (ci < SCENES.length - 1 && t >= starts[ci + 1]) ci++;
      const ch = chunks[ci], lt0 = t - starts[ci], span = SCENES[ci].d - 0.5;
      let acc = 0.25, txt = "", a = 0;
      const tot = ch.reduce((x, c) => x + c.length, 0) || 1;
      for (const c of ch) { const dd = span * c.length / tot; if (lt0 >= acc) { txt = c; a = prog(lt0, acc, acc + 0.2); } acc += dd; }
      if (window.CASTELO_CAPTIONS === false) txt = "";
      capTxt.textContent = txt; capEl.style.opacity = txt ? Math.min(a, 1 - prog(lt0, SCENES[ci].d - 0.25, SCENES[ci].d)) : 0;
      roots.forEach((r, i) => {
        const st = starts[i], en = st + SCENES[i].d;
        const visible = t >= st && t < en + FADE && !(i === SCENES.length - 1 && t > en);
        const last = i === SCENES.length - 1;
        if (!visible && !(last && t >= TOTAL)) { r.style.visibility = "hidden"; r.style.opacity = 0; return; }
        const lt0 = t - st, sc = SCENES[i];
        const lt = sc.stretch ? lt0 * sc.b / sc.d : lt0;
        const op = (i === 0 ? 1 : prog(lt0, 0, FADE)) * (last ? 1 : 1 - prog(t, en, en + FADE));
        r.style.visibility = "visible"; r.style.opacity = op;
        anims[i].forEach((el) => animEl(el, lt));
        if (sc.update) sc.update(lt, r);
      });
    };
  }

  window.CasteloAnim = { mount, get duration() { return TOTAL; } };
})();
