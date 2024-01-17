import httpx
import asyncio
import base64
import json
from fastapi import APIRouter, status, Response, HTTPException, Depends, status, Body, WebSocket, WebSocketDisconnect


from App.db.controllers.tbl_cache import delete_table_cache, insert_into_table_cache, delete_from_table_cache, select_from_table_cache, update_json_strings_in_cache


def to_base64(string_credentials):
    sample_string_bytes = string_credentials.encode("ascii")

    base64_bytes = base64.b64encode(sample_string_bytes)
    base64_string = base64_bytes.decode("ascii")

    return base64_string

async def tvh_api(batch_number ,customerCode, fallbackQuantity, userText, lower_bound, upper_bound, websocket: WebSocket):
    try:
        # Here the customer code from frontend input will be there
        # ROUTE_POST = f"https://api.tvh.com/customers/customerCode/inquiries"
        ROUTE_POST = "https://api.tvh.com/customers/00783794/inquiries"


        data_from_tbl_cache = select_from_table_cache()
        data_from_cache = data_from_tbl_cache[lower_bound:upper_bound]
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
            async with httpx.AsyncClient() as client:
                try:
                    updates = []
                    response = await client.post(ROUTE_POST, headers=headers, json=dict(payload), timeout=30)
                    response.raise_for_status()
                    print("The response is: ")
                    print(response)
                    # Parse and return the response data
                    api_response = response.json()
                    inquiry_number = dict(api_response[0])["inquiryNumberTVH"]
                    price = dict(api_response[0])["lines"][0]["price"]
                    listPrice = dict(api_response[0])["lines"][0]["listPrice"]
                    partNumber = dict(api_response[0])["lines"][0]["partNumber"]
                    makeCode = dict(api_response[0])["lines"][0]["makeCode"]
                    availability_code = dict(api_response[0])["lines"][0]["availabilityCode"]
                    await websocket.send_text(f"Thread number: {batch_number} | Inquiry number: {inquiry_number} | Part number: {partNumber} | Make code: {makeCode} ")
                    api_response_json_dumps = json.dumps(api_response, indent= 4)
                    updates.append((row.Lieferant_Marke, row.Bestellnummer, json_dump, api_response_json_dumps))

                    update_db = update_json_strings_in_cache(updates, price, listPrice, availability_code)
                    # return {"api_response": api_response}
                except httpx.HTTPError as e:
                    print(e)
                    raise HTTPException(status_code=e.response.status_code, detail=str(e.response.text))


        return {"api_response": api_response}

            # if len(updates) >= 100:
            #     # update_json_strings_in_cache(updates, price)
            #     print("\n\n\n 100 records queried successfully \n\n\n")
            #
            #     break

    except Exception as e:
        print(f"WebSocket disconnected {e}")