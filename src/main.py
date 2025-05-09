
# Step 1: Data extraction and cleaning
# 1.1. Extract data from csv file into a list
def read_csv(csvfile):
    with open(filename,'r') as file:
        csv_data = []
        for line in file:
            line = line.lower().strip().split(',')
            csv_data.append(line)
        
        return csv_data

# 1.2. Data cleaning
# 1.2.1 Remove duplicates
# Get list of duplicates in a CSV file for cross referencing


# ----------------------------------------------------------------------

# This is the main function
def main(csvfile_1,csvfile_2):
    # Get csv data, sort, and clean
    csv1_data = read_csv(csvfile_1)
    csv1_header = csv1_data[0]
    csv1_data = cev1_data[1:]
    csv1_data.sort(key=lambda x:x[0])
    
    csv2_data = read_csv(csvfile_2)
    csv2_header = csv2_data[0]
    csv2_data = cev2_data[1:]
    csv2_data.sort(key=lambda x:x[0])