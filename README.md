# MCP Tool Calling and Testing via MCP Inspector

## Overview
This repository contains two tools designed to enhance text-to-SQL workflows. The tools assist in retrieving schema details, including table names, column names, data types, and sample values and second one to execute the SQL query. These tools are integrated with the `[github/tools-agent](https://github.com/sreejith3534/Text2SQL-Agentic-Flow-Multi-Agents-using-AutoGen)` framework and registered using the MCP `@tool` decorator.

The goal is to enable an agent to call these tools, retrieve relevant schema information, and facilitate end-to-end text-to-SQL execution.

## Getting Started

### Prerequisites
Ensure you have Python installed, along with the necessary dependencies. Install the dependencies using:
```bash
pip install -r requirements.txt
```

### Running in Inspection Mode
To start the MCP server in inspection mode, use the following command:
```bash
mcp dev tool_calling.py
```
This will allow you to inspect and test tool execution via the MCP inspector.

### Listing and Executing Tools
The MCP `@tool` decorator enables tools to be listed and executed. You can view available tools and trigger them through MCP inspector.

## Next Steps
This setup will be leveraged to enable an agent to dynamically call the schema retrieval tool and facilitate full text-to-SQL execution.

Stay tuned for further updates!

