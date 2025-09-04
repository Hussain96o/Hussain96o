import requests
from PIL import Image, ImageDraw, ImageFont

USERNAME = "Hussain96o"  # غيّرها لاسم حسابك

# سحب بيانات GitHub
url = f"https://api.github.com/users/{USERNAME}"
data = requests.get(url).json()

name = data.get("name", USERNAME)
public_repos = data.get("public_repos", 0)
followers = data.get("followers", 0)
following = data.get("following", 0)

# فتح الصورة
img_path = "assets/stats.jpg"
img = Image.open(img_path).convert("RGBA")
draw = ImageDraw.Draw(img)

# الخط الافتراضي على GitHub Actions
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)

lines = [
    f"Name: {name}",
    f"Repos: {public_repos}",
    f"Followers: {followers}",
    f"Following: {following}"
]

padding = 20
y = 50
for line in lines:
    # حساب حجم النص باستخدام draw.textbbox()
    bbox = draw.textbbox((0, 0), line, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # رسم مستطيل زجاجي خلف النص
    rect_x0 = 50 - padding
    rect_y0 = y - padding
    rect_x1 = 50 + text_width + padding
    rect_y1 = y + text_height + padding
    draw.rectangle(
        [(rect_x0, rect_y0), (rect_x1, rect_y1)],
        fill=(0, 0, 0, 150)  # أسود مع شفافية
    )

    # كتابة النص فوق المستطيل
    draw.text((50, y), line, font=font, fill=(255, 255, 255, 255))
    y += text_height + 2 * padding

# حفظ الصورة المعدلة
img.save(img_path)
