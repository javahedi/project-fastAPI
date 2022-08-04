from hashlib import algorithms_available
from pydantic import BaseSettings


class Settings(BaseSettings):
    database_hostname : str
    database_port : str
    database_password : str
    database_name : str
    database_username : str
    secret_key : str
    algorithm : str
    access_token_expire_minutes : int

    class Config:
        env_file = ".env"


settings = Settings()


# to access Path
#import os
#print(os.getenv("Path"))

# in Terminal
# >> export MY_DB_URL="localhost:5432"
# >> printenv
# >> echo $MY_DB_URL