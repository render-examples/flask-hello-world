from flask import Flask
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <div style="text-align:center; font-family:sans-serif; padding:50px; background:#0f172a; color:white; min-height:100vh">
        <h1 style="color:#22c55e">✅ بوت FUTBIN شغال!</h1>
        <p>السيرفر مربوط وكل شي تمام</p>
        <a href="/sbc" style="display:inline-block; margin-top:20px; padding:15px 30px; background:#22c55e; color:white; text-decoration:none; border-radius:10px; font-weight:bold">روح لتحديات SBC</a>
    </div>
    """

@app.route('/sbc')
def sbc():
    try:
        url = "https://www.futbin.com/squad-building-challenges"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')
        titles = [t.text.strip() for t in soup.select('.sbc-name')][:10]
        if not titles:
            titles = ["قدرنا نتصل بـ FUTBIN بس ما لقينا العناوين - بنصلحها"]
        html = "<br>".join([f"🔹 {t}" for t in titles])
        return f"<div style='font-family:sans-serif; padding:20px'><h2>تحديات SBC الحالية من FUTBIN:</h2>{html}<br><br><a href='/'>رجوع</a></div>"
    except Exception as e:
        return f"خطأ: {e}"

if __name__ == '__main__':
    app.run()
