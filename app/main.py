from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import  engine
from routers import post, user, auth, vote

#-----------------------------
# we comment it as "ALEMBIC" do this job for us :-)
#models.Base.metadata.create_all(bind=engine)

#-----------------------------
app = FastAPI()


'''
Cross Origin Resource Sharing (CROS) alows you 
to make requests from a web browser on one domain 
to a server different domain. for example:
ebay.com  ===> blocked by CORS <===== google.com

go to web pag

>> inspect
>> console

type:
fetch('http://localhost:8000/').then(res => res.json()).then(console.log)
'''
 
# private domain
#origins = [
#    "https://www.google.com",
#    "http://localhost.tiangolo.com",
#    "https://localhost.tiangolo.com",
#    "http://localhost",
#    "http://localhost:8080",
#]

# public domain
origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#-----------------------------
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

#-----------------------------
@app.get("/")
def root():
    return {"message" : "Hello world  Javad Vahedi!"}
