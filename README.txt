User Instructions

1. Input the number of tables you need. (Condition: Integer)
2. Input the name of Table 1. (Condition: word characters, '_' and '-' are allowed)
3. Input the number of rows you want for Table 1. (Condition: Integer)
4. Input the number of columns you want for Table 1. (Condition: Integer)
5. Input the language/region of your preference. As of 2/4/2023, English_US and French_FR are supported languages/regions. (Condition: 'en' or 'fr')
6. Input the name of Column 1. (Condition: word characters, '_' and '-' are allowed)
7. We support a preset number of data types that produce realistic data. These are (name, address, email, id, postcode, credit card number and ISBN). If this column is one of those data types, input the type as shown in the prompt. If not, input 'n'. (Condition: Given types in the prompt or 'n')
8. If step 7 is 'n', input 'char' for character values, 'num' for numeric values and 'dt' for datetime values. (Condition: 'char' or 'num or 'dt')
9. Input whether Column 1 is a primary key for Table 1. If you intend to have a composite key, input 'y' here for each of the candidate keys. (Condition: 'y' or 'n').
10. If step 9 is 'n' (i.e. not primary/candidate key), input whether Column 1 is to have unique values. (Condition: 'y' or 'n')
11. If step 10 is 'n' (i.e. non-unique values), input the selectivity constraint, if any. Input 0 if you do not have a selectivity constraint for this column. (Condition: 0 <= selectivity <= 1)
12. The path splits from here depending on whether your column type is char, num or dt.

(CHARACTER-path)
12.1. If your column is one of the preset columns (postcode, card_num, isbn, id, name, address, email):
12.1.a. Input any values you want to exclude, separated by commas. If none, input 'n'. (Conditions: Comma-separated strings or 'n')
12.1.b. Input the maximum length of the characters. (Condition: Integer)
12.1.c. If the type is ID, input the minimum length of the characters. (Condition: Integer)
12.2. If your column is not one of the preset columns and you want to define a pattern, eg. CS5421:
12.2.a. Input the desired length of the characters. (Condition: Integer)
12.2.b. Input the desired pattern of the characters following the prompt. (Condition: String of 'l', 'd' and 'x')
12.2.c. Input any values you want to exclude, separated by commas. If none, input 'n'. (Condition: Comma-separated strings or 'n')

(NUMBER-path)
12.1. Input whether number is integer or float. (Condition: 'f' or 'i') If float:
12.1.a. Input the number of desired decimal places. (Condition: Integer)
12.1.b. Input whether the values follow a distribution (Uniform (default) or Normal or Poisson). (Condition: 's', 'n' or 'p')
12.1.b.i. If Uniform distribution, input minimum value, then maximum value in the next input. (Condition: Float)
12.1.b.i.a. Input any values you want to exclude, separated by commas. If none, input 'n'. (Condition: Comma-separated strings of integers in defined range or 'n')
12.1.b.ii. If Normal distribution, input whether to build based on mean & standard deviation values, or based on estimated min and max values. (Condition: '1' or '2')
12.1.b.ii.a. If '1', input mean, then standard deviation in the next input. (Condition: Float)
12.1.b.ii.b. If '2', input estimated minimum value, then estimated maximum value in the next input. (Condition: Float)
12.1.b.iii. If Poisson distribution, input mean. (Condition: Float)
12.2. If integer:
12.2.a. Input minimum value. (Condition: Integer)
12.2.b. Input maximum value. (Condition: Integer)
12.2.c. Input any values you want to exclude, separated by commas. If none, input 'n'. (Condition: Comma-separated strings of floats in defined range or 'n')

(DATETIME-path)
12.1. Input whether column contains only date, or time, or both. (Condition: 'd' or 't' or 'dt')
12.2. Input the desired lower bound following the format provided by the prompt.
12.3. Input the desired upper bound following the format provided by the prompt.

13. Repeat steps 6 to 12 for all other columns in Table 1.
14. If the current table is not the first table, input whether there are foreign keys. Here, it is crucial to note that you can only reference tables that have already been created prior to this table. (Condition: 'y' or 'n')
15. Input the number of foreign keys in the current table which is the referencing table. (Condition: Integer)
16. Input the foreign referenced table and column in the format provided by the prompt. Here, the foreign key is case-sensitive, so make sure to enter the column name precisely. (Condition: FOREIGN_TABLE.foreign_key)
17. Input the number of functional dependencies you have for this table. (Condition: Integer). IMPORTANT: Our code is currently not optimized for this. It works but it takes a long time to generate data. We suggest starting with a small number of rows like 10 first. If you have already input a large number of rows earlier, we suggest you input 0 here and test for FD later with a smaller number of rows.
18. Input any functional dependencies you have for this table following the prompt.
19. Repeat steps 2 to 18 for all other tables, keeping in mind once again where foreign keys are involved, to have these referencing tables created after the referenced tables have been created.