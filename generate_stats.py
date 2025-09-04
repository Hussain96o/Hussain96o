import requests
from weasyprint import HTML, CSS # قد نحتاج لاستيراد CSS للتحكم الدقيق
import base64
import os

USERNAME = "Hussain96o"  # ضع هنا اسم حسابك

# --- التأكد من وجود مجلد assets ---
if not os.path.exists("assets"):
    os.makedirs("assets")

# --- جلب بيانات الحساب من GitHub API ---
url = f"https://api.github.com/users/{USERNAME}"
data = requests.get(url).json()

name = data.get("name", USERNAME)
public_repos = data.get("public_repos", 0)
followers = data.get("followers", 0)
following = data.get("following", 0)

# --- تحويل الخلفية إلى Base64 ---
with open("assets/background.png", "rb") as f:
    encoded_bg = base64.b64encode(f.read()).decode()

# --- تحديد أبعاد 16:9 ---
width, height = 1280, 720  # أبعاد 16:9 بجودة أعلى

# --- HTML + CSS ---
# الكود هنا لم يتغير
html_template = f"""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8">
  <style>
    /* تطبيق الخلفية والأبعاد على عنصر html مباشرة */
    html {{
        width: {width}px;
        height: {height}px;
        background: url('data:image/png;base64,{encoded_bg}') no-repeat center center;
        background-size: cover;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }}
    body {{
        width: 100%;
        height: 100%;
        margin: 0;
        padding: 0;
        position: relative;
    }}
    .stats-box {{
        position: absolute;
        bottom: 25px;
        right: 25px;
        background: rgba(0,0,0,0.65);
        padding: 15px 30px;
        border-radius: 12px;
        text-align: right;
        color: white;
    }}
    .stats-box p {{
        margin: 8px 0;
        font-size: 22px;
    }}
    .stats-box h1 {{
        margin: 0 0 10px 0;
        font-size: 30px;
        border-bottom: 2px solid rgba(255, 255, 255, 0.5);
        padding-bottom: 10px;
    }}
  </style>
</head>
<body>
  <div class="stats-box">
    <h1>{name}</h1>
    <p>المستودعات العامة: {public_repos}</p>
    <p>المتابعون: {followers}</p>
    <p>يتابع: {following}</p>
  </div>
</body>
</html>
"""

# --- التحويل المباشر من HTML إلى PNG ---
# هذه هي الخطوة الجديدة والمبسطة
output_path = "assets/stats.png"
HTML(string=html_template).write_png(output_path)

print(f"✅ تم تحديث الصورة stats.png مباشرة بنجاح بأبعاد {width}x{height}!")
