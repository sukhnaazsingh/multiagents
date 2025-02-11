from langchain.tools import tool
import json
import re

@tool
def extract_identifiers(message: str) -> dict:
    """
    Dynamically extracts tracking IDs and order IDs from user messages.

    :param message: The user's message.
    :return: A dictionary containing extracted identifiers.
    """
    tracking_pattern = r"tracking\s?(id|number)?[:\s]+([A-Za-z0-9-]+)"
    order_pattern = r"order\s?(id|number)?[:\s]+([A-Za-z0-9-]+)"

    tracking_match = re.search(tracking_pattern, message, re.IGNORECASE)
    order_match = re.search(order_pattern, message, re.IGNORECASE)

    extracted_data = {}

    if tracking_match:
        extracted_data["tracking_id"] = tracking_match.group(2).strip()

    if order_match:
        extracted_data["order_id"] = order_match.group(2).strip()

    return extracted_data


@tool
def track_package(tracking_id: str) -> str:
    """Checks the status of a package given a tracking ID."""
    tracking_info = {# TODO MOCK TRACKING
        "123ABC": {"status": "in transit", "estimated_delivery": "tomorrow"},
        "456DEF": {"status": "at warehouse", "estimated_dispatch": "soon"},
        "555BCD": {"status": "delivered"},
    }
    return json.dumps(tracking_info.get(tracking_id, {"error": "Tracking ID not found."}))

@tool
def get_order_status(order_id: str) -> str:
    """Checks the status of an order given an order ID."""
    orders = {# TODO MOCK ORDERS
        "1001": {"status": "shipped", "tracking_id": "123ABC"},
        "1002": {"status": "processing", "expected_ship_date": "2 days"},
        "1003": {"status": "canceled"},
        "1004": {"status": "shipped", "tracking_id": "555BCD"}
    }
    return json.dumps(orders.get(order_id, {"error": "Order ID not found."}))
