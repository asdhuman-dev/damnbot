from dotenv import dotenv_values

config = dotenv_values(".env")

def getenv(name: str):
    try:
        return config[name]
    except:
        return None
