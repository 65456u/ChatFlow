## Install

Install from PyPI

```
pip install chatflow
```

Install from source

```
# clone this repository
git clone https://github.com/65456u/ChatFlow.git
# get into the repository
cd ChatFlow  
# install required packages
pip install -r requirements.txt
# install ChatFlow  
pip install .
```

## First ChatFlow Program

Let's first write a simple ChatFlow that simply echos the input.

```
flow origin {
  listen for message
  speak message  
}
```

To run this:

```python
from chatflow import Interpreter, Runtime

code = """
flow origin {
  listen for message
  speak message
}
"""

interpreter = Interpreter(code=code)
runtime = Runtime(interpreter)
runtime.run() 
```

## Usage

Key concepts:  

- `flow` defines a conversation flow
- `listen` gets input from user
- `speak` outputs message  

This example shows:

- Defining a simple `origin` flow
- Listening for a `message` input
- Speaking the message back to user

Check out the [docs](https://chatflow.readthedocs.io) to learn more!
