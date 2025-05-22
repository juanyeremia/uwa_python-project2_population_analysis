# Name: Juan Yeremia Yovian
# Student ID: 24911605

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
            # Normalize column 'age 80 anda over' to age 80-None
            if key[:3] == 'age' and "and over" in key:
                key = key.replace(" and over","-None")
            header_index[key] = i
        return header_index
    except Exception as e:
        print(f"Unexpected error in map_headers: {e}")
        return {}
    
# 1.2.1. Get SA2 code index, because each file has different SA2 code heaeder name
def detect_sa2_index(header,data):
    first_row_data = data[0]
    try:
        for i in range(len(first_row_data)):
            value = first_row_data[i] 
            if value.isdigit() and len(value) == 9: # Check valus is all digits and length of characters is 9
                return i
    except Exception as e:
        print(f"Error detecting SA2 code column: {e}")

    print("Warning: SA2 code column not found.")
    return None

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

# STEP 2: OP1
'''
Plan:
1. Create make_agedict() function containing age groups as keys and empty lists as values.
2. Create functions for each OP1 output.
3. At the start of each function, call make_dict().
4. Each function will fill up the dictionary generated from make_dict().
'''

# 2.1. Make a dictionary for each level
def area_dict(csv1_data,header_map1,code_key,name_key):
    # code_key =  's_t code' or 'sa3 code' or 'sa2 code'
    # name_key = 's_t name' or 'sa3 name' or 'sa2 name'
    area_dictionary = {}

    # Check whether code_key or name_key exists in header_map1 dictionary
    if code_key not in header_map1 or name_key not in header_map1:
        print(f"Error: '{code_key}' or '{name_key}' not found in header map.")
        return area_dictionary # Returns empty dictionary

    for row in csv1_data:
        try:
            code = row[header_map1[code_key]] 
            name = row[header_map1[name_key]] 
            area_dictionary[code] = name
        except IndexError:
            print("Warning: Skipping a row due to missing columns.")
            
    return area_dictionary

# 2.2. Make age-group dictionary
'''
NOTE: Contents of 'header_map2' may be in different order
header_map2 = {
    'area_code_level':0,
    'area_name_level2':1,
    'age 0-9':2,
    'age 10-19':3,
    'age 20-29':4,
    ...
}

'''

def make_agedict(csv2_header):
    keys = []
    keys_dict = {}

    # Extract age group columns
    for key in csv2_header:
        if key[:3].lower() == 'age': # Check if the header contains the word 'age'
            key = key.strip().lower()
            if "and over" in key:
                key = key.replace(" and over","-None")
            keys.append(key)
    # Sort the age group list in order of age
    try:   
        keys.sort(key=lambda x:int(x.replace("age ","").split('-')[0])) # sorting by last number
    except Exception as e:
        print(f"Error sorting age group headers: {e}")
        return keys_dict # Returns empty list
        
    # Generate the default dictionary
    for item in keys:
        keys_dict.setdefault(item,{})

    return keys_dict

# 2.3. Get population count
def get_pop_count(csv2_header,csv2_data,header_map2,area_level_dict,sa2_index,level):
    agedict = make_agedict(csv2_header)
    
    # Create a reverse 'area_dict' for sorting later in the function
    name_to_code = {}
    for code in area_level_dict:
        name = area_level_dict[code]
        name_to_code[name] = code

    for row in csv2_data:
        # 1. Get sa2 code
        sa2_code = row[sa2_index]
        
        # 2. Get area code based on level
        if level == "state":
            area_code = sa2_code[:1]
        elif level == "sa3":
            area_code = sa2_code[:5]
        else: # sa2
            area_code = sa2_code
        
        # 3. Map area name from area code
        area_name = area_level_dict.get(area_code) 
        if not area_name:
            continue # Skip if area not found
        
        # 4. Get population data
        for age_group in agedict:
            try:
                pop = int(row[header_map2[age_group]])
                agedict[age_group].setdefault(area_name,0)
                agedict[age_group][area_name] += pop
            except:
                continue # Skip invalid values
    
    # Dictionary sorting by area code
    for age_group in agedict:
        agedict[age_group] = dict(sorted(agedict[age_group].items(),key=lambda x: name_to_code.get(x[0],'')))

    return agedict

def op1(csv2_header,final_csv2,header_map2,sa2_index_2,state_dict,sa3_dict,sa2_dict):
# 1. Get populatin count dictionaries
    state_pop = get_pop_count(csv2_header,final_csv2,header_map2,state_dict,sa2_index_2,'state')
    sa3_pop = get_pop_count(csv2_header,final_csv2,header_map2,sa3_dict,sa2_index_2,'sa3')
    sa2_pop = get_pop_count(csv2_header,final_csv2,header_map2,sa2_dict,sa2_index_2,'sa2')
    
# 2. Build result
    op1_result = {} 
    for age_group in state_pop:
        try:
            if (not state_pop[age_group] or not sa3_pop.get(age_group) or 
                not sa3_pop[age_group] or not sa2_pop.get(age_group) or
                not sa2_pop[age_group]):
                continue
            
            label = age_group.replace("age ","") # Gets rid of 'age ' in the age_group header
            largest_state = sorted(state_pop[age_group],key=state_pop[age_group].get)[-1]
            largest_sa3 = sorted(sa3_pop[age_group],key=sa3_pop[age_group].get)[-1]
            largest_sa2 = sorted(sa2_pop[age_group],key=sa2_pop[age_group].get)[-1]
            
            op1_result[label] = [largest_state,largest_sa3,largest_sa2]
        
        except Exception as e:
            print(f"Error processing age group '{age_group}': '{e}'")
            continue
    
    return op1_result,sa3_pop,sa2_pop # 'sa3_pop' and 'sa2_pop' for op2()

# ----------------------------------------------------------------------
# STEP 3 - OP2
# 3.1 Sum total of populations across all age groups for each area level
def sum_all_pop(area_pop):
    total_pop = {}
    for age_group in area_pop:
        try:
            for area_name,pop in area_pop[age_group].items():
                try:
                    total_pop.setdefault(area_name,0)
                    total_pop[area_name] += pop
                except ValueError:
                    print(f"Invalid population value for '{area_name}' in '{age_group}': {pop}")
                    continue
        except Exception as e:
            print(f"Skipping age group '{age_group}' due to error: {e}")
            continue

    return total_pop

# 3.2 Finding SA3 with populations over 150,000
def sa3_over_150k(sum_population,area_dict):
    sa3_data = {}
    
    for area_name,total_pop in sum_population.items():
        try:
            if int(total_pop) > 150000:
                found = False
                for code,name in area_dict.items():
                    if name == area_name:            # If found sa3 > 150,000 and in area_dict
                        sa3_data[code] = {'population':total_pop,'sa3_name':name}
                        found = True
                        break
                if not found:
                    print(f"Warning: SA3 name '{area_name}' not found in area_dict.")
        except ValueError:
            print(f"Invalid population value for '{area_name}': {total_pop}")
            continue
        except Exception as e:
            print(f"Error processing SA3 '{area_name}': {e}")
            continue
            
    # Convert sa3_name to sa3_code
    return sa3_data

# 3.3 Finding largest SA2 code and population count per SA3 above 150,000
def largest_sa2_per_sa3(sum_pop,sa2_dict):
    grouped = {} # {sa3_code: {sa2_code:population}}
    sorted_grouped = {} # {sa3_code:[largest_sa2_code,its_pop]}

    for sa2_name,total_pop in sum_pop.items():
        try:
            total_pop = int(total_pop) # Make sure it's nto a valid number
            found = False 
            for sa2_code,name in sa2_dict.items():
                if name == sa2_name:
                    sa3_code = sa2_code[:5]
                    grouped.setdefault(sa3_code,{})
                    grouped[sa3_code][sa2_code] = total_pop
                    found = True
                    break
            if not found:
                print(f"Warning: SA2 name '{sa2_name}' not found in sa2_dict.")
        except ValueError:
            print(f"Invalid population value for SA2 '{sa2_name}': {total_pop}.")
            continue
        except Exception as e:
            print(f"Error grouping SA2 '{sa2_name}': {e}")
            continue
    
    for sa3_code,sa2_data in grouped.items():
        try:
            if not sa2_data:
                print(f"Wraning: No SA2 data under SA3 code '{sa3_code}'.")
                continue
            # Sort SA2s by population descending
            sorted_sa2s = sorted(sa2_data.items(),key=lambda x: x[1])
            largest_sa2_code,largest_pop = sorted_sa2s[-1]
            sorted_grouped[sa3_code] = [largest_sa2_code,largest_pop]
        except Exception as e:
            print(f"Error selecting largest SA2 in SA3 '{sa3_code}': {e}")
            continue

    return sorted_grouped

# 3.4 Calculate standard deviation across all age group for a given SA2
def std_dev(sa2_code,sa2_pop,sa2_dict):
    try:
        # Get current sa2_name from sa2_dict based on current sa2_code
        sa2_name = sa2_dict.get(sa2_code)
        if not sa2_name :           # If sa2_name not found, return 0.0 std dev
            return 0.0 
    
        curr_sa2_pop = []
        for age_group in sa2_pop:
            try:
                pop = sa2_pop[age_group].get(sa2_name)
                if pop is not None:
                    curr_sa2_pop.append(int(pop)) 
            except ValueError:
                print(f"Invalid population value for '{sa2_name}' in '{age_group}': {pop}")
                continue
    
        if not curr_sa2_pop or len(curr_sa2_pop) < 2:  # If curr_sa2_pop empty or only one age group has value, return 0.0 std dev
            print(f"Warning: No population values found for SA2 '{sa2_name}'.")
            return 0.0
        
        # std dev calculation
        mean = sum(curr_sa2_pop)/len(curr_sa2_pop)
        variance = 0
        for pop in curr_sa2_pop:
            variance += (pop - mean) ** 2 
        std = (variance/(len(curr_sa2_pop)-1)) ** 0.5
        
        return round(std,4)
    
    except Exception as e:
        print(f"Unexpected error in std_dev for SA2 code '{sa2_code}': {e}")
        return 0.0

def op2(sa3_pop, sa2_pop, sa3_dict, sa2_dict):
    final_output = {}  # {state_code: {sa3_code: [sa2_code, pop, std]}}
    
    try:
        # Get total population for SA3 and SA2
        sa3_total = sum_all_pop(sa3_pop)
        sa2_total = sum_all_pop(sa2_pop)
      
        # Find SA3 over 150,000 and get largest SA2 code and population  
        sa3_over_150k_dict = sa3_over_150k(sa3_total, sa3_dict)
        largest_sa2s = largest_sa2_per_sa3(sa2_total,sa2_dict)      
        
        # Generate the states keys in the dict
        for sa3_code in sa3_dict:
            state_code = sa3_code[0]
            final_output.setdefault(state_code,{})
        
        # Build output by combining `largest_sa2s' with 'std_dev'
        for sa3_code in sa3_over_150k_dict:
            try:
                state_code = sa3_code[0]
                if sa3_code not in largest_sa2s:
                    print(f"Warning: SA3 code '{sa3_code}' missing in largest_sa2s.")
                    continue
                
                sa2_code, pop = largest_sa2s[sa3_code]
                std = std_dev(sa2_code, sa2_pop,sa2_dict)

                final_output[state_code][sa3_code] = [sa2_code, pop, std]
            
            except Exception as e:
                print(f"Error processing SA3 code '{sa3_code}': {e}")
                continue
    
    except Exception as e:
        print(f"Unexpected error in OP2: {e}")    

    return final_output,sa3_total,sa2_total

# ----------------------------------------------------------------------
'''
STEP 4 - OP3
4.1. Get dictionary of SA3s with 15 or more SA2s
4.2. Get Cosine similarity
    4.2.1. Build SA2 population lists per age group
    4.2.2. Calculate Cosine similarity
4.3. Final OP3
'''

# 4.1. Get dictionary of SA3s with 15 or more SA2s
def get_sa3_15_sa2s(sa2_dict,sa3_dict):
    sa2_per_sa3 = {} # {'adelaide city':['adelaide','north adelaide','adelaide hills']}
    sa3_15_sa2s = {}

    # Get dictionary of SA3 with their SA2s as a list 
    for sa3_code,sa3_name in sa3_dict.items():
        for sa2_code,sa2_name in sa2_dict.items():
            # Check if SA2 is part of SA3
            if sa2_code[:5] == sa3_code:
                sa2_per_sa3.setdefault(sa3_name,[])
                sa2_per_sa3[sa3_name].append(sa2_name)
    
    # Get SA3s with 15 or more SA2s
    for sa3_name in sa2_per_sa3:
        if len(sa2_per_sa3[sa3_name]) >= 15:
            sa3_15_sa2s.setdefault(sa3_name,[])
            sa3_15_sa2s[sa3_name] = sa2_per_sa3[sa3_name]
    
    return sa3_15_sa2s

# 4.2. Cosine Similarity
# 4.2.1. Build SA2 population lists per age group
def build_sa2_vectors(sa3_15_sa2s,sa2_pop):
    age_groups = list(sa2_pop.keys()) # ['0-9','10-19',...]
    sa2_vectors = {} # Build SA2 population list -> {'landsdale': [pop0_9,pop10_19,...],'carramar':[pop0_9,pop10_19,...],...}
    
    for sa3_name in sa3_15_sa2s:
        sa2_list = sa3_15_sa2s[sa3_name] # Get lists of SA2s in this SA3

        # For each SA2 in the list:
        for sa2 in sa2_list:
            if sa2 not in sa2_vectors: # Avoid re-processing the same SA2
                vector = []
                
                # Build the population vector for current SA2 across all age group
                for age in age_groups:
                    try:
                        pop = sa2_pop[age][sa2] # Get pop data for that age groupd
                    except KeyError:
                        # Either age group or SA2 is missing froom data
                        pop = 0
                    vector.append(pop)
                
                if any(vector):
                    sa2_vectors[sa2] = vector # Store the vector for this SA2    
                
    return sa2_vectors

# 4.2.2. Calculate Cosine similarity
def cosine_similarity(v1, v2):
    if not v1 or not v2:
        print("Warning: One or both vectors are empty.")
        return 0.0
    
    if len(v1) != len(v2):
        print("Warning: Vectors have different lengths.")

    dot = 0      # Dot product of the two vectors
    mag1 = 0     # Magnitude of vector 1
    mag2 = 0     # Magnitude of vector 2
    
    # Loop through all elements in the vectors
    for i in range(len(v1)):
        a = v1[i]
        b = v2[i]
        dot += a * b      # Sum of products
        mag1 += a * a     # Sum of squares for vector 1
        mag2 += b * b     # Sum of squares for vector 2
        
    # If either vector has mag 0 , similarity is undefined. Return 0  
    try:    
        return dot / ((mag1 ** 0.5) * (mag2 ** 0.5))
    except ZeroDivisionError:
        return 0.0

# 4.3. Final OP3
def op3(sa3_15_sa2s,sa2_vectors):
    op3_result = {} # Final result: { sa3_name: [sa2_1, sa2_2, similarity] }
    
    # Loop through each SA3
    for sa3_name, sa2_list in sa3_15_sa2s.items():
        if len(sa2_list) < 2:
            print(f"Warning: Not enough SA2s to compare in SA3: '{sa3_name}'.")
            continue

        best_score = -1       # Current highest similarity score
        best_pair = ('', '')  # Best matching SA2 pair
        
        # Compare each unique pair of SA2s
        for i in range(len(sa2_list)):
            for j in range(i + 1, len(sa2_list)):
                sa2a = sa2_list[i]
                sa2b = sa2_list[j]

                vec1 = sa2_vectors.get(sa2a, []) # Get age vector for SA2 A
                vec2 = sa2_vectors.get(sa2b, []) # Get age vector for SA2 B
                
                if vec1 is None or vec2 is None:
                    print(f"Warning: Missing vector for SA2 pair '{sa2a}','{sa2b}'.")
                    continue
    
                score = cosine_similarity(vec1, vec2) # Calculate similarity
                
                # Update if this pair is more similar than previous best pair
                if score > best_score:
                    best_score = score
                    best_pair = (sa2a, sa2b)
        
        # Store the best pair and similarity score (rounded) for this SA3
        if best_pair[0] and best_pair[1]:
            sorted_pair = sorted(best_pair)
            op3_result[sa3_name] = [sorted_pair[0], sorted_pair[1], round(best_score, 4)]
        else:
            print(f"Warning: No valid SA2 pair found for SA3 '{sa3_name}'.")
    
    return op3_result

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
    sa2_index_1 = detect_sa2_index(csv1_header,csv1_data)
    sa2_index_2 = detect_sa2_index(csv2_header,csv2_data)
    
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
    
# ---------------------------

    # Generate area dictionaries for references
    state_dict = area_dict(final_csv1,header_map1,'s_t code','s_t name')
    sa3_dict = area_dict(final_csv1,header_map1,'sa3 code','sa3 name')
    sa2_dict = area_dict(final_csv1,header_map1,'sa2 code','sa2 name')
    
    # OP1
    OP1_result, sa3_pop, sa2_pop = op1(csv2_header, final_csv2, header_map2, sa2_index_2, state_dict, sa3_dict, sa2_dict)
    #op() result is broken down because 'sa3_pop' and 'sa2_pop' are needed for op2

    # OP2
    OP2_result,sa3_total,sa2_total = op2(sa3_pop, sa2_pop, sa3_dict, sa2_dict)
    
    # OP3
    sa3_15_sa2s = get_sa3_15_sa2s(sa2_dict,sa3_dict)
    sa2_vectors = build_sa2_vectors(sa3_15_sa2s,sa2_pop)
    
    # Filter out SA2s with 0 population values
    for sa3_name in list(sa3_15_sa2s.keys()):
        filtered_sa3_15_sa2s = []
        for sa2 in sa3_15_sa2s[sa3_name]:
            if sa2 in sa2_vectors:
                filtered_sa3_15_sa2s.append(sa2)

        if len(filtered_sa3_15_sa2s) >= 2:
            sa3_15_sa2s[sa3_name] = filtered_sa3_15_sa2s
        else:
            del sa3_15_sa2s[sa3_name]  # Remove SA3 completely
    
    OP3_result = op3(sa3_15_sa2s,sa2_vectors)
    
    return OP1_result,OP2_result,OP3_result
    
"""

Debugging Documentation:

Issue 1 – Data Preparation (2024-05-11)
- Error Description:
  The code initially assumed that both input files had a column labeled exactly as 'sa2 code', but in reality, the column names and positions varied.
- Erroneous Code Snippet:
  sa2_index_1 = header_map1['sa2 code']
  sa2_index_2 = header_map2['sa2 code']
- Test Case:
  One CSV file used 'SA2 Code', while the other had the SA2 code column with a different label.
- Reflection:
  I removed the hardcoded assumption and wrote detect_sa2_index() to scan each row for a column where values are 9-digit numbers.
  This made the code robust against variations in column names and positions and ensured it could detect SA2 codes dynamically in both files.

Issue 2 – OP1 (2024-05-14)
- Error Description:
  When multiple areas had the same population value, OP1 sometimes returned the wrong sequence of areas due to incorrect sorting method.
  I originally sorted the result based on just population value.
- Erroneous Code Snippet:
  largest_sa2 = sorted(sa2_pop[age_group], key=sa2_pop[age_group].get)[-1]
- Test Case:
  Two SA2s with identical population values caused inconsistent results depending on dictionary order.
- Reflection:
  I changed the sorting logic to use population in descending order and break ties using area code.
  This now complies with the instruction to use alphabetical area code as the tiebreaker.

Issue 3 – OP3 (2024-05-19)
- Error Description:
  OP3 produced repeated cosine similarity warnings due to empty or zero-valued population vectors.
- Erroneous Code Snippet:
  return dot / ((mag1 ** 0.5) * (mag2 ** 0.5))
- Test Case:
  An SA3 with more than 15 SA2s, but some of them had zero in all age groups, led to division by zero errors.
- Reflection:
  I added a filter to remove all-zero vectors and added a ZeroDivisionError catch to return 0.0 safely.
  I also removed SA3s with fewer than 2 valid SA2s to avoid unnecessary comparisons.
  
"""
