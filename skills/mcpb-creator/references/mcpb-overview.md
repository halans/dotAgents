# MCP Bundle (MCPB) Overview

Model Context Protocol Bundles (MCPB) provide a standardized way to package and distribute MCP servers. This document covers the core architecture and capabilities of MCPB.

## What is MCPB?

MCPB is a specification for packaging MCP servers into distributable bundles that can be easily installed and managed by MCP hosts. Each bundle is a directory containing:

- A manifest file (`manifest.json`) describing the bundle
- One or more MCP server implementations
- Dependencies and configuration
- Documentation and assets

## Key Concepts

### Bundle Structure

```
bundle-name/
├── manifest.json          # Required: Bundle metadata and configuration
├── server/               # Server implementation directory
│   ├── index.js         # Entry point for Node.js servers
│   ├── package.json     # Node.js dependencies
│   └── ...
└── README.md            # Optional: Documentation
```

### Manifest File

The `manifest.json` is the core of every bundle. It defines:

- **Bundle metadata** (name, version, description, author)
- **Server configuration** (command, arguments, environment)
- **Tool definitions** (capabilities exposed by the server)
- **Resource definitions** (data sources the server provides)
- **Security settings** (permissions, network access)

### MCP Protocol

MCPB bundles implement the Model Context Protocol, which defines:

- **Tools**: Functions that the AI can call to perform actions
- **Resources**: Data sources that provide context
- **Prompts**: Pre-defined prompt templates
- **Sampling**: Request/response handling for AI interactions

Communication happens via JSON-RPC 2.0 over stdio (standard input/output).

## Bundle Lifecycle

1. **Discovery**: Host scans for bundles in configured directories
2. **Loading**: Host reads and validates manifest.json
3. **Installation**: Host resolves and installs dependencies
4. **Startup**: Host spawns server process using manifest command
5. **Communication**: Server and host exchange JSON-RPC messages via stdio
6. **Shutdown**: Host terminates server process gracefully

## Transport Layer

MCPB uses stdio transport for communication:

- **Server reads** from stdin (JSON-RPC requests from host)
- **Server writes** to stdout (JSON-RPC responses to host)
- **Server logs** to stderr (debugging and error messages)

This design makes bundles:
- Simple to implement (no network setup)
- Secure by default (no external network access)
- Easy to debug (logs separate from protocol messages)

## Security Model

MCPB bundles run locally on the user's machine with:

- **Process isolation**: Each bundle runs in its own process
- **Permission model**: Manifest declares required capabilities
- **Resource limits**: Hosts can enforce CPU, memory, and timeout constraints
- **File system access**: By default, servers can only access their own directory

## Integration Patterns

### Tool-Based Bundles

Expose actions the AI can perform:
```javascript
{
  "name": "calculator",
  "description": "Perform mathematical calculations",
  "inputSchema": {
    "type": "object",
    "properties": {
      "expression": { "type": "string" }
    }
  }
}
```

### Resource-Based Bundles

Provide data sources for context:
```javascript
{
  "uri": "file:///path/to/data",
  "name": "Project Files",
  "mimeType": "text/plain"
}
```

### Hybrid Bundles

Combine tools and resources for complete workflows.

## Best Practices

1. **Clear tool schemas**: Define precise input/output types
2. **Error handling**: Return structured errors with helpful messages
3. **Timeouts**: Implement reasonable execution limits
4. **Logging**: Write diagnostic info to stderr, not stdout
5. **Documentation**: Include usage examples in README.md
6. **Testing**: Validate manifest and test tool responses
7. **Dependencies**: Pin versions for reproducibility

## Development Workflow

1. Create bundle directory structure
2. Write manifest.json with bundle metadata
3. Implement MCP server with tool handlers
4. Test locally with MCP host
5. Document usage and configuration
6. Package and distribute

## Common Patterns

### Hello World Bundle

Minimal bundle with a single greeting tool:
- Manifest declares one tool
- Server implements simple handler
- Returns JSON response

### File System Bundle

Tools for reading/writing files:
- Declares file system permissions
- Implements read/write/list operations
- Validates paths for security

### API Integration Bundle

Connect to external services:
- Manages API credentials
- Handles rate limiting
- Returns structured data

### Data Processing Bundle

Transform and analyze data:
- Accepts various input formats
- Performs computations
- Returns results or visualizations

## Resources

- Full specification: https://github.com/anthropics/mcpb/blob/main/README.md
- Manifest format: https://github.com/anthropics/mcpb/blob/main/MANIFEST.md
- Example bundles: https://github.com/anthropics/mcpb/tree/main/examples
- MCP SDK: https://github.com/modelcontextprotocol/sdk
