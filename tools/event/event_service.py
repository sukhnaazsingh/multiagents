import datetime
from langchain_core.tools import tool

# TODO MOCK EVENT
# Special occasions by month
SPECIAL_OCCASIONS = {
    "01": {
        "events": ["New Year's Day", "Post-Holiday Sales"],
        "product_focus": [
            "Fitness equipment & accessories",
            "Health & wellness products (vitamins, supplements)",
            "Planners & organization tools",
            "Winter clothing & accessories",
            "Holiday clearance items"
        ]
    },
    "02": {
        "events": ["Valentine's Day"],
        "product_focus": [
            "Jewelry & watches",
            "Romantic gifts (candles, chocolates, greeting cards)",
            "Beauty & self-care products",
            "Flowers & gift baskets",
            "Date night fashion & accessories"
        ]
    },
    "03": {
        "events": ["Easter (Varies)", "Spring Break"],
        "product_focus": [
            "Easter decorations & themed products",
            "Kids' toys & candy",
            "Spring fashion & accessories",
            "Travel essentials (luggage, swimwear, sunglasses)",
            "Outdoor & picnic gear"
        ]
    },
    "04": {
        "events": ["Easter (Varies)"],
        "product_focus": [
            "Easter home decor & tableware",
            "Spring gardening tools & seeds",
            "Children's holiday gifts",
            "Outdoor activity products",
            "DIY & crafting supplies"
        ]
    },
    "05": {
        "events": ["Labor Day (Some Countries)", "Memorial Day (US)"],
        "product_focus": [
            "BBQ & grilling equipment",
            "Outdoor furniture & decor",
            "Summer fashion",
            "Camping & hiking gear",
            "Home improvement & DIY tools"
        ]
    },
    "06": {
        "events": ["Summer Sales Begin"],
        "product_focus": [
            "Beachwear & swim accessories",
            "Cooling appliances & fans",
            "Travel gear (backpacks, sunglasses, hats)",
            "Sports & outdoor activities equipment",
            "Home & patio decor"
        ]
    },
    "07": {
        "events": ["Independence Day (US)"],
        "product_focus": [
            "Red, white & blue-themed decorations",
            "BBQ & picnic supplies",
            "Outdoor games & activities",
            "Summer party essentials",
            "Fireworks-related safety gear"
        ]
    },
    "08": {
        "events": ["Back to School Preparation"],
        "product_focus": [
            "School supplies (notebooks, backpacks, stationery)",
            "Electronics (laptops, tablets, calculators)",
            "Kids’ & teen fashion",
            "Lunchboxes & meal prep items",
            "Dorm room essentials"
        ]
    },
    "09": {
        "events": ["Labor Day (US)", "Oktoberfest"],
        "product_focus": [
            "Work & office essentials",
            "Home improvement & DIY products",
            "Fall fashion & footwear",
            "Beer brewing kits & Oktoberfest-themed decor",
            "Kitchen & baking essentials"
        ]
    },
    "10": {
        "events": ["Halloween", "Thanksgiving Preparation"],
        "product_focus": [
            "Halloween costumes & decorations",
            "Candy & treats",
            "Party supplies & themed accessories",
            "Thanksgiving tableware & cooking essentials",
            "Fall home decor"
        ]
    },
    "11": {
        "events": ["Black Friday", "Cyber Monday"],
        "product_focus": [
            "Consumer electronics (phones, laptops, gaming consoles)",
            "Smart home devices",
            "Fashion & accessories",
            "Fitness & health products",
            "Holiday gift sets & bundles"
        ]
    },
    "12": {
        "events": ["Christmas", "New Year's Eve"],
        "product_focus": [
            "Holiday decorations & lights",
            "Toys & kids’ gifts",
            "Winter apparel & accessories",
            "Party supplies & festive dinnerware",
            "Luxury & giftable items"
        ]
    }
}

HOLIDAY_PREPARATIONS = {
    "01": ["Plan post-holiday clearance sales", "Promote fitness & wellness products"],
    "02": ["Stock up on Valentine's Day gifts", "Highlight romantic gift bundles"],
    "03": ["Prepare Easter promotions", "Launch spring fashion sales"],
    "04": ["Continue Easter deals", "Promote gardening & outdoor products"],
    "05": ["Memorial Day discounts", "Focus on summer travel essentials"],
    "06": ["Summer sales & travel-related marketing", "Boost outdoor recreation products"],
    "07": ["Independence Day sales", "Stock up on outdoor & party supplies"],
    "08": ["Launch back-to-school promotions", "Ensure sufficient stock of school essentials"],
    "09": ["Market Oktoberfest-themed items", "Prepare for fall fashion promotions"],
    "10": ["Stock up on Halloween products", "Start early Christmas marketing"],
    "11": ["Optimize Black Friday & Cyber Monday deals", "Push early holiday gift sales"],
    "12": ["Focus on Christmas shopping rush", "Plan for post-New Year's promotions"]
}


@tool
def get_current_month() -> str:
    """Retrieves the current month as a two-digit string."""
    today = datetime.date.today()
    return today.strftime('%m')

@tool
def check_special_occasions(month: str) -> str:
    """Checks for any special occasions in the given month."""
    occasions = SPECIAL_OCCASIONS.get(month, [])
    return ", ".join(occasions) if occasions else "No major special occasions this month."

@tool
def get_preparation_tips(month: str) -> str:
    """Provides preparation tips based on upcoming peak seasons."""
    preparations = HOLIDAY_PREPARATIONS.get(month, [])
    return ", ".join(preparations) if preparations else "No special preparations needed this month."
