import uuid
from faker import Faker
import pandas as pd
import random
import string
import numpy as np

def create_fake_data(num_rows = 10000):
    fake = Faker('en_GB')
    columns = ['Customer_Comm_ID', 'Customer_ID', 'Customer_Address_Type_ID', 'Address_Line1', 'Address_Line2', 'Address_Line3', 'Address_Line4', 'Address_Line5', 'Address_Line6', 'City_Of_Residence', 'Address_Landmark', 'Street', 'Building_Identifier', 'Suite_Flat_Identifier', 'District', 'Zip_Code', 'Country_ID', 'Email_Address', 'Run_ID', 'PO_Box_No', 'Country_Subentity', 'Address_Free', 'Province', 'ProvinceStateCodeOrName', 'Source_DB', 'CTDM_GDF_Proc', 'TIN']

    data = []
    for _ in range(num_rows):
        row = [
            str(uuid.uuid4().int)[:10],  # Customer_Comm_ID
            str(uuid.uuid4().int)[:10],  # Customer_ID
            fake.random_element(elements=('residential', 'commercial')),  # Customer_Address_Type_ID
            fake.building_number() + ', ' + fake.street_name(),  # Address_Line1
            'Block ' + fake.building_number() + ', ' + fake.street_name(),  # Address_Line2
            fake.city(),  # Address_Line3
            'United Kingdom, ' + fake.postcode(),  # Address_Line4
            '',  # Address_Line5
            '',  # Address_Line6
            fake.city(),  # City_Of_Residence
            fake.street_address(),  # Address_Landmark
            fake.street_name(),  # Street
            fake.building_number(),  # Building_Identifier
            fake.building_number(),  # Suite_Flat_Identifier
            fake.city(),  # District
            fake.postcode(),  # Zip_Code
            'GB',  # Country_ID
            fake.email(),  # Email_Address
            str(uuid.uuid4().int)[:10],  # Run_ID
            fake.building_number(),  # PO_Box_No
            fake.city(),  # Country_Subentity
            fake.street_address(),  # Address_Free
            fake.city(),  # Province
            fake.city(),  # ProvinceStateCodeOrName
            fake.word(),  # Source_DB
            fake.word(),  # CTDM_GDF_Proc
            ''.join(random.choices(string.ascii_uppercase, k=2)) + ''.join(random.choices(string.digits, k=6)) + random.choice(string.ascii_uppercase)  # TIN
        ]
        data.append(row)
    return pd.DataFrame(data, columns=columns)



def concatenate_address(df_artifact, i):
    df_artifact.iloc[i, df_artifact.columns.get_loc('Address_Line1')] = df_artifact.iloc[i, df_artifact.columns.get_loc('Address_Line1')] + ', ' + df_artifact.iloc[i, df_artifact.columns.get_loc('Address_Line2')] + ', ' + df_artifact.iloc[i, df_artifact.columns.get_loc('Address_Line3')]
    df_artifact.iloc[i, df_artifact.columns.get_loc('Address_Line2')] = ''
    df_artifact.iloc[i, df_artifact.columns.get_loc('Address_Line3')] = ''
    df_artifact.iloc[i, df_artifact.columns.get_loc('Error_Type')] = 'Concatenated Address'
    return df_artifact

def truncate_address(df_artifact, i):
    df_artifact.iloc[i, df_artifact.columns.get_loc('Address_Line1')] = df_artifact.iloc[i, df_artifact.columns.get_loc('Address_Line1')] + ', ' + df_artifact.iloc[i, df_artifact.columns.get_loc('Address_Line2')] + ', ' + df_artifact.iloc[i, df_artifact.columns.get_loc('Address_Line3')]
    address_line1 = df_artifact.iloc[i, df_artifact.columns.get_loc('Address_Line1')]
    if len(address_line1) >= 30:
        df_artifact.iloc[i, df_artifact.columns.get_loc('Address_Line1')] = address_line1[:31]
    # if we want to add additional logic based on commas or a % of the string
    # else:
    #     commas = [pos for pos, char in enumerate(address_line1) if char == ',']
    #     if len(commas) > 1:
    #         df_artifact.iloc[i, df_artifact.columns.get_loc('Address_Line1')] = address_line1[:commas[1]]
    #     else:
    #         df_artifact.iloc[i, df_artifact.columns.get_loc('Address_Line1')] = address_line1[:int(len(address_line1)*0.7)]
    df_artifact.iloc[i, df_artifact.columns.get_loc('Address_Line2')] = ''
    df_artifact.iloc[i, df_artifact.columns.get_loc('Address_Line3')] = ''
    df_artifact.iloc[i, df_artifact.columns.get_loc('Error_Type')] = 'Truncated Address'
    return df_artifact

def empty_city_field(df_artifact, i):
    df_artifact.iloc[i, df_artifact.columns.get_loc('Address_Line1')] = df_artifact.iloc[i, df_artifact.columns.get_loc('Address_Line1')] + ', ' + df_artifact.iloc[i, df_artifact.columns.get_loc('City_Of_Residence')]
    df_artifact.iloc[i, df_artifact.columns.get_loc('City_Of_Residence')] = ''
    df_artifact.iloc[i, df_artifact.columns.get_loc('Error_Type')] = 'Empty City Field'
    return df_artifact

def empty_post_code_field(df_artifact, i):
    df_artifact.iloc[i, df_artifact.columns.get_loc('Address_Line1')] = df_artifact.iloc[i, df_artifact.columns.get_loc('Address_Line1')] + ', ' + df_artifact.iloc[i, df_artifact.columns.get_loc('Zip_Code')]
    df_artifact.iloc[i, df_artifact.columns.get_loc('Zip_Code')] = ''
    df_artifact.iloc[i, df_artifact.columns.get_loc('Error_Type')] = 'Empty Post Code Field'
    return df_artifact

def wrong_city_postcode_country(df_artifact, i, fake):
    df_artifact.iloc[i, df_artifact.columns.get_loc('City_Of_Residence')] = fake.word()
    df_artifact.iloc[i, df_artifact.columns.get_loc('Zip_Code')] = fake.word()
    df_artifact.iloc[i, df_artifact.columns.get_loc('Country_ID')] = fake.word()
    df_artifact.iloc[i, df_artifact.columns.get_loc('Error_Type')] = 'Wrong City, Postcode, Country'
    return df_artifact

def special_characters_in_address(df_artifact, i):
    df_artifact.iloc[i, df_artifact.columns.get_loc('Address_Line1')] = df_artifact.iloc[i, df_artifact.columns.get_loc('Address_Line1')] + ' ' + ''.join(random.choices(string.punctuation, k=5))
    df_artifact.iloc[i, df_artifact.columns.get_loc('Error_Type')] = 'Special Characters in Address'
    return df_artifact

def wrong_tin_format(df_artifact, i, fake):
    df_artifact.iloc[i, df_artifact.columns.get_loc('TIN')] = fake.word()
    df_artifact.iloc[i, df_artifact.columns.get_loc('Error_Type')] = 'Wrong TIN Format'
    return df_artifact

def missing_tin_information(df_artifact, i):
    df_artifact.iloc[i, df_artifact.columns.get_loc('TIN')] = ''
    df_artifact.iloc[i, df_artifact.columns.get_loc('Error_Type')] = 'Missing TIN Information'
    return df_artifact

def introduce_errors(df):
    """
    This function introduces a variety of errors into a dataframe for testing purposes.

    Parameters:
    df (pandas.DataFrame): The original dataframe where errors will be introduced.

    Returns:
    df_artifact (pandas.DataFrame): The dataframe with introduced errors.

    The function works as follows:
    1. It makes a copy of the original dataframe to avoid modifying the original data.
    2. It adds a new column 'Error_Type' to the dataframe, initially setting its value to "No Error Introduced" for all rows.
    3. It iterates over each row in the dataframe. For each row, it randomly decides whether to introduce each type of error, with the probability of introducing each type of error being determined by a hard-coded probability.
    4. The types of errors that can be introduced are: concatenating the address, truncating the address, emptying the city field, emptying the post code field, setting the city, post code, and country to incorrect values, adding special characters to the address, setting the TIN to an incorrect format, and removing the TIN information.
    5. The function returns the modified dataframe.
    """
    df_artifact = df.copy()
    fake = Faker('en_GB')
    
    # Add a new column for error type
    df_artifact['Error_Type'] = "No Error Introduced" 
    
    for i in range(len(df_artifact)):
        if random.random() < 0.05:
            df_artifact = concatenate_address(df_artifact, i)
        if random.random() < 0.04:
            df_artifact = truncate_address(df_artifact, i)                
        if random.random() < 0.03:
            df_artifact = empty_city_field(df_artifact, i)
        if random.random() < 0.05:
            df_artifact = empty_post_code_field(df_artifact, i)
        if random.random() < 0.04:
            df_artifact = wrong_city_postcode_country(df_artifact, i, fake)
        if random.random() < 0.06:
            df_artifact = special_characters_in_address(df_artifact, i)
        if random.random() < 0.02:
            df_artifact = wrong_tin_format(df_artifact, i, fake)
        if random.random() < 0.05:
            df_artifact = missing_tin_information(df_artifact, i)
    return df_artifact


def introduce_group_errors(df, num_rows=1):
    """
    This function introduces a variety of errors into a dataframe for testing purposes.

    Parameters:
    df (pandas.DataFrame): The original dataframe where errors will be introduced.
    num_rows (int, optional): The number of rows where each type of error will be introduced. Default is 1.

    Returns:
    df_artifact (pandas.DataFrame): The dataframe with introduced errors.

    The function works as follows:
    1. It makes a copy of the original dataframe to avoid modifying the original data.
    2. It adds a new column 'Error_Type' to the dataframe, initially setting its value to "No Error Introduced" for all rows.
    3. It defines a list of error functions, each of which introduces a specific type of error into the dataframe.
    4. It iterates over the list of error functions. For each function, it applies the function to a certain number of rows in the dataframe.
    5. The number of rows to which each error function is applied is determined by the 'num_rows' parameter.
    6. The rows to which an error function is applied are determined by the index of the error function in the list. The first 'num_rows' rows are used for the first error function, the next 'num_rows' rows for the second error function, and so on.
    7. If the total number of rows in the dataframe is less than the number of rows required for all error functions, the remaining error functions are applied to the remaining rows in the dataframe.
    8. The function returns the modified dataframe.
    """
    df_artifact = df.copy()
    df_artifact['Error_Type'] = "No Error Introduced"    
    fake = Faker('en_GB')

    error_funcs = [
        concatenate_address,
        truncate_address,
        empty_city_field,
        empty_post_code_field,
        lambda df_artifact, i: wrong_city_postcode_country(df_artifact, i, fake),
        special_characters_in_address,
        lambda df_artifact, i: wrong_tin_format(df_artifact, i, fake),
        missing_tin_information
    ]

    for i, error_func in enumerate(error_funcs):
        start_row = i * num_rows
        end_row = start_row + num_rows
        for j in range(start_row, min(end_row, len(df_artifact))):
            df_artifact = error_func(df_artifact, j)

    return df_artifact