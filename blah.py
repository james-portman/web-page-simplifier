import requests
import json
from bs4 import BeautifulSoup

url = "http://www.jamesportman.com"

result = requests.get(url)

soup = BeautifulSoup(result.text, 'html.parser')

# inline scripts:
all_script = soup.find_all('script')
for script in all_script:
    if 'src' in script.attrs:
        script_src = url + script.attrs['src']
        script_result = requests.get(script_src)
        script.string = script_result.text
        del(script.attrs['src'])

print(soup.prettify())
