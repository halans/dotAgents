#!/usr/bin/env python3
"""
MCPB Initializer - Creates a new MCP Bundle from template

Usage:
    init_mcpb.py <bundle-name> [--path <path>] [--template <template-name>]

Examples:
    init_mcpb.py my-tools --path bundles
    init_mcpb.py data-processor --path ~/mcpb --template hello-world
    init_mcpb.py api-client --template hello-world

Templates:
    hello-world-node: Basic Node.js MCP server with a greeting tool (default)
"""

import sys
import os
import json
import shutil
from pathlib import Path


MANIFEST_TEMPLATE = {
    "name": "{bundle_name}",
    "version": "0.1.0",
    "description": "TODO: Describe what this MCP bundle does and what tools it provides",
    "author": "TODO: Your Name <your.email@example.com>",
    "license": "MIT",
    "server": {
        "command": "node",
        "args": ["server/index.js"],
        "env": {}
    },
    "tools": [
        {
            "name": "example_tool",
            "description": "TODO: Replace with your actual tool description",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "TODO: Replace with your parameter description"
                    }
                },
                "required": ["message"]
            }
        }
    ]
}

SERVER_INDEX_TEMPLATE = '''import {{ Server }} from "@modelcontextprotocol/sdk/server/index.js";
import {{ StdioServerTransport }} from "@modelcontextprotocol/sdk/server/stdio.js";
import {{
  CallToolRequestSchema,
  ListToolsRequestSchema,
}} from "@modelcontextprotocol/sdk/types.js";

const server = new Server(
  {{
    name: "{bundle_name}",
    version: "0.1.0",
  }},
  {{
    capabilities: {{
      tools: {{}},
    }},
  }}
);

// Tool definitions
const TOOLS = [
  {{
    name: "example_tool",
    description: "TODO: Replace with your actual tool description",
    inputSchema: {{
      type: "object",
      properties: {{
        message: {{
          type: "string",
          description: "TODO: Replace with your parameter description",
        }},
      }},
      required: ["message"],
    }},
  }},
];

// List available tools
server.setRequestHandler(ListToolsRequestSchema, async () => {{
  return {{
    tools: TOOLS,
  }};
}});

// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {{
  const {{ name, arguments: args }} = request.params;

  try {{
    switch (name) {{
      case "example_tool":
        return handleExampleTool(args);
      default:
        throw new Error(`Unknown tool: ${{name}}`);
    }}
  }} catch (error) {{
    console.error(`[ERROR] Tool ${{name}} failed:`, error);
    throw error;
  }}
}});

// Tool handlers
async function handleExampleTool(args) {{
  console.error("[INFO] example_tool called with:", args);
  
  // TODO: Implement your tool logic here
  const result = {{
    message: args.message,
    response: "TODO: Replace with actual tool output",
  }};

  return {{
    content: [
      {{
        type: "text",
        text: JSON.stringify(result, null, 2),
      }},
    ],
  }};
}}

// Start the server
async function main() {{
  console.error("[INFO] Starting {bundle_name} MCP server...");
  
  const transport = new StdioServerTransport();
  await server.connect(transport);
  
  console.error("[INFO] Server running and ready for requests");
}}

main().catch((error) => {{
  console.error("[FATAL] Server failed to start:", error);
  process.exit(1);
}});
'''

PACKAGE_JSON_TEMPLATE = {
    "name": "{bundle_name}",
    "version": "0.1.0",
    "description": "MCP Bundle: {bundle_name}",
    "type": "module",
    "main": "server/index.js",
    "scripts": {
        "start": "node server/index.js",
        "test": "echo \\"TODO: Add tests\\" && exit 1"
    },
    "dependencies": {
        "@modelcontextprotocol/sdk": "^0.5.0"
    },
    "keywords": ["mcp", "mcpb", "model-context-protocol"],
    "author": "TODO: Your Name",
    "license": "MIT"
}

README_TEMPLATE = '''# {bundle_title}

TODO: Brief description of what this MCP bundle does.

## Installation

1. Install dependencies:
```bash
npm install
```

2. Test the server:
```bash
npm start
```

## Tools

### example_tool

TODO: Describe what this tool does.

**Input:**
- `message` (string, required): TODO: Describe this parameter

**Output:**
TODO: Describe the output format

**Example:**
```json
{{
  "name": "example_tool",
  "arguments": {{
    "message": "Hello, world!"
  }}
}}
```

## Configuration

TODO: Document any environment variables or configuration options.

## Development

### Project Structure

```
{bundle_name}/
├── manifest.json          # Bundle metadata and tool definitions
├── package.json          # Node.js dependencies
├── server/
│   └── index.js         # MCP server implementation
└── README.md            # This file
```

### Adding New Tools

1. Update `manifest.json` with the tool definition
2. Add the tool to the `TOOLS` array in `server/index.js`
3. Implement the handler function
4. Add the case to the switch statement in the request handler

### Testing

TODO: Add testing instructions

## License

TODO: Specify license
'''

GITIGNORE_TEMPLATE = '''node_modules/
.DS_Store
*.log
.env
'''


def title_case_name(name):
    """Convert hyphenated name to Title Case for display."""
    return ' '.join(word.capitalize() for word in name.split('-'))


def validate_bundle_name(name):
    """Validate bundle name follows conventions."""
    if not name:
        return False, "Bundle name cannot be empty"
    
    if not name.replace('-', '').replace('_', '').isalnum():
        return False, "Bundle name should only contain lowercase letters, numbers, and hyphens"
    
    if name[0].isdigit():
        return False, "Bundle name cannot start with a number"
    
    if len(name) < 3:
        return False, "Bundle name should be at least 3 characters"
    
    if len(name) > 64:
        return False, "Bundle name should not exceed 64 characters"
    
    return True, ""


def init_mcpb(bundle_name, output_path, template="hello-world-node"):
    """
    Initialize a new MCP bundle from template.

    Args:
        bundle_name: Name of the bundle (kebab-case)
        output_path: Path where the bundle directory should be created
        template: Template to use (default: hello-world-node)

    Returns:
        Path to created bundle directory, or None if error
    """
    # Validate bundle name
    valid, error = validate_bundle_name(bundle_name)
    if not valid:
        print(f"Error: {error}")
        return None

    # Create bundle directory
    bundle_dir = Path(output_path).resolve() / bundle_name

    if bundle_dir.exists():
        print(f"Error: Bundle directory already exists: {bundle_dir}")
        return None

    try:
        bundle_dir.mkdir(parents=True, exist_ok=False)
        print(f"Created bundle directory: {bundle_dir}")
    except Exception as e:
        print(f"Error creating directory: {e}")
        return None

    # Create server directory
    server_dir = bundle_dir / "server"
    try:
        server_dir.mkdir(exist_ok=False)
        print(f"Created server directory: {server_dir}")
    except Exception as e:
        print(f"Error creating server directory: {e}")
        return None

    bundle_title = title_case_name(bundle_name)

    # Create manifest.json
    manifest = json.loads(json.dumps(MANIFEST_TEMPLATE))
    manifest['name'] = bundle_name
    manifest_path = bundle_dir / "manifest.json"
    try:
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)
        print(f"Created manifest.json")
    except Exception as e:
        print(f"Error creating manifest.json: {e}")
        return None

    # Create server/index.js
    server_content = SERVER_INDEX_TEMPLATE.format(bundle_name=bundle_name)
    server_index_path = server_dir / "index.js"
    try:
        server_index_path.write_text(server_content)
        print(f"Created server/index.js")
    except Exception as e:
        print(f"Error creating server/index.js: {e}")
        return None

    # Create package.json
    package_json = json.loads(json.dumps(PACKAGE_JSON_TEMPLATE))
    package_json['name'] = bundle_name
    package_json['description'] = f"MCP Bundle: {bundle_name}"
    package_json_path = bundle_dir / "package.json"
    try:
        with open(package_json_path, 'w') as f:
            json.dump(package_json, f, indent=2)
        print(f"Created package.json")
    except Exception as e:
        print(f"Error creating package.json: {e}")
        return None

    # Create README.md
    readme_content = README_TEMPLATE.format(
        bundle_name=bundle_name,
        bundle_title=bundle_title
    )
    readme_path = bundle_dir / "README.md"
    try:
        readme_path.write_text(readme_content)
        print(f"Created README.md")
    except Exception as e:
        print(f"Error creating README.md: {e}")
        return None

    # Create .gitignore
    gitignore_path = bundle_dir / ".gitignore"
    try:
        gitignore_path.write_text(GITIGNORE_TEMPLATE)
        print(f"Created .gitignore")
    except Exception as e:
        print(f"Error creating .gitignore: {e}")
        return None

    print(f"\nBundle '{bundle_name}' initialized successfully at {bundle_dir}")
    print("\nNext steps:")
    print(f"1. cd {bundle_dir}")
    print("2. npm install")
    print("3. Update manifest.json with your tool definitions")
    print("4. Implement tool handlers in server/index.js")
    print("5. Test with: npm start")
    print("\nRefer to the mcpb-creator skill references for detailed guidance.")

    return bundle_dir


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    bundle_name = sys.argv[1]
    output_path = "."
    template = "hello-world-node"

    # Parse optional arguments
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == "--path" and i + 1 < len(sys.argv):
            output_path = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--template" and i + 1 < len(sys.argv):
            template = sys.argv[i + 1]
            i += 2
        else:
            print(f"Unknown argument: {sys.argv[i]}")
            print(__doc__)
            sys.exit(1)

    result = init_mcpb(bundle_name, output_path, template)
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
