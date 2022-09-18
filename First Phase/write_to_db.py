
"""Traffic Analysis Project
Author: Lotfi Hasni
Version: 1.1
Since: July 16, 2020
"""
from pymongo import MongoClient
import pandas as pd
import geojson
from decouple import config
import csv


class WriteToDB():
    """ This class allows a user to import 
        data from (csv) files to a MongoDB database
    """

    def __init__(self):
        # Points to MongoDB database, authenticates with username and password
        username = config('MONGO_USERNAME', default = '')
        password = config('MONGO_PASSWORD', default = '')
        self.client = MongoClient("mongodb+srv://" + username + ":" + password + "@cluster0.dte5n.mongodb.net/?retryWrites=true&w=majority")
        self.db = self.client.admin


    def see_database_status(self):
        """ Returns a string listing documents 
            in database
        """
        text_return = ""

        for i in self.client.list_database_names():
            if i != "admin":
                if i != "local":
                    text_return += "\nIn " + i + ": \n"
                    self.db = self.client[i]
                    for doc_group in sorted(self.db.list_collection_names(), reverse=True):
                        text_return = text_return + doc_group + "\n"
        
        return text_return

    
    def see_collection_status(self, type):
        """ Returns a string listing documents 
            in collection
        """
        text_return = ""
        for i in self.client[type].list_collection_names():
            text_return = text_return + i + "\n"
        
        return text_return

        
    def delete(self, type, year):
        """ Used to delete document
            from database
        """
    
        self.db = self.client[type]
        self.collection = self.db[year]
        self.collection.drop()
              

    def write(self, type, year,  filename):
        """ Used to import files to MongoDB
        """
 
        if filename[-7:] == "geojson":
            with open(filename) as f:
                file_data = geojson.load(f)
            db = self.client[type]
            collection = db[year]
            collection.insert_one(file_data)

        # Reads csv file into pandas dataframe
        if filename[-3:] == "csv":
            df = pd.read_csv(filename,  encoding = "utf8")

            # Looks for filename from path
            if '/' in filename:
                start_point = filename.rindex('/')
                shortened_filename = filename[start_point+1:]
            elif '\\' in filename:
                start_point = filename.rindex('\\')
                shortened_filename = filename[start_point+1:]
            else:    
                shortened_filename = filename[-100:]
                

            # Special processing: Only grabs Traffic_Incidents.csv information for 2018
            if shortened_filename == "Traffic_Incidents.csv" or filename == "Traffic_Incidents.csv" and year == "2018":
                df = df[~df.START_DT.str.contains("/2016 ")]
                df = df[~df.START_DT.str.contains("/2017 ")]
                df = df[~df.START_DT.str.contains("/2019 ")]
                df = df[~df.START_DT.str.contains("/2020 ")]

            # Special processing: Only grabs Traffic_Volumes_for_2018.csv information for 2018
            if shortened_filename == "Traffic_Volumes_for_2018.csv" or filename == "Traffic_Volumes_for_2018.csv" and year == "2018":
                df = df[df.YEAR != 2017] # Excludes potentially erroneous 2017 entry from given file

            # Special processing: Only grabs Traffic_Incidents_Archive_2017.csv information for 2017
            if shortened_filename == "Traffic_Incidents_Archive_2017.csv" or filename == "Traffic_Incidents_Archive_2017.csv" and year == "2017":
                df = df[~df.START_DT.str.contains("/2018 ")] # Excludes potentially erroneous 2018 entries from given file


            # Writes pandas dataframe into database
            self.db = self.client[type]
            self.collection = self.db[year]
            self.collection.insert_many(df.to_dict('records'))

   

if __name__ == '__main__':
                                    
    wr = WriteToDB()
    print(wr.see_database_status())
 