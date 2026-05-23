from datetime import datetime
from typing import Annotated, AsyncIterable, Iterable

import anyio
from fastapi import APIRouter, BackgroundTasks, Body, Depends , HTTPException, Header, Header, Request, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse, JSONResponse, RedirectResponse, StreamingResponse
from fastapi.sse import EventSourceResponse, ServerSentEvent
from pydantic import BaseModel, ValidationError


router = APIRouter(
    prefix = "/items",
    tags = ["items"],

    responses = { 404: {"description": "Not found"}},


)

fake_items_db = {"plumbus": {"name":"Plumbus"}, "gun":{"name": "Portal Gun"}}


###Used for Both JSON Streaming and Server Sent Events (SSE) Examples###
# class Item(BaseModel):
#     name: str
#     description: str | None

# items = [
#     Item(name="Plumbus", description="Everyone has a plumbus in their home"),
#     Item(name="Portal Gun", description="A gun that creates portals"),
#     Item(name="Meeseeks Box", description="A box that summons a meeseeks")
# ]

#######Json Streaming Examples########
# @router.get("/stream")
# async def stream_items() -> AsyncIterable[Item]:
#     for item in items:
#         yield item 

# @router.get("/stream-no-async")
# def stream_items_no_model() -> Iterable[Item]:
#     for item in items:
#         yield item

# @router.get("/stream-no-annotation")
# async def stream_items_no_annotation():
#     for item in items:
#         yield item
# @router.get("/stream-no-async-no-annotation")
# def stream_items_no_async_no_annotation():
#     for item in items:
#         yield item



####Server Sent Events (SSE) Examples######
# @router.get("/stream",response_class=EventSourceResponse)
# async def stream_items() -> AsyncIterable[Item]:
#     for item in items:
#         yield item

# @router.get("/stream-no-async", response_class=EventSourceResponse)
# def stream_items_no_async() -> Iterable[Item]:
#     for item in items:
#         yield item

# @router.get("/stream-no-annotation",response_class=EventSourceResponse)
# async def stream_items_no_annotation():
#     for item in items:
#         yield item

# @router.get("/stream-no-async-annotation",response_class=EventSourceResponse)
# def stream_items_no_async_no_annotation():
#     for item in items:
#         yield item

# ###Server Sent Events (SSE) with Dependency Injection Example######
# class Item(BaseModel):
#     name: str
#     price: float

# items = [
#     Item(name="Plumbus", price= 99.99),
#     Item(name="Portal Gun", price= 299.99),
#     Item(name="Meeseeks Box", price= 9.99)
# ]

# @router.get("/stream",response_class=EventSourceResponse)
# async def stream_items() -> AsyncIterable[ServerSentEvent]:
#    yield ServerSentEvent(comment="stream of item updates")
#    for i , item in enumerate(items):
#        yield ServerSentEvent(data=item,event = "item_update", id=str(i + 1), retry=5000)


###Server Sent Events (SSE)  with Raw Data Example######

# @router.get("/stream", response_class=EventSourceResponse)
# async def stream_logs() -> AsyncIterable[ServerSentEvent]:
#     logs = [
#         "2025-01-01 INFO Application started",
#         "2025-01-01 INFO Processing request",
#         "2025-01-01 ERROR An error occurred",
#         "2025-01-01 INFO Application stopped"
 
#     ]
#     for log_line in logs :
#         yield ServerSentEvent(raw_data=log_line)




### SSE  Resuming with Latest Event ID Example ######
# class Item(BaseModel):
#     name: str
#     price: float

# items = [
#     Item(name="Plumbus", price= 99.99),
#     Item(name="Portal Gun", price= 299.99),
#     Item(name="Meeseeks Box", price= 9.99)
# ]

# @router.get("/stream",response_class=EventSourceResponse)
# async def stream_items(
#     last_event_id : Annotated[int | None , Header()] = None
# ) -> AsyncIterable[ServerSentEvent]:
#     start = last_event_id + 1 if last_event_id is not None else 0
#     for i, item in enumerate(items):
#         if i < start:
#             continue
#         yield ServerSentEvent(data=item, id=str(i))


###SSE with Post Method Example######

# class Prompt(BaseModel):
#     text : str

# @router.post("/stream", response_class=EventSourceResponse)
# async  def stream_chat(prompt: Prompt) -> AsyncIterable[ServerSentEvent]:
#     words = prompt.text.split()
#     for word in words:
#         yield ServerSentEvent(data=word, event="token")
#     yield ServerSentEvent(raw_data="[DONE]", event="done")


# @router.get("/")
# async def read_items():
#     return fake_items_db

# @router.get("/{item_id}")
# async def read_item(item_id: str):
#     if item_id not in fake_items_db:
#         raise HTTPException(status_code=404, detail="Item not found")
#     return {"name": fake_items_db[item_id]["name"], "item_id": item_id}

# @router.put( 
#     "/{item_id}",
#     tags = ["custom"],
#     responses = {403:{"description":"Operation forbidden"}},
# )
# async def update_item(item_id: str):
#     if item_id != "plumbus":
#         raise HTTPException(
#             status_code=403, detail="You can only update the item: plumbus"

#         )
#     return {"item_id": item_id, "name": "The great Plumbus"}



#####Background Tasks Example######

# def  write_notification(email: str, message =" "):
#     with open("log.txt", mode="w") as  email_file:
#         content = f"notification for {email}: {message}"
#         email_file.write(content)


# @router.post("/send-notification/{email}")
# async def send_notification(email: str, background_taks: BackgroundTasks):
#     background_taks.add_task(write_notification, email, message="some notification")
#     return {"message": "Notification sent in the background"}



###Dependency Injection Example##

# def write_log(message:str):
#     with open("log.txt", mode="a") as log:
#         log.write(message)

# def get_query(background_tasks: BackgroundTasks, q: str | None = None):

#     if q:
#         message = f"found query: {q} \n"
#         background_tasks.add_task(write_log, message)
#         return q
    
# @router.post("/send-notification/{email}")
# async def send_notification(
#     email : str, background_taks: BackgroundTasks, q: Annotated[str, Depends(get_query)]


# ):
#     message = f"message to {email} \n"
#     background_taks.add_task(write_log, message)
#     return {"message": "Notification sent in the background", "query": q}





############################ADVANCED USER GUIDE EXAMPLES############################
#######################################################################################



# ##Data Streaming Examples##

# message = """
# Rick: (stumbles in drunkenly, and turns on the lights) Morty! You gotta come on. You got--... you gotta come with me.
# Morty: (rubs his eyes) What, Rick? What's going on?
# Rick: I got a surprise for you, Morty.
# Morty: It's the middle of the night. What are you talking about?
# Rick: (spills alcohol on Morty's bed) Come on, I got a surprise for you. (drags Morty by the ankle) Come on, hurry up. (pulls Morty out of his bed and into the hall)
# Morty: Ow! Ow! You're tugging me too hard!
# Rick: We gotta go, gotta get outta here, come on. Got a surprise for you Morty.
# """

# @router.get("/story/stream",response_class=StreamingResponse)
# async def stream_story() -> AsyncIterable[str]:
#     for line in message.splitlines():
#         yield line

# @router.get("/story/stream-no-async", response_class=StreamingResponse)
# def stream_story_no_async() -> Iterable[str]:
#     for line in message.splitlines():
#         yield line

# @router.get("/story/stream-no-annotation", response_class=StreamingResponse)
# async def stream_story_no_annotation():
#     for line in message.splitlines():
#         yield line

# @router.get("/story/stream-bytes", response_class= StreamingResponse)
# async def stream_story_bytes() -> AsyncIterable[bytes]:
#     for line in message.splitlines():
#         yield line.encode("utf-8")

# @router.get("/story/stream-no-async-bytes", response_class=StreamingResponse)
# def stream_story_no_async_bytes() -> Iterable[bytes]:
#     for line in message.splitlines():
#         yield line.encode("utf-8")

# @router.get("/story/stream-no-annotation-bytes", response_class=StreamingResponse)
# async def  stream_story_no_annotation_bytes():
#     for line in message.splitlines():
#         yield line.encode("utf-8")

# @router.get("/story/stream-no-async-no-annotation-bytes",response_class=StreamingResponse)
# def stream_story_no_async_no_annotation_bytes():
#     for line in message.splitlines():
#         yield line.encode("utf-8")








####A Custom PNGStreamingResponse Example######

# import base64
# from collections.abc import AsyncIterable, Iterable
# from io import BytesIO

# from fastapi import FastAPI
# from fastapi.responses import StreamingResponse

# image_base64 = "iVBORw0KGgoAAAANSUhEUgAAAB0AAAAdCAYAAABWk2cPAAAAbnpUWHRSYXcgcHJvZmlsZSB0eXBlIGV4aWYAAHjadYzRDYAwCET/mcIRDoq0jGOiJm7g+NJK0vjhS4DjIEfHfZ20DKqSrrWZmyFQV5ctRMOLACxglNCcXk7zVqFzJzF8kV6R5vOJ97yVH78HjfYAtg0ged033ZgAAAoCaVRYdFhNTDpjb20uYWRvYmUueG1wAAAAAAA8P3hwYWNrZXQgYmVnaW49Iu+7vyIgaWQ9Ilc1TTBNcENlaGlIenJlU3pOVGN6a2M5ZCI/Pgo8eDp4bXBtZXRhIHhtbG5zOng9ImFkb2JlOm5zOm1ldGEvIiB4OnhtcHRrPSJYTVAgQ29yZSA0LjQuMC1FeGl2MiI+CiA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPgogIDxyZGY6RGVzY3JpcHRpb24gcmRmOmFib3V0PSIiCiAgICB4bWxuczpleGlmPSJodHRwOi8vbnMuYWRvYmUuY29tL2V4aWYvMS4wLyIKICAgIHhtbG5zOnRpZmY9Imh0dHA6Ly9ucy5hZG9iZS5jb20vdGlmZi8xLjAvIgogICBleGlmOlBpeGVsWERpbWVuc2lvbj0iMjkiCiAgIGV4aWY6UGl4ZWxZRGltZW5zaW9uPSIyOSIKICAgdGlmZjpJbWFnZVdpZHRoPSIyOSIKICAgdGlmZjpJbWFnZUxlbmd0aD0iMjkiCiAgIHRpZmY6T3JpZW50YXRpb249IjEiLz4KIDwvcmRmOlJERj4KPC94OnhtcG1ldGE+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAKPD94cGFja2V0IGVuZD0idyI/PnQkBZAAAAAEc0JJVAgICAh8CGSIAAABoklEQVRIx8VXwY7FIAjE5iXWU+P/f6RHPNW9LIaOoHYP+0yMShVkwNGG1lqjfy4HfaF0oyEEt+oSQqBaa//m9Wd6PlqhhbRMDiEQM3e59FNKw5qZHpnQfuPaW6lazsztvu/eElFj5j63lNLlMz2ttbZtVMu1MTGo5Sujn93gMzOllKiUQjHGB9QxxneZhJ5iwZ1rL2fwenoGeL0q3wVGhBPHMz0PeFccIfASEeWcO8xEROd50q6eAV6s1s5XXoncas1EKqVQznnwUBdJJmm1l3hmmdlOMrGO8Vl5gZ56Y0y8IZF0BuqkQWM4B6HXrRCKa1SEqyzEo7KK59RT/VHDjX3ZvSefeW3CO6O6vsiA1NrwVkxxAcYTCcHyTjZmJd00pugBQoTnzjvn+kzLBh9GtRDjhleZFwbx3kugP3GvFzdkqRlbDYw0u/HxKjuOw2QxZCGL5V5f4l7cd6qsffUa1DcLM9N1XcTMvep5ul1e4jNPtZfWGIkE6dI8MquXg/dS2CGVJQ2ushd5GmlxFdOw+1tRa32MY4zDQ9yaZ60J3/iX+QG4U3qGrFHmswAAAABJRU5ErkJggg=="
# binary_image = base64.b64decode(image_base64)


# def read_image() -> Iterable[bytes]:
#     return BytesIO(binary_image)

# class PNGStreamingResponse(StreamingResponse):
#     media_type = "image/png"

# @router.get("/image",response_class=PNGStreamingResponse)
# async def stream_image() ->  AsyncIterable[bytes]:
#     with read_image() as image_file:
#         for chunk in image_file:
#             yield chunk

# @router.get("/image/stream-no-async", response_class=PNGStreamingResponse)
# def stream_image_no_async() -> Iterable[bytes]:
#     with read_image() as image_file:
#         for chunk in image_file:
#             yield chunk

# @router.get("/image/stream-no-async-no-annotation", response_class=PNGStreamingResponse)
# def stream_image_no_async_no_annotation():
#     with read_image() as image_file:
#         for chunk in image_file:
#             yield chunk



######OpenAPI operetionId Example######

# @router.get("/operation-id-example", operation_id="customOperationId")
# async def read_items():
#     return [{"item_id": "Foo"}]




####Advanced Description from docstring Example######


# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price : float
#     tax : float | None = None
#     tags: set [str]= set()

# @router.post("/items/", summary= "Create an item with all the information", description="Create an item with all the information, including name, description, price, tax and a set of unique tags")
# async def create_item(item: Item) -> Item:
#     """
#     Create an item with all the information, including name, description, price, tax and a set of unique tags

#     - **name**: each item must have a name
#     - **description**: a long description of the item
#     - **price**: required price of the item
#     - **tax**: if the item doesn't have tax, you can omit this
#     - **tags**: a set of unique tag strings for this item
#     """
#     return item


###OpenApi Extensions Example######

# @router.get("/items/",openapi_extra={"x-aperture-labs-portal-gun": "blue"})
# async def read_items():
#     return[{"item_id": "portal-gun"}]







# ###Custom OpenApi path operation  schema example######
# def magic_data_reader(raw_body: bytes):
#     return{
#         "size": len(raw_body),
#         "content":{
#             "name": "Magiic",
#             "price": 42,
#             "description": "Just  kiddin , no magic here.",

#         },
#     }

# @router.post("/items/", 
#    openapi_extra={
#         "requestBody": {
#             "content": {
#                 "application/json": {
#                     "schema": {
#                         "required": ["name", "price"],
#                         "type": "object",
#                         "properties": {
#                             "name": {"type": "string"},
#                             "price": {"type": "number"},
#                             "description": {"type": "string"},
#                         },
#                     }
#                 }
#             },
#             "required": True,
#         },
#     },
# )
# async def create_item(request: Request):
#     raw_body = await request.body()
#     data = magic_data_reader(raw_body)
#     return data


# ####Cu7stom OPenAPI content type example######
# import yaml
# class Item(BaseModel):
#     name: str
#     tags: list[str]

# @router.post("/items/",
#     openapi_extra={
#         "requestBody": {
#             "content": {"application/x-yaml": {"schema": Item.model_json_schema()}},
#             "required": True,
#         },
#     },
# )

# async def create_item(request: Request):
#     raw_body = await request.body()
#     try: 
#         data = yaml.safe_load(raw_body)

#     except yaml.YAMLError:#
#         raise HTTPException(status_code=422, detail="Invalid YAML")
#     try:
#         item = Item.model_validate(data)
#     except ValidationError as e:
#         raise HTTPException(status_code=422,detail=e.errors(include_url=False))
#     return item 

####Additional status codes Example######

# from fastapi.responses import JSONResponse
# from fastapi import status


# items = {"foo": {"name": "Fighters", "size": 6}, "bar": {"name": "Tenders", "size": 3}}



# @router.put("/{item_id}")
# async def upsert_item(
#     item_id:str,
#     name: Annotated[str | None , Body()] = None,
#     size: Annotated[int | None , Body()] = None,
# ):
#     if  item_id in items:
#         item = items[item_id]
#         item["name"] = name
#         item["size"] = size

#         return item
#     else:
#         item = {"name": name, "size": size}
#         items[item_id] = item
#         return JSONResponse (status_code=status.HTTP_201_CREATED, content=item)



########Using the jsonable_encoder  in a Response Example######

# class Item(BaseModel):
#     title: str
#     timestamp: datetime
#     description : str | None = None


# @router.get("/{item_id}")
# def update_item(id: str, item: Item):
#     json_compatible_item_data = jsonable_encoder(item)
#     return JSONResponse(content=json_compatible_item_data)



######Returning a custom Response Example######


# @router.get("/legacy/")
# def get_legacy_data():
#     data = """<?xml version="1.0"?>
#     <shampoo>
#     <Header>
#         Apply shampoo here.
#     </Header>
#     <Body>
#         You'll have to use soap here.
#     </Body>
#     </shampoo>
#     """
#     return Response(content=data, media_type="application/xml")

######HTML Response Example######

# @router.get("/items/",response_class= HTMLResponse)
# async def read_items():
#     return """
#     <html>
#         <head>
#             <title>Some HTML in here</title>
#         </head>
#         <body>
#             <h1>Look ma! HTML!</h1>
#         </body>
#     </html>
#     """



######Return a Response Example######



# @router.get("/items/")
# async def read_items():
#     html_content = """
#     <html>
#         <head>
#             <title>Some HTML in here</title>
#         </head>
#         <body>
#             <h1>Look ma! HTML!</h1>
#         </body>
#     </html>
#     """
#     return Response(content=html_content, status_code=200)




####Document in OpenAPI and override  Response Example######


# def generate_html_response():
#     html_content = """
#     <html>
#         <head>
#             <title>Some HTML in here</title>
#         </head>
#         <body>
#             <h1>Look ma! HTML!</h1>
#         </body>
#     </html>
#     """
#     return Response(content=html_content, status_code=200)
# @router.get("/items/", response_class=HTMLResponse)
# async def read_items():
#     return generate_html_response()



# @router.get("/legacy/")
# def get_legacy_data():
#     data = """<?xml version="1.0"?>
#     <shampoo>
#     <Header>
#         Apply shampoo here.
#     </Header>
#     <Body>
#         You'll have to use soap here.
#     </Body>
#     </shampoo>
#     """
#     return Response(content=data, media_type="application/xml")


#####PlainText Response Example######
# from fastapi.responses import PlainTextResponse
# @router.get("/plaintext/", response_class=PlainTextResponse)
# async def main():
#     return "Hello World"


####RedirectResponse exaples#######

# @router.get("/typer")
# async def redirect_typer():
#     return RedirectResponse("https://typer.tiangolo.com")




# @app.get("/fastapi", response_class=RedirectResponse)
# async def redirect_fastapi():
#     return "https://fastapi.tiangolo.com"


# @router.get("/pydantic", response_class=RedirectResponse, status_code=302)
# async def redirect_pydantic():
#    return "https://docs.pydantic.dev/"


#####StreamingResponse Examples!!!!######
# async  def fake_video_streamer():
#     for i in range(10):
#         yield b"some fake video  bytes"
#         await anyio.sleep(0)
# @router.get("/")
# async def main():
#     return StreamingResponse(fake_video_streamer())



####FileResponse Examples#####
# from fastapi.responses import FileResponse

# some_file_path = "large-video-file.mp4"



# @router.get("/")
# async def main():
#     return FileResponse(some_file_path)