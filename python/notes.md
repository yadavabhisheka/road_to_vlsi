## How i learned python 

### Starting with [Corey Schafer's python beginner series](https://www.youtube.com/playlist?list=PL-osiE80TeTskrapNbzXhwoFUiLCjGgY7)

> Strings - Working with textual data

- There are 3 ways to create a string 
```
  message = 'Hello World'            #single quotes
  message2 = "Hello World"           #double quotes
  message3 = """Hello i am World"""  #multiline strings
```
- Several methods are available in python to use on strings
```
message.lower()     #lowercase everything
message.upper()     #uppercase everything
len(message)        #get length of string
message.count()     #count no of time char or string appears
message.find()      #find the index of the char or string
message.replace()   #take two arg and replace first with sec

#string formating
message='{}, {}. Welcome!'.format(var1,var2) 
message=f'{var1}, {var2}. Welcome!'   #f-strings(3.6 & newer)

dir(variable)       #all available methods
help(str)           #help with strings
```
