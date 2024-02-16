import os
from dotenv import load_dotenv
from pyrogram import Client

load_dotenv()

api_id = os.getenv('api_id')
api_hash = os.getenv('api_hash')

client = Client('me_client', api_id, api_hash)

client.run()
