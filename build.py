import os
import markdown
import re
import shutil
import subprocess
from datetime import datetime

# --- Configuration ---
POSTS_DIR = 'articles'      # Where you put your .md files
DIST_DIR = 'dist'           # Where Cloudflare serves from
TEMPLATES_DIR = 'templates' # Where your HTML templates are
ASSETS_DIR = 'assets'       # 你的本地静态图片文件夹

# --- Helper Function: Extract Git Commit Date ---
def get_git_commit_date(file_path):
    """
    通过 Git 命令精准获取某个文件在 GitHub 上的最后一次提交日期
    """
    try:
        # 执行 git log 命令，获取该文件最后一次提交的 YYYY-MM-DD 格式日期
        date_str = subprocess.check_output(
            ["git", "log", "-1", '--format=%cd', '--date=format:%Y-%m-%d', '--', file_path]
        ).decode('utf-8').strip()
        
        return date_str if date_str else None
    except Exception:
        # 降级兜底：万一环境没有 Git 命令行工具，返回 None
        return None

# 1. 确保核心输出目录和文章子目录安全存在
os.makedirs(DIST_DIR, exist_ok=True)
os.makedirs(os.path.join(DIST_DIR, 'articles'), exist_ok=True)

# Load Templates
try:
    with open(os.path.join(TEMPLATES_DIR, 'index.html'), 'r', encoding='utf-8') as f:
        index_tpl = f.read()
    with open(os.path.join(TEMPLATES_DIR, 'article.html'), 'r', encoding='utf-8') as f:
        article_tpl = f.read()
except FileNotFoundError as e:
    print(f"❌ 错误: 找不到 {TEMPLATES_DIR} 文件夹中的模板文件 (index.html / article.html)")
    exit(1)

posts_metadata = []

# --- Process Markdown Articles ---
if not os.path.exists(POSTS_DIR):
    os.makedirs(POSTS_DIR)
    print(f"📁 已自动创建 {POSTS_DIR} 目录。请将你的 .md 文章放进去。")

# 遍历并编译文章
if os.path.exists(POSTS_DIR):
    for filename in os.listdir(POSTS_DIR):
        if filename.endswith('.md'):
            file_path = os.path.join(POSTS_DIR, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                raw_text = f.read()
                
            # --- 核心新增：解析顶部的 Front Matter 元数据 ---
            is_pinned = False
            post_date = None # 初始化为 None，方便后续判断是否需要使用 Git 时间
            
            # 检查是否存在用 --- 包裹的头部元数据
            front_matter_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', raw_text, re.DOTALL | re.MULTILINE)
            
            if front_matter_match:
                meta_text = front_matter_match.group(1)
                # 剥离掉头部元数据，留下真正的 Markdown 正文供后续解析
                body_md_raw = raw_text[front_matter_match.end():]
                
                # 提取 pinned 状态
                pinned_match = re.search(r'^pinned:\s*(true|false)', meta_text, re.MULTILINE)
                if pinned_match:
                    is_pinned = pinned_match.group(1) == 'true'
                
                # 提取 date 日期
                date_match = re.search(r'^date:\s*([\d-]+)', meta_text, re.MULTILINE)
                if date_match:
                    post_date = date_match.group(1).strip()
            else:
                body_md_raw = raw_text

            # --- 自动化时间戳感知核心：若 Front Matter 没写日期，则自动抓取 Git 真实提交时间 ---
            if not post_date:
                git_date = get_git_commit_date(file_path)
                if git_date:
                    post_date = git_date
                    print(f"🕒 自动抓取 Git 时间 -> [{filename}]: {post_date}")
                else:
                    # 终极防线：如果既没写 Front Matter，又没提交过 Git（本地新文件），则用当天系统时间
                    post_date = datetime.now().strftime('%Y-%m-%d')
                    print(f"🌱 本地新文章临时赋予今日时间 -> [{filename}]: {post_date}")

            # 提取第一个 H1 标题
            title_match = re.search(r'^#\s+(.*)', body_md_raw, re.MULTILINE)
            if title_match:
                title = title_match.group(1).strip()
                # 移除第一个 H1 行避免单页双标题
                body_md = re.sub(r'^#\s+.*', '', body_md_raw, count=1, flags=re.MULTILINE)
            else:
                title = "Untitled Post"
                body_md = body_md_raw
                
            # 解析 Markdown 为 HTML
            content_html = markdown.markdown(body_md, extensions=['extra', 'nl2br', 'sane_lists'])
            slug = filename.replace('.md', '.html')
            
            # 填充单篇文章模板（核心修改：同时支持替换 {{TITLE}}, {{CONTENT}} 和注释包裹的时间戳坑）
            full_article = article_tpl.replace('{{TITLE}}', title).replace('{{CONTENT}}', content_html)
            
            # 精准寻找并擦除你模板里写好的时间占位符注释，将其点亮为真实的 post_date
            full_article = full_article.replace('<!-- {{COMMIT_DATE}} -->', post_date)
            
            output_path = os.path.join(DIST_DIR, 'articles', slug)
            with open(output_path, 'w', encoding='utf-8') as out:
                out.write(full_article)
                
            # 将排序所需的关键资产压入队列
            posts_metadata.append({
                'title': title,
                'url': f'articles/{slug}',
                'date': post_date,
                'pinned': is_pinned
            })

# ─── 核心算法：双重加权秩序排序 ───
# 优先依据 pinned 状态（True 排前面），如果状态相同，再依据日期 date 倒序（最新排前面）
posts_metadata.sort(key=lambda x: (x['pinned'], x['date']), reverse=True)


# 构建主页的文章列表 Feed
feed_html = ""
for post in posts_metadata:
    absolute_url = f"/{post['url']}"
    
    # 如果是钉选文章，你可以选择在前端标题前加个标志，不需要的话直接把 {pin_tag} 删掉即可
    pin_tag = '<span style="color:#d9383a; font-size:1rem; margin-right:0.6rem; font-family:sans-serif; font-weight:bold; vertical-align:middle;">📌 PINNED</span>' if post['pinned'] else ''
    
    feed_html += f'''
    <a href="{absolute_url}" class="post-entry">
        <div class="post-title">{pin_tag}{post['title']} <span style="float:right; font-size:0.9rem; color:#888;">{post['date']}</span></div>
    </a>'''

# 2. 核心拼装主页并写入 dist/index.html
final_index = index_tpl.replace('{{POST_FEED}}', feed_html)
with open(os.path.join(DIST_DIR, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(final_index)

print(f"✨ 成功：已将 {len(posts_metadata)} 篇文章按照【置顶与时间流】完美写入 {DIST_DIR}/index.html")


# ─── 静态资源全自动鲁棒同步引擎 ───

# 1. 复制根目录独立的静态文件
static_files = ['favicon.png', 'og-image.png']
for file in static_files:
    if os.path.exists(file):
        shutil.copy(file, os.path.join(DIST_DIR, file))
        print(f"  -> 成功同步独立文件: {file}")

# 2. 安全同步整个 assets 文件夹
dist_assets_path = os.path.join(DIST_DIR, ASSETS_DIR)

if os.path.exists(ASSETS_DIR):
    os.makedirs(dist_assets_path, exist_ok=True)
    for item in os.listdir(ASSETS_DIR):
        s = os.path.join(ASSETS_DIR, item)
        d = os.path.join(dist_assets_path, item)
        if os.path.isdir(s):
            if os.path.exists(d):
                shutil.rmtree(d)
            shutil.copytree(s, d)
        else:
            shutil.copy2(s, d)
    print(f"⚡️ 成功：整个 '{ASSETS_DIR}' 静态图库已完美无缝同步至 -> {dist_assets_path}")
else:
    print(f"⚠️ 警告：未在项目根目录下找到 '{ASSETS_DIR}' 文件夹，请检查大小写是否全小写！")

try:
    with open(os.path.join(TEMPLATES_DIR, 'sandbox.html'), 'r', encoding='utf-8') as sf:
        sandbox_content = sf.read()
    with open(os.path.join(DIST_DIR, 'sandbox.html'), 'w', encoding='utf-8') as df:
        df.write(sandbox_content)
except FileNotFoundError:
    print("ℹ️ 提示：未在 templates 文件夹中找到 sandbox.html，跳过同步该文件。")
