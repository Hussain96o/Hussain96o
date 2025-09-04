import requests
from weasyprint import HTML

USERNAME = "Hussain96o"  # ضع هنا اسم حسابك

# --- جلب بيانات الحساب من GitHub API ---
url = f"https://api.github.com/users/{USERNAME}"
data = requests.get(url).json()

# استخراج البيانات
name = data.get("name", USERNAME)
public_repos = data.get("public_repos", 0)
followers = data.get("followers", 0)
following = data.get("following", 0)

# --- HTML + CSS ---
# الخلفية من الصورة الثابتة background.png
html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <style>
    body {{
        width: 800px;
        height: 600px;
        background: url('assets/background.png') no-repeat center center;
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

# --- تحويل HTML إلى صورة PNG ---
HTML(string=html_template).write_png("assets/stats.png")

print("✅ تم تحديث الصورة stats.png بنجاح!")
