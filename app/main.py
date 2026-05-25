# import random

# from fastapi import Depends, FastAPI, File, Form, HTTPException , Query , Path , Body, Cookie, Header, Request,Response, UploadFile, status
# from typing import Annotated , Literal, Any
# from fastapi.encoders import jsonable_encoder
# from fastapi.exceptions import RequestValidationError
# from fastapi.security import OAuth2PasswordBearer ,  OAuth2PasswordRequestForm
# from pydantic import BaseModel
# from pydantic import AfterValidator, EmailStr, HttpUrl
# from datetime import time, datetime, timedelta, timezone
# from pydantic import BaseModel , Field
# from uuid import UUID
# from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse , RedirectResponse

# app = FastAPI()
# # class Item(BaseModel):
#     name : str
#     description: str | None = None 
#     price :  float 
#     tax : float | None = None 


# @app.get("/items/")
# async def read_items(
#     q:Annotated[
#         str | None , 
#         Query(
#             title="Query string ", 
#             description="Query string for the items to search in the database that have a goot match",
#             min_length = 3

#         )] = None,
# ):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results

# movies = [
#     {"movie_id": 1, "title": "Batman Begins", "genre": "action"},
#     {"movie_id": 2, "title": "The Dark Knight", "genre": "action"},
#     {"movie_id": 3, "title": "Toy Story", "genre": "animation"},
# ]


# @app.get("/movies/search")
# async def movies_search(
#     q:Annotated[str | None, Query(min_length=3)] = None,
#     genre:str | None = None,
#     limit : Annotated[int, Query(ge=1,le=50)] = 10

# ):
#     response = {
#         "search": q,
#         "genre": genre,
#         "results":movies[:limit]
#     }
#     return response


# @app.get("/items/")
# async def read_items(
#     q:Annotated[str | None , Query(alias="item-query")] = None
# ):
#     results = {
#         "items": [
#             {"item_id":"Foo"},
#             {"item_id": "Bar"}
#         ]
#     }
#     if q :
#         results.update({"q":q})
#     return results

#Deprecatingh parameter
# @app.get("/items/")
# async def read_items(
#     q:Annotated[
#         str | None,
#         Query(
#             alias="item-query",
#             title="Query string",
#             description="Quesry string for the items to search in the database that have  a good match",
#             min_length=3,
#             max_length=50,
#             pattern="^fixedquery$",
#             deprecated=True,
#         ),

#     ] = None,
# ):
#     results = {
#         "items":[
#             {"item_id": "Foo"},
#             {"item_id": "Bar"}
#         ]
#     }
#     if q:
#         results.update({"q": q})
#     return results

#Exclude parameters from OpenAPI documentation
# @app.get("/items/")
# async def read_item(
#     hidden_query:Annotated[str | None , Query(include_in_schema=True)] = None,

# ):
#     if hidden_query:
#         return{"hidden_query": hidden_query}
#     else:
#         return{"hidden_query": "Not Found"}


#Custom Vaslidation  
# data = {
#     "isbn-9781529046137": "The Hitchhiker's Guide to the Galaxy",
#     "imdb-tt0371724": "The Hitchhiker's Guide to the Galaxy",
#     "isbn-9781439512982": "Isaac Asimov: The Complete Stories, Vol. 2",
# }

# def check_valid_id(id:str):
#     if not id.startswith(("isbn-", "imdb-")):
#         raise ValueError('Invalid ID Format, it must start with "isbn-" or "imdb-"')
    
#     return id

# @app.get("/items/")
# async def read_items(
#     id: Annotated[str | None , AfterValidator(check_valid_id)] = None,
# ):
#     if id:
#         item = data.get(id)
#     else:
#         id, item = random.choice(list(data.items()))
#     return {"id": id, "name": item}


#Path Parameters and Numeric  Validations 

# @app.get("/items/{item_id}")
# async def read_items(
#     item_id:Annotated[int,Path(title="The ID of the item to get ",description="The unique ID of the item to retrieve ")],
#     q:Annotated[str | None , Query(alias="item-query")] = None,
# ):
#     results = {"item_id": item_id}
#     if q:
#         results.update({"q": q})
#     return results
# @app.get("/items/{item_id}")
# async def read_items(q:str, item_id: int = Path(title="The ID of the item to get")):
#     results = {"item_id": item_id}
#     if q:
#         results.update({"q":q})
#     return results
# @app.get("/items{item_id}")
# async def read_items(
#     *, item_id : int = Path(title="The ID of the item to get"), q: str
# ):
#     results = {"item_id": item_id}
#     if q :
#         results.update({"q":q})
#     return results

# @app.get("/item/{item_id}")
# async def  read_items(
#     item_id: Annotated[int, Path(title="The ID  of the item to get ",ge=1)], q:str
# ):
#     results = {"item_id": item_id}
#     if q:
#         results.update({"q":q})
#     return results

# @app.get("/item/{item_id}")
# async def read_items(
#     item_id : Annotated[int, Path(title="The ID of the item to get ", gt=0, le=1000)],
#     q:str,
# ):
#     results = {"item_id": item_id}
#     if q:
#         results.update({"q": q})
#     return results

# @app.get("/item/{item_id}")
# async def read_item(
#     *,
#     item_id: Annotated[int , Path(title="The ID of the item to get",ge=0,le=1000)],
#     q:str,
#     size:Annotated[float,Query(gt=0,lt=10.5)]

# ):
#     results = {"item_id"}
#     if q:
#         results.update({"q":q})
#     if size:
#         results.update({"size":size})
#     return results


#Query Parameter with a Pydantic Model

# class FilterParams(BaseModel):
#     model_config = {"extra": "forbid"}
#     limit: int = Field(100, gt=0, le=100)
#     offset:int = Field(0,ge=0)
#     order_by: Literal["created_at", "updated_at"] = "created_at"
#     tags: list[str] = []

# @app.get("/items/")
# async def read_items(filter_query:Annotated[FilterParams,Query()]):
#     return filter_query

#Body Multiple Parameters 

# class Item(BaseModel):
#     name:str
#     description:str | None = None
#     price : float
#     tax : float | None = None
# @app.put("/items/{item_id}")
# async def update_item(
#     item_id: Annotated [int,Path(title="The ID of th3e item to get ",ge=0,le=1000)],
#     q:str | None = None,
#     item : Item | None = None ,

# ):
#     results = {"item_id":item_id}
#     if q:
#         results.update({"q":q})
#     if item:
#         results.update({"item":item})
#     return results


# class Item(BaseModel):
#     name : str
#     description : str | None = None
#     price : float
#     tax : float | None = None

# class User(BaseModel):
#     username: str
#     full_name: str | None = None 

# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item, user : User):
#     results = {"item_id": item_id, "item": item, "user": user}
#     return results


# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None


# class User(BaseModel):
#     username: str
#     full_name: str | None = None
# @app.put("/items/{item_id}")
# async def update_item(
#     item_id : int , item:Item , user : User , importance : Annotated[int, Body()]
# ):  
#     results = {"item_id": item_id, "item": item , "user": user, "importance": importance}
#     return results 

# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None


# @app.put("/item/{item_id}")
# async def update_item(item_id: int, item : Annotated[Item, Body(embed=True)]):
#     results = {"item_id": item_id, "item": item} 
#     return results


# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None


# class User(BaseModel):
#     username: str
#     full_name: str | None = None

# @app.put("/item/{item_id}")

# async def update_item(
#     *,
#     item_id: int,
#     item : Item,
#     user:User,
#     importance: Annotated[int,Body(gt=0)],
#     q:str | None  = None ,

# ):
#     results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
#     if q :
#         results.update({"q": q})
#     return results


# Body Fields 
# class Item(BaseModel):
#     name : str
#     description: str | None = Field(
#         default=None, title="The description of the item", max_length=300 
#     )
#     price : float = Field (gt=0,description="The price must be greater than zero")
#     tax: float | None = None
# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
#     results = {"item_id": item_id, "item":item}
#     return results


#List fields 
# class Item(BaseModel):
#     name:str
#     description: str | None = None 
#     price : float
#     tax: float | None = None 
#     tags : list[str] = []

# @app.put("/items/{item_id}")
# async def update_item(item_id:int, item: Annotated[Item,Body(embed=True)]):
#     results = {"item_id": item_id, "item": item}
#     return results

# class Item(BaseModel):
#     name:str
#     description: str | None = None 
#     price : float
#     tax: float | None = None 
#     tags : list[str] = set()

# @app.put("/items/{item_id}")
# async def update_item(item_id:int, item: Item):
#     results = {"item_id": item_id, "item": item}
#     return results


# class Image(BaseModel):
#     url: HttpUrl
#     name : str

# class Item(BaseModel):
#     name: str
#     description : str | None = None 
#     price : float 
#     tax: float | None = None 
#     tags : set[str] = set()
#     image:Image | None = None 
# @app.put("/items/{item_id}")
# async def update_item(item_id: int , item:Item):
#     results = {"item_id": item_id, "item":item}
#     return results

# class Image(BaseModel):
#     url: HttpUrl
#     name : str

# class Item(BaseModel):
#     name: str
#     description : str | None = None 
#     price : float 
#     tax: float | None = None 
#     tags : set[str] = set()
#     images:list[Image] | None = None 
# @app.put("/items/{item_id}")
# async def update_item(item_id: int , item:Item):
#     results = {"item_id": item_id, "item":item}
#     return results


# class Image(BaseModel):
#     url: HttpUrl
#     name : str
# class Item(BaseModel):
#     name: str
#     description: str | None = None 
#     price : float 
#     tax : float | None = None
#     tags : set[str] = set()
#     images : list[Image] | None = None 
# class Offer (BaseModel):
#     name: str
#     description: str | None = None 
#     price : float 
#     items: list [Item]

# @app.post("/offers/")
# async def create_offer(offer:Offer):
#     return offer


# class Image(BaseModel):
#     url:HttpUrl
#     name:str

# @app.post("/images/multiple/")
# async def create_multiple_images(images:list[Image]):
#     return images


# @app.post("/index-weights/")
# async def create_index_weights(weights: dict[int, float]):
#     return weights


#Declare Request Example Data

# class Item (BaseModel):
#     name: str
#     description : str | None = None 
#     price: float 
#     tax: float | None = None
#     model_config = {
#         "json_schema_extra":{
#             "examples":[
#                 {
#                     "name": "Foo",
#                     "description": "A very nice Item",
#                     "price": 35.4,
#                     "tax":3.2
#                 }
    
#             ]
#         }
#     }

# @app.put("/items/{item_id}")
# async def update_item(item_id:int,item:Item):
#     results = {"item_id": item_id, "item": item}
#     return results

#Field Additional arguments 
# class Item(BaseModel):
#     name: str = Field(examples=["Foo"])
#     description: str | None = Field(default=None, examples=["A very nice Item"])
#     price : float = Field(examples=[35.4])
#     tax: float | None = Field ( default=None, examples=[3.2])

# @app.put("/items/{item_id}")
# async def update_item(item_id: int , item: Item):
#     results = {"item_id": item_id, "item": item}
#     return results  
# class Item(BaseModel):
#     name : str
#     description: str | None = None
#     price : float 
#     tax: float | None = None


# @app.put("/items/{item_id}")
# async def update_item(
#     item_id: int,
#     item: Annotated[
#         Item,
#         Body(
#             examples=[
#                 {
#                     "name": "Foo",
#                     "description": "A very nice Item",
#                     "price": 35.5,
#                     "tax": 3.2
#                 }
#             ],
#         ),
#     ],
# ):
#     results = {"item_id": item_id, "item": Item}
#     return results

#Body With multiple examples
# class Item(BaseModel):
#     name : str
#     description: str | None = None
#     price : float 
#     tax: float | None = None

# @app.put("/items/{item_id}")
# async def update_item(
#     *,
#     item_id: int,
#     item: Annotated[
#         Item,
#         Body(
#             examples=[
#                 {
#                     "name":"Foo",
#                     "description": "A very nice Item",
#                     "price": 35.4,
#                     "tax": 3.5,
#                 },
#                 {
#                     "name": "Bar",
#                     "price": "35.5"

#                 },
#                 {
#                     "name": "Baz",
#                     "price": "thirty five point four"
#                 }
#             ],
#         ),
#     ],
# ):
#     results = {"item_id": item_id, "item": item}
#     return results

#OpenAPI-specific examples   

# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None
# @app.put("/items/{item_id}")

# async def update_item(
#     *,
#     item_id: int,
#     item: Annotated[
#         Item,
#         Body(
#             openapi_examples={
#                 "normal":{
#                     "summary": "A normal example",
#                     "description": " A **normal** item works correctly",
#                     "value":{
#                         "name":"Foo",
#                         "description": "A very nice Item",
#                         "price": 35.4,
#                         "tax": 3.2,
#                     },
#                 },"converted":{
#                     "summary": "An example with converted data",
#                     "description": "FastAPI can convert price'strings ' to actual numbers automically",
#                     "value":{
#                         "name": "Bar",
#                         "price":"35.5",

#                     },

#                 },"invalid":{
#                     "summary": "Invalid data is rejected with an error",
#                     "value":{
#                         "name" : "Baz",
#                         "price": "thirty five point four",
#                     },

#                 },

#             },

#         ),
#     ],
# ):
#     results = {"item_id": item_id, "item":item}
#     return results

# @app.put("/items/{item_id}")
# async def read_items(
#     item_id: UUID,
#     start_datetime: Annotated[datetime,Body()],
#     end_datetime: Annotated[datetime,Body()],
#     process_after: Annotated[timedelta,Body()],
#     repeat_at: Annotated[time | None , Body()] = None,


# ): 
#     start_process = start_datetime + process_after
#     duration = end_datetime - start_process
#     return{
#         "item_id": item_id,
#         "start_datetime": start_datetime,
#         "end_datetime": end_datetime,
#         "process_after":process_after,
#         "reapeat_at": repeat_at,
#         "start_process":start_process,
#         "duration": duration,
#     }

#Cookie Parameters

# @app.get("/items/")
# async def read_items(adds_id:Annotated[str | None , Cookie()] = None):
#     return {"ads_id": adds_id}


# @app.get("/items/")
# async def read_items(ads_id: str | None = Cookie(default=None)):
#     return {"ads_id": ads_id}

#Header Parameters

# @app.get("/items/")
# async def read_items(user_agent: Annotated[str | None , Header()] = None):
#     return {"User-Agent": user_agent}

# @app.get("/items/")
# async def read_items(
#     strange_header: Annotated [str | None , Header(convert_underscores=False)] = None,
# ):
#     return {"strange_header": strange_header}


# @app.get("/items/")
# async def read_items(x_token: Annotated[list[str] | None , Header()] = None):
#     return {"X=Token values": x_token}

#Coolie Parameter Models

# class Cookies(BaseModel):
#     session_id:str
#     fatebook_tracker: str | None  = None
#     googall_tracker: str | None = None

# @app.get("/items/")
# async def read_items(cookies: Annotated[Cookies, Cookie()]):
#     return cookies

# class Cookies(BaseModel):
#     model_config = {"extra": "forbid"}
#     session_id: str | None = None
#     fatebook_tracker: str | None = None
#     googall_tracker: str | None = None

# @app.get("/items/")
# async def read_items(cookies:Annotated[Cookies, Cookie()]):
#     return cookies

#Header Parameter with a Pydantic Model

# class CommonHeaders(BaseModel):
#     host:str
#     save_data: bool
#     if_modified_since : str | None = None 
#     traceparent: str | None = None 
#     x_tag: list[str] = []

# @app.get("/items")
# async def read_items(headers:Annotated[CommonHeaders,Header()]):
#     return headers


#Forbid Extra Headers

# class CommonHeaders(BaseModel):
#     model_config = {"extra": "forbid"}
#     host : str
#     save_data:bool
#     if_modified_since: str | None = None
#     traceparent : str | None = None
#     x_tag : list[str] = []

# @app.get("/items/")
# async def read_items(headers:Annotated[CommonHeaders, Header()]):
#     return headers


#Response Model - Return Type

# class Item (BaseModel):
#     name : str
#     description: str | None = None 
#     price : float 
#     tax: float | None = None
#     tags: list [str] = []

# @app.post("/items/")
# async def create_item(item: Item) -> Item:
#     return item

# @app.get("/items/")
# async def read_items() -> list[Item]:
#     return[
#         Item(name="Portal Gun", price=42.1),
#         Item(name="Plumbus", price=32.1),
#     ]

# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price : float 
#     tax : float | None = None 
#     tags : list [str] = []

# @app.post("/items/",response_model=Item)
# async def create_item(item:Item) -> Any:
#     return item

# @app.get("/items/",response_model=list[Item])
# async def read_items()-> Any:
#     return [
#         {"name": "Portal Gun", "price": 42.1},
#         {"name": "Plumbus", "price": 32.1}
#     ]

#Return the same input data

# class UserIn (BaseModel):
#     username : str
#     password: str
#     email: EmailStr
#     full_name : str | None = None 

# class UserOut(BaseModel):
#     username: str
#     email: EmailStr
#     full_name : str | None = None 

# @app.post("/user/",response_model=UserOut)
# async def create_user(user:UserIn) -> Any:
#     return user

#Return type and Data Filtering 

# class BaseUser(BaseModel):
#     username: str
#     email: EmailStr
#     full_name: str | None = None

# class UserIn(BaseUser):
#     password: str
# @app.post("/users/")
# async def create_user(user: UserIn) -> BaseUser:
#     return user

#Other Return Type Annotations 
# @app.get("/portal")
# async def get_portal(teleport: bool = False) -> Response:
#  if teleport:
#         return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
#  return JSONResponse(content={"message": "Here's your interdimensional portal."})


#Annotate a Response Subclass
# @app.get("/teleport")
# async def get_teleport() -> RedirectResponse:
#     return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")


#Invalid Return type Annotations 
# @app.get("/portal")
# async def get_portal(teleport:bool = False) -> Response | dict:
#     if teleport:
#         return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
#     return {"message": "Here is your interdimensional portal."}

#Diable response Model
# @app.get("/portal",response_model=None)
# async def get_portal(teleport:bool = False) -> Response | dict:
#     if teleport:
#         return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
#     return {"message": "Here is your interdimensional portal."}

#Response Model encoding parameters 

# class Item(BaseModel):
#     name: str
#     description: str | None = None 
#     price : float
#     tax: float = 10.5
#     tags : list[str] = []

# items = {
#     "foo": {"name": "Foo", "price":50.2},
#     "bar":{"name": "Bar","description": "The bartenders", "price": 62, "tax": 20.2},
#     "baz":{"name": "Baz","description": None, "price": 50.2,"tax":10.5, "tags": []},

# }

# @app.get("/items/{item_id}",response_model=Item, response_model_exclude_unset=True)
# async def read_item(item_id:str):
#     return items[item_id]


#Using set
# class Item(BaseModel):
#     name: str
#     description : str | None = None 
#     price : float 
#     tax : float = 10.5

# items = {
#     "foo":{"name": "Foo", "price": 34.12},
#     "bar":{"name":"Bar","description": "The Bar fighters", "price":62, "tax": 20},
#     "baz":{
#         "name": "Baz",
#         "description": "There goes my baz",
#         "price": 50.2,
#         "tax": 10.5,
#     }
# }

# @app.get(
#     "/items/{item_id}/name",
#     response_model=Item,
#     response_model_include={"name","description"},

# )
# async def read_item_name(item_id: str):
#     return items [item_id]

# @app.get(
#     "/items/{item_id}/public",
#     response_model=Item,
#     response_model_exclude={"tax"}

# )
# async def read_item_public_data(item_id:str):
#     return items[item_id]

# #Using list
# from fastapi import FastAPI
# from pydantic import BaseModel

# app = FastAPI()


# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float = 10.5


# items = {
#     "foo": {"name": "Foo", "price": 50.2},
#     "bar": {"name": "Bar", "description": "The Bar fighters", "price": 62, "tax": 20.2},
#     "baz": {
#         "name": "Baz",
#         "description": "There goes my baz",
#         "price": 50.2,
#         "tax": 10.5,
#     },
# }


# @app.get(
#     "/items/{item_id}/name",
#     response_model=Item,
#     response_model_include=["name", "description"],
# )
# async def read_item_name(item_id: str):
#     return items[item_id]


# @app.get("/items/{item_id}/public", response_model=Item, response_model_exclude=["tax"])
# async def read_item_public_data(item_id: str):
#     return items[item_id]



#Extra Models 

# class UserIn(BaseModel):
#     username: str
#     password: str
#     email: EmailStr
#     full_name: str | None = None


# class UserOut(BaseModel):
#     username: str
#     email: EmailStr
#     full_name: str | None = None


# class UserInDB(BaseModel):
#     username: str
#     hashed_password: str
#     email: EmailStr
#     full_name: str | None = None


# def fake_password_hasher(raw_password: str):
#     return "supersecret" + raw_password


# def fake_save_user(user_in: UserIn):
#     hashed_password = fake_password_hasher(user_in.password)
#     user_in_db = UserInDB(**user_in.model_dump(), hashed_password=hashed_password)
#     print("User saved! ..not really")
#     return user_in_db


# @app.post("/user/", response_model=UserOut)
# async def create_user(user_in: UserIn):
#     user_saved = fake_save_user(user_in)
#     return user_saved


#Union or anyof

# class BaseItem(BaseModel):
#     description : str
#     type: str

# class CarItem(BaseItem):
#     type: str = "car"
# class PlaneItem(BaseItem):
#     type : str = "plane"
#     size : int

# items = {
#     "item1":{"description": "All my friends drive a low rider", "type": "car"},
#     "item2":{
#         "description": "Music is my aeroplane , its my aeroplane",
#         "type": "plane",
#         "size": 5,
#     },
# }
# @app.get("/items/{item_id}", response_model=PlaneItem | CarItem)
# async def read_item(item_id:str):
#     return items[item_id]



#List of Models


# class Item(BaseModel):
#     name: str
#     description: str

# items = [
#     {"name": "Foo", "description": "There comes my here"},
#     {"name": "Red", "description": "It is my aeroplane"},

# ]
# @app.get("/items/",response_model=list[Item])
# async def read_items():
#     return items


#Response with arbitrary dict

# @app.get("/keyword-weights/", response_model=dict[str,float])
# async def read_keyword_weights():
#     return{"foo": 2.3, "bar": 4.5}


#Response Status Code

# @app.post("/items/", status_code=201)
# async def creeate_item(name:str):
#     return {"name": name}

# @app.post("/items/",status_code=status.HTTP_201_CREATED)
# async def create_item(name:str):
#     return {"name": name}

#form Data 

# @app.post("/login/",status_code=status.HTTP_201_CREATED)
# async def login(username: Annotated [str, Form()], password : Annotated[str,Form()]):
#     return {"username": username}


#Form Models

# class FormData(BaseModel):
#     username: str
#     password: str

# @app.post("/login/")
# async def login(data:Annotated [FormData, Form()]):
#     return data


#Forbid Extra  Form Fields

# class FormData(BaseModel):
#     username: str
#     password: str
#     model_config = {"extra": "forbid"}

# @app.post("/login/")
# async def login (data:Annotated [FormData, Form()]):
#     return data


 
# @app.post("/files/")
# async def create_file(file: Annotated [bytes, File()]):
#     return {"file_size": len(file)}

# @app.post("/uploadfile/")
# async def create_upload_file(file: UploadFile):
#     return{"filename": file.filename}


# @app.post("/files/")
# async def create_file(file:Annotated[bytes | None , File()] = None ):
#     if not file:
#         return {"message": "No file  sent"}
#     else:
#         return {"file_size": len(file)}
    
# @app.post("/uploadfile/")
# async def create_upload_file(file : UploadFile | None = None):
#     if not file:
#         return {"message": "No upload file sent"}
#     else:
#         return {"filename": file.filename}


# @app.post("/files/")
# async def create_file(file: Annotated[bytes, File(description= "A file read as bytes ")]):
#     return {"file_size": len(file)}

# @app.post("/uploadfile/")
# async def create_upload_file(
#     file : Annotated[UploadFile, File(description="A file read as UploadFile")],
# ):
#     return {"filename": file.filename}    



# @app.post("/files/")
# async def create_files(files: Annotated[list[bytes], File()]):
#     return {"file_sizes": [len(file) for file in files]}


# @app.post("/uploadfiles/")
# async def create_upload_files(files: list[UploadFile]):
#     return {"filenames": [file.filename for file in files]}


# @app.get("/")
# async def main():
#     content = """
# <body>
# <form action="/files/" enctype="multipart/form-data" method="post">
# <input name="files" type="file" multiple>
# <input type="submit">
# </form>
# <form action="/uploadfiles/" enctype="multipart/form-data" method="post">
# <input name="files" type="file" multiple>
# <input type="submit">
# </form>
# </body>
#     """
#     return HTMLResponse(content=content)


# @app.post("/files/")
# async def create_file(
#     file: Annotated[bytes,File()],
#     fileb: Annotated[UploadFile, File ()],
#     token : Annotated [str, Form()],

# ):
#     return {
#         "file_size": len(file),
#         "token": token,
#         "fileb_content_type": fileb.content_type,
#     }


#Handling Errors
# items = {"foo": "The Foo Wrestlers"}

# @app.get("/items/{item_id}")
# async def read_item(item_id: str):
#     if item_id not in items:
#         raise HTTPException(status_code=404, detail="Item not found")

#     return {"item": items[item_id]} 


#Add Custom headers 

# items = {"foo": "The Foo Wrestlers"}

# @app.get("/items/{item_id}")
# async def read_item(item_id: str):
#     if item_id not in items:
#         raise HTTPException(
#             status_code=404,
#             detail="Item not found",
#             headers={"X-Error": "There goes my error"},

#         )

#     return {"item": items[item_id]} 
 
# class UnicornException(Exception):
#     def __init__(self, name:str):
#         self.name = name

# @app.exception_handler(UnicornException)
# async def unicorn_exception_handler(request: Request, exc: UnicornException):
#     return JSONResponse(
#         status_code= 418,
#         content={"message": f"Oops! {exc.name} did something.There goes a rainbow .."},
#     )

# @app.get("/unicorns/{name}")
# async def read_unicorn(name:str):
#     if name == "yolo":
#         raise UnicornException(name=name)
#     return {"unicorn_name": name}



#Override the default  exception handlers
# from starlette.exceptions import HTTPException as StarletteHTTPException
# @app.exception_handler(StarletteHTTPException)
# async def http_exception_handler(request, exc):
#     return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request, exc: RequestValidationError):
#     message = "Validation errors:"
#     for error in exc.errors():
#         message += f"\nField: {error['loc']}, Error: {error['msg']}"
#     return PlainTextResponse(message, status_code=400)


# @app.get("/items/{item_id}")
# async def read_item(item_id: int):
#     if item_id == 3:
#         raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
#     return {"item_id": item_id}



# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request: Request, exc : RequestValidationError):
#     return JSONResponse(
#         status_code=422,
#         content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
#     )
# class Item(BaseModel):
#     title : str
#     size: int

# @app.post("/items/")
# async def create_item(item: Item):
#     return item



# from fastapi.exception_handlers import(
#     http_exception_handler,
#     request_validation_exception_handler,
# )
# from fastapi.exceptions import RequestValidationError
# from starlette.exceptions import HTTPException as StarlettHTTPException

# @app.exception_handler(StarlettHTTPException)
# async def custom_http_exception_handler(request, exc):
#     print(f"OMG! An HTTP error!: {repr(exc)}")
#     return await http_exception_handler(request,exc)

# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request, exc):
#     print(f"OMD ! The Client send invaslid data!: {exc}")
#     return await request_validation_exception_handler(request,exc)

# @app.get("/items/{item_id}")
# async def read_item(item_id: int):
#     if item_id == 3:
#         raise HTTPException(
#             status_code=418, 
#             detail= "Nope! I do not like 3."
#         )
#     return {"item_id": item_id}



#Response Status Code

# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price : float
#     tax: float | None = None
#     tags : set [str] = set()

# @app.post("/items/", status_code=status.HTTP_201_CREATED)
# async def create_item(item: Item) -> Item:
#     return item


#Tags  

# class Item (BaseModel):
#     name : str
#     description : str | None = None
#     price : float
#     tax: float | None = None
#     tags: set[str] = set()

# @app.post("/items/", tags=["items"])
# async def create_item(item: Item) -> Item:
#     return item

# @app.get("/items/", tags=["items"])
# async def read_items():
#     return [{"name": "Foo", "price": 42}]


# @app.get("/users/",tags = ["users"])
# async def  read_users():
#     return[{"username":  "johndoe"}]

#Summary and description

# class Item (BaseModel):
#     name: str
#     description : str | None = None 
#     price : float 
#     tax: float | None = None 
#     tags : set[str] = set()
# @app.post(
#     "/items/",
#     summary = "Create an Item",
#     description="Create an Item with all the infromation, name, description, price, tax and set of unique tags",

# )
# async def create_item(item: Item) -> Item:
#     return item

# class Item(BaseModel):
#     name: str
#     description : str | None = None
#     price : float  
#     tax : float | None = None
#     tags : set[str] = set()

# @app.post("/items/",summary="Create an Item")
# async def create_item(item:Item) ->Item:
#     """
#     Create an item with all the information:

#     - **name**: each item must have a name
#     - **description**: a long description
#     - **price**: required
#     - **tax**: if the item doesn't have tax, you can omit this
#     - **tags**: a set of unique tag strings for this item
#     """
#     return item



###response Description
# class Item(BaseModel):
#     name : str#
#     description : str | None = None 
#     price: float 
#     tax: float | None = None 
#     tags : set [str] = set()

# @app.post(
#     "/items/",
#     summary="Create an Item",
#     response_description= " The created item",

# )
# async def create_item(item:Item) -> Item :
#     """
#     Create an item with all the information:

#     - **name**: each item must have a name
#     - **description**: a long description
#     - **price**: required
#     - **tax**: if the item doesn't have tax, you can omit this
#     - **tags**: a set of unique tag strings for this item
#     """
#     return item

#Deprecate a path operation

# @app.get("/items/",tags=["items"])
# async def read_items():
#     return [{"name": "Foo", "price": 42}]

# @app.get("/users/", tags = ["users"])
# async def read_users():
#     return[{"username": "johndoe"}]

# @app.get("/elements/",tags=["items"], deprecated = True)
# async def read_elements():
#     return [{"item_id": "Foo"}]

  

#Using the jsonable_encoder

# fake_db = {}

# class Item(BaseModel):
#     titlle : str
#     timestamp: datetime
#     description : str | None = None

# @app.put("/items/{id}")
# def update_item(id:str, item: Item):
#     json_compatible_item_data = jsonable_encoder(item)
#     fake_db[id] = json_compatible_item_data



# class Item(BaseModel):
#     name: str | None = None 
#     description : str | None = None 
#     price : float | None = None
#     tax : float = 10.5
#     tags : list[str] = []

# items = {
#     "foo": {"name": "Foo", "price": 50.2},
#     "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.1},
#     "baz": {"name": "Baz","description": None, "price": 50.23, "tax": 10.5, "tags": []},

# }
# @app.get("/item/{item_id}", response_model=Item)
# async def read_item(item_id: str):
#     return items[item_id]

# @app.put("/items/{item_id}", response_model=Item)
# async def update_item(item_id: str , item: Item):
#     update_item_encoded = jsonable_encoder(item)
#     items[item_id] = update_item_encoded
#     return update_item_encoded


#Using Pydantics exclude_unset parameter


# class Item (BaseModel):
#     name : str | None = None
#     description : str | None = None 
#     price : float | None = None 
#     tax: float = 10.5
#     tags : list[str] = []

# items = {
#     "foo": {"name": "Foo", "price": 50.2},
#     "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
#     "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
# }
# @app.get("/items/{item_id}",response_model=Item)
# async def read_item(item_id: str):
#     return items[item_id]

# @app.patch("/items/{item_id}")
# async def update_item(item_id: str , item: Item) -> Item:
#     stored_item_data = items[item_id] # gets all  old data
#     stored_item_model = Item(**stored_item_data) # converts to pydantic model
#     update_data = item.model_dump(exclude_unset=True) # update only the one client send 
#     update_item = stored_item_model.model_copy(update=update_data) # copy of an existing data from a model  and update it with  the one client send !
#     items[item_id] = jsonable_encoder(update_item) # encode back Pydantic model into Json - friendly data 
#     return update_item



# async def common_parameters(q:str | None = None , skip : int = 0, limit: int = 100 ):
#     return {"q": q, "skip": skip, "limit": limit}


# @app.get("/items/")
# async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
#     return commons

# @app.get("/users/")
# async def read_users(commons: Annotated[dict, Depends(common_parameters)]):
#     return commons


# fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

# class CommonQueryParams:
#     def __init__(self , q: str | None = None , skip: int = 0, limit: int = 100):
#         self.q = q
#         self.skip = skip
#         self.limit = limit

# @app.get("/items/")
# async def rea_items(commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]):
#     response = {}
#     if commons.q:
#         response.update({"q": commons.q})
#     items = fake_items_db[commons.skip : commons.skip + commons.limit]
#     response.update({"items": items})
#     return response



####Sub Dependencies

# def query_extractor(q:str | None = None ):
#     return q

# def query_or_cookie_extractor(
#         q: Annotated[str, Depends(query_extractor)],
#         last_query: Annotated[str | None , Cookie()] = None,

# ):
#     if not q :
#         return last_query
#     return q

# @app.get("/items/")
# async def read_query(
#     query_or_default : Annotated [str, Depends (query_or_cookie_extractor)],

# ):
#     return {"q_or_cookie": query_or_default}
        


####Dependencies to the path operation decorator 
# async def verify_token(x_token:Annotated[str, Header()]):
#     if x_token  != "fake-super-secret-token":
#         raise  HTTPException(status_code=400, detail="X-Token header invalid")
    
# async def verify_key(x_key:Annotated[str, Header()]):
#     if x_key != "fake-super-secret-key":
#         raise  HTTPException(status_code=400, detail="X-Key header invalid ")
    
#     return x_key

# @app.get("/items/")
# async def read_items():
#     return [{"item": "Portal Gun"} , {"item": "Plumbus"}]

# @app.get("/users/")
# async def read_users():
#     return [{"username": "Rick"}, {"username": "Morty"}]

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl= "token")

# @app.get("/items/")
# async def read_items(token: Annotated [str, Depends(oauth2_scheme)]):
#     return {"token": token}




######Get Current User model

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# class User(BaseModel):
#     username : str
#     email : str | None = None 
#     full_name : str | None = None 
#     disabled : bool | None = None

# def fake_decode_token(token):
#     return User(
#         username= token + "fakedecoded" , email= "john@example.com" , full_name= " John Does"
#     )

# async def get_current_user(token:Annotated[str , Depends(oauth2_scheme)]):
#     user = fake_decode_token(token)
#     return user


# @app.get("/users/me")
# async def read_users_me(current_user: Annotated[User , Depends(get_current_user)]):
#     return current_user



# fake_users_db = {
#     "johndoe": {
#         "username": "johndoe",
#         "full_name": "John Doe",
#         "email": "johndoe@example.com",
#         "hashed_password": "fakehashedsecret",
#         "disabled": False,
#     },
#     "alice": {
#         "username": "alice",
#         "full_name": "Alice Wonderson",
#         "email": "alice@example.com",
#         "hashed_password": "fakehashedsecret2",
#         "disabled": True,
#     },
# }

# app = FastAPI()


# def fake_hash_password(password: str):
#     return "fakehashed" + password


# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# class User(BaseModel):
#     username: str
#     email: str | None = None
#     full_name: str | None = None
#     disabled: bool | None = None


# class UserInDB(User):
#     hashed_password: str


# def get_user(db, username: str):
#     if username in db:
#         user_dict = db[username]
#         return UserInDB(**user_dict)


# def fake_decode_token(token):
#     # This doesn't provide any security at all
#     # Check the next version
#     user = get_user(fake_users_db, token)
#     return user


# async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
#     user = fake_decode_token(token)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Not authenticated",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     return user


# async def get_current_active_user(
#     current_user: Annotated[User, Depends(get_current_user)],
# ):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user


# @app.post("/token")
# async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
#     user_dict = fake_users_db.get(form_data.username)
#     if not user_dict:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")
#     user = UserInDB(**user_dict)
#     hashed_password = fake_hash_password(form_data.password)
#     if not hashed_password == user.hashed_password:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")

#     return {"access_token": user.username, "token_type": "bearer"}


# @app.get("/users/me")
# async def read_users_me(
#     current_user: Annotated[User, Depends(get_current_active_user)],
# ):
#     return current_user




###Cors (Cross - Origiin resource Sharing )

# from fastapi.middleware.cors import CORSMiddleware
# origins = [
#     "http://localhost.tianbgolo.com",
#     "http://localhost.tiangolo.com",
#     "http://localhost",
#     "http://localhost:8080",
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.get("/")
# async def main():
#     return{"message": "Hello World"}



#####SQl Relatial Databases

# from typing import Annotated

# from fastapi import Depends, FastAPI, HTTPException, Query
# from sqlmodel import Field, Session, SQLModel, create_engine, select


# class Hero(SQLModel, table=True):
#     id: int | None = Field(default=None, primary_key=True)
#     name: str = Field(index=True)
#     age: int | None = Field(default=None, index=True)
#     secret_name: str


# sqlite_file_name = "database.db"
# sqlite_url = f"sqlite:///{sqlite_file_name}"

# connect_args = {"check_same_thread": False}
# engine = create_engine(sqlite_url, connect_args=connect_args)


# def create_db_and_tables():
#     SQLModel.metadata.create_all(engine)


# def get_session():
#     with Session(engine) as session:
#         yield session


# SessionDep = Annotated[Session, Depends(get_session)]

# app = FastAPI()


# @app.on_event("startup")
# def on_startup():
#     create_db_and_tables()


# @app.post("/heroes/")
# def create_hero(hero: Hero, session: SessionDep) -> Hero:
#     session.add(hero)
#     session.commit()
#     session.refresh(hero)
#     return hero


# @app.get("/heroes/")
# def read_heroes(
#     session: SessionDep,
#     offset: int = 0,
#     limit: Annotated[int, Query(le=100)] = 100,
# ) -> list[Hero]:
#     heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
#     return heroes


# @app.get("/heroes/{hero_id}")
# def read_hero(hero_id: int, session: SessionDep) -> Hero:
#     hero = session.get(Hero, hero_id)
#     if not hero:
#         raise HTTPException(status_code=404, detail="Hero not found")
#     return hero


# @app.delete("/heroes/{hero_id}")
# def delete_hero(hero_id: int, session: SessionDep):
#     hero = session.get(Hero, hero_id)
#     if not hero:
#         raise HTTPException(status_code=404, detail="Hero not found")
#     session.delete(hero)
#     session.commit()
#     return {"ok": True}


# from typing import Annotated
# from fastapi import Depends, FastAPI, HTTPException, Query
# from sqlmodel import Field, Session, SQLModel, create_engine, select

# class HeroBase(SQLModel):
#     name: str = Field(index=True)
#     age: int | None = Field(default=None, index = True)
    
# class Hero(HeroBase, table = True):
#     id: int | None = Field(default=None, primary_key=True)
#     secret_name: str

# class HeroPublic(HeroBase):
#     id: int

# class HeroCreate(HeroBase):
#     secret_name : str

# class HeroUpdate(HeroBase):
#     name : str | None = None
#     age :  int | None = None 
#     secret_name : str | None = None

# sqlite_file_name = "database.db"
# sqlite_url = f"sqlite:///{sqlite_file_name}"

# connect_args = {"check_same_thread": False}
# engine = create_engine(sqlite_url, connect_args=connect_args)

# def create_db_and_tables():
#     SQLModel.metadata.create_all(engine)

# def get_session():
#     with Session(engine) as session:
#         yield session

# SessionDep = Annotated[Session, Depends(get_session)]

# @app.on_event("startup")
# def on_startup():
#     create_db_and_tables()

# @app.post("/heroes/", response_model=HeroPublic)
# def create_hero(hero: HeroCreate, session: SessionDep):
#     db_hero = Hero.model_validate(hero)
#     session.add(db_hero)
#     session.commit()
#     session.refresh(db_hero)
#     return db_hero

# @app.get("/heroes/",response_model = list[HeroPublic])
# def read_heroes(
#     session: SessionDep,
#     offset : int = 0,
#     limit : Annotated[int,Query(le=100)] = 100,

# ):
#     heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
#     return heroes

# @app.get("/heroes/{hero_id}",response_model=HeroPublic)
# def read_hero(hero_id: int, session: SessionDep):
#     hero = session.get(Hero, hero_id)
#     if not hero:
#         raise HTTPException(status_code=404, detail="Hero not found")
#     return hero

# @app.patch("/heroes/{hero_id}", response_model = HeroPublic)
# def update_hero(hero_id: int , hero: HeroUpdate, session: SessionDep):
#     hero_db = session.get(Hero, hero_id)
#     if not hero_db:
#         raise HTTPException(status_code=404, detail="Hero not found")
    
#     hero_data = hero.model_dump(exclude_unset=True)
#     hero_db.sqlmodel_update(hero_data)
#     session.add(hero_db)
#     session.commit()
#     session.refresh(hero_db)
#     return hero_db

# @app.delete("/heroes/{hero_id}")
# def delete_hero(hero_id: int , session:  SessionDep):
#     hero = session.get(Hero, hero_id)
#     if not hero:
#         raise HTTPException(status_code=404, detail="Hero not found")
#     session.delete(hero)
#     session.commit()
#     return {"ok": True}




from fastapi import FastAPI, Depends
from fastapi.routing import APIRoute

from app.internal import admin
from app.routers import auth, items, tasks , users



description = """
ChimichangApp API helps you do awesome stuff. 🚀

## Items

You can **read items**.

## Users

You will be able to:

* **Create users** (_not implemented_).
* **Read users** (_not implemented_).
"""

app = FastAPI()

app.include_router(users.router)
app.include_router(items.router)
app.include_router(tasks.router)
app.include_router(auth.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    responses={418: {"description": "Internal Use Only"}},
)


@app.get("/")
def read_root():
    return {"message": "Task Manager API is running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}
