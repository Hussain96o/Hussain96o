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
width, height = img.size

# اختيار الخط وحجمه
try:
    # المسار للخط في بيئات لينكس القياسية
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
except IOError:
    # استخدام الخط الافتراضي في حالة عدم العثور على الخط المحدد
    font = ImageFont.load_default()

# النصوص المراد كتابتها
lines = [
    f"Name: {name}",
    f"Repos: {public_repos}",
    f"Followers: {followers}",
    f"Following: {following}"
]

# حساب أبعاد كتلة النص
padding = 20
line_height = font.getsize("hg")[1]  # 'hg' للحصول على ارتفاع تقريبي
total_text_height = len(lines) * line_height + (len(lines) - 1) * padding
max_text_width = 0
for line in lines:
    line_width, _ = draw.textsize(line, font=font)
    if line_width > max_text_width:
        max_text_width = line_width

# إعداد خلفية شبه شفافة للنصوص
rect_width = max_text_width + 2 * padding
rect_height = total_text_height + padding
rect_x0 = (width - rect_width) / 2
rect_y0 = (height - rect_height) / 2
rect_x1 = rect_x0 + rect_width
rect_y1 = rect_y0 + rect_height

draw.rectangle(
    [(rect_x0, rect_y0), (rect_x1, rect_y1)],
    fill=(0, 0, 0, 150)  # أسود مع شفافية
)

# كتابة النص فوق المستطيل
y = rect_y0 + padding / 2
for line in lines:
    text_width, _ = draw.textsize(line, font=font)
    x = (width - text_width) / 2
    draw.text((x, y), line, font=font, fill=(255, 255, 255, 255))
    y += line_height + padding

# حفظ الصورة المعدلة بنفس الاسم والمكان
img.save(img_path)

print("تم تحديث الصورة بنجاح!")
