#!/usr/bin/env python3
"""Render a slide deck's slide files on a 1920x1080 canvas and measure each slide.

    python3 slide_preview.py <deck folder holding project/> <output folder>
    cd <output folder> && python3 -m http.server 8765      # then open http://127.0.0.1:8765/preview.html

Reads project/deck.json for the slide order and project/slides/<id>.html for each
slide, drops the speaker notes, and writes preview.html. When the page loads (after
fonts), a script measures every slide and prints a table at the top; the same data
is in window.__deckReport. Use it to look at each slide and to catch what a person
sees at once: text pushed past the bottom margin, content running into the footer,
text outside the side margins, text under 24px, and slides that are nearly empty.

Standard library only. The measurements are an approximation of the deck tool's own
renderer: trust a failure, and still look at the picture.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

PAGE = """<!doctype html>
<html><head><meta charset="utf-8"><title>Slide preview</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=EB+Garamond:wght@400..700&family=DM+Sans:wght@400;500;700&display=swap">
<style>
 body { margin:0; background:#555; font-family:system-ui,sans-serif; }
 #report { background:#fff; color:#111; padding:16px 24px; font:14px/1.4 system-ui; max-width:1920px; margin:0 auto 24px; }
 #report table { border-collapse:collapse; width:100%; }
 #report td, #report th { border:1px solid #ccc; padding:4px 8px; text-align:left; vertical-align:top; }
 .bad { background:#fde2e0; } .ok { background:#e3f4e6; }
 .frame { width:1920px; height:1080px; position:relative; margin:0 auto 48px; overflow:hidden; background:#fff; }
 .frame > section { width:1920px; height:1080px; box-sizing:border-box; position:relative; overflow:hidden; margin:0; }
 .frame > section * { box-sizing:border-box; }
 /* The deck format ignores margin, so reset the browser defaults to match. Cells pad .35em .6em. */
 .frame section p, .frame section h1, .frame section h2, .frame section h3, .frame section ul, .frame section ol, .frame section table { margin:0; }
 .frame section ul, .frame section ol { padding-left:1.2em; }
 .frame section table { border-collapse:collapse; width:100%; }
 .frame section td, .frame section th { padding:.35em .6em; border-bottom:1px solid rgba(0,0,0,.12); }
 .tag { position:absolute; left:0; top:0; background:#000; color:#fff; font:12px system-ui; padding:2px 8px; z-index:9; opacity:.75; }
</style></head><body>
<div id="report">measuring…</div>
__FRAMES__
<script>
const W=1920,H=1080, SIDE=128;
function measure(frame){
  const sec=frame.querySelector('section'), sr=sec.getBoundingClientRect();
  const cs=getComputedStyle(sec);
  const padB=parseFloat(cs.paddingBottom)||128;
  const limit=H-padB;
  const issues=[];
  let contentBottom=0, footerTop=H;
  for(const ch of sec.children){
    const st=getComputedStyle(ch);
    const r=ch.getBoundingClientRect();
    if(ch.tagName==='ASIDE') continue;
    if(st.position==='absolute'){ footerTop=Math.min(footerTop, r.top-sr.top); continue; }
    contentBottom=Math.max(contentBottom, r.bottom-sr.top);
  }
  if(contentBottom>limit+1) issues.push('content runs '+Math.round(contentBottom-limit)+'px past the bottom margin ('+Math.round(contentBottom)+' > '+limit+')');
  if(footerTop<H && contentBottom>footerTop-8) issues.push('content touches the footer ('+Math.round(contentBottom)+' vs footer at '+Math.round(footerTop)+')');
  let minFont=999, wide=0;
  for(const el of sec.querySelectorAll('*')){
    if(el.tagName==='ASIDE'||el.closest('aside')) continue;
    const r=el.getBoundingClientRect(), st=getComputedStyle(el);
    const hasText=[...el.childNodes].some(n=>n.nodeType===3&&n.textContent.trim());
    if(hasText){
      minFont=Math.min(minFont, parseFloat(st.fontSize));
      if(r.right-sr.left>W-SIDE+2 && st.position!=='absolute') wide++;
      if(el.scrollWidth>el.clientWidth+2 && ['P','H1','H2','H3','LI','TD','TH'].includes(el.tagName)) issues.push('text wider than its box in <'+el.tagName.toLowerCase()+'>: '+el.textContent.trim().slice(0,30));
    }
  }
  if(wide) issues.push(wide+' text element(s) past the right margin');
  if(minFont<24) issues.push('text smaller than 24px ('+minFont+'px)');
  const fill=Math.round(100*contentBottom/limit);
  if(fill<45) issues.push('slide is mostly empty (content reaches '+fill+'% of the usable height)');
  return {id:frame.dataset.id, contentBottom:Math.round(contentBottom), limit, fill, issues};
}
document.fonts.ready.then(()=>setTimeout(()=>{
  const rows=[...document.querySelectorAll('.frame')].map(measure);
  window.__deckReport=rows;
  const bad=rows.filter(r=>r.issues.length).length;
  document.getElementById('report').innerHTML=
    '<b>'+rows.length+' slides, '+bad+' with problems.</b><table><tr><th>#</th><th>Slide</th><th>Content bottom / limit</th><th>Problems</th></tr>'+
    rows.map((r,i)=>'<tr class="'+(r.issues.length?'bad':'ok')+'"><td>'+(i+1)+'</td><td>'+r.id+'</td><td>'+r.contentBottom+' / '+r.limit+'</td><td>'+(r.issues.join('; ')||'none')+'</td></tr>').join('')+'</table>';
},300));
</script></body></html>
"""


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    deck, out = Path(sys.argv[1]), Path(sys.argv[2])
    index = json.loads((deck / "project" / "deck.json").read_text(encoding="utf-8"))
    frames = []
    for i, sid in enumerate(index["order"], 1):
        if not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", sid):
            raise SystemExit(f"bad slide id: {sid}")
        html = (deck / "project" / "slides" / f"{sid}.html").read_text(encoding="utf-8")
        html = re.sub(r"<aside>.*?</aside>", "", html, flags=re.S)
        frames.append(f'<div class="frame" data-id="{sid}"><div class="tag">{i}. {sid}</div>{html}</div>')
    out.mkdir(parents=True, exist_ok=True)
    (out / "preview.html").write_text(PAGE.replace("__FRAMES__", "\n".join(frames)), encoding="utf-8")
    print(f"wrote {out / 'preview.html'} ({len(frames)} slides)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
