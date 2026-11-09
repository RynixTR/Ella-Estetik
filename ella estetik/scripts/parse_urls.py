import re
import json

with open("photos_html.html", encoding="utf-8") as f:
    content = f.read()

urls = set(re.findall(r'https?://[^\s"\'\)\<]+(?:googleusercontent|ggpht)[^\s"\'\)\<]+', content))
print(f"Total matching URLs: {len(urls)}")
for u in sorted(urls):
    print(u)
