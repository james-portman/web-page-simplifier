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
            img.attrs['src'] = 'data:image/png;base64,' + base64.b64encode(img_result.content).decode("utf-8")

def inline_css(soup):
    """
    <link href="/images/fonts/ukf-icons/styles.css" rel="stylesheet"/>
    """
    all_css = soup.find_all('link', rel="stylesheet")
    for css in all_css:
        if 'href' in css.attrs:
            if "://" in css.attrs['href']:
                css_src = css.attrs['href']
            else:
                css_src = url + "/" + css.attrs['href']
            css_result = requests.get(css_src)
            new_css = soup.new_tag("style")
            new_css.string = css_result.text
            css.insert_before(new_css)
            css.decompose()

inline_src(soup)
inline_img(soup)
inline_css(soup)

print(soup.prettify())
