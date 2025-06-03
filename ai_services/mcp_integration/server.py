"""
Model Context Protocol (MCP) Server for Disaster Response AI Agents
Exposes AGNO agents as MCP tools for integration with LLM applications
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional, Sequence
from datetime import datetime
import json

from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    JSONValue,
)

from agno_agents.coordinator import AgentCoordinator
from core.database import get_supabase_client

logger = logging.getLogger(__name__)


class DisasterResponseMCPServer:
    """MCP Server exposing disaster response AI agent capabilities"""

    def __init__(self):
        self.server = Server("disaster-response-mcp")
        self.agent_coordinator = None
        self.supabase = get_supabase_client()

        # Initialize agent coordinator
        try:
            self.agent_coordinator = AgentCoordinator()
        except Exception as e:
            logger.error(f"Failed to initialize agent coordinator: {e}")

        self._setup_tools()
        self._setup_resources()
        self._setup_handlers()

    def _setup_tools(self):
        """Define MCP tools that expose agent capabilities"""

        @self.server.list_tools()
        async def handle_list_tools() -> List[Tool]:
            """List available disaster response tools"""
            return [
                Tool(
                    name="process_emergency_request",
                    description="Process an emergency help request through the AGNO agent pipeline",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string",
                                "description": "Brief title of the emergency request",
                            },
                            "description": {
                                "type": "string",
                                "description": "Detailed description of the emergency situation",
                            },
                            "location": {
                                "type": "string",
                                "description": "Location of the emergency (optional)",
                            },
                            "contact_info": {
                                "type": "string",
                                "description": "Contact information for the requester (optional)",
                            },
                            "requester_id": {
                                "type": "string",
                                "description": "ID of the person making the request (optional)",
                            },
                        },
                        "required": ["title", "description"],
                    },
                ),
                Tool(
                    name="get_agent_status",
                    description="Get current status of the disaster response AI agent system",
                    inputSchema={"type": "object", "properties": {}},
                ),
                Tool(
                    name="get_active_requests",
                    description="Retrieve active disaster response requests with their status",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "status": {
                                "type": "string",
                                "enum": [
                                    "PENDING",
                                    "PROCESSING",
                                    "ASSIGNED",
                                    "IN_PROGRESS",
                                    "COMPLETED",
                                ],
                                "description": "Filter requests by status (optional)",
                            },
                            "priority": {
                                "type": "string",
                                "enum": ["CRITICAL", "HIGH", "MEDIUM", "LOW"],
                                "description": "Filter requests by priority (optional)",
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Maximum number of requests to return (default: 10)",
                            },
                        },
                    },
                ),
                Tool(
                    name="assign_volunteer_to_task",
                    description="Assign a volunteer to a specific disaster response task",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "task_id": {
                                "type": "string",
                                "description": "ID of the task to assign",
                            },
                            "volunteer_id": {
                                "type": "string",
                                "description": "ID of the volunteer to assign",
                            },
                            "notes": {
                                "type": "string",
                                "description": "Additional assignment notes (optional)",
                            },
                        },
                        "required": ["task_id", "volunteer_id"],
                    },
                ),
                Tool(
                    name="get_available_resources",
                    description="Get current availability of disaster response resources",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "resource_type": {
                                "type": "string",
                                "enum": [
                                    "FOOD",
                                    "WATER",
                                    "MEDICAL",
                                    "SHELTER",
                                    "TRANSPORT",
                                    "EQUIPMENT",
                                ],
                                "description": "Filter by resource type (optional)",
                            },
                            "location": {
                                "type": "string",
                                "description": "Filter by location (optional)",
                            },
                        },
                    },
                ),
                Tool(
                    name="prioritize_requests",
                    description="Run prioritization agent on pending requests",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "request_ids": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Specific request IDs to prioritize (optional, defaults to all pending)",
                            }
                        },
                    },
                ),
            ]

        @self.server.call_tool()
        async def handle_call_tool(
            name: str, arguments: Dict[str, Any]
        ) -> List[TextContent]:
            """Handle tool calls"""
            try:
                if name == "process_emergency_request":
                    return await self._process_emergency_request(arguments)
                elif name == "get_agent_status":
                    return await self._get_agent_status(arguments)
                elif name == "get_active_requests":
                    return await self._get_active_requests(arguments)
                elif name == "assign_volunteer_to_task":
                    return await self._assign_volunteer_to_task(arguments)
                elif name == "get_available_resources":
                    return await self._get_available_resources(arguments)
                elif name == "prioritize_requests":
                    return await self._prioritize_requests(arguments)
                else:
                    return [TextContent(type="text", text=f"Unknown tool: {name}")]
            except Exception as e:
                logger.error(f"Error executing tool {name}: {e}")
                return [TextContent(type="text", text=f"Error: {str(e)}")]

    def _setup_resources(self):
        """Define MCP resources for disaster response data"""

        @self.server.list_resources()
        async def handle_list_resources() -> List[Resource]:
            """List available disaster response resources"""
            return [
                Resource(
                    uri="disaster://requests/active",
                    name="Active Emergency Requests",
                    description="Current active emergency requests in the system",
                ),
                Resource(
                    uri="disaster://agents/status",
                    name="Agent System Status",
                    description="Status and metrics of the AI agent system",
                ),
                Resource(
                    uri="disaster://resources/inventory",
                    name="Resource Inventory",
                    description="Current inventory of disaster response resources",
                ),
                Resource(
                    uri="disaster://volunteers/available",
                    name="Available Volunteers",
                    description="List of available volunteers and their skills",
                ),
            ]

        @self.server.read_resource()
        async def handle_read_resource(uri: str) -> str:
            """Read disaster response resources"""
            try:
                if uri == "disaster://requests/active":
                    return await self._get_active_requests_resource()
                elif uri == "disaster://agents/status":
                    return await self._get_agent_status_resource()
                elif uri == "disaster://resources/inventory":
                    return await self._get_resources_inventory()
                elif uri == "disaster://volunteers/available":
                    return await self._get_available_volunteers()
                else:
                    return f"Unknown resource: {uri}"
            except Exception as e:
                logger.error(f"Error reading resource {uri}: {e}")
                return f"Error reading resource: {str(e)}"

    def _setup_handlers(self):
        """Setup additional MCP handlers"""

        @self.server.set_logging_level()
        async def handle_set_logging_level(level: str) -> None:
            """Set logging level"""
            logging.getLogger().setLevel(getattr(logging, level.upper()))

    # Tool implementation methods

    async def _process_emergency_request(
        self, args: Dict[str, Any]
    ) -> List[TextContent]:
        """Process emergency request through agent pipeline"""
        try:
            if not self.agent_coordinator:
                return [
                    TextContent(type="text", text="Agent coordinator not available")
                ]

            # Create request in database
            request_data = {
                "title": args["title"],
                "description": args["description"],
                "location": args.get("location"),
                "contact_info": args.get("contact_info"),
                "requester_id": args.get("requester_id"),
                "status": "PENDING",
                "created_at": datetime.utcnow().isoformat(),
            }

            # Insert into database
            result = self.supabase.table("requests").insert(request_data).execute()
            request_id = result.data[0]["id"]

            # Process through agent pipeline
            processing_result = await self.agent_coordinator._process_single_request(
                request_data
            )

            response = {
                "success": True,
                "request_id": request_id,
                "message": "Emergency request processed successfully",
                "processing_result": processing_result,
            }

            return [TextContent(type="text", text=json.dumps(response, indent=2))]

        except Exception as e:
            error_response = {
                "success": False,
                "error": str(e),
                "message": "Failed to process emergency request",
            }
            return [TextContent(type="text", text=json.dumps(error_response, indent=2))]

    async def _get_agent_status(self, args: Dict[str, Any]) -> List[TextContent]:
        """Get agent system status"""
        try:
            if not self.agent_coordinator:
                status = {
                    "status": "unavailable",
                    "message": "Agent coordinator not initialized",
                }
            else:
                status = self.agent_coordinator.get_system_status()

            return [TextContent(type="text", text=json.dumps(status, indent=2))]

        except Exception as e:
            error_response = {"error": str(e), "message": "Failed to get agent status"}
            return [TextContent(type="text", text=json.dumps(error_response, indent=2))]

    async def _get_active_requests(self, args: Dict[str, Any]) -> List[TextContent]:
        """Get active disaster requests"""
        try:
            query = self.supabase.table("requests").select("*")

            # Apply filters
            if args.get("status"):
                query = query.eq("status", args["status"])
            if args.get("priority"):
                query = query.eq("priority", args["priority"])

            # Apply limit
            limit = args.get("limit", 10)
            query = query.limit(limit)

            result = query.execute()

            response = {
                "requests": result.data,
                "count": len(result.data),
                "filters_applied": {k: v for k, v in args.items() if v is not None},
            }

            return [TextContent(type="text", text=json.dumps(response, indent=2))]

        except Exception as e:
            error_response = {
                "error": str(e),
                "message": "Failed to retrieve active requests",
            }
            return [TextContent(type="text", text=json.dumps(error_response, indent=2))]

    async def _assign_volunteer_to_task(
        self, args: Dict[str, Any]
    ) -> List[TextContent]:
        """Assign volunteer to task"""
        try:
            task_id = args["task_id"]
            volunteer_id = args["volunteer_id"]
            notes = args.get("notes", "")

            # Update task assignment
            update_data = {
                "assigned_to": volunteer_id,
                "status": "ASSIGNED",
                "updated_at": datetime.utcnow().isoformat(),
            }

            if notes:
                update_data["notes"] = notes

            result = (
                self.supabase.table("tasks")
                .update(update_data)
                .eq("id", task_id)
                .execute()
            )

            if result.data:
                response = {
                    "success": True,
                    "message": f"Volunteer {volunteer_id} assigned to task {task_id}",
                    "assignment": result.data[0],
                }
            else:
                response = {
                    "success": False,
                    "message": f"Task {task_id} not found or assignment failed",
                }

            return [TextContent(type="text", text=json.dumps(response, indent=2))]

        except Exception as e:
            error_response = {
                "success": False,
                "error": str(e),
                "message": "Failed to assign volunteer to task",
            }
            return [TextContent(type="text", text=json.dumps(error_response, indent=2))]

    async def _get_available_resources(self, args: Dict[str, Any]) -> List[TextContent]:
        """Get available resources"""
        try:
            query = (
                self.supabase.table("resources").select("*").eq("status", "AVAILABLE")
            )

            # Apply filters
            if args.get("resource_type"):
                query = query.eq("resource_type", args["resource_type"])
            if args.get("location"):
                query = query.ilike("location", f"%{args['location']}%")

            result = query.execute()

            response = {
                "resources": result.data,
                "count": len(result.data),
                "filters_applied": {k: v for k, v in args.items() if v is not None},
            }

            return [TextContent(type="text", text=json.dumps(response, indent=2))]

        except Exception as e:
            error_response = {
                "error": str(e),
                "message": "Failed to retrieve available resources",
            }
            return [TextContent(type="text", text=json.dumps(error_response, indent=2))]

    async def _prioritize_requests(self, args: Dict[str, Any]) -> List[TextContent]:
        """Prioritize pending requests"""
        try:
            if not self.agent_coordinator:
                return [
                    TextContent(type="text", text="Agent coordinator not available")
                ]

            request_ids = args.get("request_ids")

            if request_ids:
                # Process specific requests
                result = await self.agent_coordinator.process_incidents_batch(
                    request_ids
                )
            else:
                # Process all pending requests
                result = await self.agent_coordinator.trigger_immediate_processing()

            response = {
                "success": True,
                "message": "Prioritization completed",
                "result": result,
            }

            return [TextContent(type="text", text=json.dumps(response, indent=2))]

        except Exception as e:
            error_response = {
                "success": False,
                "error": str(e),
                "message": "Failed to prioritize requests",
            }
            return [TextContent(type="text", text=json.dumps(error_response, indent=2))]

    # Resource implementation methods

    async def _get_active_requests_resource(self) -> str:
        """Get active requests as resource"""
        try:
            result = (
                self.supabase.table("requests")
                .select("*")
                .neq("status", "COMPLETED")
                .execute()
            )
            return json.dumps(result.data, indent=2)
        except Exception as e:
            return f"Error retrieving active requests: {str(e)}"

    async def _get_agent_status_resource(self) -> str:
        """Get agent status as resource"""
        try:
            if not self.agent_coordinator:
                return json.dumps(
                    {
                        "status": "unavailable",
                        "message": "Agent coordinator not initialized",
                    }
                )

            status = self.agent_coordinator.get_system_status()
            return json.dumps(status, indent=2)
        except Exception as e:
            return f"Error retrieving agent status: {str(e)}"

    async def _get_resources_inventory(self) -> str:
        """Get resource inventory"""
        try:
            result = self.supabase.table("resources").select("*").execute()
            return json.dumps(result.data, indent=2)
        except Exception as e:
            return f"Error retrieving resource inventory: {str(e)}"

    async def _get_available_volunteers(self) -> str:
        """Get available volunteers"""
        try:
            result = (
                self.supabase.table("users")
                .select("*")
                .eq("role", "volunteer")
                .eq("availability", True)
                .execute()
            )
            return json.dumps(result.data, indent=2)
        except Exception as e:
            return f"Error retrieving available volunteers: {str(e)}"

    async def run(self):
        """Run the MCP server"""
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="disaster-response-mcp",
                    server_version="1.0.0",
                    capabilities=self.server.get_capabilities(
                        notification_options=None, experimental_capabilities=None
                    ),
                ),
            )


# Entry point for running MCP server
async def main():
    """Main entry point for MCP server"""
    server = DisasterResponseMCPServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
