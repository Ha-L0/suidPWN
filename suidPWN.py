import httplib2
import base64
import sys
import argparse
import html

programepilog = "example usage: python3 " + sys.argv[0]
programdescription = "Search for suid binaries allowing privilege escalation. "
programdescription += "Tool made by H4&L0. Credits for LPE techniques to https://gtfobins.github.io/"
parser = argparse.ArgumentParser(description=programdescription, epilog=programepilog)
parser.add_argument("-fd", "--find", help="print find suid binaries string", action="store_true", required=False)
parser.add_argument("-f", "--file", help="read suid files result from file", required=False)
parser.add_argument("-c", "--credits", help="show credits", action="store_true", required=False)
args = parser.parse_args()

if args.find:
    find = "\nfind / -type f -a \\( -perm -u+s -o -perm -g+s \\) -exec ls -l {} \\; 2> /dev/null"
    print(find)
    sys.exit(0)

if args.credits:
    creds = "\nWe made this tool while working and different CTF boxes.\n"
    creds += "The reason was to fast identify SUID binaries which are vulnerable to an LPE.\n"
    creds += "We basically just scraped the binaries from the gtfobins website, stored them into a " \
             "text file and wrote this script to check SUID binaries from the target against this text file.\n"
    creds += "All the credits of the local privilege escalation techniques go to gtfobins. These guys are awesome! <3"
    print(creds)
    sys.exit(0)

if args.file:
    f = open(args.file, 'r')
    suidPastes = f.readlines()
    f.close()
else:
    print("Paste your find output. When you are done press ctrl+d")
    suidPastes = sys.stdin.readlines()

f = open('binaries', 'r')
binaries = f.readlines()
f.close()

print()
print()
found = 0
for line in suidPastes:
    line = line.strip()
    line = line.split('/')
    line = line[len(line)-1]
    for binary in binaries:
        binary = binary.split(',')
        binary[0] = binary[0].strip()
        if binary[0] == line:
            if "<BLANK>" in binary[2]:
                http = httplib2.Http()
                status, response = http.request(binary[1])
                if "suid" in response.decode():
                    found = 1
                    print('[+] ' + binary[0])
                    print('[*] Getting ' + binary[0] + ' escalation technique from gtfobins.github.io.')
                    print('>')

                    # extracting SUID content from response (change stuff here if they change the website)
                    tmpResponse = response.decode()
                    tmpResponse = tmpResponse.split('<h2 id="suid" class="function-name">SUID</h2>')[1]
                    tmpResponse = tmpResponse.split('<pre><code>')[1]
                    tmpResponse = tmpResponse.split('</code></pre>')[0]
                    tmpResponse = html.unescape(tmpResponse)
                    printResponse = '>\t' + tmpResponse.replace('\n', '\n>\t')
                    print(printResponse)
                    print('>')
                    print('>\tsource: ' + binary[1])
                    print('')
                    print('')

                    tmpResponse = base64.b64encode(tmpResponse.encode())
                    f = open('binaries', 'r')
                    fc = f.readlines()
                    f.close()
                    ffc = ''
                    for l in fc:
                        if binary[0] == l.split(',')[0]:
                            tmpResponse = str(tmpResponse)
                            tmpResponse = tmpResponse[2:len(tmpResponse)-1]
                            l = l.replace('<BLANK>', tmpResponse)
                        ffc += l
                    f = open('binaries', 'w')
                    f.write(ffc)
                    f.close()
            else:
                found = 1
                print('[+] ' + binary[0])
                f = open('binaries', 'r')
                fc = f.readlines()
                for l in fc:
                    if binary[0] == l.split(',')[0]:
                        b64Command = l.split(',')[2]
                        b64Command = str(base64.b64decode(b64Command))
                        b64Command = b64Command[2:len(b64Command)-1].replace('\\n', '\n')
                        b64Command = '>\t' + b64Command.replace('\n', '\n>\t')
                        print('>')
                        print(b64Command)
                        print('>')
                        print('>')
                        print('>\tsource: ' + binary[1])
                        print('')
                        print('')
                f.close()

if found == 0:
    print("[-] No suid binary identified which can be used for a privilege escalation.")
