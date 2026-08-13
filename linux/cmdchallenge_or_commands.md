# cmd challenge 

**Wonderful place to learn commands used in bash shell, i will be using it for learning new commands and methods.**

26-07-2026

> echo "hello world"                        #hello world
> pwd                                       #current working directory
> ls                                        #list files in the directory
> cat access.log                            # getting a files contents
> tail -5 access.log                        #last 5 lines
> touch take-the-command-challenge          #creating a file
> mkdir -p tmp/file                         #create directory 
> cp take-the-command-challenge tmp/file    #copy file
> mv take-the-command-challenge tmp/file    #move file
> ln -s tmp/files/take-the-command-challenge take-the-command-challenge  #symbolic link

27-07-2026

> rm -rf .* *                               #delete all the files 
> rm -rf **/*doc                            #delete all with .doc ext
> cat access.log | grep "GET"               #access.log having lines with GET
> ls | grep -lr "500"                       #out of the file which one has 500 in the file
> ls | grep access.log                      #file with name access.log
> grep -rh '500'                            #files with 500 in it

30-07-2026

>grep -ro --include "access.log*" ^[0-9]*   #files with ip
>ls -l | grep -c .                          #count files in a directory
>sort access.log                            #sorted access.log
>grep "GET" access.log | wc -l              #Count no of GET
>tr ';' '\n' < split-me.txt                 # replace ; and spilt
>echo {1..100}                              #print number from 1-100
>
