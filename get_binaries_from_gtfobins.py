import httplib2
from bs4 import BeautifulSoup, SoupStrainer
import html.parser

binaries = set()

print("[*] Getting binary list from gtfobins...")
http = httplib2.Http()
status, response = http.request('https://github.com/GTFOBins/GTFOBins.github.io/tree/master/_gtfobins')

for link in BeautifulSoup(response, parse_only=SoupStrainer('a'), features="html.parser"):
    if link.has_attr('href'):
        linkOnPage = link['href']
        if linkOnPage.endswith('.md'):
            binaryLink = "https://gtfobins.github.io/gtfobins/"
            cur_binary = linkOnPage.split('/')
            cur_binary = cur_binary[len(cur_binary)-1]
            cur_binary = cur_binary.replace('.md', '')
            binaries.add(cur_binary + ',' + binaryLink + cur_binary)

# create suid file
f = open('binaries', 'w')

for item in binaries:
    f.write(item + '\n')

f.close()
print("[+] Done.")
