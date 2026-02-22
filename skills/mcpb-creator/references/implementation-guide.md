# MCPB Implementation Guide

Best practices, patterns, and guidelines for building production-ready MCP bundles.

## MCP Server Implementation

### Using the MCP SDK

Install the official SDK:
```bash
npm install @modelcontextprotocol/sdk
```

Basic server structure:
```javascript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { CallToolRequestSchema, ListToolsRequestSchema } from "@modelcontextprotocol/sdk/types.js";

const server = new Server({
  name: "bundle-name",
  version: "1.0.0"
}, {
  capabilities: {
    tools: {}
  }
});

// Register tool handlers
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "tool_name",
        description: "Tool description",
        inputSchema: {
          type: "object",
          properties: {},
          required: []
        }
      }
    ]
  };
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  
  switch (name) {
    case "tool_name":
      return await handleToolName(args);
    default:
      throw new Error(`Unknown tool: ${name}`);
  }
});

// Start the server
const transport = new StdioServerTransport();
await server.connect(transport);
```

### Protocol Communication

#### Request Format (from host)
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "tool_name",
    "arguments": {
      "param1": "value1"
    }
  }
}
```

#### Response Format (from server)
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Result data"
      }
    ]
  }
}
```

#### Error Response
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32600,
    "message": "Invalid request",
    "data": {
      "details": "Additional context"
    }
  }
}
```

## Error Handling

### Standard Error Codes

```javascript
const ErrorCodes = {
  PARSE_ERROR: -32700,
  INVALID_REQUEST: -32600,
  METHOD_NOT_FOUND: -32601,
  INVALID_PARAMS: -32602,
  INTERNAL_ERROR: -32603
};
```

### Best Practices

1. **Validate inputs**: Check parameters before processing
```javascript
function validateInput(args, schema) {
  if (!args.path || typeof args.path !== 'string') {
    throw new Error("Invalid 'path' parameter: must be a string");
  }
}
```

2. **Catch exceptions**: Wrap tool logic in try-catch
```javascript
async function handleTool(args) {
  try {
    const result = await performOperation(args);
    return {
      content: [{ type: "text", text: JSON.stringify(result) }]
    };
  } catch (error) {
    console.error("[ERROR]", error);
    throw new Error(`Operation failed: ${error.message}`);
  }
}
```

3. **Return structured errors**: Include helpful context
```javascript
catch (error) {
  if (error.code === 'ENOENT') {
    throw new Error(`File not found: ${args.path}`);
  } else if (error.code === 'EACCES') {
    throw new Error(`Permission denied: ${args.path}`);
  }
  throw error;
}
```

## Security Measures

### Input Validation

Always validate and sanitize inputs:
```javascript
function validatePath(path) {
  // Prevent directory traversal
  if (path.includes('..')) {
    throw new Error("Invalid path: directory traversal not allowed");
  }
  
  // Ensure absolute path or relative to safe directory
  const safePath = resolveSafePath(path);
  
  return safePath;
}
```

### File System Access

Restrict access to safe directories:
```javascript
import path from 'path';

const SAFE_BASE = process.env.WORKSPACE_DIR || process.cwd();

function resolveSafePath(userPath) {
  const resolved = path.resolve(SAFE_BASE, userPath);
  
  // Ensure resolved path is within safe base
  if (!resolved.startsWith(SAFE_BASE)) {
    throw new Error("Access denied: path outside workspace");
  }
  
  return resolved;
}
```

### Environment Variables

Never expose sensitive data:
```javascript
// Good: Use environment variables for credentials
const apiKey = process.env.API_KEY;

// Bad: Hardcode credentials
const apiKey = "sk-secret123"; // Never do this!
```

## Timeout Management

### Implementation

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
  try {
    const result = await withTimeout(
      performOperation(args),
      30000 // 30 second timeout
    );
    return { content: [{ type: "text", text: JSON.stringify(result) }] };
  } catch (error) {
    if (error.message === 'Operation timeout') {
      throw new Error("Operation exceeded 30 second limit");
    }
    throw error;
  }
}
```

## Logging and Debugging

### Proper Logging

Write logs to stderr, never stdout:
```javascript
// Good: Logs to stderr
console.error("[INFO] Server starting...");
console.error("[DEBUG] Tool called:", toolName);

// Bad: Pollutes stdout (breaks JSON-RPC)
console.log("Server starting"); // Never do this!
```

### Log Levels

```javascript
const LOG_LEVEL = process.env.LOG_LEVEL || 'info';

function log(level, ...args) {
  const levels = ['error', 'warn', 'info', 'debug'];
  if (levels.indexOf(level) <= levels.indexOf(LOG_LEVEL)) {
    console.error(`[${level.toUpperCase()}]`, ...args);
  }
}

// Usage
log('info', 'Server started');
log('debug', 'Tool called with args:', args);
log('error', 'Operation failed:', error);
```

## Tool Response Patterns

### Simple Text Response

```javascript
return {
  content: [
    {
      type: "text",
      text: "Operation completed successfully"
    }
  ]
};
```

### Structured Data Response

```javascript
const data = { files: ['a.txt', 'b.txt'], count: 2 };

return {
  content: [
    {
      type: "text",
      text: JSON.stringify(data, null, 2)
    }
  ]
};
```

### Multiple Content Items

```javascript
return {
  content: [
    {
      type: "text",
      text: "Found 3 files:"
    },
    {
      type: "text",
      text: JSON.stringify(fileList, null, 2)
    }
  ]
};
```

## Testing Strategies

### Unit Tests

Test individual tool handlers:
```javascript
import { describe, it, expect } from 'vitest';

describe('read_file tool', () => {
  it('should read file contents', async () => {
    const result = await handleReadFile({ path: 'test.txt' });
    expect(result.content[0].text).toContain('expected content');
  });
  
  it('should throw error for missing file', async () => {
    await expect(
      handleReadFile({ path: 'missing.txt' })
    ).rejects.toThrow('File not found');
  });
});
```

### Integration Tests

Test full server lifecycle:
```javascript
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

async function testServer() {
  const transport = new StdioClientTransport({
    command: "node",
    args: ["server/index.js"]
  });
  
  const client = new Client({
    name: "test-client",
    version: "1.0.0"
  }, {
    capabilities: {}
  });
  
  await client.connect(transport);
  
  // Test listing tools
  const tools = await client.listTools();
  console.log("Available tools:", tools);
  
  // Test calling a tool
  const result = await client.callTool({
    name: "tool_name",
    arguments: { param: "value" }
  });
  console.log("Tool result:", result);
  
  await client.close();
}
```

### Manifest Validation

Validate manifest.json programmatically:
```javascript
import fs from 'fs';

function validateManifest(manifestPath) {
  const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf-8'));
  
  // Check required fields
  const required = ['name', 'version', 'description', 'server'];
  for (const field of required) {
    if (!manifest[field]) {
      throw new Error(`Missing required field: ${field}`);
    }
  }
  
  // Validate version format
  if (!/^\d+\.\d+\.\d+$/.test(manifest.version)) {
    throw new Error(`Invalid version format: ${manifest.version}`);
  }
  
  // Validate tools
  if (manifest.tools) {
    for (const tool of manifest.tools) {
      if (!tool.name || !tool.description || !tool.inputSchema) {
        throw new Error(`Invalid tool definition: ${JSON.stringify(tool)}`);
      }
    }
  }
  
  console.log("Manifest validation passed");
}
```

## Performance Optimization

### Async Operations

Use async/await for I/O operations:
```javascript
async function handleBatchOperation(args) {
  // Good: Parallel execution
  const results = await Promise.all(
    args.files.map(file => readFile(file))
  );
  
  // Bad: Sequential execution
  // const results = [];
  // for (const file of args.files) {
  //   results.push(await readFile(file));
  // }
  
  return { content: [{ type: "text", text: JSON.stringify(results) }] };
}
```

### Caching

Cache expensive operations:
```javascript
const cache = new Map();

async function handleWithCache(args) {
  const cacheKey = JSON.stringify(args);
  
  if (cache.has(cacheKey)) {
    log('debug', 'Cache hit');
    return cache.get(cacheKey);
  }
  
  const result = await expensiveOperation(args);
  cache.set(cacheKey, result);
  
  return result;
}
```

## Deployment Checklist

- [ ] Manifest.json is valid and complete
- [ ] All tools have clear descriptions and schemas
- [ ] Input validation implemented for all parameters
- [ ] Error handling with informative messages
- [ ] Timeouts for long-running operations
- [ ] Logging to stderr only (stdout reserved for JSON-RPC)
- [ ] Security measures (path validation, no credential exposure)
- [ ] Dependencies pinned in package.json
- [ ] README.md with usage examples
- [ ] Tests pass and cover core functionality
- [ ] Server starts successfully with manifest command
- [ ] Tool calls return properly structured responses

## Common Pitfalls

1. **Writing to stdout**: All logs must go to stderr
2. **Missing error handlers**: Unhandled exceptions crash the server
3. **Invalid JSON responses**: Must follow MCP response schema
4. **Blocking operations**: Use async for I/O operations
5. **Security holes**: Always validate and sanitize user inputs
6. **Poor error messages**: Include context to help users debug
7. **No timeouts**: Long operations should have limits
8. **Hardcoded paths**: Use environment variables or relative paths
