[Helper files cover page](./README.md) | [Lab guide cover page](../lab_guide/README.md)

![line](../img/banner_line.png)

# Python primer

## General

### Running Python script:
```bash
python filename.py
```
>**Note**: Remember to always save your file before running. In our experience, forgetting to save your file before running it is a common mistake among Python beginners.

### Reading a Python error message

When getting an error message after running a script, don't panic! Python error messages are really helpful on identifying what went wrong.

Below you see an example of error message when forgetting to close the string quotation. Note that the error message gives you the line where the script failed, which will help you in troubleshooting. Note that sometimes the line given is next line after your mistake, so if you cant find error on the mentioned line, look above it.

```bash
$ cat example.py 
my_devices = [
    "c9k",
    "c8k,
    "nexus9k"
]

print(my_switches)

$ python example.py
  File "example.py", line 3
    "c8k,
         ^
SyntaxError: EOL while scanning string literal
```

### Indentation

Python relies heavily on correct indentation of your code. When writing your code, every block such as the [function](#functions) definitions, [conditionals](#conditionals), and [loops](#loops) need to have the correct indentation for Python to understand which lines belong logically to which code block. Use 4 spaces for one indentation level.

```python
my_vlans = [100, 200, 300, "IOT"]

for vlan in my_vlans:
    print(vlan) #one level of indentation to identify this belongs under for loop

    if vlan == 200:
        print("This is VLAN 200!") #One more level of indentation to identify this belongs under the conditional
```

## Basic Python structures

### Types and variables

Variables are used to store data. In Python, a variable is not tied to a certain data type, so you may replace the value of a variable with a value that has a different data type than the original value.

Some of the types that you will work on during this lab:

- Strings (`str`) -> text
    ```python
    my_string = "This is a string"
    my_another_string = 'This is also a string'
    my_long_string = """
    This is a
    multiline 
    string.
    """
    ```
- Integers (`int`) -> numbers
    ```python
    my_number = 2
    ```
- Lists (`list`)
    ```python
    my_vlans = [100, 200, 300, "IOT"]
    print(my_vlans[2]) #prints 300
    ```
    > **Note**: List uses square brackets `[ ]` and can be a combination of different types of values. To access an item in a lits, the index of that item is used. The index counting starts from `0`, meaning that the first item in the list has index 0.
    > Lists are often looped through using a [for loop](#loops).

- [Dictionaries](#dictionary) (`dict`)
    ```python
    my_switch = {
        "name": "Cat9k",
        "model": "Catalyst 9300",
        "reachable": True,
        "rack_number": 5
    }

    print(my_switch["reachable"]) #prints True
    ```
    > **Note**: Dictionary uses curly brackets `{ }`, and has a key:value structure. Each key needs to be unique to identify the value returned. Values can be a combination of different types of values. To access an item in a dictionary, the name of the key is used.

- Boolean (`bool`) -> True or False
    ```python
    interface_enabled = False
    ```
    > **Note**: Booleans are used in [conditionals](#conditionals).

### f-strings

When working with printing variable values, `f-string` is a really nice way to include the variables into a string. `f-string` frees you from having to worry about the type of the variable being printed. `f-string` is identified with the `f` right before the string, and variables can be included with curly brackets `{variable_name}`.

```python
my_switch = "Catalyst 9K"
print(f"I have a switch called {my_switch}")
```

### Conditionals

Conditionals use `if` - `elif` - `else` structure to test if something is `True` or not. At minimum, conditional needs one `if`, but it can also have `elif`s and `else`. Conditionals can have multiple `elif` blocks (=else if), and one `else` block that is reached if nothing before it is `True`.

```python
interface_enabled = False
switch_reachable = True
number_of_endpoints = 4

if interface_enabled:
    print("interface is enabled!") #will not be printed

if switch_reachable:
    print("switch is reachable!") #will be printed
else:
    print("Switch is not reachable!") #will not be printed

if number_of_endpoints > 10:
    print("There are more than 10 endpoints connected.") #will not be printed
elif number_of_endpoints > 3:
    print("There are less than 10 but more than 3 endpoints connected.") #will be printed
else:
    print("There are 3 or less endpoints connected.") #will not be printed
```

The above prints the following:
```bash
switch is reachable!
There are less than 10 but more than 3 endpoints connected.
```

### Loops

Loops are really useful in network automation. There are two kinds of loops supported (`for` and `while`), but as most of the network tasks would fall under `for`, lets focus on that.

For loop iterates through values of a list or other iterable Python type.

```python
my_vlans = [100, 200, 300, "IOT"]

for vlan in my_vlans:
    print(vlan)
```
```bash
100
200
300
IOT
```

You can also loop through dictionary keys:
```python
my_switch = {
    "name": "Cat9k",
    "model": "Catalyst 9300",
    "reachable": True,
    "rack_number": 5
}
for key in my_switch:
    print(key)
```
```bash
name
model
reachable
rack_number
```

To loop key-value pairs of a dictionary, use the dictionary method `items()`.
```python
my_switch = {
    "name": "Cat9k",
    "model": "Catalyst 9300",
    "reachable": True,
    "rack_number": 5
}
for key, value in my_switch.items():
    print(f"- {key} is {value}")
```
```bash
- name is Cat9k
- model is Catalyst 9300
- reachable is True
- rack_number is 5
```

### Functions

Functions help you make reusable code. Functions are also important when you want to create your own modules for your scripts ([see more below](#importing-your-own-code)).

Function is defined with the keyword `def`. You can define parameters that can be passed to the function, as well as a return value that will be returned once the function is ran.

```python
def my_function(parameter1, parameter2):
    print(f"The parameters are: {parameter1}, {parameter2}")
    return "This is returned from the function"

response = my_function("router", "switch")
print(response) #prints the returned value
```
```bash
The parameters are: router, switch
This is returned from the function
```

To add readability and usability of your functions, a good idea is to include type hints. Python is not enforcing the types, but they are good documentation for anyone reading your code on how the function should be used.

```python
def my_function(parameter1:str, parameter2:int)->str:
    print(f"The first parameter should be a string: {parameter1}")
    print(f"The second parameter should be an integer: {parameter2}")
    return "A string is returned"
```

## Imports

### Importing a library

You can and should utilize Python libraries when writing your automation scripts. Libraries are ready made code that you can import to your script, without having to invent the wheel again for common use cases. `ncclient` used with NETCONF connections and `requests` used with REST APIs are two good examples of useful libraries.

> **Note**: In the lab environment, the libraries are already installed, but in general, if using a library that is not part of the in-built modules, you would need to use Python module `pip` to first install the library.
> ```bash
> pip install requests
> ```

To include library or module in your script, you need to `import` it. You can import the whole library or parts of it.

```python
import requests

my_request = request.get(url, payload)
#Note the namespace! You need to define that the functionality get comes from requests library

from ncclient import manager

connection = manager.connect(attributes)
#Note the namespace! You refer directly to manager as you selected to import that from the ncclient
```

### Importing your own code

It is good practice to code with modular approach, as your code becomes more readable and more easily maintainable. This means that your functions are defined in different files, and similar functionalities are collected under same file or in the same folder.

To import your own code, you also use the `import` key word.

Example of a folder:
```bash
$ ls
main.py     my_script.py       my_second_script.py
```

`main.py`:
```python
import my_script
from my_second_script import example_function
```

## Error handling and data validation in Python script

### If-else

When receiving data from an event, or after making a REST API call, it is good to include some error handling in case something went wrong or data was returned in a wrong way.

If-else conditional structure can be used for error handling, especially when the error wouldn't naturally raise an `Exception` in Python. An example of this would be a REST API Request - the request itself may be successful from Python's perspective, but if the returned status code is not the right one, you would like to handle the problem instead of letting the code crash.

Below you can see an example of reacting to a non-ok status code of a request in a conditional:
```
    response = requests.post(url, headers=headers, json=payload)

    if str(response.status_code)[0] != "2":
        raise Exception(f"Error: {response.text}")
```
>**Note**: When working with REST APIs, status code starting with `2` (for example `200`) indicates that the API call was successful. If any other kind of status code is returned, something in the API call went wrong: might be that the targeted resource doesn't exist, or maybe you mistyped your password.

### Try-Except-Else

`Try` - `Except` - `Else` structure is used to react to situations were Python is raising an exception. This can for example be used when trying to open a file - "What if the file doesn't exist?", "What if the permissions don't allow that file to be opened?", etc.

What you are trying to do is going to be written in the block `try:`. What to do if an Exception is raised while trying, is defined in `except:` block. `else:` can be used to indicate what to do if `try` was successful.

Example:

```python
    try:
        #Trying to retrieve the data of a Webex card action
        card_data = netbox_card.netbox_card_attachment_event(webex.webex_token, event)

    except Exception as err:
        #If data handling fails, sending a message to tell that the action failed
        webex.send_message(webex.webex_token, webex.my_email,
                           "Something went wrong when handling your request...")

        print(f"Error occurred: {err}")
```

![line](../img/banner_line.png)