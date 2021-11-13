from pymongo import MongoClient
class recipe():
    def __init__(self) -> None:
        self.name = ""
        self.ingredients=[]
        self.steps=[]
    def setRecipe(self,name,igd,steps):
        self.name = name
        self.ingredients=igd
        self.steps=steps
    
    def printRecipe(self):
        for i,j in self.ingredients:
            print(i,j)
        for i,j in self.steps:
            print(i)
            for idg,qty in j:
                print(idg,qty)
class rec_db():
    
    def __init__(self) -> None:        
        client = MongoClient("mongodb+srv://codemonk:database12qw@cluster0.jsshi.mongodb.net")
        db=client['myFirstDatabase']
        self.coll=db['recipies']
    def print_all(self):
        cursor = self.coll.find({})
        cursor=list(cursor)
        print(cursor)
    def check_exists(self,name):
        '''Returns whether the recipie exists or not.'''
        res = self.coll.count_documents({"name":name})
        return res != 0
    def ingredients(self, name):
        '''Returns a list of all the ingredients needed for the recipie as well as total time.'''
        if self.coll.count_documents({"name":name}):
            res = self.coll.find({"name":name})[0]
            return [res['ingredients'],res['total_time']]
        else:
            return None
    def steps(self, name):
        '''Returns a list of all the ingredients needed for the recipie.'''
        if self.coll.count_documents({"name":name}):
            res = self.coll.find({"name":name})[0]
            return res['steps']
        else:
            return None

