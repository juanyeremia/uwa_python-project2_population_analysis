
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
        
# Output: [[row_2],[row_3],[row_4],...]

# 1.2. Header mapping
# Get a dictionary of the headers as key, and their index values as the value
def map_headers(header_row): # 'header_row' = ['State Name', 'SA2 Code', ...]
    header_index = {}
    try:
        for i in range(len(header_row)):
            key = header_row[i].strip().lower() # Header rows can have mixed upper/lower cases
            header_index[key] = i
        return header_index
    except Exception as e:
        print(f"Unexpected error in map_headers: {e}")
        return {}

# 1.3. Cleanup data
# 1.3.1 Removing duplicates
# Get list of duplicates in a CSV file for cross referencing
def find_dup(csvdata,sa2_index): # 'list' = result of read_csv()
    dup = []
    try:
        for i in range(len(csvdata)-1): # len() - 1 because otherwise will get out of bounds error due to the if check of i+1
            if csvdata[i][sa2_index] == csvdata[i+1][sa2_index]:
                dup.append(csvdata[i][sa2_index])
        
        # No need to check last row because it will not be a duplicate
        return dup
    except IndexError:
        print(f"IndexError in find_dup: Skipping malfromed row.")
        return []
    except Exception as e:
        print(f"Unexpected error in find_dup: {e}")
        return []
    
# Check a data list with another file's duplicate list
def cleanup(csvdata,duplicates,sa2_index): # 'duplicates' = combined list of duplicates in file 1 and 2
    cleaned_data = []
    try:
        for row in csvdata:
           if row[sa2_index] not in duplicates:
               cleaned_data.append(row)
        
        return cleaned_data
    except Exception as e:
        print(f"Unexpected error in cleanup: {e}")
        return []

# 1.3.2 Remove invalid data
def find_invalid(dupclean_csv2,sa2_index): # input: [[row_2],[row_3],[row_4],...]
    invalid_sa2 = []
    try:
        for row in dupclean_csv2:
            sa2_code = row[sa2_index]
            for value in row[2:]:
                try:
                    val = int(value) # Attempt conversion. If successful, move on to the next.
                    if val < 0:
                        invalid_sa2.append(sa2_code) # If value is Int, check if negative.
                        break   # Break loop because only need to find one invalid.
                except:
                    invalid_sa2.append(sa2_code) # If conversion failed, add to list
                    break   # Break loop because only need to find one invalid.
        return invalid_sa2
    except Exception as e:
        print(f"Unexpected error in find_invalid: {e}")
        return []
       
def remove_invalid(dupclean_csv2,invalid_sa2,sa2_index):
    cleaned_data = []
    try:
        for row in dupclean_csv2:
            if row[sa2_index] not in invalid_sa2: # Check if SA2 code is present in 
                cleaned_data.append(row)
        return cleaned_data
    except Exception as e:
        print(f"Unexpected error in remove_invalid: {e}")
        return []

    
# ----------------------------------------------------------------------

# This is the main function
def main(csvfile_1,csvfile_2):
# Step 1. Data preparation
    # 1.1 Read files
    csv1_data = read_csv(csvfile_1)
    csv2_data = read_csv(csvfile_2)
    
    if not csv1_data or not csv2_data:
        return {},{},{}
    
    # Separate headers from data
    csv1_header = csv1_data[0]
    csv1_data = csv1_data[1:]
    
    csv2_header = csv2_data[0]
    csv2_data = csv2_data[1:]
    
    # 1.2 Header mapping
    header_map1 = map_headers(csv1_header)
    header_map2 = map_headers(csv2_header)
    
    # SA2 code index from each dictionary
    sa2_index_1 = header_map1.get('sa2 code')
    sa2_index_2 = header_map2.get('sa2 code')
    
    # Error handling for sa2 mapping
    if sa2_index_1 is None or sa2_index_2 is None:
        print("Error: 'sa2 code' column not found in one or both files.")
        return {},{},{}
    
    # 1.3 Cleanup data
    # Sort each data for cleanup purposes
    csv1_data.sort(key=lambda x:x[sa2_index_1])
    csv2_data.sort(key=lambda x:x[sa2_index_2])
    
    # 1.3.1Remove duplicates
    # Find duplicates
    dup1 = find_dup(csv1_data,sa2_index_1)
    dup2 = find_dup(csv2_data,sa2_index_2)
    all_dups = list(set(dup1 + dup2))
    
    # Remove duplicates
    final_csv1 = cleanup(csv1_data,all_dups,sa2_index_1)
    cleaned_csv2 = cleanup(csv2_data,all_dups,sa2_index_2)
    
    # 1.3.2 Remove invalid
    invalid_sa2 = find_invalid(cleaned_csv2,sa2_index_1)
    final_csv2 = remove_invalid(cleaned_csv2,invalid_sa2,sa2_index_1)
    
    