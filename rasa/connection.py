import pprint
from pymongo import MongoClient
class recipe():
    def __init__(self) -> None:
        self.ingredients=[]
        self.steps=[]
    def setRecipe(self,igd,steps):
        self.ingredients=igd
        self.steps=steps
    def printRecipe(self):
        for i,j in self.ingredients:
            print(i,j)
        for i,j in self.steps:
            print(i)
            for idg,qty in j:
                print(idg,qty)
pp = pprint.PrettyPrinter(width=100, compact=True)
client = MongoClient()
client = MongoClient(${{secret.MONGO_DB_URL}})
dbs=client.list_database_names()
db=client['myFirstDatabase']
colls=db.list_collection_names()
coll=db['recipies']
cursor = coll.find({})
cursor=list(cursor)
#
pp.pprint(cursor[1])

