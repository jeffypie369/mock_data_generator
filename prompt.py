# TODO: Account for composite keys (Jeff) - Done
# TODO: Add one more language/region for more "realistic" data. French? https://faker.readthedocs.io/en/master/locales/fr_FR.html# (Jeff) - Done
# TODO: Add foreign key question when it is not the first table (Jeff) - Done

import pandas as pd
from random import randrange
import re
from functions import *

def reinput():
    value = input("You have provided an incorrect input. Please try again:\n")
    return value

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

def main():
    invalid_characters = "\"!@#$%^&*()+?=,<>/1234567890"
    num_tables = input("How many tables do you need?\n")
    while not num_tables.isnumeric(): # Only numbers
        num_tables = reinput()
    
    tables_dict = {}
    all_output_dict = {}

    for i in range(int(num_tables)):
        # Table
        table_name = input("Input the name of Table " + str(i+1) + ":\n")
        while any(c in invalid_characters for c in table_name): # Only word characters
            table_name = reinput()
        table_name = str.upper(table_name)
        tables_dict[table_name] = {}
        num_rows = input("How many rows of data do you need for " + str.upper(table_name) + "? Min: 1, Max: 10000\n")
        while not num_rows.isnumeric(): # Only numbers
            num_rows = reinput()
        tables_dict[table_name]["num_rows"] = int(num_rows)
        tables_dict[table_name]["entity_list"] = list()

        # Entities
        if i == 0:
            num_entities = input("How many columns for " + str.upper(table_name) + "?\n")
        else:
            num_entities = input("How many columns for " + str.upper(table_name) + " not counting foreign keys?\n")
        while not num_entities.isnumeric(): # Only numbers
            num_entities = reinput()
        region = input("For the columns name, address and email, we currently support the following languages/regions: English, French. Input 'en' for English and 'fr' for French.\n")
        while region not in ["en", "fr"]: # Only "en" or "fr"
            region = reinput()
        for j in range(int(num_entities)):
            entity = input("What is the name of column " + str(j+1) + "?\n")
            while any(c in invalid_characters for c in entity): # Only word characters
                entity = reinput()
            tables_dict[table_name][entity] = {}
            tables_dict[table_name]["entity_list"].append(entity)
            entity_type = input("Is " + str.upper(entity) + " one of the known types in the following list?\n[name, address, email, id, postcode, card_num, isbn]\nIf yes, input the type. If no, input 'n'\n")
            if entity_type == 'n':
                entity_type = input("Choose datatype of " + str.upper(entity) + ":\n- For character values, input 'char'.\n- For numeric values, input 'num'.\n- For date/time values, input 'dt'.\n")
            while any(c in invalid_characters for c in entity_type): # Only word characters
                entity_type = reinput()
            tables_dict[table_name][entity]["type"] = entity_type

            # General Constraints
            is_primary_key = input("Is " + str.upper(entity) + " a primary key of " + str.upper(table_name) + "? Input 'y' for yes, 'n' for no:\n(NOTE: Having more than one primary key implies having a composite key)\n")
            while not any(c in "yn" for c in is_primary_key): # Only y or n
                is_primary_key = reinput()
            if is_primary_key == 'n':
                is_unique = input("Is " + str.upper(entity) + " unique? Input 'y' for yes, 'n' for no:\n")
                while not any(c in "yn" for c in is_unique): # Only y or n
                    is_unique = reinput()
                if is_unique == 'n':
                    tables_dict[table_name][entity]["is_unique"] = False
                else:
                    tables_dict[table_name][entity]["is_unique"] = True

            selectivity = input("Input selectivity, where 0 <= selectivity <= 1. Input 0 for no selectivity constraint:\n")
            while not isfloat(selectivity): # Only float
                selectivity = reinput()
            tables_dict[table_name][entity]["selectivity"] = float(selectivity)

            # CHAR-specific Constraints (Xu Zeng)
            if entity_type == 'postcode' or  entity_type == 'card_num' or  entity_type == 'isbn' or entity_type == 'id' or entity_type == 'name' or entity_type == 'address' or entity_type == 'email':
                exclude_list = input("Input any values in your defined range that you want to exclude.\nSeparate them by commas (e.g. E1W 3TJ, SW1A 1AA).\nIf none, input 'n':\n")
                exclude_list = exclude_list.split(",")
                exclude_list = [val.strip() for val in exclude_list]
                tables_dict[table_name][entity]["exclusion"] = exclude_list
                if entity_type == 'id' or entity_type == 'name' or entity_type == 'address' or entity_type == 'email':
                    max_length = input("What is the maximum length of " + str.upper(entity) + "?\n")
                    while not max_length.isnumeric(): # Only numbers
                        max_length = reinput()
                    tables_dict[table_name][entity]["max"] = int(max_length)
                    if entity_type == 'id':
                        min_length = input("What is the minimum length of " + str.upper(entity) + "?\n")
                        while not min_length.isnumeric(): # Only numbers
                            min_length = reinput()
                        tables_dict[table_name][entity]["min"] = int(min_length)
                    if entity_type in ["name", "address", "email"]:
                        if region == "en":
                            tables_dict[table_name][entity]["region"] = "en_US"
                        else:
                            tables_dict[table_name][entity]["region"] = "fr_FR"
            
            if entity_type == 'char':
                length = input("What is the length of " + str.upper(entity) + "?\n")
                while not length.isnumeric(): # Only numbers
                    length = reinput()
                pattern = input("Input the pattern for " + str.upper(entity) + ".\nUse 'l' for letters, 'd' for digits, and 'x' for any character. (e.g. lddxx): \n")
                exclude_list = input("Input any values in your defined range that you want to exclude.\nSeparate them by commas (e.g. abc, 123).\nIf none, input 'n':\n")
                exclude_list = exclude_list.split(",")
                exclude_list = [val.strip() for val in exclude_list]
                tables_dict[table_name][entity]["exclusion"] = exclude_list
                tables_dict[table_name][entity]["length"] = int(length)
                tables_dict[table_name][entity]["pattern"] = list(pattern)
            
            # INT/FLOAT-specific Constraints (Amanda)
            
            if entity_type == 'num':
                numeric_type = input("Does " + str.upper(entity) + " contain integers (no decimal places) or floats (with decimal places)?\nIf integers, input 'i'. If floats, input 'f'.\n")
                while not any(c in "fi" for c in numeric_type): # Only f or i
                    numeric_type = reinput()
                tables_dict[table_name][entity]["num_type"] = numeric_type

                if numeric_type == 'f':
                    distribution = input("Will " + str.upper(entity) + " values be in a specific mathematical distribution? Input:\n- 'n' for Normal Distribution\n- 'p' for Poisson Distribution\n- 's' to skip (default: Uniform Distribution)\n")
                    while not any(c in "nps" for c in distribution): # Only n or p or s
                        distribution = reinput()
                    tables_dict[table_name][entity]["distribution"] = distribution

                    decimals = input("How many decimal places do you want " + str.upper(entity) + " values to have? Input an integer (e.g. 2):\n")
                    while not decimals.isnumeric(): # Only numbers
                        decimals = reinput()
                    tables_dict[table_name][entity]["decimals"] = int(decimals)

                    if distribution == 's': # Uniform Distribution of Floats
                        minimum = input("What is the minimum value allowed for " + str.upper(entity) + "?\n")
                        while not isfloat(minimum): # Only float
                            minimum = reinput()
                        tables_dict[table_name][entity]["min"] = float(minimum)
                        maximum = input("What is the maximum value allowed for " + str.upper(entity) + "?\n")
                        while not isfloat(maximum) or float(maximum) < float(minimum): # Only float
                            maximum = reinput()
                        tables_dict[table_name][entity]["max"] = float(maximum)

                    elif distribution == 'n': # Normal Distribution of Floats
                        mean = input("Input mean value (e.g. 0) in the Normal distribution for " + str.upper(entity) + ":\n")
                        while not isfloat(mean): # Only float
                            mean = reinput()
                        sd = input("Input standard deviation value (e.g. 1) in the normal distribution for " + str.upper(entity) + ":\n")
                        while not isfloat(sd): # Only float
                            sd = reinput()
                        tables_dict[table_name][entity]["mean"] = float(mean)
                        tables_dict[table_name][entity]["sd"] = float(sd)

                    elif distribution == 'p': # Poisson Distribution of Floats
                        mean = input("Input lambda mean value (e.g. 10) in the Poisson distribution for " + str.upper(entity) + ":\n")
                        tables_dict[table_name][entity]["mean"] = float(mean)

                elif numeric_type == 'i' : # Uniform Distribution of Integers
                    minimum = input("What is the minimum value allowed for " + str.upper(entity) + "?\n")
                    while not re.match(r'^-?\d+$', minimum): # Only integer
                        minimum = reinput()
                    maximum = input("What is the maximum value allowed for " + str.upper(entity) + "?\n")
                    while not re.match(r'^-?\d+$', maximum): # Only integer
                        maximum = reinput()
                    
                    tables_dict[table_name][entity]["min"] = int(minimum)
                    tables_dict[table_name][entity]["max"] = int(maximum)
                    # minimum_compulsory = input("Must there be a " + str.upper(entity) + " value of " + minimum + " in the dataset?\nIf compulsory, input 'y'. If not, input 'n'\n")
                    # while not any(c in "yn" for c in minimum_compulsory): # Only y or n
                    #     minimum_compulsory = reinput()
                    # tables_dict[table_name][entity]["compulsory_min"] = True if minimum_compulsory == 'y' else False
                    # maximum_compulsory = input("Must there be a " + str.upper(entity) + " value of " + maximum + " in the dataset?\nIf compulsory, input 'y'. If not, input 'n'\n")
                    # while not any(c in "yn" for c in maximum_compulsory): # Only y or n
                    #     maximum_compulsory = reinput()
                    # tables_dict[table_name][entity]["compulsory_max"] = True if maximum_compulsory == 'y' else False

                    exclusion = input("Input any integers in your defined range that you want to exclude for " + str.upper(entity) + ".\nSeparate them by commas (e.g. -1, 0, 1).\nIf none, input 'n':\n")
                    if exclusion=='n':
                        pass
                    else:
                        exclusion = exclusion.split(",")
                        exclusion_processed, exclusion_error, retry_flag = [], [], False
                        for val in exclusion:
                            val = val.strip()
                            try:
                                val = int(val)
                                exclusion_processed.append(val)
                            except:
                                exclusion_error.append(val)
                                retry_flag = True
                        while retry_flag == True:
                            exclusion_addon = input("The following input values were not processed due to formatting: " + str(exclusion_error) + "\nPlease verify that your inputs are integers, and input any corrected/additional values you wish to add. Separate them by commas (e.g. -1, 0, 1).\nIf you wish to skip, input 's':\n")
                            exclusion_error, retry_flag = [], False
                            if exclusion_addon == 's':
                                pass
                            else:
                                exclusion_addon = exclusion_addon.split(",")
                                for val in exclusion_addon:
                                    val = val.strip()
                                    try:
                                        val = int(val)
                                        exclusion_processed.append(val)
                                    except:
                                        exclusion_error.append(val)
                                        retry_flag = True
                        # exclusion = [int(val.strip()) for val in exclusion]
                        tables_dict[table_name][entity]["exclusion"] = exclusion_processed



            # Datetime-specific Constraints (Kenny)
            if entity_type == 'dt':
                datetime_type = input("Does " + str.upper(entity) + " contain only the date or time, or both?\nIf only date, input 'd'. If only time, input 't'.\nIf both, input 'dt'.\n")
                while not any(c in "dt" for c in datetime_type): # Only d or t
                            datetime_type = reinput()

                if datetime_type == 'd':
                    minimum = input("What is the lower bound of date allowed for " + str.upper(entity) + "? Please input using this format: YYYY, MM, DD (e.g. for 15 March 2023, input 2023, 3, 15)\n")
                    minimum = minimum.split(",")
                    minimum = [int(val.strip()) for val in minimum]
                    tables_dict[table_name][entity]["min"] = int(minimum)
                    maximum = input("What is the upper bound of date allowed for " + str.upper(entity) + "? Please input using this format: YYYY, MM, DD (e.g. for 15 March 2023, input 2023, 3, 15)\n")
                    maximum = maximum.split(",")
                    maximum = [int(val.strip()) for val in maximum]
                    tables_dict[table_name][entity]["max"] = int(maximum)

                elif datetime_type == 't':
                    minimum = input("What is the lower bound of time allowed for " + str.upper(entity) + "? Please input using this format (24HR): hh, mm, ss (e.g. for 3:55:29pm, input 15, 55, 29)\n")
                    minimum = minimum.split(",")
                    minimum = [int(val.strip()) for val in minimum]
                    tables_dict[table_name][entity]["min"] = int(minimum)
                    maximum = input("What is the upper bound of time allowed for " + str.upper(entity) + "? Please input using this format (24HR): hh, mm, ss (e.g. for 3:55:29pm, input 15, 55, 29)\n")
                    maximum = maximum.split(",")
                    maximum = [int(val.strip()) for val in maximum]
                    tables_dict[table_name][entity]["max"] = int(maximum)

                elif datetime_type == 'dt':
                    minimum = input("What is the lower bound of datetime allowed for " + str.upper(entity) + "? Please input using this format (24HR): YYYY, MM, DD, hh, mm, ss (e.g. for 14 February 1999, 6:25:30pm, input 1999, 2, 14, 18, 25, 30)\n")
                    minimum = minimum.split(",")
                    minimum = [int(val.strip()) for val in minimum]
                    tables_dict[table_name][entity]["min"] = int(minimum)
                    maximum = input("What is the upper bound of datetime allowed for " + str.upper(entity) + "? Please input using this format (24HR): YYYY, MM, DD, hh, mm, ss (e.g. for 14 February 1999, 6:25:30pm, input 1999, 2, 14, 18, 25, 30)\n")
                    maximum = maximum.split(",")
                    maximum = [int(val.strip()) for val in maximum]
                    tables_dict[table_name][entity]["max"] = int(maximum)


        # Foreign Key Constraint
        if i > 0:
            has_foreign_key = input("Does " + table_name + " have any foreign keys? Input 'y' for yes, 'n' for no:\n")
            while not any(c in "yn" for c in has_foreign_key): # Only y or n
                has_foreign_key = reinput()
            if has_foreign_key == 'y':
                tables_dict[table_name]["foreign_keys"] = []
                num_foreign_keys = input("How many foreign keys are there?\n")
                while not num_foreign_keys.isnumeric(): # Only numbers
                    num_foreign_keys = reinput()
                for k in range(int(num_foreign_keys)):
                    foreign_key = input("Input the foreign table and column of the foreign key in the format TABLE.COLUMN (e.g., Student.student_id):\n")
                    foreign_table, foreign_key = foreign_key.split('.')
                    foreign_key_tup = (str.upper(foreign_table), foreign_key)
                    tables_dict[table_name]["foreign_keys"].append(foreign_key_tup)
        
        num_fd = input("Input the number of functional dependencies (FDs) in this table, 0 if None.\n")
        while not num_fd.isnumeric(): # Only numbers
            num_fd = reinput()
        fd_list = []
        if int(num_fd) > 0:
            for m in range(int(num_fd)):
                fd = input("Input FD" + str(m+1) + " in the format \"COLUMN_1 -> COLUMN_2, COLUMN_3\" (e.g. student_id -> student_name, student_address).\nFor reference, this table has the following columns: "+ str(tables_dict[table_name]["entity_list"]))
                fd = fd.split('->')
                for nidx, n in enumerate(fd):
                    n = list(n.split(','))
                    for idx, _ in enumerate(n):
                        n[idx] = _.strip()
                    fd[nidx] = n
                    fd_list.append(fd)

        # TODO: Generating data (Kenny)
        # Implementation does not consider FD constraints
        if len(fd_list) == 0:
            output_dict = {}
            name_list = []
            for indiv_entity in tables_dict[table_name]["entity_list"]:
                if (tables_dict[table_name][indiv_entity]["type"] == 'postcode'):
                    # requires import from jeff's code
                    output_dict[indiv_entity] = postcode_generator(num_rows=tables_dict[table_name]["num_rows"], selectivity=tables_dict[table_name][indiv_entity]["selectivity"], exclusion=tables_dict[table_name][indiv_entity]["exclusion"])
                elif (tables_dict[table_name][indiv_entity]["type"] == 'card_num'):
                    output_dict[indiv_entity] = credit_card_number_generator(num_rows=tables_dict[table_name]["num_rows"], selectivity=tables_dict[table_name][indiv_entity]["selectivity"], exclusion=tables_dict[table_name][indiv_entity]["exclusion"])
                elif (tables_dict[table_name][indiv_entity]["type"] == 'isbn'):
                    output_dict[indiv_entity] = isbn_generator(num_rows=tables_dict[table_name]["num_rows"], selectivity=tables_dict[table_name][indiv_entity]["selectivity"], exclusion=tables_dict[table_name][indiv_entity]["exclusion"])
                elif (tables_dict[table_name][indiv_entity]["type"] == 'id'):
                    output_dict[indiv_entity] = id_generator(min=tables_dict[table_name][indiv_entity]["min"], max=tables_dict[table_name][indiv_entity]["max"], selectivity=tables_dict[table_name][indiv_entity]["selectivity"], exclusion=tables_dict[table_name][indiv_entity]["exclusion"], num_rows=tables_dict[table_name]["num_rows"])
                elif (tables_dict[table_name][indiv_entity]["type"] == 'name'):
                    names_list = name_generator(max=tables_dict[table_name][indiv_entity]["max"], num_rows=tables_dict[table_name]["num_rows"], selectivity=tables_dict[table_name][indiv_entity]["selectivity"], exclusion=tables_dict[table_name][indiv_entity]["exclusion"], region=tables_dict[table_name][indiv_entity]["region"])
                    output_dict[indiv_entity] = names_list
                elif (tables_dict[table_name][indiv_entity]["type"] == 'address'):
                    output_dict[indiv_entity] = address_generator(max=tables_dict[table_name][indiv_entity]["max"], num_rows=tables_dict[table_name]["num_rows"], selectivity=tables_dict[table_name][indiv_entity]["selectivity"], exclusion=tables_dict[table_name][indiv_entity]["exclusion"], region=tables_dict[table_name][indiv_entity]["region"])
                elif (tables_dict[table_name][indiv_entity]["type"] == 'email'):
                    if names_list:
                        output_dict[indiv_entity] = email_generator_from_names(names_list=name_list, max=tables_dict[table_name][indiv_entity]["max"], num_rows=tables_dict[table_name]["num_rows"], exclusion=tables_dict[table_name][indiv_entity]["exclusion"])
                    else:
                        output_dict[indiv_entity] = email_generator(max=tables_dict[table_name][indiv_entity]["max"], num_rows=tables_dict[table_name]["num_rows"], selectivity=tables_dict[table_name][indiv_entity]["selectivity"], exclusion=tables_dict[table_name][indiv_entity]["exclusion"], region=tables_dict[table_name][indiv_entity]["region"])
                elif (tables_dict[table_name][indiv_entity]["type"] == 'char'):
                    output_dict[indiv_entity] = generate_random_strings(length=tables_dict[table_name][indiv_entity]["length"], pattern=tables_dict[table_name][indiv_entity]["pattern"], num_rows=tables_dict[table_name]["num_rows"], selectivity=tables_dict[table_name][indiv_entity]["selectivity"], exclusion=tables_dict[table_name][indiv_entity]["exclusion"])
                elif (tables_dict[table_name][indiv_entity]["type"] == 'num'):
                    if (tables_dict[table_name][indiv_entity]["num_type"] == 'i'):
                        output_dict[indiv_entity] = int_generator(tables_dict[table_name]["num_rows"], tables_dict[table_name][indiv_entity]["min"], tables_dict[table_name][indiv_entity]["max"], exclusion=tables_dict[table_name][indiv_entity]["exclusion"], unique=False, selectivity=tables_dict[table_name][indiv_entity]["selectivity"])
                    elif (tables_dict[table_name][indiv_entity]["num_type"] == 'f'):
                        if (tables_dict[table_name][indiv_entity]["distribution"] == 'n'):
                            output_dict[indiv_entity] = float_generator_normal(float_generator_uniform(tables_dict[table_name]["num_rows"], tables_dict[table_name][indiv_entity]["min"], tables_dict[table_name][indiv_entity]["max"], decimals=tables_dict[table_name][indiv_entity]["decimals"]))
                        # elif (indiv_entity["distribution"] == 'p'):
                            # output_dict[indiv_entity] )
                        else:
                            output_dict[indiv_entity] = float_generator_uniform(tables_dict[table_name]["num_rows"], tables_dict[table_name][indiv_entity]["min"], tables_dict[table_name][indiv_entity]["max"], exclusion=tables_dict[table_name][indiv_entity]["exclusion"], decimals=tables_dict[table_name][indiv_entity]["decimals"], selectivity=tables_dict[table_name][indiv_entity]["selectivity"])
                
                elif (indiv_entity["type"] == 'dt'):
                    if (indiv_entity["dt_type"] == 'd'):
                        output_list.append(generate_date(lower_bound_time=tables_dict[table_name][indiv_entity]["min"], upper_bound_time=tables_dict[table_name][indiv_entity]["max"], number_of_times_to_generate=tables_dict[table_name]["num_rows"], exclusion=tables_dict[table_name][indiv_entity]["exclusion"], selectivity=tables_dict[table_name][indiv_entity]["selectivity"]))
                    elif (indiv_entity["dt_type"] == 't'):
                        output_list.append(generate_time(lower_bound_time=tables_dict[table_name][indiv_entity]["min"], upper_bound_time=tables_dict[table_name][indiv_entity]["max"], number_of_times_to_generate=tables_dict[table_name]["num_rows"], exclusion=tables_dict[table_name][indiv_entity]["exclusion"], selectivity=tables_dict[table_name][indiv_entity]["selectivity"]))
                    elif (indiv_entity["dt_type"] == 'dt'):    
                        output_list.append(generate_datetime(lower_bound_time=tables_dict[table_name][indiv_entity]["min"], upper_bound_time=tables_dict[table_name][indiv_entity]["max"], number_of_times_to_generate=tables_dict[table_name]["num_rows"], exclusion=tables_dict[table_name][indiv_entity]["exclusion"], selectivity=tables_dict[table_name][indiv_entity]["selectivity"]))
            
            if i > 0 and "foreign_keys" in tables_dict[table_name]:
                fk_dict = {}
                for fk in tables_dict[table_name]["foreign_keys"]:
                    fk_table = fk[0]
                    fk_entity = fk[1]
                    if fk_table not in fk_dict:
                        fk_dict[fk_table] = []
                    fk_dict[fk_table].append(fk_entity)
                for fk_table in fk_dict:
                    fk_data = all_output_dict[fk_table]
                    df_fk_data = pd.DataFrame(fk_data)
                    df_fk_data = df_fk_data[fk_dict[fk_table]]
                    fk_num_rows = int(tables_dict[fk_table]["num_rows"])
                    for _ in range(int(num_rows)):
                        num = randrange(fk_num_rows)
                        for ent in fk_dict[fk_table]:
                            if ent not in output_dict:
                                output_dict[ent] = []
                            output_dict[ent].append(df_fk_data[ent][num])

            # Save table data to csv
            output = pd.DataFrame(output_dict)
            all_output_dict[str.upper(table_name)] = output_dict
            output.to_csv(str.upper(table_name) + '_data.csv')
        
        else:
            output_list = list()
            output_dict = {}
            entity_dict = {}
            entity_index = 0
            for entity in entity_list:
                entity_dict[entity] = entity_index
                entity_index = entity_index + 1
            
            lhs = []
            rhs = []
            for fd in fd_list:
                for lhs_fd in fd[0]:
                    lhs.append(entity_dict[lhs_fd])
                for rhs_fd in fd[1]:
                    rhs.append(entity_dict[rhs_fd])

                
            for row_index in range(int(num_rows)):
                temp_row = list()
                row_satisfies_fd = True
                for indiv_entity in tables_dict[table_name]["entity_list"]:
                    if (indiv_entity["type"] == 'postcode'):
                        # requires import from jeff's code
                        data_generated = postcode_generator(num_rows=1, selectivity=tables_dict[table_name][indiv_entity]["selectivity"], exclusion=tables_dict[table_name][indiv_entity]["exclusion"])
                    elif (indiv_entity["type"] == 'card_num'):
                        data_generated = credit_card_number_generator(num_rows=1, selectivity=tables_dict[table_name][indiv_entity]["selectivity"], exclusion=tables_dict[table_name][indiv_entity]["exclusion"])
                    elif (indiv_entity["type"] == 'isbn'):
                        data_generated = isbn_generator(num_rows=1, selectivity=tables_dict[table_name][indiv_entity]["selectivity"], exclusion=tables_dict[table_name][indiv_entity]["exclusion"])
                    elif (indiv_entity["type"] == 'id'):
                        data_generated = id_generator(min=tables_dict[table_name][indiv_entity]["min"], max=tables_dict[table_name][indiv_entity]["max"], selectivity=tables_dict[table_name][indiv_entity]["selectivity"], exclusion=tables_dict[table_name][indiv_entity]["exclusion"], num_rows=1)
                    elif (indiv_entity["type"] == 'name'):
                        data_generated = name_generator(max=tables_dict[table_name][indiv_entity]["max"], num_rows=1, selectivity=tables_dict[table_name][indiv_entity]["selectivity"], exclusion=tables_dict[table_name][indiv_entity]["exclusion"], region=tables_dict[table_name][indiv_entity]["region"])
                    elif (indiv_entity["type"] == 'address'):
                        data_generated = address_generator(max=tables_dict[table_name][indiv_entity]["max"], num_rows=1, selectivity=tables_dict[table_name][indiv_entity]["selectivity"], exclusion=tables_dict[table_name][indiv_entity]["exclusion"], region=tables_dict[table_name][indiv_entity]["region"])
                    elif (indiv_entity["type"] == 'email'):
                        if names_list:
                            data_generated = email_generator_from_names(names_list=name_list, max=tables_dict[table_name][indiv_entity]["max"], num_rows=1, selectivity=tables_dict[table_name][indiv_entity]["selectivity"], exclusion=tables_dict[table_name][indiv_entity]["exclusion"])
                        else:
                            data_generated = email_generator(max=tables_dict[table_name][indiv_entity]["max"], num_rows=1, selectivity=tables_dict[table_name][indiv_entity]["selectivity"], exclusion=tables_dict[table_name][indiv_entity]["exclusion"], region=tables_dict[table_name][indiv_entity]["region"])
                    elif (indiv_entity["type"] == 'char'):
                        data_generated = generate_random_strings(length=tables_dict[table_name][indiv_entity]["length"], pattern=tables_dict[table_name][indiv_entity]["pattern"], num_rows=1, selectivity=tables_dict[table_name][indiv_entity]["selectivity"], exclusion=tables_dict[table_name][indiv_entity]["exclusion"])
                    elif (indiv_entity["type"] == 'num'):
                        if (indiv_entity["num_type"] == 'i'):
                            data_generated = int_generator_single(tables_dict[table_name][indiv_entity]["min"], tables_dict[table_name][indiv_entity]["max"], exclusion=tables_dict[table_name][indiv_entity]["exclusion"])
                        elif (indiv_entity["num_type"] == 'f'):
                            if (indiv_entity["distribution"] == 'n'):
                                data_generated = float_generator_single(tables_dict[table_name][indiv_entity]["min"], tables_dict[table_name][indiv_entity]["max"], distribution='normal', exclusion=tables_dict[table_name][indiv_entity]["exclusion"], decimals=tables_dict[table_name][indiv_entity]["decimals"])
                            else:
                                data_generated = float_generator_single(tables_dict[table_name][indiv_entity]["min"], tables_dict[table_name][indiv_entity]["max"], distribution='uniform', exclusion=tables_dict[table_name][indiv_entity]["exclusion"], decimals=tables_dict[table_name][indiv_entity]["decimals"])
                    elif (indiv_entity["type"] == 'dt'):
                        if (indiv_entity["dt_type"] == 'd'):
                            data_generated = generate_date(lower_bound_time=tables_dict[table_name][indiv_entity]["min"], upper_bound_time=tables_dict[table_name][indiv_entity]["max"], number_of_times_to_generate=1, exclusion=tables_dict[table_name][indiv_entity]["exclusion"], selectivity=tables_dict[table_name][indiv_entity]["selectivity"])
                        elif (indiv_entity["dt_type"] == 't'):
                            data_generated = generate_time(lower_bound_time=tables_dict[table_name][indiv_entity]["min"], upper_bound_time=tables_dict[table_name][indiv_entity]["max"], number_of_times_to_generate=1, exclusion=tables_dict[table_name][indiv_entity]["exclusion"], selectivity=tables_dict[table_name][indiv_entity]["selectivity"])
                        elif (indiv_entity["dt_type"] == 'dt'):    
                            data_generated = generate_datetime(lower_bound_time=tables_dict[table_name][indiv_entity]["min"], upper_bound_time=tables_dict[table_name][indiv_entity]["max"], number_of_times_to_generate=1, exclusion=tables_dict[table_name][indiv_entity]["exclusion"], selectivity=tables_dict[table_name][indiv_entity]["selectivity"])
                    
                    temp_row.append(data_generated)
                    
                    # if i > 0 and "foreign_keys" in tables_dict[table_name]:
                    #     fk_dict = {}
                    #     for fk in tables_dict[table_name]["foreign_keys"]:
                    #         fk_table = fk[0]
                    #         fk_entity = fk[1]
                    #         if fk_table not in fk_dict:
                    #             fk_dict[fk_table] = []
                    #         fk_dict[fk_table].append(fk_entity)
                    #     for fk_table in fk_dict:
                    #         fk_data = all_output_dict[fk_table]
                    #         df_fk_data = pd.DataFrame(fk_data)
                    #         df_fk_data = df_fk_data[fk_dict[fk_table]]
                    #         fk_num_rows = int(tables_dict[fk_table]["num_rows"])
                    #         num = randrange(fk_num_rows)
                    #         for ent in fk_dict[fk_table]:
                    #             if ent not in output_dict:
                    #                 output_dict[ent] = []
                    #             output_dict[ent].append(df_fk_data[ent][num])

                temp_row_lhs = []
                temp_row_rhs = []
                for lhs_index in lhs:
                    temp_row_lhs.append(temp_row[lhs_index])
                for rhs_index in rhs:
                    temp_row_rhs.append(temp_row[rhs_index])
                
                for each_row in output_list:
                    output_row_lhs = []
                    output_row_rhs = []
                    for lhs_index in lhs:
                        output_row_lhs.append(each_row[lhs_index])
                    for rhs_index in rhs:
                        output_row_rhs.append(each_row[rhs_index])
                    
                    if (temp_row_lhs == output_row_lhs):
                        row_satisfies_fd = temp_row_rhs == output_row_rhs    


                if row_satisfies_fd is True:
                    output_list.append(temp_row)
                    print(output_list)
                
            # to import csv
            # myFile = open('realistic_data_generator_fd.csv', 'w')
            # writer = csv.writer(myFile)
            # writer.writerow(tables_dict[table_name]["entity_list"])
            # for row in output_list:
            #     writer.writerow(row)
            # myFile.close()

        ## ==> Determine order of column creations based on FDs
        ## ==> Selectivity of RHS may get overridden

        # Inter-table Constraints (Foreign Keys)

    print(num_rows)
    print(tables_dict)

if __name__ == "__main__":
    main()
