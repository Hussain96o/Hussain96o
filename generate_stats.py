import requests
from weasyprint import HTML
from pdf2image import convert_from_path
from PIL import Image
import base64

USERNAME = "Hussain96o"  # ضع هنا اسم حسابك

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
width, height = 800, 450  # 16:9

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
        padding: 20px 40px;
        border-radius: 15px;
        text-align: center;
        color: white;
        font-size: 24px;
    }}
    .box h1 {{
        margin: 0 0 15px 0;
        font-size: 32px;
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
pdf_path = "assets/stats.pdf"
HTML(string=html_template).write_pdf(pdf_path)

# --- تحويل PDF إلى PNG بنفس الأبعاد 16:9 ---
pages = convert_from_path(pdf_path, dpi=200)
img = pages[0].resize((width, height), Image.ANTIALIAS)
img.save("assets/stats.png", "PNG")

print("✅ تم تحديث الصورة stats.png بنجاح بنفس أبعاد الخلفية 16:9!")
