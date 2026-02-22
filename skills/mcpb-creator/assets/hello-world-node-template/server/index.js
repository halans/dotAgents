import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

/**
 * Hello World MCP Server
 * 
 * A simple MCP server demonstrating:
 * - Basic server setup with the MCP SDK
 * - Tool definition and registration
 * - Input validation and error handling
 * - Proper logging (stderr) vs protocol communication (stdout)
 * - Structured JSON responses
 */

const server = new Server(
  {
    name: "hello-world",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// Tool definitions matching manifest.json
const TOOLS = [
  {
    name: "greet",
    description: "Generate a personalized greeting message. Accepts a name and optional greeting style.",
    inputSchema: {
      type: "object",
      properties: {
        name: {
          type: "string",
          description: "The name of the person to greet",
        },
        style: {
          type: "string",
          enum: ["formal", "casual", "enthusiastic"],
          description: "The style of greeting to use",
          default: "casual",
        },
      },
      required: ["name"],
    },
  },
];

/**
 * Handler for listing available tools
 */
server.setRequestHandler(ListToolsRequestSchema, async () => {
  console.error("[INFO] Listing available tools");
  return {
    tools: TOOLS,
  };
});

/**
 * Handler for tool execution
 */
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  
  console.error(`[INFO] Tool called: ${name}`);
  console.error(`[DEBUG] Arguments:`, JSON.stringify(args, null, 2));

  try {
    switch (name) {
      case "greet":
        return await handleGreet(args);
      
      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  } catch (error) {
    console.error(`[ERROR] Tool '${name}' failed:`, error.message);
    throw error;
  }
});

/**
 * Greet tool handler
 * 
 * Generates a personalized greeting based on name and style.
 * Demonstrates input validation, error handling, and structured responses.
 * 
 * @param {Object} args - Tool arguments
 * @param {string} args.name - Name to greet
 * @param {string} [args.style='casual'] - Greeting style
 * @returns {Object} MCP tool response with greeting message
 */
async function handleGreet(args) {
  // Input validation
  if (!args.name) {
    throw new Error("Missing required parameter: 'name'");
  }

  if (typeof args.name !== "string") {
    throw new Error("Parameter 'name' must be a string");
  }

  if (args.name.trim().length === 0) {
    throw new Error("Parameter 'name' cannot be empty");
  }

  // Default style if not provided
  const style = args.style || "casual";

  // Validate style enum
  const validStyles = ["formal", "casual", "enthusiastic"];
  if (!validStyles.includes(style)) {
    throw new Error(
      `Invalid style '${style}'. Must be one of: ${validStyles.join(", ")}`
    );
  }

  // Generate greeting based on style
  let greeting;
  const name = args.name.trim();

  switch (style) {
    case "formal":
      greeting = `Good day, ${name}. It is a pleasure to make your acquaintance.`;
      break;
    
    case "casual":
      greeting = `Hey ${name}! Nice to meet you.`;
      break;
    
    case "enthusiastic":
      greeting = `Hello ${name}! 🎉 So excited to meet you!!!`;
      break;
  }

  console.error(`[INFO] Generated ${style} greeting for: ${name}`);

  // Return structured MCP response
  return {
    content: [
      {
        type: "text",
        text: JSON.stringify({
          greeting: greeting,
          name: name,
          style: style,
          timestamp: new Date().toISOString(),
        }, null, 2),
      },
    ],
  };
}

/**
 * Start the MCP server
 */
async function main() {
  console.error("[INFO] Starting Hello World MCP server...");
  console.error("[INFO] MCP SDK version:", Server.version || "unknown");
  
  try {
    const transport = new StdioServerTransport();
    await server.connect(transport);
    
    console.error("[INFO] Server running and ready for requests");
    console.error("[INFO] Available tools:", TOOLS.map(t => t.name).join(", "));
  } catch (error) {
    console.error("[FATAL] Failed to start server:", error);
    process.exit(1);
  }
}

// Handle graceful shutdown
process.on("SIGINT", () => {
  console.error("[INFO] Received SIGINT, shutting down gracefully...");
  process.exit(0);
});

process.on("SIGTERM", () => {
  console.error("[INFO] Received SIGTERM, shutting down gracefully...");
  process.exit(0);
});

// Start the server
main().catch((error) => {
  console.error("[FATAL] Unhandled error:", error);
  process.exit(1);
});
