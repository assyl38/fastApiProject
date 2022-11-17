from pymongo import MongoClient
#Mongo driver
import motor.motor_asyncio

from Backend.model import Kmeans

client= motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')

database = client.PFE
collection = database.clients
mongodb_uri = 'mongodb://localhost:27017'
client = MongoClient(mongodb_uri)
database = client.PFE
collection_name = database.user


async def fetch_one_client(CLIENT_AGE):
    document = await collection.find_one({"CLIENT_AGE":CLIENT_AGE})
    return document

async def fetch_all_client():
    kmeans = []
    cursor = collection.find({})
    async for document in cursor:
        kmeans.append(Kmeans(**document))
    return kmeans

async def create_client(kmeans):
    document = kmeans
    result = await collection.insert_one(document)
    return document


async def update_client(CLIENT_ENCOURS_ENGAGEMENT, CLIENT_MMM,CLIENT_VRD_MOY):
    await collection.update_one({"CLIENT_ENCOURS_ENGAGEMENT": CLIENT_ENCOURS_ENGAGEMENT}, {"$set": {"CLIENT_MMM": CLIENT_MMM}}, {"$set": {"CLIENT_VRD_MOY": CLIENT_VRD_MOY}})
    document = await collection.find_one({"CLIENT_ENCOURS_ENGAGEMENT": CLIENT_ENCOURS_ENGAGEMENT})
    return document

async def remove_client(CLIENT_ENCOURS_ENGAGEMENT):
    await collection.delete_one({"CLIENT_ENCOURS_ENGAGEMENT": CLIENT_ENCOURS_ENGAGEMENT})
    return True