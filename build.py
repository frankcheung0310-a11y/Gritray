import os
import markdown
from datetime import datetime

# 1. Setup paths
ARTICLES_DIR = 'articles'
DIST_DIR = 'dist' # Cloudflare will point here
TEMPLATE_INDEX = 'templates/index.html'
TEMPLATE_ARTICLE = 'templates/article.html'

if not os.path.exists(DIST_DIR):
    os.makedirs(os.path.join(DIST_DIR, 'articles'))

# 2. Process all Markdown files
posts = []
for filename in os.listdir(ARTICLES_DIR):
    if filename.endswith('.md'):
        with open(os.path.join(ARTICLES_DIR, filename), 'r') as f:
            content = f.read()
            html_content = markdown.markdown(content)
            title = content.split('\n')[0].replace('# ', '') # Use first line as title
            
            # Generate clean filename
            slug = filename.replace('.md', '.html')
            
            # Fill article template
            with open(TEMPLATE_ARTICLE, 'r') as t:
                article_html = t.read().replace('{{TITLE}}', title).replace('{{CONTENT}}', html_content)
            
            with open(os.path.join(DIST_DIR, 'articles', slug), 'w') as out:
                out.write(article_html)
            
            posts.append({
                'title': title,
                'slug': f'articles/{slug}',
                'date': datetime.now().strftime('%b %d, %Y')
            })

# 3. Build Index.html
post_links = ""
for post in posts:
    post_links += f'''
    <a href="{post['slug']}" class="post-entry">
        <div class="post-date">{post['date']}</div>
        <div class="post-title">{post['title']}</div>
    </a>'''

with open(TEMPLATE_INDEX, 'r') as t:
    index_html = t.read().replace('{{POST_FEED}}', post_links)

with open(os.path.join(DIST_DIR, 'index.html'), 'w') as out:
    out.write(index_html)
