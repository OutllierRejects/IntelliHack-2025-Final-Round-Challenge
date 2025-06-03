#!/usr/bin/env python3
"""
Standalone script to run the Disaster Response MCP Server
"""

import asyncio
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp_integration.server import main

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nMCP Server stopped.")
    except Exception as e:
        print(f"Error running MCP server: {e}")
        sys.exit(1)
