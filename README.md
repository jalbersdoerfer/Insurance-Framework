# Life Insurance Simulation Framework

A Python-based framework for actuarial calculations and simulations in life insurance.

## Overview

This project implements a modular framework for modelling mortality and life insurance contracts.

The primary objective is to apply actuarial mathematics using Python while following principles of object-oriented programming.

The framework currently focuses on term life insurance and can be extended to other life insurance products.

## Features

- Mortality modelling based on empirical mortality tables
- Calculation of annual death and survival probabilities
- Expected present value of insurance benefits
- Calculation of net premiums for term life insurance using the equivalence principle
- Calculation of prospective reserve for term life insurance contract

## Actuarial Concepts

The current implementation covers:

- Annual mortality probabilities (qx)
- Annual survival probabilities (px)
- Deferred death probabilities
- Discounting and present value calculations
- Annual premiums
- Equivalence principle
- Prospective reserve calculations

## Data

The mortality model uses mortality data obtained from the German Federal Statistical Office (Destatis).

The original data is transformed into a standardized mortality table containing age- and gender-specific mortality probabilities.

## Technologies

- Python
- NumPy
- Pandas
- Matplotlib
- Jupyter Notebook

## Project Structure

The project separates the actuarial calculation logic and the data preprocessing into independent components.

## Limitations and Assumptions

The current framework is a simplified actuarial model intended for my own educational and demonstration purposes.

The implementation assumes:

- Annual mortality probabilities
- A constant technical interest rate
- Annual premium payments in advance
- Death benefits paid at the end of the year of death
- No expenses, commissions, taxes or surrender benefits
- No lapse or policyholder behaviour modelling

The mortality assumptions are based on the selected population mortality table and do not necessarily represent insured-life mortality.

## Analysis
The notebook 01_mortality_probabilities.ipynb visualizes the one-year death probabilities $q_x$ and survival probabilities 
$p_x$ from the mortality table across all available ages. Both probabilities are plotted separately for males and females to illustrate 
mortality patterns and gender differences by age. The survival probabilities are derived from the death probabilities using $p_x = 1 - q_x$.

![Death and Survival Probabilities](reports/figures/death_and_survival_probabilities_by_age.png)

The notebook 02_term_life_analysis.ipynb demonstrates how annual net premiums vary with the entry age of the insured person and 
how the prospective reserves change over the lifetime of a contract with a policyholder that is fifty years old at the beginning
of the contract.

It compares male and female policyholders using gender-specific mortality assumptions.

The analysis uses the equivalence principle to calculate annual net premiums for a 10-year term life insurance contract.

![Term Life Insurance Premium by Age](reports/figures/net_premium_TLI_by_age.png)
![Prospective Reserve over Contract Duration](reports/figures/prospective_reserve_TLI_over_years.png)

## Future Development

Planned extensions include:

- Whole life insurance
- Endowment insurance
- Annuity products
- Gross premium calculations
- Technical provisions and prospective reserves
- Monte Carlo portfolio simulations
- Sensitivity and scenario analysis