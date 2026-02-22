```skill
---
name: mcpb-creator
description: Guide for creating Model Context Protocol Bundles (MCPB). Use when users want to build MCP servers as distributable bundles with proper manifest structure, tool definitions, security measures, and best practices.
---

# MCPB Creator

This skill provides comprehensive guidance for creating production-ready Model Context Protocol Bundles (MCPB).

## About MCPB

Model Context Protocol Bundles (MCPB) are standardized packages for distributing MCP servers. Each bundle contains:

- **manifest.json**: Bundle metadata, tool definitions, and server configuration
- **Server implementation**: MCP protocol server (Node.js, Python, etc.)
- **Dependencies**: Package manager files (package.json, requirements.txt, etc.)
- **Documentation**: README with usage examples

MCPB bundles run locally, communicate via stdio (JSON-RPC), and provide tools that AI agents can call to perform actions or access resources.

## Core Principles

1. **Production-ready code**: Implement proper error handling, validation, and security
2. **Clear tool schemas**: Define precise input/output types with JSON Schema
3. **Defensive programming**: Validate all inputs, handle edge cases, return informative errors
4. **MCPB compliance**: Follow exact specifications for manifest structure and protocol communication
5. **Local execution**: Bundles run on the user's machine with file system access
6. **Stdio transport**: Server reads JSON-RPC from stdin, writes responses to stdout, logs to stderr

## Workflow

### Step 1: Understand Requirements

Gather detailed information about what the bundle should do:

- **What tools should the bundle provide?** (e.g., file operations, API calls, data processing)
- **What inputs do tools accept?** (parameters, types, validation rules)
- **What outputs do tools return?** (data structures, formats)
- **What resources does it need?** (file system access, network, external APIs)
- **What dependencies are required?** (npm packages, system commands)

### Step 2: Initialize Bundle Structure

Use the initialization script to create the bundle:

```bash
scripts/init_mcpb.py <bundle-name> --path <output-directory>
```

This creates:
```
bundle-name/
├── manifest.json          # Bundle metadata and tool definitions
├── package.json          # Node.js dependencies
├── server/
│   └── index.js         # MCP server implementation
├── README.md            # Documentation
└── .gitignore           # Git ignore rules
```

### Step 3: Define Tools in Manifest

Edit `manifest.json` to define your tools:

1. **Update bundle metadata**:
   - `name`: kebab-case identifier (must be unique)
   - `version`: Semantic versioning (0.1.0, 1.0.0, etc.)
   - `description`: Clear explanation of bundle purpose
   - `author`: Your name and email
   - `license`: Software license (MIT, Apache-2.0, etc.)

2. **Define tools array**: Each tool needs:
   - `name`: snake_case identifier (e.g., `read_file`, `search_data`)
   - `description`: What the tool does (for AI to understand when to use it)
   - `inputSchema`: JSON Schema defining parameters (must have `"type": "object"`)

**Example tool definition**:
```json
{
  "name": "process_data",
  "description": "Process input data and return structured results",
  "inputSchema": {
    "type": "object",
    "properties": {
      "data": {
        "type": "string",
        "description": "Raw data to process"
      },
      "format": {
        "type": "string",
        "enum": ["json", "csv", "xml"],
        "description": "Output format"
      }
    },
    "required": ["data"]
  }
}
```

### Step 4: Implement Server

Edit `server/index.js` to implement the MCP protocol:

1. **Update tool definitions**: Copy tool schemas from manifest to the `TOOLS` array
2. **Implement tool handlers**: Create async function for each tool
3. **Add tool routing**: Add case to switch statement linking tool name to handler
4. **Implement validation**: Validate inputs before processing
5. **Implement error handling**: Use try-catch and return informative errors
6. **Add logging**: Use `console.error()` for debugging (never `console.log()`)

**Handler pattern**:
```javascript
async function handleToolName(args) {
  console.error("[INFO] tool_name called with:", args);
  
  // Validate inputs
  if (!args.requiredParam || typeof args.requiredParam !== 'string') {
    throw new Error("Invalid parameter: requiredParam must be a string");
  }
  
  try {
    // Implement tool logic
    const result = await performOperation(args);
    
    // Return structured response
    return {
      content: [
        {
          type: "text",
          text: JSON.stringify(result, null, 2)
        }
      ]
    };
  } catch (error) {
    console.error("[ERROR] Operation failed:", error);
    throw new Error(`Operation failed: ${error.message}`);
  }
}
```

### Step 5: Add Security Measures

Implement security best practices:

1. **Input validation**: Check all parameters for type, format, and constraints
2. **Path validation**: Prevent directory traversal attacks (sanitize file paths)
3. **Resource limits**: Add timeouts for long-running operations
4. **Error sanitization**: Don't expose sensitive information in error messages
5. **Environment variables**: Use env vars for credentials, never hardcode secrets

**Path validation example**:
```javascript
import path from 'path';

const WORKSPACE_DIR = process.env.WORKSPACE_DIR || process.cwd();

function validatePath(userPath) {
  // Prevent directory traversal
  if (userPath.includes('..')) {
    throw new Error("Invalid path: directory traversal not allowed");
  }
  
  // Resolve to absolute path within workspace
  const resolvedPath = path.resolve(WORKSPACE_DIR, userPath);
  
  // Ensure resolved path is within workspace
  if (!resolvedPath.startsWith(WORKSPACE_DIR)) {
    throw new Error("Access denied: path outside workspace");
  }
  
  return resolvedPath;
}
```

**Timeout example**:
```javascript
function withTimeout(promise, timeoutMs) {
  return Promise.race([
    promise,
    new Promise((_, reject) =>
      setTimeout(() => reject(new Error('Operation timeout')), timeoutMs)
    )
  ]);
}

async function handleLongOperation(args) {
  const result = await withTimeout(
    performOperation(args),
    30000 // 30 second timeout
  );
  return {
    content: [{ type: "text", text: JSON.stringify(result) }]
  };
}
```

### Step 6: Update Documentation

Edit `README.md` to document:

1. **Bundle description**: What it does and why it's useful
2. **Installation steps**: How to install dependencies
3. **Tool documentation**: For each tool:
   - What it does
   - Input parameters (types, constraints, defaults)
   - Output format
   - Usage examples
4. **Configuration**: Environment variables, settings
5. **Development guide**: How to add new tools, run tests

### Step 7: Validate and Test

1. **Validate manifest**:
```bash
scripts/validate_mcpb.py <bundle-directory>
```

2. **Install dependencies**:
```bash
cd <bundle-directory>
npm install
```

3. **Test server startup**:
```bash
npm start
```
The server should start without errors and log "[INFO] Server running and ready for requests"

4. **Test tool calls** using an MCP host or manual JSON-RPC:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list"
}
```

Expected response:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "tools": [...]
  }
}
```

5. **Test error handling**: Call tools with invalid inputs and verify errors are clear

### Step 8: Finalize

1. **Review checklist**:
   - [ ] Manifest validates successfully
   - [ ] All tools have clear descriptions and schemas
   - [ ] Input validation implemented for all parameters
   - [ ] Error messages are informative and safe
   - [ ] Timeouts for long operations
   - [ ] No `console.log()` in code (only `console.error()`)
   - [ ] Security measures in place
   - [ ] Dependencies pinned in package.json
   - [ ] README documents all tools with examples
   - [ ] Server starts and responds to tool calls

2. **Package for distribution**: Add to version control, publish to registry, or share directory

## Reference Materials

- **references/mcpb-overview.md**: MCPB architecture, capabilities, and integration patterns
- **references/manifest-spec.md**: Complete manifest.json structure and field definitions
- **references/implementation-guide.md**: Best practices, security, testing, and common patterns

## Common Tool Patterns

### File Operations
```javascript
async function handleReadFile(args) {
  const safePath = validatePath(args.path);
  const content = await fs.readFile(safePath, 'utf-8');
  return {
    content: [{
      type: "text",
      text: content
    }]
  };
}
```

### Data Processing
```javascript
async function handleProcessData(args) {
  const parsed = JSON.parse(args.data);
  const processed = transformData(parsed);
  return {
    content: [{
      type: "text",
      text: JSON.stringify(processed, null, 2)
    }]
  };
}
```

### External API Calls
```javascript
async function handleApiCall(args) {
  const response = await withTimeout(
    fetch(args.url, {
      method: args.method || 'GET',
      headers: { 'Authorization': `Bearer ${process.env.API_KEY}` }
    }),
    10000
  );
  const data = await response.json();
  return {
    content: [{
      type: "text",
      text: JSON.stringify(data, null, 2)
    }]
  };
}
```

### List/Search Operations
```javascript
async function handleSearch(args) {
  const results = await searchOperation(args.query);
  return {
    content: [{
      type: "text",
      text: JSON.stringify({
        query: args.query,
        count: results.length,
        results: results
      }, null, 2)
    }]
  };
}
```

## Scripts

### Initialize Bundle
```bash
scripts/init_mcpb.py <bundle-name> [--path <directory>]
```
Creates new bundle with template structure.

### Validate Bundle
```bash
scripts/validate_mcpb.py <bundle-directory>
```
Validates manifest.json structure and required fields.

## Best Practices Summary

1. **Tool naming**: Use snake_case for tool names, kebab-case for bundle name
2. **Descriptions**: Write clear descriptions for AI to understand tool purpose
3. **Schemas**: Define precise inputSchema with types, descriptions, and required fields
4. **Validation**: Check all inputs before processing
5. **Errors**: Return structured errors with helpful context
6. **Logging**: Use stderr for logs, stdout only for JSON-RPC
7. **Security**: Validate paths, sanitize inputs, use timeouts
8. **Testing**: Test with valid/invalid inputs, edge cases
9. **Documentation**: Include examples for every tool
10. **Dependencies**: Pin versions in package.json for reproducibility

## Troubleshooting

### Server won't start
- Check manifest.json syntax (valid JSON)
- Verify server.command points to valid executable
- Verify server.args[0] points to existing file
- Check for syntax errors in server/index.js
- Run `npm install` to install dependencies

### Tool calls fail
- Verify tool name matches between manifest and server
- Check inputSchema validation in handler
- Look for errors in stderr output
- Test with exact schema-compliant inputs

### Validation errors
- Run `scripts/validate_mcpb.py` for specific issues
- Check manifest field names and types
- Verify semantic versioning format
- Ensure tool names use snake_case

### Response format errors
- Ensure responses follow MCP schema
- Must return object with `content` array
- Each content item needs `type` and `text` fields
- Only write JSON-RPC to stdout, logs to stderr
```