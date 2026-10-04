import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-me")
    DATABASE_URL = os.environ.get("DATABASE_URL", "smartlead.db")
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
    AI_PROVIDER = os.environ.get("AI_PROVIDER", "groq")
    CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "*")
    BUSINESS_CONTEXT = os.environ.get(
        "BUSINESS_CONTEXT",
        "Sen SNK Dijital Medya’nın Akıllı Satış Asistanısın. "
        "Ziyaretçilere banner reklam, sponsorlu içerik, video tanıtım ve "
        "sosyal medya görünürlüğü seçenekleri hakkında Türkçe, kısa ve "
        "profesyonel bilgi ver. Uygun olduğunda ziyaretçiyi iletişim "
        "bilgisi bırakmaya yönlendir."
    )

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
