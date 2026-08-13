km = float(input("Enter km:"))
c = float(input("Enter celsius:"))

def km_to_miles(km):
    return km * 0.621371

def celsius_to_fahrenheit(c):
    return (c * 9/5) + 32

print(f'{km}km in miles:',km_to_miles(km))
print(f'{c}c in fahernheit:',celsius_to_fahrenheit(c))
