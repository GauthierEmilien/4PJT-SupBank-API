from pymongo import MongoClient
from pymongo.results import InsertOneResult, InsertManyResult, DeleteResult
from pymongo.cursor import Cursor
from typing import List


class DB:

    def __init__(self, database_name: str):
        self.__client = MongoClient()
        self.__db = self.__client[database_name]

    def insert(self, collection: str, element: dict) -> InsertOneResult:
        return self.__db[collection].insert_one(element)

    def insert_many(self, collection: str, elements: List[dict]) -> InsertManyResult:
        return self.__db[collection].insert_many(elements)

    def get_all(self, collection: str, filter: dict = None) -> Cursor:
        filter_dict = {} if filter is None else filter
        return self.__db[collection].find(filter_dict)

    def get_one(self, collection: str, filter: dict):
        return self.__db[collection].find_one(filter)

    def delete_all(self, collection: str) -> DeleteResult:
        return self.__db[collection].delete_many({})
