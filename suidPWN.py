import httplib2
import sys
import argparse

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
            http = httplib2.Http()
            status, response = http.request(binary[1])
            if "suid" in response.decode():
               found = 1
               print('[+] ' + binary[0])
               print('\t' + binary[1])

if found == 0:
    print("[-] No suid binary identified which can be used for a privilege escalation.")

