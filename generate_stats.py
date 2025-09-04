import requests
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

USERNAME = "Hussain96o"

# --- التأكد من وجود مجلد assets ---
if not os.path.exists("assets"):
    os.makedirs("assets")

# --- جلب بيانات الحساب مع معالجة الأخطاء ---
try:
    url = f"https://api.github.com/users/{USERNAME}"
    data = requests.get(url).json()
    # التحقق من أن المفاتيح موجودة قبل استخدامها
    name = data.get("name", USERNAME)
    public_repos = data.get("public_repos", 0)
    followers = data.get("followers", 0)
    following = data.get("following", 0)
    print("✅ تم جلب بيانات GitHub بنجاح.")
except requests.exceptions.RequestException as e:
    print(f"❌ خطأ في الاتصال بـ GitHub API: {e}")
    # في حالة الفشل، نستخدم بيانات افتراضية حتى لا يتوقف السكريبت
    name, public_repos, followers, following = "GitHub User", 0, 0, 0

# --- إعداد الصورة ---
try:
    # 1. افتح صورة الخلفية وتأكد 100% من تحويلها لوضع الشفافية
    # هذا السطر هو أهم سطر لضمان عمل الشفافية
    img = Image.open("assets/background.png").convert("RGBA")
except FileNotFoundError:
    print("❌ خطأ: لم يتم العثور على ملف الخلفية 'assets/background.png'. تأكد من وجوده.")
    exit()

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
margin = 40      # الهامش الخارجي من حافة الصورة
padding = 30     # الهامش الداخلي في الصندوق
line_spacing = 15 # المسافة بين السطور

lines = [
    (f"Public Repos: {public_repos}", font_body),
    (f"Followers: {followers}", font_body),
    (f"Following: {following}", font_body),
]

# حساب عرض وارتفاع الصندوق بشكل ديناميكي
box_width = int(max(ImageDraw.Draw(img).textlength(text, font=font) for text, font in lines + [(name, font_header)]) + (padding * 2))
box_height = int(font_header.getbbox(name)[3] + (padding * 2) + (font_body.getbbox("T")[3] * len(lines)) + (line_spacing * (len(lines))))

# تحديد إحداثيات الصندوق
box_x0 = img_width - box_width - margin
box_y0 = img_height - box_height - margin
box_x1 = img_width - margin
box_y1 = img_height - margin

# --- [الطريقة الموثوقة] تطبيق تأثير الزجاج الشفاف ---

# 1. قص منطقة الصندوق من الخلفية الأصلية
box_crop = img.crop((box_x0, box_y0, box_x1, box_y1))

# 2. طبّق ضبابية على الجزء المقصوص
blurred_box = box_crop.filter(ImageFilter.GaussianBlur(radius=10))

# 3. أنشئ طبقة زجاجية منفصلة وشفافة تماماً
glass_layer = Image.new("RGBA", (box_width, box_height), (255, 255, 255, 0))

# 4. ارسم المستطيل الأبيض شبه الشفاف على هذه الطبقة الجديدة
draw_glass = ImageDraw.Draw(glass_layer)
draw_glass.rectangle(
    (0, 0, box_width, box_height),
    fill=(255, 255, 255, 40),       # طبقة بيضاء خفيفة لمحاكاة الزجاج
    outline=(255, 255, 255, 90),    # إطار أبيض خفيف
    width=2
)

# 5. ادمج الطبقة الضبابية مع الطبقة الزجاجية باستخدام alpha_composite
#    هذه الدالة تضمن دمج الشفافية بشكل صحيح
final_box = Image.alpha_composite(blurred_box, glass_layer)

# 6. الصق الصندوق النهائي (الذي يحتوي على كل التأثيرات) على الصورة الأصلية
img.paste(final_box, (box_x0, box_y0))

# --- كتابة النصوص فوق الصندوق النهائي ---
draw = ImageDraw.Draw(img)
text_color = (15, 15, 15)  # لون نص داكن للوضوح
current_y = box_y0 + padding

# كتابة الاسم
name_width = draw.textlength(name, font=font_header)
draw.text((box_x1 - padding - name_width, current_y), name, font=font_header, fill=text_color)
current_y += font_header.getbbox(name)[3] + line_spacing

# رسم خط فاصل
draw.line([box_x0 + padding, current_y, box_x1 - padding, current_y], fill=(0, 0, 0, 80), width=1)
current_y += line_spacing

# كتابة الإحصائيات
for text, font in lines:
    text_width = draw.textlength(text, font=font)
    draw.text((box_x1 - padding - text_width, current_y), text, font=font, fill=text_color)
    current_y += font.getbbox(text)[3] + line_spacing

# --- حفظ الصورة النهائية ---
output_path = "assets/stats.png"
img.save(output_path, "PNG")

print(f"✅ تم تحديث الصورة '{output_path}' بنجاح مع التأثير الزجاجي الصحيح.")
