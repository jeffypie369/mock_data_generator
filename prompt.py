# TODO: Account for composite keys (Jeff) - Done
# TODO: Add one more language/region for more "realistic" data. French? https://faker.readthedocs.io/en/master/locales/fr_FR.html# (Jeff)
# TODO: Add foreign key question when it is not the first table (Jeff) - Done

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
    invalid_characters = "\"!@#$%^&*()-+?_=,<>/1234567890"
    num_tables = input("How many tables do you need?\n")
    while not num_tables.isnumeric(): # Only numbers
        num_tables = reinput()
    
    tables_dict = {}

    for i in range(int(num_tables)):
        # Table
        table_name = input("Input the name of Table " + str(i+1) + ":\n")
        while any(c in invalid_characters for c in table_name): # Only word characters
            table_name = reinput()
        tables_dict[table_name] = {}
        num_rows = input("How many rows of data do you need for " + str.upper(table_name) + "? Min: 1, Max: 10000\n")
        while not num_rows.isnumeric(): # Only numbers
            num_rows = reinput()
        tables_dict[table_name]["num_rows"] = num_rows

        # Entities
        if i == 0:
            num_entities = input("How many columns for " + str.upper(table_name) + "?\n")
        else:
            num_entities = input("How many columns for " + str.upper(table_name) + " not counting foreign keys?\n")
        while not num_entities.isnumeric(): # Only numbers
            num_entities = reinput()
        for j in range(int(num_entities)):
            entity = input("What is the name of column " + str(j+1) + "?\n")
            while any(c in invalid_characters for c in entity): # Only word characters
                entity = reinput()
            tables_dict[table_name][entity] = {}
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

                if numeric_type == 'f':
                    distribution = input("Will " + str.upper(entity) + " values be in a specific mathematical distribution? Input:\n- 'n' for Normal Distribution\n- 'p' for Poisson Distribution\n- 's' to skip (default: Uniform Distribution)\n")
                    while not any(c in "nps" for c in distribution): # Only n or p or s
                        distribution = reinput()
                    tables_dict[table_name][entity]["distribution"] = distribution

                    decimals = input("How many decimal places do you want " + str.upper(entity) + " values to have? Input an integer (e.g. 2):\n")
                    while not decimals.isnumeric(): # Only numbers
                        decimals = reinput()
                    tables_dict[table_name][entity]["decimals"] = int(decimals)

                    if distribution == 'n': # Normal Distribution of Floats
                        mean = input("Input mean value (e.g. 0) in the Normal distribution for " + str.upper(entity) + ":\n")
                        while not isfloat(mean): # Only float
                            mean = reinput()
                        sd = input("Input standard deviation value (e.g. 1) in the normal distribution for " + str.upper(entity) + ":\n")
                        while not isfloat(sd): # Only float
                            sd = reinput()
                        tables_dict[table_name][entity]["mean"] = float(mean)
                        tables_dict[table_name][entity]["sd"] = float(sd)

                    if distribution == 'p': # Poisson Distribution of Floats
                        mean = input("Input lambda mean value (e.g. 10) in the Poisson distribution for " + str.upper(entity) + ":\n")
                        tables_dict[table_name][entity]["mean"] = float(mean)

                if numeric_type == 'i' or (numeric_type == 'f' and distribution == 's'): # Uniform Distribution of Integers/Floats
                    minimum = input("What is the minimum value allowed for " + str.upper(entity) + "?\n")
                    while not isfloat(minimum): # Only float
                        minimum = reinput()
                    tables_dict[table_name][entity]["min"] = int(minimum) if numeric_type == 'i' else float(minimum)
                    minimum_compulsory = input("Must there be a " + str.upper(entity) + " value of " + minimum + " in the dataset?\nIf compulsory, input 'y'. If not, input 'n'\n")
                    while not any(c in "yn" for c in minimum_compulsory): # Only y or n
                        minimum_compulsory = reinput()
                    tables_dict[table_name][entity]["compulsory_min"] = True if minimum_compulsory == 'y' else False
                    maximum = input("What is the maximum value allowed for " + str.upper(entity) + "?\n")
                    while not isfloat(maximum): # Only float
                        maximum = reinput()
                    tables_dict[table_name][entity]["max"] = int(maximum) if numeric_type == 'i' else float(maximum)
                    maximum_compulsory = input("Must there be a " + str.upper(entity) + " value of " + maximum + " in the dataset?\nIf compulsory, input 'y'. If not, input 'n'\n")
                    while not any(c in "yn" for c in maximum_compulsory): # Only y or n
                        maximum_compulsory = reinput()
                    tables_dict[table_name][entity]["compulsory_max"] = True if maximum_compulsory == 'y' else False

                    if numeric_type == 'i':
                        exclusion = input("Input any values in your defined range that you want to exclude for " + str.upper(entity) + ".\nSeparate them by commas (e.g. -1, 0, 1).\nIf none, input 'n':\n")
                        exclusion = exclusion.split(",")
                        exclusion = [int(val.strip()) for val in exclusion]
                        tables_dict[table_name][entity]["exclusion"] = exclusion



            # Datetime-specific Constraints (Kenny)
            if entity_type == 'dt':
                datetime_type = input("Does " + str.upper(entity) + " contain only the date or time, or both?\nIf only date, input 'd'. If only time, input 't'.\nIf both, input 'dt'.\n")
            while not any(c in "dt" for c in datetime_type): # Only d or t
                        datetime_type = reinput()

            if datetime_type == 'd':
                minimum = input("What is the lower bound of date allowed for " + str.upper(entity) + "? Please input using this format: YY, MM, DD (e.g. for 15 March 2023, input 15, 3, 2023)\n")
                minimum = minimum.split(",")
                minimum = [int(val.strip()) for val in minimum]
                tables_dict[table_name][entity]["min"] = int(minimum)
                maximum = input("What is the upper bound of date allowed for " + str.upper(entity) + "? Please input using this format: YY, MM, DD (e.g. for 15 March 2023, input 15, 3, 2023)\n")
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
                minimum = input("What is the lower bound of datetime allowed for " + str.upper(entity) + "? Please input using this format (24HR): YY, MM, DD, hh, mm, ss (e.g. for 14 February 1999, 6:25:30pm, input 14, 2, 1999, 18, 25, 30)\n")
                minimum = minimum.split(",")
                minimum = [int(val.strip()) for val in minimum]
                tables_dict[table_name][entity]["min"] = int(minimum)
                maximum = input("What is the upper bound of datetime allowed for " + str.upper(entity) + "? Please input using this format (24HR): YY, MM, DD, hh, mm, ss (e.g. for 14 February 1999, 6:25:30pm, input 14, 2, 1999, 18, 25, 30)\n")
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
                for k in range(num_foreign_keys):
                    foreign_key = input("Input the foreign table and column of the foreign key in the format TABLE.COLUMN (e.g., Student.student_id):\n")
                    foreign_table, foreign_key = foreign_key.split('.')
                    foreign_key_tup = (str.upper(foreign_table), foreign_key)
                    tables_dict[table_name]["foreign_keys"].append(foreign_key_tup)

        # Intra-table Constraints (FDs within table)
        # TODO: Generating data (Kenny)
        ## ==> Determine order of column creations based on FDs
        ## ==> Selectivity of RHS may get overridden

        # Inter-table Constraints (Foreign Keys)

    print(num_rows)
    print(tables_dict)

if __name__ == "__main__":
    main()
