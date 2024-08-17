#LIBRARY
from collections import deque
import re
from termcolor import colored
from bs4 import BeautifulSoup
import requests
import urllib.parse

#HEADER TOOLS
print(colored('''
=========================================================
+             +                                         +         
+  ▌ ▌▛▀▖▌    +  Author   : Demrx                       +
+  ▌ ▌▙▄▘▌    +  Version  : 1.0                         +
+  ▌ ▌▌▚ ▌    +  Github   : https://github.com/Demrx    +
+  ▝▀ ▘ ▘▀▀▘  +  Tools    : Lacak email dari URL        +
+    SCAN     +                                         +
=========================================================           
''','light_yellow'))

user_url = str(input(colored('[+] Masukkan URL : ','light_red')))
urls = deque([user_url])
scraped_urls = set()
emails = set()
count = 0
limit = int(input('[+] Masukkan limit pencarian : '))
print('')
print(colored('=========================================================','light_yellow'))
print('')

try:
    while True:
        count += 1
        if count > limit:
            break
        url = urls.popleft()
        scraped_urls.add(url)
        parts = urllib.parse.urlsplit(url)
        base_url = f'{parts.scheme}://{parts.netloc}'
        path = url[:url.rfind('/')+1] if '/' in parts.path else url

        print(colored(f'[{count}] Memproses {url}','light_red'))

        try:
            response = requests.get(url)
        except(requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
            continue

        new_emails = set(re.findall(r'[a-z0-9\.\-+_]+@\w+\.+[a-z\.]+', response.text, re.I))
        emails.update(new_emails)

        soup = BeautifulSoup(response.text, 'html.parser')
        for anchor in soup.find_all('a'):
            link = anchor.attrs['href'] if 'href' in anchor.attrs else ''
            if link.startswith('/'):
                link = base_url + link
            elif not link.startswith('http'):
                link = path + link
            if not link in urls and not link in scraped_urls:
                urls.append(link)

except KeyboardInterrupt:
    print('[-] Closing')

print('\n[!] Done Cuy!')
print(colored(f'\n[!] {len(emails)} Email ditemukan','light_green'))
print(colored('=========================================================','light_yellow'))

for mail in emails:
    print(colored('[:] '+ mail,'light_green'))
print('\n')