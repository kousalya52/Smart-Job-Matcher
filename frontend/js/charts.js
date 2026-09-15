/* ============================================================
   charts.js — hand-built SVG data visualizations.
   No chart library dependency: keeps the whole app offline-capable
   and gives it a visual identity that isn't a default chart-lib look.
   ============================================================ */

const Charts = (() => {

  const NS = 'http://www.w3.org/2000/svg';
  const el = (tag, attrs = {}) => {
    const node = document.createElementNS(NS, tag);
    Object.entries(attrs).forEach(([k, v]) => node.setAttribute(k, v));
    return node;
  };

  function bandColor(pct) {
    if (pct >= 70) return 'var(--accent-match)';
    if (pct >= 40) return 'var(--accent-gold)';
    return 'var(--accent-gap)';
  }

  // ---------------- GAUGE ----------------
  function renderGauge(container, percent, label) {
    container.innerHTML = '';
    const size = 220, stroke = 16, r = (size - stroke) / 2, c = size / 2;
    const circumference = 2 * Math.PI * r;
    const svg = el('svg', { viewBox: `0 0 ${size} ${size}`, class: 'gauge-svg' });

    const track = el('circle', {
      cx: c, cy: c, r, fill: 'none', stroke: 'var(--border-strong)', 'stroke-width': stroke
    });
    const arc = el('circle', {
      cx: c, cy: c, r, fill: 'none', stroke: bandColor(percent), 'stroke-width': stroke,
      'stroke-linecap': 'round',
      'stroke-dasharray': circumference,
      'stroke-dashoffset': circumference,
      transform: `rotate(-90 ${c} ${c})`
    });
    svg.appendChild(track);
    svg.appendChild(arc);

    const text = el('text', {
      x: c, y: c - 4, 'text-anchor': 'middle', class: 'gauge-number'
    });
    text.textContent = '0%';
    const sub = el('text', { x: c, y: c + 24, 'text-anchor': 'middle', class: 'gauge-label' });
    sub.textContent = label || 'Match';
    svg.appendChild(text);
    svg.appendChild(sub);
    container.appendChild(svg);

    // animate
    requestAnimationFrame(() => {
      arc.style.transition = 'stroke-dashoffset 1.1s cubic-bezier(.16,1,.3,1)';
      arc.setAttribute('stroke-dashoffset', String(circumference * (1 - percent / 100)));
      let cur = 0;
      const step = () => {
        cur += Math.max(1, (percent - cur) * 0.12);
        if (cur >= percent) cur = percent;
        text.textContent = Math.round(cur) + '%';
        if (cur < percent) requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
    });
  }

  // ---------------- RADAR ----------------
  function renderRadar(container, skillsList) {
    container.innerHTML = '';
    const items = skillsList.slice(0, 10);
    const n = Math.max(items.length, 3);
    const size = 420, c = size / 2, r = size / 2 - 70;
    const svg = el('svg', { viewBox: `0 0 ${size} ${size}`, class: 'radar-svg' });

    const angleFor = i => (Math.PI * 2 * i / n) - Math.PI / 2;
    const pointAt = (i, frac) => {
      const a = angleFor(i);
      return [c + Math.cos(a) * r * frac, c + Math.sin(a) * r * frac];
    };

    // grid rings
    [0.25, 0.5, 0.75, 1].forEach(frac => {
      const pts = items.map((_, i) => pointAt(i, frac).join(',')).join(' ');
      svg.appendChild(el('polygon', {
        points: pts, fill: 'none', stroke: 'var(--border-strong)', 'stroke-width': 1
      }));
    });

    // axis lines + labels
    items.forEach((item, i) => {
      const [x, y] = pointAt(i, 1);
      svg.appendChild(el('line', { x1: c, y1: c, x2: x, y2: y, stroke: 'var(--border-strong)', 'stroke-width': 1 }));
      const [lx, ly] = pointAt(i, 1.18);
      const label = el('text', {
        x: lx, y: ly, 'text-anchor': Math.abs(lx - c) < 10 ? 'middle' : (lx > c ? 'start' : 'end'),
        class: 'radar-label'
      });
      label.textContent = item.name.length > 16 ? item.name.slice(0, 15) + '…' : item.name;
      svg.appendChild(label);
    });

    // data polygon
    const dataPts = items.map((item, i) => pointAt(i, item.matched ? 1 : 0.28));
    svg.appendChild(el('polygon', {
      points: dataPts.map(p => p.join(',')).join(' '),
      fill: 'var(--primary)', 'fill-opacity': 0.18,
      stroke: 'var(--primary)', 'stroke-width': 2
    }));

    // dots
    items.forEach((item, i) => {
      const [x, y] = dataPts[i];
      svg.appendChild(el('circle', {
        cx: x, cy: y, r: item.matched ? 6 : 5,
        fill: item.matched ? 'var(--accent-match)' : 'var(--accent-gap)',
        stroke: 'var(--bg)', 'stroke-width': 2
      }));
    });

    container.appendChild(svg);
  }

  // ---------------- RANKED BARS ----------------
  function renderRankedBars(container, ranked, highlightRoleId) {
    container.innerHTML = '';
    const top = ranked.slice(0, 6);
    const wrap = document.createElement('div');
    wrap.className = 'bars-wrap';
    top.forEach((r, i) => {
      const row = document.createElement('div');
      row.className = 'bar-row' + (r.roleId === highlightRoleId ? ' bar-row--active' : '');
      row.innerHTML = `
        <div class="bar-row__label">
          <span class="bar-row__title">${r.title}</span>
          <span class="bar-row__pct">${r.percent}%</span>
        </div>
        <div class="bar-row__track">
          <div class="bar-row__fill" style="width:0%; background:${bandColor(r.percent)}"></div>
        </div>`;
      wrap.appendChild(row);
    });
    container.appendChild(wrap);
    requestAnimationFrame(() => {
      wrap.querySelectorAll('.bar-row__fill').forEach((fill, i) => {
        setTimeout(() => { fill.style.width = top[i].percent + '%'; }, i * 90);
      });
    });
  }

  return { renderGauge, renderRadar, renderRankedBars };
})();
