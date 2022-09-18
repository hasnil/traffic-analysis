
"""Traffic Analysis Project
Author: Lotfi Hasni
Version: 1.1
Since: July 16, 2020
"""

from decouple import config
import pymongo # Uses MongoDB for database
from pymongo import MongoClient

class ReadDict():
    """ Performs reading from database
    """
    def __init__(self):
        username = config('MONGO_USERNAME', default = '')
        password = config('MONGO_PASSWORD', default = '')
        self.client = MongoClient("mongodb+srv://" + username + ":" + password + "@cluster0.dte5n.mongodb.net/?retryWrites=true&w=majority")
        self.db = self.client.admin


    def sort(self, database_type, database_year, top_num = 25):
        """ This function returns the database entries sorted
            in descending order. Use top_num = 'all' if you 
            would like to return all entries
        """
        # Points to database
        self.db = self.client[database_type]
        self.collection = self.db[database_year]

        if database_type == "TrafficVolume":

            if database_year == "2018":
                term = 'VOLUME'
            else: 
                term = 'volume'

            # Sorted database documents
            cursor_object = self.collection.find().sort(term, pymongo.DESCENDING)
            each_row_list = list(cursor_object)

            header_list = list(each_row_list[0].keys())
            del header_list[0]

            for i in range(len(each_row_list)):
                each_row_list[i] = list(each_row_list[i].values())
                del each_row_list[i][0]

            final_list = []
            final_list.append(header_list)

            for i in range(len(each_row_list)):
                final_list.append(each_row_list[i])

            if top_num == "all":
                return final_list
            else:
                # Returns list of lists, with each list being the next row
                return final_list[:top_num]


        elif database_type == "TrafficAccidents":

            header_list = ['Sample Incident Info', 'Sample Description','Sample START_DT','Sample MODIFIED_DT','Sample Quadrant','Longitude','Latitude','Location','Number of Incidents']

            cursor_object = self.collection.aggregate([
                {   #Gets the count for each 'location'
                    "$group": {"_id": "$location","count": {"$sum": pymongo.ASCENDING}}},
                {"$sort": {"count": pymongo.DESCENDING}}])

            each_row_list = list(cursor_object)

            for i in range(len(each_row_list)):
                each_row_list[i] = list(each_row_list[i].values())

            if top_num != "all":
                # List of most common accident locations with count
                each_row_list = each_row_list[:top_num]
                
            database_list = []

            # Retrieves another database list of lists to match locations with sample entries(faster than find_one)
            cursor_object_2 = self.collection.find({})
            each_row_list_2 = list(cursor_object_2)

            # Index of location is found
            sample_header_list = list(each_row_list_2[0].keys())
            del sample_header_list[0]
            location_index = sample_header_list.index("location")
            
            # Extraneous id column removed
            for i in range(len(each_row_list_2)):
                each_row_list_2[i] = list(each_row_list_2[i].values())
                del each_row_list_2[i][0]

            # Finds a row that matches location for each location
            for i in range(len(each_row_list)):
                searched = each_row_list[i][0] # The location being searched for
                for j in range(len(each_row_list_2)):
                    if each_row_list_2[j][location_index] == searched:
                        database_list.append(each_row_list_2[j])
                        break

            # Modifies database values to match header
            for i in range(len(database_list)):
                if database_year == "2018":
                    del database_list[i][-3:]
                else:
                    del database_list[i][-2:]
                # Location and count are added to the end of each sample data row
                database_list[i].extend(each_row_list[i])

            final_list = []
            final_list.append(header_list)
            # Header and data together
            final_list.extend(database_list)

        return final_list
    



if __name__ == '__main__':
    
    test = ReadDict()
    row_list = test.sort("TrafficAccidents","2018",'all')
    print(row_list[:5])
    