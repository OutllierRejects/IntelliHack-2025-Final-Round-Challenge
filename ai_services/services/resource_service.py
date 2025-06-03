"""
Resource management service for handling emergency resources and assignments
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
import math
import logging
from core.database import get_supabase_client

logger = logging.getLogger(__name__)
supabase = get_supabase_client()


def get_resources(filters: Dict = None) -> List[Dict]:
    """Get resources with optional filtering"""
    try:
        query = supabase.table("resources").select("*")

        if filters:
            for key, value in filters.items():
                if key in ["resource_type", "location", "id"]:
                    query = query.eq(key, value)
                elif key == "low_stock":
                    # Filter for resources below threshold
                    query = query.filter("current_stock", "lt", "threshold")

        response = query.order("resource_type").execute()

        return response.data if response.data else []

    except Exception as e:
        logger.error(f"Failed to get resources: {e}")
        return []


def update_resource_stock(
    resource_id: str, change_amount: int, operation: str = "decrement"
) -> Optional[Dict]:
    """Update resource stock (increment or decrement)"""
    try:
        # Get current resource
        current_response = (
            supabase.table("resources").select("*").eq("id", resource_id).execute()
        )

        if not current_response.data:
            logger.error(f"Resource {resource_id} not found")
            return None

        current_resource = current_response.data[0]
        current_stock = current_resource.get("current_stock", 0)

        # Calculate new stock
        if operation == "increment":
            new_stock = current_stock + change_amount
        else:  # decrement
            new_stock = max(0, current_stock - change_amount)

        # Update stock
        update_data = {
            "current_stock": new_stock,
            "updated_at": datetime.utcnow().isoformat(),
        }

        response = (
            supabase.table("resources")
            .update(update_data)
            .eq("id", resource_id)
            .execute()
        )

        if response.data:
            logger.info(
                f"Updated resource {resource_id} stock: {current_stock} -> {new_stock}"
            )

            # Check if below threshold
            threshold = current_resource.get("threshold", 0)
            if new_stock <= threshold:
                logger.warning(
                    f"Resource {resource_id} is below threshold: {new_stock} <= {threshold}"
                )
                # TODO: Trigger low stock alert

            return response.data[0]
        else:
            return None

    except Exception as e:
        logger.error(f"Failed to update resource stock {resource_id}: {e}")
        return None


def replenish_resource(resource_id: str, amount: int) -> Optional[Dict]:
    """Replenish resource stock"""
    return update_resource_stock(resource_id, amount, "increment")


def consume_resource(resource_id: str, amount: int) -> Optional[Dict]:
    """Consume resource stock"""
    return update_resource_stock(resource_id, amount, "decrement")


def create_resource(resource_data: Dict) -> Dict:
    """Create a new resource"""
    try:
        # Add timestamps
        now = datetime.utcnow().isoformat()
        resource_data.update({"created_at": now, "updated_at": now})

        response = supabase.table("resources").insert(resource_data).execute()

        if response.data:
            logger.info(f"Created new resource: {response.data[0]['id']}")
            return response.data[0]
        else:
            raise Exception("Failed to create resource - no data returned")

    except Exception as e:
        logger.error(f"Failed to create resource: {e}")
        raise


def get_low_stock_resources() -> List[Dict]:
    """Get resources that are below their threshold"""
    try:
        # Use raw SQL query for comparison
        response = supabase.rpc("get_low_stock_resources").execute()

        if response.data:
            return response.data
        else:
            # Fallback to manual filtering
            all_resources = get_resources()
            low_stock = []
            for resource in all_resources:
                if resource.get("current_stock", 0) <= resource.get("threshold", 0):
                    low_stock.append(resource)
            return low_stock

    except Exception as e:
        logger.error(f"Failed to get low stock resources: {e}")
        return []


def reserve_resources(resource_requirements: List[Dict]) -> bool:
    """Reserve resources for a task"""
    try:
        for requirement in resource_requirements:
            resource_type = requirement.get("resource_type")
            quantity = requirement.get("quantity", 0)
            location = requirement.get("location")

            # Find available resource
            filters = {"resource_type": resource_type}
            if location:
                filters["location"] = location

            resources = get_resources(filters)

            # Find resource with sufficient stock
            available_resource = None
            for resource in resources:
                if resource.get("current_stock", 0) >= quantity:
                    available_resource = resource
                    break

            if not available_resource:
                logger.error(f"Insufficient {resource_type} stock (need {quantity})")
                return False

            # Reserve by decrementing stock
            result = consume_resource(available_resource["id"], quantity)
            if not result:
                logger.error(f"Failed to reserve {quantity} of {resource_type}")
                return False

        return True

    except Exception as e:
        logger.error(f"Failed to reserve resources: {e}")
        return False


def get_resource_dashboard_stats() -> Dict:
    """Get dashboard statistics for resources"""
    try:
        stats = {}

        # Get total resources
        all_resources = get_resources()
        stats["total_resources"] = len(all_resources)

        # Get low stock count
        low_stock = get_low_stock_resources()
        stats["low_stock_count"] = len(low_stock)

        # Get resource breakdown by type
        type_counts = {}
        for resource in all_resources:
            resource_type = resource.get("resource_type", "unknown")
            type_counts[resource_type] = type_counts.get(resource_type, 0) + 1

        stats["resource_types"] = type_counts
        stats["low_stock_resources"] = low_stock

        return stats

    except Exception as e:
        logger.error(f"Failed to get resource dashboard stats: {e}")
        return {}
