import requests
from PIL import Image, ImageDraw, ImageFont, ImageFilter
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

# --- إعداد الصورة ---
try:
    # 1. افتح صورة الخلفية
    img = Image.open("assets/background.png").convert("RGBA")
except FileNotFoundError:
    print("❌ خطأ: لم يتم العثور على ملف الخلفية 'assets/background.png'. يرجى التأكد من وجوده.")
    exit()

# 2. حمّل الخط. استخدام خطوط إنجليزية قياسية.
try:
    # يمكنك استخدام أي خط مثبت على نظامك مثل "arial.ttf"
    font_header = ImageFont.truetype("arialbd.ttf", size=32) # Bold for header
    font_body = ImageFont.truetype("arial.ttf", size=22)
except IOError:
    print("⚠️ تحذير: لم يتم العثور على خط Arial. سيتم استخدام الخط الافتراضي.")
    font_header = ImageFont.load_default()
    font_body = ImageFont.load_default()

# 3. جهّز أداة الرسم
draw = ImageDraw.Draw(img, "RGBA")

# --- حساب الأبعاد والمواقع ---
img_width, img_height = img.size
margin = 40
padding = 25
line_spacing = 12

# النصوص باللغة الإنجليزية
lines = [
    (f"Public Repos: {public_repos}", font_body),
    (f"Followers: {followers}", font_body),
    (f"Following: {following}", font_body),
]

# حساب عرض وارتفاع الصندوق بناءً على حجم النصوص
box_width = max(draw.textlength(text, font=font) for text, font in lines + [(name, font_header)]) + (padding * 2)
box_height = font_header.getbbox(name)[3] + (padding * 2) + (font_body.getbbox("T")[3] * len(lines)) + (line_spacing * (len(lines)))

# تحديد إحداثيات الصندوق في الركن الأيمن السفلي
box_x0 = int(img_width - box_width - margin)
box_y0 = int(img_height - box_height - margin)
box_x1 = int(img_width - margin)
box_y1 = int(img_height - margin)

# --- تطبيق تأثير الزجاج الشفاف ---

# 1. قص منطقة الصندوق من الخلفية
box_crop = img.crop((box_x0, box_y0, box_x1, box_y1))

# 2. طبّق فلتر الضبابية (Blur)
blurred_box = box_crop.filter(ImageFilter.GaussianBlur(radius=15)) # يمكنك التحكم في قوة الضبابية

# 3. الصق النسخة الضبابية مرة أخرى في مكانها
img.paste(blurred_box, (box_x0, box_y0))

# 4. ارسم فوقها طبقة بيضاء شبه شفافة لإعطاء الإحساس بالزجاج
draw.rectangle(
    [box_x0, box_y0, box_x1, box_y1],
    fill=(255, 255, 255, 50) # لون أبيض مع شفافية عالية جدًا (Alpha=50)
)
# 5. (اختياري) إضافة إطار خفيف جدًا لتعزيز الشكل
draw.rectangle(
    [box_x0, box_y0, box_x1, box_y1],
    outline=(255, 255, 255, 80), # إطار أبيض شبه شفاف
    width=1
)

# --- كتابة النصوص ---
text_color = (10, 10, 10) # لون أسود/داكن للوضوح على الخلفية الفاتحة
current_y = box_y0 + padding

# كتابة الاسم
name_width = draw.textlength(name, font=font_header)
draw.text(
    (box_x1 - padding - name_width, current_y),
    name,
    font=font_header,
    fill=text_color
)
current_y += font_header.getbbox(name)[3] + line_spacing

# رسم خط فاصل
draw.line(
    [box_x0 + padding, current_y, box_x1 - padding, current_y],
    fill=(0, 0, 0, 100),
    width=1
)
current_y += line_spacing

# كتابة باقي الإحصائيات
for text, font in lines:
    text_width = draw.textlength(text, font=font)
    draw.text(
        (box_x1 - padding - text_width, current_y),
        text,
        font=font,
        fill=text_color
    )
    current_y += font.getbbox(text)[3] + line_spacing


# --- حفظ الصورة النهائية ---
output_path = "assets/stats.png"
img.save(output_path, "PNG")

print(f"✅ تم تحديث الصورة '{output_path}' بنجاح مع تأثير الزجاج!")
