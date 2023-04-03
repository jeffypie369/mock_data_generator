# Instructions

To run the program, navigate to your local directory containing the Python files `prompt.py` and `function.py`.
Open terminal and run the following command:
```bash
python prompt.py
```
Generated data output will be downloaded as a CSV file in the same directory on your local machine.

## Step-by-Step Guide to Use Mock Data Generator CLI

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

### CHARACTER Path
12a. If your column is one of the preset columns (postcode, card_num, isbn, id, name, address, email):
  1. Input any values you want to exclude, separated by commas. If none, input 'n'. (Conditions: Comma-separated strings or 'n')
  2. Input the maximum length of the characters. (Condition: Integer)
  3. If the type is ID, input the minimum length of the characters. (Condition: Integer)

12b. If your column is not one of the preset columns and you want to define a pattern, eg. CS5421:
  1. Input the desired length of the characters. (Condition: Integer)
  2. Input the desired pattern of the characters following the prompt. (Condition: String of 'l', 'd' and 'x')
  3. Input any values you want to exclude, separated by commas. If none, input 'n'. (Condition: Comma-separated strings or 'n')

### NUMBER Path
12a. Input whether number is integer or float. (Condition: 'f' or 'i') If float:
  1. Input the number of desired decimal places. (Condition: Integer)
  2. Input whether the values follow a distribution (Uniform (default) or Normal or Poisson). (Condition: 's', 'n' or 'p')
  3. If Uniform distribution, input minimum value, then maximum value in the next input. (Condition: Float)
  4. If Uniform distribution, input any values you want to exclude, separated by commas. If none, input 'n'. (Condition: Comma-separated strings of integers in defined range or 'n')
  5. If Normal distribution, input whether to build based on mean & standard deviation values, or based on estimated min and max values. (Condition: '1' or '2')
  6. If Normal distribution and 12a.5 input is '1', input mean, then standard deviation in the next input. (Condition: Float)
  7. If Normal distribution and 12a.5 input is '2', input estimated minimum value, then estimated maximum value in the next input. (Condition: Float)
  8. If Poisson distribution, input mean. (Condition: Float)

12b. If integer:
  1. Input minimum value. (Condition: Integer)
  2. Input maximum value. (Condition: Integer)
  3. Input any values you want to exclude, separated by commas. If none, input 'n'. (Condition: Comma-separated strings of floats in defined range or 'n')

### DATETIME Path
12a. Input whether column contains only date, or time, or both. (Condition: 'd' or 't' or 'dt')

12b. Input the desired lower bound following the format provided by the prompt.

12c. Input the desired upper bound following the format provided by the prompt.


13. Repeat steps 6 to 12 for all other columns in Table 1.
14. If the current table is not the first table, input whether there are foreign keys. Here, it is crucial to note that you can only reference tables that have already been created prior to this table. (Condition: 'y' or 'n')
15. Input the number of foreign keys in the current table which is the referencing table. (Condition: Integer)
16. Input the foreign referenced table and column in the format provided by the prompt. Here, the foreign key is case-sensitive, so make sure to enter the column name precisely.
17. Input the number of functional dependencies you have for this table. (Condition: Integer).
18. Input any functional dependencies you have for this table following the prompt.
19. Repeat steps 2 to 18 for all other tables, keeping in mind once again where foreign keys are involved, to have these referencing tables created after the referenced tables have been created.
