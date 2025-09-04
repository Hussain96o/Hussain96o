import requests
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
from collections import Counter
import time

USERNAME = "Hussain96o"
# تم حذف GITHUB_TOKEN و HEADERS من هنا

def get_github_stats(username):
    """
    يجلب إحصائيات GitHub المتقدمة (الكوميتات، النجوم، واللغات) بدون توكن.
    """
    print("Fetching user and repository data (unauthenticated)...")
    user_url = f"https://api.github.com/users/{username}"
    # تم حذف headers من طلب requests
    user_data = requests.get(user_url).json()
    
    public_repos_count = user_data.get("public_repos", 0)
    name = user_data.get("name", username)
    
    repos_url = f"https://api.github.com/users/{username}/repos?type=owner&per_page=100"
    all_repos = []
    page = 1
    while True:
        # تم حذف headers من طلب requests
        response = requests.get(f"{repos_url}&page={page}")
        repos = response.json()
        if not repos or not isinstance(repos, list):
            # تحقق من رسالة الخطأ لتحديد ما إذا كان السبب هو تجاوز الحد
            if isinstance(repos, dict) and 'message' in repos:
                print(f"❌ API Error: {repos['message']}")
            break
        all_repos.extend(repos)
        page += 1
        
    print(f"Found {len(all_repos)} repositories. Calculating stats...")
    total_commits = 0
    language_counts = Counter()
    
    for i, repo in enumerate(all_repos):
        repo_name = repo['name']
        print(f"  - Processing repo {i+1}/{len(all_repos)}: {repo_name}")
        
        language = repo.get("language")
        if language:
            language_counts[language] += 1
            
        commit_stats_url = f"https://api.github.com/repos/{username}/{repo_name}/stats/contributors"
        for _ in range(3):
            # تم حذف headers من طلب requests
            stats_response = requests.get(commit_stats_url)
            if stats_response.status_code == 200:
                contributors = stats_response.json()
                if isinstance(contributors, list):
                    for contributor in contributors:
                        if contributor['author']['login'].lower() == username.lower():
                            total_commits += contributor['total']
                break
            elif stats_response.status_code == 403: # خطأ تجاوز الحد
                 print("  - Rate limit likely exceeded. Skipping commit stats for this repo.")
                 break # اخرج من حلقة المحاولات
            time.sleep(2)

    top_languages = [lang for lang, count in language_counts.most_common(3)]
    
    return {
        "name": name,
        "commits": total_commits,
        "repos": public_repos_count,
        "languages": top_languages,
    }

# --- الجزء الرئيسي من السكريبت (لم يتغير) ---
if __name__ == "__main__":
    stats = get_github_stats(USERNAME)
    
    # ... باقي الكود من هنا إلى النهاية يبقى كما هو تمامًا ...
    # ... (لصق باقي الكود الخاص بالرسم هنا) ...
    # --- إعداد الصورة ---
    img = Image.open("assets/background.png").convert("RGBA")
    font_title = ImageFont.truetype("arial.ttf", size=18)
    font_value = ImageFont.truetype("arialbd.ttf", size=36) # خط عريض للقيم
    
    # --- أبعاد الصندوق والأعمدة ---
    img_width, img_height = img.size
    box_width, box_height = 550, 150
    margin = 40
    border_radius = 20
    
    box_x0, box_y0 = img_width - box_width - margin, img_height - box_height - margin
    box_x1, box_y1 = img_width - margin, img_height - margin
    
    # --- تطبيق التأثير الزجاجي (مع زوايا مستديرة) ---
    box_crop = img.crop((box_x0, box_y0, box_x1, box_y1))
    blurred_box = box_crop.filter(ImageFilter.GaussianBlur(radius=15))
    
    # إنشاء طبقة زجاجية شفافة ومستديرة
    glass_layer = Image.new("RGBA", (box_width, box_height), (255, 255, 255, 0))
    draw_glass = ImageDraw.Draw(glass_layer)
    draw_glass.rounded_rectangle(
        (0, 0, box_width, box_height),
        radius=border_radius,
        fill=(255, 255, 255, 30),
        outline=(255, 255, 255, 80),
        width=2
    )
    
    final_box = Image.alpha_composite(blurred_box, glass_layer)
    img.paste(final_box, (box_x0, box_y0))

    # --- رسم الأعمدة والمحتوى ---
    draw = ImageDraw.Draw(img)
    column_width = box_width / 3
    
    # محتوى الأعمدة
    columns_data = [
        {"title": "Total Commits", "value": stats['commits']},
        {"title": "Public Repos", "value": stats['repos']},
        {"title": "Top Languages", "value": "\n".join(stats['languages'])},
    ]

    # تغيير خط اللغات ليكون أصغر
    font_lang = ImageFont.truetype("arial.ttf", size=16)

    # العمود الأول (Commits)
    draw_column(draw, columns_data[0], box_x0, box_y0, column_width, box_height, font_title, font_value)

    # العمود الثاني (Repos)
    draw_column(draw, columns_data[1], box_x0 + column_width, box_y0, column_width, box_height, font_title, font_value)

    # العمود الثالث (Languages) - يتم رسمه بشكل خاص لأنه نص متعدد الأسطر
    lang_title = columns_data[2]["title"]
    lang_value = columns_data[2]["value"]
    lang_cx = box_x0 + (column_width * 2.5) # مركز العمود الثالث
    
    title_width = draw.textlength(lang_title, font=font_title)
    draw.text((lang_cx - title_width / 2, box_y0 + 25), lang_title, font=font_title, fill=(220, 220, 220, 200))
    
    # رسم اللغات في المنتصف
    draw.multiline_text(
        (lang_cx, box_y0 + (box_height / 2) + 5),
        lang_value,
        font=font_lang,
        fill=(255, 255, 255),
        anchor="mm", # توسيط أفقي وعمودي
        align="center"
    )

    # رسم الخطوط الفاصلة
    line_color = (255, 255, 255, 80)
    line_y0, line_y1 = box_y0 + 20, box_y1 - 20
    draw.line((box_x0 + column_width, line_y0, box_x0 + column_width, line_y1), fill=line_color, width=2)
    draw.line((box_x0 + 2 * column_width, line_y0, box_x0 + 2 * column_width, line_y1), fill=line_color, width=2)

    # --- حفظ الصورة ---
    output_path = "assets/stats.png"
    img.save(output_path, "PNG")
    print(f"✅ تم تحديث الصورة بنجاح بالتصميم الجديد!")
