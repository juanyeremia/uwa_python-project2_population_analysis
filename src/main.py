
# STEP 1: DATA PREPARATION
# 1.1. Read and extract data
def read_csv(csvfile):
    try:
        with open(csvfile,'r') as file:
            csv_data = []
            for line in file:
                line = line.lower().strip().split(',') # Each row becomes a list
                csv_data.append(line)
            
            return csv_data
    except FileNotFoundError:
        print(f"File '{csvfile}' not found.")
        return []
    except PermissionError:
        print(f"No permission to read '{csvfile}'")
        return []
    except Exception as e:
         print(f"Unexpected error while reading '{csvfile}': {e}")
         return []
        
# Output: [[row_1],[row_2],[row_3],...]

# 1.2. Cleanup data
# 1.2.1 Removing duplicates
# Get list of duplicates in a CSV file for cross referencing
def find_dup(list): # 'list' = result of read_csv()
    dup = []
    for i in range(len(list)-1): # len() - 1 because otherwise will get out of bounds error due to the if check of i+1
        if list[i][0] == list[i+1][0]:
            dup.append(list[i][0])
    
    # No need to check last row because it will not be a duplicate
    return dup

# Check a data list with another file's duplicate list
def cleanup(csvdata,duplicates): # 'duplicates' = combined list of duplicates in file 1 and 2
    cleaned_data = []
    for row in csvdata:
       if row[0] not in duplicates:
           cleaned_data.append(row)
    
    return cleaned_data

# ----------------------------------------------------------------------

# This is the main function
def main(csvfile_1,csvfile_2):
# Get csv data and sort
    csv1_data = read_csv(csvfile_1)
    csv1_header = csv1_data[0]
    csv1_data = csv1_data[1:]
    csv1_data.sort(key=lambda x:x[0])
    
    csv2_data = read_csv(csvfile_2)
    csv2_header = csv2_data[0]
    csv2_data = csv2_data[1:]
    csv2_data.sort(key=lambda x:x[0])
    
# Cleanup csv data
# Remove duplicates
    # Find duplicates
    dup1 = find_dup(csv1_data)
    dup2 = find_dup(csv2_data)
    all_dups = list(set(dup1 + dup2))
    
    # Remove duplicates
    cleaned_csv1 = cleanup(csv1_data,all_dups)
    cleaned_csv2 = cleanup(csv2_data,all_dups)
    
    
    
    
    