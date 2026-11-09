import urllib.request
import re
from PIL import Image

sample_url = "https://lh3.googleusercontent.com/gps-cs-s/ANWiy9RnGXvIQkiC_TxdeD_aK--DxQCDUhP0TqzBnR8PBbSMxYSYyyXp-gb2VHJykQclIDvR8q3EbIZH7QifggJlNq_dQBve6MjnJy7SHK2uwur1KWnDEICWDhdhp_GSsMuzzA9WuwD9=s1600"

req = urllib.request.Request(sample_url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as resp, open("test_sample.jpg", "wb") as f:
    f.write(resp.read())

img = Image.open("test_sample.jpg")
print(f"Downloaded image size: {img.size}, format: {img.format}")
