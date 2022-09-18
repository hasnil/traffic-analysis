
"""Traffic Analysis Project
Author: Lotfi Hasni
Version: 1.1
Since: July 16, 2020
"""
import folium
from shapely.geometry import MultiLineString
import read_from_database as rd
from folium import plugins
from folium.plugins import HeatMap


class Mapper():
    """ This class performs various 
        mapping functions for traffic data.
    """
    def __init__(self):
        """ Constructor method for object creation
        """
        self.reader = rd.ReadFromDatabase()
        self.map_object = folium.Map(location = (51.0443, -114.0631), zoom_start= 12) #Centered on Calgary Tower
        self.message = 'Click Here to Learn More'

    def process_multi_line_string(self, multi_line_string):
        """ Takes string multi_line_string
            and returns list of latitude - longitude tuples
        """
        first_stage = multi_line_string.replace("MULTILINESTRING ((", "").replace("))","").replace(",","").replace("(","").replace(")","")
        second_stage = first_stage.split(" ")

        latitudes = []
        longitudes = []

        for i in range(len(second_stage)):
            # Even entries are longitudes in given files
            if i % 2 ==0:
                longitudes.append(second_stage[i])
            if i % 2 != 0:
                latitudes.append(second_stage[i])

        for i in range(len(latitudes)):
            latitudes[i] = float(latitudes[i])

        for i in range(len(longitudes)):
            longitudes[i] = float(longitudes[i])

        coords = list(zip(latitudes,longitudes))

        return coords


    def draw_polylines(self, segment_name,length_m,volume,coords):
        """ This function is used to draw 
            polylines the map html
        """
        # Information to be displayed when one hovers over segment
        tool_tip_text = "segment_name: " + segment_name + " length_m: " + str(length_m) + " volume: " + str(volume)
        my_polyline = folium.PolyLine(locations = coords, weight=6, tooltip= tool_tip_text)
        self.map_object.add_child(my_polyline)

    

    def draw_incident_heat_map(self, year):
        """ This function draws a heat map representation
            of traffic incident frequency on the map
        """

        # Info is taken from database and manipulated to be list of latitude - longitude lists
        database_list = self.reader.recov(1, 'TrafficAccidents', year, True)

        # Find location column index
        if "location" in database_list[0]:
            location_index = database_list[0].index("location")

        if "Location" in database_list[0]:
            location_index = database_list[0].index("Location")

        if "LOCATION" in database_list[0]:
            location_index = database_list[0].index("LOCATION")

        list_of_lat_long_strings = []

        for i in range(1, len(database_list)):
            list_of_lat_long_strings.append(database_list[i][location_index])


        list_of_coord_lists = [""]*len(list_of_lat_long_strings)

        for i in range(len(list_of_lat_long_strings)):

            list_of_coord_lists[i] = list_of_lat_long_strings[i].replace(",","").replace("(","").replace(")","").split(" ")
            list_of_coord_lists[i][0] = float(list_of_coord_lists[i][0])
            list_of_coord_lists[i][1] = float(list_of_coord_lists[i][1])

        # HeatMap plugin is used on map
        HeatMap(list_of_coord_lists, max_opacity= 0.9).add_to(self.map_object)

        

    def draw_top_markers(self, type,year,segment_index, length_m_index, volume_index, the_geom_index):
        """ Draws top marker for type and year chosen
        """
        if type == "TrafficVolume":
            database_list = self.reader.sort('TrafficVolume', year)
            top_volume = database_list[1][volume_index]
            top_segment = database_list[1][segment_index]
            top_length = database_list[1][length_m_index]
            top_coords = self.process_multi_line_string(database_list[1][the_geom_index])

            # Create marker for max volume
            text_volume = '<p style="text-align:center;"><b>Maximum Traffic Volume Location ' + year + '</b></p>'+\
                "segment_name: " + top_segment + "\nlength_m: " + str(top_length) + "\nvolume: " + str(top_volume)
            folium.Marker(top_coords[int(len(top_coords)/2)], popup = folium.Popup(text_volume),\
                icon=folium.Icon(icon='road', color = 'green'), tooltip = self.message).add_to(self.map_object)

        elif type == "TrafficAccidents":
            database_list = self.reader.sort('TrafficAccidents', year)
            top_location = tuple(float(x) for x in database_list[1][-2].strip("()").split(","))
            top_number_incidents = database_list[1][-1]

            # Create marker for max traffic accidents
            text_accidents = '<p style="text-align:center;"><b>Maximum Incidents Location ' + year + '</b></p>'+\
                "Location:" + "(" + str(top_location[0]) + "," + str(top_location[1]) + ")" + "\nNumber of Incidents: " + str(top_number_incidents)
            folium.Marker((top_location[0],top_location[1]), popup = folium.Popup(text_accidents),\
                icon=folium.Icon(icon='flash', color = 'red'), tooltip = self.message).add_to(self.map_object)
            # Draws heatmap for incident locations
            self.draw_incident_heat_map(year)


    def obtain_data(self, type, year, full_database = True):
        """ Uses other functions to direct
            map creation
        """
        # Series of if-else statements to determine header indexes
        if full_database == True: 
            database_list = self.reader.recov(1, 'TrafficVolume', year, True)
        else:
            database_list = self.reader.sort('TrafficVolume', year)
        
        if "segment_name" in database_list[0]:
            segment_index = database_list[0].index("segment_name")

        if "secname" in database_list[0]:
            segment_index = database_list[0].index("secname")

        if "SECNAME" in database_list[0]:
            segment_index = database_list[0].index("SECNAME")

        if "the_geom" in database_list[0]:
            the_geom_index = database_list[0].index("the_geom")

        if "multilinestring" in database_list[0]:
            the_geom_index = database_list[0].index("multilinestring")

        if "length_m" in database_list[0]:
            length_m_index = database_list[0].index("length_m")

        if "shape_leng" in database_list[0]:
            length_m_index = database_list[0].index("shape_leng")

        if "Shape_Leng" in database_list[0]:
            length_m_index = database_list[0].index("Shape_Leng")
        
        if "volume" in database_list[0]:
            volume_index = database_list[0].index("volume")

        if "VOLUME" in database_list[0]:
            volume_index = database_list[0].index("VOLUME")
        
        for i in database_list[1:]:
            segment_name = i[segment_index]
            length_m = i[length_m_index]
            volume = i[volume_index]
            coords = self.process_multi_line_string(i[the_geom_index])
            self.draw_polylines(segment_name,length_m,volume,coords)
        
        self.draw_top_markers(type, year, segment_index, length_m_index, volume_index, the_geom_index)



    def draw(self, type, year, full_database = True):
        """ Initiates creation of
            map
        """
        self.obtain_data(type, year, full_database)   

        # Makes and saves html file to make map
        self.map_object.save(type + year + 'Map.html')


if __name__ == '__main__':
    test = Mapper()
    test.draw("TrafficAccidents","2017")
