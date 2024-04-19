import pickle
from abc import ABC, abstractmethod


class DAO(ABC):
    @abstractmethod
    def __init__(self, datasource=""):
        self.__datasource = datasource
        self.__cache = (
            {}
        )  # é aqui que vai ficar a lista que estava no controlador. Nesse exemplo estamos usando um dicionario
        try:
            self.__load()
        except FileNotFoundError:
            self.__dump()

    def __dump(self):
        # print("DUMPOU DAO")
        pickle.dump(self.__cache, open(self.__datasource, "wb"))

    def __load(self):
        # print("CARREGOU DAO")
        self.__cache = pickle.load(open(self.__datasource, "rb"))
        # printa todos os elementos do cache
        # for key, value in self.__cache.items():
        #    print(f"chave - {key}, valor -{value}")

    # esse método precisa chamar o self.__dump()
    def add(self, key, obj):
        self.__cache[key] = obj
        # print(f"Adicionou {obj} com chave {key}")
        self.__dump()  # atualiza o arquivo depois de add novo amigo
        # print("ADICIONOU DAO")

    # cuidado: esse update só funciona se o objeto com essa chave já existe
    def update(self, key, obj):
        try:
            if self.__cache[key] is not None:
                self.__cache[key] = obj  # atualiza a entrada
                self.__dump()  # atualiza o arquivo
                # print("ATUALIZOU DAO")
        except KeyError as e:
            print(e)
            return

    def get(self, key):
        try:
            # print("GETOU DAO")
            return self.__cache[key]
        except KeyError as e:
            print(e)
            return

    # esse método precisa chamar o self.__dump()
    def remove(self, key):
        try:
            self.__cache.pop(key)
            self.__dump()
            # print("REMOVEU DAO")  # atualiza o arquivo depois de remover um objeto
        except KeyError as e:
            print(e)
            return

    def get_all(self):
        self.__load()  # Garante que os dados mais recentes sejam carregados do arquivo
        return self.__cache.values()
