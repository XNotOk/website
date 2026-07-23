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
    return dict_to_css({
        "*": {"margin": "0", "padding": "0", "box-sizing": "border-box"},
        "body": {
            "font-family": "'Segoe UI', system-ui, -apple-system, sans-serif",
            "color": "#2d2d2d",
            "line-height": "1.6",
            "background": LIGHT,
        },
    })


class Header(Component):
    def render(self) -> str:
        s = Style({
            "background": NAVY,
            "padding": "16px 40px",
            "display": "flex",
            "align-items": "center",
            "justify-content": "space-between",
        })
        logo_s = Style({
            "font-size": "24px",
            "font-weight": "800",
            "color": GOLD,
            "letter-spacing": "-0.5px",
        })
        nav_s = Style({
            "display": "flex",
            "gap": "20px",
            "align-items": "center",
        })
        link = Style({
            "color": WHITE,
            "font-size": "14px",
            "font-weight": "500",
            "transition": "color 0.3s",
            ":hover": {"color": GOLD},
        })
        btn = Style({
            "background": GOLD,
            "color": NAVY,
            "padding": "10px 24px",
            "border-radius": "50px",
            "font-size": "14px",
            "font-weight": "700",
            "transition": "background 0.3s",
            ":hover": {"background": "#e89f2c"},
        })
        return tags.nav(class_=s.class_name)(
            tags.div(class_=logo_s.class_name)("Fare-Cab"),
            tags.div(class_=nav_s.class_name)(
                tags.a(href="#", class_=link.class_name)("Home"),
                tags.a(href="#heathrow", class_=link.class_name)("Heathrow"),
                tags.a(href="#", class_=link.class_name)("All Fares"),
                tags.a(href="#", class_=btn.class_name)("Get a Quote"),
            ),
        ).render()


class Hero(Component):
    def render(self) -> str:
        s = Style({
            "background": f"linear-gradient(135deg, {NAVY} 0%, #0f3460 100%)",
            "padding": "80px 40px",
            "text-align": "center",
        })
        h1_s = Style({
            "font-size": "40px",
            "font-weight": "800",
            "color": WHITE,
            "max-width": "650px",
            "margin": "0 auto 16px",
            "line-height": "1.2",
        })
        p_s = Style({
            "font-size": "18px",
            "color": "rgba(255,255,255,0.8)",
            "max-width": "550px",
            "margin": "0 auto 32px",
        })
        return tags.section(class_=s.class_name)(
            tags.h1(class_=h1_s.class_name)("London Black Cab Fares"),
            tags.p(class_=p_s.class_name)(
                "Know your fare before you ride. Instant Heathrow airport transfer pricing."
            ),
        ).render()


class FareLookup(Component):
    def render(self) -> str:
        section_s = Style({
            "padding": "80px 40px",
            "max-width": "800px",
            "margin": "0 auto",
        })
        card_s = Style({
            "background": WHITE,
            "border-radius": "20px",
            "padding": "48px",
            "box-shadow": "0 8px 40px rgba(0,0,0,0.08)",
        })
        h2_s = Style({
            "font-size": "28px",
            "font-weight": "700",
            "color": NAVY,
            "margin-bottom": "8px",
        })
        sub_s = Style({
            "font-size": "15px",
            "color": GREY,
            "margin-bottom": "32px",
        })
        label_s = Style({
            "font-size": "14px",
            "font-weight": "600",
            "color": NAVY,
            "display": "block",
            "margin-bottom": "8px",
        })
        row_s = Style({
            "display": "flex",
            "gap": "12px",
            "align-items": "center",
        })
        inp = Style({
            "flex": "1",
            "padding": "14px 20px",
            "border": "2px solid #e0e0e0",
            "border-radius": "12px",
            "font-size": "18px",
            "font-weight": "600",
            "outline": "none",
            "transition": "border-color 0.3s",
            ":focus": {"border-color": GOLD},
            "text-transform": "uppercase",
        })

        btn = Style({
            "background": GOLD,
            "color": NAVY,
            "border": "none",
            "padding": "14px 32px",
            "border-radius": "12px",
            "font-size": "16px",
            "font-weight": "700",
            "cursor": "pointer",
            "white-space": "nowrap",
            "transition": "background 0.3s",
            ":hover": {"background": "#e89f2c"},
        })

        res = Style({
            "margin-top": "32px",
            "padding": "24px",
            "border-radius": "12px",
            "display": "none",
        })

        fls = Style({
            "margin-top": "40px",
            "padding": "24px",
            "background": LIGHT,
            "border-radius": "12px",
            "text-align": "center",
        })

        lookup_js = """
        <script>
        async function lookupFare() {
            const input = document.getElementById('postcode-input');
            const result = document.getElementById('fare-result');
            const prefix = input.value.trim().toUpperCase();

            if (!prefix) {
                result.style.display = 'block';
                result.style.background = '#fff3cd';
                result.style.color = '#856404';
                result.innerHTML = 'Please enter a postcode area (e.g. SW1, N1, TW6)';
                return;
            }

            result.innerHTML = '<div style="text-align:center;padding:12px">Looking up fare...</div>';
            result.style.display = 'block';
            result.style.background = '#f8f9fa';
            result.style.color = '#2d2d2d';

            try {
                const response = await fetch('/api/rpc', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        func: 'get_fare',
                        args: [prefix],
                        kwargs: {}
                    })
                });
                const data = await response.json();

                if (data.error) {
                    result.style.background = '#fff3cd';
                    result.style.color = '#856404';
                    result.innerHTML = '<strong>Not found:</strong> No fare data for "' + prefix + '". Try a shorter prefix like SW1 or N1.';
                    return;
                }

                const fare = data.result;
                result.style.background = '#d4edda';
                result.style.color = '#155724';
                result.innerHTML = '<div style="font-size:14px;margin-bottom:4px">Fare from <strong>' + fare.prefix + '</strong> (' + fare.zone + ') to Heathrow:</div>' +
                    '<div style="font-size:36px;font-weight:800;color:#1a1a2e">&pound;' + fare.cost.toFixed(2) + '</div>';
            } catch (e) {
                result.style.background = '#f8d7da';
                result.style.color = '#721c24';
                result.innerHTML = 'Error looking up fare. Is the server running?';
            }
        }

        document.addEventListener('DOMContentLoaded', function() {
            document.getElementById('postcode-input').addEventListener('keydown', function(e) {
                if (e.key === 'Enter') lookupFare();
            });
        });
        </script>
        """

        return tags.section(class_=section_s.class_name)(
            Raw(lookup_js),
            tags.div(class_=card_s.class_name)(
                tags.h2(class_=h2_s.class_name)("Heathrow Fare Lookup"),
                tags.p(class_=sub_s.class_name)(
                    "Enter your postcode area to see the fixed fare to Heathrow Airport."
                ),
                tags.div(class_=label_s.class_name)("Postcode Area"),
                tags.div(class_=row_s.class_name)(
                    tags.input_(
                        type="text",
                        id="postcode-input",
                        class_=inp.class_name,
                        placeholder="e.g. SW1, N1, TW6",
                        maxlength="4",
                        style={"text-transform": "uppercase"},
                    ),
                    tags.button(class_=btn.class_name, onclick="lookupFare()")("Check Fare"),
                ),
                tags.div(id="fare-result", class_=res.class_name)(""),
            ),
        ).render()


class AllFaresSection(Component):
    def render(self) -> str:
        section_s = Style({
            "padding": "60px 40px 80px",
            "max-width": "800px",
            "margin": "0 auto",
        })
        h2_s = Style({
            "font-size": "28px",
            "font-weight": "700",
            "color": NAVY,
            "text-align": "center",
            "margin-bottom": "32px",
        })
        table_wrap = Style({
            "background": WHITE,
            "border-radius": "16px",
            "overflow": "hidden",
            "box-shadow": "0 4px 24px rgba(0,0,0,0.06)",
        })
        table_s = Style({
            "width": "100%",
            "border-collapse": "collapse",
        })
        th_s = Style({
            "background": NAVY,
            "color": WHITE,
            "padding": "14px 20px",
            "text-align": "left",
            "font-size": "14px",
            "font-weight": "600",
        })
        td_s = Style({
            "padding": "12px 20px",
            "border-bottom": "1px solid #e9ecef",
            "font-size": "14px",
        })
        td_alt = Style({
            "background": LIGHT,
            "padding": "12px 20px",
            "border-bottom": "1px solid #e9ecef",
            "font-size": "14px",
        })
        cost_s = Style({
            "font-weight": "700",
            "color": NAVY,
        })

        from fares_db import get_conn
        with get_conn() as conn:
            rows = conn.execute(
                "SELECT postcode_prefix, cost, zone FROM fares ORDER BY postcode_prefix"
            ).fetchall()

        rows_html = ""
        for i, (prefix, cost, zone) in enumerate(rows):
            cls = td_s.class_name if i % 2 == 0 else td_alt.class_name
            rows_html += (
                f"<tr>"
                f"<td class='{cls}'><strong>{prefix}</strong></td>"
                f"<td class='{cls}'>{zone}</td>"
                f"<td class='{cls}'><span class='{cost_s.class_name}'>£{cost:.2f}</span></td>"
                f"</tr>"
            )

        return tags.section(class_=section_s.class_name)(
            tags.h2(class_=h2_s.class_name)("All Heathrow Fares"),
            tags.div(class_=table_wrap.class_name)(
                tags.table(class_=table_s.class_name)(
                    tags.thead()(
                        tags.tr()(
                            tags.th(class_=th_s.class_name)("Area"),
                            tags.th(class_=th_s.class_name)("Zone"),
                            tags.th(class_=th_s.class_name)("Fare"),
                        )
                    ),
                    tags.tbody()(Raw(rows_html)),
                )
            ),
        ).render()


class Footer(Component):
    def render(self) -> str:
        s = Style({
            "background": NAVY,
            "color": WHITE,
            "padding": "40px 40px 24px",
            "text-align": "center",
        })
        logo_s = Style({
            "font-size": "20px",
            "font-weight": "800",
            "color": GOLD,
            "margin-bottom": "8px",
        })
        p_s = Style({
            "font-size": "13px",
            "color": "rgba(255,255,255,0.5)",
        })
        return tags.footer(class_=s.class_name)(
            tags.div(class_=logo_s.class_name)("Fare-Cab"),
            tags.p(class_=p_s.class_name)("Copyright 2026 Fare-Cab. All rights reserved."),
        ).render()


class FareCabPage(Component):
    def render(self) -> str:
        return "".join(
            c.render() for c in [
                Header(),
                Hero(),
                FareLookup(),
                AllFaresSection(),
                Footer(),
            ]
        )


if __name__ == "__main__":
    app = App(root=FareCabPage(), title="Fare-Cab | London Black Cab Fares")
    app.doc.add_style(global_styles())
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(output_dir, "index.html")
    with open(output_path, "w") as f:
        f.write(app.render())
    print(f"Built {output_path}")
