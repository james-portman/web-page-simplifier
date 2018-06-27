import requests
import json
from bs4 import BeautifulSoup
import base64
import sys

if len(sys.argv) < 2:
    raise Exception("Please provide a URL")
url = sys.argv[1]

result = requests.get(url)

soup = BeautifulSoup(result.text, 'html.parser')


def inline_src(soup):
    all_script = soup.find_all('script')
    for script in all_script:
        if 'src' in script.attrs:
            if "://" in script.attrs['src']:
                script_src = script.attrs['src']
            else:
                script_src = url + "/" + script.attrs['src']
            script_result = requests.get(script_src)
            script.string = script_result.text
            del(script.attrs['src'])

def inline_img(soup):
    all_imgs = soup.find_all('img')
    for img in all_imgs:
        if 'src' in img.attrs:
            if "://" in img.attrs['src']:
                img_src = img.attrs['src']
            else:
                img_src = url + "/" + img.attrs['src']
            img_result = requests.get(img_src)
            img.attrs['src'] = 'data:image/png;base64,'+ base64.b64encode(img_result.content)

inline_src(soup)
inline_img(soup)

print(soup.prettify())
