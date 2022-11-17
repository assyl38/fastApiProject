from datetime import datetime, timedelta

from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware

from Backend import otp_generator, mail
from Backend.jwttoken import create_access_token
from fastapi import FastAPI, HTTPException, Depends, status, Response
from fastapi.security import OAuth2PasswordRequestForm

from Backend.database import (
    fetch_one_client,
    fetch_all_client,
    create_client,
    update_client,
    remove_client, database, collection_name, collection,
)
from Backend.hashing import Hash
from Backend.model import Kmeans, User
from Backend.modelclassifier import decision_maker
from Backend.settings import password

app = FastAPI()



origins = ['http://localhost:3000',]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials= True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return {"Ping"}

@app.get("/apii/kmeans")
async def get_todo():
    response = await fetch_all_client()
    return response

@app.get("/api/kmeans/{CLIENT_AGE}", response_model=Kmeans)
async def get_todo_by_title(CLIENT_AGE):
    response = await fetch_one_client(CLIENT_AGE)
    if response:
        return response
    raise HTTPException(404, f"There is no todo with the age {CLIENT_AGE}")

@app.post("/api/kmeans/", response_model=Kmeans)
async def post_todo(todo: Kmeans):
    response = await create_client(todo.dict())
    if response:
        return response
    raise HTTPException(400, "Something went wrong")

@app.put("/api/kmeans/{CLIENT_ENCOURS_ENGAGEMENT}/", response_model=Kmeans)
async def put_todo(CLIENT_ENCOURS_ENGAGEMENT:float, CLIENT_MMM:float,CLIENT_VRD_MOY:float):
    response = await update_client(CLIENT_ENCOURS_ENGAGEMENT, CLIENT_MMM,CLIENT_VRD_MOY)
    if response:
        return response
    raise HTTPException(404, f"There is no todo with the engagement {CLIENT_ENCOURS_ENGAGEMENT}")

@app.delete("/api/kmeans/{CLIENT_ENCOURS_ENGAGEMENT}")
async def delete_todo(CLIENT_ENCOURS_ENGAGEMENT):
    response = await remove_client(CLIENT_ENCOURS_ENGAGEMENT)
    if response:
        return "Successfully deleted todo"
    raise HTTPException(404, f"There is no todo with the title {CLIENT_ENCOURS_ENGAGEMENT}")


# Segment clients
@app.post('/predict')
async def predict(kmeans: Kmeans = Depends()):
    return {'segment': decision_maker(kmeans).tolist()}



@app.post('/register')
async def create_user(request:User):
   hashed_pass = Hash.bcrypt(request.password)
   user_object = dict(request)
   user_object["password"] = hashed_pass
   user_id = collection_name.insert_one(user_object)
   email = request.email
   try:
       mail_details = await collection_name.find_one({"email": email})
       if mail_details == None:
           details = {
               "email": email,
               "password": password,
               "otp": 0,
               "verified": False
           }
           details: User =User(**details)
           details = jsonable_encoder(details)
           await database.user_collection.insert_one(details)
           return ("successfully registered")
       else:
           return ("email already existed")
   except Exception as e:
       return (str(e))


async def raiseHTTPException(status_code):
    pass


@app.post('/login')
async def login(request:OAuth2PasswordRequestForm = Depends()):
    user =collection_name.find_one({"username":request.username})
    if not user:
       raiseHTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if not Hash.verify(user["password"],request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    access_token = create_access_token(data={"sub": user["username"] })
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/generate_otp")
async def generate_otp(data: dict):
    email = data['email']
    try:
        mail_details = collection_name.find_one({"email": email})
        if mail_details:
            otp = otp_generator.otp_generator()
            msg = mail.send_mail(email, otp[0])
            updated_student =  collection_name.update_one({"email": email}, {"$set": {"otp": int(otp[1]), "verified": False}})
        if updated_student:

            return ("otp generated")
        return False
    except Exception as e:
        return (str(e))

@app.post("/verify_otp")
async def verify_otp(data: dict):
    otp = data["otp"]
    email = data["email"]
    try:
        mail_details = collection_name.find_one({"email": email})
        if int(otp) == mail_details["otp"]:
            collection_name.update_one(
                {"email": email}, {"$set": {"verified": True}}
            )
            return ("otp verified successfully")
        else:
            collection_name.update_one(
                {"email": email}, {"$set": {"verified": False}}
            )
            return ("wrong otp entered")
    except Exception as e:
        return (str(e))

@app.post("/change_password")
async def change_password(data: dict):
    email = data["email"]
    new_password = data["new_password"]
    try:
        mail_details = collection_name.find_one({"email": email})
        if mail_details:
            if mail_details["verified"] == True:
                collection_name.update_one(
                    {"email": email}, {"$set": {"password": new_password}}
                )
                collection_name.update_one(
                    {"email": email}, {"$set": {"verified": False}}
                )
                return ("password changed successfully")
            else:
                return ("otp is not verified for this mail")
        else:
            return ("invalid mail")
    except Exception as e:
        return (str(e))



