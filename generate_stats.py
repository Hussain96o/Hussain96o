import requests
from weasyprint import HTML
from pdf2image import convert_from_path
import base64
from PIL import Image  # إضافة مكتبة Pillow لقراءة أبعاد الصورة

USERNAME = "Hussain96o"

# --- جلب بيانات GitHub API ---
url = f"https://api.github.com/users/{USERNAME}"
data = requests.get(url).json()

name = data.get("name", USERNAME)
public_repos = data.get("public_repos", 0)
followers = data.get("followers", 0)
following = data.get("following", 0)

# --- تحويل الخلفية إلى Base64 ---
with open("assets/background.png", "rb") as f:
    encoded_bg = base64.b64encode(f.read()).decode()

# --- قراءة أبعاد الصورة الأصلية ---
with Image.open("assets/background.png") as img:
    width, height = img.size  # الحصول على الأبعاد الأصلية للصورة

# --- HTML + CSS ---
html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <style>
    body {{
        width: {width}px;
        height: {height}px;
        background: url('data:image/png;base64,{encoded_bg}') no-repeat center center;
        background-size: cover;
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: sans-serif;
        margin: 0;
        padding: 0;
    }}
    .box {{
        background: rgba(0,0,0,0.6);
        padding: 30px 50px;
        border-radius: 15px;
        text-align: center;
        color: white;
        font-size: 28px;
    }}
    .box h1 {{
        margin: 0 0 20px 0;
        font-size: 36px;
    }}
  </style>
</head>
<body>
  <div class="box">
    <h1>{name}</h1>
    <p>Repos: {public_repos}</p>
    <p>Followers: {followers}</p>
    <p>Following: {following}</p>
  </div>
</body>
</html>
"""

# --- حفظ PDF أولاً ---
HTML(string=html_template).write_pdf("assets/stats.pdf")

# --- تحويل PDF إلى PNG ---
pages = convert_from_path("assets/stats.pdf", dpi=200)
pages[0].save("assets/stats.png", "PNG")

print(f"✅ تم تحديث الصورة stats.png بنجاح بأبعاد الصورة الأصلية ({width}x{height})!")
