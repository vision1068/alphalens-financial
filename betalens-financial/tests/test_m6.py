import json
from pathlib import Path
from types import SimpleNamespace

from betalens import alerts, analyst
from betalens.data import parsers
from betalens.models import CompanyData, YearFigures

CFG = {"alert_signals": ["STRONG_BUY", "STRONG_SELL"], "holding_alert_signals": ["SELL", "STRONG_SELL"]}


def card(symbol="AAA", signal="STRONG_BUY", score=90.0, flags=None):
    return {"symbol": symbol, "name": f"{symbol} Ltd", "signal": signal, "score": score, "coverage_pct": 62.0,
            "price": 100.0, "red_flags": flags or [],
            "factors": [{"name": "valuation", "score": 95.0, "weight": 20, "reasons": ["P/E 4.0"]},
                        {"name": "revenue_growth", "score": 55.0, "weight": 12, "reasons": ["Sales grew 6%"]},
                        {"name": "price_trend", "score": 10.0, "weight": 6, "reasons": ["Price is below its 200-day average"]},
                        {"name": "debt", "score": None, "weight": 12, "reasons": ["Needs balance sheet data"]}]}


def company(symbol="AAA"):
    return CompanyData(symbol, name=f"{symbol} Ltd", sector="CEMENT", price=100.0, pe_ratio=4.0,
                       years=[YearFigures(2026, sales=10, profit_after_tax=2, eps=5.0)])


class FakeClient:
    def __init__(self, replies):
        self.replies, self.calls = list(replies), []
        self.messages = SimpleNamespace(create=self._create)

    def _create(self, **kwargs):
        self.calls.append(kwargs)
        reply = self.replies.pop(0)
        if isinstance(reply, Exception):
            raise reply
        return SimpleNamespace(content=[SimpleNamespace(type="text", text=reply)])


GOOD = json.dumps({"summary": "Cheap versus its sector.", "strengths": ["Low P/E"], "risks": ["No debt data"],
                   "checks": ["Read the cash flow statement"], "extra": "ignored"})


def test_parse_note_validates_and_trims():
    note = analyst.parse_note("Here you go:\n" + GOOD)
    assert note == {"summary": "Cheap versus its sector.", "strengths": ["Low P/E"], "risks": ["No debt data"],
                    "checks": ["Read the cash flow statement"]}
    assert analyst.parse_note("no json") is None and analyst.parse_note('{"summary": ""}') is None
    assert analyst.parse_note('{"summary": "x", "risks": "not a list"}')["risks"] == []
    assert len(analyst.parse_note(json.dumps({"summary": "x", "risks": list("abcdef")}))["risks"]) == 3


def test_notes_are_written_once_and_rewritten_when_the_picture_changes():
    cards, companies = [card()], {"AAA": company()}
    client = FakeClient([GOOD, GOOD])
    notes, written = analyst.write_notes(cards, companies, {}, "claude-sonnet-5-5", 30, client)
    assert written == 1 and notes["AAA"]["summary"] == "Cheap versus its sector." and notes["AAA"]["model"] == "claude-sonnet-5-5"
    sent = client.calls[0]
    assert sent["model"] == "claude-sonnet-5-5" and "AAA" in sent["messages"][0]["content"]
    _, written = analyst.write_notes(cards, companies, notes, "claude-sonnet-5-5", 30, client)
    assert written == 0 and len(client.calls) == 1                      # unchanged company: no API call
    cards[0]["signal"] = "BUY"
    _, written = analyst.write_notes(cards, companies, notes, "claude-sonnet-5-5", 30, client)
    assert written == 1


def test_notes_prioritise_strong_signals_respect_limit_and_survive_failures():
    cards = [card("H1", "HOLD"), card("SB", "STRONG_BUY"), card("B1", "BUY"), card("NA", "INSUFFICIENT_DATA")]
    companies = {s: company(s) for s in ("H1", "SB", "B1", "NA")}
    assert [k["symbol"] for k in analyst.select(cards, companies, {}, 2)] == ["SB", "B1"]
    client = FakeClient([RuntimeError("boom"), "not json", GOOD])
    notes, written = analyst.write_notes(cards, companies, {}, "m", 30, client)
    assert written == 1 and list(notes) == ["H1"]


def test_no_api_key_means_no_calls(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    assert analyst.write_notes([card()], {"AAA": company()}, {"AAA": {"key": "old"}}, "m", 30) == ({"AAA": {"key": "old"}}, 0)


def test_alerts_fire_once_per_change():
    cards = [card("AAA", "STRONG_BUY"), card("BBB", "SELL"), card("CCC", "HOLD"), card("DDD", "STRONG_SELL")]
    div = {"symbol": "AAA", "verdict": "WORTH_A_LOOK", "book_closure_from": "2026-12-01", "amount_per_share": 5.0,
           "yield_pct": 5.0, "last_buy_date": "2026-11-27", "ex_date": "2026-11-30", "expected_drop_rs": 4.5,
           "signal": "BUY", "score": 80, "reasons": ["Recovered quickly"]}
    skip = dict(div, symbol="CCC", verdict="SKIP")
    pending, state = alerts.find_alerts(cards, [div, skip], {}, CFG, {"BBB"})
    assert [(a["kind"], (a.get("card") or a["dividend"])["symbol"]) for a in pending] == \
        [("signal", "AAA"), ("holding", "BBB"), ("signal", "DDD"), ("dividend", "AAA")]
    again, _ = alerts.find_alerts(cards, [div, skip], state, CFG, {"BBB"})
    assert again == []
    cards[2]["signal"] = "STRONG_SELL"
    changed, _ = alerts.find_alerts(cards, [div], state, CFG, set())
    assert [a["card"]["symbol"] for a in changed] == ["CCC"]
    assert alerts.find_alerts([card("BBB", "SELL")], [], {}, CFG, set())[0] == []      # Sell on a share not held


def test_compose_escapes_and_summarises():
    pending, _ = alerts.find_alerts([card("AAA", "STRONG_BUY", flags=["Check <b>split</b>"])], [], {}, CFG, set())
    subject, text, body = alerts.compose(pending, {"AAA": {"summary": "Cheap.", "risks": ["No debt data"]}}, "https://x.netlify.app")
    assert subject == "BetaLens: 1 Strong Buy"
    assert "Valuation 95/100: P/E 4.0" in text and "Analyst note: Cheap." in text and "https://x.netlify.app" in text
    assert "&lt;b&gt;split&lt;/b&gt;" in body and "<b>split</b>" not in body
    assert alerts.top_reasons(card())[0].startswith("Valuation") and len(alerts.top_reasons(card())) == 3


def test_send_uses_gmail_and_skips_without_settings(monkeypatch):
    sent = {}

    class FakeSmtp:
        def __init__(self, host, port, timeout):
            sent["server"] = (host, port)
        def __enter__(self): return self
        def __exit__(self, *a): return False
        def login(self, user, password): sent["login"] = (user, password)
        def send_message(self, msg): sent["msg"] = msg

    for k in ("SMTP_USERNAME", "SMTP_PASSWORD", "ALERT_EMAIL_TO"):
        monkeypatch.delenv(k, raising=False)
    assert alerts.send("s", "t", "<p>h</p>", FakeSmtp) is False and not sent
    monkeypatch.setenv("SMTP_USERNAME", "from@example.com")
    monkeypatch.setenv("SMTP_PASSWORD", "abcd efgh ijkl mnop")
    monkeypatch.setenv("ALERT_EMAIL_TO", "to@example.com")
    assert alerts.send("Subject", "text", "<p>html</p>", FakeSmtp) is True
    assert sent["server"] == ("smtp.gmail.com", 465) and sent["login"] == ("from@example.com", "abcdefghijklmnop")
    assert sent["msg"]["To"] == "to@example.com" and sent["msg"]["Subject"] == "Subject"


def test_announcement_titles_are_parsed():
    c = parsers.parse_company_page((Path(__file__).parent / "fixtures" / "company_PSO.html").read_text(encoding="utf-8"), "PSO")
    assert c.announcements and any("Quarterly Report" in a for a in c.announcements)
    f = analyst.facts({"score": 1, "signal": "HOLD", "coverage_pct": 1, "factors": []}, c)
    assert f["recent_announcement_titles"] == c.announcements[:8] and f["symbol"] == "PSO"


def test_analyst_stops_after_repeated_failures():
    cards = [card(f"S{i}", "BUY") for i in range(6)]
    companies = {k["symbol"]: company(k["symbol"]) for k in cards}
    client = FakeClient([RuntimeError("400")] * 6)
    notes, written = analyst.write_notes(cards, companies, {}, "m", 30, client)
    assert written == 0 and notes == {} and len(client.calls) == 3
