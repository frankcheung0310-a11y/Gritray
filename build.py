import os
import markdown
import re
import shutil

# --- Configuration ---
POSTS_DIR = 'articles'      # Where you put your .md files
DIST_DIR = 'dist'           # Where Cloudflare serves from
TEMPLATES_DIR = 'templates' # Where your HTML templates are
ASSETS_DIR = 'assets'       # 你的图片仓库文件夹

# Ensure output directories exist
if not os.path.exists(DIST_DIR):
    os.makedirs(os.path.join(DIST_DIR, 'articles'), exist_ok=True)
elif not os.path.exists(os.path.join(DIST_DIR, 'articles')):
    os.makedirs(os.path.join(DIST_DIR, 'articles'), exist_ok=True)

# Load Templates
try:
    with open(f'{TEMPLATES_DIR}/index.html', 'r', encoding='utf-8') as f:
        index_tpl = f.read()
    with open(f'{TEMPLATES_DIR}/article.html', 'r', encoding='utf-8') as f:
        article_tpl = f.read()
except FileNotFoundError as e:
    print(f"Error: Template files not found in {TEMPLATES_DIR} folder.")
    exit(1)

posts_metadata = []

# --- Process Markdown Articles ---
if not os.path.exists(POSTS_DIR):
    os.makedirs(POSTS_DIR)
    print(f"Created {POSTS_DIR} directory. Please add .md files there.")

for filename in os.listdir(POSTS_DIR):
    if filename.endswith('.md'):
        file_path = os.path.join(POSTS_DIR, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            raw_text = f.read()
            
            # 1. Extract the first H1 title (e.g., # My Title)
            title_match = re.search(r'^#\s+(.*)', raw_text, re.MULTILINE)
            if title_match:
                title = title_match.group(1).strip()
                # 2. Remove the first H1 line to avoid double titles in article.html
                body_md = re.sub(r'^#\s+.*', '', raw_text, count=1, flags=re.MULTILINE)
            else:
                title = "Untitled Post"
                body_md = raw_text
            
            # 3. Convert Markdown to HTML with advanced extensions
            content_html = markdown.markdown(body_md, extensions=['extra', 'nl2br', 'sane_lists'])
            
            # Generate the output filename (slug)
            slug = filename.replace('.md', '.html')
            
            # 4. Fill article template
            full_article = article_tpl.replace('{{TITLE}}', title).replace('{{CONTENT}}', content_html)
            
            # Save the individual article page
            output_path = os.path.join(DIST_DIR, 'articles', slug)
            with open(output_path, 'w', encoding='utf-8') as out:
                out.write(full_article)
            
            # Store metadata for the index page link list
            posts_metadata.append({
                'title': title,
                'url': f'articles/{slug}',
                'filename': filename 
            })

# Build Post Feed for Index
feed_html = ""
for post in posts_metadata:
    absolute_url = f"/{post['url']}"
    feed_html += f'''
    <a href="{absolute_url}" class="post-entry">
        <div class="post-title">{post['title']}</div>
    </a>'''

# 5. Final Index Assembly
final_index = index_tpl.replace('{{POST_FEED}}', feed_html)
with open(os.path.join(DIST_DIR, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(final_index)

print(f"Successfully built {len(posts_metadata)} articles into {DIST_DIR}/")


# ─── 核心修复：同步所有的静态资源与整个图片文件夹 ───

# 1. 复制根目录的独立静态文件
static_files = ['favicon.png', 'og-image.png']
for file in static_files:
    if os.path.exists(file):
        shutil.copy(file, os.path.join(DIST_DIR, file))
        print(f"Successfully synced file: {file}")

# 2. 复制整个 assets 文件夹到 dist/assets
dist_assets_path = os.path.join(DIST_DIR, ASSETS_DIR)

# 如果 dist 里已经有老 assets 文件夹，先删掉它保证无缝更新
if os.path.exists(dist_assets_path):
    shutil.rmtree(dist_assets_path)

# 如果本地存在 assets 文件夹，将其完整复制过去
if os.path.exists(ASSETS_DIR):
    shutil.copytree(ASSETS_DIR, dist_assets_path)
    print(f"Successfully synced entire folder: {ASSETS_DIR} -> {dist_assets_path}")
else:
    print(f"Warning: Local '{ASSETS_DIR}' folder not found. No images were copied.")
