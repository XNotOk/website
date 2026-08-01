import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pyfront.core.app import App
from pyfront.core.base import Component
from pyfront.dom import tags
from pyfront.styling.engine import Style, dict_to_css
from pyfront.utils.html_tools import Raw


NAVY = "#1a1a2e"
GOLD = "#fbb13c"
WHITE = "#ffffff"
LIGHT = "#f8f9fa"
GREY = "#6c757d"


def global_styles() -> str:
    base = {
        "font-family": "'Segoe UI', system-ui, -apple-system, sans-serif",
        "color": "#2d2d2d",
        "line-height": "1.6",
        "background": LIGHT,
    }
    return dict_to_css({"*": {"margin": "0", "padding": "0", "box-sizing": "border-box"}, "body": base}) + f"""
html {{ scroll-behavior: smooth; }}
@keyframes pf-fade-up {{ from {{ opacity: 0; transform: translateY(18px); }} to {{ opacity: 1; transform: translateY(0); }} }}
@keyframes pf-float {{ 0%,100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-10px); }} }}
.hero-anim {{ animation: pf-fade-up .7s ease both; }}
.hero-anim-1 {{ animation: pf-fade-up .7s ease .1s both; }}
.hero-anim-2 {{ animation: pf-fade-up .7s ease .2s both; }}
.hero-anim-3 {{ animation: pf-fade-up .7s ease .3s both; }}
.hero-cab {{ animation: pf-float 6s ease-in-out infinite; }}
.feature-card {{ transition: transform .3s ease, box-shadow .3s ease; }}
.feature-card:hover {{ transform: translateY(-6px); box-shadow: 0 18px 44px rgba(0,0,0,0.14) !important; }}
.hero-inner {{ display: flex; align-items: center; gap: 48px; max-width: 1100px; margin: 0 auto; text-align: left; }}
.hero-text {{ flex: 1; min-width: 0; }}
.hero-visual {{ flex: 1; min-width: 0; display: flex; justify-content: center; }}
.hero-cab {{ width: 100%; max-width: 460px; height: auto; display: block; filter: drop-shadow(0 24px 40px rgba(0,0,0,0.45)); }}
.hero-stats {{ display: flex; gap: 40px; margin-top: 36px; flex-wrap: wrap; }}
.hero-stat {{ text-align: left; }}
.hero-stat b {{ display: block; font-size: 26px; color: #fff; line-height: 1.1; }}
.hero-stat span {{ font-size: 12px; color: rgba(255,255,255,0.65); text-transform: uppercase; letter-spacing: 1px; }}
.features-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-top: 40px; }}
.steps-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-top: 40px; }}
.step-num {{ width: 40px; height: 40px; border-radius: 50%; background: {GOLD}; color: {NAVY}; display: flex; align-items: center; justify-content: center; font-size: 17px; font-weight: 800; margin-bottom: 14px; }}
@media (max-width: 768px) {{
.nav-links {{ display: none; flex-direction: column; position: absolute; top: 64px; left: 0; right: 0; background: {NAVY}; padding: 20px; gap: 20px; z-index: 1000; }}
.nav-links.open {{ display: flex; }}
.nav-toggle {{ display: block; }}
.nav-toggle span {{ display: block; width: 24px; height: 3px; background: {WHITE}; margin: 5px 0; border-radius: 2px; transition: all .3s; }}
.hero-title {{ font-size: 28px !important; }}
.hero-sub {{ font-size: 15px !important; }}
.hero-inner {{ flex-direction: column; text-align: center; gap: 24px; }}
.hero-stats {{ justify-content: center; }}
.hero-stat {{ text-align: center; }}
.hero-visual {{ order: -1; }}
.hero-cab {{ max-width: 300px; }}
.lookup-card {{ padding: 28px 20px !important; }}
.lookup-row {{ flex-direction: column !important; }}
.quote-card {{ padding: 28px 20px !important; }}
.quote-grid {{ grid-template-columns: 1fr !important; }}
.fares-table-wrap {{ overflow-x: auto !important; }}
.features-grid {{ grid-template-columns: 1fr; }}
.steps-grid {{ grid-template-columns: 1fr; }}
}}
@media (min-width: 769px) {{
.nav-toggle {{ display: none; }}
.nav-links {{ display: flex !important; gap: 32px; align-items: center; }}
}}
"""


def page_wrapper(current_page: str, body: str) -> str:
    nav_js = """
    <script>
    function toggleNav() {
        document.getElementById('nav-links').classList.toggle('open');
    }
    </script>
    """
    return "".join([
        nav_js,
        _header(current_page),
        body,
        _footer(),
    ])


def _header(active: str) -> str:
    s = Style({
        "background": NAVY,
        "padding": "12px 32px",
        "display": "flex",
        "align-items": "center",
        "justify-content": "space-between",
        "position": "relative",
    })
    logo_wrap = Style({
        "background": WHITE,
        "border-radius": "8px",
        "padding": "4px 14px 4px 4px",
        "display": "inline-flex",
        "align-items": "center",
        "gap": "10px",
        "text-decoration": "none",
    })
    logo_img = Style({
        "height": "36px",
        "width": "auto",
        "display": "block",
    })
    logo_text = Style({
        "font-family": "'Times New Roman', Times, serif",
        "font-size": "20px",
        "font-weight": "700",
        "color": NAVY,
        "letter-spacing": "-0.5px",
    })
    link = Style({
        "color": WHITE,
        "font-size": "14px",
        "font-weight": "500",
        "padding": "8px 0",
        "text-decoration": "none",
        "transition": "color 0.3s",
        ":hover": {"color": GOLD},
    })
    link_active = Style({
        "color": GOLD,
        "font-size": "14px",
        "font-weight": "500",
        "padding": "8px 0",
        "text-decoration": "none",
    })
    btn = Style({
        "background": GOLD,
        "color": NAVY,
        "padding": "8px 24px",
        "border-radius": "50px",
        "font-size": "13px",
        "font-weight": "700",
        "text-decoration": "none",
        "transition": "background 0.3s",
        ":hover": {"background": "#e89f2c"},
    })

    links = [
        ("Home", "index.html"),
        ("Heathrow", "heathrow.html"),
    ]

    def nav_link(label: str, href: str) -> str:
        if active == label:
            return tags.a(href=href, class_=link_active.class_name)(label).render()
        return tags.a(href=href, class_=link.class_name)(label).render()

    nav_items = "".join(nav_link(l, h) for l, h in links)
    quote_btn = tags.a(href="quote.html", class_=btn.class_name)("Get a Quote").render()

    return tags.nav(class_=s.class_name)(
        tags.a(href="index.html", class_=logo_wrap.class_name)(
            tags.img(src="logo.png", alt="Fare-Cab", class_=logo_img.class_name),
            tags.span(class_=logo_text.class_name)("Fare Cab"),
        ),
        tags.div(class_="nav-toggle", onclick="toggleNav()")(
            Raw('<span></span><span></span><span></span>'),
        ),
        tags.div(id="nav-links", class_="nav-links")(
            Raw(nav_items + quote_btn),
        ),
    ).render()


def _footer() -> str:
    s = Style({
        "background": NAVY,
        "color": WHITE,
        "padding": "32px 24px 20px",
        "text-align": "center",
    })
    logo_wrap = Style({
        "background": WHITE,
        "border-radius": "6px",
        "padding": "3px 6px",
        "display": "inline-flex",
        "align-items": "center",
        "margin-bottom": "8px",
    })
    logo_img = Style({
        "height": "24px",
        "width": "auto",
        "display": "block",
    })
    link = Style({
        "color": "rgba(255,255,255,0.6)",
        "font-size": "13px",
        "text-decoration": "none",
        "margin": "0 10px",
        "transition": "color 0.3s",
        ":hover": {"color": GOLD},
    })
    p_s = Style({
        "font-size": "12px",
        "color": "rgba(255,255,255,0.4)",
        "margin-top": "12px",
    })
    return tags.footer(class_=s.class_name)(
        tags.div(class_=logo_wrap.class_name)(
            tags.img(src="logo.png", alt="Fare-Cab", class_=logo_img.class_name),
        ),
        tags.div(style={"margin-top": "8px"})(
            tags.a(href="index.html", class_=link.class_name)("Home"),
            tags.a(href="heathrow.html", class_=link.class_name)("Heathrow"),
            tags.a(href="quote.html", class_=link.class_name)("Get a Quote"),
        ),
        tags.p(style={"margin-top": "8px", "font-size": "13px", "color": "rgba(255,255,255,0.6)"})(
            tags.a(href="mailto:support@fare-cab.co.uk", style={"color": "#fbb13c", "text-decoration": "none"})("support@fare-cab.co.uk"),
        ),
        tags.p(class_=p_s.class_name)("Copyright 2026 Fare-Cab. All rights reserved."),
    ).render()


def _min_fare() -> float:
    rows = _get_fares_data()
    return min(cost for _, cost, _ in rows)


CAB_SVG = """<svg viewBox="0 0 520 260" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="London black cab" class="hero-cab">
<defs>
  <linearGradient id="pf-cab-body" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#23262e"/>
    <stop offset="1" stop-color="#0f1115"/>
  </linearGradient>
  <linearGradient id="pf-cab-glass" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#8fd3f2"/>
    <stop offset="1" stop-color="#cdeefb"/>
  </linearGradient>
</defs>
<ellipse cx="260" cy="222" rx="210" ry="14" fill="rgba(0,0,0,0.35)"/>
<g>
  <path d="M66 196 Q58 196 58 188 L58 172 Q58 158 72 158 L96 158 L112 120 Q118 108 132 108 L252 108 Q264 108 274 116 L306 142 Q322 156 342 156 L374 156 Q400 156 400 178 L400 196 Z" fill="url(#pf-cab-body)" stroke="#05060a" stroke-width="2"/>
  <path d="M96 158 L112 120 Q118 108 132 108 L236 108 Q250 108 260 116 L282 138 Q288 146 298 146 L340 146" fill="none" stroke="#33373f" stroke-width="3"/>
  <path d="M118 152 L132 118 Q138 108 152 108 L210 108 Q226 108 234 122 L252 148" fill="url(#pf-cab-glass)" stroke="#1c2026" stroke-width="2"/>
  <path d="M262 148 Q274 130 288 130 L326 130 Q340 130 352 142 L370 152" fill="url(#pf-cab-glass)" stroke="#1c2026" stroke-width="2"/>
  <rect x="120" y="162" width="266" height="26" rx="8" fill="url(#pf-cab-glass)" stroke="#1c2026" stroke-width="2" opacity="0.85"/>
  <path d="M220 162 L220 188" stroke="#1c2026" stroke-width="2"/>
  <rect x="84" y="176" width="22" height="10" rx="4" fill="#e05a4e"/>
  <rect x="402" y="176" width="26" height="12" rx="5" fill="#fbb13c"/>
  <rect x="140" y="158" width="110" height="14" rx="7" fill="#fbb13c"/>
  <circle cx="150" cy="214" r="32" fill="#05060a"/>
  <circle cx="150" cy="214" r="14" fill="#2b2f37"/>
  <circle cx="368" cy="214" r="32" fill="#05060a"/>
  <circle cx="368" cy="214" r="14" fill="#2b2f37"/>
  <path d="M150 182 L150 214 M150 214 L132 228 M150 214 L168 228" stroke="#1b1e24" stroke-width="3" opacity="0.6"/>
  <path d="M368 182 L368 214 M368 214 L350 228 M368 214 L386 228" stroke="#1b1e24" stroke-width="3" opacity="0.6"/>
  <rect x="66" y="120" width="8" height="38" rx="4" fill="#e05a4e"/>
  <rect x="408" y="118" width="10" height="40" rx="5" fill="#fbb13c"/>
</g>
<text x="260" y="250" text-anchor="middle" font-family="Times New Roman, serif" font-size="15" font-weight="bold" fill="#fbb13c" letter-spacing="4">FARE CAB</text>
</svg>"""


class HeroSection(Component):
    def render(self) -> str:
        s = Style({
            "background": f"linear-gradient(135deg, {NAVY} 0%, #0f3460 100%)",
            "padding": "80px 24px",
            "position": "relative",
            "overflow": "hidden",
        })
        h1_s = Style({
            "font-size": "44px",
            "font-weight": "800",
            "color": WHITE,
            "max-width": "620px",
            "margin-bottom": "16px",
            "line-height": "1.15",
        })
        p_s = Style({
            "font-size": "17px",
            "color": "rgba(255,255,255,0.8)",
            "max-width": "500px",
            "margin-bottom": "32px",
        })
        btn = Style({
            "display": "inline-block",
            "background": GOLD,
            "color": NAVY,
            "padding": "14px 36px",
            "border-radius": "50px",
            "font-size": "16px",
            "font-weight": "700",
            "text-decoration": "none",
            "transition": "background 0.3s, transform 0.3s",
            ":hover": {"background": "#e89f2c", "transform": "translateY(-2px)"},
        })
        btn_ghost = Style({
            "display": "inline-block",
            "border": "1px solid rgba(255,255,255,0.5)",
            "color": WHITE,
            "padding": "14px 36px",
            "border-radius": "50px",
            "font-size": "16px",
            "font-weight": "700",
            "text-decoration": "none",
            "margin-left": "12px",
            "transition": "background 0.3s, transform 0.3s",
            ":hover": {"background": "rgba(255,255,255,0.12)", "transform": "translateY(-2px)"},
        })
        badge = Style({
            "display": "inline-block",
            "background": "rgba(255,255,255,0.12)",
            "border": "1px solid rgba(255,255,255,0.25)",
            "color": "#fff",
            "padding": "8px 20px",
            "border-radius": "50px",
            "font-size": "13px",
            "font-weight": "600",
            "margin-bottom": "24px",
        })
        cta_row = Style({
            "display": "flex",
            "flex-wrap": "wrap",
            "gap": "12px",
        })
        return tags.section(class_=s.class_name)(
            tags.div(class_="hero-inner")(
                tags.div(class_="hero-text")(
                    tags.div(class_="hero-anim-1")(
                        tags.span(class_=badge.class_name)(f"Fares from \u00a3{_min_fare():.0f}"),
                    ),
                    tags.h1(class_=f"{h1_s.class_name} hero-title hero-anim-1", style={"font-size": "44px"})("London Black Cab Fares"),
                    tags.p(class_=f"{p_s.class_name} hero-sub hero-anim-2")(
                        "Know your fare before you ride. Instant Heathrow airport transfer pricing — fixed, no meter, no surprises."
                    ),
                    tags.div(class_=f"{cta_row.class_name} hero-anim-2")(
                        tags.a(href="heathrow.html", class_=btn.class_name)("Check Heathrow Fare"),
                        tags.a(href="quote.html", class_=btn_ghost.class_name)("Get a Quote"),
                    ),
                    tags.div(class_="hero-stats hero-anim-3")(
                        tags.div(class_="hero-stat")(
                            Raw(f"<b>from \u00a3{_min_fare():.0f}</b>"),
                            tags.span()("Heathrow fares"),
                        ),
                        tags.div(class_="hero-stat")(
                            Raw("<b>100+</b>"),
                            tags.span()("Postcode areas"),
                        ),
                        tags.div(class_="hero-stat")(
                            Raw("<b>24/7</b>"),
                            tags.span()("Always available"),
                        ),
                    ),
                ),
                tags.div(class_="hero-visual hero-anim-3")(
                    Raw(CAB_SVG),
                ),
            ),
        ).render()


def _get_fares_data():
    from fares_db import get_conn
    with get_conn() as conn:
        return conn.execute(
            "SELECT postcode_prefix, cost, zone FROM fares ORDER BY postcode_prefix"
        ).fetchall()


def _fares_js_obj(rows) -> str:
    items = [f'"{p}":{{"cost":{c},"zone":"{z}"}}' for p, c, z in rows]
    return "{" + ",".join(items) + "}"


def _fare_lookup_html(rows) -> str:
    return f"""
    <script>
    const FARES = {_fares_js_obj(rows)};
    function lookupFare() {{
        const input = document.getElementById('pcode');
        const result = document.getElementById('fresult');
        const raw = input.value.trim().toUpperCase();
        if (!raw) {{
            result.style.display = 'block'; result.style.background = '#fff3cd'; result.style.color = '#856404';
            result.innerHTML = 'Enter a postcode area like SW1 or N1.'; return;
        }}
        function show(prefix, zone) {{
            const f = FARES[prefix];
            result.style.background = '#d4edda'; result.style.color = '#155724';
            result.innerHTML = '<div style="font-size:14px">Fares from <strong>'+prefix+'</strong> ('+zone+') to Heathrow:</div>' +
                '<div style="font-size:36px;font-weight:800;color:#1a1a2e">from \u00a3'+Math.round(f.cost)+'</div>' +
                '<div style="font-size:12px;margin-top:6px;opacity:.75">Fixed price, no hidden extras.</div>';
            result.style.display = 'block';
        }}
        const exact = FARES[raw];
        if (exact) {{ show(raw, exact.zone); return; }}
        let match=null, ml=0;
        for(const k of Object.keys(FARES)) {{ if(raw.startsWith(k)&&k.length>ml){{ match=k;ml=k.length; }} }}
        if(match) {{ show(match, FARES[match].zone); }}
        else {{
            result.style.background='#fff3cd'; result.style.color='#856404';
            result.innerHTML='No fare data for "'+raw+'". Try SW1 or N1.';
        }}
        result.style.display='block';
    }}
    document.addEventListener('DOMContentLoaded',function(){{
        document.getElementById('pcode').addEventListener('keydown',function(e){{if(e.key==='Enter')lookupFare();}});
    }});
    </script>"""


def _lookup_card_section(rows=None) -> str:
    card_s = Style({
        "background": WHITE, "border-radius": "20px",
        "padding": "48px", "box-shadow": "0 8px 40px rgba(0,0,0,0.08)",
    })
    h2_s = Style({
        "font-size": "28px", "font-weight": "700", "color": NAVY, "margin-bottom": "8px",
    })
    sub_s = Style({
        "font-size": "15px", "color": GREY, "margin-bottom": "32px",
    })
    label_s = Style({
        "font-size": "14px", "font-weight": "600", "color": NAVY,
        "display": "block", "margin-bottom": "8px",
    })
    inp = Style({
        "flex": "1", "padding": "14px 20px", "border": "2px solid #e0e0e0",
        "border-radius": "12px", "font-size": "18px", "font-weight": "600",
        "outline": "none", "transition": "border-color 0.3s",
        ":focus": {"border-color": GOLD}, "text-transform": "uppercase",
    })
    btn = Style({
        "background": GOLD, "color": NAVY, "border": "none",
        "padding": "14px 28px", "border-radius": "12px",
        "font-size": "15px", "font-weight": "700", "cursor": "pointer",
        "white-space": "nowrap", "transition": "background 0.3s",
        ":hover": {"background": "#e89f2c"},
    })
    res = Style({
        "margin-top": "32px", "padding": "24px",
        "border-radius": "12px", "display": "none",
    })

    if rows is None:
        rows = _get_fares_data()

    return tags.div(class_=f"{card_s.class_name} lookup-card")(
        Raw(_fare_lookup_html(rows)),
        tags.h2(class_=h2_s.class_name)("Heathrow Fare Lookup"),
        tags.p(class_=sub_s.class_name)("Enter your postcode area to see fares to Heathrow."),
        tags.div(class_=label_s.class_name)("Postcode Area"),
        tags.div(class_="lookup-row", style={"display": "flex", "gap": "12px", "align-items": "center", "flex-wrap": "wrap"})(
            tags.input_(type="text", id="pcode", class_=inp.class_name,
                placeholder="e.g. SW1, N1, TW6", maxlength="4",
                style={"text-transform": "uppercase", "flex": "1", "min-width": "140px"}),
            tags.button(class_=btn.class_name, onclick="lookupFare()")("Check Fare"),
        ),
        tags.div(id="fresult", class_=res.class_name)(""),
    ).render()


def _fares_table_section(rows=None) -> str:
    h2_s = Style({
        "font-size": "28px", "font-weight": "700", "color": NAVY, "margin-bottom": "8px",
    })
    table_wrap = Style({
        "background": WHITE, "border-radius": "16px",
        "overflow-x": "auto", "box-shadow": "0 4px 24px rgba(0,0,0,0.06)",
    })
    table_s = Style({"width": "100%", "border-collapse": "collapse", "min-width": "300px"})
    th_s = Style({
        "background": NAVY, "color": WHITE, "padding": "12px 16px",
        "text-align": "left", "font-size": "13px", "font-weight": "600",
    })
    td_s = Style({
        "padding": "10px 16px", "border-bottom": "1px solid #e9ecef", "font-size": "13px",
    })
    td_alt = Style({
        "background": LIGHT, "padding": "10px 16px",
        "border-bottom": "1px solid #e9ecef", "font-size": "13px",
    })
    cost_s = Style({"font-weight": "700", "color": NAVY})

    if rows is None:
        rows = _get_fares_data()
    rows_html = ""
    for i, (prefix, cost, zone) in enumerate(rows):
        cls = td_s.class_name if i % 2 == 0 else td_alt.class_name
        rows_html += (
            f"<tr><td class='{cls}'><strong>{prefix}</strong></td>"
            f"<td class='{cls}'>{zone}</td>"
            f"<td class='{cls}'><span class='{cost_s.class_name}'>from \u00a3{cost:.0f}</span></td></tr>"
        )

    return tags.div(style={"margin-top": "48px"})(
        tags.h2(class_=h2_s.class_name)("All Heathrow Fares"),
        tags.div(class_=f"{table_wrap.class_name} fares-table-wrap")(
            tags.table(class_=table_s.class_name)(
                tags.thead()(tags.tr()(
                    tags.th(class_=th_s.class_name)("Area"),
                    tags.th(class_=th_s.class_name)("Zone"),
                    tags.th(class_=th_s.class_name)("Fares from"),
                )),
                tags.tbody()(Raw(rows_html)),
            ),
        ),
    ).render()


def _page_banner(title: str, sub: str) -> str:
    s = Style({
        "background": f"linear-gradient(135deg, {NAVY} 0%, #0f3460 100%)",
        "padding": "64px 24px",
        "text-align": "center",
    })
    h1_s = Style({
        "font-size": "36px", "font-weight": "800", "color": WHITE, "margin-bottom": "10px",
    })
    p_s = Style({
        "font-size": "16px", "color": "rgba(255,255,255,0.8)",
        "max-width": "560px", "margin": "0 auto",
    })
    return tags.section(class_=s.class_name)(
        tags.h1(class_=f"{h1_s.class_name} hero-anim")(title),
        tags.p(class_=f"{p_s.class_name} hero-anim-1")(sub),
    ).render()


class HeathrowPage(Component):
    def render(self) -> str:
        rows = _get_fares_data()
        section_s = Style({
            "padding": "60px 24px",
            "max-width": "800px",
            "margin": "0 auto",
        })
        body = (
            _page_banner("Heathrow Fares", "Fixed, upfront pricing to Heathrow Airport. Enter your postcode area for your fare from.") +
            tags.section(class_=section_s.class_name)(
                Raw(_lookup_card_section(rows)),
                Raw(_fares_table_section(rows)),
            ).render()
        )
        return page_wrapper("Heathrow", body)


class QuotePage(Component):
    def render(self) -> str:
        section_s = Style({
            "padding": "60px 24px",
            "max-width": "700px",
            "margin": "0 auto",
        })
        card_s = Style({
            "background": WHITE, "border-radius": "20px",
            "padding": "48px", "box-shadow": "0 8px 40px rgba(0,0,0,0.08)",
        })
        h2_s = Style({
            "font-size": "28px", "font-weight": "700", "color": NAVY, "margin-bottom": "8px",
        })
        sub_s = Style({
            "font-size": "15px", "color": GREY, "margin-bottom": "32px",
        })
        grid_s = Style({
            "display": "grid", "grid-template-columns": "1fr 1fr", "gap": "24px",
        })
        full_s = Style({"grid-column": "1 / -1"})
        label_s = Style({
            "display": "block", "font-size": "13px",
            "font-weight": "600", "color": NAVY, "margin-bottom": "8px",
        })
        field_s = Style({
            "width": "100%", "padding": "14px 16px",
            "border": "2px solid #e0e0e0", "border-radius": "10px",
            "font-size": "15px", "outline": "none",
            "transition": "border-color 0.3s",
            ":focus": {"border-color": GOLD},
        })
        ta_s = Style({
            "width": "100%", "padding": "14px 16px",
            "border": "2px solid #e0e0e0", "border-radius": "10px",
            "font-size": "15px", "outline": "none", "resize": "vertical",
            "min-height": "100px", "font-family": "inherit",
            ":focus": {"border-color": GOLD},
        })
        submit_s = Style({
            "background": GOLD, "color": NAVY, "border": "none",
            "padding": "16px 56px", "border-radius": "50px",
            "font-size": "16px", "font-weight": "700",
            "cursor": "pointer", "transition": "background 0.3s",
            ":hover": {"background": "#e89f2c"},
        })
        success_s = Style({
            "display": "none", "background": "#d4edda", "color": "#155724",
            "padding": "24px", "border-radius": "12px",
            "margin-top": "32px", "text-align": "center",
        })
        error_s = Style({
            "display": "none", "background": "#f8d7da", "color": "#721c24",
            "padding": "24px", "border-radius": "12px",
            "margin-top": "32px", "text-align": "center",
        })
        note_s = Style({
            "text-align": "center", "font-size": "13px",
            "color": GREY, "margin-top": "20px",
        })

        form = (
            _page_banner("Get a Quote", "Tell us about your journey and we'll confirm your fixed black cab fare.") +
            tags.section(class_=section_s.class_name)(
                Raw("""
                <script>
                async function submitQuote(e) {
                e.preventDefault();
                var f=document.getElementById('qf'),b=f.querySelector('button[type=submit]'),
                    s=document.getElementById('qs'),er=document.getElementById('qerr');
                b.disabled=true; b.textContent='Sending...';
                try {
                    var r=await fetch('https://formspree.io/f/mwvgrlde',{
                        method:'POST',headers:{'Content-Type':'application/json','Accept':'application/json'},
                        body:JSON.stringify({
                            name:document.getElementById('qn').value,email:document.getElementById('qemail').value,
                            phone:document.getElementById('qp').value,passengers:document.getElementById('qpa').value,
                            pickup:document.getElementById('qpu').value,destination:document.getElementById('qd').value,
                            date:document.getElementById('qdt').value,message:document.getElementById('qm').value
                        })
                    });
                    if(r.ok){s.style.display='block';er.style.display='none';f.reset();}
                    else{er.style.display='block';s.style.display='none';}
                }catch(e){er.style.display='block';s.style.display='none';}
                b.disabled=false; b.textContent='Request Quote';
                s.scrollIntoView({behavior:'smooth'});
            }
            </script>
            """),
            tags.div(class_=f"{card_s.class_name} quote-card")(
                tags.h2(class_=h2_s.class_name)("Get a Quote"),
                tags.p(class_=sub_s.class_name)("Fill in your details for a tailored quote."),
                tags.form(id="qf", onsubmit="submitQuote(event)")(
                    tags.div(class_=f"{grid_s.class_name} quote-grid")(
                        tags.div()(
                            tags.label(class_=label_s.class_name, for_="qn")("Full Name"),
                            tags.input_(type="text", id="qn", class_=field_s.class_name, placeholder="Your name", required="required"),
                        ),
                        tags.div()(
                            tags.label(class_=label_s.class_name, for_="qemail")("Email"),
                            tags.input_(type="email", id="qemail", class_=field_s.class_name, placeholder="your@email.com", required="required"),
                        ),
                        tags.div()(
                            tags.label(class_=label_s.class_name, for_="qp")("Phone"),
                            tags.input_(type="tel", id="qp", class_=field_s.class_name, placeholder="07700 900000"),
                        ),
                        tags.div()(
                            tags.label(class_=label_s.class_name, for_="qpa")("Passengers"),
                            tags.input_(type="number", id="qpa", class_=field_s.class_name, placeholder="2", min="1", max="8"),
                        ),
                        tags.div(class_=full_s.class_name)(
                            tags.label(class_=label_s.class_name, for_="qpu")("Pickup Postcode"),
                        )(
                            tags.input_(type="text", id="qpu", class_=field_s.class_name, placeholder="e.g. SW1A 1AA", required="required"),
                        ),
                        tags.div(class_=full_s.class_name)(
                            tags.label(class_=label_s.class_name, for_="qd")("Destination"),
                        )(
                            tags.input_(type="text", id="qd", class_=field_s.class_name, placeholder="e.g. Heathrow Airport, T5", value="Heathrow Airport"),
                        ),
                        tags.div(class_=full_s.class_name)(
                            tags.label(class_=label_s.class_name, for_="qdt")("Travel Date & Time"),
                        )(
                            tags.input_(type="datetime-local", id="qdt", class_=field_s.class_name),
                        ),
                        tags.div(class_=full_s.class_name)(
                            tags.label(class_=label_s.class_name, for_="qm")("Notes"),
                        )(
                            tags.textarea(id="qm", class_=ta_s.class_name, placeholder="Any special requirements..."),
                        ),
                    ),
                    tags.div(style={"text-align": "center", "margin-top": "36px"})(
                        tags.button(type="submit", class_=submit_s.class_name)("Request Quote"),
                    ),
                    tags.div(id="qs", class_=success_s.class_name)(
                        "Thank you! We'll be in touch shortly."
                    ),
                    tags.div(id="qerr", class_=error_s.class_name)(
                        'Something went wrong. Email us at <a href="mailto:support@fare-cab.co.uk" style="color:#721c24;font-weight:700;text-decoration:underline">support@fare-cab.co.uk</a>.'
                    ),
                    tags.p(class_=note_s.class_name)(
                        "Your data is kept secure. By submitting you agree to our privacy policy."
                    ),
                ),
            ),
        ).render()
        )

        return page_wrapper("Get a Quote", form)


class FeaturesSection(Component):
    def render(self) -> str:
        section_s = Style({
            "padding": "72px 24px",
            "max-width": "1100px",
            "margin": "0 auto",
        })
        h2_s = Style({
            "font-size": "32px", "font-weight": "800", "color": NAVY, "text-align": "center", "margin-bottom": "10px",
        })
        sub_s = Style({
            "font-size": "15px", "color": GREY, "text-align": "center", "max-width": "520px", "margin": "0 auto 8px",
        })
        card_s = Style({
            "background": WHITE, "border-radius": "16px", "padding": "28px 24px",
            "box-shadow": "0 4px 24px rgba(0,0,0,0.06)",
        })
        icon_s = Style({
            "width": "44px", "height": "44px", "border-radius": "12px",
            "background": "#fdf1dc", "display": "flex", "align-items": "center", "justify-content": "center",
            "margin-bottom": "16px",
        })
        h3_s = Style({
            "font-size": "17px", "font-weight": "700", "color": NAVY, "margin-bottom": "8px",
        })
        p_s = Style({
            "font-size": "14px", "color": GREY, "line-height": "1.6",
        })

        def card(icon, title, text):
            return tags.div(class_=f"feature-card {card_s.class_name}")(
                tags.div(class_=icon_s.class_name)(Raw(icon)),
                tags.h3(class_=h3_s.class_name)(title),
                tags.p(class_=p_s.class_name)(text),
            ).render()

        cards = "".join([
            card(
                '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#e89f2c" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 1v22M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>',
                "Fixed Fares",
                "The price you see is the price you pay. No meter, no hidden extras, no surge.",
            ),
            card(
                '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#e89f2c" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>',
                "Licensed & Insured",
                "Fully licensed black cab drivers with professional service and complete peace of mind.",
            ),
            card(
                '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#e89f2c" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/></svg>',
                "Meet & Greet",
                "We track your flight and meet you at arrivals, ready to help with your bags.",
            ),
            card(
                '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#e89f2c" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
                "24/7 Availability",
                "Day or night, weekends and bank holidays — we're always on the road.",
            ),
        ])

        return tags.section(class_=section_s.class_name)(
            tags.h2(class_=h2_s.class_name)("Why ride with Fare-Cab?"),
            tags.p(class_=sub_s.class_name)("The honest way to get to Heathrow — by the people who know London best."),
            tags.div(class_="features-grid")(Raw(cards)),
        ).render()


class HowItWorksSection(Component):
    def render(self) -> str:
        section_s = Style({
            "padding": "56px 24px 88px",
            "max-width": "1100px",
            "margin": "0 auto",
        })
        h2_s = Style({
            "font-size": "32px", "font-weight": "800", "color": NAVY, "text-align": "center", "margin-bottom": "10px",
        })
        sub_s = Style({
            "font-size": "15px", "color": GREY, "text-align": "center", "max-width": "520px", "margin": "0 auto 8px",
        })
        card_s = Style({
            "background": WHITE, "border-radius": "16px", "padding": "28px 24px",
            "box-shadow": "0 4px 24px rgba(0,0,0,0.06)",
        })
        h3_s = Style({
            "font-size": "17px", "font-weight": "700", "color": NAVY, "margin-bottom": "8px",
        })
        p_s = Style({
            "font-size": "14px", "color": GREY, "line-height": "1.6",
        })

        steps = [
            ("1", "Enter your postcode", "Type your postcode area — SW1, N1, TW6 — into the lookup box."),
            ("2", "See your fare instantly", "Get a fixed price in seconds, before you even pick up the phone."),
            ("3", "Book your black cab", "Send a quote request and a licensed driver will confirm right away."),
        ]

        cards = "".join([
            tags.div(class_=card_s.class_name)(
                tags.div(class_="step-num")(num),
                tags.h3(class_=h3_s.class_name)(title),
                tags.p(class_=p_s.class_name)(text),
            ).render()
            for num, title, text in steps
        ])

        return tags.section(class_=section_s.class_name)(
            tags.h2(class_=h2_s.class_name)("How it works"),
            tags.p(class_=sub_s.class_name)("Getting to Heathrow has never been simpler."),
            tags.div(class_="steps-grid")(Raw(cards)),
        ).render()


class HomePage(Component):
    def render(self) -> str:
        section_s = Style({
            "padding": "60px 24px",
            "max-width": "800px",
            "margin": "0 auto",
        })
        body = tags.section(class_=section_s.class_name)(
            Raw(_lookup_card_section()),
        ).render()
        return page_wrapper("Home",
            HeroSection().render() + FeaturesSection().render() + HowItWorksSection().render() + body
        )


def build_page(filename: str, title: str, root: Component):
    app = App(root=root, title=title)
    app.doc.add_head_link('<link rel="icon" type="image/png" href="favicon-48.png" sizes="48x48">')
    app.doc.add_head_link('<link rel="icon" type="image/png" href="favicon-96.png" sizes="96x96">')
    app.doc.add_head_link('<link rel="icon" type="image/x-icon" href="favicon.ico" sizes="48x48">')
    app.doc.add_style(global_styles())
    output_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(output_dir, filename)
    with open(path, "w") as f:
        f.write(app.render())
    print(f"Built {path}")


if __name__ == "__main__":
    build_page("index.html", "Fare-Cab | London Black Cab Fares", HomePage())
    build_page("heathrow.html", "Heathrow Fares | Fare-Cab", HeathrowPage())
    build_page("quote.html", "Get a Quote | Fare-Cab", QuotePage())
