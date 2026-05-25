from pydantic import BaseModel , ConfigDict , Field 


class CategoryCreate(BaseModel):
    name : str  = Field (min_length=1, max_length=50)

class CategoryUpdate(BaseModel):
    name : str | None = Field (default= None , min_length= 1, max_length= 50)


class CategoryResponse(BaseModel):
    id: int 
    name : str

    user_id : int 

    model_config = ConfigDict (from_attributes=True)