import httpx
import asyncio
import base64

from App.db.controllers.tbl_cache import delete_table_cache, insert_into_table_cache, delete_from_table_cache, select_from_table_cache


def to_base64(string_credentials):
    sample_string_bytes = string_credentials.encode("ascii")

    base64_bytes = base64.b64encode(sample_string_bytes)
    base64_string = base64_bytes.decode("ascii")

    return base64_string

def tvh_api(line_number):

    data_from_tbl_cache = select_from_table_cache(conn)

    line = {
        "lineNumber": index,
        "makeCode": row.Lieferant_Marke,
        "partNumber": row.Bestellnummer,
        "customerPartNumber": f"Testanfrage Teil {index}",
        "quantity": 3,
        "text": f"inquiry extra text{index}"
    }

    payload = {
        "text": "Text abc def",
        "customerInquiryNumber": "Testanfrage inquiry",
        "customerCode": "00597861",
        "customerContactName": "Jan Theunert",
        "lines": [line]
    }

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic MDA1OTc4NjErcmVzdEB0dmguY29tOm5UQ2VucjRBNjJ5MkUzSkZXcmdicUZoOA=='
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(ROUTE_POST, headers=headers, json=dict(video))
            response.raise_for_status()
            # Parse and return the response data
            api_response = response.json()
            print(api_response)
            return {"api_response": api_response}
        except httpx.HTTPError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e.response.text))