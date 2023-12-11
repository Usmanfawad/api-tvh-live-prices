from fastapi import APIRouter, status, Response, HTTPException, Depends, status, Body
import asyncio
import httpx

import time


from App.db.session import get_db
from App.db.controllers.tbl_cache import delete_table_cache, insert_into_table_cache, delete_from_table_cache, select_from_table_cache


from App.schema import UserInput

router = APIRouter()

@router.post("/", tags=["index"])
async def user_home(userInput : UserInput):
    print(userInput)
    return {
        "Success": "500"
    }

@router.post("/submitProcess", tags=["home"])
async def user_home():
    print("URL")
    # delete_table = delete_table_cache()
    insert_table = insert_into_table_cache()
    if insert_table:
        return {
            "Success": "500"
        }
    else:
        print("Err")
        raise HTTPException(status_code=404, detail="Table didnt delete")



async def perform_database_operation(batch_number):
    # Your asynchronous database operation here
    print(f"Batch {batch_number} in progress")
    await asyncio.sleep(10)
    return f"Batch {batch_number} completed."

@router.get("/process_batches")
async def process_batches():
    results = await asyncio.gather(
        perform_database_operation(1),
        perform_database_operation(2),
        perform_database_operation(3),
        perform_database_operation(4),
    )
    return results