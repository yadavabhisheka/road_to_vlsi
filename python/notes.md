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

> Integers and float - working with numeric data

```
int x         #x is an integer
float x       #x is a decimal number
type()        #get the type of variable 
num += 1      #increment num by 1
num -= 1      #decrement num by 1

abs()         #absolute or +ve value
round(x.xx,y) #round off to y places and if no y then nearest integer

all Arthimetic Operators(+,-,/,*,//,**,%)
all Comparison Operators(==,!=,<,>,>=,<=,is)

Casting :
int(var)
float(var)
```

> Lists, Tuples and Sets

- Lists- What and How?
```
- Lists are mutabe objects.
list_1 = ['value1','value2','value3','value4'] #declaration
list_value_2 = list_1[1]                       #List Indexing

Methods used with lists

list.append('value')          #inserted at the last index
list.insert(index,'value')    #inserted on the specific loca^
list1.extend(list2)           #one list's values will insert
list.remove('value')          #remove this entry
list.pop()                    #pop out last element of list
list.reverse()                #reversing a list
list.sort()                   #sorting a list in inc^ order
list.sort(reverse=True)       #sorting in dec^ order
sorted(list)                  #sort and store w/o main list
min(list)                     #minimum value from list
max(list)                     #maximum value from list
sum(list)                     #sum of the list
list.index('value')           #finding index of value
.join()                       #making list to str
.spilt()                      #making str to list

empty_list = []
empty_list = list()
```
- Tuples- What and How?
```
- Tuples are immutable objects.
tuple_1 = ('value','2value','3value')

empty_tuple= tuple()
empty_tuple= ()
```

- Sets: 
```
set_1 = {'value','value2','value3'}
set_1.intersection('set2')
set_1.difference('set_2')
set_1.union('set_2')

empty_set= set()
```

> Dictionaries
``` 
student = {'name':'Jhon','age':'23','courses':['maths','phy','chem']}             #declaration
student(['name'])                                                                 #getvalue
student.get('keypair','notfound')                                                 #getvalue and msg if not found

student(['name']) = 'newname'                                                     #changevalue
student.update({dict})                                                            #changemultiplevalues
del student['age']                                                                #delete the key and vlaue
student.pop{'key'}                                                                #pop and store
student.key()                                                                     #gives all the keys
student.value()                                                                   #get all the values
student.item()                                                                    #get all key value pairs
```

>Conditionals and Booleans - If, Else, and Elif Statements

```
if (conditions):
    #true than execute
elif (second Conditions):
    #true than execute
else:
    #if everything is false than this

boolean operations
- and
- or
- not

is keyword                          #used to compare id of two variable
```

>Loops and Iterations - For/While Loops
