import csv

class csv_data:


    def __init__(self, csv_file):
        
        with open(csv_file, "r") as item:
            reader = csv.DictReader(item)
            self.column_names = reader.fieldnames

        self.csv_file = csv_file
        self.keep_file_updated()

    def keep_file_updated(self):
        
        with open(self.csv_file, "r") as item:
            product = list(csv.DictReader(item))
    
        self.__all_data = product
        return self.__all_data

    @property
    def all_data(self):
        self.keep_file_updated()
        return self.__all_data


    @all_data.setter
    def all_data(self, value):
        self.__all_data = value

   
    def save_item_to_file(self, new_data_dict):

        with open(self.csv_file, "a", newline='') as planet:
            writer = csv.DictWriter(planet, fieldnames=self.column_names)
            writer.writerow(new_data_dict)

        return self.all_data

    def write_to_file(self, data_rows):

        with open(self.csv_file, "w", newline='') as item:
            writer = csv.DictWriter(item, fieldnames=self.column_names)
            writer.writeheader()
            writer.writerows(data_rows)

        self.keep_file_updated()
        return self.all_data

    def remove_a_row(self, row_for_deletion):
        
        self.all_data.remove(row_for_deletion)
        self.write_to_file(self.__all_data)
        
        self.keep_file_updated()

        return self.all_data
