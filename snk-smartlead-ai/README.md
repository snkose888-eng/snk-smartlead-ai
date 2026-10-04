# SNK Dijital Medya – Akıllı Satış Asistanı

SNK Dijital Medya internet sitesinde kullanılmak üzere hazırlanan SmartLead AI tabanlı örnek backend projesidir.

## Özellikler
- Türkçe akıllı satış asistanı
- Reklam ve tanıtım hizmetleri hakkında yönlendirme
- İsim / telefon / mesaj bilgisini lead olarak kaydetme
- Lead kayıtlarını görüntüleyen yönetim paneli
- `/health` sağlık kontrolü

## Yerel çalıştırma
1. `python -m venv venv`
2. Sanal ortamı etkinleştirin.
3. `pip install -r requirements.txt`
4. İsteğe bağlı olarak `.env` dosyasında `GROQ_API_KEY` tanımlayın.
5. `python run.py`

`.env` dosyası GitHub'a yüklenmemelidir.

## Render
Build Command: `pip install -r requirements.txt`

Start Command: `gunicorn run:app`
