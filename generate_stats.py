import requests
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

USERNAME = "Hussain96o"

# --- التأكد من وجود مجلد assets ---
if not os.path.exists("assets"):
    os.makedirs("assets")

# --- جلب بيانات الحساب ---
try:
    url = f"https://api.github.com/users/{USERNAME}"
    data = requests.get(url).json()
    name = data.get("name", USERNAME)
    public_repos = data.get("public_repos", 0)
    followers = data.get("followers", 0)
    following = data.get("following", 0)
except requests.exceptions.RequestException as e:
    print(f"❌ خطأ في الاتصال بـ GitHub API: {e}")
    # استخدام بيانات افتراضية للمتابعة
    name, public_repos, followers, following = "GitHub User", 0, 0, 0

# --- إعداد الصورة ---
try:
    # 1. افتح صورة الخلفية وتأكد 100% من تحويلها لوضع الشفافية
    img = Image.open("assets/background.png").convert("RGBA")
except FileNotFoundError:
    print("❌ خطأ: لم يتم العثور على ملف الخلفية 'assets/background.png'.")
    exit()

# --- طباعة تشخيصية مهمة ---
print(f"Image Mode after opening and converting: {img.mode}") # يجب أن تكون النتيجة 'RGBA'

# 2. حمّل الخط
try:
    font_header = ImageFont.truetype("arialbd.ttf", size=28)
    font_body = ImageFont.truetype("arial.ttf", size=20)
except IOError:
    print("⚠️ تحذير: لم يتم العثور على خط Arial. سيتم استخدام الخط الافتراضي.")
    font_header = ImageFont.load_default()
    font_body = ImageFont.load_default()

# --- حساب الأبعاد ---
img_width, img_height = img.size
margin = 40
padding = 30
line_spacing = 15

lines = [
    (f"Public Repos: {public_repos}", font_body),
    (f"Followers: {followers}", font_body),
    (f"Following: {following}", font_body),
]

box_width = int(max(draw.textlength(text, font=font) for text, font in lines + [(name, font_header)]) + (padding * 2))
box_height = int(font_header.getbbox(name)[3] + (padding * 2) + (font_body.getbbox("T")[3] * len(lines)) + (line_spacing * (len(lines))))

box_x0 = img_width - box_width - margin
box_y0 = img_height - box_height - margin
box_x1 = img_width - margin
box_y1 = img_height - margin

# --- [الطريقة الجديدة] تطبيق تأثير الزجاج الشفاف ---

# 1. قص منطقة الصندوق من الخلفية الأصلية
box_crop = img.crop((box_x0, box_y0, box_x1, box_y1))

# 2. طبّق ضبابية على الجزء المقصوص
blurred_box = box_crop.filter(ImageFilter.GaussianBlur(radius=10))

# 3. أنشئ طبقة جديدة شفافة تماماً بنفس حجم الصندوق
glass_layer = Image.new("RGBA", (box_width, box_height), (255, 255, 255, 0))

# 4. ارسم المستطيل الأبيض شبه الشفاف على هذه الطبقة الجديدة
draw_glass = ImageDraw.Draw(glass_layer)
draw_glass.rectangle(
    (0, 0, box_width, box_height),
    fill=(255, 255, 255, 40), # طبقة بيضاء خفيفة
    outline=(255, 255, 255, 90), # إطار
    width=2
)

# 5. ادمج الطبقة الضبابية مع الطبقة الزجاجية
#    هذا يضمن تطبيق الشفافية بشكل صحيح
final_box = Image.alpha_composite(blurred_box, glass_layer)

# 6. الصق الصندوق النهائي (الذي يحتوي الآن على كل التأثيرات) على الصورة الأصلية
img.paste(final_box, (box_x0, box_y0))

# --- كتابة النصوص فوق الصندوق النهائي ---
#    (نرسم على الصورة الرئيسية 'img' وليس على الطبقات)
draw = ImageDraw.Draw(img)
text_color = (15, 15, 15)
current_y = box_y0 + padding

# ... (باقي كود كتابة النصوص لم يتغير) ...
name_width = draw.textlength(name, font=font_header)
draw.text((box_x1 - padding - name_width, current_y), name, font=font_header, fill=text_color)
current_y += font_header.getbbox(name)[3] + line_spacing
draw.line([box_x0 + padding, current_y, box_x1 - padding, current_y], fill=(0, 0, 0, 80), width=1)
current_y += line_spacing
for text, font in lines:
    text_width = draw.textlength(text, font=font)
    draw.text((box_x1 - padding - text_width, current_y), text, font=font, fill=text_color)
    current_y += font.getbbox(text)[3] + line_spacing

# --- حفظ الصورة النهائية ---
output_path = "assets/stats.png"
img.save(output_path, "PNG")

print(f"✅ تم تحديث الصورة '{output_path}' بالطريقة الأكثر قوة!")
