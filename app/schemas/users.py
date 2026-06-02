from datetime import datetime
import string

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


# data neded to register user
class UserCreate(BaseModel):
    username: str = Field(
        min_length=3,  #username filds should at least needs to contain 3 characters  long 
        max_length=50, # userename fileds should at max needs to contain 50 characters long 
        pattern=r"^[A-Za-z0-9_]+$" # username field  should need  follow Upper & lower  case  letters and number 
        
        )
    @field_validator("username",mode="before") # This validation process happens before actual pydantic validation like when username = "  dada  " it  checks and removes spaces and after validation  whether it is string or not !
    @classmethod
    def clean_username(cls,value : str) -> str:
        if isinstance(value,str):
            return value.strip()
        return value
    
    email: EmailStr   # This Emailstr validation type  that check whether  email field input follows  a standard format 
    
    password : str = Field (
        min_length=8,  # Password Field needs to contain at least 8 chars long  
        max_length=128 # Password Field  needs to contain at max 128 chars long 
    )
    @field_validator("password")
    @classmethod
    def validate_passwords(cls, passwords : str) -> str:

        special_chars = string.punctuation  ## this is being used  to validate  special chars 
        if " " in passwords :  ## Condition check  for empty spaces 
            raise ValueError("Password can not  contain spaces ")
        
        if not any(char.isalpha() for char in passwords):  ## Condition check for  letters sonly chars 
            raise ValueError("Password cannot contain only letters")
        
        if not any(char.isdigit() for char in passwords):## Condition check for at least    one digits   
            raise ValueError("Password must contain at least one number")
        
        if not any(char.isupper() for char in passwords): ## Condition check for at least one Upper case  letters 
            raise ValueError ("Password must contain one Uppercase letter!")
        
        if not any(char.islower()  for char in passwords): ##Condition check for at least one  Lower case letter 
            raise ValueError("Password must contain  one Lowercased letter!")
        
        if not any(char in special_chars for char in passwords): ## Condition check wheather password contains at least one special characters 
            raise ValueError("Password must contain at least one special characters!")
        

        
        return passwords


# safe data returnned to client 
class UserResponse(BaseModel):
    id : int 
    username: str
    email : EmailStr
    timezone: str

    model_config = ConfigDict(from_attributes=True)    



# Data needed to login
class UserLogin(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=1)

