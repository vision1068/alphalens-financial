"""Email alerts for new Strong Buy / Strong Sell signals, held shares turning Sell, and dividends worth a look.

An alert is sent once when a company enters the state, not every day it stays there. The record of what
has been alerted is saved only after the email is sent, so a failed send is retried on the next run.
"""
from __future__ import annotations

import html
import os
import smtplib
from email.message import EmailMessage

LABEL = {"STRONG_BUY": "Strong Buy", "BUY": "Buy", "HOLD": "Hold", "SELL": "Sell", "STRONG_SELL": "Strong Sell"}
FACTOR = {"revenue_growth": "Revenue growth", "earnings_growth": "Earnings growth", "profitability": "Profitability",
          "cash_flow_quality": "Cash flow quality", "cash_conversion_cycle": "Cash conversion cycle", "debt": "Debt",
          "liquidity": "Liquidity", "valuation": "Valuation", "dividend": "Dividend", "price_trend": "Price trend"}
DISCLAIMER = "Decision support only, not financial advice. BetaLens never places trades. Check before acting."


def top_reasons(card: dict, n: int = 3) -> list[str]:
    """The factors that moved the score furthest from neutral, with their first stated reason."""
    scored = [f for f in card["factors"] if f["score"] is not None and f["reasons"]]
    scored.sort(key=lambda f: -abs(f["score"] - 50) * f["weight"])
    return [f"{FACTOR.get(f['name'], f['name'])} {f['score']:.0f}/100: {f['reasons'][0]}" for f in scored[:n]]


def find_alerts(cards: list[dict], upcoming: list[dict], state: dict, cfg: dict, holdings: set[str]) -> tuple[list[dict], dict]:
    """Return (alerts to send now, the state to save once they are sent)."""
    alerts, new_state = [], {}
    for card in cards:
        symbol, signal = card["symbol"], card["signal"]
        new_state[symbol] = signal
        if state.get(symbol) == signal:
            continue
        if signal in cfg["alert_signals"]:
            alerts.append({"kind": "signal", "card": card})
        elif symbol in holdings and signal in cfg["holding_alert_signals"]:
            alerts.append({"kind": "holding", "card": card})
    for u in upcoming:
        if u["verdict"] != "WORTH_A_LOOK":
            continue
        key = f"DIV:{u['symbol']}:{u['book_closure_from']}"
        new_state[key] = "sent"
        if key not in state:
            alerts.append({"kind": "dividend", "dividend": u})
    return alerts, new_state


def compose(alerts: list[dict], notes: dict, dashboard_url: str) -> tuple[str, str, str]:
    """Return (subject, plain text, HTML)."""
    counts: dict[str, int] = {}
    blocks_text, blocks_html = [], []
    for a in alerts:
        if a["kind"] == "dividend":
            u = a["dividend"]
            counts["dividend worth a look"] = counts.get("dividend worth a look", 0) + 1
            title = f"{u['symbol']}: dividend Rs {u['amount_per_share']:.2f} per share ({u['yield_pct']}% yield), worth a look"
            lines = [f"Last day to buy: {u['last_buy_date']}; ex-dividend day: {u['ex_date']}",
                     f"Expected price drop on the ex-dividend day: about Rs {u['expected_drop_rs']}",
                     f"Analyst signal: {LABEL.get(u['signal'], u['signal'])} (score {u['score']})", *u["reasons"]]
        else:
            card = a["card"]
            label = LABEL.get(card["signal"], card["signal"])
            counts[label] = counts.get(label, 0) + 1
            held = " (you hold this share)" if a["kind"] == "holding" else ""
            title = f"{card['symbol']} {card.get('name', '')}: {label}{held}, score {card['score']} of 100, Rs {card['price']}"
            lines = top_reasons(card)
            if card.get("red_flags"):
                lines.append("Warning: " + "; ".join(card["red_flags"]))
            note = notes.get(card["symbol"])
            if note:
                lines.append("Analyst note: " + note["summary"])
                lines += [f"Risk: {r}" for r in note.get("risks", [])[:2]]
        blocks_text.append(title + "\n" + "\n".join(f"  - {line}" for line in lines))
        blocks_html.append(f"<h3 style='margin:18px 0 4px'>{html.escape(title)}</h3><ul style='margin:0'>"
                           + "".join(f"<li>{html.escape(str(line))}</li>" for line in lines) + "</ul>")
    subject = "BetaLens: " + ", ".join(f"{n} {k}" for k, n in counts.items())
    link_text = f"\n\nDashboard: {dashboard_url}" if dashboard_url else ""
    link_html = f"<p><a href='{html.escape(dashboard_url, quote=True)}'>Open the dashboard</a></p>" if dashboard_url else ""
    text = "\n\n".join(blocks_text) + link_text + f"\n\n{DISCLAIMER}\n"
    body = ("<div style='font-family:system-ui,Arial,sans-serif;font-size:15px;line-height:1.5'>" + "".join(blocks_html)
            + link_html + f"<p style='color:#666;font-size:13px'>{html.escape(DISCLAIMER)}</p></div>")
    return subject, text, body


def send(subject: str, text: str, body_html: str, smtp_factory=smtplib.SMTP_SSL) -> bool:
    """Send through Gmail. Returns False (and prints why) when the mail settings are missing."""
    user, password, to = (os.environ.get(k, "").strip() for k in ("SMTP_USERNAME", "SMTP_PASSWORD", "ALERT_EMAIL_TO"))
    if not (user and password and to):
        print("Email alert skipped: SMTP_USERNAME, SMTP_PASSWORD or ALERT_EMAIL_TO is not set")
        return False
    msg = EmailMessage()
    msg["Subject"], msg["From"], msg["To"] = subject, f"BetaLens <{user}>", to
    msg.set_content(text)
    msg.add_alternative(body_html, subtype="html")
    with smtp_factory("smtp.gmail.com", 465, timeout=30) as smtp:
        smtp.login(user, password.replace(" ", ""))   # Google shows app passwords with spaces
        smtp.send_message(msg)
    return True
