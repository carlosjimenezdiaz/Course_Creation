# Dummy Data Generator

This project includes several Python scripts that serve different purposes:

- [`prompts.py`](prompts.py): This script is used to manage and handle system prompts, with functions that are called from `app.py`.
- [`app.py`](app.py): This script is the main Streamlit application, which is used to generate dummy data. It engages in conversation, asking for context and then generating code to create synthetic data, then runs that code, displays a sample and makes the resulting .csv downloadable. 

## Setup Instructions

To set up a Conda environment for this project, follow these steps:

1. Install [Anaconda](https://www.anaconda.com/products/distribution) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html) if you haven't already.

2. Update Conda (optional but recommended):

If you have not yet installed conda, you may do so by installing the Anaconda Distribution or Miniconda. If you have conda installed already (you can check in your terminal by entering “conda info”), all you need to do is update conda:

```sh
conda info
conda update -n base conda
```

3. Install mamba solver (optional but recommended):

Back in March of 2023, the conda team introduced a new experimental solver, conda-libmamba-solver, greatly improving the speed and efficiency of the conda solver.

To install and set the new solver, run the following commands:

```sh
conda install -n base conda-libmamba-solver
conda config --set solver libmamba
```

4. Create a new Conda environment with Python 3.11.7 (you can replace `myenv` with the name you want to give to your environment):

```sh
conda create -n myenv python=3.11.7
```

5. Activate the environment:

```sh
conda activate myenv
```

6. Install the required packages:

```sh
pip install -r requirements.txt
```

7. Create a file named secrets.toml in the .streamlit folder, containing the following template:

```sh
OPENAI_API_KEY = ""
AZURE_OPENAI_ENDPOINT = ""
 
[connections.snowflake]
user = ""
password = ""
warehouse = ""
role = ""
account = ""
```

## Usage

After setting up the environment and installing the required packages, you can run the scripts using Streamlit. For example, to run `app.py`, use the following command:

```sh
streamlit run app.py
```