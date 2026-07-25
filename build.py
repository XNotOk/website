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
@media (max-width: 768px) {{
.nav-links {{ display: none; flex-direction: column; position: absolute; top: 64px; left: 0; right: 0; background: {NAVY}; padding: 20px; gap: 20px; z-index: 1000; }}
.nav-links.open {{ display: flex; }}
.nav-toggle {{ display: block; }}
.nav-toggle span {{ display: block; width: 24px; height: 3px; background: {WHITE}; margin: 5px 0; border-radius: 2px; transition: all .3s; }}
.hero-title {{ font-size: 28px !important; }}
.hero-sub {{ font-size: 15px !important; }}
.lookup-card {{ padding: 28px 20px !important; }}
.lookup-row {{ flex-direction: column !important; }}
.quote-card {{ padding: 28px 20px !important; }}
.quote-grid {{ grid-template-columns: 1fr !important; }}
.fares-table-wrap {{ overflow-x: auto !important; }}
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
        tags.p(class_=p_s.class_name)("Copyright 2026 Fare-Cab. All rights reserved."),
    ).render()


class HeroSection(Component):
    def render(self) -> str:
        s = Style({
            "background": f"linear-gradient(135deg, {NAVY} 0%, #0f3460 100%)",
            "padding": "80px 24px",
            "text-align": "center",
        })
        h1_s = Style({
            "font-size": "40px",
            "font-weight": "800",
            "color": WHITE,
            "max-width": "600px",
            "margin": "0 auto 16px",
            "line-height": "1.2",
        })
        p_s = Style({
            "font-size": "18px",
            "color": "rgba(255,255,255,0.8)",
            "max-width": "500px",
            "margin": "0 auto 32px",
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
            "transition": "background 0.3s",
            ":hover": {"background": "#e89f2c"},
        })
        return tags.section(class_=s.class_name)(
            tags.h1(class_=f"{h1_s.class_name} hero-title", style={"font-size": "40px"})("London Black Cab Fares"),
            tags.p(class_=f"{p_s.class_name} hero-sub")(
                "Know your fare before you ride. Instant Heathrow airport transfer pricing."
            ),
            tags.a(href="heathrow.html", class_=btn.class_name)("Check Heathrow Fare"),
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
        const exact = FARES[raw];
        if (exact) {{
            result.style.background = '#d4edda'; result.style.color = '#155724';
            result.innerHTML = '<div style="font-size:14px">Fare from <strong>'+raw+'</strong> ('+exact.zone+') to Heathrow:</div>' +
                '<div style="font-size:36px;font-weight:800;color:#1a1a2e">\u00a3'+exact.cost.toFixed(2)+'</div>';
            result.style.display = 'block'; return;
        }}
        let match=null, ml=0;
        for(const k of Object.keys(FARES)) {{ if(raw.startsWith(k)&&k.length>ml){{ match=k;ml=k.length; }} }}
        if(match) {{
            const f=FARES[match];
            result.style.background='#d4edda'; result.style.color='#155724';
            result.innerHTML='<div style="font-size:14px">Fare from <strong>'+match+'</strong> ('+f.zone+') to Heathrow:</div>'+
                '<div style="font-size:36px;font-weight:800;color:#1a1a2e">\u00a3'+f.cost.toFixed(2)+'</div>';
        }} else {{
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
        tags.p(class_=sub_s.class_name)("Enter your postcode area for the fixed fare to Heathrow."),
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
            f"<td class='{cls}'><span class='{cost_s.class_name}'>\u00a3{cost:.2f}</span></td></tr>"
        )

    return tags.div(style={"margin-top": "48px"})(
        tags.h2(class_=h2_s.class_name)("All Heathrow Fares"),
        tags.div(class_=f"{table_wrap.class_name} fares-table-wrap")(
            tags.table(class_=table_s.class_name)(
                tags.thead()(tags.tr()(
                    tags.th(class_=th_s.class_name)("Area"),
                    tags.th(class_=th_s.class_name)("Zone"),
                    tags.th(class_=th_s.class_name)("Fare"),
                )),
                tags.tbody()(Raw(rows_html)),
            ),
        ),
    ).render()


class HeathrowPage(Component):
    def render(self) -> str:
        rows = _get_fares_data()
        section_s = Style({
            "padding": "60px 24px",
            "max-width": "800px",
            "margin": "0 auto",
        })
        body = tags.section(class_=section_s.class_name)(
            Raw(_lookup_card_section(rows)),
            Raw(_fares_table_section(rows)),
        ).render()
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

        form = tags.section(class_=section_s.class_name)(
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
                        "Something went wrong. Try again or email us."
                    ),
                    tags.p(class_=note_s.class_name)(
                        "Your data is kept secure. By submitting you agree to our privacy policy."
                    ),
                ),
            ),
        ).render()

        return page_wrapper("Get a Quote", form)


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
            HeroSection().render() + body
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
