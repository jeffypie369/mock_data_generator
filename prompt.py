# TODO: Account for composite keys (Jeff)
# TODO: Add one more language/region for more "realistic" data. French? https://faker.readthedocs.io/en/master/locales/fr_FR.html# (Jeff)
# TODO: Add foreign key question when it is not the first table (Jeff)
def main():
    num_rows = input("How many rows of data do you need? Min: 1, Max: 10000\n") # Put this later under each table
    num_tables = input("How many tables do you need?\n")
    
    tables_dict = {}

    for i in range(int(num_tables)):
        # Table
        table_name = input("Input the name of Table " + str(i+1) + ":\n")
        tables_dict[table_name] = {}

        # Entities
        num_entities = input("How many columns for " + table_name + "?\n")
        for j in range(int(num_entities)):
            entity = input("What is the name of column " + str(j+1) + "?\n")
            tables_dict[table_name][entity] = {}
            entity_type = input("Is " + entity + " one of the known types in the following list?\n[name, address, email, postcode, age, id]\nIf yes, input the type. If no, input 'n'\n")
            if entity_type == 'n':
                entity_type_and_length = input("Input type and length in the format TYPE(LENGTH), e.g. VARCHAR(64):\n") # TODO: Can list available types
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
            # TODO: shift nonequalities to specific type constraints
            nonequalities = input("Input non-equalities separated by commas (e.g. Donald Duck, Mickey Mouse, Minnie Mouse). If none, input 'n':\n")
            nonequalities = nonequalities.split(",")
            nonequalities = [val.strip() for val in nonequalities]
            tables_dict[table_name][entity]["nonequalities"] = nonequalities

            # CHAR-specific Constraints (Xu Zeng)
            
            # INT/FLOAT-specific Constraints (Amanda)

            # Datetime-specific Constraints (Kenny)

        # Intra-table Constraints (FDs within table)
        # TODO: Generating data (Kenny)
        ## ==> Determine order of column creations based on FDs
        ## ==> Selectivity of RHS may get overridden

    # Inter-table Constraints (FDs across tables)

    print(num_rows)
    print(tables_dict)

if __name__ == "__main__":
    main()
