import pandas as pd
import numpy as np
from faker import Faker
import uuid

# Setting random seed for reproducibility
Faker.seed(0)

# Number of rows in the dataset
num_rows = 1000

# Generating customer IDs
customer_ids = [str(uuid.uuid4()) for _ in range(num_rows)]

# Generating ages following a normal distribution with mean 40 and standard deviation 10
ages = np.random.normal(loc=40, scale=10, size=num_rows)

# Generating incomes following a log-normal distribution
incomes = np.random.lognormal(mean=0, sigma=1, size=num_rows)

# Adding Gaussian noise to the numerical data
ages += np.random.normal(loc=0, scale=1, size=num_rows)
incomes += np.random.normal(loc=0, scale=1, size=num_rows)

# Creating the DataFrame
data = {
    'customer_id': customer_ids,
    'age': ages,
    'income': incomes
}

df = pd.DataFrame(data)

# Saving the dataset to a CSV file
df.to_csv('data/your_dataset.csv', index=False)