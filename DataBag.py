#! /usr/bin/env python
# -*- encoding: utf-8 -*-
import pickle
import time
import os

class Data():

    id = ""
    data = {}

    def __init__(self, id, data={}, oldData=[]):
        self.id = id
        self.data = data
        self.oldData = list(oldData)

    def setData(self, data):
        self.oldData.append({time.time():self.data})
        self.data = data

    def getData(self):
        return {"id": self.id,
                "data": self.data,
                "oldData": self.oldData}

    def loadData(self, data):
        self.id = data["id"]
        self.data = data["data"]
        self.oldData = list(data["oldData"])

class DataBag():

    bag = []

    def __init__(self):
        self.bag = []

    def addData(self, data):
        self.bag.append(data)

    def setData(self, id, data):
        for elem in self.bag:
            if (id == elem.id):
                elem.setData(data)
                return elem
        newdata = Data(id, data)
        self.bag.append(newdata)
        return newdata

    def deleteData(self, data):
        for elem in self.bag:
            if (data.id == elem.id):
                self.bag.remove(data)

    def getData(self, id):
        for data in self.bag:
            if (id == data.id):
                return data
        return None

    def serialize(self, filename="data.db"):
        try:
            dictInfo = []
            if (os.path.exists(filename)):
                os.remove(filename)
            for data in self.bag:
                dictInfo.append(data.getData())
            with open(filename, "wb") as f:
                f.write(pickle.dumps(dictInfo))
        except Exception as err:
            print err

    def deserialize(self, filename="data.db"):
        try:
            dictInfo = []
            with open(filename, "rb") as f:
                dictInfo = pickle.load(f)
            for data in dictInfo:
                if (self.getData(data["id"])):
                    self.getData(data["id"]).loadData(data)
                else:
                    self.bag.append(Data(data["id"], data["data"], data["oldData"]))
        except:
            pass
