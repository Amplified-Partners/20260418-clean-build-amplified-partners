"""Vellum Brief — mobile-first HTML renderer.

Renders a Brief sheet into a self-contained HTML page optimised for
iPhone Safari / iMessage preview.  Critical CSS is inlined; no external
fonts or frameworks.  Target: TTI < 1 s on 4G.

Signed-by: Devon-a947 | 2026-05-11
"""

from __future__ import annotations

from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

_TEMPLATE_DIR = Path(__file__).parent / "templates"
_STATIC_DIR = Path(__file__).parent / "static"

_env = Environment(
    loader=FileSystemLoader(str(_TEMPLATE_DIR)),
    autoescape=select_autoescape(["html"]),
)


def _load_critical_css() -> str:
    """Read brief.css and return it for inline injection."""
    css_path = _STATIC_DIR / "brief.css"
    return css_path.read_text(encoding="utf-8")


def render_brief(sheet_data: dict, token: str) -> str:
    """Render the Brief HTML for a given sheet.

    Parameters
    ----------
    sheet_data : dict
        Must contain at minimum::

            {
                "sheet_id": str,
                "title": str,
                "date": str,          # human-readable, e.g. "Mon 12 May"
                "headline": str,      # 2-3 sentence summary
                "sections": [         # expandable detail cards
                    {
                        "icon": str,      # single emoji
                        "title": str,
                        "summary": str,   # one-liner
                        "details": str,   # longer body (may contain HTML)
                    },
                    ...
                ],
            }

    token : str
        Share token for authenticated replies.

    Returns
    -------
    str
        Fully self-contained HTML page.
    """
    template = _env.get_template("brief.html")
    critical_css = _load_critical_css()
    return template.render(
        sheet=sheet_data,
        token=token,
        critical_css=critical_css,
    )
