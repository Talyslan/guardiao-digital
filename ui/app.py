from flask import Flask, render_template, request, redirect, url_for, flash
from ui.services.api_client import APIClient, APIError
from uuid import uuid4
import os

app = Flask(__name__)
app.secret_key = os.environ.get("UI_SECRET_KEY", "dev-secret-key")

HISTORY = []

API_BASE = os.environ.get("GUARDIAO_API_URL", "http://127.0.0.1:8000/api/v1")
api = APIClient(API_BASE)


@app.route("/", methods=["GET"])  
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    text = request.form.get("text", "").strip()
    url = request.form.get("url", "").strip() or None

    if not text and not url:
        flash("Por favor informe um texto ou uma URL para analisar.", "warning")
        return redirect(url_for("index"))

    payload = {"text": text}
    if url:
        payload["url"] = url

    try:
        result = api.post("/analyze", json=payload)
    except APIError as e:
        details = getattr(e, 'details', None)
        msg = str(e)
        if isinstance(details, dict):
            detail_text = details.get('detail') or details.get('message') or details.get('text')
            if detail_text:
                msg = f"{msg} — {detail_text}"
        if request.headers.get('HX-Request'):
            return render_template('partials/error_fragment.html', message=msg), 502
        flash(f"Erro ao comunicar com a API: {msg}", "danger")
        return redirect(url_for("index"))

    entry = {
        "id": str(uuid4()),
        "text": text,
        "url": url,
        "result": result,
    }
    HISTORY.insert(0, entry)
    
    if request.headers.get('HX-Request'):
        return render_template('partials/result_fragment.html', analysis=result)
    return render_template("result.html", analysis=result, entry=entry)


@app.route("/phishing", methods=["GET", "POST"])
def phishing_analyze():
    if request.method == "GET":
        return render_template("phishing.html")

    text = request.form.get("text", "").strip() or None
    url = request.form.get("url", "").strip() or None
    email = request.form.get("email", "").strip() or None

    if not any((text, url, email)):
        flash("Informe pelo menos um campo para análise de phishing.", "warning")
        return redirect(url_for("phishing_analyze"))

    payload = {k: v for k, v in (('text', text), ('url', url), ('email', email)) if v}

    try:
        result = api.post("/phishing/analyze", json=payload)
    except APIError as e:
        details = getattr(e, 'details', None)
        msg = str(e)
        if isinstance(details, dict):
            detail_text = details.get('detail') or details.get('message') or details.get('text')
            if detail_text:
                msg = f"{msg} — {detail_text}"
        if request.headers.get('HX-Request'):
            return render_template('partials/error_fragment.html', message=msg), 502
        flash(f"Erro ao comunicar com a API: {msg}", "danger")
        return redirect(url_for("phishing_analyze"))

    entry = {"id": str(uuid4()), "text": text, "url": url, "email": email, "result": result}
    HISTORY.insert(0, entry)
    if request.headers.get('HX-Request'):
        return render_template('partials/result_fragment.html', analysis=result)
    return render_template("phishing_result.html", analysis=result, entry=entry)


@app.route("/history")
def history():
    return render_template("history.html", history=HISTORY)


@app.route('/history/list')
def history_list_fragment():
    return render_template('partials/history_list_fragment.html', history=HISTORY)


@app.route('/history/<entry_id>/fragment')
def history_detail_fragment(entry_id):
    for e in HISTORY:
        if e["id"] == entry_id:
            return render_template('partials/detail_fragment.html', entry=e)
    return render_template('partials/detail_fragment.html', entry=None), 404


@app.route("/history/<entry_id>")
def history_detail(entry_id):
    for e in HISTORY:
        if e["id"] == entry_id:
            return render_template("detail.html", entry=e)
    flash("Análise não encontrada.", "warning")
    return redirect(url_for("history"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050, debug=True)
