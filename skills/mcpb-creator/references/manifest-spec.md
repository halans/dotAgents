# MCPB Manifest Specification

Complete specification for `manifest.json` structure and field definitions.

## Schema

```json
{
  "name": "string",
  "version": "string",
  "description": "string",
  "author": "string (optional)",
  "license": "string (optional)",
  "homepage": "string (optional)",
  "server": {
    "command": "string",
    "args": ["string"],
    "env": {
      "KEY": "value"
    }
  },
  "tools": [
    {
      "name": "string",
      "description": "string",
      "inputSchema": {
        "type": "object",
        "properties": {},
        "required": []
      }
    }
  ],
  "resources": [
    {
      "uri": "string",
      "name": "string",
      "description": "string (optional)",
      "mimeType": "string (optional)"
    }
  ]
}
```

## Required Fields

### name
- **Type**: string
- **Format**: lowercase, alphanumeric, hyphens allowed
- **Example**: `"hello-world"`, `"file-system-tools"`
- **Purpose**: Unique identifier for the bundle

### version
- **Type**: string
- **Format**: Semantic versioning (MAJOR.MINOR.PATCH)
- **Example**: `"1.0.0"`, `"0.2.1"`
- **Purpose**: Bundle version for compatibility tracking

### description
- **Type**: string
- **Max length**: 500 characters recommended
- **Example**: `"Provides basic file system operations via MCP tools"`
- **Purpose**: Human-readable explanation of bundle capabilities

### server
- **Type**: object
- **Purpose**: Defines how to start the MCP server process

#### server.command
- **Type**: string
- **Example**: `"node"`, `"python3"`, `"./binary"`
- **Purpose**: Executable to run (must be in PATH or relative to bundle)

#### server.args
- **Type**: array of strings
- **Example**: `["server/index.js"]`, `["server.py", "--port", "8080"]`
- **Purpose**: Command-line arguments passed to the executable

#### server.env (optional)
- **Type**: object (key-value pairs)
- **Example**: `{"NODE_ENV": "production", "LOG_LEVEL": "info"}`
- **Purpose**: Environment variables for the server process

## Optional Fields

### author
- **Type**: string
- **Example**: `"Jane Smith <jane@example.com>"`
- **Purpose**: Bundle creator attribution

### license
- **Type**: string
- **Example**: `"MIT"`, `"Apache-2.0"`
- **Purpose**: Software license identifier

### homepage
- **Type**: string (URL)
- **Example**: `"https://github.com/username/bundle-name"`
- **Purpose**: Link to documentation or source code

### tools
- **Type**: array of tool objects
- **Purpose**: Declare tools (functions) the server implements

#### Tool Object Fields

**name** (required)
- **Type**: string
- **Format**: lowercase, alphanumeric, underscores allowed
- **Example**: `"get_file_content"`, `"search_files"`

**description** (required)
- **Type**: string
- **Example**: `"Read the contents of a file at the given path"`
- **Purpose**: Explain what the tool does for the AI

**inputSchema** (required)
- **Type**: JSON Schema object
- **Purpose**: Define expected input parameters
- **Must include**: `"type": "object"`
- **Should include**: `properties` and `required` arrays

Example inputSchema:
```json
{
  "type": "object",
  "properties": {
    "path": {
      "type": "string",
      "description": "File path to read"
    },
    "encoding": {
      "type": "string",
      "enum": ["utf-8", "ascii", "base64"],
      "default": "utf-8"
    }
  },
  "required": ["path"]
}
```

### resources
- **Type**: array of resource objects
- **Purpose**: Declare data sources the server provides

#### Resource Object Fields

**uri** (required)
- **Type**: string
- **Format**: URI format (file://, http://, custom scheme)
- **Example**: `"file:///path/to/data"`, `"database://table"`

**name** (required)
- **Type**: string
- **Example**: `"Project Files"`, `"Database Records"`

**description** (optional)
- **Type**: string
- **Purpose**: Explain what the resource contains

**mimeType** (optional)
- **Type**: string
- **Example**: `"text/plain"`, `"application/json"`
- **Purpose**: Hint at content type

## Validation Rules

### Bundle Name
- Must be unique within the host environment
- Should use kebab-case (lowercase with hyphens)
- No spaces or special characters except hyphens
- Length: 3-64 characters

### Version Numbers
- Must follow semantic versioning
- Three components: MAJOR.MINOR.PATCH
- All components must be non-negative integers
- Example valid: `1.0.0`, `0.1.2`, `2.3.10`
- Example invalid: `1.0`, `v1.0.0`, `1.0.0-beta`

### Tool Names
- Must be unique within the bundle
- Should use snake_case (lowercase with underscores)
- Should be descriptive verbs or verb phrases
- Length: 3-64 characters

### Input Schemas
- Must be valid JSON Schema (draft 7 or later)
- Root type must be `"object"`
- Should include `properties` for parameters
- Should include `required` array for mandatory fields
- Should include `description` for each property

## Complete Example

```json
{
  "name": "file-tools",
  "version": "1.0.0",
  "description": "Basic file system operations including read, write, and list",
  "author": "Development Team <dev@example.com>",
  "license": "MIT",
  "homepage": "https://github.com/example/file-tools",
  "server": {
    "command": "node",
    "args": ["server/index.js"],
    "env": {
      "NODE_ENV": "production"
    }
  },
  "tools": [
    {
      "name": "read_file",
      "description": "Read the contents of a file",
      "inputSchema": {
        "type": "object",
        "properties": {
          "path": {
            "type": "string",
            "description": "Absolute or relative file path"
          }
        },
        "required": ["path"]
      }
    },
    {
      "name": "write_file",
      "description": "Write content to a file",
      "inputSchema": {
        "type": "object",
        "properties": {
          "path": {
            "type": "string",
            "description": "File path to write to"
          },
          "content": {
            "type": "string",
            "description": "Content to write"
          }
        },
        "required": ["path", "content"]
      }
    }
  ],
  "resources": [
    {
      "uri": "file:///workspace",
      "name": "Workspace Files",
      "description": "All files in the current workspace",
      "mimeType": "text/plain"
    }
  ]
}
```

## Common Mistakes

1. **Missing required fields**: Ensure name, version, description, and server.command are present
2. **Invalid tool names**: Use snake_case, not camelCase or kebab-case
3. **Missing inputSchema type**: Always include `"type": "object"` in inputSchema
4. **Invalid version**: Use semantic versioning (X.Y.Z), not other formats
5. **Wrong command path**: Command must be executable and in PATH or relative to bundle
6. **Stdout pollution**: Server must write only JSON-RPC to stdout, logs go to stderr

## Validation Checklist

- [ ] All required fields present (name, version, description, server.command)
- [ ] Valid JSON syntax (no trailing commas, proper quotes)
- [ ] Semantic version format (X.Y.Z)
- [ ] Bundle name uses kebab-case
- [ ] Tool names use snake_case
- [ ] Each tool has name, description, and inputSchema
- [ ] Each inputSchema has `"type": "object"`
- [ ] Server command is valid and executable
- [ ] No additional unknown fields in root object
