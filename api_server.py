"""API local do A.R.G.U.S. protegida por token."""
import hmac
import os
import secrets
from functools import wraps
from pathlib import Path

from flask import Flask, Response, jsonify, render_template, request
from database import db
from integrations import load_config, sync_to_cloud, trigger_integrations
from monitor import monitor
from predictions import predict_from_history
from themes import get_theme_preference
from webcam import webcam

app = Flask(__name__)
TOKEN_FILE = Path("database/api_token.txt")
MAX_MESSAGE_LENGTH = 2_000


def get_api_token():
    configured = os.getenv("ARGUS_API_TOKEN")
    if configured:
        return configured
    TOKEN_FILE.parent.mkdir(exist_ok=True)
    if not TOKEN_FILE.exists():
        TOKEN_FILE.write_text(secrets.token_urlsafe(32), encoding="utf-8")
    return TOKEN_FILE.read_text(encoding="utf-8").strip()


def _request_is_authorized():
    token = request.headers.get("X-API-Key", "") or request.args.get("token", "")
    return bool(token) and hmac.compare_digest(token, get_api_token())


def require_api_token(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not _request_is_authorized():
            return jsonify({"error": "unauthorized"}), 401
        return view(*args, **kwargs)
    return wrapped


@app.route("/api/stats")
@require_api_token
def get_stats(): return jsonify(monitor.get_all_stats())


@app.route("/api/history")
@require_api_token
def get_history(): return jsonify(db.get_latest_stats(limit=min(max(request.args.get("limit", 20, type=int), 1), 500)))


@app.route("/api/predictions")
@require_api_token
def predictions(): return jsonify(predict_from_history(db.get_latest_stats(limit=100)))


@app.route("/api/health")
@require_api_token
def health(): return jsonify({"status": "ok"})


@app.route("/api/integrations", methods=["POST"])
@require_api_token
def integrations_endpoint():
    payload = request.get_json(silent=True) or {}
    return jsonify(trigger_integrations(str(payload.get("message", "A.R.G.U.S. atualização recebida"))[:MAX_MESSAGE_LENGTH]))


@app.route("/api/cloud/sync", methods=["POST"])
@require_api_token
def cloud_sync_endpoint(): return jsonify(sync_to_cloud())


@app.route("/api/webcam/start", methods=["POST"])
@require_api_token
def webcam_start():
    return jsonify({"active": webcam.start_recording()})


@app.route("/api/webcam/stop", methods=["POST"])
@require_api_token
def webcam_stop():
    webcam.stop_recording()
    return jsonify({"active": False})


def _video_stream():
    while webcam.is_recording:
        frame = webcam.get_jpeg_frame()
        if frame:
            yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"


@app.route("/webcam/feed")
@require_api_token
def webcam_feed():
    if not webcam.is_recording:
        webcam.start_recording()
    return Response(_video_stream(), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/webcam")
@require_api_token
def webcam_page():
    return render_template("webcam.html", api_token=request.args.get("token", ""))


@app.route("/dashboard")
@require_api_token
def dashboard_page():
    stats = monitor.get_all_stats()
    alerts = [label + " alta" for key, threshold, label in (("cpu", 80, "CPU"), ("ram", 80, "RAM"), ("temperature", 70, "Temperatura")) if stats.get(key, 0) > threshold]
    return render_template("dashboard_web.html", theme=get_theme_preference(), stats=stats, alerts=alerts, config=load_config(), api_token=request.args.get("token", ""))


if __name__ == "__main__":
    print("API local: http://127.0.0.1:5000; token em database/api_token.txt")
    app.run(host="127.0.0.1", port=5000, debug=False, threaded=True)
