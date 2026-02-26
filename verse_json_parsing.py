"""
Practice extracting data from nested JSON - very common!
"""

import json

sample_json = {
    "status": "success",
    "data": {
        "users": [
            {
                "id": 1,
                "name": "John Doe",
                "email": "john@example.com",
                "orders": [
                    {"order_id": "O001", "total": 150.00, "items": [{"product": "Laptop", "qty": 1}]},
                    {"order_id": "O002", "total": 50.00, "items": [{"product": "Mouse", "qty": 2}]}
                ]
            },
            {
                "id": 2,
                "name": "Jane Smith",
                "email": "jane@example.com",
                "orders": [
                    {"order_id": "O003", "total": 200.00, "items": [{"product": "Monitor", "qty": 1}]}
                ]
            }
        ]
    }
}


def extract_user_summary(json_data):
    """
    Extract:
    1. List of all user emails
    2. Total revenue across all users
    3. User with highest total spend
    4. All unique products ordered
    """

    users = json_data.get('data', {}).get('users', [])

    # 1. Emails
    emails = [user.get('email') for user in users]

    # 2. Total revenue
    total_revenue = sum(
        order.get('total', 0)
        for user in users
        for order in user.get('orders', [])
    )

    # 3. Top spender
    user_spending = {}
    for user in users:
        user_total = sum(order.get('total', 0) for order in user.get('orders', []))
        user_spending[user.get('name')] = user_total

    top_spender = max(user_spending, key=user_spending.get)

    # 4. Unique products
    products = set()
    for user in users:
        for order in user.get('orders', []):
            for item in order.get('items', []):
                products.add(item.get('product'))

    return {
        'emails': emails,
        'total_revenue': total_revenue,
        'top_spender': top_spender,
        'unique_products': list(products)
    }


result = extract_user_summary(sample_json)
print(json.dumps(result, indent=2))