# TODO: Account for composite keys (Jeff) - Done
# TODO: Add one more language/region for more "realistic" data. French? https://faker.readthedocs.io/en/master/locales/fr_FR.html# (Jeff)
# TODO: Add foreign key question when it is not the first table (Jeff) - Done
def main():
    num_tables = input("How many tables do you need?\n")
    
    tables_dict = {}

    for i in range(int(num_tables)):
        # Table
        table_name = input("Input the name of Table " + str(i+1) + ":\n")
        tables_dict[table_name] = {}
        num_rows = input("How many rows of data do you need for " + table_name + "? Min: 1, Max: 10000\n")
        tables_dict[table_name]["num_rows"] = num_rows

        # Entities
        if i == 0:
            num_entities = input("How many columns for " + str.upper(table_name) + "?\n")    
        else:
            num_entities = input("How many columns for " + str.upper(table_name) + " not counting foreign keys?\n")
        for j in range(int(num_entities)):
            entity = input("What is the name of column " + str(j+1) + "?\n")
            tables_dict[table_name][entity] = {}
            entity_type = input("Is " + str.upper(entity) + " one of the known types in the following list?\n[name, address, email, id, postcode, card_num, isbn]\nIf yes, input the type. If no, input 'n'\n")
            if entity_type == 'n':
                entity_type = input("Choose datatype of " + str.upper(entity) + ":\n- For character values, input 'char'.\n- For numeric values, input 'num'.\n- For date/time values, input 'dt'.\n")
            tables_dict[table_name][entity]["type"] = entity_type

            # General Constraints
            is_primary_key = input("Is " + str.upper(entity) + " a primary key of " + str.upper(table_name) + "? Input 'y' for yes, 'n' for no:\n(NOTE: Having more than one primary key implies having a composite key)\n")
            if is_primary_key == 'n':
                is_unique = input("Is " + str.upper(entity) + " unique? Input 'y' for yes, 'n' for no:\n")
                if is_unique == 'n':
                    tables_dict[table_name][entity]["is_unique"] = False
                else:
                    tables_dict[table_name][entity]["is_unique"] = True

            selectivity = input("Input selectivity, where 0 <= selectivity <= 1. Input 0 for no selectivity constraint:\n")
            tables_dict[table_name][entity]["selectivity"] = float(selectivity)
            # TODO: shift exclusion to specific type constraints
            # exclusion = input("Input any values in your defined range that you want to exclude.\nSeparate them by commas (e.g. Donald Duck, Mickey Mouse, Minnie Mouse).\nIf none, input 'n':\n")
            # exclusion = exclusion.split(",")
            # exclusion = [val.strip() for val in exclusion]
            # tables_dict[table_name][entity]["exclusion"] = exclusion

            # CHAR-specific Constraints (Xu Zeng)
            if entity_type == 'postcode' or  entity_type == 'card_num' or  entity_type == 'isbn' or entity_type == 'id' or entity_type == 'name' or entity_type == 'address' or entity_type == 'email':
                exclude_list = input("Input any values in your defined range that you want to exclude.\nSeparate them by commas (e.g. E1W 3TJ, SW1A 1AA).\nIf none, input 'n':\n")
                exclude_list = exclude_list.split(",")
                exclude_list = [val.strip() for val in exclude_list]
                tables_dict[table_name][entity]["exclude_list"] = exclude_list
                if entity_type == 'id' or entity_type == 'name' or entity_type == 'address' or entity_type == 'email':
                    max_length = input("What is the maximum length of " + str.upper(entity) + "?\n")
                    tables_dict[table_name][entity]["max_length"] = int(max_length)
            
            if entity_type == 'char':
                length = input("What is the length of " + str.upper(entity) + "?\n")
                pattern = input("Input the pattern for " + str.upper(entity) + ".\nUse 'l' for letters, 'd' for digits, and 'x' for any character. (e.g. lddxx): \n")
                exclude_list = input("Input any values in your defined range that you want to exclude.\nSeparate them by commas (e.g. abc, 123).\nIf none, input 'n':\n")
                exclude_list = exclude_list.split(",")
                exclude_list = [val.strip() for val in exclude_list]
                tables_dict[table_name][entity]["exclude_list"] = exclude_list
                tables_dict[table_name][entity]["length"] = int(length)
                tables_dict[table_name][entity]["pattern"] = list(pattern)
            
            # INT/FLOAT-specific Constraints (Amanda)
            
            if entity_type == 'num':
                numeric_type = input("Does " + str.upper(entity) + " contain integers (no decimal places) or floats (with decimal places)?\nIf integers, input 'i'. If floats, input 'f'.\n")

                if numeric_type == 'f':
                    distribution = input("Will " + str.upper(entity) + " values be in a specific mathematical distribution? Input:\n- 'n' for Normal Distribution\n- 'p' for Poisson Distribution\n- 's' to skip (default: Uniform Distribution)\n")
                    tables_dict[table_name][entity]["distribution"] = distribution

                    decimals = input("How many decimal places do you want " + str.upper(entity) + " values to have? Input an integer (e.g. 2):\n")
                    tables_dict[table_name][entity]["decimals"] = int(decimals)

                    if distribution == 'n': # Normal Distribution of Floats
                        mean = input("Input mean value (e.g. 0) in the Normal distribution for " + str.upper(entity) + ":\n")
                        sd = input("Input standard deviation value (e.g. 1) in the normal distribution for " + str.upper(entity) + ":\n")
                        tables_dict[table_name][entity]["mean"] = float(mean)
                        tables_dict[table_name][entity]["sd"] = float(sd)

                    if distribution == 'p': # Poisson Distribution of Floats
                        mean = input("Input lambda mean value (e.g. 10) in the Poisson distribution for " + str.upper(entity) + ":\n")
                        tables_dict[table_name][entity]["mean"] = float(mean)

                if numeric_type == 'i' or (numeric_type == 'f' and distribution == 's'): # Uniform Distribution of Integers/Floats
                    minimum = input("What is the minimum value allowed for " + str.upper(entity) + "?\n")
                    tables_dict[table_name][entity]["min"] = int(minimum) if numeric_type == 'i' else float(minimum)
                    minimum_compulsory = input("Must there be a " + str.upper(entity) + " value of " + minimum + " in the dataset?\nIf compulsory, input 'y'. If not, input 'n'\n")
                    tables_dict[table_name][entity]["compulsory_min"] = True if minimum_compulsory == 'y' else False
                    maximum = input("What is the maximum value allowed for " + str.upper(entity) + "?\n")
                    tables_dict[table_name][entity]["max"] = int(maximum) if numeric_type == 'i' else float(maximum)
                    maximum_compulsory = input("Must there be a " + str.upper(entity) + " value of " + maximum + " in the dataset?\nIf compulsory, input 'y'. If not, input 'n'\n")
                    tables_dict[table_name][entity]["compulsory_max"] = True if maximum_compulsory == 'y' else False

                    if numeric_type == 'i':
                        exclusion = input("Input any values in your defined range that you want to exclude for " + str.upper(entity) + ".\nSeparate them by commas (e.g. -1, 0, 1).\nIf none, input 'n':\n")
                        exclusion = exclusion.split(",")
                        exclusion = [int(val.strip()) for val in exclusion]
                        tables_dict[table_name][entity]["exclusion"] = exclusion



            # Datetime-specific Constraints (Kenny)

                
        # Foreign Key Constraint
        if i > 0:
            has_foreign_key = input("Does " + table_name + " have any foreign keys? Input 'y' for yes, 'n' for no:\n")
            if has_foreign_key == 'y':
                tables_dict[table_name]["foreign_keys"] = []
                num_foreign_keys = input("How many foreign keys are there?\n")
                for k in num_foreign_keys:
                    foreign_key = input("Input the foreign table and column of the foreign key in the format TABLE.COLUMN (e.g., Student.student_id):\n")
                    foreign_table, foreign_key = foreign_key.split('.')
                    foreign_key_tup = (foreign_table, foreign_key)
                    tables_dict[table_name]["foreign_keys"].append(foreign_key_tup)

        # Intra-table Constraints (FDs within table)
        # TODO: Generating data (Kenny)
        ## ==> Determine order of column creations based on FDs
        ## ==> Selectivity of RHS may get overridden

    # Inter-table Constraints (FDs across tables)

    print(num_rows)
    print(tables_dict)

if __name__ == "__main__":
    main()
