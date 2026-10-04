from flask import Blueprint, jsonify, render_template, request
from .database import lead_ekle, tum_leadler
from .services.ai_service import ai_service, AIServiceError

bp = Blueprint("main", __name__)

@bp.get("/")
def index():
    return render_template("index.html")

@bp.get("/dashboard")
def dashboard():
    return render_template("dashboard.html", leads=tum_leadler())

@bp.post("/api/sohbet")
def sohbet():
    data = request.get_json(silent=True) or {}
    mesaj = (data.get("mesaj") or "").strip()
    gecmis = data.get("gecmis") or []
    if not mesaj:
        return jsonify({"basari": False, "hata": "Mesaj zorunludur."}), 400
    try:
        yanit = ai_service.yanit_uret(mesaj, gecmis)
        return jsonify({"basari": True, "yanit": yanit}), 200
    except AIServiceError as exc:
        return jsonify({"basari": False, "hata": str(exc)}), 503

@bp.post("/api/leads")
def leads_ekle():
    data = request.get_json(silent=True) or {}
    isim = (data.get("isim") or "").strip()
    telefon = (data.get("telefon") or "").strip()
    mesaj = (data.get("mesaj") or "").strip()
    if not isim or not telefon:
        return jsonify({"basari": False, "hata": "İsim ve telefon zorunludur."}), 400
    lead_id = lead_ekle(isim, telefon, mesaj)
    return jsonify({"basari": True, "id": lead_id}), 201

@bp.get("/api/leads")
def leads_listele():
    return jsonify({"basari": True, "leads": tum_leadler()}), 200
