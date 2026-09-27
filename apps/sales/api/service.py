import os
import requests
import json

def create_khalti_url(**kwargs):
    khalti_api_key = os.getenv("KHALTI_API_KEY")
    if not khalti_api_key:
        raise RuntimeError(
            "KHALTI_API_KEY is not set. Add it to your .env file."
        )

    amount = kwargs.get("amount")
    purchase_order_id = kwargs.get("purchase_order_id")
    purchase_order_name = kwargs.get("purchase_order_name")

    customer_name = kwargs.get("customer_name")
    customer_email = kwargs.get("customer_email")
    customer_phone = kwargs.get("customer_phone")

    amount_breakdown = kwargs.get("amount_breakdown", [])

    product_details = kwargs.get("product_details", [])


    url = "https://dev.khalti.com/api/v2/epayment/initiate/"

    payload = json.dumps(
        {
            "return_url": os.getenv("KHALTI_RETURN_URL", "http://localhost:8000/callback/"),   #After Payment then return
            "website_url": "https://example.com/",
            "amount": amount,
            "purchase_order_id": purchase_order_id,
            "purchase_order_name": purchase_order_name,
            "customer_info": {
                "name": customer_name,
                "email": customer_email,
                "phone": customer_phone,
            },
            "amount_breakdown": amount_breakdown,
            "product_details": product_details,
        }
    )
    headers = {
        'Authorization': f'key {khalti_api_key}',
        'Content-Type': 'application/json',
    }

    response = requests.post(url, headers=headers, data=payload)

    print(response.json())
    return response.json()