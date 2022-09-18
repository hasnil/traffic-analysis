
"""Traffic Analysis Project
Author: Lotfi Hasni
Version: 1.1
Since: July 16, 2020
"""
from decouple import config
import pymongo # Uses MongoDB for database
from pymongo import MongoClient


class ReadFromDatabase():
    """ Performs reading and sorting 
        of traffic data from MongoDB 
    """
    def __init__(self):
        # Database connection
        username = config('MONGO_USERNAME', default = '')
        password = config('MONGO_PASSWORD', default = '')
        self.client = MongoClient("mongodb+srv://" + username + ":" + password + "@cluster0.dte5n.mongodb.net/?retryWrites=true&w=majority")
        self.db = self.client.admin


    def sort(self, database_type, database_year, top_num = 25):
        """ This function returns the database entries sorted
            in descending order for volume or incidents. Use 
            top_num = 'all' if you would like to return all entries
        """
        # Points to collection location
        self.db = self.client[database_type]
        self.collection = self.db[database_year]

        if database_type == "TrafficVolume":
            # Checks how 'volume' term is reported in documents
            if self.collection.find_one({'volume': { '$exists': True}}):
                term = 'volume'
            elif self.collection.find_one({'Volume': { '$exists': True}}):
                term = 'Volume'
            elif self.collection.find_one({'VOLUME': { '$exists': True}}):
                term = 'VOLUME'

            # Sorted database documents by volume
            cursor_object = self.collection.find().sort(term, pymongo.DESCENDING)
            each_row_list = list(cursor_object)

            header_list = list(each_row_list[0].keys())
            del header_list[0]

            # Removes id column
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
                return final_list[:top_num+1]


        elif database_type == "TrafficAccidents":

            # Traffic accidents are sorted by most common location so they will have different incidents. Samples are used instead
            header_list = ['Sample Incident Info', 'Sample Description','Sample START_DT','Sample MODIFIED_DT','Sample Quadrant','Longitude','Latitude','Location','Number of Incidents']

            # Cursor object used to find the most common locations in the collection and the corresponding count
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
                del database_list[i][location_index:]
                
                # Location and count are added to the end of each sample data row
                database_list[i].extend(each_row_list[i])

            final_list = []
            final_list.append(header_list)
            # Header and data together
            final_list.extend(database_list)

        return final_list



    def recov(self, start_id, database_type, database_year, full_database = False):
        """ This function is used to retrieve volume or incidents data rows from database in the
            order they are stored. A list of each row list is returned. Returns header
            and 25 rows if full_database parameter is False.
        """

        self.db = self.client[database_type]
        self.collection = self.db[database_year]

        # Cursor object used as reference to obtaian results of query
        cursor_object = self.collection.find({})
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
        
        if(full_database == False):
            if start_id == 1:
                final_list = final_list[:26] #Gets constant number, chosen as 25
            else:
                if len(final_list) - start_id >= 25:
                    final_list = final_list[start_id: start_id + 25]
                else:
                    final_list = final_list[-25:]

        return final_list



    def analyze(self, database_type, database_year):
        """ Computes max volume or max number of incidents
            for year
        """
        # Uses sort function
        analysis_list = self.sort(database_type, database_year)

        # Takes corresponding column for max
        if database_type == "TrafficVolume" and database_year == "2018":
            max_volume_or_accidents = analysis_list[1][-2]
        else:    
            max_volume_or_accidents = analysis_list[1][-1]

        return max_volume_or_accidents



if __name__ == '__main__':
    # Used for testing
    test = ReadFromDatabase()
    row_list = test.sort("TrafficVolume", "2018")
    print(row_list)