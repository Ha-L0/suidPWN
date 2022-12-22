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
            binaries.add(cur_binary + ',' + binaryLink + cur_binary + ',<BLANK>\n')

# take care that already saved escalations do not get deleted when performing an update
saveSet = set()

f = open('binaries', 'r')
fc = f.readlines()
f.close()

for line in fc:
    origLine = line
    line = line.split(',')
    if line[2].strip() != '<BLANK>':
        saveSet.add(origLine)

# create suid file
f = open('binaries', 'w')

for item in binaries:
    itemToSave = 0
    for saveItem in saveSet:
        if item.split(',')[0] == saveItem.split(',')[0]:
            itemToSave = 1

    if itemToSave == 0:
        f.write(item)

for item in saveSet:
    f.write(item)

f.close()
print("[+] Done.")
