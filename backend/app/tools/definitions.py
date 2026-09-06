from typing import List, Dict, Any

SALES_AGENT_TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "search_products",
            "description": "Searches the business product catalog for products matching a user inquiry, budget, tags, or category. ALWAYS use this when customer asks what is available, asks for recommendations, or specifies a price range/budget.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Keywords, product names, gift ideas, colors, categories (e.g. 'black hoodie', 'gift for wife under 3000 taka', 't-shirt')"
                    },
                    "category": {
                        "type": "string",
                        "description": "Optional category filter (e.g. 'Clothing', 'Accessories', 'Electronics')"
                    },
                    "min_price": {
                        "type": "number",
                        "description": "Optional minimum price filter"
                    },
                    "max_price": {
                        "type": "number",
                        "description": "Optional maximum budget/price filter (e.g. 3000)"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of results to return (default 5)",
                        "default": 5
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_product",
            "description": "Retrieves comprehensive details, specifications, images, and description for a specific product by ID or SKU.",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_id_or_sku": {
                        "type": "string",
                        "description": "The product UUID, SKU code, or exact title"
                    }
                },
                "required": ["product_id_or_sku"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_inventory",
            "description": "Checks real-time inventory and stock availability for a product and specific variant (size, color, material). ALWAYS call this before confirming that an item is in stock.",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_id_or_sku": {
                        "type": "string",
                        "description": "Product name, SKU, or UUID"
                    },
                    "size": {
                        "type": "string",
                        "description": "Size variant (e.g. 'S', 'M', 'L', 'XL', 'XXL')"
                    },
                    "color": {
                        "type": "string",
                        "description": "Color variant (e.g. 'Black', 'Red', 'Navy Blue')"
                    }
                },
                "required": ["product_id_or_sku"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_product_variants",
            "description": "Lists all available sizes, colors, and option combinations for a given product.",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_id": {
                        "type": "string",
                        "description": "Product UUID or SKU"
                    }
                },
                "required": ["product_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_order",
            "description": "Retrieves the live status, item breakdown, and delivery state for an existing customer order.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_number_or_id": {
                        "type": "string",
                        "description": "Order number (e.g. 'ORD-2026-0001') or Order UUID"
                    },
                    "customer_phone": {
                        "type": "string",
                        "description": "Optional customer phone number for security verification"
                    }
                },
                "required": ["order_number_or_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_order",
            "description": "Places a new confirmed customer order into the database. ONLY call this AFTER the customer has explicitly confirmed their purchase details (items, quantity, delivery address, payment method).",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_name": {
                        "type": "string",
                        "description": "Full name of the recipient"
                    },
                    "customer_phone": {
                        "type": "string",
                        "description": "WhatsApp or contact phone number"
                    },
                    "delivery_address": {
                        "type": "string",
                        "description": "Full delivery address"
                    },
                    "delivery_city": {
                        "type": "string",
                        "description": "City or district (e.g. 'Dhaka', 'Chittagong', 'Sylhet')"
                    },
                    "items": {
                        "type": "array",
                        "description": "List of ordered items",
                        "items": {
                            "type": "object",
                            "properties": {
                                "product_name": {"type": "string"},
                                "variant_name": {"type": "string"},
                                "quantity": {"type": "integer"},
                                "unit_price": {"type": "number"}
                            },
                            "required": ["product_name", "quantity", "unit_price"]
                        }
                    },
                    "payment_method": {
                        "type": "string",
                        "description": "Payment method: 'COD' (Cash on Delivery), 'BKASH', 'NAGAD', 'CARD'",
                        "enum": ["COD", "BKASH", "NAGAD", "CARD", "ONLINE"]
                    },
                    "notes": {
                        "type": "string",
                        "description": "Special delivery instructions or customer notes"
                    }
                },
                "required": ["customer_name", "customer_phone", "delivery_address", "items", "payment_method"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_order",
            "description": "Updates customer order information or cancellation status.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "Order UUID or order number"
                    },
                    "status": {
                        "type": "string",
                        "description": "New status (e.g. 'CANCELLED', 'CONFIRMED')"
                    },
                    "notes": {
                        "type": "string",
                        "description": "Update notes"
                    }
                },
                "required": ["order_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_shipping",
            "description": "Calculates delivery charge and estimated delivery time based on customer location and item count.",
            "parameters": {
                "type": "object",
                "properties": {
                    "delivery_address": {
                        "type": "string",
                        "description": "Customer delivery address"
                    },
                    "city": {
                        "type": "string",
                        "description": "City name (e.g. 'Dhaka', 'Outside Dhaka')"
                    },
                    "item_count": {
                        "type": "integer",
                        "description": "Total quantity of items",
                        "default": 1
                    }
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_shipping_status",
            "description": "Fetches real-time shipment courier status and tracking info for an order.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id_or_tracking": {
                        "type": "string",
                        "description": "Order number or courier tracking number"
                    }
                },
                "required": ["order_id_or_tracking"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "capture_lead",
            "description": "Records potential buyer interest, budget, location, and assigns a lead score for CRM follow-up.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "phone": {"type": "string"},
                    "intent": {"type": "string"},
                    "interested_products": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "budget": {"type": "number"},
                    "location": {"type": "string"},
                    "lead_score": {
                        "type": "integer",
                        "description": "Lead score from 1 to 100 based on purchase intent"
                    }
                },
                "required": ["phone", "intent"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_support_ticket",
            "description": "Creates an internal support or inquiry ticket when an issue requires specialized human attention or warranty review.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_phone": {"type": "string"},
                    "subject": {"type": "string"},
                    "issue_description": {"type": "string"},
                    "priority": {
                        "type": "string",
                        "enum": ["LOW", "MEDIUM", "HIGH", "URGENT"]
                    }
                },
                "required": ["customer_phone", "subject", "issue_description"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "transfer_to_human",
            "description": "Transfers the WhatsApp conversation to a human support/sales agent. Use when customer explicitly requests a person, makes a serious complaint, asks for complex refund, or expresses anger.",
            "parameters": {
                "type": "object",
                "properties": {
                    "reason": {
                        "type": "string",
                        "description": "Reason for escalation (e.g. 'Customer requested human agent', 'Refund dispute', 'Complex bulk pricing')"
                    },
                    "department": {
                        "type": "string",
                        "description": "Target department: 'SALES', 'SUPPORT', 'BILLING'"
                    }
                },
                "required": ["reason"]
            }
        }
    }
]
