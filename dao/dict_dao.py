import pickle
from abc import ABC, abstractmethod

class DictDAO(ABC):
    @abstractmethod
    def __init__(self, datasource=''):
        self.__datasource = datasource
        self.__cache = {} 
        try:
            self.__load()
        except FileNotFoundError:
            self.__dump()

    def __dump(self):
        pickle.dump(self.__cache, open(self.__datasource, 'wb'))

    def __load(self):
        self.__cache = pickle.load(open(self.__datasource, 'rb'))

    def add(self, key, obj):
        self.__cache[key] = obj
        self.__dump() 

    def update(self, key, obj):
        try:
            if self.__cache[key] is not None:
                self.__cache[key] = obj
                self.__dump()
        except:
            pass

    def change_key(self, old_key, new_key):
        self.__cache[new_key] = self.__cache.pop(old_key)
        self.__dump()

    def get(self, key):
        return self.__cache[key]

    def remove(self, key):
        self.__cache.pop(key)
        self.__dump() 

    def get_all(self):
        return self.__cache.values()
    
