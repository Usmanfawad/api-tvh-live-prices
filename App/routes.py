from fastapi import APIRouter, status, Response, HTTPException, Depends, status, Body, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

from typing import Deque, List, Optional, Tuple

import asyncio
import httpx
import json
import datetime
import time
import os


from App.db.session import get_db
from App.db.controllers.tbl_cache import delete_table_cache, insert_into_table_cache, delete_from_table_cache, select_from_table_cache
from App.tvh.api import tvh_api
from App.post_processing import *

from App.schema import UserInput

router = APIRouter()

@router.post("/", tags=["index"])
async def user_home(userInput: UserInput):
    print(get_db())
    # tvh_api_call = await tvh_api(customerCode=userInput.customerCode, fallbackQuantity=userInput.fallbackQuantity, userText=userInput.userText)
    return {
        "Success": "500"
    }

@router.post("/preProcessing", tags=["preProcessing"])
async def pre_processing():
    print("Being called")
    delete_table = delete_table_cache()
    insert_table = insert_into_table_cache()
    # delete_from = delete_from_table_cache()
    try:
        return {
            "Success": "Pre Processing script successful"
        }
    except Exception as e:
        print("Exception")
        raise HTTPException(status_code=404, detail="Access db pre-processing error.")

@router.post("/postProcessing", tags=["postProcessing"])
async def post_processing():
    print("Being called")
    update_tbl_Preis()
    try:
        return {
            "Success": "Post processing script successful"
        }
    except Exception as e:
        print("Exception")
        raise HTTPException(status_code=404, detail="Access db post-processing error.")


userInput = {}

@router.websocket("/ws/{customerCode}/{userPassword}/{customerPartNumber}/{userText}/{fallbackQuantity}/{toUpdateArticles}/{parallelConnections}")
async def websocket_endpoint(
        websocket: WebSocket,
        customerCode: str,
        userPassword: str,
        customerPartNumber: Optional[str] = "No text",
        userText: Optional[str] = "No text",
        fallbackQuantity: Optional[int] = 1,
        toUpdateArticles: Optional[int] = 10000,
        parallelConnections : Optional[int] = 1
):


    userInput['customerCode'] = customerCode
    userInput['fallbackQuantity'] = fallbackQuantity
    userInput['userText'] = userText


    await websocket.accept()
    await simulate_task(websocket, parallelConnections = parallelConnections, toUpdateArticles = toUpdateArticles)
    await websocket.close()



async def perform_database_operation(batch_number, lower_bound, upper_bound, websocket: WebSocket):
    # Your asynchronous database operation here
    await asyncio.sleep(batch_number + 3)
    ct = datetime.datetime.now()
    await websocket.send_text(f" -------- Initiate time: {ct} -------- ")
    await websocket.send_text(f" -------- Thread {batch_number} Initiated --------")
    tvh_api_call = await tvh_api(
        batch_number=batch_number,
        customerCode=userInput['customerCode'],
        fallbackQuantity=userInput['fallbackQuantity'],
        userText=userInput['userText'],
        lower_bound=lower_bound,
        upper_bound=upper_bound,
        websocket=websocket
    )
    await websocket.send_text(f"\n -------- Thread {batch_number} terminated -------- \n")
    ct = datetime.datetime.now()
    await websocket.send_text(f" -------- Termination time: {ct} -------- ")

    # await asyncio.sleep(10)
    return f"Batch {batch_number} completed."



async def simulate_task(
        websocket: WebSocket,
        parallelConnections : Optional[int] = 1,
        toUpdateArticles: Optional[int] = 10000
):
    print("To update articles  : " + str(toUpdateArticles))
    print("Parallel connections: " + str(parallelConnections))
    st = datetime.datetime.now()
    await websocket.send_text(f" -------- Start timestamp: {st} -------- ")
    try:
        if parallelConnections == 1:
            print(str(parallelConnections) + " thread executing")
            results = await asyncio.gather(
                perform_database_operation(1, 0, toUpdateArticles, websocket)
            )
        elif parallelConnections == 2:

            to_increment = int(toUpdateArticles / 3)

            results = await asyncio.gather(
                perform_database_operation(1, 0, to_increment, websocket),
                perform_database_operation(2, to_increment, to_increment * 2 + 1, websocket)
            )
        elif parallelConnections == 3:

            to_increment = int(toUpdateArticles / 3)
            print(to_increment)
            results = await asyncio.gather(
                perform_database_operation(1, 0, to_increment, websocket),
                perform_database_operation(2, to_increment, to_increment * 2, websocket),
                perform_database_operation(3, to_increment * 2, to_increment * 3 + 2, websocket)
            )
        elif parallelConnections == 4:

            to_increment = int(toUpdateArticles / 4)

            results = await asyncio.gather(
                perform_database_operation(1, 0, to_increment, websocket),
                perform_database_operation(2, to_increment, to_increment * 2, websocket),
                perform_database_operation(3, to_increment * 2, to_increment * 3, websocket),
                perform_database_operation(4, to_increment * 3, to_increment * 4 + 3, websocket)
            )
        else:
            print("Unexepected error occured")

        result_data = {"status": "success", "message": "Task completed!"}
        await websocket.send_text(json.dumps(result_data))

    except WebSocketDisconnect:
        print("WebSocket disconnected")

    et = datetime.datetime.now()
    await websocket.send_text(f" -------- End timestamp: {et} -------- ")