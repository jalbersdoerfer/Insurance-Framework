from mortality import MortalityTable


class TermLifeInsurance:

    def __init__(self, term: int, interest_rate: float, death_benefit: float,
                 mortality_table: MortalityTable):

        if term <= 0:
            raise ValueError("Term must be positive.")

        if interest_rate <= -1:
            raise ValueError("Interest rate must be greater than -1.")

        if death_benefit <= 0:
            raise ValueError("Death benefit must be positive.")
        
        self.term = term
        self.interest_rate = interest_rate
        self.death_benefit = death_benefit
        self.mortality_table = mortality_table

        self.discount_factor = 1 / (1 + interest_rate)
        
    
    def expected_present_value_benefit(self, age: int, gender: str) -> float:
        """
        Returns the expected present value of the death benefit based on a given age and gender.

        Assumption: 
        Death benefit is paid at the end of the year of death.
        """

        # Set initial ddp to 0.0
        discounted_death_probabilities = 0.0

        # Calculate the discounted death probabilities
        for year in range(1, self.term + 1): 
            death_probability = self.mortality_table.get_death_probability(age, gender, year)
            discounted_death_probabilities += (self.discount_factor ** year) * death_probability

        # Return expected present value of benefit
        return self.death_benefit * discounted_death_probabilities


    def premium_annuity_factor(self, age: int, gender: str) -> float:
        """
        Present value of a temporary life annuity-due

        Premiums are paid annually in advance, conditional on survival.
        """

        # Set initial annuity factor to 0.0
        annuity_factor = 0.0
        
        # Calculate the discounted survival probabilities
        for year in range(self.term):
            survival_probability = self.mortality_table.get_survival_probability(age, gender, year)
            annuity_factor += (self.discount_factor ** year) * survival_probability

        return annuity_factor


    def net_premium(self, age: int, gender: str) -> float: 
        """
        Calculates the annual net premium using the equivalence principle.

        Assumptions:
        - Premiums are paid annually in advance
        - The death benefit is paid at the end of the year of death
        - No expenses, commissions or additional benefits
        """

        # Get the expected present value of the benefits for given age and gender
        epv_benefit = self.expected_present_value_benefit(age, gender)

        # Get the premium annuity factor 
        premium_factor = self.premium_annuity_factor(age, gender)

        return epv_benefit / premium_factor

    def prospective_reserve(self, age: int, gender: str, t: int) -> float:
        """
        Calculates the prospective reserve at time t.

        The reserve is calculated immediately before the premium payment at time t.

        Assumptions:
        - Premiums are paid annually in advance
        - The death benefit is paid at the end of the year of death
        - The original net premium is used throughout the contract
        - No expenses, commissions or additional benefits
        """

        # Check if t is a valid contract duration
        if not isinstance(t, int):
            raise ValueError("t must be an integer.")

        if t < 0 or t > self.term:
            raise ValueError("t must be between 0 and the contract term.")

        # No future benefits or premiums remain at maturity
        if t == self.term:
            return 0.0

        # Remaining contract term
        remaining_term = self.term - t

        # Current age of the insured person
        current_age = age + t

        # Calculate the original annual net premium
        premium = self.net_premium(age, gender)

        # Calculate EPV of future benefits
        epv_benefits = 0.0
        for k in range(1, remaining_term + 1):
            death_probability = self.mortality_table.get_death_probability(current_age, gender, k)
            epv_benefits += (self.discount_factor ** k) * death_probability
        epv_benefits *= self.death_benefit

        # Calculate EPV of future premiums
        epv_premiums = 0.0
        for k in range(remaining_term):
            survival_probability = self.mortality_table.get_survival_probability(current_age, gender, k)
            epv_premiums += (self.discount_factor ** k) * survival_probability
        epv_premiums *= premium

        # Prospective reserve = EPV(future benefits) - EPV(future premiums)
        return epv_benefits - epv_premiums