import httpx
import os
import asyncio
import base64
import json
from decimal import Decimal


from fastapi import APIRouter, status, Response, HTTPException, Depends, status, Body, WebSocket, WebSocketDisconnect


from App.db.controllers.tbl_cache import delete_table_cache, insert_into_table_cache, delete_from_table_cache, select_from_table_cache, update_json_strings_in_cache


PATH_API_PY = os.getenv("ENV_PATH_API_PY")

def to_base64(string_credentials):
    # 00597861+rest@tvh.com:nTCenr4A62y2E3JFWrgbqFh8
    sample_string_bytes = string_credentials.encode("ascii")

    base64_bytes = base64.b64encode(sample_string_bytes)
    base64_string = base64_bytes.decode("ascii")

    return base64_string

async def tvh_api(
        batch_number,
        userPassword,
        customerPartNumber,
        fallbackQuantity,
        customerCode,
        userText,
        lower_bound,
        upper_bound,
        websocket: WebSocket
):
    # Getting makecodes from the file
    with open(r"C:\NextRevol\NufaersatzteileProject\App\makeCodes.json", "r") as json_file:
        data = json.load(json_file)
    try:
        # Here the customer code from frontend input will be there
        # ROUTE_POST = f"https://api.tvh.com/customers/customerCode/inquiries"
        ROUTE_POST = "https://api.tvh.com/customers/00783794/inquiries"


        str_creds = f"{customerCode}+rest@tvh.com:{userPassword}"
        creds_encoded = to_base64(str_creds)


        data_from_tbl_cache = select_from_table_cache()
        data_from_cache = data_from_tbl_cache[lower_bound:upper_bound]
        updates = []

        for index, row in enumerate(data_from_cache, 1):
            try:
                # if row[3] == "":
                # print("Json request: NULL")
                # print("----------------------Loop----------------------")ls
                # enumerate, starting item 1
                line = {
                    # Line number fixed, its just when you send multiple requests at one time
                    "lineNumber": 1,
                    "makeCode": data[row[0]],
                    "partNumber": row[1],
                    "customerPartNumber": f"{customerPartNumber} {index}",
                    # Fallback quantity condition, if it exists in the database, then use it or else input
                    # "quantity": row.inquiryAmount,
                    "quantity" : 1,
                    "text": userText
                }
                print(customerCode)
                payload = {
                    "text": "Text abc def",
                    "customerInquiryNumber": "Testanfrage inquiry",
                    # Customer code static
                    # "customerCode": customerCode,
                    "customerCode": f"{customerCode}",
                    "customerContactName": "Jan Theunert",
                    "lines": [line]
                }

                headers = {
                    'Content-Type': 'application/json',
                    # Authorization header static
                    # 'Authorization': f"Basic {creds_encoded}"
                    'Authorization': 'Basic MDA1OTc4NjErcmVzdEB0dmguY29tOm5UQ2VucjRBNjJ5MkUzSkZXcmdicUZoOA=='
                }

                complete_request = {
                    "url": ROUTE_POST,
                    "method": "POST",
                    "headers": headers,
                    "payload": payload
                }
                json_dump = json.dumps(complete_request, indent=4)

            except Exception as e:
                # Case where the pre httpx error is for instance '#NV'. The key cannot be found. In this case, delete the item.
                # add a script inside tbl_cache.py that just inserts, error inside the json_string column and add implementation here
                print("Pre httpx async error is: " + str(e))
                continue

            async with httpx.AsyncClient() as client:
                try:
                    # print("----------------------API call----------------------")
                    updates = []
                    response = await client.post(ROUTE_POST, headers=headers, json=dict(payload), timeout=150)
                    response.raise_for_status()
                    print("The response is: ")
                    print(response)
                    # Parse and return the response data
                    api_response = response.json()
                    inquiry_number = dict(api_response[0])["inquiryNumberTVH"]
                    try:
                        price = Decimal(dict(api_response[0])["lines"][0]["price"]).quantize(Decimal('0.00'))
                        listPrice = Decimal(dict(api_response[0])["lines"][0]["listPrice"]).quantize(Decimal('0.00'))
                    except:
                        price = dict(api_response[0])["lines"][0]["price"]
                        listPrice = dict(api_response[0])["lines"][0]["listPrice"]
                    partNumber = dict(api_response[0])["lines"][0]["partNumber"]
                    makeCode = dict(api_response[0])["lines"][0]["makeCode"]
                    availability_code = dict(api_response[0])["lines"][0]["availabilityCode"]
                    await websocket.send_text(f"Thread number: {batch_number} | Inquiry number: {inquiry_number} | Part number: {partNumber} | Make code: {makeCode} ")
                    api_response_json_dumps = json.dumps(api_response, indent= 4)
                    updates.append((row[0], row[1], json_dump, api_response_json_dumps))
                    print("Price: " + str(price))
                    print("ListPrice: " + str(listPrice))
                    update_db = update_json_strings_in_cache(updates, price, listPrice, availability_code)
                    # return {"api_response": api_response}

                except httpx.HTTPError as e:
                    print("Error here")
                    with open(r'C:\NextRevol\NufaersatzteileProject\App\db\errorLog.txt', 'a') as f:
                        f.write(str(payload))
                        f.write("\n")
                    print("httpx Error: " + str(e))
                    # add a script inside tbl_cache.py that just inserts, error inside the json_string column and add implementation here
                    # raise HTTPException(status_code=e.response.status_code, detail=str(e.response.text))

        return {"api_response": api_response}

            # if len(updates) >= 100:
            #     # update_json_strings_in_cache(updates, price)
            #     print("\n\n\n 100 records queried successfully \n\n\n")
            #
            #     break

    except Exception as e:
        pass
        print(f"WebSocket disconnected and thread terminated {e}")