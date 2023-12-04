from fastapi import APIRouter, status, Response, HTTPException, Depends, status, Body
import asyncio


import time


from App.db.session import get_db
from App.db.controllers.fill_cache_table import delete_table_cache, insert_into_table_cache, delete_from_table_cache, select_from_table_cache


router = APIRouter()

@router.get("/", tags=["index"])
async def user_home():
    return {
        "Success": "500"
    }

@router.post("/submitProcess", tags=["home"])
async def user_home():
    print("URL")
    # delete_table = delete_table_cache()
    delete_table = insert_into_table_cache()
    if delete_table:
        return {
            "Success": "500"
        }
    else:
        print("Err")
        raise HTTPException(status_code=404, detail="Table didnt delete")



async def perform_database_operation(batch_number):
    # Your asynchronous database operation here
    print(f"Batch {batch_number} in progress")
    await asyncio.sleep(10)  # Simulating a 10-minute operation
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