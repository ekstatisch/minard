import pandas as pd
import sqlite3

class CreateMinardDB:
    def __init__(self):
        # read data
        with open("data/minard.txt") as f:
            lines = f.readlines()
        column_names = lines[2].split()
        # data clean
        patterns_to_be_replaces = {"(", ")", "$", ","}
        adjusted_column_names = []
        for column_name in column_names:
            for pattern in patterns_to_be_replaces:
                if pattern in column_name:
                    column_name = column_name.replace(pattern, "")
            adjusted_column_names.append(column_name)

        # data classification
        self.column_names_city = adjusted_column_names[:3]
        self.column_names_temp = adjusted_column_names[3:7]
        self.column_names_troop = adjusted_column_names[7:]
        self.lines = lines

    def create_city_dataframe(self):
        # create city data
        longitudes, latitudes, cities = [], [], []
        i = 6
        while i <= 25:
            long, lat, city = self.lines[i].split()[:3]
            longitudes.append(float(long))
            latitudes.append(float(lat))
            cities.append(city)
            i += 1

        city_data = (longitudes, latitudes, cities)
        #print(city_data)

        city_df = pd.DataFrame()
        for column_name, data in zip(self.column_names_city, city_data):
            city_df[column_name] = data
        return city_df
    
    def create_temperature_dataframe(self):
        #create temperature data
        longitudes, temperature, days, dates = [],[],[],[]
        i = 6
        while i <= 14:
            lines_split = self.lines[i].split()
            longitudes.append(float(lines_split[3]))
            temperature.append(float(lines_split[4]))
            days.append(int(lines_split[5]))
            if(i == 10):
                dates.append("Nov 24")
            else:
                dates.append(lines_split[6]+" "+lines_split[7])
            i += 1
        temperatre_data = (longitudes, temperature, days, dates)

        temperature_df = pd.DataFrame()
        for column_name, data in zip(self.column_names_temp, temperatre_data):
            temperature_df[column_name] = data
        return temperature_df
    
    def create_troop_dataframe(self):
        # create troop data
        longitudes, latitudes, survivals, directions, divisions = [], [], [], [], []
        i = 6
        while i <= 53:
            lines_split = self.lines[i].split()
            divisions.append(int(lines_split[-1]))
            directions.append(lines_split[-2])
            survivals.append(int(lines_split[-3]))
            latitudes.append(float(lines_split[-4]))
            longitudes.append(float(lines_split[-5]))
            i += 1 
        troop_data = (longitudes, latitudes, survivals, directions, divisions)

        troop_df = pd.DataFrame()
        for column_name, data in zip(self.column_names_troop, troop_data):
            troop_df[column_name] = data
        return troop_df

    def create_database(self):
        connection = sqlite3.connect("data/minard.db")
        city_df = self.create_city_dataframe()
        temp_df = self.create_temperature_dataframe()
        troop_df = self.create_troop_dataframe()
        df_dict = {
            "cities" : city_df,
            "temperature" : temp_df,
            "troops" : troop_df
        }
        for k,v in df_dict.items():
            v.to_sql(name=k, con=connection,index=False, if_exists="replace")
        connection.close()

create_minard_db = CreateMinardDB()
create_minard_db.create_database()