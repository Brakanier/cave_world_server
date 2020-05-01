from starlette.config import Config

config = Config(".env")
# REDIRECT_URL = config("REDIRECT_URL")

APP_ID=config("APP_ID")
APP_SECRET=config("APP_SECRET")
APP_SERVICE_TOKEN=config("APP_SERVICE_TOKEN")

# CLIENT_URL = config("CLIENT_URL")
# SERVER_URL = config("SERVER_URL")


DB_URL = config("DB_URL")


# STORAGE_PATH = config('STORAGE_PATH')