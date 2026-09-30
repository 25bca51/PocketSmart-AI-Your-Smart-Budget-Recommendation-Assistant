from typing import List


PLATFORM_CATALOG = {
    "home": [
        {
            "name": "Modern LED Ceiling Light",
            "category": "Lighting",
            "platform": "Amazon",
            "price": 2499,
            "url": "https://www.amazon.in/",
        },
        {
            "name": "Minimalist Floor Lamp",
            "category": "Lighting",
            "platform": "IKEA",
            "price": 3999,
            "url": "https://www.ikea.com/in/en/",
        },
        {
            "name": "Energy Efficient Ceiling Fan",
            "category": "Fan",
            "platform": "Amazon",
            "price": 3299,
            "url": "https://www.amazon.in/",
        },
        {
            "name": "Six-Seater Dining Table",
            "category": "Furniture",
            "platform": "IKEA",
            "price": 14999,
            "url": "https://www.ikea.com/in/en/",
        },
        {
            "name": "Contemporary Wall Art",
            "category": "Decor",
            "platform": "Amazon",
            "price": 1299,
            "url": "https://www.amazon.in/",
        },
        {
            "name": "Modern Storage Cabinet",
            "category": "Storage",
            "platform": "IKEA",
            "price": 8999,
            "url": "https://www.ikea.com/in/en/",
        },
    ],
    "party": [
        {
            "name": "Catering Package",
            "category": "Catering",
            "platform": "Zomato",
            "price": 12000,
            "url": "https://www.zomato.com/",
        },
        {
            "name": "Food Delivery Package",
            "category": "Catering",
            "platform": "Swiggy",
            "price": 10000,
            "url": "https://www.swiggy.com/",
        },
        {
            "name": "Birthday Decoration Package",
            "category": "Decoration",
            "platform": "Amazon",
            "price": 3500,
            "url": "https://www.amazon.in/",
        },
        {
            "name": "Event Hotel Room Package",
            "category": "Accommodation",
            "platform": "OYO",
            "price": 6000,
            "url": "https://www.oyorooms.com/",
        },
        {
            "name": "Party Lighting Kit",
            "category": "Entertainment",
            "platform": "Amazon",
            "price": 2500,
            "url": "https://www.amazon.in/",
        },
    ],
    "jewelry": [
        {
            "name": "Elegant Gold-Tone Necklace Set",
            "category": "Necklace",
            "platform": "Amazon",
            "price": 2499,
            "url": "https://www.amazon.in/",
        },
        {
            "name": "Traditional Kundan Earrings",
            "category": "Earrings",
            "platform": "Flipkart",
            "price": 1799,
            "url": "https://www.flipkart.com/",
        },
        {
            "name": "Minimal Pearl Bracelet",
            "category": "Bracelet",
            "platform": "Amazon",
            "price": 1299,
            "url": "https://www.amazon.in/",
        },
        {
            "name": "Statement Jewelry Set",
            "category": "Jewelry Set",
            "platform": "Flipkart",
            "price": 3999,
            "url": "https://www.flipkart.com/",
        },
        {
            "name": "Classic Stud Earrings",
            "category": "Earrings",
            "platform": "Amazon",
            "price": 999,
            "url": "https://www.amazon.in/",
        },
    ],
}


def get_platform_catalog(planner_type: str) -> List[dict]:
    return PLATFORM_CATALOG.get(planner_type, []).copy()


def filter_by_budget(
    products: List[dict],
    budget: float,
) -> List[dict]:
    return [
        product
        for product in products
        if product["price"] <= budget
    ]