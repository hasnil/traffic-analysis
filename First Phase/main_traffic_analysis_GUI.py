
"""Traffic Analysis Project
Author: Lotfi Hasni
Version: 1.1
Since: July 16, 2020
Sources: ENSF 592 Course Documents, City of Calgary Records

This program is used to initiate and direct the Traffic Analysis GUI, which allows for 
a user to write, read, sort, analyze and map a database's traffic data for the City of Calgary.
Related classes are used in obtaining, maniuplating, and presenting this data.
"""

import os
import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk, StringVar, OptionMenu, Grid, filedialog
import read_from_database as rd
import write_to_db as wr
import graph_plotter
import mapper as mp


class MainTrafficAnalysisGUI():
    """ This class represents a Traffic Analysis GUI which
        can report traffic data to a user and serves as the 
        starting point for related classes
    """

    def run(self):
        """ This function is responsible for building
            and running the Traffic Analysis GUI
        """
        # Creates new window
        window = tk.Tk()
        window.title("Traffic Analysis GUI")
        window.geometry("1600x900") # default size

        # Creation of first frame (left)
        frame1 = tk.Frame(master=window, width= 300, relief=tk.SOLID, borderwidth=2, height=100, bg="lavender" )
        frame1.pack(fill=tk.BOTH, side=tk.LEFT)

        # Creation of second frame (right)
        frame2 = tk.Frame(master=window, width=1300)
        frame2.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        # Labels for status bar messages
        label = tk.Label(height = 5, borderwidth= 3, relief= tk.SOLID, master=frame1, text="Status Messages")
        label.pack(side = tk.BOTTOM, fill = tk.X, padx = 3, pady = 2, expand=True)
        label.config(font = ("TkMenuFont", 12))

        label_1 = tk.Label(height = 1, master=frame1, text="Status:", bg = "lavender")
        label_1.pack(side = tk.BOTTOM, fill = tk.X)
        label_1.config(font = ("TkMenuFont", 14))

        # Button for preparing map
        map_button = tk.Button(height = 4, borderwidth= 2, relief= tk.SOLID, master=frame1, text="Map",bg = "mint cream")
        map_button.pack(side = tk.BOTTOM, fill = tk.X, pady = 21, padx = 5, expand=True)
        map_button.config(font = ("TkMenuFont", 12))

        # Button for analyzing maximum incidents and volumes
        analysis_button = tk.Button(height = 4, borderwidth= 2, relief= tk.SOLID, master=frame1, text="Analysis",bg = "mint cream")
        analysis_button.pack(side = tk.BOTTOM, fill = tk.X, pady = 21, padx = 5, expand=True)
        analysis_button.config(font = ("TkMenuFont", 12))

        # Button for sorting of traffic data
        sort_button = tk.Button(height = 4, borderwidth= 2, relief= tk.SOLID, master=frame1, text="Sort",bg = "mint cream")
        sort_button.pack(side = tk.BOTTOM, fill = tk.X, pady = 21, padx = 5, expand=True)
        sort_button.config(font = ("TkMenuFont", 12))

        # Button for reading traffic data from database
        read_button = tk.Button(height = 4, borderwidth= 2, relief= tk.SOLID, master=frame1, text="Read",bg = "mint cream")
        read_button.pack(side = tk.BOTTOM, fill = tk.X, pady = 21, padx = 5, expand=True)
        read_button.config(font = ("TkMenuFont", 12))

        # Label that will be used to communicate messages to user while database is being accessed
        entry_label = tk.Label(height = 5, master=frame2, text= '', font = ("Courier",  12))
        entry_label.pack(side = tk.TOP)

        # Text box to display which files are currently in database
        text_1 = tk.Text(frame2, height = 0, width = 0, font = ("Courier",  12), bg = 'gray94')
        text_1.tag_configure("center", justify='center')
        text_1.insert("1.0","The following files (collections) are currently stored in the traffic databases:\n")
        text_1.tag_add("center","1.0","end")
        text_1.place(relx = 0.5, rely = 0.5, anchor = 'center')

        # Button to allow user to see database files
        greeting_button = tk.Button(height = 10,justify='center', borderwidth= 5, bg = 'light grey', relief= tk.RAISED, master=frame2, text="Welcome!\nClick Here if You Would Like To See Which Traffic Information\nis Currently in the Database or if You Would Like to Add/Delete")
        greeting_button.place(relx = 0.5, rely = 0.5, anchor = 'center')
        greeting_button.config(font = ("Arial", 12))

        # Area for user entry of database type
        enter_here = tk.Entry(frame2, borderwidth = 0, width = 0 , bg = 'gray94')
        enter_here.place(relx = 0.45, rely = 0.15)

        # Area for user entry of database year
        enter_here_2 = tk.Entry(frame2, borderwidth = 0, width = 0 , bg = 'gray94')
        enter_here_2.place(relx = 0.45, rely = 0.18)

        # Used for read more button
        global count 
        count = 26


        def comboclick(event):
            """ Nested function to handle event
                for user clicking an option in
                database type combobox
            """
            if myCombo.get() == "Traffic Accidents":
                database_type = "TrafficAccidents"
                return database_type
            elif myCombo.get() == "Traffic Volume":
                database_type = "TrafficVolume"
                return database_type


        def comboclick_year(event):
            """ Handles event for clicking in
                database year combobox
            """
            if myCombo_2.get() == "2016":
                database_year = "2016"
                return database_year
            elif myCombo_2.get() == "2017":
                database_year = "2017"
                return database_year
            elif myCombo_2.get() == "2018":
                database_year = "2018"
                return database_year


        def handle_click_analysis(event):
            """ Event handler for
                analysis button
            """
            #Updates status bar
            label.config(text="Now analyzing", bg="SteelBlue1")
            analysis_button.configure(bg = "IndianRed1");map_button.configure(bg = "mint cream");read_button.configure(bg = "mint cream");sort_button.configure(bg = "mint cream")

            window.update_idletasks() # Ensures that user knows data is being processed

            
            try:
                # Clears frame from all prior data
                for entries in frame2.winfo_children():
                    entries.destroy()

                # Sees which type the user has selected
                t = comboclick(event)
                
                x_values = ('2016','2017','2018')

                reading_operation = rd.ReadFromDatabase() # Reads from database

                # Obtains maximum for each year from database
                max_volume_or_incidents_2016 = reading_operation.analyze(t,x_values[0])
                max_volume_or_incidents_2017 = reading_operation.analyze(t,x_values[1])
                max_volume_or_incidents_2018 = reading_operation.analyze(t,x_values[2])

                y_values = (max_volume_or_incidents_2016,max_volume_or_incidents_2017,max_volume_or_incidents_2018)

                # Uses graph plotter class to display data
                graph = graph_plotter.GraphPlotter()
                graph.create_graph(frame2,x_values,y_values,t)

                # Updates status bar    
                label.config(text="Successfully analyzed", bg="spring green")

            except:
                label.config(text="Error: Unable to analyze data\nPlease retry",bg="red") # In case of failure


        def handle_click_read_more(event):
            try:
                label.config(text="Now reading \nfrom database", bg="SteelBlue1")
                window.update_idletasks() 

                # The type the user has chosen
                t = comboclick(event)
                # The year the user has chosen
                y = comboclick_year(event)
                
                reading_operation = rd.ReadFromDatabase()

                global count

                # Table read from database
                table_list = reading_operation.recov(count, t, y)

                label.config(text="Successfully read \nfrom database", bg="spring green")

                height = len(table_list) # From reading file
                width = len(table_list[0]) 

                # Creates and populates table of entries with data values
                for i in range(1, height+1):

                    for j in range(width):
                        Grid.columnconfigure(frame2, j, weight = 1)
                        cell = str(table_list[i-1][j])
                        b = ttk.Entry(frame2, justify= 'center')
                        b.insert(0, cell) # Adds text
                        b.grid(row=i,column=j, padx=1,pady=1, sticky="ew")

                count += 25
            except:
                label.config(text="Error encountered: End of document",bg="red")


        def handle_click_read(event):
            """ Reads from database
                and displays rows in GUI
            """

            label.config(text="Now reading \nfrom database", bg="SteelBlue1")
            read_button.configure(bg = "IndianRed1");map_button.configure(bg = "mint cream");analysis_button.configure(bg = "mint cream");sort_button.configure(bg = "mint cream")
            window.update_idletasks() 

            try:
                for entries in frame2.winfo_children():
                    entries.destroy()

                # The type the user has chosen
                t = comboclick(event)
                # The year the user has chosen
                y = comboclick_year(event)
                
                reading_operation = rd.ReadFromDatabase()
                # Table read from database
                table_list = reading_operation.recov(1,t,y)

                label.config(text="Successfully read \nfrom database", bg="spring green")

                height = len(table_list) # From reading file
                width = len(table_list[0]) 

                # Creates and populates table of entries with data values
                for i in range(height):
                    for j in range(width):
                        Grid.columnconfigure(frame2, j, weight = 1)
                        cell = str(table_list[i][j])
                        b = ttk.Entry(frame2, justify= 'center')
                        b.insert(0, cell) # Adds text
                        b.grid(row=i,column=j, padx=1,pady=1, sticky="ew")



                # Button for reading more traffic data from database
                read_more_button = tk.Button(height = 2, borderwidth= 2, relief= tk.SOLID, master=frame2, text="Read More",bg = "IndianRed1")
                read_more_button.place(relx = 0.45, rely = 0.9)
                read_more_button.config(font = ("TkMenuFont", 12))
                read_more_button.bind("<Button-1>", handle_click_read_more)

            
            except:
                label.config(text="Error: Unable to read data\nPlease try again",bg="red")
                

                
        def handle_click_sort(event):
            """ Event handler for sort button.
                Uses ReadFromDatabase.
            """
            label.config(text="Now sorting", bg="SteelBlue1")
            sort_button.configure(bg = "IndianRed1");map_button.configure(bg = "mint cream");analysis_button.configure(bg = "mint cream");read_button.configure(bg = "mint cream")
            window.update_idletasks()
            
            try:
                for entries in frame2.winfo_children():
                    entries.destroy()

                t = comboclick(event)
                y = comboclick_year(event)
                
                reading_operation = rd.ReadFromDatabase() 
                table_list = reading_operation.sort(t,y)

                label.config(text="Successfully sorted", bg="spring green")

                height = len(table_list)
                width = len(table_list[0])

                for i in range(height):

                    for j in range(width):
                        Grid.columnconfigure(frame2, j, weight = 1)
                        
                        cell = str(table_list[i][j])
                    
                        b = ttk.Entry(frame2, justify= 'center')
                        b.insert(0, cell) # Adds text
                        b.grid(row=i,column=j, padx=1,pady=1, sticky="ew")
            except:
                label.config(text="Error: Unable to sort data\nPlease retry",bg="red")


        def handle_click_open_map(event):
            """ Opens html file for map 
                when button is pressed
            """
            t = comboclick(event)
            y = comboclick_year(event)
            os.system(t + y + 'Map.html')


        def handle_click_map(event):
            """ Handles the event when GUI
                user presses map button
            """
            label.config(text="Now preparing map...", bg="SteelBlue1")
            map_button.configure(bg = "IndianRed1");sort_button.configure(bg = "mint cream");analysis_button.configure(bg = "mint cream");read_button.configure(bg = "mint cream")
            window.update_idletasks() 

            try:
                for entries in frame2.winfo_children():
                    entries.destroy()

                t = comboclick(event)
                y = comboclick_year(event)

                # Uses Mapper object to create map file
                mapper = mp.Mapper()
                mapper.draw(t,y)

                # Creates and displays button to open map
                open_map_button = tk.Button(height = 5, width = 25, borderwidth= 7, relief= tk.RAISED, master=frame2, text="Click Here to Open Map",bg = "medium purple")
                open_map_button.pack(side = tk.BOTTOM, expand=True)
                open_map_button.config(font = ("TkMenuFont", 18))
                open_map_button.bind("<Button-1>", handle_click_open_map)

                label.config(text="Map successful\nSee button on right", bg="spring green")

            except:
                label.config(text="Error: Unable to create map\nPlease retry",bg="red")


        def handle_click_add(event):
            """ Handles adding files to database
            """
            # Retrieves user text from entries
            user_database_name = enter_here.get()
            user_collection_name = enter_here_2.get()

            try:
                # Checks if file alrady exists in database
                if user_database_name != "" and user_collection_name != "":
                    writer = wr.WriteToDB()
                    collections = writer.see_collection_status(user_database_name)
                    if user_collection_name in collections:
                        entry_label.config(text = "That file already exists in the database. If you would like to replace it, \nplease delete the existing file first.")
                    else:
                        entry_label.config(text = "Now Adding...")
                        window.filename = filedialog.askopenfilename(initialdir = "/", title = "Select file", filetypes = (("csv files","*.csv"),("all files","*.*")))

                        # Adds file
                        push = wr.WriteToDB()
                        push.write(user_database_name, user_collection_name, window.filename)

                        text = push.see_database_status() # Updates database status
                        text_1.delete(1.0, "end")
                        text_1.tag_configure("center", justify='center')
                        text_1.insert(tk.END,"\n"+ text)
                        text_1.tag_add("center", 1.0, "end")
                        entry_label.config(text = "Added")
            except:
                label.config(text="Error: Unable to add\nPlease retry",bg="red")



        def handle_click_del(event):
            """ Handles adding files to database
            """
            user_database_name = enter_here.get()
            user_collection_name = enter_here_2.get()

            try:
                # Checks if file doesn't exist in database
                if user_database_name != "" and user_collection_name != "":
                    check = wr.WriteToDB()
                    collections = check.see_collection_status(user_database_name)
                    if user_collection_name not in collections:
                        entry_label.config(text = "That file already doesn't exist in the database")
                    else:
                        entry_label.config(text = "Now Deleting...")

                        # Deletes file and updates user
                        deleter = wr.WriteToDB()
                        deleter.delete(user_database_name, user_collection_name)

                        text = deleter.see_database_status()
                        text_1.delete(1.0, "end")
                        text_1.tag_configure("center", justify='center')
                        text_1.insert(tk.END,"\n"+ text)
                        text_1.tag_add("center", 1.0, "end")
                        entry_label.config(text = "Deleted")
            except:
                label.config(text="Error: Unable to delete\nPlease retry",bg="red")
                
            

        def handle_click_greeting(event):
            """ Event handler for greeting button.
                Allows user to see database contents.
            """
            try:
                # Clears button from frame
                greeting_button.destroy()

                writer = wr.WriteToDB()
                text = writer.see_database_status()

                # Makes display space appear
                text_1.config(height = 20, width = 80, bg = 'white')
                text_1.insert(tk.END,"\n"+ text)
            
                # Button for adding files
                a_button = tk.Button(height = 2, width = 25, justify='center', borderwidth= 2, bg = 'light blue', relief= tk.SOLID, master=frame2, text="ADD")
                a_button.place(relx = 0.3, rely= 0.7)
                a_button.config(font = ("Helvetica", 12))
                a_button.bind("<Button-1>", handle_click_add)

                # Button for deleting files
                d_button = tk.Button(height = 2, width = 25, justify='center', borderwidth= 2, bg = 'orange red', relief= tk.SOLID, master=frame2, text="DEL")
                d_button.place(relx = 0.55, rely= 0.7)
                d_button.config(font = ("Helvetica", 12))
                d_button.bind("<Button-1>", handle_click_del)

                # Makes entry spaces appear
                enter_here.config(borderwidth = 3, width = 20, bg = 'white')
                enter_here_2.config(borderwidth = 3, width = 20, bg = 'white')

                entry_label.config(text = "Please type the database (e.g. TrafficAccidents or TrafficVolume) you would like to access. \nBelow that type the file name (year) you would like to deal with and press the 'add' or 'delete' button.")

            except:
                for entries in frame2.winfo_children():
                    entries.destroy()
                label.config(text="Error: Something went wrong.\nDatabase connection may not be possible",bg="red")


        # Changes size for all combobox dropdown options
        larger_font = tkFont.Font(family="TkMenuFont",size=18)
        window.option_add("*TCombobox*Listbox*Font", larger_font)

        # Creation of year combobox
        myCombo_2 = ttk.Combobox(master = frame1, justify='center', value = ["Year","2016", "2017","2018"], font = ("TkMenuFont", 18))
        myCombo_2.current(0)
        myCombo_2.bind("<<ComboboxSelected>>", comboclick_year) #runs comboclick function
        myCombo_2.pack(side = tk.BOTTOM, fill = tk.X, pady = 21, padx = 5, expand=True)

        # Creation of type combobox
        myCombo = ttk.Combobox(master = frame1, justify = 'center', value =["Type", "Traffic Accidents", "Traffic Volume"], font = ("TkMenuFont", 18))
        myCombo.current(0)
        myCombo.bind("<<ComboboxSelected>>", comboclick) #runs comboclick function
        myCombo.pack(side = tk.BOTTOM, fill = tk.X, pady = 21, padx = 5, expand=True)

        # Binds GUI buttons to actions
        read_button.bind("<Button-1>", handle_click_read)
        sort_button.bind("<Button-1>", handle_click_sort)
        analysis_button.bind("<Button-1>", handle_click_analysis)
        map_button.bind("<Button-1>", handle_click_map)
        greeting_button.bind("<Button-1>", handle_click_greeting)

        # Keeps GUI running until exited manually
        window.mainloop()

    
def main():
    """ Main execution point
    """
    my_GUI = MainTrafficAnalysisGUI()
    my_GUI.run()


if __name__ == '__main__':
    main()