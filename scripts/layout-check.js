#!/usr/bin/env node
/**
 * Layout check — catches what the geometry linter cannot: pages that look broken in a real browser.
 *   NODE_PATH=$(npm root -g) node scripts/layout-check.js http://localhost:5900 [page ...]
 * With no pages it checks the home page, every hub and one page per category.
 * For each page, at 320 / 390 / 768 / 1200 px wide it reports:
 *   - horizontal overflow (page wider than the viewport)
 *   - elements that stick out of the viewport on the right
 *   - CSS classes used in the HTML that have NO rule in the stylesheet (typo / forgotten CSS)
 *   - sibling cards in one row whose bottom edges differ (ragged rows)
 *   - inline text runs glued together: two sibling inline/inline-block elements with no space between
 *     and no block layout (the "57concepts" bug)
 *   - tap targets (links/buttons) smaller than 28px tall at 390 px
 * Exit code 1 if any problem is found. See docs/rules/lessons-learned.md.
 */
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const base = process.argv[2]; const pages = process.argv.slice(3);
if (!base) { console.error('usage: layout-check.js <baseUrl> [page ...]'); process.exit(2); }
const defaults = ['index.html','cloud/index.html','ai/index.html','azure/index.html','aws/index.html',
  'ai/concepts/rag.html','azure/concepts/compute.html','aws/concepts/compute.html','azure/concepts/service-bus.html'];
const css = fs.readFileSync(path.join(__dirname, '..', 'assets/style.css'), 'utf8');
const IGNORE = new Set(['sep','cur','num','str','cmt','kw','fn','arrow','chev','free','bx','zone','zone-title','arrow-pill','flow-arrow','mark','done','locked','soon','live','left']);
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  let bad = 0;
  for (const pg of (pages.length ? pages : defaults)) {
    for (const w of [320, 390, 768, 1200]) {
      const p = await b.newPage({ viewport: { width: w, height: 900 } });
      await p.goto(base.replace(/\/$/, '') + '/' + pg); await p.waitForTimeout(350);
      const res = await p.evaluate(({ w, css, IGNORE }) => {
        const out = [];
        const de = document.documentElement;
        if (de.scrollWidth > w + 1) out.push(`page is ${de.scrollWidth}px wide in a ${w}px viewport`);
        const wide = [...document.querySelectorAll('body *')].filter(e => { const r = e.getBoundingClientRect(); return r.width > 0 && r.right > w + 2 && !e.closest('.table-wrap, svg, pre, .code-block, .journey-wrap, .kdsearch-results, .fixed-pager, .kd-crumbs, .glow'); }).slice(0, 3);
        wide.forEach(e => out.push(`sticks out right: <${e.tagName.toLowerCase()} class="${e.className && e.className.baseVal === undefined ? e.className : ''}">`));
        const used = new Set(); document.querySelectorAll('[class]').forEach(e => { if (typeof e.className === 'string') e.className.split(/\s+/).forEach(c => c && used.add(c)); });
        const missing = [...used].filter(c => !IGNORE.includes(c) && !css.includes('.' + c));
        if (missing.length) out.push('classes with no CSS rule: ' + missing.join(', '));
        document.querySelectorAll('.tile-grid, .cloud-cards, .pick-grid, .scenario-grid, .how-strip, .deep-grid').forEach(g => {
          const kids = [...g.children]; const rows = {};
          kids.forEach(k => { const r = k.getBoundingClientRect(); (rows[Math.round(r.top)] = rows[Math.round(r.top)] || []).push(r.bottom); });
          Object.values(rows).forEach(bs => { if (bs.length > 1 && Math.max(...bs) - Math.min(...bs) > 2) out.push(`ragged row in .${g.className.split(' ')[0]} (bottoms differ by ${Math.round(Math.max(...bs) - Math.min(...bs))}px)`); });
        });
        // glued inline text: adjacent element siblings, both inline, no whitespace text between
        document.querySelectorAll('main *').forEach(e => {
          if (e.closest('svg, pre, .code-block')) return;
          const n = e.nextSibling; const nx = e.nextElementSibling;
          if (!nx || n !== nx) return; // whitespace text node exists between, or not adjacent
          const a = getComputedStyle(e), c = getComputedStyle(nx);
          const inl = s => (s.display === 'inline' || s.display === 'inline-block') && parseFloat(s.marginLeft) < 3 && parseFloat(s.marginRight) < 3 && parseFloat(s.paddingLeft) < 3;
          if (inl(a) && inl(c) && /\w$/.test(e.textContent.trim()) && /^\w/.test(nx.textContent.trim()) && !/^(A|B|I|EM|STRONG|CODE|SPAN)$/.test('') )
            out.push(`inline text glued together: "${e.textContent.trim().slice(0, 20)}" + "${nx.textContent.trim().slice(0, 20)}"`);
        });
        if (w === 390) {
          const small = [...document.querySelectorAll('main a, main button, .fixed-pager a')].filter(a => { const r = a.getBoundingClientRect(); const d = getComputedStyle(a).display; return r.height > 0 && r.height < 28 && d !== 'inline' && !a.closest('.fact-note, .deep-card, p, li, td, th, figcaption'); });
          if (small.length) out.push(`${small.length} tap target(s) under 28px tall, e.g. "${small[0].textContent.trim().slice(0, 25)}"`);
        }
        return out;
      }, { w, css, IGNORE: [...IGNORE] });
      const uniq = [...new Set(res)];
      if (uniq.length) { bad += uniq.length; console.log(`✗ ${pg} @${w}px`); uniq.forEach(r => console.log('    - ' + r)); }
      await p.close();
    }
  }
  console.log(bad ? `\n${bad} layout problem(s)` : 'layout OK');
  await b.close(); process.exit(bad ? 1 : 0);
})();
