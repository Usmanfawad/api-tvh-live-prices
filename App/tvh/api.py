import httpx
import asyncio
import base64
import json

from App.db.controllers.tbl_cache import delete_table_cache, insert_into_table_cache, delete_from_table_cache, select_from_table_cache, update_json_strings_in_cache


def to_base64(string_credentials):
    sample_string_bytes = string_credentials.encode("ascii")

    base64_bytes = base64.b64encode(sample_string_bytes)
    base64_string = base64_bytes.decode("ascii")

    return base64_string

async def tvh_api(customerCode, fallbackQuantity, userText):

    # Here the customer code from frontend input will be there
    # ROUTE_POST = f"https://api.tvh.com/customers/customerCode/inquiries"
    ROUTE_POST = "https://api.tvh.com/customers/00597861/inquiries"


    data_from_cache = select_from_table_cache()
    print(data_from_cache)

    updates = []

    for index, row in enumerate(data_from_cache, 1):
        # enumerate, starting item 1
        line = {
            # Line number fixed, its just when you send multiple requests at one time
            "lineNumber": 1,
            "makeCode": row.Lieferant_Marke,
            "partNumber": row.Bestellnummer,
            "customerPartNumber": f"Testanfrage Teil {index}",
            # Fallback quantity condition, if it exists in the database, then use it or else input
            "quantity": row.inquiryAmount,
            "text": userText
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
        updates.append((row.Lieferant_Marke, row.Bestellnummer, json_dump))
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(ROUTE_POST, headers=headers, json=dict(payload))
                response.raise_for_status()
                # Parse and return the response data
                api_response = response.json()
                print(api_response)
                update_json_strings_in_cache(updates)
                # return {"api_response": api_response}
            except httpx.HTTPError as e:
                raise HTTPException(status_code=e.response.status_code, detail=str(e.response.text))

        if len(updates) >= 2:
            update_json_strings_in_cache(updates)
            updates = []
            return {"api_response": api_response}
            break