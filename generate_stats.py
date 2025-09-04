import requests
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
from collections import Counter
import time

USERNAME = "Hussain96o"

def get_github_stats(username):
    """
    يجلب إحصائيات GitHub المتقدمة (الكوميتات، اللغات بالبايت، والمستودعات).
    """
    print("Fetching user and repository data (unauthenticated)...")
    user_url = f"https://api.github.com/users/{username}"
    user_data = requests.get(user_url).json()
    
    public_repos_count = user_data.get("public_repos", 0)
    name = user_data.get("name", username)
    
    repos_url = f"https://api.github.com/users/{username}/repos?type=owner&per_page=100"
    all_repos = []
    page = 1
    while True:
        response = requests.get(f"{repos_url}&page={page}")
        repos = response.json()
        if not repos or not isinstance(repos, list):
            if isinstance(repos, dict) and 'message' in repos and 'API rate limit exceeded' in repos['message']:
                print("❌ API rate limit exceeded while fetching repos. Stats will be incomplete.")
            break
        all_repos.extend(repos)
        page += 1
        
    print(f"Found {len(all_repos)} repositories. Calculating stats...")
    total_commits = 0
    language_bytes = Counter()
    
    for i, repo in enumerate(all_repos):
        repo_name = repo['name']
        print(f"  - Processing repo {i+1}/{len(all_repos)}: {repo_name}")
        
        # 1. جلب اللغات بالبايت (أكثر دقة)
        languages_url = repo.get("languages_url")
        try:
            lang_response = requests.get(languages_url)
            if lang_response.status_code == 200:
                for lang, bytes_count in lang_response.json().items():
                    language_bytes[lang] += bytes_count
        except requests.exceptions.RequestException:
            print(f"    - Could not fetch languages for {repo_name}")

        # 2. جلب إحصائيات الكوميت
        commit_stats_url = f"https://api.github.com/repos/{username}/{repo_name}/stats/contributors"
        # ... (باقي منطق الكوميت لم يتغير)
        for _ in range(3):
            stats_response = requests.get(commit_stats_url)
            if stats_response.status_code == 200:
                contributors = stats_response.json()
                if isinstance(contributors, list):
                    for contributor in contributors:
                        if contributor['author']['login'].lower() == username.lower():
                            total_commits += contributor['total']
                break
            elif stats_response.status_code == 403:
                 print("  - Rate limit likely exceeded. Skipping commit stats for this repo.")
                 break
            time.sleep(2)

    # 3. حساب النسب المئوية لأفضل لغتين
    total_bytes = sum(language_bytes.values())
    top_languages_stats = []
    if total_bytes > 0:
        for lang, count in language_bytes.most_common(2):
            percentage = (count / total_bytes) * 100
            top_languages_stats.append(f"{lang} {percentage:.1f}%")
            
    # معالجة الحالة الفارغة
    if not top_languages_stats:
        top_languages_stats = ["N/A"]
    
    return {
        "name": name,
        "commits": total_commits,
        "repos": public_repos_count,
        "languages": top_languages_stats,
    }

def draw_column(draw, content, x, y, width, height, font_title, font_value):
    title, value = content["title"], str(content["value"])
    cx = x + width / 2
    title_width = draw.textlength(title, font=font_title)
    draw.text((cx - title_width / 2, y + 25), title, font=font_title, fill=(220, 220, 220, 200))
    value_width = draw.textlength(value, font=font_value)
    draw.text((cx - value_width / 2, y + (height / 2) - 10), value, font=font_value, fill=(255, 255, 255))

# --- الجزء الرئيسي من السكريبت ---
if __name__ == "__main__":
    stats = get_github_stats(USERNAME)
    
    img = Image.open("assets/background.png").convert("RGBA")
    
    try:
        font_title = ImageFont.truetype("assets/Poppins-Regular.ttf", size=18)
        font_value = ImageFont.truetype("assets/Poppins-Bold.ttf", size=36)
        font_lang = ImageFont.truetype("assets/Poppins-Regular.ttf", size=16)
    except IOError:
        print("❌ خطأ: لم يتم العثور على ملفات الخطوط. استخدم الخط الافتراضي.")
        font_title, font_value, font_lang = [ImageFont.load_default()] * 3

    # ... باقي كود الرسم لم يتغير ...
    img_width, img_height = img.size
    box_width, box_height = 550, 150
    margin, border_radius = 40, 20
    box_x0, box_y0 = img_width - box_width - margin, img_height - box_height - margin
    box_x1, box_y1 = img_width - margin, img_height - margin
    
    box_crop = img.crop((box_x0, box_y0, box_x1, box_y1))
    blurred_box = box_crop.filter(ImageFilter.GaussianBlur(radius=15))
    glass_layer = Image.new("RGBA", (box_width, box_height), (255, 255, 255, 0))
    draw_glass = ImageDraw.Draw(glass_layer)
    draw_glass.rounded_rectangle((0, 0, box_width, box_height), radius=border_radius, fill=(255, 255, 255, 30), outline=(255, 255, 255, 80), width=2)
    final_box = Image.alpha_composite(blurred_box, glass_layer)
    img.paste(final_box, (box_x0, box_y0))

    draw = ImageDraw.Draw(img)
    column_width = box_width / 3
    
    columns_data = [
        {"title": "Total Commits", "value": stats['commits']},
        {"title": "Public Repos", "value": stats['repos']},
        {"title": "Top Languages", "value": "\n".join(stats['languages'])},
    ]

    draw_column(draw, columns_data[0], box_x0, box_y0, column_width, box_height, font_title, font_value)
    draw_column(draw, columns_data[1], box_x0 + column_width, box_y0, column_width, box_height, font_title, font_value)

    lang_title = columns_data[2]["title"]
    lang_value = columns_data[2]["value"]
    lang_cx = box_x0 + (column_width * 2.5)
    title_width = draw.textlength(lang_title, font=font_title)
    draw.text((lang_cx - title_width / 2, box_y0 + 25), lang_title, font=font_title, fill=(220, 220, 220, 200))
    draw.multiline_text((lang_cx, box_y0 + (box_height / 2) + 5), lang_value, font=font_lang, fill=(255, 255, 255), anchor="mm", align="center")

    line_color = (255, 255, 255, 80)
    line_y0, line_y1 = box_y0 + 20, box_y1 - 20
    draw.line((box_x0 + column_width, line_y0, box_x0 + column_width, line_y1), fill=line_color, width=2)
    draw.line((box_x0 + 2 * column_width, line_y0, box_x0 + 2 * column_width, line_y1), fill=line_color, width=2)

    output_path = "assets/stats.png"
    img.save(output_path, "PNG")
    print(f"✅ تم تحديث الصورة بنجاح مع تصحيح إحصائيات اللغات!")
