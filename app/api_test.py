import httpx
import asyncio
import base64
import json

ROUTE_POST = "https://api.tvh.com/customers/00783794/inquiries"



line = {
    # Line number fixed, its just when you send multiple requests at one time
    "lineNumber": 1,
    "makeCode": 'TVH',
    "partNumber": '140TA4159',
    "customerPartNumber": f"Testanfrage Teil 2",
    # Fallback quantity condition, if it exists in the database, then use it or else input
    # "quantity": row.inquiryAmount,
    "quantity" : 1,
    "text": 'Inquiry extra text'
}
payload = {
    "text": "Text abc def",
    "customerInquiryNumber": "Testanfrage inquiry",
    # Customer code static
    # "customerCode": customerCode,
    "customerCode": "00783794",
    "customerContactName": "Jan Theunert",
    "lines": [line]
}

headers = {
    'Content-Type': 'application/json',
    # Authorization header static
    'Authorization': 'Basic MDA3ODM3OTQrcmVzdEB0dmguY29tOm5ZWnFMcXhnRHl6ZXk1dzJqTkZ2SHQ0dw=='
}

complete_request = {
    "url": ROUTE_POST,
    "method": "POST",
    "headers": headers,
    "payload": payload
}
json_dump = json.dumps(complete_request, indent=4)

response = httpx.post(ROUTE_POST, headers=headers, json=dict(payload), timeout=150)
print(response.json())
