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
            "scroll-behavior": "smooth",
        },
    })


class Header(Component):
    def render(self) -> str:
        s = Style({
            "background": NAVY,
            "padding": "12px 40px",
            "display": "flex",
            "align-items": "center",
            "justify-content": "space-between",
        })
        logo_wrap = Style({
            "background": WHITE,
            "border-radius": "8px",
            "padding": "4px 8px",
            "display": "inline-flex",
            "align-items": "center",
        })
        logo_s = Style({
            "height": "40px",
            "width": "auto",
            "display": "block",
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
            tags.a(href="#home", class_=logo_wrap.class_name)(
                tags.img(src="logo.png", alt="Fare-Cab", class_=logo_s.class_name),
            ),
            tags.div(class_=nav_s.class_name)(
                tags.a(href="#home", class_=link.class_name)("Home"),
                tags.a(href="#heathrow", class_=link.class_name)("Heathrow"),
                tags.a(href="#fares", class_=link.class_name)("All Fares"),
                tags.a(href="#quote", class_=btn.class_name)("Get a Quote"),
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
        return tags.section(id="home", class_=s.class_name)(
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

        from fares_db import get_conn
        with get_conn() as conn:
            rows = conn.execute(
                "SELECT postcode_prefix, cost, zone FROM fares ORDER BY postcode_prefix"
            ).fetchall()
        fares_json = []
        for prefix, cost, zone in rows:
            fares_json.append(f'"{prefix}":{{"cost":{cost},"zone":"{zone}"}}')
        fares_js_obj = "{" + ",".join(fares_json) + "}"

        lookup_js = f"""
        <script>
        const FARES = {fares_js_obj};

        function lookupFare() {{
            const input = document.getElementById('postcode-input');
            const result = document.getElementById('fare-result');
            const raw = input.value.trim().toUpperCase();

            if (!raw) {{
                result.style.display = 'block';
                result.style.background = '#fff3cd';
                result.style.color = '#856404';
                result.innerHTML = 'Please enter a postcode area (e.g. SW1, N1, TW6)';
                return;
            }}

            const exact = FARES[raw];
            if (exact) {{
                result.style.background = '#d4edda';
                result.style.color = '#155724';
                result.innerHTML = '<div style="font-size:14px;margin-bottom:4px">Fare from <strong>' + raw + '</strong> (' + exact.zone + ') to Heathrow:</div>' +
                    '<div style="font-size:36px;font-weight:800;color:#1a1a2e">&pound;' + exact.cost.toFixed(2) + '</div>';
                result.style.display = 'block';
                return;
            }}

            let match = null;
            let matchLen = 0;
            for (const key of Object.keys(FARES)) {{
                if (raw.startsWith(key) && key.length > matchLen) {{
                    match = key;
                    matchLen = key.length;
                }}
            }}
            if (match) {{
                const f = FARES[match];
                result.style.background = '#d4edda';
                result.style.color = '#155724';
                result.innerHTML = '<div style="font-size:14px;margin-bottom:4px">Fare from <strong>' + match + '</strong> (' + f.zone + ') to Heathrow:</div>' +
                    '<div style="font-size:36px;font-weight:800;color:#1a1a2e">&pound;' + f.cost.toFixed(2) + '</div>';
            }} else {{
                result.style.background = '#fff3cd';
                result.style.color = '#856404';
                result.innerHTML = 'No fare data for "' + raw + '". Try a shorter prefix like SW1 or N1.';
            }}
            result.style.display = 'block';
        }}

        document.addEventListener('DOMContentLoaded', function() {{
            document.getElementById('postcode-input').addEventListener('keydown', function(e) {{
                if (e.key === 'Enter') lookupFare();
            }});
        }});
        </script>
        """

        return tags.section(id="heathrow", class_=section_s.class_name)(
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

        return tags.section(id="fares", class_=section_s.class_name)(
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


class QuoteSection(Component):
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
            "margin-bottom": "36px",
        })
        grid_s = Style({
            "display": "grid",
            "grid-template-columns": "1fr 1fr",
            "gap": "20px",
        })
        full_s = Style({
            "grid-column": "1 / -1",
        })
        label_s = Style({
            "display": "block",
            "font-size": "13px",
            "font-weight": "600",
            "color": NAVY,
            "margin-bottom": "6px",
        })
        field_s = Style({
            "width": "100%",
            "padding": "12px 16px",
            "border": "2px solid #e0e0e0",
            "border-radius": "10px",
            "font-size": "15px",
            "outline": "none",
            "transition": "border-color 0.3s",
            ":focus": {"border-color": GOLD},
        })
        textarea_s = Style({
            "width": "100%",
            "padding": "12px 16px",
            "border": "2px solid #e0e0e0",
            "border-radius": "10px",
            "font-size": "15px",
            "outline": "none",
            "transition": "border-color 0.3s",
            "resize": "vertical",
            "min-height": "100px",
            "font-family": "inherit",
            ":focus": {"border-color": GOLD},
        })
        submit_s = Style({
            "background": GOLD,
            "color": NAVY,
            "border": "none",
            "padding": "14px 48px",
            "border-radius": "50px",
            "font-size": "16px",
            "font-weight": "700",
            "cursor": "pointer",
            "transition": "background 0.3s",
            ":hover": {"background": "#e89f2c"},
        })
        success_s = Style({
            "display": "none",
            "background": "#d4edda",
            "color": "#155724",
            "padding": "24px",
            "border-radius": "12px",
            "margin-top": "24px",
            "text-align": "center",
            "font-size": "16px",
            "font-weight": "500",
        })
        note_s = Style({
            "text-align": "center",
            "font-size": "13px",
            "color": GREY,
            "margin-top": "20px",
        })

        quote_js = """
        <script>
        async function submitQuote(event) {
            event.preventDefault();
            const form = document.getElementById('quote-form');
            const btn = form.querySelector('button[type="submit"]');
            const success = document.getElementById('quote-success');
            const error = document.getElementById('quote-error');

            btn.disabled = true;
            btn.textContent = 'Sending...';

            const data = {
                name: document.getElementById('quote-name').value,
                email: document.getElementById('quote-email').value,
                phone: document.getElementById('quote-phone').value,
                passengers: document.getElementById('quote-passengers').value,
                pickup: document.getElementById('quote-pickup').value,
                destination: document.getElementById('quote-destination').value,
                date: document.getElementById('quote-date').value,
                message: document.getElementById('quote-message').value,
            };

            try {
                const res = await fetch('https://formspree.io/f/mwvgrlde', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json', 'Accept': 'application/json'},
                    body: JSON.stringify(data),
                });
                if (res.ok) {
                    success.style.display = 'block';
                    error.style.display = 'none';
                    form.reset();
                } else {
                    error.style.display = 'block';
                    success.style.display = 'none';
                }
            } catch (e) {
                error.style.display = 'block';
                success.style.display = 'none';
            }
            btn.disabled = false;
            btn.textContent = 'Request Quote';
            success.scrollIntoView({ behavior: 'smooth' });
        }
        </script>
        """

        return tags.section(id="quote", class_=section_s.class_name)(
            Raw(quote_js),
            tags.div(class_=card_s.class_name)(
                tags.h2(class_=h2_s.class_name)("Get a Quote"),
                tags.p(class_=sub_s.class_name)(
                    "Fill in your details and we'll get back to you with a tailored quote."
                ),
                tags.form(id="quote-form", onsubmit="submitQuote(event)")(
                    tags.div(class_=grid_s.class_name)(
                        tags.div()(
                            tags.label(class_=label_s.class_name, for_="quote-name")("Full Name"),
                            tags.input_(type="text", id="quote-name", class_=field_s.class_name, placeholder="Your name", required="required"),
                        ),
                        tags.div()(
                            tags.label(class_=label_s.class_name, for_="quote-email")("Email"),
                            tags.input_(type="email", id="quote-email", class_=field_s.class_name, placeholder="your@email.com", required="required"),
                        ),
                        tags.div()(
                            tags.label(class_=label_s.class_name, for_="quote-phone")("Phone"),
                            tags.input_(type="tel", id="quote-phone", class_=field_s.class_name, placeholder="07700 900000"),
                        ),
                        tags.div()(
                            tags.label(class_=label_s.class_name, for_="quote-passengers")("Passengers"),
                            tags.input_(type="number", id="quote-passengers", class_=field_s.class_name, placeholder="2", min="1", max="8"),
                        ),
                        tags.div(class_=full_s.class_name)(
                            tags.label(class_=label_s.class_name, for_="quote-pickup")("Pickup Postcode"),
                        )(
                            tags.input_(type="text", id="quote-pickup", class_=field_s.class_name, placeholder="e.g. SW1A 1AA", required="required"),
                        ),
                        tags.div(class_=full_s.class_name)(
                            tags.label(class_=label_s.class_name, for_="quote-destination")("Destination"),
                        )(
                            tags.input_(type="text", id="quote-destination", class_=field_s.class_name, placeholder="e.g. Heathrow Airport, Terminal 5", value="Heathrow Airport"),
                        ),
                        tags.div(class_=full_s.class_name)(
                            tags.label(class_=label_s.class_name, for_="quote-date")("Travel Date & Time"),
                        )(
                            tags.input_(type="datetime-local", id="quote-date", class_=field_s.class_name),
                        ),
                        tags.div(class_=full_s.class_name)(
                            tags.label(class_=label_s.class_name, for_="quote-message")("Additional Notes"),
                        )(
                            tags.textarea(id="quote-message", class_=textarea_s.class_name, placeholder="Any special requirements..."),
                        ),
                    ),
                    tags.div(style={"text-align": "center", "margin-top": "28px"})(
                        tags.button(type="submit", class_=submit_s.class_name)("Request Quote"),
                    ),
                    tags.div(id="quote-success", class_=success_s.class_name)(
                        "Thank you! Your quote request has been received. We'll be in touch shortly."
                    ),
                    tags.div(id="quote-error", class_=Style({
                        "display": "none",
                        "background": "#f8d7da",
                        "color": "#721c24",
                        "padding": "24px",
                        "border-radius": "12px",
                        "margin-top": "24px",
                        "text-align": "center",
                        "font-size": "16px",
                        "font-weight": "500",
                    }).class_name)(
                        "Something went wrong. Please try again or email us directly."
                    ),
                    tags.p(class_=note_s.class_name)(
                        "By submitting you agree to our privacy policy. Your data is kept secure."
                    ),
                ),
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
        logo_wrap_f = Style({
            "background": WHITE,
            "border-radius": "6px",
            "padding": "3px 6px",
            "display": "inline-flex",
            "align-items": "center",
            "margin-bottom": "8px",
        })
        logo_s = Style({
            "height": "28px",
            "width": "auto",
            "display": "block",
        })
        p_s = Style({
            "font-size": "13px",
            "color": "rgba(255,255,255,0.5)",
        })
        return tags.footer(class_=s.class_name)(
            tags.img(src="logo.png", alt="Fare-Cab", class_=logo_s.class_name),
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
                QuoteSection(),
                Footer(),
            ]
        )


if __name__ == "__main__":
    app = App(root=FareCabPage(), title="Fare-Cab | London Black Cab Fares")
    app.doc.add_head_link('<link rel="icon" type="image/png" href="favicon-48.png" sizes="48x48">')
    app.doc.add_head_link('<link rel="icon" type="image/png" href="favicon-96.png" sizes="96x96">')
    app.doc.add_head_link('<link rel="icon" type="image/x-icon" href="favicon.ico" sizes="48x48">')
    app.doc.add_style(global_styles())
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(output_dir, "index.html")
    with open(output_path, "w") as f:
        f.write(app.render())
    print(f"Built {output_path}")
