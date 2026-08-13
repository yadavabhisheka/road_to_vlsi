# OverTheWire: Bandit — Full Writeup

My walkthrough of the [OverTheWire Bandit](https://overthewire.org/wargames/bandit/) wargame, done as part of my Linux prep for [Road to VLSI](https://github.com/yadavabhisheka/ROAD_TO_VLSI)

Each level includes: the goal, the exact command(s) I used, the password I found, and what the level was actually testing.

---

## Level 0

**Goal:**
Log into the game using SSH. Host: `bandit.labs.overthewire.org`, Port: `2220`, Username: `bandit0`, Password: `bandit0`.

**Command(s) used:**
```bash
ssh -p 2220 bandit0@bandit.labs.overthewire.org
```

**Password found:**
```
bandit0
```
*(this is the starting password given by the challenge itself, not one found by solving anything)*

**Understanding:**
This level is just about setting up the connection correctly. By default `ssh` connects on port 22, but Bandit runs its SSH service on a non-standard port (`2220`) — so the `-p` flag is required to override the default. The general syntax is `ssh -p <port> <username>@<host>`. Once authenticated with the given password, you land in a shell on the Bandit game server as user `bandit0`, ready to start Level 1.

---

## Level 0 → Level 1

**Goal:**
The password for the next level is stored in a file called `readme` located in the home directory. Use this password to log into `bandit1` using SSH.

**Command(s) used:**
```bash
cat readme
```

**Password found:**
```
6y2kwnwK6grgvwvpvLaa2T1cpFEKOhNR
```

**Understanding:**
`cat` (short for "concatenate") reads a file's contents and prints them straight to standard output. Since `readme` was a small file, `cat` was enough here — no pager like `less` or `more` was needed. Landing in the home directory by default after SSH login meant no `cd` or path was needed; running `cat readme` directly found the file. This password is then used to SSH in as `bandit1` on port 2220, the same way as Level 0.

---

## Level 1 → Level 2

**Goal:**
The password for the next level is stored in a file called `-` located in the home directory.

**Command(s) used:**
```bash
cat ./-
```

**Password found:**
```
PK8fYLZg2hnHSz83plBL1iEPKdD3QToB
```

**Understanding:**
The tricky part here is the filename itself: `-`. In most shell commands, a single dash at the start of an argument is interpreted as a flag/option, not a filename — so running `cat -` doesn't open the file, it tells `cat` to read from standard input instead (and the terminal just hangs waiting for input). To force the shell to treat `-` as a literal filename, you prefix it with a path so it no longer starts with a dash: `./-` means "the file named `-` in the current directory." This is a common gotcha with dashed/special filenames, and `./` is the standard fix.

---

## Level 2 → Level 3

**Goal:**
The password for the next level is stored in a file called `--spaces in this filename--` located in the home directory.

**Command(s) used:**
```bash
ls
cat ./--spaces\ in\ this\ filename--
```

**Password found:**
```
7ZZ2LFrykP2zEyvBl4m3clcL7tGYJPME
```

**Understanding:**
This combines the previous lesson (leading `--` needs `./` so it isn't read as a flag) with a new one: spaces inside a filename. The shell normally treats a space as an argument separator — so `filename` becomes several separate arguments if it has unescaped spaces in it. To tell the shell "this space is part of the filename, not a separator," each space is escaped with a backslash (`\ `).

**Mistake made along the way:** First tried `cat ./--spaces\in\this\filename` — escaping around the words but not the actual spaces, and missing the trailing `--`. That collapsed into `--spacesinthisfilename` with no spaces at all, so the shell looked for a file that didn't exist (`No such file or directory`). Running `ls` first to see the exact filename, then carefully escaping only the space characters (`\ ` between each word) and keeping the full name including the trailing `--`, fixed it: `cat ./--spaces\ in\ this\ filename--`.

**Takeaway:** When a filename has unusual characters, wrapping it in quotes (`cat "./--spaces in this filename--"`) is often simpler and less error-prone than escaping every individual character — worth remembering for future levels.

---

## Level 3 → Level 4

**Goal:**
The password for the next level is stored in a hidden file in the `inhere` directory.

**Command(s) used:**
```bash
cd inhere
ls -a
cat ./...Hiding-From-You
```

**Password found:**
```
xzTXq1rDJQVVAzdv5cHq1TQytTWufAMq
```

**Understanding:**
"Hidden" files in Linux are just files whose name starts with a dot (`.`) — this is a naming convention, not a real permission or protection. The regular `ls` doesn't show them, so `-a` ("all") is needed to reveal dotfiles along with normal ones. Inside `inhere`, the hidden file was named `...Hiding-From-You` — the leading dots make it hidden, and the rest is just a (slightly cheeky) filename. `cat ./...Hiding-From-You` reads it directly, same as any normal file once you know the exact name.

---

## Level 4 → Level 5

**Goal:**
The password for the next level is stored in the only human-readable file in the `inhere` directory.

**Command(s) used:**
```bash
cd inhere
file ./-file0*
cat ./-file07
```

**Password found:**
```
6C7h9GD8M6ai5nr7wo1RonrzFjj9yIrG
```

**Understanding:**
This level has 10 files, all named `-fileXX`, so eyeballing which one is "human-readable" isn't possible from the name alone — the `file` command is needed to identify file *type* by inspecting its actual content/signature, not just its extension. Since all filenames start with `-`, running `file` on them needs the same `./` fix as earlier levels (otherwise `-fileXX` gets parsed as options). Using a wildcard, `file ./-file0*`, ran the type-check on all ten at once. The output showed most were generic `data`, one was an `OpenPGP Secret Key`, one was `Non-ISO extended-ASCII text`, and `-file07` was plain `ASCII text` — the only genuinely human-readable one. `cat ./-file07` then printed the password.

---

## Level 5 → Level 6

**Goal:**
The password for the next level is stored somewhere under the `inhere` directory and has all of the following properties: human-readable, 1033 bytes in size, not executable.

**Command(s) used:**
```bash
cd inhere
find -type f -size 1033c -not -executable
cat ./maybehere07/.file2
```

**Password found:**
```
pXa26xhMWaC2SvDotA4r9EgZkulOeSBW
```

**Understanding:**
This level nests the password inside numbered subdirectories (`maybehere00` through `maybehere19`), so manually checking each one isn't practical. `find` is built exactly for this kind of search-by-criteria task: `-type f` restricts results to regular files (skipping directories), `-size 1033c` matches an exact size of 1033 bytes (the `c` suffix means bytes, not blocks), and `-not -executable` excludes any file with the executable permission bit set. Combining all three flags narrowed the entire directory tree down to one match: `./maybehere07/.file2` — itself a hidden file (leading dot) inside one of the numbered folders. `cat` then printed the password directly.

---

## Level 6 → Level 7

**Goal:**
The password for the next level is stored somewhere on the server and has all of the following properties: owned by user `bandit7`, owned by group `bandit6`, 33 bytes in size.

**Command(s) used:**
```bash
find / -user bandit7 -group bandit6 -size 33c 2>/dev/null
cat /var/lib/dpkg/info/bandit7.password
```

**Password found:**
```
Bmnnvf82KzQlfxgAI2d1zYbr1u9pr3E3
```

**Understanding:**
Unlike the previous level, this password could be anywhere on the whole filesystem, not just under a known folder — so the search starts at `/` (the root) instead of the current directory. Three filters narrow it down: `-user bandit7` matches files owned by that user, `-group bandit6` matches files owned by that group, and `-size 33c` matches an exact size of 33 bytes. Because this searches the entire filesystem as a low-privilege user, `find` hits many directories it isn't allowed to read and prints a "Permission denied" error for each — `2>/dev/null` redirects file descriptor 2 (stderr) to `/dev/null`, a null device that discards output, so only real matches show up. This narrowed the whole server down to one file: `/var/lib/dpkg/info/bandit7.password`, which `cat` then printed.

---

## Level 7 → Level 8

**Goal:**
The password for the next level is stored in the file `data.txt` next to the word `millionth`.

**Command(s) used:**
```bash
cat data.txt | grep "millionth"
```

**Password found:**
```
VR1ljMayciFxbnUokuQmJFw6QC9VKtub
```

**Understanding:**
`data.txt` here has many lines, each a word followed by some value — too many to scroll through manually. The `|` (pipe) sends the output of one command as input to the next, so `cat data.txt | grep "millionth"` feeds the entire file's contents into `grep`, which searches line-by-line for a given pattern — in this case, the literal text "millionth" — and prints only the matching line. This found the one line containing the word `millionth` along with the password sitting right next to it.

*(Note: `grep "millionth" data.txt` — passing the filename directly to `grep` instead of piping through `cat` — does the same thing with one less process; this is sometimes called a "useless use of cat," but both work and are common to see.)*

---

## Level 8 → Level 9

**Goal:**
The password for the next level is stored in the file `data.txt` and is the only line of text that occurs only once.

**Command(s) used:**
```bash
sort data.txt | uniq -u
```

**Password found:**
```
EjmOSvuAu7sGAHqHVcBDPirRe9T03kxl
```

**Understanding:**
`uniq` reports or filters out repeated lines, but it only works correctly on **adjacent** duplicate lines — so the file needs to be sorted first, which is why it's piped through `sort` before reaching `uniq`. The `-u` flag tells `uniq` to print only lines that are unique — i.e., ones that appear exactly once with no duplicates anywhere in the (now-sorted) file. Since the file was mostly repeated lines of junk data with just one truly one-off line (the password), `sort data.txt | uniq -u` isolated that single line directly.

---

## Level 9 → Level 10

**Goal:**
The password for the next level is stored in the file `data.txt`, in one of the few human-readable strings, preceded by several `=` characters.

**Command(s) used:**
```bash
strings data.txt | grep "="
```

**Password found:**
```
B0s2khmbT9u0geKuOoVGW3JZKhndE3BG
```

**Understanding:**
`data.txt` here is mostly binary/garbage data (not plain text), so a normal `cat` would print unreadable characters. `strings` scans a file and pulls out only the sequences that look like printable, human-readable text — filtering the noise down to legible fragments. Since the goal specifically said the password was preceded by several `=` characters, piping through `grep "="` narrowed the (still fairly long) `strings` output straight down to the one line matching that pattern: `========== B0s2khmbT9u0geKuOoVGW3JZKhndE3BG`.

---

## Level 10 → Level 11

**Goal:**
The password for the next level is stored in the file `data.txt`, which contains base64 encoded data.

**Command(s) used:**
```bash
base64 -d data.txt
```

**Password found:**
```
pYfOY6HwUsDj5rL9UvyhU7MCmv8vN5Ro
```

**Understanding:**
Base64 is an encoding scheme that represents binary data using only printable ASCII characters (letters, digits, `+`, `/`, and `=` padding) — it's used to safely transmit or store data in text-only formats, not for encryption/security. `data.txt` contained the password in this encoded form. The `base64` command handles both encoding and decoding; the `-d` flag tells it to decode rather than encode. Running `base64 -d data.txt` reversed the encoding and printed the original plain-text line, `The password is <password>`.

---

## Level 11 → Level 12

**Goal:**
The password for the next level is stored in the file `data.txt`, where all lowercase (a-z) and uppercase (A-Z) letters have been rotated by 13 positions.

**Command(s) used:**
```bash
cat data.txt | tr "A-Za-z" "N-ZA-Mn-za-m"
```

**Password found:**
```
GROozWPO8QyN0mGrjUkID0WCYkZiQxrN
```

**Understanding:**
This is a classic ROT13 cipher — each letter is shifted 13 places through the alphabet (and since the alphabet has 26 letters, applying ROT13 twice returns the original text). `tr` translates characters: it takes two character sets and maps each character in the first set to the corresponding character in the second, position by position. `"A-Za-z"` is the full alphabet (uppercase then lowercase), and `"N-ZA-Mn-za-m"` is that same alphabet rotated by 13 — `N` maps to where `A` was, `A` maps to where `N` was, and so on. Piping `data.txt` through this translation decoded the ROT13 text back to plain English, revealing the password.

*(Note: `tr [N-ZA-M n-za-m]` — an earlier attempt using square brackets and a space instead of two properly quoted, comma-free character-range strings — is invalid syntax for `tr` and produced garbled output. `tr` expects two matching character sets as separate arguments, not one bracketed expression.)*

---

## Level 12 → Level 13

**Goal:**
The password for the next level is stored in the file `data.txt`, which is a hexdump of a file that has been repeatedly compressed. It's recommended to create a working directory under `/tmp` using `mktemp -d`, then copy the datafile there.

**Command(s) used:**
```bash
mktemp -d
cp data.txt /tmp/tmp.ZzlMSUTuSC
cd /tmp/tmp.ZzlMSUTuSC

xxd -r data.txt > data
file data                    # gzip compressed data
mv data data.gz
gzip -d data.gz

file data                    # bzip2 compressed data
mv data data.bz2
bzip2 -d data.bz2

file data                    # gzip compressed data
mv data data.gz
gzip -d data.gz

file data                    # POSIX tar archive
tar -xf data

file data5.bin               # POSIX tar archive
tar -xf data5.bin

file data6.bin                # bzip2 compressed data
mv data6.bin data6.bin.bz2
bzip2 -d data6.bin.bz2

file data6.bin                # POSIX tar archive
tar -xf data6.bin

file data8.bin                # gzip compressed data
mv data8.bin data8.bin.gz
gzip -d data8.bin.gz

file data8.bin                # ASCII text
cat data8.bin
```

**Password found:**
```
qQYQiHOBPR8zR61qxYqX45quvihF2uzk
```

**Understanding:**
This level layers several concepts together. `mktemp -d` creates a fresh, uniquely-named temporary directory (safer than picking a name manually, since a guessable name could collide with another user's files) — the datafile is copied there to work in isolation from the home directory. `data.txt` itself is a **hexdump**, a text representation of raw binary data as hexadecimal byte pairs (this is how binary data can be safely viewed/edited as plain text). `xxd -r` reverses this — the `-r` flag means "reverse," converting the hex text back into the original binary bytes, redirected (`>`) into a new file called `data`.

From there, the file had been compressed **repeatedly, with different tools each time** — the actual compression method isn't visible from the filename alone (all generically named `data`), so `file` is run after every step to identify what kind of file it currently is. Based on what `file` reports, the matching decompression tool is used: `gzip -d` for gzip data, `bzip2 -d` for bzip2 data, `tar -xf` to extract a tar archive. Since `gzip`/`bzip2` expect a specific file extension to work correctly, each file is `mv`'d to add the right extension (`.gz`, `.bz2`) immediately before decompressing it. This repeats — gzip → bzip2 → gzip → tar → tar → bzip2 → tar → gzip — until `file` finally reports plain `ASCII text`, at which point `cat` reveals the password directly.

**Takeaway:** When a file's true type is unknown or its compression history is hidden, `file` is the tool to identify it at each stage — don't assume from the filename or extension.

---

## Level 13 → Level 14

**Goal:**
The password for the next level is stored in `/etc/bandit_pass/bandit14` and can only be read by user `bandit14`. This level doesn't give the next password directly — instead it gives a private SSH key that must be used to log in as `bandit14`.

**Command(s) used:**
```bash
# on bandit13
cat sshkey.private

# transferred the key to the local machine, then on the local machine:
ssh -i sshkey.private bandit14@bandit.labs.overthewire.org -p 2220

# once logged in as bandit14:
cat /etc/bandit_pass/bandit14
```

**Password found:**
```
aaWecNkG4FhxJQxz07uiwzVP6bJiYS65
```

**Understanding:**
Unlike every level before this, authentication here is by **SSH key pair** instead of a password — a standard, more secure alternative to typing a password each time. `bandit13`'s home directory contained `sshkey.private`, the private half of a key pair already set up to authenticate as `bandit14`. The `-i` flag on `ssh` tells it to use a specific identity (key) file for authentication instead of prompting for a password: `ssh -i sshkey.private bandit14@<host> -p 2220`.

The key first needed to be moved off the `bandit13` account onto the machine actually running the `ssh` command. A direct `scp` from inside the Bandit server back to itself failed, because OverTheWire blocks SSH connections originating from `localhost` back to itself (to conserve server resources) — the error explicitly said so: *"Connecting from localhost is blocked to conserve resources."* Instead, the key's contents were copied out to the local machine directly (e.g. via `cat` and saving the output), and the `ssh -i` command was then run from the local machine instead of from within the Bandit server itself.

One more gotcha: the first `ssh -i sshkey.private bandit14@...` attempt from the local machine used the default SSH port (22) and failed, since Bandit only listens on port 2220 — adding `-p 2220` fixed it. Once inside as `bandit14`, `cat /etc/bandit_pass/bandit14` printed the password directly (readable because this session is now authenticated *as* `bandit14`, matching the file's read permission).

---

## Level 14 → Level 15

**Goal:**
The password for the next level can be retrieved by submitting the password of the current level to port 30000 on localhost.

**Command(s) used:**
```bash
telnet localhost 30000
```
*(then typed the bandit14 password and pressed Enter, once connected)*

**Password found:**
```
pbLYuZtTg4MgaqfJx8jbA9gKKGqM68A7
```

**Understanding:**
This level introduces raw network interaction instead of file-reading. `localhost` (also `127.0.0.1`) always refers to "this machine" — connecting to it doesn't leave the server. A **port** is a numbered endpoint a program listens on to accept connections; here, something is listening on port 30000 specifically for this challenge. `telnet` opens a plain, unencrypted interactive text connection to a given host and port — after `telnet localhost 30000`, the connection was live and whatever text was typed next was sent straight to the listening program. Typing the current password (`bandit14`'s) and pressing Enter caused the service to check it, print `Correct!`, and return the password for `bandit15` before closing the connection.

---

## Level 15 → Level 16

**Goal:**
The password for the next level can be retrieved by submitting the password of the current level to port 30001 on localhost, using SSL/TLS encryption.

**Command(s) used:**
```bash
openssl s_client -connect localhost:30001
```
*(then typed the bandit15 password and pressed Enter, once the handshake finished)*

**Password found:**
```
kS0Hf0u5HiXFwKMKFqXvPdOTNGGa0X8V
```

**Understanding:**
Same idea as the previous level, but this port requires an **encrypted** connection (SSL/TLS) rather than plain text — `telnet` can't do that, so `openssl s_client` is used instead, acting as an SSL/TLS client. Connecting triggers a full handshake: the server presents its certificate (here a self-signed one, `CN=SnakeOil` — a well-known placeholder name for test/demo certificates), OpenSSL verifies it and reports `verify error:num=18:self-signed certificate` (expected, not fatal — self-signed just means no external authority vouches for it), and a secure encrypted channel is established. All the certificate details, session ticket, and cipher info that print are just this setup process, not something to act on. Once the handshake output settles, the connection is open and waiting for input — typing the current password and pressing Enter sends it through the encrypted channel, and the service replies `Correct!` followed by the next password.

---

## Level 16 → Level 17

**Goal:**
The credentials for the next level can be retrieved by submitting the password of the current level to a port on localhost in the range 31000–32000. First find which of these ports have a server listening, then find which of those speak SSL/TLS. Only one server actually returns the next credentials — the rest just echo back whatever is sent.

**Command(s) used:**
```bash
nmap -p 31000-32000 localhost
# found 5 open ports: 31046, 31518, 31691, 31790, 31960

openssl s_client -connect localhost:31046 -quiet   # SSL error -> not SSL
openssl s_client -connect localhost:31518 -quiet   # real handshake -> SSL
openssl s_client -connect localhost:31691 -quiet   # SSL error -> not SSL
openssl s_client -connect localhost:31790 -quiet   # real handshake -> SSL

# submitted the bandit16 password to each SSL-speaking port until one returned a key;
# port 31790 gave the real result, saved straight to a file:
openssl s_client -connect localhost:31790 -quiet > /tmp/key.private
# (typed the bandit16 password once connected, then closed the connection)

cat /tmp/key.private   # confirms "Correct!" and shows the private key

# transferred key.private to the local machine, then:
ssh -i key.private bandit17@bandit.labs.overthewire.org -p 2220

# once logged in as bandit17:
cat /etc/bandit_pass/bandit17
```

**Password found:**
```
pWXMAZoxGC8JmDMfmT5MGEsobMM3vnj2
```

**Understanding:**
This level combines everything from the previous few: port scanning, SSL detection, and SSH-key authentication, in one task. `nmap -p 31000-32000 localhost` scans that entire port range and reports which ports have something actively listening — five were open. Since not all of them necessarily speak SSL/TLS, each had to be tested individually with `openssl s_client`: ports that responded with a real certificate handshake (`CN=SnakeOil`, etc.) speak SSL; ports that immediately threw an `SSL routines...unexpected message` error do not (they're likely plain-text services that don't understand the SSL handshake bytes being sent to them).

Of the SSL-speaking ports, the current password still had to be submitted to each one to find the single port that actually validates it — the rest just echo input back. Redirecting the whole `openssl s_client` session straight to a file (`> /tmp/key.private`) captured the connection's output, including the `Correct!` confirmation and the returned private SSH key, without needing to manually copy text off the screen — cleaner than the approach used back in Level 13.

From there it's the same pattern as Level 13 → 14: the private key had to be moved to the local machine (Bandit blocks SSH connections back to itself from `localhost`), then `ssh -i key.private bandit17@... -p 2220` logged in using that key instead of a password, and `cat /etc/bandit_pass/bandit17` revealed the final password.

---

## Level 17 → Level 18

**Goal:**
There are 2 files in the home directory: `passwords.old` and `passwords.new`. The password for the next level is in `passwords.new` and is the only line that has changed between the two files.

**Command(s) used:**
```bash
diff passwords.old passwords.new
```

**Password found:**
```
OQxXZjELNdr90zuhOTDYBEomI0SZITXI
```

**Understanding:**
`diff` compares two files line by line and reports exactly where they differ, instead of requiring a manual side-by-side read-through of two large password lists. The output format `42c42` means "line 42 changed to line 42" — the `<` line shows the old content (from `passwords.old`), and the `>` line shows the new content (from `passwords.new`), separated by `---`. Since only one line differed between the two files, this immediately isolated the new password without needing to inspect every other line.

*(Note: logging into `bandit18` this way returns a `Permission denied` on the first password attempt shown in the screenshot — worth double-checking the copied password carefully, as this level is also the one where OverTheWire's own hint warns that a "Byebye!" message on login is expected behavior tied to the next level, `bandit19`, not a sign of doing anything wrong.)*

---

## Level 18 → Level 19

**Goal:**
The password for the next level is stored in a file `readme` in the home directory. Someone has modified `.bashrc` to log you out immediately when you log in with SSH.

**Command(s) used:**
```bash
ssh bandit18@bandit.labs.overthewire.org -p 2220 cat readme
```

**Password found:**
```
KpsOfPkcP7i1FlIExk2QEjyt6dw8dxZI
```

**Understanding:**
Normally, logging in with `ssh` starts an interactive shell — and on login, bash runs startup files like `.bashrc`. Here, `.bashrc` had been deliberately modified (as the goal states) to immediately print "Byebye!" and disconnect, before a normal interactive session (and any chance to run commands like `cat readme`) could start.

The workaround is a lesser-known feature of `ssh`: instead of just `ssh user@host`, you can append a command directly to the end of the SSH command — `ssh bandit18@bandit.labs.overthewire.org -p 2220 cat readme`. When `ssh` is given a command like this, it runs *only that one command* on the remote machine over a non-interactive session and returns its output, without ever spawning the interactive login shell that would trigger the sabotaged `.bashrc`. This bypassed the logout trap entirely and printed `readme`'s contents (the password) directly.

---

## Level 19 → Level 20

**Goal:**
Use the setuid binary in the home directory to gain access to the next level. Execute it without arguments to find out how to use it. The password can be found in `/etc/bandit_pass`, after using the binary.

**Command(s) used:**
```bash
ls
./bandit20-do
./bandit20-do cat /etc/bandit_pass/bandit20
```

**Password found:**
```
4pIjcunZ0fK2vmp3IwfG8Vf7VhxD6pOA
```

**Understanding:**
A **setuid** binary is a program that, when executed, runs with the permissions of its *owner* rather than the permissions of whoever is running it — normally, a program runs with the current user's own privileges, but a setuid bit changes that. Here, `bandit20-do` is owned by user `bandit20`, so anyone executing it (including `bandit19`) actually runs it *as* `bandit20`, gaining that user's access for the duration of the command.

Running it with no arguments (`./bandit20-do`) printed its own usage instructions: `Run a command as another user. Example: ./bandit20-do whoami`. Following that pattern, `./bandit20-do cat /etc/bandit_pass/bandit20` ran `cat /etc/bandit_pass/bandit20` *as bandit20* — which is why it could read a file normally only `bandit20` has permission to see, even though the command was launched from `bandit19`'s own session.

---

## Level 20 → Level 21

**Goal:**
There is a setuid binary in the home directory (`suconnect`) that connects to localhost on the port given as a command-line argument. It reads a line of text from that connection and compares it to the current level's password (`bandit20`'s). If correct, it transmits the next password (`bandit21`'s) back.

**Command(s) used:**
```bash
# Terminal 1 (listener):
nc -lvp 12345
# (once connected, typed the bandit20 password and pressed Enter)

# Terminal 2 (client):
./suconnect 12345
```

**Password found:**
```
bW9kBv5WC3P4yoDyf12LSdGuNz5ka6hY
```

**Understanding:**
`suconnect` acts as a *client* — it connects **out** to a port on localhost and waits to read a line from whatever is listening there; it never listens itself. So something else first has to be listening on that port, ready to send the password when `suconnect` connects. This needs two separate terminal sessions running at the same time: one to act as the listener, one to run `suconnect` as the client connecting to it.

`nc -lvp 12345` starts `netcat` in listening mode (`-l`) on port `12345`, with verbose output (`-v`) and forcing the port (`-p`). In the first attempt, `./suconnect 2220` was tried, but that's Bandit's own SSH port — `suconnect` connected there, read the SSH server's own greeting banner (`SSH-2.0-OpenSSH_10.2p1`) instead of a password, and correctly rejected it as a mismatch. A second attempt, `./suconnect 12345` with nothing listening yet, failed with "Could not connect" — nothing was there to connect to.

Once `nc -lvp 12345` was running in the first terminal, `./suconnect 12345` from the second terminal successfully connected to it. Typing the current password into the `nc` terminal sent it over that connection; `suconnect` read it, matched it against `bandit20`'s real password, and (since it runs setuid as `bandit20`) had permission to read and transmit `bandit21`'s password back — which appeared on the `nc` (listening) side of the connection.

---

## Level 21 → Level 22

**Goal:**
A program is running automatically at regular intervals from `cron`, the time-based job scheduler. Look in `/etc/cron.d/` for the configuration and see what command is being executed.

**Command(s) used:**
```bash
cd /etc/cron.d
ls
cat cronjob_bandit22

cd /usr/bin
cat cronjob_bandit22.sh

cat /tmp/t706lds9S0RqQh9aMcz6ShpAoZKF7fgv
```

**Password found:**
```
RYVux2rHEm9tiXHmLFzuR7Vhx6AZQMEz
```

**Understanding:**
`cron` is Linux's built-in job scheduler — it runs commands automatically on a schedule defined in files under `/etc/cron.d/` (among other locations). `ls`ing that directory showed several scheduled jobs, including `cronjob_bandit22`. Reading it (`cat cronjob_bandit22`) showed a schedule line pointing to a script: `/usr/bin/cronjob_bandit22.sh`, run **as user `bandit22`**, every minute.

`cat`ing that script revealed what it actually does:
```bash
chmod 644 /tmp/t706lds9S0RqQh9aMcz6ShpAoZKF7fgv
cat /etc/bandit_pass/bandit22 > /tmp/t706lds9S0RqQh9aMcz6ShpAoZKF7fgv
```
It copies `bandit22`'s password into a predictably-named file under `/tmp` and makes that file world-readable (`644`). Since cron runs this script *as bandit22* automatically, it already has permission to read `/etc/bandit_pass/bandit22` — the script does the privileged read on its own, on a timer, and leaves the result somewhere any user can pick up afterward. Trying to run the script manually as `bandit21` (`./cronjob_bandit22.sh`) failed with "Permission denied," since `bandit21` doesn't have execute rights on it directly — but that didn't matter, because cron had already run it automatically in the background as `bandit22`. Simply reading the output file it left behind — `cat /tmp/t706lds9S0RqQh9aMcz6ShpAoZKF7fgv` — revealed the password directly.

---

## Level 22 → Level 23

**Goal:**
A program is running automatically at regular intervals from `cron`. Look in `/etc/cron.d/` for the configuration and see what command is being executed. The script for this level is intentionally easy to read — try executing it to see the debug information it prints if unclear.

**Command(s) used:**
```bash
cd /etc/cron.d
cat cronjob_bandit23

cd /usr/bin
cat cronjob_bandit23.sh

# ran it manually to see the debug output and understand the logic:
./cronjob_bandit23.sh

# computed the same filename the script would generate for user bandit23:
echo I am user bandit23 | md5sum | cut -d ' ' -f 1

# read the file the real (cron-run) job had already generated for bandit23:
cat /tmp/8ca319486bfbbc3663ea0fbe81326349
```

**Password found:**
```
gKXDTAXnIz3OBxiPjRZ2uqutUlPZrBsw
```

**Understanding:**
This is a step up from the previous level: instead of a fixed output filename, `cronjob_bandit23.sh` computes the target filename *dynamically*, based on the current user:
```bash
myname=$(whoami)
mytarget=$(echo I am user $myname | md5sum | cut -d ' ' -f 1)
cat /etc/bandit_pass/$myname > /tmp/$mytarget
```
It takes the string `"I am user <username>"`, runs it through `md5sum` (a hash function that turns any input into a fixed-length, effectively unique hexadecimal string), and uses that hash as the filename in `/tmp`. `cut -d ' ' -f 1` trims `md5sum`'s output down to just the hash itself (`md5sum` normally prints the hash followed by a space and a dash).

Running the script manually as `bandit22` computed the hash for `"I am user bandit22"` and wrote *bandit22's own* password there — not useful, since that's the current user's own password already known. But cron runs this same script automatically **as `bandit23`** on its own schedule, which independently computes the hash for `"I am user bandit23"` and writes bandit23's password to *that* filename in `/tmp`. Running `echo I am user bandit23 | md5sum | cut -d ' ' -f 1` locally reproduced the exact same hash the script would generate for `bandit23`, without needing to actually be that user — since the hash only depends on the fixed string, not on any privilege. `cat`ing the resulting filename (`/tmp/8ca319486bfbbc3663ea0fbe81326349`) read the password that cron's automatic run (as `bandit23`) had already deposited there.

---

## Level 23 → Level 24

**Goal:**
A program is running automatically at regular intervals from `cron`. Look in `/etc/cron.d/` for the configuration. This level requires writing your own first shell script. Note: the script is deleted from its drop location once executed, so keep a copy elsewhere.

**Command(s) used:**
```bash
cat /usr/bin/cronjob_bandit24.sh   # inspect what the cron job actually does

mktemp -d
cd /tmp/tmp.Zz9K9w3b1p

cat > getpass.sh << 'EOF'
#!/bin/bash
cat /etc/bandit_pass/bandit24 > /tmp/tmp.Zz9K9w3b1p/bandit24_password.txt
chmod 777 /tmp/tmp.Zz9K9w3b1p/bandit24_password.txt
EOF

chmod +x getpass.sh
chmod 777 /tmp/tmp.Zz9K9w3b1p          # let bandit24 write into this directory
cp getpass.sh /var/spool/bandit24/foo/

# after ~60 seconds, once cron has run it:
cat /tmp/tmp.Zz9K9w3b1p/bandit24_password.txt
```

**Password found:**
```
hVQMk3lJNsmQ7VF3ubyrNNBom7BOgVXv
```

**Understanding:**
`cronjob_bandit24.sh` runs as `bandit24` and scans `/var/spool/bandit24/foo/` for files. For each one, it checks the file's **owner** with `stat --format "%U"`, and only *executes* files owned by `bandit23` — then deletes every file in that folder regardless (`rm -rf`), whether it ran or not. So the task isn't reading an existing file — it's writing and dropping a script for `bandit24`'s cron job to execute on your behalf.

`mktemp -d` created a private, unpredictable working directory to keep the output isolated from other users. The script itself (`getpass.sh`) does the same two things suggested at the start of this task: read `bandit24`'s password (readable *because the script runs as `bandit24`*) and write it out somewhere retrievable, then loosen that output file's permissions so it can be read back afterward.

The key gotcha: `mktemp -d` creates directories permissioned `700` (owner-only — here, only `bandit23`). When cron later runs the script *as `bandit24`*, `bandit24` doesn't have write access into that directory by default, so the `cat ... > .../bandit24_password.txt` line inside the script silently failed — no output file appeared, and `cat`ing it just returned "No such file or directory." The fix was `chmod 777` on the **temp directory itself** (not just the file), opening write access for any user including `bandit24`, then re-copying the script into `/var/spool/bandit24/foo/` so cron would pick up a fresh copy (the previous copy had already been deleted by the `rm -rf` after its failed run). After that, waiting for cron's next run cycle and reading the output file revealed the password.

**Takeaway:** when a privileged process writes into a directory you own, the *directory's* permissions matter just as much as the file's — a directory that's writable only by you blocks another user's process from creating anything inside it, even if the file it tries to create would otherwise be writable.

---

## Level 24 → Level 25

**Goal:**
A daemon is listening on port 30002 and will give the password for `bandit25` if given the password for `bandit24` and a secret 4-digit pincode. There's no way to retrieve the pincode except by brute-forcing all 10,000 combinations. A new connection isn't needed for every attempt.

**Command(s) used:**
```bash
for i in $(seq -w 0 9999); do echo "<bandit24_password> $i"; done > /tmp/pins.txt
nc localhost 30002 < /tmp/pins.txt > /tmp/output.txt
grep -A 1 "^Correct!" /tmp/output.txt
```

**Password found:**
```
SoHfqMOEqIX2IYKVciZxvgpR9a2Djx4P
```

**Understanding:**
A quick manual test via `telnet localhost 30002` confirmed the daemon's exact expected format (`<password> <pincode>` on one line) and — critically — that after a wrong guess it prints `Wrong!` and stays connected, waiting for another line, rather than closing the connection. That behavior is what makes brute-forcing all 10,000 combinations practical in one shot instead of reconnecting per guess.

`seq -w 0 9999` generates every number from 0 to 9999, and `-w` ("width") pads them all to the same number of digits based on the largest value in the range — so `0` becomes `0000`, `1` becomes `0001`, and so on, matching the required 4-digit format. The loop wrote all 10,000 `<password> <pincode>` lines into a file. Piping that entire file into a single `nc localhost 30002` connection (`nc ... < /tmp/pins.txt`) sent every guess through the one open connection, and its full response (thousands of `Wrong!` lines, or eventually a match) was redirected into `/tmp/output.txt` for review.

The first extraction attempt, `grep -i "correct"` (case-insensitive), matched far more than intended — the daemon's own rejection message is `Wrong! Please enter the correct current password...`, so every single failed attempt also contained the word "correct" and got matched. The fix was to anchor the search to the start of the line and match the exact capitalization of the real success message: `grep -A 1 "^Correct!"` — `^` anchors to line start (so it only matches lines that *begin* with "Correct!", not ones where "correct" appears mid-sentence), and `-A 1` ("after") also prints the line immediately following the match, which is where the daemon transmits the actual `bandit25` password.

---

## Level 25 → Level 26

**Goal:**
Logging into `bandit26` from `bandit25` should be easy — but `bandit26`'s login shell isn't `/bin/bash`, it's something else. Find out what it is, how it works, and how to break out of it.

**Command(s) used:**
```bash
# on bandit25:
cat /etc/passwd | grep bandit26
# -> bandit26:x:11026:11026:bandit level 26:/home/bandit26:/usr/bin/showtext

cat /usr/bin/showtext
# -> #!/bin/sh
#    export TERM=linux
#    exec more ~/text.txt
#    exit 0

ls                          # found: bandit26.sshkey

# transferred the key to the local machine (had to exit bandit25's
# SSH session first — connecting back to localhost is blocked):
scp -P 2220 bandit25@bandit.labs.overthewire.org:~/bandit26.sshkey ~/Desktop/

# shrank the local terminal window to a small number of visible rows,
# then connected using the key:
ssh -i bandit26.sshkey bandit26@bandit.labs.overthewire.org -p 2220

# once `more` paused mid-file (showing --More--), pressed v to open vi,
# then from inside vi:
:e /etc/bandit_pass/bandit26
```

**Password found:**
```
jHdv2ELQhT22BkprMNDjybZDAkw1zeBJ
```

**Understanding:**
`bandit26`'s account uses `/usr/bin/showtext` as its login shell instead of `/bin/bash` — any valid shell path works in `/etc/passwd`, not just real shells, so it's entirely possible to force a user into running a custom script the instant they log in. `showtext` runs `more ~/text.txt` (displaying some ASCII art) and then exits immediately, closing the connection — no interactive shell is ever reached normally.

The way around it hinges on how `more` behaves: it's a pager that only pauses and waits for input if the content doesn't fit in one screen. Deliberately shrinking the terminal window (fewer visible rows) meant the same file no longer fit on one screen, so `more` paused mid-way and showed `--More--` at the bottom instead of finishing instantly. While paused, `more` supports single-key commands — pressing `v` opens the file in whatever editor `$EDITOR` is set to (typically `vi`), *before* the script's `exit 0` line ever runs.

From inside `vi`, instead of the more commonly used shell-escape (`:!/bin/bash` or `:set shell=... :shell`, which spawns an interactive shell), a simpler alternative was used here: `vi`'s own `:e <path>` ("edit") command, which opens *any* file the current user has permission to read directly inside the editor — including `/etc/bandit_pass/bandit26`, which `bandit26` can read (it's their own password file). This skipped needing a full shell entirely and displayed the password straight in the editor buffer.

Getting the SSH key itself required repeating the same lesson from Levels 13 and 16: Bandit blocks SSH/`scp` connections that originate from `localhost` back to itself, so the key had to be pulled via `scp` run from the actual local machine, not from inside an active `bandit25` session.

---

## Level 26 → Level 27

**Goal:**
Good job getting a shell! Now grab the password for `bandit27`.

**Command(s) used:**
```bash
ls
# -> bandit27-do  text.txt

./bandit27-do cat /etc/bandit_pass/bandit27
```

**Password found:**
```
STJLJBRRphMxKB392CT4iOr5CbzPU9ER
```

**Understanding:**
Same pattern as Level 19 → 20: `bandit27-do` is a setuid binary owned by `bandit27`, so running it executes the given command *as* `bandit27` rather than as the current user. Once inside the real `bash` shell gained by escaping `more`/`vi` in the previous level, this was a plain repeat of the earlier technique — `./bandit27-do cat /etc/bandit_pass/bandit27` ran `cat` as `bandit27`, which has permission to read its own password file, and printed the password directly.

---

## Level 27 → Level 28

**Goal:**
A git repository is hosted at `ssh://bandit27-git@bandit.labs.overthewire.org:2220/home/bandit27-git/repo`. The password for `bandit27-git` is the same as for `bandit27`. Clone the repository from the local machine (not the Bandit server) and find the password for the next level inside it.

**Command(s) used:**
```bash
git clone ssh://bandit27-git@bandit.labs.overthewire.org:2220/home/bandit27-git/repo
cd repo
ls
cat README
```

**Password found:**
```
y8Yd2ssKcpHpud7UvOSOxwamRMzIGIeQ
```

**Understanding:**
This level is a straight `git clone` over SSH rather than a plain `scp`/`ssh` file grab, and the syntax differs slightly from a normal SSH login: instead of `ssh -p 2220 user@host`, the port goes directly inside the URL as `ssh://user@host:2220/path/to/repo`. Git recognises the `ssh://` scheme and handles the SSH handshake (including the password prompt for `bandit27-git`) itself before pulling down the repository contents.

The task explicitly said to do this "from your local machine (not the OverTheWire machine!)" — a repeat of the same restriction seen with `scp` in earlier levels, since Bandit blocks connections that originate from its own server back to itself. Running `git clone` from the actual local machine avoided that block entirely.

Once cloned, `repo` turned out to contain just a single `README` file — no history digging or branch exploration was needed here, since the password was sitting in the file directly. `cat README` printed it straight away.

---

## Level 28 → Level 29

**Goal:**
A git repository is hosted at `ssh://bandit28-git@bandit.labs.overthewire.org:2220/home/bandit28-git/repo`. The password for `bandit28-git` is the same as for `bandit28`. Clone the repository from the local machine and find the password for the next level.

**Command(s) used:**
```bash
git clone ssh://bandit28-git@bandit.labs.overthewire.org:2220/home/bandit28-git/repo
cd repo
ls
cat README.md
# -> password shown here is redacted (xxxxxxxxxx)

git log
git log -p -1
```

**Password found:**
```
Em7eGtqaMySwNFjCpwzzHhLhospOcdt0
```

**Understanding:**
This level looks identical to Level 27 → 28 at first, but the twist is that `README.md` in the current checkout has the password deliberately redacted (`password: xxxxxxxxxx`) — a fix was made *after* the real password had already been committed to the repo's history. Since git tracks every past version of a file, deleting or overwriting content in a later commit doesn't erase it; the old version is still fully retrievable from the commit history unless it's rewritten and force-pushed (and even then, until garbage-collected).

`git log` listed the repo's three commits, and the most recent one — `"fix info leak"` — was the giveaway: an explicit admission that an earlier commit had leaked something sensitive. `git log -p -1` showed the diff (`-p`) of just that most recent commit (`-1`), revealing exactly what changed line-by-line. The diff showed the line `- password: Em7eGtqaMySwNFjCpwzzHhLhospOcdt0` being removed and `+ password: xxxxxxxxxx` being added in its place — meaning the real password, still fully visible in the diff's "removed" line, was sitting right there in the "leak" commit that was supposed to have fixed the problem.

**Takeaway:** committing a secret and then "removing" it in a later commit does not delete it from the repository — the old blob is still reachable via `git log -p`, `git show <commit>`, or just checking out the earlier commit. The only real fix is to rotate/invalidate the leaked secret itself, since the git history can't be trusted to keep it hidden.

---

## Level 29 → Level 30

**Goal:**
A git repository is hosted at `ssh://bandit29-git@bandit.labs.overthewire.org:2220/home/bandit29-git/repo`. The password for `bandit29-git` is the same as for `bandit29`. Clone the repository from the local machine and find the password for the next level.

**Command(s) used:**
```bash
git clone ssh://bandit29-git@bandit.labs.overthewire.org:2220/home/bandit29-git/repo
cd repo
ls
cat README.md
# -> only shows: password: <no passwords in production!>

git log
git log -p -1
# -> master branch's only real change is "fix username", no leaked password here

git branch -r
# -> origin/HEAD -> origin/master
#    origin/dev
#    origin/master
#    origin/sploits-dev

git checkout dev
git checkout origin/dev      # detached HEAD

git log
# -> extra commit: "add data needed for development"

git log -p -1
# -> diff reveals the real password
```

**Password found:**
```
jq9Dfg2rXsfYsWMgFuKlXhphjdH7USgX
```

**Understanding:**
This level builds directly on the previous one but closes the easy loophole: on the `master` branch, `README.md` never actually contained a real password in its history — the only change tracked there was a `"fix username"` commit, and the password field was a placeholder (`<no passwords in production!>`) from the very first commit. So `git log -p` on `master` alone comes up empty.

The real content was hiding on a different branch. `git branch -r` (`-r` for "remote") lists all branches that exist on the remote but aren't necessarily checked out locally — and it revealed two branches beyond `master`: `dev` and `sploits-dev`. This is the key lesson of the level: a `git clone` only checks out the default branch by default, but it still *fetches* all other branches' data — they're just not visible unless you go looking for them.

`git checkout dev` created a local tracking branch from `origin/dev`; a second `git checkout origin/dev` (checking out the remote ref directly) landed in a detached-HEAD state, which is fine for read-only inspection. `git log` on that branch showed one extra commit beyond what `master` had — `"add data needed for development"` — and `git log -p -1` showed its diff, which was the actual leaked password sitting in `README.md`'s development version, never merged back into (and cleaned up on) `master`.

**Takeaway:** a repository's other branches — especially ones with names like `dev` or `sploits-dev` — often contain content that was deliberately kept off the main branch, but `git clone` pulls the full history of every branch regardless. Checking `git branch -r` before assuming a repo is "empty" is a habit worth keeping.

---

## Level 30 → Level 31

**Goal:**
A git repository is hosted at `ssh://bandit30-git@bandit.labs.overthewire.org:2220/home/bandit30-git/repo`. The password for `bandit30-git` is the same as for `bandit30`. Clone the repository from the local machine and find the password for the next level.

**Command(s) used:**
```bash
git clone ssh://bandit30-git@bandit.labs.overthewire.org:2220/home/bandit30-git/repo
cd repo
ls
cat README.md
# -> just an epmty file... muahaha

git log
# -> single commit, "initial commit of README.md" — nothing else in history

git branch -r
# -> only origin/master, no other branches this time

git tag
# -> secret

git show secret
```

**Password found:**
```
82NkymblpGBYmIXG6ZQ8YldBYstHpfUf
```

**Understanding:**
This level closes off both tricks from the previous two levels on purpose: `git log -p` on the single existing commit shows nothing useful (the README really is just a joke about being empty), and `git branch -r` confirms there's no second branch to pivot to this time. The secret is stashed somewhere else entirely — a **tag**.

Tags in git are just named pointers to a specific commit, normally used to mark release points (`v1.0`, etc.), but nothing stops one from being used to smuggle data instead. `git tag` (with no arguments) lists all tags in the repo, and it revealed one named `secret` — an obvious signal given the level's theme. `git show <tag-name>` displays what a tag points to, which in this case wasn't just a bare commit reference but printed the password directly, since the tag itself carried an annotated message containing it.

**Mistake made along the way:** ran `git tag secret` (intending to create a new tag) instead of just `git show secret` — git correctly refused with `fatal: tag 'secret' already exists`, which was actually a useful hint confirming the tag was real and worth inspecting further.

**Takeaway:** git has several places besides commit content where data can be hidden — branches, tags, stashes, and even commit/tag messages themselves. When a repo's obvious files come up empty, checking `git tag`, `git branch -a`, and `git stash list` is worth doing before assuming there's nothing left to find.

---

## Level 31 → Level 32

**Goal:**
A git repository is hosted at `ssh://bandit31-git@bandit.labs.overthewire.org:2220/home/bandit31-git/repo`. The password for `bandit31-git` is the same as for `bandit31`. Clone the repository from the local machine and find the password for the next level.

**Command(s) used:**
```bash
git clone ssh://bandit31-git@bandit.labs.overthewire.org:2220/home/bandit31-git/repo
cd repo
cat README.md
# -> This time your task is to push a file to the remote repository.
#    Details:
#      File name: key.txt
#      Content: 'May I come in?'
#      Branch: master

touch key.txt
echo "May I come in?" > key.txt
git add key.txt
# -> blocked: "The following paths are ignored by one of your .gitignore files: key.txt"

rm .gitignore
git add key.txt
git commit -m "Upload a file"
git push origin master
```

**Password found:**
```
pWuj5jBQ6IgV0NXwiH6g1pXRF8S1YvbT
```

**Understanding:**
Unlike every previous git level, this one required *writing to* the remote repo rather than reading from it. The `README.md` spelled out the exact deliverable: a file named `key.txt` containing the literal text `May I come in?`, committed to the `master` branch and pushed back to the server — the server-side hook then checks the pushed content and hands back the password if it matches.

The first snag was git refusing to stage the file at all: a `.gitignore` in the repo specifically excluded `key.txt`, so `git add key.txt` was silently rejected with a warning rather than an error that would've been more obvious. Git offered two ways around this — force-add with `-f`, or remove the ignore rule entirely — and since the rule itself was clearly the obstacle (not a real project convention worth respecting here), deleting `.gitignore` outright and re-running `git add` was simpler and let the file be tracked normally afterward.

**Mistake made along the way:** the first push attempt used `git push origin main`, which failed with `error: src refspec main does not match any` — this repo's default branch is `master`, not `main` (the two names are common defaults from different git versions/hosts and aren't interchangeable). Switching to `git push origin master` matched the branch that actually existed locally and pushed successfully.

Once the push landed, the server ran its own validation step (visible in the `remote:` output lines) confirming the file's name, branch, and exact content matched what was expected, then printed the password directly in the push response.

**Takeaway:** a `.gitignore` file blocking `git add` is a soft guard, not a hard one — `-f` or removing the rule both bypass it — and `main` vs `master` is worth checking with `git branch` before pushing, since guessing the wrong default branch name is a very common real-world mistake too.

---

## Level 32 → Level 33

**Goal:**
Logging into `bandit32` drops you into an unusual restricted shell rather than a normal one — the task is to figure out how it behaves and use that to reach a real shell, then read the password for `bandit33`.

**Command(s) used:**
```bash
# on connecting, greeted with:
# WELCOME TO THE UPPERCASE SHELL

ls
# -> sh: 1: LS: Permission denied

$0
# -> drops into a real lowercase `sh` shell

cat /etc/bandit_pass/bandit33
```

**Password found:**
```
u4P2CyPOwPGLe94RdD9Uo2FxFwvnFswM
```

**Understanding:**
This login shell announces itself outright: `WELCOME TO THE UPPERCASE SHELL`. Testing it by typing an ordinary command (`ls`) showed exactly what it does — it uppercases whatever's typed *before* running it, so `ls` became `LS`, which the underlying shell (`sh`) doesn't recognize as any valid command, hence `sh: 1: LS: Permission denied`. The same happened with `bash` and `BASH` — no command name survives being forced into uppercase, since Unix commands are case-sensitive and almost none exist in all-caps.

**Mistake made along the way:** tried typing `bash` and `BASH` directly, expecting one of them might slip through — but the shell uppercases the input regardless of what case it started in, so there's no way to "pre-uppercase" your way past the transform; it always runs the uppercased version.

The way out relies on the fact that the uppercasing is a pure text transform with no letters to act on in certain inputs. `$0` is a special shell parameter that expands to the name of the currently running shell/script — it contains no alphabetic characters, so uppercasing it changes nothing (`$0` uppercased is still `$0`). Sending it as input caused the restricted shell to literally execute its own `$0` (i.e., invoke itself/the underlying shell binary again), which spawned a **fresh, non-restricted `sh` shell** — one without the uppercase wrapper applied to it. From there, ordinary lowercase commands worked normally, and `cat /etc/bandit_pass/bandit33` read the password directly.

**Takeaway:** input-filtering restricted shells that transform text (uppercasing, character stripping, blacklisting) can often be escaped by finding an input that is unaffected by the transform but still meaningful to the shell — special parameters like `$0`, `$$`, or `$SHELL` are prime candidates since they contain no letters (or the transform doesn't change their meaning) yet can be used to spawn or reference a real shell process.

---

## Level 33 → Level 34 (Final Level)

**Goal:**
Bandit Level 33 is the last level currently available in the game.

**Command(s) used:**
```bash
ls
cat README.txt
```

**Output:**
```
Congratulations on solving the last level of this game!

At this moment, there are no more levels to play in this game.
```

**Understanding:**
There is no Level 34 to solve — Bandit's official page for Level 33 → 34 confirms this directly: "At this moment, level 34 does not exist yet." Level 33 is the final level of the wargame as it currently stands, and its `README.txt` is simply a congratulatory message rather than a puzzle. This marks the end of the Bandit series — all 33 levels (0 through 33) completed.

---

## Summary

Bandit taught, in rough order of appearance: basic Linux navigation and file reading; shell quoting/escaping for tricky filenames; file-type identification vs. trusting extensions; permission and SUID/SGID exploitation; brute-forcing and automated scripting; port scanning and network services (`nc`, `telnet`, SSL/TLS); cron jobs and race conditions; restricted shells and shell-escape techniques; and finally, git — cloning, history inspection, branches, tags, and pushing changes. It's a solid practical foundation for the Linux command-line skills expected in embedded/VLSI lab environments, CI pipelines, and general SRE/security work alike.
