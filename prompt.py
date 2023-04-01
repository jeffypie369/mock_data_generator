# TODO: Account for composite keys (Jeff) - Done
# TODO: Add one more language/region for more "realistic" data. French? https://faker.readthedocs.io/en/master/locales/fr_FR.html# (Jeff)
# TODO: Add foreign key question when it is not the first table (Jeff) - Done

# TODO: exception handling for null values (due to pigeonhole) for primary keys

def main():
    num_tables = input("How many tables do you need?\n")
    
    tables_dict = {}

    for i in range(int(num_tables)):
        # Table
        table_name = input("Input the name of Table " + str(i+1) + ":\n")
        tables_dict[table_name] = {}
        num_rows = input("How many rows of data do you need for " + str.upper(table_name) + "? Min: 1, Max: 10000\n")
        tables_dict[table_name]["num_rows"] = int(num_rows)
        tables_dict[table_name]["entity_list"] = list()

        # Entities
        if i == 0:
            num_entities = input("How many columns for " + str.upper(table_name) + "?\n")    
        else:
            num_entities = input("How many columns for " + str.upper(table_name) + " not counting foreign keys?\n")
        for j in range(int(num_entities)):
            entity = input("What is the name of column " + str(j+1) + "?\n")
            tables_dict[table_name][entity] = {}
            tables_dict[table_name]["entity_list"].append(entity)
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

            # CHAR-specific Constraints (Xu Zeng)
            if entity_type == 'postcode' or  entity_type == 'card_num' or  entity_type == 'isbn' or entity_type == 'id' or entity_type == 'name' or entity_type == 'address' or entity_type == 'email':
                exclude_list = input("Input any values in your defined range that you want to exclude.\nSeparate them by commas (e.g. E1W 3TJ, SW1A 1AA).\nIf none, input 'n':\n")
                exclude_list = exclude_list.split(",")
                exclude_list = [val.strip() for val in exclude_list]
                tables_dict[table_name][entity]["exclusion"] = exclude_list
                if entity_type == 'id' or entity_type == 'name' or entity_type == 'address' or entity_type == 'email':
                    max_length = input("What is the maximum length of " + str.upper(entity) + "?\n")
                    tables_dict[table_name][entity]["max"] = int(max_length)
            
            if entity_type == 'char':
                length = input("What is the length of " + str.upper(entity) + "?\n")
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

                if numeric_type == 'f':
                    distribution = input("Will " + str.upper(entity) + " values be in a specific mathematical distribution? Input:\n- 'n' for Normal Distribution\n- 'p' for Poisson Distribution\n- 's' to skip (default: Uniform Distribution)\n")
                    tables_dict[table_name][entity]["distribution"] = distribution

                    decimals = input("How many decimal places do you want " + str.upper(entity) + " values to have? Input an integer (e.g. 2):\n")
                    tables_dict[table_name][entity]["decimals"] = int(decimals)
                    tables_dict[table_name][entity]["num_type"] = numeric_type

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
                    tables_dict[table_name][entity]["num_type"] = numeric_type

                    if numeric_type == 'i':
                        exclusion = input("Input any values in your defined range that you want to exclude for " + str.upper(entity) + ".\nSeparate them by commas (e.g. -1, 0, 1).\nIf none, input 'n':\n")
                        exclusion = exclusion.split(",")
                        exclusion = [int(val.strip()) for val in exclusion]
                        tables_dict[table_name][entity]["exclusion"] = exclusion



            # Datetime-specific Constraints (Kenny)
            if entity_type == 'dt':
                datetime_type = input("Does " + str.upper(entity) + " contain only the date or time, or both?\nIf only date, input 'd'. If only time, input 't'.\nIf both, input 'dt'.\n")

            if datetime_type == 'd':
                minimum = input("What is the lower bound of date allowed for " + str.upper(entity) + "? Please input using this format: YY, MM, DD (e.g. for 15 March 2023, input 15, 3, 2023)\n")
                minimum = minimum.split(",")
                minimum = [int(val.strip()) for val in minimum]
                tables_dict[table_name][entity]["min"] = minimum
                maximum = input("What is the upper bound of date allowed for " + str.upper(entity) + "? Please input using this format: YY, MM, DD (e.g. for 15 March 2023, input 15, 3, 2023)\n")
                maximum = maximum.split(",")
                maximum = [int(val.strip()) for val in maximum]
                tables_dict[table_name][entity]["max"] = maximum
                tables_dict[table_name][entity]["dt_type"] = datetime_type

            elif datetime_type == 't':
                minimum = input("What is the lower bound of time allowed for " + str.upper(entity) + "? Please input using this format (24HR): hh, mm, ss (e.g. for 3:55:29pm, input 15, 55, 29)\n")
                minimum = minimum.split(",")
                minimum = [int(val.strip()) for val in minimum]
                tables_dict[table_name][entity]["min"] = minimum
                maximum = input("What is the upper bound of time allowed for " + str.upper(entity) + "? Please input using this format (24HR): hh, mm, ss (e.g. for 3:55:29pm, input 15, 55, 29)\n")
                maximum = maximum.split(",")
                maximum = [int(val.strip()) for val in maximum]
                tables_dict[table_name][entity]["max"] = maximum
                tables_dict[table_name][entity]["dt_type"] = datetime_type

            elif datetime_type == 'dt':
                minimum = input("What is the lower bound of datetime allowed for " + str.upper(entity) + "? Please input using this format (24HR): YY, MM, DD, hh, mm, ss (e.g. for 14 February 1999, 6:25:30pm, input 14, 2, 1999, 18, 25, 30)\n")
                minimum = minimum.split(",")
                minimum = [int(val.strip()) for val in minimum]
                tables_dict[table_name][entity]["min"] = minimum
                maximum = input("What is the upper bound of datetime allowed for " + str.upper(entity) + "? Please input using this format (24HR): YY, MM, DD, hh, mm, ss (e.g. for 14 February 1999, 6:25:30pm, input 14, 2, 1999, 18, 25, 30)\n")
                maximum = maximum.split(",")
                maximum = [int(val.strip()) for val in maximum]
                tables_dict[table_name][entity]["max"] = maximum
                tables_dict[table_name][entity]["dt_type"] = datetime_type

                
        # Foreign Key Constraint
        if i > 0:
            has_foreign_key = input("Does " + table_name + " have any foreign keys? Input 'y' for yes, 'n' for no:\n")
            if has_foreign_key == 'y':
                tables_dict[table_name]["foreign_keys"] = []
                num_foreign_keys = input("How many foreign keys are there?\n")
                for k in range(num_foreign_keys):
                    foreign_key = input("Input the foreign table and column of the foreign key in the format TABLE.COLUMN (e.g., Student.student_id):\n")
                    foreign_table, foreign_key = foreign_key.split('.')
                    foreign_key_tup = (str.upper(foreign_table), foreign_key)
                    tables_dict[table_name]["foreign_keys"].append(foreign_key_tup)

        # Intra-table Constraints (FDs within table)
        # FDs: [ [[entityA, entityB], [entityC]], [[entityA], [entityD, entityE]] ] (AB->C, A->DE)
        # will require input
        
        

        # TODO: Generating data (Kenny)
        # Implementation does not consider FD constraints
        ### if fd_list is None
        output_list = list()
        for indiv_entity in tables_dict[table_name]["entity_list"]:
            if (indiv_entity["type"] == 'postcode'):
                # requires import from jeff's code
                output_list.append(postcode_generator(num_rows=tables_dict[table_name]["num_rows"], selectivity=tables_dict[table_name][indiv_entity]["selectivity"], exclusion=tables_dict[table_name][indiv_entity]["exclusion"]))
            elif (indiv_entity["type"] == 'card_num'):
                output_list.append(credit_card_number_generator(num_rows=tables_dict[table_name]["num_rows"], selectivity=tables_dict[table_name][indiv_entity]["selectivity"], exclusion=tables_dict[table_name][indiv_entity]["exclusion"]))
            elif (indiv_entity["type"] == 'isbn'):
                output_list.append(isbn_generator(num_rows=tables_dict[table_name]["num_rows"], selectivity=tables_dict[table_name][indiv_entity]["selectivity"], exclusion=tables_dict[table_name][indiv_entity]["exclusion"]))
            elif (indiv_entity["type"] == 'id'):
                output_list.append(id_generator(min=tables_dict[table_name][indiv_entity]["min"], max=tables_dict[table_name][indiv_entity]["max"], selectivity=tables_dict[table_name][indiv_entity]["selectivity"], exclusion=tables_dict[table_name][indiv_entity]["exclusion"], num_rows=tables_dict[table_name]["num_rows"]))
            elif (indiv_entity["type"] == 'name'):
                output_list.append(name_generator(max=tables_dict[table_name][indiv_entity]["max"], num_rows=tables_dict[table_name]["num_rows"], selectivity=tables_dict[table_name][indiv_entity]["selectivity"], exclusion=tables_dict[table_name][indiv_entity]["exclusion"]))
            elif (indiv_entity["type"] == 'address'):
                output_list.append(address_generator(max=tables_dict[table_name][indiv_entity]["max"], num_rows=tables_dict[table_name]["num_rows"], selectivity=tables_dict[table_name][indiv_entity]["selectivity"], exclusion=tables_dict[table_name][indiv_entity]["exclusion"]))
            elif (indiv_entity["type"] == 'email'):
                output_list.append(email_generator(max=tables_dict[table_name][indiv_entity]["max"], num_rows=tables_dict[table_name]["num_rows"], selectivity=tables_dict[table_name][indiv_entity]["selectivity"], exclusion=tables_dict[table_name][indiv_entity]["exclusion"]))
            elif (indiv_entity["type"] == 'char'):
                output_list.append(generate_random_strings(length=tables_dict[table_name][indiv_entity]["length"], pattern=tables_dict[table_name][indiv_entity]["pattern"], num_rows=tables_dict[table_name]["num_rows"], selectivity=tables_dict[table_name][indiv_entity]["selectivity"], exclusion=tables_dict[table_name][indiv_entity]["exclusion"]))
            elif (indiv_entity["type"] == 'num'):
                if (indiv_entity["num_type"] == 'i'):
                    output_list.append(int_generator(tables_dict[table_name]["num_rows"], tables_dict[table_name][indiv_entity]["min"], tables_dict[table_name][indiv_entity]["max"], exclusion=tables_dict[table_name][indiv_entity]["exclusion"], unique=False, selectivity=tables_dict[table_name][indiv_entity]["selectivity"]))
                elif (indiv_entity["num_type"] == 'f'):
                    if (indiv_entity["distribution"] == 'n'):
                        output_list.append(float_generator_normal(float_generator_uniform(tables_dict[table_name]["num_rows"], tables_dict[table_name][indiv_entity]["min"], tables_dict[table_name][indiv_entity]["max"], decimals=tables_dict[table_name][indiv_entity]["decimals"])))
                    # elif (indiv_entity["distribution"] == 'p'):
                        # output_list.append()
                    else:
                        output_list.append(float_generator_uniform(tables_dict[table_name]["num_rows"], tables_dict[table_name][indiv_entity]["min"], tables_dict[table_name][indiv_entity]["max"], exclusion=tables_dict[table_name][indiv_entity]["exclusion"], decimals=tables_dict[table_name][indiv_entity]["decimals"], selectivity=tables_dict[table_name][indiv_entity]["selectivity"]))

            elif (indiv_entity["type"] == 'dt'):
                if (indiv_entity["dt_type"] == 'd'):
                    output_list.append(generate_date(lower_bound_time=tables_dict[table_name][indiv_entity]["min"], upper_bound_time=tables_dict[table_name][indiv_entity]["max"], number_of_times_to_generate=tables_dict[table_name]["num_rows"], exclusion=tables_dict[table_name][indiv_entity]["exclusion"], selectivity=tables_dict[table_name][indiv_entity]["selectivity"]))
                elif (indiv_entity["dt_type"] == 't'):
                    output_list.append(generate_time(lower_bound_time=tables_dict[table_name][indiv_entity]["min"], upper_bound_time=tables_dict[table_name][indiv_entity]["max"], number_of_times_to_generate=tables_dict[table_name]["num_rows"], exclusion=tables_dict[table_name][indiv_entity]["exclusion"], selectivity=tables_dict[table_name][indiv_entity]["selectivity"]))
                elif (indiv_entity["dt_type"] == 'dt'):    
                    output_list.append(generate_datetime(lower_bound_time=tables_dict[table_name][indiv_entity]["min"], upper_bound_time=tables_dict[table_name][indiv_entity]["max"], number_of_times_to_generate=tables_dict[table_name]["num_rows"], exclusion=tables_dict[table_name][indiv_entity]["exclusion"], selectivity=tables_dict[table_name][indiv_entity]["selectivity"]))
        # to import csv
        myFile = open('realistic_data_generator.csv', 'w')
        writer = csv.writer(myFile)
        writer.writerow(tables_dict[table_name]["entity_list"])
        for list_index in range(len(int(num_rows))):
            temp_row = list()
            for entity_index in range(len(tables_dict[table_name]["entity_list"])):
                temp_row.append(output_list[entity_index][list_index])
            writer.writerow(temprow)
        myFile.close()

        # ### if fd_list is not None
        # output_list = list()
        # dependency_dict = {}
        # temp_dependency_dict = {}
        # for fd in fd_list:
        #     dependency_dict[fd] = {}
            
        # for row_index in range(int(num_rows)):
        #     temp_dependency_dict = {}
        #     for fd in fd_list:
        #         temp_dependency_dict[fd] = {}
        #         temp_row = list()
        #         lhs_temp = list()
        #         rhs_temp = list()
        #         for indiv_entity in tables_dict[table_name]["entity_list"]:
        #             if (indiv_entity["type"] == 'postcode'):
        #                 # requires import from jeff's code
        #                 data_generated = postcode_generator(num_rows=1, selectivity=tables_dict[table_name][indiv_entity]["selectivity"], exclusion=tables_dict[table_name][indiv_entity]["exclusion"])
        #             elif (indiv_entity["type"] == 'card_num'):
        #                 data_generated = credit_card_number_generator(num_rows=1, selectivity=tables_dict[table_name][indiv_entity]["selectivity"], exclusion=tables_dict[table_name][indiv_entity]["exclusion"])
        #             elif (indiv_entity["type"] == 'isbn'):
        #                 data_generated = isbn_generator(num_rows=1, selectivity=tables_dict[table_name][indiv_entity]["selectivity"], exclusion=tables_dict[table_name][indiv_entity]["exclusion"])
        #             elif (indiv_entity["type"] == 'id'):
        #                 data_generated = id_generator(min=tables_dict[table_name][indiv_entity]["min"], max=tables_dict[table_name][indiv_entity]["max"], selectivity=tables_dict[table_name][indiv_entity]["selectivity"], exclusion=tables_dict[table_name][indiv_entity]["exclusion"], num_rows=1)
        #             elif (indiv_entity["type"] == 'name'):
        #                 data_generated = name_generator(max=tables_dict[table_name][indiv_entity]["max"], num_rows=1, selectivity=tables_dict[table_name][indiv_entity]["selectivity"], exclusion=tables_dict[table_name][indiv_entity]["exclusion"])
        #             elif (indiv_entity["type"] == 'address'):
        #                 data_generated = address_generator(max=tables_dict[table_name][indiv_entity]["max"], num_rows=1, selectivity=tables_dict[table_name][indiv_entity]["selectivity"], exclusion=tables_dict[table_name][indiv_entity]["exclusion"])
        #             elif (indiv_entity["type"] == 'email'):
        #                 data_generated = email_generator(max=tables_dict[table_name][indiv_entity]["max"], num_rows=1, selectivity=tables_dict[table_name][indiv_entity]["selectivity"], exclusion=tables_dict[table_name][indiv_entity]["exclusion"])
        #             elif (indiv_entity["type"] == 'char'):
        #                 data_generated = generate_random_strings(length=tables_dict[table_name][indiv_entity]["length"], pattern=tables_dict[table_name][indiv_entity]["pattern"], num_rows=1, selectivity=tables_dict[table_name][indiv_entity]["selectivity"], exclusion=tables_dict[table_name][indiv_entity]["exclusion"])
        #             elif (indiv_entity["type"] == 'num'):
        #                 if (indiv_entity["num_type"] == 'i'):
        #                     data_generated = int_generator_single(tables_dict[table_name][indiv_entity]["min"], tables_dict[table_name][indiv_entity]["max"], exclusion=tables_dict[table_name][indiv_entity]["exclusion"])
        #                 elif (indiv_entity["num_type"] == 'f'):
        #                     if (indiv_entity["distribution"] == 'n'):
        #                         data_generated = float_generator_single(tables_dict[table_name][indiv_entity]["min"], tables_dict[table_name][indiv_entity]["max"], distribution='normal', exclusion=exclusion=tables_dict[table_name][indiv_entity]["exclusion"], decimals=tables_dict[table_name][indiv_entity]["decimals"])
        #                     else:
        #                         data_generated = float_generator_single(tables_dict[table_name][indiv_entity]["min"], tables_dict[table_name][indiv_entity]["max"], distribution='uniform', exclusion=exclusion=tables_dict[table_name][indiv_entity]["exclusion"], decimals=tables_dict[table_name][indiv_entity]["decimals"])
        #             elif (indiv_entity["type"] == 'dt'):
        #                 if (indiv_entity["dt_type"] == 'd'):
        #                     data_generated = generate_date(lower_bound_time=tables_dict[table_name][indiv_entity]["min"], upper_bound_time=tables_dict[table_name][indiv_entity]["max"], number_of_times_to_generate=1, exclusion=tables_dict[table_name][indiv_entity]["exclusion"], selectivity=tables_dict[table_name][indiv_entity]["selectivity"])
        #                 elif (indiv_entity["dt_type"] == 't'):
        #                     data_generated = generate_time(lower_bound_time=tables_dict[table_name][indiv_entity]["min"], upper_bound_time=tables_dict[table_name][indiv_entity]["max"], number_of_times_to_generate=1, exclusion=tables_dict[table_name][indiv_entity]["exclusion"], selectivity=tables_dict[table_name][indiv_entity]["selectivity"])
        #                 elif (indiv_entity["dt_type"] == 'dt'):    
        #                     data_generated = generate_datetime(lower_bound_time=tables_dict[table_name][indiv_entity]["min"], upper_bound_time=tables_dict[table_name][indiv_entity]["max"], number_of_times_to_generate=1, exclusion=tables_dict[table_name][indiv_entity]["exclusion"], selectivity=tables_dict[table_name][indiv_entity]["selectivity"])
        #             if indiv_entity in fd[0]:
        #                 lhs_temp.append(data_generated)
        #             if indiv_entity in fd[1]:
        #                 rhs_temp.append(data_generated)
        #             temp_row.append(data_generated)

        #         if (dependency_dict[fd][lhs_temp] is None and temp_dependency_dict[fd][lhs_temp] is None):
        #             temp_dependency_dict[fd][lhs_temp] = rhs_temp
        #         else:
        #             if (dependency_dict[fd][lhs_temp] == rhs_temp or temp_dependency_dict[fd][lhs_temp] == rhs_temp):
        #                 temp_dependency_dict[fd][lhs_temp] = rhs_temp
        #             else:
        #                 break
            
            

                

        ## ==> Determine order of column creations based on FDs
        ## ==> Selectivity of RHS may get overridden

        # Inter-table Constraints (Foreign Keys)

    print(num_rows)
    print(tables_dict)

if __name__ == "__main__":
    main()
