import pandas as pd
import numpy as np

class MortalityTable: 

    def __init__(self, data: pd.DataFrame):

        # Required columns in the data
        required_columns = {
            'age', 
            'qx_male',  
            'qx_female'
        }

        # Check if all necessary columns are in the data
        if not required_columns.issubset(data.columns):
            raise ValueError(
                f"Missing columns: {required_columns - set(data.columns)}")

        # Copy the data for validity checks
        data = data.copy()

        # Check for duplicate ages in the data
        if data['age'].duplicated().any():
            raise ValueError('Duplicate ages found in mortality table.')

        # Set index of the data to 'age' for more efficient dataframe search
        data = data.set_index('age').sort_index()

        # Check if data contains missing values or invalid probabilities and create px columns
        for gender in ['male', 'female']:
            column = f"qx_{gender}"
            if data[column].isna().any():
                raise ValueError(f"Missing values in {column}.")
            if not data[column].between(0, 1).all():
                raise ValueError(f"Invalid probabilities in {column}.")
            # Create the px columns for the genders
            data[f"px_{gender}"] = 1 - data[column]

        # Asign data
        self.data = data

    
    def _validate_gender(self, gender: str) -> str:
        """
        Checks if gender is 'male' or 'female and returns the gender in lower case. 
        Otherwise throw a ValueError.
        """
        gender = gender.lower()

        if gender not in ['male', 'female']:
            raise ValueError("Gender must be 'male' or 'female'.")

        return gender
        

    def get_death_probability(self, age: int, gender: str, year: int) -> float: 
        """
        Probability of dying during year n, conditional on being alive at the starting age.
        """

        # Check if year >= 1
        if year < 1: 
            raise ValueError('Year must be at least 1.')

        # Check if given gender is valid
        gender = self._validate_gender(gender)

        # Define death age
        death_age = age + year - 1

        # Check if death_age is in mortality table
        if death_age not in self.data.index:
            raise ValueError(f"Age {death_age} not available in mortality table.")

        # Get probability that individual with given age survives until it reaches the death_age
        survival_probability = self.get_survival_probability(age, gender, year-1)

        # Retrieve the death probability from the data
        qx = self.data.at[death_age, f"qx_{gender}"]

        return survival_probability * qx


    def get_survival_probability(self, age: int, gender: str, years: int) -> float:
        """
        Probability of surviving the next 'years' years.
        """
        
        # Check if years is at least zero.
        if years < 0: 
            raise ValueError("Years cannot be negative.")

        # Check if given gender is valid
        gender = self._validate_gender(gender)

        # Return probability 1 if years is 0 (surviving another 0 years is trivial when being alive)
        if years == 0:
            return 1.0

        # Start with survival probability = 1 
        survival_probability = 1.0

        # Multiply the survival probabilities for each year until 'years'
        for year in range(years):
            current_age = age + year
            # Check if current age is in the data
            if current_age not in self.data.index:
                raise ValueError(f"Age {current_age} not available.")
            # Get the survival probability and multiply with the current value
            px = self.data.at[current_age, f"px_{gender}"]
            survival_probability *= px

        return survival_probability

        
    def sample_death_ages(self, age: int, gender: str, n_samples: int=1, seed: int=10) -> np.ndarray:
        """
        Returns an array of length 'n_samples' with different death ages for an individual with 
        given age and gender according to the distribution given from the mortality table.

        CAUTION:
        If max_age+1 is in the sample, this means that the individual survived the max_age from the table.
        In this case it does NOT mean that the individual died with this age.
        """
        
        # Checks if n_samples at least 1
        if n_samples < 1:
            raise ValueError('n_samples must be positive.')

        # Check if given gender is valid
        gender = self._validate_gender(gender)

        # Get the highest age available in the mortality table
        max_age = int(self.data.index.max())

        # Check if valid starting age was given.
        if age not in self.data.index or age > max_age: 
            raise ValueError('Starting age not available.')

        # Get all possible death ages given the starting age 
        # (the value of max_age + 1 represents survival beyond the last age available in the table)
        death_ages = np.arange(age, max_age+1)

        # Get probabilities for dying in each possible year given being alive at age 'age'
        probabilities = np.array(
            [self.get_death_probability(age, gender, year) for year in range(1, max_age - age + 2)]
        )

        # Get the probability of surviving the last possible age in the table
        survival_probability = self.get_survival_probability(age, gender, max_age - age + 1)

        # Add it to the end of the array
        probabilities = np.append(probabilities, survival_probability)

        # Create a list with all the possible outcomes. max_age + 1 represents survival beyond max_age
        possible_outcomes = np.append(death_ages, max_age + 1)

        # Create Random Number Generator
        rng = np.random.default_rng(seed)

        return rng.choice(possible_outcomes, size=n_samples, p=probabilities)