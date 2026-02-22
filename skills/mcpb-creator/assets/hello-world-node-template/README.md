# Hello World MCP Bundle

A simple MCP bundle demonstrating the basic structure and implementation patterns for Model Context Protocol servers.

## Overview

This bundle provides a single `greet` tool that generates personalized greeting messages. It serves as a reference implementation showing:

- Proper MCPB bundle structure
- MCP SDK usage for server implementation
- Tool definition and registration
- Input validation and error handling
- Structured JSON responses
- Proper logging practices (stderr for logs, stdout for protocol)

## Installation

1. Install dependencies:
```bash
npm install
```

2. Test the server:
```bash
npm start
```

The server will start and wait for JSON-RPC requests on stdin.

## Tools

### greet

Generate a personalized greeting message with customizable style.

**Input:**
- `name` (string, required): The name of the person to greet
- `style` (string, optional): The greeting style - one of:
  - `"formal"`: Professional, respectful greeting
  - `"casual"`: Friendly, informal greeting (default)
  - `"enthusiastic"`: Excited, energetic greeting with emoji

**Output:**
JSON object containing:
- `greeting`: The generated greeting message
- `name`: The name that was greeted
- `style`: The style that was used
- `timestamp`: ISO timestamp of when the greeting was generated

**Example Request:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "greet",
    "arguments": {
      "name": "Alice",
      "style": "enthusiastic"
    }
  }
}
```

**Example Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "{\n  \"greeting\": \"Hello Alice! 🎉 So excited to meet you!!!\",\n  \"name\": \"Alice\",\n  \"style\": \"enthusiastic\",\n  \"timestamp\": \"2024-01-15T10:30:00.000Z\"\n}"
      }
    ]
  }
}
```

## Project Structure

```
hello-world/
├── manifest.json          # Bundle metadata and tool definitions
├── package.json          # Node.js dependencies and scripts
├── server/
│   └── index.js         # MCP server implementation
├── README.md            # This file
└── .gitignore           # Git ignore rules
```

## Development

### Adding New Tools

1. **Update manifest.json**: Add tool definition to the `tools` array
```json
{
  "name": "your_tool",
  "description": "What your tool does",
  "inputSchema": {
    "type": "object",
    "properties": {
      "param": {
        "type": "string",
        "description": "Parameter description"
      }
    },
    "required": ["param"]
  }
}
```

2. **Update server/index.js**:
   - Add tool to `TOOLS` array
   - Create handler function (e.g., `handleYourTool`)
   - Add case to switch statement in `CallToolRequestSchema` handler

3. **Implement handler**:
```javascript
async function handleYourTool(args) {
  // Validate inputs
  if (!args.param) {
    throw new Error("Missing required parameter: 'param'");
  }

  // Implement logic
  const result = performOperation(args);

  // Return structured response
  return {
    content: [
      {
        type: "text",
        text: JSON.stringify(result, null, 2)
      }
    ]
  };
}
```

### Testing

Manual testing using stdio:

1. Start the server:
```bash
npm start
```

2. Send JSON-RPC request via stdin:
```json
{"jsonrpc":"2.0","id":1,"method":"tools/list"}
```

3. View response on stdout and logs on stderr

### Best Practices Demonstrated

1. **Input Validation**: All parameters are validated for type, presence, and constraints
2. **Error Handling**: Try-catch blocks with informative error messages
3. **Logging**: Uses `console.error()` for logs (stderr), never pollutes stdout
4. **Structured Responses**: Returns properly formatted MCP tool responses
5. **Documentation**: Clear comments explaining code functionality
6. **Schema Compliance**: Tool definitions match between manifest and server
7. **Graceful Shutdown**: Handles SIGINT/SIGTERM signals

### Common Patterns

**Simple validation:**
```javascript
if (!args.param || typeof args.param !== 'string') {
  throw new Error("Invalid parameter: param must be a string");
}
```

**Enum validation:**
```javascript
const validValues = ["opt1", "opt2", "opt3"];
if (!validValues.includes(args.param)) {
  throw new Error(`Invalid value. Must be one of: ${validValues.join(", ")}`);
}
```

**Structured response:**
```javascript
return {
  content: [
    {
      type: "text",
      text: JSON.stringify(resultData, null, 2)
    }
  ]
};
```

## Troubleshooting

**Server won't start:**
- Check that Node.js is installed: `node --version`
- Verify dependencies are installed: `npm install`
- Look for syntax errors in server/index.js
- Check stderr output for error messages

**Tool calls fail:**
- Verify request matches JSON-RPC 2.0 format
- Check that tool name matches definition
- Ensure arguments match inputSchema
- Look for validation errors in stderr

**No response received:**
- Ensure request is sent to stdin
- Check that stdout is not buffered
- Verify server is running and connected
- Look for logs in stderr

## License

MIT
