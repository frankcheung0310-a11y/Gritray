import os
import markdown
import re

# Set directories
POSTS_DIR = 'articles'
DIST_DIR = 'dist'
TEMPLATES_DIR = 'templates'

if not os.path.exists(DIST_DIR):
    os.makedirs(os.path.join(DIST_DIR, 'articles'))

# Load Templates
with open(f'{TEMPLATES_DIR}/index.html', 'r') as f:
    index_tpl = f.read()
with open(f'{TEMPLATES_DIR}/article.html', 'r') as f:
    article_tpl = f.read()

posts_metadata = []

# Process Markdown Articles
for filename in os.listdir(POSTS_DIR):
    if filename.endswith('.md'):
        with open(os.path.join(POSTS_DIR, filename), 'r', encoding='utf-8') as f:
            raw_text = f.read()
            
            # Smartly find the first H1 title
            title_match = re.search(r'^#\s+(.*)', raw_text, re.MULTILINE)
            title = title_match.group(1) if title_match else "Untitled Post"
            
            # Convert the ENTIRE markdown to HTML
            # We keep the title in HTML but can hide it via CSS if needed
            content_html = markdown.markdown(raw_text, extensions=['extra', 'codehilite'])
            
            slug = filename.replace('.md', '.html')
            
            # Fill article template
            full_article = article_tpl.replace('{{TITLE}}', title).replace('{{CONTENT}}', content_html)
            
            with open(os.path.join(DIST_DIR, 'articles', slug), 'w', encoding='utf-8') as out:
                out.write(full_article)
            
            posts_metadata.append({
                'title': title,
                'url': f'articles/{slug}'
            })

# Build Post Feed for Index
feed_html = ""
for post in posts_metadata:
    feed_html += f'''
    <a href="{post['url']}" class="post-entry">
        <div class="post-title">{post['title']}</div>
    </a>'''

# Final Index
final_index = index_tpl.replace('{{POST_FEED}}', feed_html)
with open(os.path.join(DIST_DIR, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(final_index)
