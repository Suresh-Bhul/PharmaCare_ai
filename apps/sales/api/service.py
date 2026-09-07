import requests
import json

def create_khalti_url(**kwargs):
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
            "return_url": "http://localhost:8000/callback/",   #After Payment then return
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
        'Authorization': 'key ea674cb4220148678bea350de88201b9',
        'Content-Type': 'application/json',
    }

    response = requests.post(url, headers=headers, data=payload)

    print(response.json())
    return response.json()