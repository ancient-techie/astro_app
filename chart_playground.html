<!DOCTYPE html>
<!-- data-lang drives every translated rule; the boot script below overwrites
     it from localStorage before the first paint, and this default keeps the
     page readable with JavaScript off. -->
<html lang="en" data-lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title data-i18n="pg.page_title">Play with Chart - Vedic Birth Chart</title>
<script>
  (function () {
    try {
      var saved = window.localStorage.getItem("vedic-chart-lang");
      if (saved === "en" || saved === "ta") {
        document.documentElement.setAttribute("data-lang", saved);
        document.documentElement.setAttribute("lang", saved);
      }
    } catch (err) {}
  })();
</script>
<!-- Same dictionaries the generator and admin pages use (served from
     i18n.py), so a term never differs between pages. -->
<script src="/i18n.js"></script>
<meta name="description" content="Drag-and-drop South Indian Rashi chart playground, pre-filled from your generated birth chart.">
<meta name="theme-color" content="#0b0d17">
<link rel="manifest" href="/manifest.json">
<link rel="icon" href="/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="VedicChart">
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Lato:wght@300;400;700&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box;margin:0;padding:0}
/* Shrinks fluidly as the window narrows (capped at the original 115px) so the
   chart grid and the Grahas palette - which both use it, palette tokens
   included - keep sitting side by side instead of the palette wrapping to a
   new row below the fold. */
:root{--cell:clamp(40px,calc((100vw - 267px) / 4),115px)}
body{min-height:100vh;background:#12111e;background-image:radial-gradient(ellipse at 20% 40%,#1a1535 0%,#0c1030 60%,#12111e 100%);display:flex;flex-direction:column;align-items:center;font-family:'Lato',sans-serif;color:#e0d5c5;padding:24px clamp(8px,4vw,16px) 80px}
/* TOP BAR */
.top-bar{width:100%;max-width:1100px;display:flex;align-items:center;justify-content:space-between;margin-bottom:16px;flex-wrap:wrap;gap:10px}
.top-bar-left,.top-bar-right{display:flex;align-items:center;gap:14px;flex-wrap:wrap}
h1{font-family:'Cinzel',serif;font-size:1.6rem;letter-spacing:.15em;color:#d4af37;text-shadow:0 0 24px rgba(212,175,55,.5)}
.back-link{font-family:'Cinzel',serif;font-size:.72rem;letter-spacing:.08em;padding:8px 18px;border-radius:20px;border:1.5px solid rgba(212,175,55,.5);background:rgba(212,175,55,.08);color:#e0c477;text-decoration:none;transition:all .2s;white-space:nowrap}
.back-link:hover{background:rgba(212,175,55,.18);border-color:#d4af37;color:#ffe060}
/* Language toggle - matches the control on the generator and admin pages. */
.lang-switch{flex-shrink:0;display:inline-flex;gap:2px;padding:3px;border:1.5px solid rgba(212,175,55,.45);border-radius:999px;background:rgba(212,175,55,.06)}
.lang-switch button{padding:5px 11px;font-family:'Cinzel',serif;font-size:11px;font-weight:700;letter-spacing:.04em;color:rgba(224,213,197,.7);background:transparent;border:none;border-radius:999px;cursor:pointer;white-space:nowrap;transition:background .15s,color .15s}
.lang-switch button:hover{color:#e0c477}
.lang-switch button.active{background:linear-gradient(135deg,#d4af37 0%,#f0d878 100%);color:#1c1710;box-shadow:0 2px 10px rgba(212,175,55,.35)}
.admin-link{font-family:'Cinzel',serif;font-size:.72rem;letter-spacing:.08em;padding:8px 18px;border-radius:20px;border:1.5px solid rgba(120,170,255,.5);background:rgba(90,140,255,.08);color:#a9c3ff;text-decoration:none;transition:all .2s;white-space:nowrap}
.admin-link:hover{background:rgba(90,140,255,.18);border-color:#7aa2ff;color:#cfe0ff}
.clear-btn{font-family:'Cinzel',serif;font-size:.72rem;letter-spacing:.08em;padding:8px 20px;border-radius:20px;border:1.5px solid rgba(255,80,60,.6);background:rgba(255,50,30,.1);color:#ff8877;cursor:pointer;transition:all .2s}
.clear-btn:hover{background:rgba(255,50,30,.22);border-color:#ff6655;color:#ffaa99}
/* CONTROLS */
.controls-bar{display:flex;align-items:center;gap:14px;background:rgba(255,255,255,.05);border:1px solid rgba(212,175,55,.25);border-radius:30px;padding:8px 22px;margin-bottom:22px;font-size:12px;color:rgba(220,210,180,.75);font-family:'Cinzel',serif;letter-spacing:.07em}
.controls-bar input[type=range]{-webkit-appearance:none;appearance:none;width:150px;height:4px;border-radius:2px;outline:none;cursor:pointer;background:linear-gradient(to right,#d4af37 0%,#d4af37 65%,rgba(255,255,255,.15) 65%)}
.controls-bar input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:14px;height:14px;border-radius:50%;background:#d4af37;box-shadow:0 0 6px rgba(212,175,55,.7);cursor:pointer}
.controls-bar input[type=range]::-moz-range-thumb{width:14px;height:14px;border-radius:50%;background:#d4af37;border:none;cursor:pointer}
.opacity-value{min-width:34px;color:#d4af37;font-weight:700;font-size:11px}
/* LAYOUT */
.main-layout{display:flex;gap:clamp(8px,3vw,28px);align-items:flex-start;flex-wrap:wrap;justify-content:center}
/* CHART */
/* --cell shrinks fluidly as the window narrows (capped at the original 115px)
   so the chart and the Grahas palette keep sitting side by side - instead of
   the palette wrapping to a new row and needing a scroll to reach it. */
.chart-wrapper{position:relative;padding:clamp(8px,4vw,26px)}
.chart-grid{display:grid;grid-template-columns:repeat(4,var(--cell));grid-template-rows:repeat(4,var(--cell));border:3px solid #7a5c10;background:#7a5c10;gap:2px;position:relative;box-shadow:0 0 50px rgba(212,175,55,.2),0 6px 30px rgba(0,0,0,.6)}
.cell{background:#c8bd9e;position:relative;overflow:visible;transition:background .4s ease;display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:var(--cell)}
.cell.empty{background:#0c0c1a;pointer-events:none}
.cell.active-drop{outline:2px dashed rgba(212,175,55,.9);outline-offset:-2px}
/* Tap-to-place mode (mobile alternative to drag-and-drop): once a palette
   planet is selected, every valid house gets a steady gold outline so it's
   obvious where a tap will land - no hover state needed. */
.chart-grid.selecting .cell:not(.empty){cursor:pointer;box-shadow:inset 0 0 0 2px rgba(212,175,55,.6);}
.chart-grid.selecting .cell:not(.empty):hover{box-shadow:inset 0 0 0 2px rgba(255,224,96,.95);}
.sign-label{position:absolute;bottom:4px;left:50%;transform:translateX(-50%);font-size:calc(var(--cell) * 0.0652);font-family:'Cinzel',serif;font-weight:700;letter-spacing:.04em;white-space:nowrap;pointer-events:none;z-index:2;color:#1a1000;background:rgba(255,242,200,.72);border-radius:3px;padding:1px 5px;box-shadow:0 0 0 1px rgba(160,120,30,.3)}
.house-number{position:absolute;font-size:max(8px,calc(var(--cell) * 0.0957));font-family:'Cinzel',serif;font-weight:700;color:#ffe060;text-shadow:0 1px 4px rgba(0,0,0,.95),0 0 8px rgba(0,0,0,.7);pointer-events:none;z-index:20;line-height:1}
.house-num-top{top:calc(var(--cell) * -0.1739);left:50%;transform:translateX(-50%)}
.house-num-right{right:calc(var(--cell) * -0.2087);top:50%;transform:translateY(-50%)}
.house-num-bottom{bottom:calc(var(--cell) * -0.1739);left:50%;transform:translateX(-50%)}
.house-num-left{left:calc(var(--cell) * -0.2087);top:50%;transform:translateY(-50%)}
.planets-container{display:flex;flex-wrap:wrap;gap:max(1px,calc(var(--cell) * 0.0261));padding:calc(var(--cell) * 0.0348) calc(var(--cell) * 0.0348) calc(var(--cell) * 0.1739);z-index:4;position:relative;justify-content:center;align-items:center}
.planet-token{display:inline-flex;align-items:center;justify-content:center;padding:calc(var(--cell) * 0.0261) calc(var(--cell) * 0.0609);border-radius:4px;font-size:max(7px,calc(var(--cell) * 0.087));font-weight:700;font-family:'Cinzel',serif;cursor:grab;user-select:none;transition:transform .15s,box-shadow .15s;position:relative;z-index:10;white-space:nowrap;box-shadow:0 1px 5px rgba(0,0,0,.5)}
.planet-token:hover{transform:scale(1.1);box-shadow:0 3px 10px rgba(0,0,0,.6)}
.planet-token:active{cursor:grabbing}
.planet-token.dragging{opacity:.3}
/* Selected in the palette, waiting for a tap on a house */
.planet-token.token-selected{outline:2px solid #ffe060;outline-offset:2px;box-shadow:0 0 10px rgba(255,224,96,.85) !important;transform:scale(1.1);}
/* Placed on the chart and armed with its remove (x) button */
.planet-token.token-armed{z-index:25;}
.token-remove-btn{
  position:absolute;top:-7px;right:-7px;z-index:30;
  width:15px;height:15px;padding:0;border-radius:50%;
  display:flex;align-items:center;justify-content:center;
  background:#ff3b30;color:#fff;font-family:'Lato',sans-serif;
  font-size:11px;font-weight:900;line-height:1;
  border:1.5px solid rgba(255,255,255,.85);
  box-shadow:0 2px 6px rgba(0,0,0,.6);
  cursor:pointer;
}
.token-remove-btn:hover{background:#ff6655;}
.token-remove-btn:active{transform:scale(0.9);}
svg.rays-overlay{position:absolute;pointer-events:none;z-index:6;top:0;left:0;width:100%;height:100%}
/* PALETTE */
.palette{background:rgba(255,255,255,.04);border:1px solid rgba(212,175,55,.3);border-radius:12px;padding:clamp(8px,3vw,18px) clamp(6px,2.5vw,14px);min-width:clamp(70px,22vw,115px);box-shadow:0 0 20px rgba(0,0,0,.4)}
.palette h3{font-family:'Cinzel',serif;font-size:clamp(.6rem,2.4vw,.82rem);color:#d4af37;text-align:center;margin-bottom:clamp(6px,2vw,12px);letter-spacing:.1em}
.palette-slot{display:flex;align-items:center;justify-content:center;margin-bottom:7px;min-height:32px}
.legend{margin-top:clamp(8px,2.5vw,14px);font-size:clamp(7px,2vw,10px);color:rgba(220,215,200,.45);text-align:center;line-height:1.8}
/* DASHBOARD */
.dashboard-container{width:100%;max-width:1100px;margin-top:32px}
.dash-tabs{display:flex;gap:0;flex-wrap:wrap}
.dash-tab{flex:1;min-width:80px;padding:10px 6px;text-align:center;font-family:'Cinzel',serif;font-size:.65rem;letter-spacing:.06em;cursor:pointer;border:1px solid rgba(212,175,55,.2);background:rgba(255,255,255,.03);color:rgba(212,175,55,.5);transition:all .2s;border-bottom:none;border-radius:8px 8px 0 0}
.dash-tab.active-tab{background:rgba(255,255,255,.07);font-weight:700}
.dash-tab.tab-good.active-tab{color:#44dd88;border-top:2px solid #44dd88}
.dash-tab.tab-bad.active-tab{color:#ff6655;border-top:2px solid #ff4444}
.dash-tab.tab-well.active-tab{color:#d4af37;border-top:2px solid #d4af37}
.dash-tab.tab-plan.active-tab{color:#cc88ff;border-top:2px solid #cc88ff}
.dash-tab.tab-stana.active-tab{color:#55ccff;border-top:2px solid #55ccff}
.dash-tab.tab-dig.active-tab{color:#ff99aa;border-top:2px solid #ff99aa}
.dash-tab.tab-total.active-tab{color:#ffcc44;border-top:2px solid #ffcc44}
.dashboard{background:rgba(255,255,255,.03);border:1px solid rgba(212,175,55,.2);border-radius:0 0 14px 14px;padding:20px 20px;box-shadow:0 0 30px rgba(0,0,0,.4)}
.dashboard h2{font-family:'Cinzel',serif;font-size:.95rem;letter-spacing:.12em;margin-bottom:16px;text-align:center}
.dashboard h2.good-title{color:#44dd88} .dashboard h2.bad-title{color:#ff6655}
.dashboard h2.well-title{color:#d4af37} .dashboard h2.plan-title{color:#cc88ff}
.dashboard h2.stana-title{color:#55ccff} .dashboard h2.dig-title{color:#ff99aa}
.dashboard h2.total-title{color:#ffcc44}
.dash-sections{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:14px}
.dash-section{background:rgba(255,255,255,.04);border:1px solid rgba(212,175,55,.1);border-radius:10px;padding:14px}
.dash-section h3{font-family:'Cinzel',serif;font-size:.65rem;letter-spacing:.1em;margin-bottom:10px;text-transform:uppercase;border-bottom:1px solid rgba(212,175,55,.1);padding-bottom:6px}
.dash-section h3.good-h3{color:rgba(68,221,136,.85)} .dash-section h3.bad-h3{color:rgba(255,80,70,.85)}
.dash-section h3.well-h3{color:rgba(212,175,55,.85)} .dash-section h3.plan-h3{color:rgba(204,136,255,.85)}
.dash-section h3.stana-h3{color:rgba(85,204,255,.85)} .dash-section h3.dig-h3{color:rgba(255,153,170,.85)}
.dash-section h3.total-h3{color:rgba(255,204,68,.85)}
.dash-row{display:flex;align-items:center;gap:8px;margin-bottom:7px;font-size:11px}
.dash-label{min-width:92px;color:rgba(220,210,180,.8);font-family:'Cinzel',serif;font-size:10px}
.dash-bar-wrap{flex:1;height:8px;background:rgba(255,255,255,.08);border-radius:4px;overflow:hidden}
.dash-bar{height:100%;border-radius:4px;transition:width .5s ease}
.dash-pct{min-width:38px;text-align:right;font-size:10px;font-weight:700}
.dash-pct.good-pct{color:#44dd88} .dash-pct.bad-pct{color:#ff6655} .dash-pct.well-pct{color:#d4af37}
.dash-tag{display:inline-block;padding:1px 6px;border-radius:10px;font-size:9px;font-weight:700;font-family:'Cinzel',serif;vertical-align:middle}
.el-fire{color:#ff6633} .el-earth{color:#88aa44} .el-air{color:#66bbff} .el-water{color:#4499dd}
.badge-fire{background:rgba(255,80,20,.2);color:#ff7744;border:1px solid rgba(255,80,20,.35)}
.badge-earth{background:rgba(100,140,40,.2);color:#99bb55;border:1px solid rgba(100,140,40,.35)}
.badge-air{background:rgba(80,160,220,.2);color:#77ccff;border:1px solid rgba(80,160,220,.35)}
.badge-water{background:rgba(40,100,200,.2);color:#55aaee;border:1px solid rgba(40,100,200,.35)}
.badge-movable{background:rgba(220,60,60,.15);color:#ff9988;border:1px solid rgba(220,60,60,.3)}
.badge-fixed{background:rgba(80,80,200,.15);color:#aabbff;border:1px solid rgba(80,80,200,.3)}
.badge-mutable{background:rgba(60,180,100,.15);color:#88ffbb;border:1px solid rgba(60,180,100,.3)}
.badge-east{background:rgba(240,100,30,.15);color:#ff8855;border:1px solid rgba(240,100,30,.3)}
.badge-south{background:rgba(30,160,80,.15);color:#55dd88;border:1px solid rgba(30,160,80,.3)}
.badge-west{background:rgba(80,120,220,.15);color:#88aaff;border:1px solid rgba(80,120,220,.3)}
.badge-north{background:rgba(220,180,40,.15);color:#eecc55;border:1px solid rgba(220,180,40,.3)}
.signs-table{width:100%;border-collapse:collapse;font-size:10px}
.signs-table th{font-family:'Cinzel',serif;font-size:8px;text-align:left;padding:3px 4px;border-bottom:1px solid rgba(212,175,55,.12)}
.signs-table td{padding:4px 4px;color:rgba(220,210,180,.8);border-bottom:1px solid rgba(255,255,255,.04)}
.signs-table tr:hover td{background:rgba(255,255,255,.03)}
.no-data{color:rgba(220,210,180,.3);font-style:italic;font-size:10px;text-align:center;padding:14px 0}
.dash-panel{display:none} .dash-panel.active-panel{display:block}
.dash-tab.tab-sigcol.active-tab{color:#aaffdd;border-top:2px solid #aaffdd}
.dashboard h2.sigcol-title{color:#aaffdd}
.dash-section h3.sigcol-h3{color:rgba(170,255,221,.85)}
.sign-color-card{
  background:rgba(255,255,255,.04);border:1px solid rgba(170,255,221,.1);
  border-radius:10px;padding:12px 14px;
}
.sign-color-row{
  display:flex;align-items:center;gap:10px;
  padding:7px 0;border-bottom:1px solid rgba(255,255,255,.05);
}
.sign-color-row:last-child{border-bottom:none}
.sign-swatch{
  width:36px;height:36px;border-radius:6px;flex-shrink:0;
  border:1px solid rgba(255,255,255,.18);
  box-shadow:0 2px 6px rgba(0,0,0,.4);
}
.sign-color-info{flex:1;min-width:0}
.sign-name{
  font-family:'Cinzel',serif;font-size:10px;font-weight:700;
  margin-bottom:2px;
}
.sign-color-layers{
  display:flex;flex-wrap:wrap;gap:4px;align-items:center;
}
.sign-color-chip{
  display:inline-flex;align-items:center;gap:3px;
  padding:1px 6px;border-radius:10px;
  font-size:8.5px;font-weight:700;font-family:'Cinzel',serif;
}
.sign-color-chip .chip-dot{
  width:7px;height:7px;border-radius:50%;flex-shrink:0;
}
.sign-color-hex{
  font-size:8px;color:rgba(200,195,175,.45);
  margin-top:1px;letter-spacing:.04em;
}

/* ── PALETTE PLACEHOLDER ── */
.palette-placeholder{
  display:flex;align-items:center;justify-content:center;
  width:100%;min-height:24px;padding:3px 4px;
  font-family:'Cinzel',serif;font-size:8.5px;letter-spacing:.04em;
  color:#ffe060;
  border:1px dashed rgba(212,175,55,.18);
  border-radius:4px;font-style:italic;
}


/* ── PALETTE CHECKBOXES ── */
.cb-header-row{
  display:grid;grid-template-columns:1fr clamp(14px,4vw,22px) clamp(14px,4vw,22px);
  align-items:center;gap:clamp(2px,1vw,3px);
  padding:4px 2px 6px;
  border-bottom:1px solid rgba(212,175,55,.18);
  margin-bottom:6px;
}
.cb-header-label{
  font-family:'Cinzel',serif;font-size:clamp(6px,1.8vw,8px);letter-spacing:.06em;
  color:rgba(212,175,55,.55);text-transform:uppercase;
}
.cb-col-label{
  font-size:clamp(7px,2vw,9px);text-align:center;color:rgba(212,175,55,.55);
  font-weight:700;cursor:default;
  user-select:none;line-height:1;
}
.palette-row{
  display:grid;grid-template-columns:1fr clamp(14px,4vw,22px) clamp(14px,4vw,22px);
  align-items:center;gap:clamp(2px,1vw,3px);
  margin-bottom:6px;min-height:28px;
}
.palette-token-cell{display:flex;align-items:center;justify-content:flex-start;}
.cb-cell{display:flex;align-items:center;justify-content:center;}

/* Custom checkbox styling */
.cb-arrow, .cb-color{
  -webkit-appearance:none;appearance:none;
  width:clamp(10px,3vw,13px);height:clamp(10px,3vw,13px);border-radius:3px;
  cursor:pointer;position:relative;
  flex-shrink:0;transition:all .15s;
}
.cb-arrow{
  border:1.5px solid rgba(180,210,255,.5);
  background:rgba(100,160,255,.08);
}
.cb-arrow:checked{
  background:#5599ff;
  border-color:#88bbff;
  box-shadow:0 0 5px rgba(85,153,255,.5);
}
.cb-color{
  border:1.5px solid rgba(255,200,100,.4);
  background:rgba(255,180,50,.06);
}
.cb-color:checked{
  background:#d4af37;
  border-color:#ffe060;
  box-shadow:0 0 5px rgba(212,175,55,.5);
}
.cb-arrow:checked::after,.cb-color:checked::after{
  content:'✓';position:absolute;top:50%;left:50%;
  transform:translate(-50%,-50%);
  font-size:9px;font-weight:900;color:#fff;line-height:1;
}
/* Master checkboxes (slightly larger) */
.cb-master{
  -webkit-appearance:none;appearance:none;
  width:clamp(11px,3.2vw,15px);height:clamp(11px,3.2vw,15px);border-radius:3px;
  cursor:pointer;position:relative;
  flex-shrink:0;transition:all .15s;
}
.cb-master-arrow{border:1.5px solid rgba(180,210,255,.6);background:rgba(100,160,255,.1);}
.cb-master-arrow:checked{background:#3377ee;border-color:#88bbff;box-shadow:0 0 6px rgba(85,153,255,.6);}
.cb-master-color{border:1.5px solid rgba(255,200,100,.5);background:rgba(255,180,50,.08);}
.cb-master-color:checked{background:#b8920a;border-color:#ffe060;box-shadow:0 0 6px rgba(212,175,55,.6);}
.cb-master:checked::after{
  content:'✓';position:absolute;top:50%;left:50%;
  transform:translate(-50%,-50%);
  font-size:10px;font-weight:900;color:#fff;line-height:1;
}
.cb-master:indeterminate::after{
  content:'–';position:absolute;top:50%;left:50%;
  transform:translate(-50%,-50%);
  font-size:11px;font-weight:900;color:#fff;line-height:1;
}
/* ── COMPARE MODE ─────────────────────────────────────────────────────
   The whole chart UI (controls, grid, palette, dashboards) lives in a
   <template> and is stamped out once per chart, so a second chart is a
   second independent instance rather than a second copy of the code.
   Single mode = one panel at the original size; compare mode = two
   panels side by side, each with its own palette, rays and dashboards. */
.compare-btn{font-family:'Cinzel',serif;font-size:.72rem;letter-spacing:.08em;padding:8px 18px;border-radius:20px;border:1.5px solid rgba(120,255,210,.45);background:rgba(60,220,180,.08);color:#8ff0d2;cursor:pointer;transition:all .2s;white-space:nowrap}
.compare-btn:hover{background:rgba(60,220,180,.2);border-color:#5fe0c0;color:#c8fff0}
.compare-btn[aria-pressed="true"]{background:linear-gradient(135deg,#2fbf9c 0%,#7ff0d0 100%);border-color:#9cffe4;color:#06201a;font-weight:700;box-shadow:0 2px 12px rgba(60,220,180,.35)}

/* Compare toolbar - only meaningful with two charts on screen. */
.compare-bar{display:none;align-items:center;justify-content:center;gap:10px;flex-wrap:wrap;width:100%;max-width:1100px;margin:0 auto 18px;padding:8px 16px;border:1px solid rgba(120,255,210,.25);border-radius:26px;background:rgba(60,220,180,.06)}
body.compare .compare-bar{display:flex}
.cmp-action{font-family:'Cinzel',serif;font-size:.64rem;letter-spacing:.06em;padding:6px 14px;border-radius:16px;border:1px solid rgba(212,175,55,.4);background:rgba(212,175,55,.08);color:#e0c477;cursor:pointer;transition:all .18s;white-space:nowrap}
.cmp-action:hover{background:rgba(212,175,55,.2);border-color:#d4af37;color:#ffe060}
.cmp-sync{display:inline-flex;align-items:center;gap:6px;font-family:'Cinzel',serif;font-size:.62rem;letter-spacing:.06em;color:rgba(220,210,180,.75);cursor:pointer;user-select:none}
.cmp-sync input{-webkit-appearance:none;appearance:none;width:13px;height:13px;border-radius:3px;border:1.5px solid rgba(120,255,210,.5);background:rgba(60,220,180,.08);cursor:pointer;position:relative}
.cmp-sync input:checked{background:#3fd8b4;border-color:#9cffe4}
.cmp-sync input:checked::after{content:'✓';position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);font-size:9px;font-weight:900;color:#06201a;line-height:1}

/* Panel shell */
.panels{width:100%;display:flex;gap:clamp(10px,2vw,22px);align-items:flex-start;justify-content:center;flex-wrap:wrap}
.panel{display:flex;flex-direction:column;align-items:center;width:100%;max-width:1100px;min-width:0}
.panel[hidden]{display:none}
.panel-head{display:flex;align-items:center;justify-content:center;gap:12px;flex-wrap:wrap;margin-bottom:18px}
.panel-badge{display:none;font-family:'Cinzel',serif;font-size:.72rem;font-weight:700;letter-spacing:.12em;padding:6px 16px;border-radius:18px;white-space:nowrap}
body.compare .panel-badge{display:inline-block}
.panel-a .panel-badge{color:#ffe060;border:1.5px solid rgba(212,175,55,.6);background:rgba(212,175,55,.12)}
.panel-b .panel-badge{color:#9fd0ff;border:1.5px solid rgba(120,170,255,.6);background:rgba(90,140,255,.12)}
body.compare .panel{flex:1 1 460px;max-width:none;border:1px solid rgba(255,255,255,.07);border-radius:16px;padding:14px clamp(6px,1.2vw,14px) 18px;background:rgba(255,255,255,.015)}
/* The coloured top rail matches each panel's badge, so it stays obvious which
   half you are editing once both charts are full of planets. */
body.compare .panel-a{border-top:2px solid rgba(212,175,55,.55)}
body.compare .panel-b{border-top:2px solid rgba(120,170,255,.55)}
/* Two charts share the viewport, so the cell (and everything sized off it)
   shrinks to roughly half the single-chart budget. */
body.compare .panel{--cell:clamp(28px,calc((50vw - 340px) / 4),104px)}
body.compare .palette{min-width:clamp(62px,11vw,104px);max-width:190px;padding:clamp(6px,1.4vw,14px) clamp(5px,1.2vw,11px)}
body.compare .palette h3{font-size:clamp(.55rem,1.2vw,.78rem)}
/* The chart, its gutter and the palette all give up a little room so the two
   stay side by side on a laptop instead of the palette dropping below. A flex
   line wraps on the item's natural width, so the palette needs a max-width -
   its legend sentence would otherwise claim ~250px and push itself down. */
body.compare .main-layout{gap:clamp(6px,1.2vw,14px)}
body.compare .chart-wrapper{padding:clamp(6px,1.4vw,16px)}
body.compare .cb-header-row,
body.compare .palette-row{grid-template-columns:1fr clamp(13px,1.6vw,18px) clamp(13px,1.6vw,18px)}
body.compare .controls-bar{padding:6px 16px;font-size:11px;margin-bottom:0}
body.compare .controls-bar input[type=range]{width:104px}
body.compare .dash-tab{font-size:.58rem;min-width:64px;padding:8px 4px}
body.compare .dashboard{padding:16px 14px}
body.compare .dash-sections{grid-template-columns:repeat(auto-fit,minmax(170px,1fr))}
.panel .controls-bar{margin-bottom:0}
.panel .dashboard-container{width:100%;margin-top:26px}
/* The ray-opacity control wraps its own slider, so no id/for pair is needed
   for a label that now exists once per panel. */
.ray-ctl{display:inline-flex;align-items:center;gap:12px;cursor:pointer}
/* Phone width: the opacity control, the chart badge and Clear share one row,
   so let that row (and the control itself) wrap instead of running off the
   side of the screen. */
@media (max-width:560px){
  .panel-head{max-width:100%}
  .controls-bar{flex-wrap:wrap;justify-content:center;max-width:100%;padding:8px 14px}
  .controls-bar input[type=range]{width:min(150px,42vw)}
  .ray-ctl{flex-wrap:wrap;justify-content:center}
  .compare-bar{padding:8px 10px;border-radius:18px}
}
/* Below this width two charts side by side would be unreadable, so compare
   mode stacks them - still two full, independent charts. */
@media (max-width:900px){
  body.compare .panels{flex-direction:column;align-items:center}
  body.compare .panel{flex:1 1 auto;width:100%;--cell:clamp(38px,calc((100vw - 300px) / 4),106px)}
  body.compare .palette{min-width:clamp(70px,22vw,115px)}
}
</style>
</head>
<body>

<div class="top-bar">
  <div class="top-bar-left">
    <a class="back-link" href="/">← <span data-i18n="pg.back">Back to Generator</span></a>
    <h1>✦ <span data-i18n="pg.title">South Indian Birth Chart</span> ✦</h1>
  </div>
  <div class="top-bar-right">
    <div class="lang-switch" role="group" aria-label="Language">
      <button type="button" data-lang-btn="en" aria-pressed="true">English</button>
      <button type="button" data-lang-btn="ta" aria-pressed="false">&#2980;&#2990;&#3007;&#2996;&#3021;</button>
    </div>
    <a class="admin-link" href="/admin">⚙ <span data-i18n="nav.admin">Admin</span></a>
    <button type="button" class="compare-btn" id="compareToggle" aria-pressed="false">⇄ <span id="compareToggleLabel" data-i18n="pg.compare">Compare Charts</span></button>
  </div>
</div>

<!-- Compare toolbar - only shown while two charts are on screen. -->
<div class="compare-bar" id="compareBar" role="group" aria-label="Compare charts">
  <button type="button" class="cmp-action" id="copyAB" data-i18n="pg.copy_a_b">Copy A &#8594; B</button>
  <button type="button" class="cmp-action" id="copyBA" data-i18n="pg.copy_b_a">Copy B &#8594; A</button>
  <button type="button" class="cmp-action" id="swapAB" data-i18n="pg.swap_ab">Swap A &#8644; B</button>
  <label class="cmp-sync" title="Keep both charts on the same dashboard tab" data-i18n-attr="title:pg.sync_tabs_title">
    <input type="checkbox" id="syncTabs" checked>
    <span data-i18n="pg.sync_tabs">Sync tabs</span>
  </label>
</div>

<!-- One panel in single mode, two side by side in compare mode. Both are
     stamped from #panelTpl and driven by their own ChartInstance. -->
<div class="panels" id="panels"></div>

<!-- ═══ CHART PANEL TEMPLATE ═══════════════════════════════════════════
     Everything here used to sit directly in the body with unique ids. It is
     a template now because compare mode needs a second, fully independent
     copy - so ids became classes / data-attributes that each instance looks
     up inside its own root element. -->
<template id="panelTpl">
  <section class="panel">
    <div class="panel-head">
      <span class="panel-badge"></span>
      <div class="controls-bar">
        <label class="ray-ctl">&#10230; <span data-i18n="pg.ray_opacity">Aspect Ray Opacity</span>
          <input type="range" class="ray-opacity" min="0" max="100" value="65">
        </label>
        <span class="opacity-value">65%</span>
      </div>
      <button type="button" class="clear-btn js-clear">&#10227; <span data-i18n="pg.clear">Clear Chart</span></button>
    </div>

    <div class="main-layout">
      <div class="chart-wrapper">
        <div class="chart-grid"></div>
        <svg class="rays-overlay" xmlns="http://www.w3.org/2000/svg"></svg>
      </div>
      <div class="palette">
        <h3 data-i18n="pg.grahas">Grahas</h3>
        <div class="cb-header-row">
          <div class="cb-header-label" data-i18n="pg.col_planet">Planet</div>
          <div class="cb-col-label" title="Show aspect arrows" data-i18n-attr="title:pg.col_arrow_title">&#8599;</div>
          <div class="cb-col-label" title="Show sign colors" data-i18n-attr="title:pg.col_color_title">&#9679;</div>
        </div>
        <div class="cb-header-row" style="border-bottom:1px solid rgba(212,175,55,.12);margin-bottom:8px;padding-bottom:8px;">
          <div style="font-family:Cinzel,serif;font-size:8px;color:rgba(212,175,55,.45);padding-left:2px;" data-i18n="pg.all">All</div>
          <div class="cb-cell"><input type="checkbox" class="cb-master cb-master-arrow" checked></div>
          <div class="cb-cell"><input type="checkbox" class="cb-master cb-master-color" checked></div>
        </div>
        <div class="palette-list"></div>
        <!-- Filled in by refreshStaticText(): the string interpolates the Asc
             token, so it can't ride on a plain data-i18n attribute. -->
        <div class="legend">Drag planets into chart, or tap one then tap a house.<br>Tap a placed planet to remove it.<br><br><span style="color:#d4af37">Asc</span> = house 1.</div>
      </div>
    </div>

    <div class="dashboard-container">
      <div class="dash-tabs">
        <div class="dash-tab tab-good active-tab" data-tab="good">&#10022; <span data-i18n="pg.tab_good">Goodness</span></div>
        <div class="dash-tab tab-bad"  data-tab="bad">&#9789; <span data-i18n="pg.tab_bad">Badness</span></div>
        <div class="dash-tab tab-well" data-tab="well">&#8853; <span data-i18n="pg.tab_well">Wellness</span></div>
        <div class="dash-tab tab-plan" data-tab="plan">&#9775; <span data-i18n="pg.tab_plan">Subathuva</span></div>
        <div class="dash-tab tab-stana" data-tab="stana">&#9733; <span data-i18n="pg.tab_stana">Stana Bala</span></div>
        <div class="dash-tab tab-dig"  data-tab="dig">&#9672; <span data-i18n="pg.tab_dig">Dig+Nish Bala</span></div>
        <div class="dash-tab tab-total" data-tab="total">&#8859; <span data-i18n="pg.tab_total">Total Strength</span></div>
        <div class="dash-tab tab-sigcol" data-tab="sigcol">&#127912; <span data-i18n="pg.tab_sigcol">Sign Colors</span></div>
      </div>
      <div class="dashboard">
        <div class="dash-panel active-panel" data-panel="good">
          <h2 class="good-title">&#10022; <span data-i18n="pg.panel_good">Goodness Dashboard</span> &#10022;</h2>
          <div class="dash-sections" data-sections="good"><div class="no-data" style="grid-column:1/-1" data-i18n="pg.no_data">Place planets to see analysis.</div></div>
        </div>
        <div class="dash-panel" data-panel="bad">
          <h2 class="bad-title">&#9789; <span data-i18n="pg.panel_bad">Badness Dashboard</span> &#9789;</h2>
          <div class="dash-sections" data-sections="bad"><div class="no-data" style="grid-column:1/-1" data-i18n="pg.no_data">Place planets to see analysis.</div></div>
        </div>
        <div class="dash-panel" data-panel="well">
          <h2 class="well-title">&#8853; <span data-i18n="pg.panel_well">Wellness Dashboard</span> &#8853;</h2>
          <div class="dash-sections" data-sections="well"><div class="no-data" style="grid-column:1/-1" data-i18n="pg.no_data">Place planets to see analysis.</div></div>
        </div>
        <div class="dash-panel" data-panel="plan">
          <h2 class="plan-title">&#9775; <span data-i18n="pg.panel_plan">Subathuva &#8212; Planet Wellness</span> &#9775;</h2>
          <div class="dash-sections" data-sections="plan"><div class="no-data" style="grid-column:1/-1" data-i18n="pg.no_data">Place planets to see analysis.</div></div>
        </div>
        <div class="dash-panel" data-panel="stana">
          <h2 class="stana-title">&#9733; <span data-i18n="pg.panel_stana">Stana Bala (Positional Strength)</span> &#9733;</h2>
          <div class="dash-sections" data-sections="stana"><div class="no-data" style="grid-column:1/-1" data-i18n="pg.no_data">Place planets to see analysis.</div></div>
        </div>
        <div class="dash-panel" data-panel="dig">
          <h2 class="dig-title">&#9672; <span data-i18n="pg.panel_dig">Dig Bala + Nish Bala</span> &#9672;</h2>
          <div class="dash-sections" data-sections="dig"><div class="no-data" style="grid-column:1/-1" data-i18n="pg.no_data">Place planets to see analysis.</div></div>
        </div>
        <div class="dash-panel" data-panel="total">
          <h2 class="total-title">&#8859; <span data-i18n="pg.panel_total">Total Planet Strength</span> &#8859;</h2>
          <div class="dash-sections" data-sections="total"><div class="no-data" style="grid-column:1/-1" data-i18n="pg.no_data">Place planets to see analysis.</div></div>
        </div>
        <div class="dash-panel" data-panel="sigcol">
          <h2 class="sigcol-title">&#127912; <span data-i18n="pg.panel_sigcol">Sign Color Breakdown</span> &#127912;</h2>
          <div data-sections="sigcol"><div class="no-data" data-i18n="pg.no_data_colors">Place planets to see sign colors.</div></div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
// ═══════════════════════════════════════════════════
//  TRANSLATION SHORTHANDS
// ═══════════════════════════════════════════════════
// Every identifier below stays English - SIGNS, the planet codes, the score
// keys - so all the astrology maths is unchanged. Only the strings that
// reach the DOM go through these, at render time.
const T  = (key, params) => I18N.t(key, params);            // UI string
const PN = (code) => I18N.term('pg_planet', code);          // full planet name
const PA = (code) => I18N.term('pg_planet_abbr', code);     // chart-token label
const SN = (sign) => I18N.term('sign', sign);               // rashi name

// First `n` *graphemes* of a string. Plain .slice() counts UTF-16 units, so
// it can strip the pulli off a Tamil cluster and leave "கும" where "கும்"
// was meant; Intl.Segmenter keeps each cluster whole.
const _segmenter = typeof Intl!=='undefined' && Intl.Segmenter
  ? new Intl.Segmenter(undefined,{granularity:'grapheme'}) : null;
function shortLabel(text,n){
  if(!_segmenter) return text.slice(0,n);
  return [..._segmenter.segment(text)].slice(0,n).map(s=>s.segment).join('');
}
const EL = (el)   => I18N.term('element', el);
const MO = (m)    => I18N.term('modality', m);
const DI = (d)    => I18N.term('direction', d);

// Score "sources" are built as compact tokens like "Jup(+30)" or
// "Sat(Ketu-mitig,-12)". Rather than thread translation through the scoring
// maths, the planet code and the handful of qualifier words are swapped here,
// at the point the string is displayed.
const SRC_WORDS={
  'Moon-dark-self':'pg.src_moon_dark_self',
  'Moon-dark':'pg.src_moon_dark',
  'Moon-self':'pg.src_moon_self',
  'Ketu-mitig':'pg.src_ketu_mitig',
};
function SRC(text){
  if(!text) return text;
  let out=text;
  // Longest first, so "Moon-dark-self" isn't half-matched by "Moon-dark".
  Object.keys(SRC_WORDS).sort((a,b)=>b.length-a.length).forEach(word=>{
    out=out.split(word).join(T(SRC_WORDS[word]));
  });
  out=out.replace(/\bMoon\b/g,PN('Mon'));
  ['Sun','Mon','Mar','Mer','Jup','Ven','Sat','Rahu','Ketu'].forEach(code=>{
    out=out.replace(new RegExp('\\b'+code+'\\b','g'),PA(code));
  });
  return out;
}
const SRCLIST=(arr)=>arr.map(SRC).join(', ');

// ═══════════════════════════════════════════════════
//  SIGN / PLANET METADATA
// ═══════════════════════════════════════════════════
const SIGNS=['Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces'];
const GRID_SIGNS=['Pisces','Aries','Taurus','Gemini','Aquarius',null,null,'Cancer','Capricorn',null,null,'Leo','Sagittarius','Scorpio','Libra','Virgo'];
const SIGN_ELEMENT={Aries:'fire',Leo:'fire',Sagittarius:'fire',Taurus:'earth',Virgo:'earth',Capricorn:'earth',Gemini:'air',Libra:'air',Aquarius:'air',Cancer:'water',Scorpio:'water',Pisces:'water'};
const SIGN_MODALITY={Aries:'movable',Cancer:'movable',Libra:'movable',Capricorn:'movable',Taurus:'fixed',Leo:'fixed',Scorpio:'fixed',Aquarius:'fixed',Gemini:'mutable',Virgo:'mutable',Sagittarius:'mutable',Pisces:'mutable'};
const ELEMENT_DIRECTION={fire:'east',earth:'south',air:'west',water:'north'};
const DEFAULT_BG='#c8bd9e';
const SIGN_BASE_SCORE=50; // every sign starts with 50 neutral points

// ── STANA BALA TABLES ──────────────────────────────
// exaltation=100, moola-trikona=80, own=60, friend=40, neutral=30, enemy=20, debilitation=0
const EXALTATION={Sun:'Aries',Mon:'Taurus',Mar:'Capricorn',Jup:'Cancer',Sat:'Libra',Ven:'Pisces',Mer:'Virgo',Rahu:'Gemini',Ketu:'Sagittarius'};
const DEBILITATION={Sun:'Libra',Mon:'Scorpio',Mar:'Cancer',Jup:'Capricorn',Sat:'Aries',Ven:'Virgo',Mer:'Pisces',Rahu:'Sagittarius',Ketu:'Gemini'};
// Moola Trikona: a portion of own sign with elevated status
const MOOLA_TRIKONA={Sun:'Leo',Mon:'Taurus',Mar:'Aries',Jup:'Sagittarius',Sat:'Aquarius',Ven:'Libra',Mer:'Virgo'};
// Ownership (primary)
const OWN_SIGN={Sun:['Leo'],Mon:['Cancer'],Mar:['Aries','Scorpio'],Jup:['Sagittarius','Pisces'],Sat:['Capricorn','Aquarius'],Ven:['Taurus','Libra'],Mer:['Gemini','Virgo'],Rahu:['Gemini'],Ketu:['Sagittarius']};
// Friend / Neutral / Enemy relationships (classic Jyotish)
// Returns 'friend','neutral','enemy' for planet in sign
const FRIEND_SIGNS={
  Sun:   {friends:['Moon','Mars','Jupiter'],   neutrals:['Mercury'],          enemies:['Venus','Saturn']},
  Mon:   {friends:['Sun','Mercury'],            neutrals:['Mars','Jupiter','Venus','Saturn'], enemies:[]},
  Mar:   {friends:['Sun','Moon','Jupiter'],     neutrals:['Venus','Saturn'],   enemies:['Mercury']},
  Jup:   {friends:['Sun','Moon','Mars'],        neutrals:['Saturn'],           enemies:['Mercury','Venus']},
  Sat:   {friends:['Mercury','Venus'],          neutrals:['Jupiter'],          enemies:['Sun','Moon','Mars']},
  Ven:   {friends:['Mercury','Saturn'],         neutrals:['Mars','Jupiter'],   enemies:['Sun','Moon']},
  Mer:   {friends:['Sun','Venus'],              neutrals:['Mars','Jupiter','Saturn'], enemies:['Moon']},
};
// Sign lords
const SIGN_LORD={Aries:'Mar',Taurus:'Ven',Gemini:'Mer',Cancer:'Mon',Leo:'Sun',Virgo:'Mer',Libra:'Ven',Scorpio:'Mar',Sagittarius:'Jup',Capricorn:'Sat',Aquarius:'Sat',Pisces:'Jup'};

function getStanaBala(planet, sign) {
  if(planet==='Asc') return {score:0,label:'—'};
  if(sign===EXALTATION[planet]) return {score:100,label:'Exaltation'};
  if(sign===DEBILITATION[planet]) return {score:0,label:'Debilitation'};
  if(MOOLA_TRIKONA[planet]===sign) return {score:80,label:'Moola Trikona'};
  const ownSigns=OWN_SIGN[planet]||[];
  if(ownSigns.includes(sign)) return {score:60,label:'Own Sign'};
  // For Rahu/Ketu no friendship table
  if(planet==='Rahu'||planet==='Ketu') return {score:30,label:'Neutral'};
  const lord=SIGN_LORD[sign];
  const rel=FRIEND_SIGNS[planet];
  if(!rel) return {score:30,label:'Neutral'};
  // Jupiter and Saturn — neutral to each other
  if((planet==='Jup'&&lord==='Sat')||(planet==='Sat'&&lord==='Jup')) return {score:30,label:'Neutral (Jup/Sat)'};
  const planetName={Sun:'Sun',Mon:'Moon',Mar:'Mars',Jup:'Jupiter',Sat:'Saturn',Ven:'Venus',Mer:'Mercury'}[lord]||lord;
  if(rel.friends.some(f=>f===planetName||f===lord)) return {score:40,label:"Friend's House"};
  if(rel.enemies.some(f=>f===planetName||f===lord)) return {score:20,label:'Enemy House'};
  return {score:30,label:'Neutral'};
}

// Neecha Bhanga (cancellation of debilitation) checker
function hasNeechaBhanga(planet, signIdx, signToPlanets) {
  // Basic rule: lord of debilitation sign is in kendra (1,4,7,10) from Asc,
  // OR exaltation lord of the debilitated planet is in kendra,
  // OR exaltation lord is conjunct debilitated planet.
  // Simplified: if the planet that owns the debilitation sign is placed, or
  // if the planet that exalts this planet is placed in an angular sign from moon/lagna.
  // We'll use: debilitation lord conjunct or in kendra of current sign.
  const debSign=DEBILITATION[planet]; if(!debSign) return false;
  const debSignIdx=SIGNS.indexOf(debSign);
  if(signIdx!==debSignIdx) return false; // only applies when debilitated
  const debLord=SIGN_LORD[debSign];
  // Check if debLord is in a kendra from this planet's sign (1,4,7,10)
  for(let si=0;si<12;si++){
    if(signToPlanets[si]?.includes(debLord)){
      const offset=((si-signIdx+12)%12)+1;
      if([1,4,7,10].includes(offset)) return true;
    }
  }
  // Or exaltation lord of planet conjuncts it
  const exaltSign=EXALTATION[planet]; if(!exaltSign) return false;
  const exaltLord=SIGN_LORD[exaltSign];
  if(signToPlanets[signIdx]?.includes(exaltLord)) return true;
  return false;
}

// ── DIG BALA ──────────────────────────────────────
// Dig Bala = directional strength based on house from Asc
// Best house → 100, opposite → 0, linear interpolation
const DIG_BALA_HOUSE={Mon:4,Ven:4,Jup:1,Mer:1,Sat:7,Mar:10,Sun:10};
// Nish Bala = temporal strength (simplified: day/night planet)
// Day planets: Sun, Jup, Sat (strong during day = odd houses 1,3,5,7,9,11 from Asc loosely)
// Night planets: Mon, Ven, Mar
// We simplify: day planets in angular (1,4,7,10) get 80, else 50; night in succedent (2,5,8,11) get 80, else 50
const DAY_PLANET=['Sun','Jup','Sat'];
const NIGHT_PLANET=['Mon','Ven','Mar'];

function getDigBala(planet, sign, ascSIdx) {
  if(planet==='Asc'||planet==='Rahu'||planet==='Ketu') return 0;
  const bestH=DIG_BALA_HOUSE[planet]; if(!bestH) return 0;
  if(ascSIdx===-1) return 0;
  const sIdx=SIGNS.indexOf(sign);
  const houseNum=((sIdx-ascSIdx+12)%12)+1;
  // Distance from best house (1-indexed, circular)
  const dist=Math.min(Math.abs(houseNum-bestH),(12-Math.abs(houseNum-bestH)));
  // 0 distance → 100, 6 distance → 0
  return Math.round((1-dist/6)*100);
}

function getNishBala(planet, sign, ascSIdx) {
  if(planet==='Asc'||planet==='Rahu'||planet==='Ketu') return 0;
  if(ascSIdx===-1) return 50;
  const sIdx=SIGNS.indexOf(sign);
  const h=((sIdx-ascSIdx+12)%12)+1;
  const angular=[1,4,7,10], succedent=[2,5,8,11], cadent=[3,6,9,12];
  if(DAY_PLANET.includes(planet)){
    if(angular.includes(h)) return 80;
    if(succedent.includes(h)) return 60;
    return 40;
  }
  if(NIGHT_PLANET.includes(planet)){
    if(succedent.includes(h)) return 80;
    if(angular.includes(h)) return 60;
    return 40;
  }
  return 50;
}

// ── PLANET COLORS ────────────────────────────────
const PLANET_BASE={
  Sun: {bg:'#FF9900',text:'#1a0500',mix:[255,153,0]},
  Mon: {bg:'#E8F0FF',text:'#0a1030',mix:[210,225,255]},
  Mar: {bg:'#FF2200',text:'#fff',mix:[255,34,0]},
  Jup: {bg:'#FFD700',text:'#1a0800',mix:[255,215,0]},
  Sat: {bg:'#1144CC',text:'#c0d4ff',mix:[17,68,204]},
  Ven: {bg:'#FFB0C8',text:'#3a0020',mix:[255,176,200]},
  Rahu:{bg:'#111111',text:'#ddccbb',mix:[18,18,18]},
  Ketu:{bg:'#5C1500',text:'#FF8866',mix:[92,21,0]},
  Mer: {bg:'#00CC33',text:'#d0ffd8',mix:[0,204,51]},
  Asc: {bg:'transparent',text:'#FFD700',mix:null},
};

// ── SCORE WEIGHTS ─────────────────────────────────
// SIGN SCORE MODIFIERS (multipliers on base sign score from planet in/aspecting sign)
// Benefic multipliers (additive boost % of sign base)
const SIGN_GOOD_MULT={
  Jup:1.0, Ven:0.8, Mer:0.6,
  // Moon: varies by phase (handled dynamically)
};
// Malefic reduction % of current sign score
const SIGN_BAD_MULT={
  Sat:0.80, Mar:0.75, Rahu:0.90, Sun:0.20, Ketu:0.30,
  // Moon new: 1.0 (complete), moon at 12/2: 0.80 (handled dynamically)
};
// PLANET INTERACTION SCORE MODIFIERS (conjunction/aspect effects on other planets)
// Benefic boost% to target planet's goodness score
const PLANET_GOOD_MULT={
  Jup:1.0, Ven:0.8, Mer:0.7,
  // Moon: 1.2 (6th/8th from sun), 1.8 (7th), graded otherwise
};
// Malefic reduction% of target planet's goodness score
const PLANET_BAD_MULT={
  Sat:0.70, Mar:0.60, Rahu:0.80, Ketu:0.30,
  // New Moon (dist 1 from sun): 0.90
};

// ── MOON PHASE ────────────────────────────────────
function moonBrightness(moonSIdx,sunSIdx){
  if(sunSIdx===-1||moonSIdx===-1) return 1.0;
  const dist=((moonSIdx-sunSIdx+12)%12)+1;
  if(dist===1) return 0.0;
  if(dist===7) return 1.0;
  if(dist>=2&&dist<=6) return (dist-1)/6;
  return (13-dist)/6;
}
function moonBadFactor(moonSIdx,sunSIdx){
  if(sunSIdx===-1||moonSIdx===-1) return 0;
  const dist=((moonSIdx-sunSIdx+12)%12)+1;
  if(dist===1) return 1.0;
  if(dist===2||dist===12) return 0.35;
  return 0;
}
// Moon as sign goodness multiplier (1.8 at dist7, 1.2 at dist6/8, grades in between)
function moonSignGoodMult(moonSIdx,sunSIdx){
  if(sunSIdx===-1) return 1.0;
  const dist=((moonSIdx-sunSIdx+12)%12)+1;
  if(dist===7) return 1.8;
  if(dist===6||dist===8) return 1.2;
  if(dist===1) return 0;
  return moonBrightness(moonSIdx,sunSIdx); // 0..1 for others
}
// Moon as sign badness multiplier
function moonSignBadMult(moonSIdx,sunSIdx){
  if(sunSIdx===-1) return 0;
  const dist=((moonSIdx-sunSIdx+12)%12)+1;
  if(dist===1) return 1.0;  // new moon: 100%
  if(dist===2||dist===12) return 0.80;
  return 0;
}
// Moon as planet goodness mult for interaction (1.2/1.8/1.2 for dist 6/7/8)
function moonPlanetGoodMult(moonSIdx,sunSIdx){
  if(sunSIdx===-1) return moonBrightness(moonSIdx,sunSIdx);
  const dist=((moonSIdx-sunSIdx+12)%12)+1;
  if(dist===7) return 1.8;
  if(dist===6||dist===8) return 1.2;
  return moonBrightness(moonSIdx,sunSIdx);
}
function moonColor(brightness){
  if(brightness<=0) return {bg:'#0a0820',text:'#334466',mix:[10,8,32]};
  const dark=[10,8,32],bright=[232,240,255];
  const r=Math.round(dark[0]+(bright[0]-dark[0])*brightness);
  const g=Math.round(dark[1]+(bright[1]-dark[1])*brightness);
  const b=Math.round(dark[2]+(bright[2]-dark[2])*brightness);
  return {bg:`rgb(${r},${g},${b})`,text:brightness>0.5?'#0a1030':'#99aacc',mix:[r,g,b]};
}

// ── ASPECT RULES ─────────────────────────────────
function getAspectOffsets(planet,signIdx,sunSIdx){
  if(['Rahu','Ketu','Asc'].includes(planet)) return [1];
  if(planet==='Mon'){
    const bright=moonBrightness(signIdx,sunSIdx);
    if(bright<=0) return [1];
    if(sunSIdx!==-1){const dist=((signIdx-sunSIdx+12)%12)+1;if([6,7,8].includes(dist)) return [1,6,7,8];}
    return [1,7];
  }
  if(planet==='Sat') return [1,3,7,10];
  if(planet==='Jup') return [1,5,7,9];
  if(planet==='Mar') return [1,4,7,8];
  return [1,7]; // Sun,Ven,Mer
}
function aspectSign(sIdx,offset){return(sIdx+offset-1)%12;}
function gridPosOfSign(sIdx){return GRID_SIGNS.findIndex(s=>s&&SIGNS.indexOf(s)===sIdx);}

// ══════════════════════════════════════════════════
//  CHART INSTANCE
// ══════════════════════════════════════════════════
// One call = one self-contained chart: its own placements, palette, aspect
// rays, per-planet checkboxes and eight dashboards, all looked up inside
// `root` (a #panelTpl clone) rather than by page-wide id. Compare mode is
// then just a second call - the two charts never share state.
//
//   root  - the .panel element this chart owns
//   opts.onTabChange(tab) - fired when the user picks a dashboard tab, so
//                           the other chart can follow along.
function createChart(root,opts){
  opts=opts||{};

  // ── STATE ─────────────────────────────────────────
  let cellPlanets={};
  let rayOpacity=0.65;
  let activeTab='good';
  // Tap-to-place (mobile alternative to drag-and-drop): the palette planet
  // currently armed for placement, and the on-chart planet currently showing
  // its remove (x) button. Only one of each can be active at a time.
  let selectedPalettePlanet=null;
  let removeTargetPlanet=null;
  // Per-planet visibility: showArrow[p]=true means draw aspect rays for planet p
  //                        showColor[p]=true means color signs from planet p's aspects
  const showArrow={};
  const showColor={};
  // The checkbox <input>s themselves, so they can be found without page-unique
  // ids - two charts on screen would otherwise collide on them.
  const cbArrows={},cbColors={};
  const PLANETS_INIT=['Sun','Mon','Mar','Jup','Sat','Ven','Rahu','Ketu','Mer','Asc'];
  PLANETS_INIT.forEach(p=>{showArrow[p]=true;showColor[p]=true;});

  // ── HELPERS ───────────────────────────────────────
  function findPlanetSignIdx(planet){
    for(let pos=0;pos<16;pos++) if(cellPlanets[pos]?.includes(planet)&&GRID_SIGNS[pos]) return SIGNS.indexOf(GRID_SIGNS[pos]);
    return -1;
  }
  function getSignToPlanets(){
    const m={};for(let i=0;i<12;i++) m[i]=[];
    for(let pos=0;pos<16;pos++){if(!cellPlanets[pos]?.length||!GRID_SIGNS[pos]) continue;
      const si=SIGNS.indexOf(GRID_SIGNS[pos]);
      cellPlanets[pos].forEach(p=>{if(p!=='Asc') m[si].push(p);});
    }
    return m;
  }

  // ── BUILD GRID ────────────────────────────────────
  const chartWrapper=root.querySelector('.chart-wrapper');
  const chartGrid=root.querySelector('.chart-grid');
  const raysOverlay=root.querySelector('.rays-overlay');
  const paletteEl=root.querySelector('.palette-list');
  // Dashboard section holders, addressed per instance instead of by page id.
  const sec=(key)=>root.querySelector(`[data-sections="${key}"]`);
  for(let i=0;i<16;i++){
    const cell=document.createElement('div');
    cell.className='cell';cell.dataset.pos=i;
    if(!GRID_SIGNS[i]){cell.classList.add('empty');}
    else{
      cellPlanets[i]=[];
      const lbl=document.createElement('div');lbl.className='sign-label';
      // data-i18n-term lets I18N.apply() retranslate the sign labels on a
      // language switch without rebuilding the grid.
      lbl.setAttribute('data-i18n-term','sign:'+GRID_SIGNS[i]);
      lbl.textContent=SN(GRID_SIGNS[i]);cell.appendChild(lbl);
      const pc=document.createElement('div');pc.className='planets-container';cell.appendChild(pc);
      cell.addEventListener('dragover',onDragOver);
      cell.addEventListener('drop',e=>onDrop(e,i));
      cell.addEventListener('dragleave',onDragLeave);
      cell.addEventListener('click',e=>onCellClick(e,i));
    }
    chartGrid.appendChild(cell);
  }

  // ── PALETTE ───────────────────────────────────────
  const PLANETS=['Sun','Mon','Mar','Jup','Sat','Ven','Rahu','Ketu','Mer','Asc'];
  const paletteSlots={};
  // paletteRows[p] = the outer .palette-row div (holds token + checkboxes)
  const paletteRows={};

  PLANETS.forEach(p=>{
    const isAsc=(p==='Asc');
    // Outer row: grid(token | cb-arrow | cb-color)  — Asc gets no checkboxes
    const row=document.createElement('div');
    row.className='palette-row';
    if(isAsc) row.style.gridTemplateColumns='1fr';

    // Token cell — holds either the token or a placeholder when planet is on chart
    const tokenCell=document.createElement('div');
    tokenCell.className='palette-token-cell';
    tokenCell.appendChild(createToken(p));
    row.appendChild(tokenCell);

    if(!isAsc){
      // Arrow checkbox cell
      const cbArrCell=document.createElement('div');
      cbArrCell.className='cb-cell';
      const cbArr=document.createElement('input');
      cbArr.type='checkbox'; cbArr.checked=true;
      cbArr.className='cb-arrow'; cbArrows[p]=cbArr;
      cbArr.title=T('pg.show_arrows_for',{planet:PN(p)});
      cbArr.addEventListener('change',function(){
        showArrow[p]=this.checked;
        updateMasterCb('arrow');
        updateRays();
      });
      cbArrCell.appendChild(cbArr);
      row.appendChild(cbArrCell);

      // Color checkbox cell
      const cbColCell=document.createElement('div');
      cbColCell.className='cb-cell';
      const cbCol=document.createElement('input');
      cbCol.type='checkbox'; cbCol.checked=true;
      cbCol.className='cb-color'; cbColors[p]=cbCol;
      cbCol.title=T('pg.show_colors_for',{planet:PN(p)});
      cbCol.addEventListener('change',function(){
        showColor[p]=this.checked;
        updateMasterCb('color');
        updateCellColors();
      });
      cbColCell.appendChild(cbCol);
      row.appendChild(cbColCell);
    }

    paletteEl.appendChild(row);
    paletteSlots[p]=tokenCell;
    paletteRows[p]=row;
  });

  paletteEl.addEventListener('dragover',onDragOver);
  paletteEl.addEventListener('drop',onDropPalette);
  paletteEl.addEventListener('dragleave',onDragLeave);

  // ── CHECKBOX HELPERS ──────────────────────────────
  function toggleAllCb(type,checked){
    PLANETS.forEach(p=>{
      if(type==='arrow'){
        showArrow[p]=checked;
        const cb=cbArrows[p];
        if(cb) cb.checked=checked;
      } else {
        showColor[p]=checked;
        const cb=cbColors[p];
        if(cb) cb.checked=checked;
      }
    });
    if(type==='arrow') updateRays();
    else updateCellColors();
  }

  function updateMasterCb(type){
    const master=root.querySelector(type==='arrow'?'.cb-master-arrow':'.cb-master-color');
    if(!master) return;
    const vals=PLANETS.map(p=>type==='arrow'?showArrow[p]:showColor[p]);
    const allOn=vals.every(v=>v);
    const allOff=vals.every(v=>!v);
    master.checked=allOn;
    master.indeterminate=(!allOn&&!allOff);
  }

  function createToken(planet,moonBright){
    const t=document.createElement('div');t.className='planet-token';t.textContent=PA(planet);
    t.title=PN(planet);
    t.draggable=true;t.dataset.planet=planet;
    let bg,textCol,border;
    if(planet==='Mon'){
      const b=moonBright!==undefined?moonBright:1.0;
      const mc=moonColor(b);bg=mc.bg;textCol=mc.text;border='1px solid rgba(200,220,255,.4)';
    }else if(planet==='Asc'){bg='rgba(255,215,0,.1)';textCol='#FFD700';border='1.5px solid #d4af37';}
    else{bg=PLANET_BASE[planet].bg;textCol=PLANET_BASE[planet].text;border='1px solid rgba(255,255,255,.2)';}
    t.style.background=bg;t.style.color=textCol;t.style.border=border;
    if(planet!=='Asc'&&planet!=='Mon'){const[r,g,b]=PLANET_BASE[planet].mix;t.style.boxShadow=`0 1px 6px rgba(${r},${g},${b},.55)`;}
    t.addEventListener('dragstart',onDragStart);t.addEventListener('dragend',onDragEnd);
    t.addEventListener('click',onTokenClick);
    if(planet===selectedPalettePlanet) t.classList.add('token-selected');
    return t;
  }

  // ── DRAG & DROP ───────────────────────────────────
  let dragPlanet=null,dragSourcePos=null;
  function onDragStart(e){
    // A real drag is starting - cancel any tap-to-place selection or armed
    // remove button first, so the two interaction modes never fight over the
    // same token (e.g. a stale "selected" planet getting placed a second time
    // via a later tap, after this drag already moved it).
    cancelTapMode();
    dragPlanet=e.target.closest('[data-planet]')?.dataset.planet;const fromPalette=!!e.target.closest('.palette');const posAttr=e.target.closest('[data-pos]')?.dataset.pos;dragSourcePos=(!fromPalette&&posAttr!==undefined)?parseInt(posAttr):null;e.target.classList.add('dragging');e.dataTransfer.effectAllowed='move';}
  function onDragEnd(e){e.target.classList.remove('dragging');}
  function onDragOver(e){e.preventDefault();const cell=e.currentTarget.closest?.('.cell');if(cell&&!cell.classList.contains('empty')) cell.classList.add('active-drop');}
  function onDragLeave(e){const cell=e.currentTarget.closest?.('.cell');if(cell) cell.classList.remove('active-drop');}
  function onDrop(e,targetPos){e.preventDefault();e.currentTarget.classList.remove('active-drop');if(!dragPlanet) return;if(dragSourcePos!==null) removePlanetFromCell(dragSourcePos,dragPlanet);addPlanetToCell(targetPos,dragPlanet);dragPlanet=null;dragSourcePos=null;}
  function onDropPalette(e){e.preventDefault();if(!dragPlanet) return;if(dragSourcePos!==null) removePlanetFromCell(dragSourcePos,dragPlanet);ensurePaletteToken(dragPlanet);dragPlanet=null;dragSourcePos=null;updateAll();}
  function addPlanetToCell(pos,planet){if(!cellPlanets[pos]) cellPlanets[pos]=[];removePaletteToken(planet);cellPlanets[pos].push(planet);renderCell(pos);updateAll();}
  function removePlanetFromCell(pos,planet){if(!cellPlanets[pos]) return;const i=cellPlanets[pos].indexOf(planet);if(i!==-1) cellPlanets[pos].splice(i,1);renderCell(pos);updateAll();}

  // ── TAP-TO-PLACE (mobile alternative to drag-and-drop) ─────────────
  // Tap a planet in the palette to arm it, then tap any house to drop it
  // there. Tap a planet already on the chart to arm its remove (x) button
  // instead; tapping the (x) sends it back to the palette. Tapping anywhere
  // else (another token, a house with nothing armed, or empty space) clears
  // whichever of the two is currently armed.
  function onTokenClick(e){
    e.stopPropagation();
    const planet=e.currentTarget.dataset.planet;
    const onChart=!e.currentTarget.closest('.palette');
    if(onChart) armRemoveButton(planet,e.currentTarget);
    else armPaletteSelection(planet);
  }
  function armPaletteSelection(planet){
    disarmRemoveButton();
    setSelectedPalettePlanet(selectedPalettePlanet===planet?null:planet);
  }
  function setSelectedPalettePlanet(planet){
    if(selectedPalettePlanet){
      paletteSlots[selectedPalettePlanet]?.querySelector('.planet-token')?.classList.remove('token-selected');
    }
    selectedPalettePlanet=planet;
    chartGrid.classList.toggle('selecting',!!planet);
    if(planet){
      paletteSlots[planet]?.querySelector('.planet-token')?.classList.add('token-selected');
    }
  }
  function armRemoveButton(planet,tokenEl){
    setSelectedPalettePlanet(null);
    if(removeTargetPlanet===planet){disarmRemoveButton();return;}
    disarmRemoveButton();
    removeTargetPlanet=planet;
    tokenEl.classList.add('token-armed');
    const btn=document.createElement('button');
    btn.type='button';btn.className='token-remove-btn';btn.textContent='×';
    btn.setAttribute('aria-label','Remove '+planet+' from the chart');
    btn.addEventListener('click',function(ev){
      ev.stopPropagation();
      const pos=parseInt(tokenEl.closest('.cell').dataset.pos,10);
      disarmRemoveButton();
      removePlanetFromCell(pos,planet);
      ensurePaletteToken(planet);
      updateAll();
    });
    tokenEl.appendChild(btn);
  }
  function disarmRemoveButton(){
    if(!removeTargetPlanet) return;
    root.querySelectorAll('.token-remove-btn').forEach(b=>b.remove());
    root.querySelectorAll('.planet-token.token-armed').forEach(t=>t.classList.remove('token-armed'));
    removeTargetPlanet=null;
  }
  function cancelTapMode(){setSelectedPalettePlanet(null);disarmRemoveButton();}
  function onCellClick(e,pos){
    e.stopPropagation();
    if(!selectedPalettePlanet) return;
    const planet=selectedPalettePlanet;
    setSelectedPalettePlanet(null);
    addPlanetToCell(pos,planet);
  }
  // Tapping anywhere that didn't already handle its own click (a token or a
  // house) cancels whichever tap-to-place action is mid-flight.
  document.addEventListener('click',cancelTapMode);
  function removePaletteToken(p){
    const s=paletteSlots[p];if(!s) return;
    s.innerHTML='';
    // Add placeholder text so the row doesn't collapse
    const ph=document.createElement('div');
    ph.className='palette-placeholder';
    ph.textContent=T('pg.on_chart',{planet:PN(p)});
    s.appendChild(ph);
  }
  function ensurePaletteToken(p){
    const s=paletteSlots[p];if(!s) return;
    // Clear placeholder or any existing content, then re-add token
    s.innerHTML='';
    s.appendChild(createToken(p));
  }
  function renderCell(pos){
    const pc=chartGrid.children[pos].querySelector('.planets-container');if(!pc) return;pc.innerHTML='';
    const sunSIdx=findPlanetSignIdx('Sun');
    (cellPlanets[pos]||[]).forEach(p=>{
      const b=(p==='Mon')?moonBrightness(SIGNS.indexOf(GRID_SIGNS[pos]),sunSIdx):undefined;
      pc.appendChild(createToken(p,b));
    });
  }

  // ── CLEAR ALL ─────────────────────────────────────
  function clearAll(){
    cancelTapMode();
    for(let pos=0;pos<16;pos++){if(GRID_SIGNS[pos]) cellPlanets[pos]=[];}
    PLANETS.forEach(p=>ensurePaletteToken(p));
    updateAll();
  }

  // ── OPACITY SLIDER ────────────────────────────────
  function onRayOpacityChange(input){
    const val=parseInt(input.value);rayOpacity=val/100;
    root.querySelector('.opacity-value').textContent=val+'%';
    input.style.background=`linear-gradient(to right,#d4af37 0%,#d4af37 ${val}%,rgba(255,255,255,.15) ${val}%)`;
    updateRays();
  }

  // ── TAB SWITCHING ─────────────────────────────────
  // `echo` is false when the switch was mirrored from the other chart, so the
  // two panels can stay in step without bouncing the event back and forth.
  function switchTab(tab,echo){
    activeTab=tab;
    root.querySelectorAll('.dash-tab').forEach(t=>t.classList.toggle('active-tab',t.dataset.tab===tab));
    root.querySelectorAll('.dash-panel').forEach(p=>p.classList.toggle('active-panel',p.dataset.panel===tab));
    if(echo!==false&&typeof opts.onTabChange==='function') opts.onTabChange(tab);
  }

  // ═══════════════════════════════════════════════════
  //  UPDATE ALL
  // ═══════════════════════════════════════════════════
  function updateAll(){
    for(let pos=0;pos<16;pos++){if(GRID_SIGNS[pos]) renderCell(pos);}
    updateCellColors();updateHouseNumbers();updateRays();updateAllDashboards();
  }

  // ── CELL COLORS ───────────────────────────────────
  function updateCellColors(){
    const signColors={};GRID_SIGNS.forEach(s=>{if(s) signColors[SIGNS.indexOf(s)]=[];});
    const sunSIdx=findPlanetSignIdx('Sun');
    for(let pos=0;pos<16;pos++){
      if(!cellPlanets[pos]?.length||!GRID_SIGNS[pos]) continue;
      const si=SIGNS.indexOf(GRID_SIGNS[pos]);
      cellPlanets[pos].forEach(planet=>{
        if(planet==='Asc') return;
        // Skip if sign color is turned off for this planet
        if(!showColor[planet]) return;
        getAspectOffsets(planet,si,sunSIdx).forEach(off=>{
          const target=aspectSign(si,off);if(signColors[target]===undefined) return;
          let rgb;
          if(planet==='Mon'){const bright=moonBrightness(si,sunSIdx);if(bright<=0) return;rgb=moonColor(bright).mix;}
          else{rgb=PLANET_BASE[planet].mix;if(!rgb) return;}
          signColors[target].push(`rgba(${rgb[0]},${rgb[1]},${rgb[2]},.62)`);
        });
      });
    }
    for(let pos=0;pos<16;pos++){
      const sign=GRID_SIGNS[pos];if(!sign) continue;
      const cell=chartGrid.children[pos];
      const colors=signColors[SIGNS.indexOf(sign)]||[];
      if(!colors.length){cell.style.background=DEFAULT_BG;}
      else{const layers=colors.map((c,i)=>`radial-gradient(ellipse at ${16+i*15}% ${25+i*13}%,${c} 0%,transparent 70%)`);cell.style.background=layers.join(',')+ `,${DEFAULT_BG}`;}
    }
  }

  // ── HOUSE NUMBERS ─────────────────────────────────
  function updateHouseNumbers(){
    root.querySelectorAll('.house-number').forEach(el=>el.remove());
    let ascPos=-1;for(let pos=0;pos<16;pos++) if(cellPlanets[pos]?.includes('Asc')&&GRID_SIGNS[pos]){ascPos=pos;break;}
    if(ascPos===-1) return;
    const ascSIdx=SIGNS.indexOf(GRID_SIGNS[ascPos]);
    const SIDE={Aries:'top',Taurus:'top',Gemini:'top',Cancer:'right',Leo:'right',Virgo:'right',Libra:'bottom',Scorpio:'bottom',Sagittarius:'left',Capricorn:'left',Aquarius:'left',Pisces:'left'};
    for(let pos=0;pos<16;pos++){
      const sign=GRID_SIGNS[pos];if(!sign) continue;
      const num=((SIGNS.indexOf(sign)-ascSIdx+12)%12)+1;
      const el=document.createElement('div');el.className=`house-number house-num-${SIDE[sign]}`;el.textContent=num;
      chartGrid.children[pos].appendChild(el);
    }
  }

  // ── RAYS ──────────────────────────────────────────
  function updateRays(){
    raysOverlay.innerHTML='';const svgNS='http://www.w3.org/2000/svg';
    const gRect=chartGrid.getBoundingClientRect();
    // A hidden panel (compare mode off) measures zero, which would draw every
    // ray on top of itself; it is redrawn when the panel is shown again.
    if(!gRect.width) return;
    const wRect=chartWrapper.getBoundingClientRect();
    raysOverlay.style.top=(gRect.top-wRect.top)+'px';raysOverlay.style.left=(gRect.left-wRect.left)+'px';
    raysOverlay.style.width=gRect.width+'px';raysOverlay.style.height=gRect.height+'px';
    const sunSIdx=findPlanetSignIdx('Sun');
    for(let pos=0;pos<16;pos++){
      if(!cellPlanets[pos]?.length||!GRID_SIGNS[pos]) continue;
      const si=SIGNS.indexOf(GRID_SIGNS[pos]);
      cellPlanets[pos].forEach(planet=>{
        if(['Asc','Rahu','Ketu'].includes(planet)) return;
        // Skip if arrow visibility is turned off for this planet
        if(!showArrow[planet]) return;
        const offsets=getAspectOffsets(planet,si,sunSIdx);
        offsets.filter(o=>o!==1).forEach(off=>{
          const tSIdx=aspectSign(si,off);const tPos=gridPosOfSign(tSIdx);if(tPos===-1) return;
          let rgb;
          if(planet==='Mon'){const bright=moonBrightness(si,sunSIdx);if(bright<=0) return;rgb=moonColor(bright).mix;}
          else{rgb=PLANET_BASE[planet].mix;if(!rgb) return;}
          const sr=chartGrid.children[pos].getBoundingClientRect();const tr=chartGrid.children[tPos].getBoundingClientRect();
          const x1=sr.left+sr.width/2-gRect.left,y1=sr.top+sr.height/2-gRect.top;
          const x2=tr.left+tr.width/2-gRect.left,y2=tr.top+tr.height/2-gRect.top;
          const stroke=`rgb(${rgb[0]},${rgb[1]},${rgb[2]})`;
          const line=document.createElementNS(svgNS,'line');
          line.setAttribute('x1',x1);line.setAttribute('y1',y1);line.setAttribute('x2',x2);line.setAttribute('y2',y2);
          line.setAttribute('stroke',stroke);line.setAttribute('stroke-width','2.5');line.setAttribute('stroke-dasharray','6,4');line.setAttribute('opacity',rayOpacity);
          raysOverlay.appendChild(line);
          const angle=Math.atan2(y2-y1,x2-x1),al=11,aw=0.40;
          const poly=document.createElementNS(svgNS,'polygon');
          poly.setAttribute('points',[`${x2},${y2}`,`${x2-al*Math.cos(angle-aw)},${y2-al*Math.sin(angle-aw)}`,`${x2-al*Math.cos(angle+aw)},${y2-al*Math.sin(angle+aw)}`].join(' '));
          poly.setAttribute('fill',stroke);poly.setAttribute('opacity',rayOpacity);raysOverlay.appendChild(poly);
        });
      });
    }
  }

  // ═══════════════════════════════════════════════════
  //  SIGN SCORING ENGINE (Goodness / Badness for Signs)
  // ═══════════════════════════════════════════════════
  // Each sign starts at SIGN_BASE_SCORE=50.
  // Benefic planets in/aspecting sign add: base * multiplier
  // Malefic planets in/aspecting sign reduce: current * (1 - multiplier)
  // Order: apply benefics first, then malefics on top (can only reduce to 0)

  function computeSignScores(){
    const sunSIdx=findPlanetSignIdx('Sun');
    const moonSIdx=findPlanetSignIdx('Mon');
    const goodScores={},badScores={};
    for(let i=0;i<12;i++){goodScores[i]={score:SIGN_BASE_SCORE,sources:[]};badScores[i]={score:0,sources:[]};}

    // Which signs does each planet reach?
    for(let pos=0;pos<16;pos++){
      if(!cellPlanets[pos]?.length||!GRID_SIGNS[pos]) continue;
      const si=SIGNS.indexOf(GRID_SIGNS[pos]);
      cellPlanets[pos].forEach(planet=>{
        if(planet==='Asc') return;
        const offsets=getAspectOffsets(planet,si,sunSIdx);
        offsets.forEach(off=>{
          const target=aspectSign(si,off);
          // ── BENEFICS (boost goodness) ──
          if(['Jup','Ven','Mer'].includes(planet)){
            const mult=SIGN_GOOD_MULT[planet];
            goodScores[target].score+=SIGN_BASE_SCORE*mult;
            goodScores[target].sources.push(`${planet}(+${Math.round(SIGN_BASE_SCORE*mult)})`);
          }
          if(planet==='Mon'){
            const bright=moonBrightness(si,sunSIdx);
            const mult=moonSignGoodMult(si,sunSIdx);
            if(mult>0){
              goodScores[target].score+=SIGN_BASE_SCORE*mult;
              goodScores[target].sources.push(`Moon(+${Math.round(SIGN_BASE_SCORE*mult)})`);
            }
            // Moon badness on sign
            const badMult=moonSignBadMult(si,sunSIdx);
            if(badMult>0){
              badScores[target].score+=SIGN_BASE_SCORE*badMult;
              badScores[target].sources.push(`Moon-dark(-${Math.round(SIGN_BASE_SCORE*badMult)})`);
            }
          }
          // ── MALEFICS (add to badness) ──
          if(['Sat','Mar','Rahu','Ketu','Sun'].includes(planet)){
            const mult={Sat:0.80,Mar:0.75,Rahu:0.90,Sun:0.20,Ketu:0.30}[planet];
            // Sun: only own sign (no aspect badness)
            if(planet==='Sun'&&off!==1) return;
            badScores[target].score+=SIGN_BASE_SCORE*mult;
            badScores[target].sources.push(`${planet}(-${Math.round(SIGN_BASE_SCORE*mult)})`);
          }
        });
      });
    }

    // Normalize
    const maxG=Math.max(...Object.values(goodScores).map(s=>s.score),1);
    const maxB=Math.max(...Object.values(badScores).map(s=>s.score),1);
    for(let i=0;i<12;i++){goodScores[i].pct=Math.round(goodScores[i].score/maxG*100);badScores[i].pct=Math.round(badScores[i].score/maxB*100);}
    return {goodScores,badScores};
  }

  // ═══════════════════════════════════════════════════
  //  PLANET SCORING ENGINE (Subathuva)
  // ═══════════════════════════════════════════════════
  // Rules:
  // - Mars aspecting Jupiter: NO effect (Mars cannot harm Jupiter via aspect)
  // - Mars aspecting Moon (bright): NO effect
  // - Jupiter aspecting Mars: full effect (boosts Mars goodness)
  // - Full Moon aspecting any planet: full boost
  // - Ketu conjunction with Saturn/Mars (when no other malefic aspects): reduces their badness
  // - When Saturn/Mars+Ketu get malefic aspect (other malefic): Ketu mitigation removed

  function computePlanetScores(){
    const sunSIdx=findPlanetSignIdx('Sun');
    const moonSIdx=findPlanetSignIdx('Mon');
    const bright=moonSIdx!==-1?moonBrightness(moonSIdx,sunSIdx):1.0;
    const badFactor=moonSIdx!==-1?moonBadFactor(moonSIdx,sunSIdx):0;
    const signTP=getSignToPlanets();

    // Placed planets
    const placed=[];
    for(let pos=0;pos<16;pos++){
      if(!cellPlanets[pos]?.length||!GRID_SIGNS[pos]) continue;
      cellPlanets[pos].forEach(p=>{if(p!=='Asc') placed.push({planet:p,sIdx:SIGNS.indexOf(GRID_SIGNS[pos])});});
    }
    const pScores={};
    placed.forEach(({planet})=>{if(!pScores[planet]) pScores[planet]={goodness:0,badness:0,goodSrc:[],badSrc:[]};});

    // Which signs does each placed planet reach?
    function reachOf(p,si){return getAspectOffsets(p,si,sunSIdx).map(off=>aspectSign(si,off));}

    // Check if a planet at targetSIdx is receiving any OTHER malefic aspect besides the ketu-sat/mar group
    function hasOtherMaleficAspect(targetSIdx,ketuSIdx,excludePlanets){
      const malefics=['Sat','Mar','Rahu','Mon']; // Mon as new moon
      for(const {planet:src,sIdx:srcSIdx} of placed){
        if(excludePlanets.includes(src)) continue;
        if(!malefics.includes(src)) continue;
        if(src==='Mon'&&badFactor<=0) continue;
        const reach=reachOf(src,srcSIdx);
        if(reach.includes(targetSIdx)) return true;
      }
      return false;
    }

    // ── For each target planet, check who reaches it ──
    placed.forEach(({planet:target,sIdx:targetSIdx})=>{
      if(!pScores[target]) return;

      placed.forEach(({planet:src,sIdx:srcSIdx})=>{
        if(src===target&&srcSIdx===targetSIdx) return; // same planet
        const reach=reachOf(src,srcSIdx);
        if(!reach.includes(targetSIdx)) return; // doesn't reach target

        const isConj=(srcSIdx===targetSIdx);

        // ══ RULE: Mars cannot harm Jupiter via aspect (conj is ok for badness) ══
        if(src==='Mar'&&target==='Jup'&&!isConj) return;
        // ══ RULE: Mars has no effect on full Moon at all (bright>0.5) ══
        if(src==='Mar'&&target==='Mon'&&bright>0.5) return;

        // ── BENEFICS give goodness ──
        if(['Jup','Ven','Mer'].includes(src)){
          const mult=PLANET_GOOD_MULT[src];
          const pts=100*mult;
          pScores[target].goodness+=pts;
          pScores[target].goodSrc.push(`${src}(+${Math.round(pts)})`);
        }
        if(src==='Mon'&&bright>0){
          const mult=moonPlanetGoodMult(moonSIdx,sunSIdx);
          const pts=100*mult;
          pScores[target].goodness+=pts;
          pScores[target].goodSrc.push(`Moon(+${Math.round(pts)})`);
        }

        // ── MALEFICS give badness ──
        // Ketu mitigation: if Saturn or Mars is conjunct Ketu (and no other malefic aspect on them), reduce their badness
        const ketuSIdx=findPlanetSignIdx('Ketu');
        if(src==='Sat'||src==='Mar'){
          let pts=src==='Sat'?100:75;
          // Ketu conjunction check
          if(ketuSIdx!==-1&&signTP[srcSIdx]?.includes('Ketu')){
            // Check no other malefic aspects the source
            const otherMaleficAspects=hasOtherMaleficAspect(srcSIdx,ketuSIdx,['Ketu',src]);
            if(!otherMaleficAspects){
              // Ketu reduces badness of Sat/Mar
              pts=Math.round(pts*0.4); // 60% reduction
              pScores[target].badSrc.push(`${src}(Ketu-mitig,-${pts})`);
            } else {
              pScores[target].badSrc.push(`${src}(-${pts})`);
            }
          } else {
            pScores[target].badSrc.push(`${src}(-${pts})`);
          }
          pScores[target].badness+=pts;
        }
        if(src==='Rahu'&&isConj){
          pScores[target].badness+=80*PLANET_BAD_MULT.Rahu;
          pScores[target].badSrc.push(`Rahu(-${Math.round(80*PLANET_BAD_MULT.Rahu)})`);
        }
        if(src==='Sun'&&isConj){
          pScores[target].badness+=50;
          pScores[target].badSrc.push(`Sun(-50)`);
        }
        if(src==='Ketu'&&isConj){
          pScores[target].badness+=40*PLANET_BAD_MULT.Ketu;
          pScores[target].badSrc.push(`Ketu(-${Math.round(40*PLANET_BAD_MULT.Ketu)})`);
        }
        if(src==='Mon'&&badFactor>0&&isConj){
          const pts=100*badFactor;
          pScores[target].badness+=pts;
          pScores[target].badSrc.push(`Moon-dark(-${Math.round(pts)})`);
        }
      });

      // Self-brightness for Moon token
      if(target==='Mon'&&bright>0){
        const mult=moonPlanetGoodMult(moonSIdx,sunSIdx);
        pScores[target].goodness+=100*mult;
        pScores[target].goodSrc.push(`Moon-self(+${Math.round(100*mult)})`);
      }
      if(target==='Mon'&&badFactor>0){
        pScores[target].badness+=100*badFactor;
        pScores[target].badSrc.push(`Moon-dark-self(-${Math.round(100*badFactor)})`);
      }
    });

    Object.keys(pScores).forEach(p=>{pScores[p].wellness=pScores[p].goodness-pScores[p].badness;});
    return pScores;
  }

  // ═══════════════════════════════════════════════════
  //  STANA BALA ENGINE
  // ═══════════════════════════════════════════════════
  function computeStanaBala(){
    const signTP=getSignToPlanets();
    const results=[];
    for(let pos=0;pos<16;pos++){
      if(!cellPlanets[pos]?.length||!GRID_SIGNS[pos]) continue;
      const sign=GRID_SIGNS[pos];
      const si=SIGNS.indexOf(sign);
      cellPlanets[pos].forEach(planet=>{
        if(planet==='Asc') return;
        let {score,label}=getStanaBala(planet,sign);
        let nb=false;
        if(score===0){// check neecha bhanga
          nb=hasNeechaBhanga(planet,si,signTP);
          if(nb){score=35;label='Debilitation (Neecha Bhanga)';}
        }
        results.push({planet,sign,score,label,neechaBhanga:nb});
      });
    }
    return results;
  }

  // ═══════════════════════════════════════════════════
  //  DIG + NISH BALA ENGINE
  // ═══════════════════════════════════════════════════
  function computeDigNishBala(){
    const ascSIdx=findPlanetSignIdx('Asc');
    const results=[];
    for(let pos=0;pos<16;pos++){
      if(!cellPlanets[pos]?.length||!GRID_SIGNS[pos]) continue;
      const sign=GRID_SIGNS[pos];
      cellPlanets[pos].forEach(planet=>{
        if(planet==='Asc') return;
        const dig=getDigBala(planet,sign,ascSIdx);
        const nish=getNishBala(planet,sign,ascSIdx);
        results.push({planet,sign,dig,nish,total:Math.round((dig+nish)/2)});
      });
    }
    return results;
  }

  // ═══════════════════════════════════════════════════
  //  AGGREGATE HELPERS
  // ═══════════════════════════════════════════════════
  function aggregateCat(scoreMap){
    const el={fire:0,earth:0,air:0,water:0};
    const mod={movable:0,fixed:0,mutable:0};
    const dir={east:0,south:0,west:0,north:0};
    for(let i=0;i<12;i++){const s=scoreMap[i]?.score||0;const sign=SIGNS[i];const e=SIGN_ELEMENT[sign];const m=SIGN_MODALITY[sign];const d=ELEMENT_DIRECTION[e];el[e]+=s;mod[m]+=s;dir[d]+=s;}
    return{el,mod,dir};
  }

  // ═══════════════════════════════════════════════════
  //  BAR COLORS
  // ═══════════════════════════════════════════════════
  const BC={
    fire:'linear-gradient(90deg,#ff5500,#ff9900)',earth:'linear-gradient(90deg,#557722,#88bb44)',
    air:'linear-gradient(90deg,#2277aa,#55ccff)',water:'linear-gradient(90deg,#224499,#4499ee)',
    movable:'linear-gradient(90deg,#cc3333,#ff8888)',fixed:'linear-gradient(90deg,#3333aa,#7799ff)',mutable:'linear-gradient(90deg,#228855,#55ee99)',
    east:'linear-gradient(90deg,#cc7700,#ffcc00)',south:'linear-gradient(90deg,#226633,#55ee77)',west:'linear-gradient(90deg,#3355aa,#77aaff)',north:'linear-gradient(90deg,#445599,#88bbff)',
    good:'linear-gradient(90deg,#116633,#44ff88)',bad:'linear-gradient(90deg,#881100,#ff4433)',
    stana:'linear-gradient(90deg,#115577,#55ccff)',dig:'linear-gradient(90deg,#551133,#ff99aa)',
    total:'linear-gradient(90deg,#665500,#ffcc44)',
  };

  // ═══════════════════════════════════════════════════
  //  HTML BUILDERS
  // ═══════════════════════════════════════════════════
  function pBadge(planet){
    const c=PLANET_BASE[planet];if(!c) return PA(planet);
    const bg=c.bg==='transparent'?'rgba(212,175,55,.15)':c.bg;
    return `<span title="${PN(planet)}" style="display:inline-block;padding:1px 6px;border-radius:3px;font-size:9px;font-weight:700;font-family:'Cinzel',serif;background:${bg};color:${c.text};box-shadow:0 1px 3px rgba(0,0,0,.4)">${PA(planet)}</span>`;
  }

  function buildBar(pct,bg,height='8px'){
    return `<div style="flex:1;height:${height};background:rgba(255,255,255,.08);border-radius:4px;overflow:hidden;min-width:60px;">
      <div style="height:100%;width:${Math.min(pct,100)}%;background:${bg};border-radius:4px;transition:width .4s;"></div></div>`;
  }

  function buildSignsTable(ranked,ascSIdx,mode){
    if(!ranked.length) return `<div class="no-data">${T('pg.no_data_simple')}</div>`;
    const maxS=Math.max(...ranked.map(d=>d.score),1);
    const hCol=mode==='good'?'rgba(68,221,136,.7)':'rgba(255,80,70,.7)';
    let html=`<table class="signs-table"><tr>`;
    ['pg.sign','pg.h','pg.score','pg.sources'].forEach(key=>{
      html+=`<th style="color:${hCol}">${T(key)}</th>`;
    });
    html+='</tr>';
    ranked.forEach(d=>{
      const sign=SIGNS[d.sIdx];const el=SIGN_ELEMENT[sign];
      const hn=ascSIdx!==-1?((d.sIdx-ascSIdx+12)%12)+1:'–';
      const pct=Math.round(d.score/maxS*100);
      const bg=mode==='good'?BC.good:BC.bad;
      const uniq=SRCLIST([...new Set(d.sources)]);
      html+=`<tr><td><span class="el-${el}">${SN(sign)}</span></td><td style="text-align:center;color:#ffe060">${hn}</td>
        <td style="min-width:90px">${buildBar(pct,bg,'6px')}</td>
        <td style="font-size:8.5px;color:rgba(200,195,175,.55)">${uniq||'—'}</td></tr>`;
    });
    return html+'</table>';
  }

  // The three category breakdowns (element / modality / direction) share a
  // shape, so they share an order table too - key, translator, badge class.
  const CAT_ORDERS={
    el:  {title:'pg.elements',  label:EL, keys:['fire','earth','air','water']},
    mod: {title:'pg.modality',  label:MO, keys:['movable','fixed','mutable']},
    dir: {title:'pg.direction', label:DI, keys:['east','south','west','north']},
  };

  function buildCatSection(cat,mode){
    const color=mode==='good'?'rgba(68,221,136,.8)':'rgba(255,80,70,.8)';
    let html='';
    ['el','mod','dir'].forEach(key=>{
      const {title,label,keys}=CAT_ORDERS[key];
      const vals=Object.values(cat[key]);const maxV=Math.max(...vals,1);
      html+=`<div class="dash-section"><h3 style="color:${color}">✦ ${T(title)}</h3>`;
      keys.forEach(k=>{
        const pct=Math.round(cat[key][k]/maxV*100);
        html+=`<div class="dash-row"><div class="dash-label"><span class="dash-tag badge-${k}">${label(k)}</span></div>${buildBar(pct,BC[k])}<span class="dash-pct ${mode==='good'?'good-pct':'bad-pct'}">${pct}%</span></div>`;
      });
      html+='</div>';
    });
    return html;
  }

  // ═══════════════════════════════════════════════════
  //  UPDATE ALL DASHBOARDS
  // ═══════════════════════════════════════════════════
  function updateAllDashboards(){
    const anyPlaced=Object.values(cellPlanets).some(a=>a&&a.length>0);
    const ascSIdx=findPlanetSignIdx('Asc');
    const sunSIdx=findPlanetSignIdx('Sun');
    const moonSIdx=findPlanetSignIdx('Mon');
    const bright=moonSIdx!==-1?moonBrightness(moonSIdx,sunSIdx):1.0;

    const noData=`<div class="no-data" style="grid-column:1/-1">${T('pg.no_data')}</div>`;
    if(!anyPlaced){['good','bad','well','plan','stana','dig','total'].forEach(t=>sec(t).innerHTML=noData);updateSignColorsDashboard();return;}

    const {goodScores,badScores}=computeSignScores();
    const goodCat=aggregateCat(goodScores);
    const badCat=aggregateCat(badScores);

    // ── GOODNESS TAB ──
    const goodRanked=Object.entries(goodScores).map(([si,d])=>({sIdx:parseInt(si),...d})).filter(d=>d.score>0).sort((a,b)=>b.score-a.score);
    const moonPct=Math.round(bright*100);
    const dist=moonSIdx!==-1&&sunSIdx!==-1?((moonSIdx-sunSIdx+12)%12)+1:null;
    const phase=bright>=.99?`🌕 ${T('pg.full_moon')}`:bright<=.01?`🌑 ${T('pg.new_moon_short')}`
      :dist<=7?`🌒 ${T('pg.waxing',{pct:moonPct})}`:`🌖 ${T('pg.waning',{pct:moonPct})}`;
    const mc=moonColor(bright);
    const moonSection=`<div class="dash-section"><h3 class="good-h3">☽ ${T('pg.moon_phase')}</h3>
      <div style="display:flex;flex-direction:column;gap:6px">
        <div style="color:rgba(200,215,255,.9);font-size:12px">${phase}</div>
        ${dist!==null?`<div style="font-size:10px;color:rgba(180,190,220,.65)">${T('pg.house_from_sun',{n:`<b style="color:#ffe060">${dist}</b>`})}</div>`:''}
        <div style="display:flex;align-items:center;gap:8px">${buildBar(moonPct,'linear-gradient(90deg,#334466,#aaccff)')}<span class="dash-pct good-pct">${moonPct}%</span></div>
        <div style="display:flex;align-items:center;gap:6px;margin-top:4px">
          <div style="width:14px;height:14px;border-radius:50%;background:${mc.bg};border:1px solid rgba(150,170,220,.5)"></div>
          <span style="font-size:9px;color:rgba(200,215,255,.6)">${T('pg.moon_color_note')}</span>
        </div>
      </div></div>`;
    sec('good').innerHTML=
      `<div class="dash-section" style="grid-column:1/-1"><h3 class="good-h3">✦ ${T('pg.signs_goodness')}</h3>${buildSignsTable(goodRanked,ascSIdx,'good')}</div>`+
      buildCatSection(goodCat,'good')+moonSection;

    // ── BADNESS TAB ──
    const badRanked=Object.entries(badScores).map(([si,d])=>({sIdx:parseInt(si),...d})).filter(d=>d.score>0).sort((a,b)=>b.score-a.score);
    const moonBadPct=moonSIdx!==-1&&sunSIdx!==-1?Math.round(moonBadFactor(moonSIdx,sunSIdx)*100):0;
    const moonBadSection=`<div class="dash-section"><h3 class="bad-h3">☽ ${T('pg.moon_darkness')}</h3>
      ${moonBadPct===0?`<div class="no-data">${T('pg.moon_not_dark')}</div>`:`<div style="display:flex;flex-direction:column;gap:6px">
        <div style="color:rgba(255,160,140,.9);font-size:11px">${dist===1?`🌑 ${T('pg.new_moon')}`:dist===2?`🌒 ${T('pg.second_from_sun')}`:`🌘 ${T('pg.twelfth_from_sun')}`}</div>
        <div style="display:flex;align-items:center;gap:8px">${buildBar(moonBadPct,'linear-gradient(90deg,#660011,#cc2233)')}<span class="dash-pct bad-pct">${moonBadPct}%</span></div>
      </div>`}</div>`;
    sec('bad').innerHTML=
      `<div class="dash-section" style="grid-column:1/-1"><h3 class="bad-h3">☽ ${T('pg.signs_badness')}</h3>${buildSignsTable(badRanked,ascSIdx,'bad')}</div>`+
      buildCatSection(badCat,'bad')+moonBadSection;

    // ── WELLNESS TAB ──
    const wellRanked=Object.entries(goodScores).map(([si,d])=>{
      const b=badScores[parseInt(si)];const net=d.score-(b?.score||0);return{sIdx:parseInt(si),good:d.score,bad:b?.score||0,net};
    }).sort((a,b)=>b.net-a.net);
    const maxAbsNet=Math.max(...wellRanked.map(d=>Math.abs(d.net)),1);
    const maxGood=Math.max(...wellRanked.map(d=>d.good),1);
    const maxBad2=Math.max(...wellRanked.map(d=>d.bad),1);
    let wellHtml=`<div class="dash-section" style="grid-column:1/-1"><h3 class="well-h3">⊕ ${T('pg.signs_wellness')}</h3>
      <table class="signs-table"><tr>
        <th style="color:rgba(212,175,55,.7)">${T('pg.sign')}</th><th style="color:rgba(212,175,55,.7)">${T('pg.h')}</th>
        <th style="color:rgba(68,221,136,.7)">${T('pg.good')}</th><th style="color:rgba(255,80,70,.7)">${T('pg.bad')}</th>
        <th style="color:rgba(212,175,55,.7)">${T('pg.net')}</th></tr>`;
    wellRanked.forEach(d=>{
      const sign=SIGNS[d.sIdx];const el=SIGN_ELEMENT[sign];
      const hn=ascSIdx!==-1?((d.sIdx-ascSIdx+12)%12)+1:'–';
      const isPos=d.net>=0;
      const netPct=Math.round(Math.abs(d.net)/maxAbsNet*50);
      const netColor=isPos?'#44ff88':d.net<0?'#ff4433':'#aaa';
      const netBg=isPos?BC.good:BC.bad;
      const netStr=d.net>0?`+${Math.round(d.net)}`:Math.round(d.net)===0?'0':`${Math.round(d.net)}`;
      wellHtml+=`<tr><td><span class="el-${el}">${SN(sign)}</span></td><td style="text-align:center;color:#ffe060">${hn}</td>
        <td><span style="color:#44dd88;font-size:10px;font-weight:700">${Math.round(d.good/maxGood*100)}%</span></td>
        <td><span style="color:#ff6655;font-size:10px;font-weight:700">${Math.round(d.bad/maxBad2*100)}%</span></td>
        <td><div style="display:flex;align-items:center;gap:4px">
          <div style="width:80px;height:7px;background:rgba(255,255,255,.07);border-radius:3px;overflow:hidden;position:relative">
            <div style="position:absolute;${isPos?'right:0':'left:0'};top:0;height:100%;width:${netPct*2}%;background:${netBg};border-radius:3px"></div>
            <div style="position:absolute;left:50%;top:0;height:100%;width:1px;background:rgba(255,255,255,.25)"></div>
          </div>
          <span style="font-size:10px;font-weight:700;color:${netColor};min-width:34px">${netStr}</span>
        </div></td></tr>`;
    });
    wellHtml+='</table></div>';
    // Wellness categories
    const wellCatEl={},wellCatMod={},wellCatDir={};
    ['fire','earth','air','water'].forEach(k=>wellCatEl[k]=(goodCat.el[k]||0)-(badCat.el[k]||0));
    ['movable','fixed','mutable'].forEach(k=>wellCatMod[k]=(goodCat.mod[k]||0)-(badCat.mod[k]||0));
    ['east','south','west','north'].forEach(k=>wellCatDir[k]=(goodCat.dir[k]||0)-(badCat.dir[k]||0));
    function buildWellCat(catData,catKey){
      const {title,label,keys}=CAT_ORDERS[catKey];
      const maxAbs=Math.max(...Object.values(catData).map(v=>Math.abs(v)),1);
      let h=`<div class="dash-section"><h3 class="well-h3">⊕ ${T(title)}</h3>`;
      keys.forEach(k=>{
        const lbl=label(k);
        const net=catData[k];const pct=Math.round(Math.abs(net)/maxAbs*50);
        const isPos=net>0;const bg=isPos?BC.good:BC.bad;const col=isPos?'#44ff88':net<0?'#ff4433':'#aaa';
        const str=net>0?`+${Math.round(net)}`:Math.round(net)===0?'0':`${Math.round(net)}`;
        h+=`<div class="dash-row"><div class="dash-label"><span class="dash-tag badge-${k}">${lbl}</span></div>
          <div style="flex:1;height:8px;background:rgba(255,255,255,.07);border-radius:4px;overflow:hidden;position:relative">
            <div style="position:absolute;${isPos?'right:0':'left:0'};top:0;height:100%;width:${pct*2}%;background:${bg};border-radius:4px"></div>
            <div style="position:absolute;left:50%;top:0;height:100%;width:1px;background:rgba(255,255,255,.2)"></div>
          </div>
          <span style="min-width:40px;text-align:right;font-size:10px;font-weight:700;color:${col}">${str}</span></div>`;
      });
      return h+'</div>';
    }
    sec('well').innerHTML=wellHtml+
      buildWellCat(wellCatEl,'el')+
      buildWellCat(wellCatMod,'mod')+
      buildWellCat(wellCatDir,'dir');

    // ── SUBATHUVA (PLANET) TAB ──
    const pScores=computePlanetScores();
    const pEntries=Object.entries(pScores).map(([p,s])=>({planet:p,...s}));
    if(!pEntries.length){sec('plan').innerHTML=noData;}
    else {
    const maxPG=Math.max(...pEntries.map(e=>e.goodness),1);
    const maxPB=Math.max(...pEntries.map(e=>e.badness),1);
    const maxPW=Math.max(...pEntries.map(e=>Math.abs(e.wellness)),1);
    function makePlanetTable(rows,mode,maxV){
      if(!rows.length) return `<div class="no-data">${T('pg.none_simple')}</div>`;
      const color=mode==='good'?'rgba(68,221,136,.6)':mode==='bad'?'rgba(255,100,80,.6)':'rgba(204,136,255,.6)';
      const bg=mode==='good'?BC.good:mode==='bad'?BC.bad:null;
      return `<table style="width:100%;border-collapse:collapse;font-size:10px">
        <tr><th style="font-family:'Cinzel',serif;font-size:8px;color:${color};padding:2px 4px;border-bottom:1px solid rgba(255,255,255,.08)">${T('pg.planet')}</th>
        <th style="font-family:'Cinzel',serif;font-size:8px;color:rgba(200,195,175,.5);padding:2px 4px;border-bottom:1px solid rgba(255,255,255,.08)">${T('pg.score')}</th>
        <th style="font-family:'Cinzel',serif;font-size:8px;color:rgba(200,195,175,.5);padding:2px 4px;border-bottom:1px solid rgba(255,255,255,.08)">${T('pg.sources')}</th></tr>
        ${rows.map(e=>{
          const val=mode==='good'?e.goodness:mode==='bad'?e.badness:e.wellness;
          const pct=Math.round(Math.abs(val)/maxV*100);
          const isNeg=val<0;
          const barBg=mode==='wellness'?(isNeg?BC.bad:BC.good):(bg||BC.good);
          const vColor=mode==='good'?'#44ff88':mode==='bad'?'#ff6655':(isNeg?'#ff6655':'#44ff88');
          const vStr=mode==='wellness'?(val>=0?`+${Math.round(val)}`:`${Math.round(val)}`):Math.round(Math.abs(val));
          const src=SRCLIST((mode==='good'?e.goodSrc:mode==='bad'?e.badSrc:[...e.goodSrc,...e.badSrc]).slice(0,5));
          return `<tr><td style="padding:4px">${pBadge(e.planet)}</td>
            <td style="padding:4px"><div style="display:flex;align-items:center;gap:5px">${buildBar(pct,barBg,'6px')}<span style="font-size:10px;font-weight:700;color:${vColor};min-width:28px">${vStr}</span></div></td>
            <td style="padding:4px;font-size:8.5px;color:rgba(200,195,175,.5);max-width:140px;word-break:break-word">${src||'—'}</td></tr>`;
        }).join('')}</table>`;
    }
    const byG=[...pEntries].sort((a,b)=>b.goodness-a.goodness).filter(e=>e.goodness>0);
    const byB=[...pEntries].sort((a,b)=>b.badness-a.badness).filter(e=>e.badness>0);
    const byW=[...pEntries].sort((a,b)=>b.wellness-a.wellness);
    sec('plan').innerHTML=
      `<div class="dash-section"><h3 class="plan-h3">✦ ${T('pg.planet_goodness')}</h3>${makePlanetTable(byG,'good',maxPG)}</div>`+
      `<div class="dash-section"><h3 class="plan-h3">☽ ${T('pg.planet_badness')}</h3>${makePlanetTable(byB,'bad',maxPB)}</div>`+
      `<div class="dash-section" style="grid-column:span 2"><h3 class="plan-h3">☯ ${T('pg.planet_wellness')}</h3>
        <table style="width:100%;border-collapse:collapse;font-size:10px">
          <tr><th style="font-family:'Cinzel',serif;font-size:8px;color:rgba(204,136,255,.6);padding:2px 4px;border-bottom:1px solid rgba(255,255,255,.08)">${T('pg.planet')}</th>
          <th style="font-family:'Cinzel',serif;font-size:8px;color:rgba(68,221,136,.5);padding:2px 4px;border-bottom:1px solid rgba(255,255,255,.08)">${T('pg.good')}</th>
          <th style="font-family:'Cinzel',serif;font-size:8px;color:rgba(255,80,70,.5);padding:2px 4px;border-bottom:1px solid rgba(255,255,255,.08)">${T('pg.bad')}</th>
          <th style="font-family:'Cinzel',serif;font-size:8px;color:rgba(204,136,255,.5);padding:2px 4px;border-bottom:1px solid rgba(255,255,255,.08)">${T('pg.net')}</th>
          <th style="font-family:'Cinzel',serif;font-size:8px;color:rgba(200,195,175,.4);padding:2px 4px;border-bottom:1px solid rgba(255,255,255,.08)">${T('pg.influences')}</th></tr>
          ${byW.map(e=>{
            const wPct=Math.round(Math.abs(e.wellness)/maxPW*50);
            const gPct=Math.round(e.goodness/maxPG*100);
            const bPct=Math.round(e.badness/maxPB*100);
            const isPos=e.wellness>=0;
            const wC=isPos?'#44ff88':'#ff6655';
            const wBg=isPos?BC.good:BC.bad;
            const wStr=e.wellness>=0?`+${Math.round(e.wellness)}`:`${Math.round(e.wellness)}`;
            const src=SRCLIST([...new Set([...e.goodSrc,...e.badSrc])].slice(0,5));
            return `<tr><td style="padding:4px">${pBadge(e.planet)}</td>
              <td style="padding:4px"><span style="color:#44ff88;font-size:10px;font-weight:700">${gPct}%</span></td>
              <td style="padding:4px"><span style="color:#ff6655;font-size:10px;font-weight:700">${bPct}%</span></td>
              <td style="padding:4px"><div style="display:flex;align-items:center;gap:4px">
                <div style="width:70px;height:7px;background:rgba(255,255,255,.07);border-radius:3px;overflow:hidden;position:relative">
                  <div style="position:absolute;${isPos?'right:0':'left:0'};top:0;height:100%;width:${wPct*2}%;background:${wBg};border-radius:3px"></div>
                  <div style="position:absolute;left:50%;top:0;height:100%;width:1px;background:rgba(255,255,255,.25)"></div>
                </div>
                <span style="font-size:10px;font-weight:700;color:${wC};min-width:32px">${wStr}</span>
              </div></td>
              <td style="padding:4px;font-size:8.5px;color:rgba(200,195,175,.5);max-width:160px;word-break:break-word">${src||'—'}</td></tr>`;
          }).join('')}
        </table></div>`;
    } // end plan else block

    // ── STANA BALA TAB ──
    const stana=computeStanaBala();
    const stanaColor={'Exaltation':'#ffdd44','Moola Trikona':'#ffaa33','Own Sign':'#88ff88',"Friend's House":'#55ccff','Neutral':'#aaaaaa','Enemy House':'#ff6644','Debilitation':'#ff2222'};
    if(!stana.length){sec('stana').innerHTML=noData;}
    else {
    const maxStana=Math.max(...stana.map(s=>s.score),1);
    const sortedStana=[...stana].sort((a,b)=>b.score-a.score);
    sec('stana').innerHTML=
      `<div class="dash-section" style="grid-column:1/-1"><h3 class="stana-h3">★ ${T('pg.panel_stana')}</h3>
        <table class="signs-table"><tr>
          ${['pg.planet','pg.sign','pg.status','pg.score','pg.strength']
            .map(k=>`<th style="color:rgba(85,204,255,.7)">${T(k)}</th>`).join('')}</tr>
          ${sortedStana.map(({planet,sign,score,label,neechaBhanga})=>{
            const pct=Math.round(score/maxStana*100);
            const el=SIGN_ELEMENT[sign];
            const lColor=stanaColor[label.split('(')[0].trim()]||'#aaaaaa';
            return `<tr><td>${pBadge(planet)}</td>
              <td><span class="el-${el}">${SN(sign)}</span></td>
              <td style="font-size:9px;color:${lColor}">${I18N.term('stana_label',label)}${neechaBhanga?' 🔄':''}</td>
              <td style="font-weight:700;color:${lColor}">${score}</td>
              <td style="min-width:100px">${buildBar(pct,BC.stana,'6px')}</td></tr>`;
          }).join('')}
        </table>
        <div style="margin-top:10px;font-size:9px;color:rgba(200,195,175,.45)">${T('pg.stana_note')}</div>
      </div>`;
    } // end stana else block

    // ── DIG + NISH BALA TAB ──
    const digNish=computeDigNishBala();
    if(!digNish.length){sec('dig').innerHTML=noData;}
    else {
    const maxDig=Math.max(...digNish.map(d=>d.dig),1);
    const maxNish=Math.max(...digNish.map(d=>d.nish),1);
    const maxTotal=Math.max(...digNish.map(d=>d.total),1);
    const sortedDig=[...digNish].sort((a,b)=>b.total-a.total);
    sec('dig').innerHTML=
      `<div class="dash-section" style="grid-column:1/-1"><h3 class="dig-h3">◈ ${T('pg.panel_dig')}</h3>
        <table class="signs-table"><tr>
          <th style="color:rgba(255,153,170,.7)">${T('pg.planet')}</th>
          <th style="color:rgba(255,153,170,.7)">${T('pg.sign')}</th>
          <th style="color:rgba(255,153,170,.7)">${T('pg.dig_bala_info')}</th>
          <th style="color:rgba(85,204,255,.7)">${T('pg.dig')}</th>
          <th style="color:rgba(255,204,68,.7)">${T('pg.nish')}</th>
          <th style="color:rgba(255,153,170,.7)">${T('pg.combined')}</th></tr>
          ${sortedDig.map(({planet,sign,dig,nish,total})=>{
            const el=SIGN_ELEMENT[sign];
            const dPct=Math.round(dig/maxDig*100);
            const nPct=Math.round(nish/maxNish*100);
            const tPct=Math.round(total/maxTotal*100);
            return `<tr><td>${pBadge(planet)}</td>
              <td><span class="el-${el}">${SN(sign)}</span></td>
              <td style="font-size:8.5px;color:rgba(200,195,175,.55)">${I18N.term('dig_info',planet)||'—'}</td>
              <td><div style="display:flex;align-items:center;gap:3px">${buildBar(dPct,BC.dig,'5px')}<span style="color:#ff99aa;font-size:9px;min-width:22px">${dig}</span></div></td>
              <td><div style="display:flex;align-items:center;gap:3px">${buildBar(nPct,BC.total,'5px')}<span style="color:#ffcc44;font-size:9px;min-width:22px">${nish}</span></div></td>
              <td><div style="display:flex;align-items:center;gap:3px">${buildBar(tPct,BC.stana,'5px')}<span style="color:#55ccff;font-size:9px;min-width:22px">${total}</span></div></td>
            </tr>`;
          }).join('')}
        </table>
        <div style="margin-top:10px;font-size:9px;color:rgba(200,195,175,.4)">${T('pg.dig_note')}</div>
      </div>`;
    } // end dig else block

    // ── TOTAL STRENGTH TAB ──
    // Combine: Subathuva wellness (normalized) + Stana Bala (normalized) + Dig+Nish (normalized)
    // Weight: 40% Subathuva + 35% Stana + 25% Dig+Nish
    const stanaArr=typeof stana!=='undefined'&&Array.isArray(stana)?stana:[];
    const digNishArr=typeof digNish!=='undefined'&&Array.isArray(digNish)?digNish:[];
    const allPlanets=[...new Set([...stanaArr.map(s=>s.planet),...digNishArr.map(d=>d.planet),...Object.keys(pScores)])];
    const totalScores=allPlanets.map(planet=>{
      const sub=pScores[planet];
      const subW=sub?(sub.wellness)/(Math.max(...Object.values(pScores).map(s=>Math.abs(s.wellness)),1)):0;
      const stanaEntries=stanaArr.filter(s=>s.planet===planet);
      const stanaAvg=stanaEntries.length?stanaEntries.reduce((a,b)=>a+b.score,0)/stanaEntries.length:30;
      const digEntries=digNishArr.filter(d=>d.planet===planet);
      const digAvg=digEntries.length?digEntries.reduce((a,b)=>a+b.total,0)/digEntries.length:0;
      const total=Math.round(subW*40+stanaAvg*0.35+digAvg*0.25);
      const subWellStr=sub?`${sub.wellness>=0?'+':''}${Math.round(sub.wellness)}`:'-';
      const stanaLabel=stanaEntries.map(s=>I18N.term('stana_label',s.label)).join(', ')||'—';
      return{planet,subWell:sub?sub.wellness:0,stana:Math.round(stanaAvg),dig:Math.round(digAvg),total,subWellStr,stanaLabel};
    });
    const sortedTotal=[...totalScores].sort((a,b)=>b.total-a.total);
    const maxT=Math.max(...sortedTotal.map(s=>Math.abs(s.total)),1);
    sec('total').innerHTML=
      `<div class="dash-section" style="grid-column:1/-1"><h3 class="total-h3">⊛ ${T('pg.combined_strength')}</h3>
        <table class="signs-table"><tr>
          <th style="color:rgba(255,204,68,.7)">${T('pg.planet')}</th>
          <th style="color:rgba(204,136,255,.7)">${T('pg.subathuva')}</th>
          <th style="color:rgba(85,204,255,.7)">${T('pg.stana_bala')}</th>
          <th style="color:rgba(255,153,170,.7)">${T('pg.dig_nish')}</th>
          <th style="color:rgba(255,204,68,.7)">${T('pg.total_strength')}</th></tr>
          ${sortedTotal.map(({planet,subWellStr,stana:stS,dig:dg,total,stanaLabel})=>{
            const isPos=total>=0;
            const pct=Math.round(Math.abs(total)/maxT*100);
            const tColor=isPos?'#ffcc44':'#ff6655';
            const tBg=isPos?BC.total:BC.bad;
            return `<tr><td style="padding:4px">${pBadge(planet)}</td>
              <td style="padding:4px"><span style="color:${parseFloat(subWellStr)>=0?'#44ff88':'#ff6655'};font-size:10px;font-weight:700">${subWellStr}</span></td>
              <td style="padding:4px"><div style="display:flex;flex-direction:column;gap:1px"><span style="color:#55ccff;font-size:10px;font-weight:700">${stS}</span><span style="font-size:8px;color:rgba(200,195,175,.45)">${stanaLabel}</span></div></td>
              <td style="padding:4px"><span style="color:#ff99aa;font-size:10px;font-weight:700">${dg}</span></td>
              <td style="padding:4px"><div style="display:flex;align-items:center;gap:5px">
                ${buildBar(pct,tBg,'8px')}
                <span style="font-size:11px;font-weight:700;color:${tColor};min-width:32px">${total>0?'+'+total:total}</span>
              </div></td></tr>`;
          }).join('')}
        </table>
        <div style="margin-top:10px;font-size:9px;color:rgba(200,195,175,.4)">${T('pg.total_note')}</div>
      </div>`;

    // ── SIGN COLORS TAB ──
    updateSignColorsDashboard();
  }


  // ═══════════════════════════════════════════════════
  //  SIGN COLORS DASHBOARD
  // ═══════════════════════════════════════════════════

  // Human-readable colour names live in the shared dictionary now, so they read
  // the same on this page as anywhere else - see TERMS["planet_colour"].
  const PLANET_COLOR_NAME=(planet)=>I18N.term('planet_colour',planet);

  // Named colors for blended results (rough perceptual mapping)
  function blendedColorName(layers){
    // layers = [{planet,type,rgb}]  type='placement'|'aspect'
    if(!layers.length) return {name:T('pg.default_parchment'),hex:'#c8bd9e'};

    // Find the dominant hue based on planets present
    const names=layers.map(l=>l.type==='aspect'?T('pg.aspect_overlay'):PLANET_COLOR_NAME(l.planet));
    // Compute blended RGB
    // We use the same radial-gradient stacking the chart does, but for the
    // card swatch we blend all equally
    let r=200,g=189,b=158; // parchment base in RGB
    layers.forEach(l=>{
      if(l.type==='aspect') return; // aspect color is overlay, keep base visual close
      const[pr,pg,pb]=l.rgb;
      // Average in each planet colour at 62% weight toward it
      r=Math.round(r*0.5+pr*0.5);
      g=Math.round(g*0.5+pg*0.5);
      b=Math.round(b*0.5+pb*0.5);
    });
    const hex='#'+[r,g,b].map(v=>v.toString(16).padStart(2,'0')).join('');
    return{name:names.join(' + '),hex};
  }

  function rgbToHex(rgb){
    return '#'+rgb.map(v=>Math.max(0,Math.min(255,v)).toString(16).padStart(2,'0')).join('');
  }

  // Get text color for a background (light vs dark)
  function contrastText(hex){
    const r=parseInt(hex.slice(1,3),16),g=parseInt(hex.slice(3,5),16),b=parseInt(hex.slice(5,7),16);
    const lum=(0.299*r+0.587*g+0.114*b)/255;
    return lum>0.45?'#1a1000':'#f0e8d0';
  }

  function updateSignColorsDashboard(){
    const el=sec('sigcol');
    if(!el) return;

    const anyPlaced=Object.values(cellPlanets).some(a=>a&&a.length>0);
    if(!anyPlaced){el.innerHTML=`<div class="no-data">${T('pg.no_data_colors')}</div>`;return;}

    const sunSIdx=findPlanetSignIdx('Sun');

    // For every sign, collect which planets color it and how (placement vs aspect)
    // signInfo[signIdx] = [{planet, type:'placement'|'aspect', rgb, colorName, hex}]
    const signInfo={};
    for(let i=0;i<12;i++) signInfo[i]=[];

    for(let pos=0;pos<16;pos++){
      if(!cellPlanets[pos]?.length||!GRID_SIGNS[pos]) continue;
      const si=SIGNS.indexOf(GRID_SIGNS[pos]);
      cellPlanets[pos].forEach(planet=>{
        if(planet==='Asc') return;
        // Only include if showColor is on for this planet
        if(!showColor[planet]) return;

        const offsets=getAspectOffsets(planet,si,sunSIdx);
        offsets.forEach(off=>{
          const target=aspectSign(si,off);
          let rgb;
          if(planet==='Mon'){
            const bright=moonBrightness(si,sunSIdx);
            if(bright<=0) return;
            rgb=moonColor(bright).mix;
          } else {
            rgb=PLANET_BASE[planet].mix;
            if(!rgb) return;
          }

          const type=(off===1)?'placement':'aspect';
          const hex=rgbToHex(rgb);

          // Avoid duplicate entries for same planet+sign combo
          const already=signInfo[target].find(e=>e.planet===planet&&e.type===type);
          if(!already){
            let colorNameStr;
            if(planet==='Mon'){
              const bright=moonBrightness(si,sunSIdx);
              const moonPct=Math.round(bright*100);
              colorNameStr=moonPct>=99?T('pg.full_moon_silver'):moonPct<=1?T('pg.new_moon_dark'):
                           T('pg.moon_brightness',{pct:moonPct});
            } else {
              colorNameStr=type==='aspect'?T('pg.aspect_overlay'):PLANET_COLOR_NAME(planet);
            }
            signInfo[target].push({planet,type,rgb,hex,colorNameStr});
          }
        });
      });
    }

    // Build the grid of sign color cards
    // Group into rows of 4 (matching the chart layout order)
    const gridOrder=['Pisces','Aries','Taurus','Gemini','Aquarius','Cancer','Capricorn','Leo','Sagittarius','Scorpio','Libra','Virgo'];

    let html=`<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:12px;padding:4px 0;">`;

    gridOrder.forEach(signName=>{
      const sIdx=SIGNS.indexOf(signName);
      const layers=signInfo[sIdx];
      const el2=SIGN_ELEMENT[signName];

      // Compute blended background for the swatch
      let swatchBg='#c8bd9e'; // default parchment
      let swatchText='#1a1000';
      if(layers.length){
        // Do a proper blend: start with parchment, overlay each planet color
        let r=200,g=189,b=158;
        layers.forEach((l,i)=>{
          const alpha=0.55;
          r=Math.round(r*(1-alpha)+l.rgb[0]*alpha);
          g=Math.round(g*(1-alpha)+l.rgb[1]*alpha);
          b=Math.round(b*(1-alpha)+l.rgb[2]*alpha);
        });
        swatchBg='#'+[r,g,b].map(v=>v.toString(16).padStart(2,'0')).join('');
        swatchText=contrastText(swatchBg);
      }

      // Planet chips
      const chipsHtml=layers.map(l=>{
        const chipBg=l.type==='aspect'?'rgba(255,255,255,.08)':l.hex+'33';
        const chipBorder=l.type==='aspect'?'rgba(255,255,255,.15)':l.hex+'88';
        const chipText=l.type==='aspect'?'rgba(200,195,175,.65)':l.hex;
        return `<span class="sign-color-chip" style="background:${chipBg};border:1px solid ${chipBorder};color:${chipText};">
          ${l.type!=='aspect'?`<span class="chip-dot" style="background:${l.hex};"></span>`:''}
          <span title="${PN(l.planet)}">${PA(l.planet)}</span>
          <span style="font-weight:400;opacity:.7;font-size:7.5px">${l.type==='aspect'?T('pg.aspect_tag'):T('pg.placed_tag')}</span>
        </span>`;
      });

      // Color name strings
      const placedLayers=layers.filter(l=>l.type==='placement');
      const aspectLayers=layers.filter(l=>l.type==='aspect');
      const colorDesc=layers.length===0?T('pg.default_parchment'):
        [
          ...placedLayers.map(l=>l.colorNameStr),
          ...aspectLayers.length?['+ '+T('pg.aspect_overlay')]:[]
        ].join(', ');

      html+=`<div class="sign-color-card">
        <div class="sign-color-row">
          <!-- Swatch -->
          <div class="sign-swatch" style="background:${swatchBg};display:flex;align-items:center;justify-content:center;">
            <span style="font-family:'Cinzel',serif;font-size:9px;font-weight:700;color:${swatchText};text-align:center;line-height:1.2;padding:2px;">${shortLabel(SN(signName),3)}</span>
          </div>
          <!-- Info -->
          <div class="sign-color-info">
            <div class="sign-name">
              <span class="el-${el2}">${SN(signName)}</span>
              <span style="font-size:8px;margin-left:4px;color:rgba(200,195,175,.4)">${swatchBg}</span>
            </div>
            ${layers.length===0
              ? `<div style="font-size:9px;color:rgba(200,195,175,.35);font-style:italic">${T('pg.no_influence')}</div>`
              : `<div class="sign-color-layers">${chipsHtml.join('')}</div>`
            }
            <div style="font-size:8px;color:rgba(200,195,175,.4);margin-top:3px;">${colorDesc}</div>
          </div>
        </div>
      </div>`;
    });

    html+='</div>';
    el.innerHTML=html;
  }

  // ── LANGUAGE ──────────────────────────────────────
  // Two kinds of text need attention on a switch: the few strings that
  // interpolate a translated value (so a plain data-i18n attribute can't carry
  // them), and everything the dashboards build at render time. I18N.apply()
  // covers the rest - the static chrome and the sign labels on the grid.
  function refreshStaticText(){
    const legend=root.querySelector('.legend');
    if(legend) legend.innerHTML=T('pg.legend',{asc:PA('Asc')});
    PLANETS.forEach(p=>{
      const arr=cbArrows[p];
      if(arr) arr.title=T('pg.show_arrows_for',{planet:PN(p)});
      const col=cbColors[p];
      if(col) col.title=T('pg.show_colors_for',{planet:PN(p)});
      // "<planet> (on chart)" placeholders are written once, when the planet
      // leaves the palette, so they need retranslating in place.
      const ph=paletteSlots[p]?.querySelector('.palette-placeholder');
      if(ph) ph.textContent=T('pg.on_chart',{planet:PN(p)});
      // Same for the palette tokens themselves. updateAll() rebuilds the ones
      // sitting on the chart (renderCell re-runs createToken), but a token still
      // in its palette slot is only ever built once - at init, or when the
      // planet comes back off the chart - so without this it keeps whichever
      // language it was born in.
      const tok=paletteSlots[p]?.querySelector('.planet-token');
      if(tok){ tok.textContent=PA(p); tok.title=PN(p); }
    });
  }

  // ── CONTROL WIRING ─────────────────────────────────
  // These used to be inline onclick/oninput attributes calling page-global
  // functions; with two charts on screen each panel has to reach its own.
  root.querySelector('.js-clear').addEventListener('click',clearAll);
  root.querySelector('.ray-opacity').addEventListener('input',function(){onRayOpacityChange(this);});
  root.querySelector('.cb-master-arrow').addEventListener('change',function(){toggleAllCb('arrow',this.checked);});
  root.querySelector('.cb-master-color').addEventListener('change',function(){toggleAllCb('color',this.checked);});
  root.querySelector('.dash-tabs').addEventListener('click',function(e){
    const tab=e.target.closest('.dash-tab');
    if(tab) switchTab(tab.dataset.tab);
  });

  // ── INIT ────────────────────────────────────────────
  I18N.apply(root);   // the clone carries data-i18n markers but was never translated
  refreshStaticText();
  updateAll();
  I18N.onChange(()=>{
    refreshStaticText();
    updateAll();   // redraws tokens, house numbers, rays and all 8 dashboards
  });
  window.addEventListener('resize',updateRays);

  // ── PUBLIC API ─────────────────────────────────────
  // Placements travel between charts as a plain {planet: sign} map - the same
  // shape the ?positions= URL param uses - so copy/swap and URL loading share
  // one code path.
  return {
    root,
    updateAll,
    clearAll,
    setTab:(tab)=>switchTab(tab,false),
    getTab:()=>activeTab,
    getPlacements(){
      const out={};
      for(let pos=0;pos<16;pos++){
        if(!GRID_SIGNS[pos]) continue;
        (cellPlanets[pos]||[]).forEach(p=>{out[p]=GRID_SIGNS[pos];});
      }
      return out;
    },
    setPlacements(map){
      clearAll();
      Object.entries(map||{}).forEach(([planet,sign])=>{
        const pos=GRID_SIGNS.findIndex(s=>s===sign);
        if(pos===-1||!PLANETS.includes(planet)) return;
        addPlanetToCell(pos,planet);
      });
    },
  };
}

// ══════════════════════════════════════════════════
//  PANELS — SINGLE CHART vs COMPARE
// ══════════════════════════════════════════════════
// Chart A is built at load. Chart B is built the first time compare is
// switched on and then only hidden/shown, so its placements survive a trip
// back to single mode - and its I18N/resize listeners are registered once.
const panelsEl=document.getElementById('panels');
const panelTpl=document.getElementById('panelTpl');
const compareToggle=document.getElementById('compareToggle');
const compareLabel=document.getElementById('compareToggleLabel');
const syncTabsCb=document.getElementById('syncTabs');

function buildPanel(side,labelKey){
  const node=panelTpl.content.firstElementChild.cloneNode(true);
  node.classList.add('panel-'+side);
  const badge=node.querySelector('.panel-badge');
  badge.setAttribute('data-i18n',labelKey);
  badge.textContent=T(labelKey);
  panelsEl.appendChild(node);
  return createChart(node,{
    onTabChange:(tab)=>{
      // Mirror the tab onto the other chart so the same two numbers sit
      // side by side - unless the user has unlinked them.
      if(!compareOn||!syncTabsCb.checked) return;
      const other=(side==='a')?chartB:chartA;
      if(other) other.setTab(tab);
    },
  });
}

let compareOn=false;
const chartA=buildPanel('a','pg.chart_a');
let chartB=null;

function setCompare(on){
  compareOn=on;
  if(on&&!chartB) chartB=buildPanel('b','pg.chart_b');
  document.body.classList.toggle('compare',on);
  if(chartB) chartB.root.hidden=!on;
  compareToggle.setAttribute('aria-pressed',on?'true':'false');
  compareLabel.setAttribute('data-i18n',on?'pg.compare_exit':'pg.compare');
  compareLabel.textContent=T(on?'pg.compare_exit':'pg.compare');
  // --cell (and so every ray endpoint) changes with the layout, so both
  // charts are redrawn once the new widths have actually been applied.
  requestAnimationFrame(()=>{
    chartA.updateAll();
    if(on&&chartB) chartB.updateAll();
  });
  if(on&&chartB&&syncTabsCb.checked) chartB.setTab(chartA.getTab());
}

compareToggle.addEventListener('click',()=>setCompare(!compareOn));
syncTabsCb.addEventListener('change',function(){
  if(this.checked&&chartB) chartB.setTab(chartA.getTab());
});
document.getElementById('copyAB').addEventListener('click',()=>{
  if(chartB) chartB.setPlacements(chartA.getPlacements());
});
document.getElementById('copyBA').addEventListener('click',()=>{
  if(chartB) chartA.setPlacements(chartB.getPlacements());
});
document.getElementById('swapAB').addEventListener('click',()=>{
  if(!chartB) return;
  const a=chartA.getPlacements(),b=chartB.getPlacements();
  chartA.setPlacements(b);chartB.setPlacements(a);
});
// The toggle's label is the one string whose key changes at runtime, so it is
// re-read on a language switch; data-i18n + I18N.apply() cover everything else.
I18N.onChange(()=>{
  compareLabel.textContent=T(compareOn?'pg.compare_exit':'pg.compare');
});

// ── AUTO-LOAD POSITIONS FROM APP ─────────────────────
// When opened from the "🪐 Play with Chart" button on the main app, the
// Rashi (D1) planet placements are passed in the URL as a JSON-encoded
// map of {"Sun":"Leo","Mon":"Taurus",...,"Asc":"Aries"}. Drop each planet
// straight into its sign's cell so the chart opens already populated —
// everything else (drag/drop, dashboards, aspect rays) keeps working
// exactly as if it had been placed by hand. A second map in ?positions_b=
// opens the page in compare mode with both charts filled in.
(function loadPositionsFromURL(){
  const params=new URLSearchParams(location.search);
  const parse=(raw)=>{
    if(!raw) return null;
    try{ return JSON.parse(raw); }
    catch(err){ console.warn('Could not load planet positions from URL:',err); return null; }
  };
  const a=parse(params.get('positions'));
  const b=parse(params.get('positions_b'));
  if(a) chartA.setPlacements(a);
  if(b||params.get('compare')==='1'){
    setCompare(true);
    if(b) chartB.setPlacements(b);
  }
})();

// ── PWA: register the same service worker as the main app ──────────────
if('serviceWorker' in navigator){
  window.addEventListener('load',()=>{
    navigator.serviceWorker.register('/service-worker.js').catch(()=>{});
  });
}
</script>
</body>
</html>
