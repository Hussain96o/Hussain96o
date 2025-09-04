import requests
from PIL import Image, ImageDraw, ImageFont

USERNAME = "Hussain96o"  # ضع هنا اسم حسابك

# سحب بيانات الحساب من GitHub API
url = f"https://api.github.com/users/{USERNAME}"
data = requests.get(url).json()

# استخراج الإحصائيات
name = data.get("name", USERNAME)
public_repos = data.get("public_repos", 0)
followers = data.get("followers", 0)
following = data.get("following", 0)

# فتح الصورة من المسار assets/stats.jpg
img_path = "assets/stats.jpg"
img = Image.open(img_path).convert("RGBA")
draw = ImageDraw.Draw(img)

# اختيار الخط الافتراضي على GitHub Actions
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)

# النصوص المراد كتابتها
lines = [
    f"Name: {name}",
    f"Repos: {public_repos}",
    f"Followers: {followers}",
    f"Following: {following}"
]

# إعداد خلفية زجاجية للنصوص
padding = 20  # مساحة حول النص
y = 50
for line in lines:
    text_width, text_height = draw.textsize(line, font=font)
    
    # رسم مستطيل نصف شفاف خلف النص
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

# حفظ الصورة المعدلة بنفس الاسم والمكان
img.save(img_path)