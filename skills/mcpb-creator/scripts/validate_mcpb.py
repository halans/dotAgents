#!/usr/bin/env python3
"""
Quick validation script for MCPB bundles - validates manifest.json structure
"""

import sys
import json
import re
from pathlib import Path


def validate_bundle(bundle_path):
    """Validate an MCPB bundle structure and manifest"""
    bundle_path = Path(bundle_path)

    if not bundle_path.exists():
        return False, f"Bundle directory not found: {bundle_path}"

    if not bundle_path.is_dir():
        return False, f"Path is not a directory: {bundle_path}"

    # Check for manifest.json
    manifest_path = bundle_path / "manifest.json"
    if not manifest_path.exists():
        return False, "No manifest.json file found in bundle directory"

    # Read and parse manifest
    try:
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON in manifest.json: {e}"
    except Exception as e:
        return False, f"Error reading manifest.json: {e}"

    # Define allowed top-level properties
    ALLOWED_PROPERTIES = {
        'name', 'version', 'description', 'author', 'license', 
        'homepage', 'server', 'tools', 'resources', 'prompts'
    }

    # Check for unexpected properties
    unexpected_keys = set(manifest.keys()) - ALLOWED_PROPERTIES
    if unexpected_keys:
        return False, (
            f"Unexpected key(s) in manifest: {', '.join(sorted(unexpected_keys))}. "
            f"Allowed properties are: {', '.join(sorted(ALLOWED_PROPERTIES))}"
        )

    # Check required fields
    required_fields = ['name', 'version', 'description', 'server']
    for field in required_fields:
        if field not in manifest:
            return False, f"Missing required field '{field}' in manifest"

    # Validate name
    name = manifest['name']
    if not isinstance(name, str):
        return False, f"Name must be a string, got {type(name).__name__}"
    
    name = name.strip()
    if not name:
        return False, "Name cannot be empty"
    
    # Check name format (lowercase, alphanumeric, hyphens)
    if not re.match(r'^[a-z0-9-]+$', name):
        return False, f"Name '{name}' should use kebab-case (lowercase letters, numbers, and hyphens only)"
    
    if name.startswith('-') or name.endswith('-') or '--' in name:
        return False, f"Name '{name}' cannot start/end with hyphen or contain consecutive hyphens"
    
    if len(name) < 3:
        return False, f"Name '{name}' is too short (minimum 3 characters)"
    
    if len(name) > 64:
        return False, f"Name '{name}' is too long (maximum 64 characters)"

    # Validate version (semantic versioning)
    version = manifest['version']
    if not isinstance(version, str):
        return False, f"Version must be a string, got {type(version).__name__}"
    
    if not re.match(r'^\d+\.\d+\.\d+$', version):
        return False, f"Version '{version}' must follow semantic versioning (MAJOR.MINOR.PATCH)"

    # Validate description
    description = manifest['description']
    if not isinstance(description, str):
        return False, f"Description must be a string, got {type(description).__name__}"
    
    description = description.strip()
    if not description:
        return False, "Description cannot be empty"
    
    if len(description) > 1000:
        return False, f"Description is too long ({len(description)} characters, maximum 1000)"

    # Validate server object
    server = manifest['server']
    if not isinstance(server, dict):
        return False, f"Server must be an object, got {type(server).__name__}"
    
    if 'command' not in server:
        return False, "Server object missing required 'command' field"
    
    if not isinstance(server['command'], str):
        return False, f"Server command must be a string, got {type(server['command']).__name__}"
    
    if 'args' in server:
        if not isinstance(server['args'], list):
            return False, f"Server args must be an array, got {type(server['args']).__name__}"
        for arg in server['args']:
            if not isinstance(arg, str):
                return False, f"Server args must be strings, got {type(arg).__name__}"
    
    if 'env' in server:
        if not isinstance(server['env'], dict):
            return False, f"Server env must be an object, got {type(server['env']).__name__}"

    # Validate tools (if present)
    if 'tools' in manifest:
        tools = manifest['tools']
        if not isinstance(tools, list):
            return False, f"Tools must be an array, got {type(tools).__name__}"
        
        tool_names = set()
        for i, tool in enumerate(tools):
            if not isinstance(tool, dict):
                return False, f"Tool at index {i} must be an object"
            
            # Check required tool fields
            if 'name' not in tool:
                return False, f"Tool at index {i} missing 'name' field"
            if 'description' not in tool:
                return False, f"Tool at index {i} missing 'description' field"
            if 'inputSchema' not in tool:
                return False, f"Tool at index {i} missing 'inputSchema' field"
            
            # Validate tool name
            tool_name = tool['name']
            if not isinstance(tool_name, str):
                return False, f"Tool name at index {i} must be a string"
            
            # Check for snake_case (lowercase with underscores)
            if not re.match(r'^[a-z][a-z0-9_]*$', tool_name):
                return False, f"Tool name '{tool_name}' should use snake_case (lowercase with underscores)"
            
            # Check for duplicate tool names
            if tool_name in tool_names:
                return False, f"Duplicate tool name: '{tool_name}'"
            tool_names.add(tool_name)
            
            # Validate inputSchema
            schema = tool['inputSchema']
            if not isinstance(schema, dict):
                return False, f"Tool '{tool_name}' inputSchema must be an object"
            
            if 'type' not in schema:
                return False, f"Tool '{tool_name}' inputSchema missing 'type' field"
            
            if schema['type'] != 'object':
                return False, f"Tool '{tool_name}' inputSchema type must be 'object', got '{schema['type']}'"

    # Validate resources (if present)
    if 'resources' in manifest:
        resources = manifest['resources']
        if not isinstance(resources, list):
            return False, f"Resources must be an array, got {type(resources).__name__}"
        
        for i, resource in enumerate(resources):
            if not isinstance(resource, dict):
                return False, f"Resource at index {i} must be an object"
            
            if 'uri' not in resource:
                return False, f"Resource at index {i} missing 'uri' field"
            if 'name' not in resource:
                return False, f"Resource at index {i} missing 'name' field"

    # Check if server entry point exists
    if 'args' in server and len(server['args']) > 0:
        entry_point = bundle_path / server['args'][0]
        if not entry_point.exists():
            return False, f"Server entry point not found: {server['args'][0]}"

    return True, "Manifest validation passed"


def main():
    if len(sys.argv) < 2:
        print("Usage: validate_mcpb.py <bundle-directory>")
        print("\nValidates the structure and manifest.json of an MCPB bundle.")
        sys.exit(1)

    bundle_path = sys.argv[1]
    
    print(f"Validating bundle: {bundle_path}")
    success, message = validate_bundle(bundle_path)
    
    if success:
        print(f"✓ {message}")
        print("\nValidation successful!")
        sys.exit(0)
    else:
        print(f"✗ Validation failed: {message}")
        sys.exit(1)


if __name__ == "__main__":
    main()
