## Introduction

ChatFlow is a domain-specific language designed specifically for authoring conversational dialog flows, such as for chatbots and voice assistants. 

It utilizes an easy to read declarative format to define different conversation flows, the actions within them, and how they connect together. This makes it intuitive for developers to visualize and manage complex dialog logic.

Under the hood, ChatFlow scripts are compiled into an intermediate tree representation. The included runtime engine can then interpret and execute the conversation flows based on user inputs.

## Key Features

- **Readability**: ChatFlow features a highly readable grammar that enables both developers and non-technical people to understand conversation logic. It uses English-like syntax following natural language constructs, which reduces the learning curve.
    
- **Integration**: ChatFlow provides rich integration capabilities with external systems via Python. It allows data processing in real-time during the conversation. Users can define custom execution flows named "tributaries", which enable integration with anything in Python including databases, APIs and more.

- **Interpreted**: ChatFlow scripts compile into an intermediate tree format, which enables analysis, optimization and detailed debug information.
    
- **Extensibility**: ChatFlow provides extension points to customize execution by defining tributaries.

- **Information Flow**: ChatFlow follows one-way flow of information between flows, where data can only be passed from caller flows to callee flows. This improves modularity and hides complexity.


## Learning ChatFlow

1. [Quick Start](tutorials.md)
2. [Grammar](grammar.md)
3. [Concepts](concepts.md)
4. [Advanced](advanced.md)


## Acknowledgements

ChatFlow owes much gratitude to the open source projects that helped make it possible.

In particular:

- **Lark**  
    ChatFlow builds on the excellent [Lark parsing toolkit](https://github.com/lark-parser/lark) for generating the abstract syntax tree from the Conversation Flow scripts. The ability to define a clean grammar and easily parse it into a manipulatable tree structure is invaluable.

## License

Lark uses the [MIT license](LICENSE).
