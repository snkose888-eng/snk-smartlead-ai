
from flask import Blueprint, jsonify, render_template, request
from .database import lead_ekle, tum_leadler
from .services.ai_service import ai_service, AIServiceError

bp = Blueprint("main", __name__)


# ANA SAYFA
@bp.get("/")
def index():
    return render_template("index.html")


# YÖNETİM PANELİ
@bp.get("/dashboard")
def dashboard():
    return render_template(
        "dashboard.html",
        leads=tum_leadler()
    )


# YAPAY ZEKA CHATBOT
@bp.post("/api/sohbet")
def sohbet():

    data = request.get_json(silent=True) or {}

    mesaj = (data.get("mesaj") or "").strip()
    gecmis = data.get("gecmis") or []

    if not mesaj:
        return jsonify({
            "basari": False,
            "hata": "Mesaj zorunludur."
        }), 400

    try:
        yanit = ai_service.yanit_uret(
            mesaj,
            gecmis
        )

        return jsonify({
            "basari": True,
            "yanit": yanit
        }), 200

    except AIServiceError as exc:
        return jsonify({
            "basari": False,
            "hata": str(exc)
        }), 503


# İLETİŞİM FORMUNDAN VERİ ALMA
@bp.post("/api/leads")
def leads_ekle():

    data = request.get_json(silent=True) or {}

    # Wix Studio iletişim formu
    ad = (data.get("ad") or "").strip()
    soyad = (data.get("soyad") or "").strip()

    # Önceki Wix koduyla uyumluluk
    isim = (data.get("isim") or "").strip()

    telefon = (data.get("telefon") or "").strip()
    mesaj = (data.get("mesaj") or "").strip()

    # Ad ve soyadı birleştir
    if ad and soyad:
        isim = f"{ad} {soyad}"

    # Zorunlu alan kontrolü
    if not isim or not mesaj:
        return jsonify({
            "basari": False,
            "hata": "Ad, soyad ve mesaj zorunludur."
        }), 400

    try:
        # Veritabanına kaydet
        lead_id = lead_ekle(
            isim,
            telefon,
            mesaj
        )

        return jsonify({
            "basari": True,
            "mesaj": "İletişim mesajı kaydedildi.",
            "id": lead_id
        }), 201

    except Exception:
        bp.logger.exception("Lead kaydetme hatası") if hasattr(bp, "logger") else None
        return jsonify({
            "basari": False,
            "hata": "Mesaj kaydedilemedi."
        }), 500


# YÖNETİM PANELİ İÇİN MESAJLARI LİSTELEME
@bp.get("/api/leads")
def leads_listele():

    try:
        leads = tum_leadler()

        return jsonify({
            "basari": True,
            "leads": leads
        }), 200

    except Exception:
        return jsonify({
            "basari": False,
            "hata": "Mesajlar getirilemedi."
        }), 500
