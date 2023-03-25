def main():
    num_rows = input("How many rows of data do you need? Min: 1, Max: 10000\n")
    num_tables = input("How many tables do you need?\n")
    
    tables_dict = {}

    for i in range(int(num_tables)):
        # Table
        table_name = input("Input the name of Table " + str(i+1) + ":\n")
        tables_dict[table_name] = {}

        # Entities
        num_entities = input("How many entities for " + table_name + "?\n")
        for j in range(int(num_entities)):
            entity = input("What is the name of entity " + str(j+1) + "?\n")
            tables_dict[table_name][entity] = {}
            entity_type = input("Is " + entity + " one of the known types in the following list?\n[name, address, email, postcode, age, id]\nIf yes, input the type. If no, input 'n'\n")
            if entity_type == 'n':
                entity_type_and_length = input("Input type and length in the format TYPE(LENGTH), e.g. VARCHAR(64):\n")
                entity_type, entity_length = entity_type_and_length.split("(")
                entity_length = entity_length[:-1]
                tables_dict[table_name][entity]["length"] = entity_length
            tables_dict[table_name][entity]["type"] = entity_type

            # General Constraints
            is_primary_key = input("Is " + entity + " the primary key of " + table_name + "? Input 'y' for yes, 'n' for no:\n")
            if is_primary_key == 'n':
                is_unique = input("Is " + entity + " unique? Input 'y' for yes, 'n' for no:\n")
                if is_unique == 'n':
                    tables_dict[table_name][entity]["is_unique"] = False
                else:
                    tables_dict[table_name][entity]["is_unique"] = True
            selectivity = input("Input selectivity, where 0 <= selectivity <= 1. Input 0 for no selectivity constraint:\n")
            tables_dict[table_name][entity]["selectivity"] = selectivity
            nonequalities = input("Input non-equalities separated by commas (e.g. Donald Duck, Mickey Mouse, Minnie Mouse). If none, input 'n':\n")
            nonequalities = nonequalities.split(",")
            nonequalities = [val.strip() for val in nonequalities]
            tables_dict[table_name][entity]["nonequalities"] = nonequalities

            # CHAR-specific Constraints
            
            # INT/FLOAT-specific Constraints

            # Datetime-specific Constraints


        # Intra-table Constraints

    # Inter-table Constraints

    print(num_rows)
    print(tables_dict)

if __name__ == "__main__":
    main()


# entities = input("Input the entities of " + table_name + " separated by commas (e.g. name, student_id, email):\n")
        # entities = entities.split(",")
        # entities = [ent.strip() for ent in entities]
        # entities_dict[table_name] = entities