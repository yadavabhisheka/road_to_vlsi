# The Complete Bash Scripting Course - Full Length Guide to learning the Bash Shell

**A full flechted bash course by DAVE EDDY, doing this to attain a fluency in scripting itself i knew commands, now we have to automate things.**

#### Chapter 01

##### Terminal and Finder

- REPL - Real eval print loop
- echo, pwd, ls, touch, rm, clear, cd

##### Basic File Manipulation

- mv, rm -i(interactive), Ctrl + l(clear), alias rm='rm -i', history, 
- .hiddenfile(creating a hidden file), ls -a(all files)
- cd .(current dir),cd ..(one before), cd - (previous dir)

##### Searching in files

- /usr/share/dict/words (file with multiple words), cat, grep '^__' (anything have this in front), grep '__$' (anything have this in back)
- \>/>> redirecting to a file / append something in a file
- grep -A1(after that 1 line) -B1(before that 1 line) -C1(that thing in center and above and below one line) -i(case insesitive) -o(only that letter or after and before that)
- cat /usr/share/dict/words |(pipeline) grep -i "dave" | grep ly

##### Paging files

- less , q to quit , / to search something, arrow keys of J and K to up and down 
- more same as less

#### Chapter 2

##### Man Pages

- Mannual pages for all the commands and their agruments, can be navigated just like less.
- help for the built in commands.
- type to get whats builtin and what not and also the bins and aliases.
- compgen -b to get all the built in commands.

##### Programs and Commands

- file to knew what type of file it is.
- echo $PATH or echo $PATH | tr ':' "\n"

##### Basic variables

- name="Abhishek     Yadav" (to reserve the spaces)
- thing=\`uname -a`
- thing=$(uname -a)

##### Vim Crash Course

- i to insert, Esc to back in navigation mode, :w to write, :q to quit
- dd to delete a line, . to give the previous command 
- yy copy p to paste, o insert from new line, u to undos

#### Chapter 3

##### Finally scripting

- #!/usr/bin/env bash (first line to get the terminal know its bash)
- bash -n file (to know any errors in syntax)
- echo $? (previous command was a success or not)

##### User Input

- read -p 'msg' var (read and prompt a msg and save to a variable)
- var=$1 (read the commands arguments)
- $@ (to get a array in arguments)

##### Functions

- just writing the whole program 
  ```
  #!/usr/bin/env bash
  greet(){
    local name=$1
    echo "hello $name"
    return 0
  }
  for name in "$@"; do
        greet "$name" >> file.txt
  done

  greet dave
  echo $? 
  ``` 
##### Conditionals 

- [[  ]] - test mode
- if (command to be executed) ; then
             what output we want if command exceuted
  fi  

##### For-Loops

- ((   ))- math mode
- for (some command or things); do
            action to be done
  done

##### Input/outut

- read var

 ##### Case Statements

 - 