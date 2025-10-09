import os, time, json, requests
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(), override=False) #For loading the .env file and accessing any sensitive info like API keys

"""
Return a NASA_API_KEY. If you have a valid .env key in your file, then you will return that key.
Otherwise, yo uwill return NASA's default "DEMO_KEY" to still use methods.
"""
def getNASA_APIKey():
    key = os.getenv("NASA_API_KEY")
    
    if (key):
        return key
    else:
        return "DEMO_KEY"

def getDate():

    return ""