import json
import math

from statistics import mean
from math import pi


class SimpleDataTool:

    AGENTS_FILEPATH = 'sfcc_2023_agents.json'
    CLAIM_HANDLERS_FILEPATH = 'sfcc_2023_claim_handlers.json'
    CLAIMS_FILEPATH = 'sfcc_2023_claims.json'
    DISASTERS_FILEPATH = 'sfcc_2023_disasters.json'

    REGION_MAP = {
        'west': 'Alaska,Hawaii,Washington,Oregon,California,Montana,Idaho,Wyoming,Nevada,Utah,Colorado,Arizona,New Mexico',
        'midwest': 'North Dakota,South Dakota,Minnesota,Wisconsin,Michigan,Nebraska,Iowa,Illinois,Indiana,Ohio,Missouri,Kansas',
        'south': 'Oklahoma,Texas,Arkansas,Louisiana,Kentucky,Tennessee,Mississippi,Alabama,West Virginia,Virginia,North Carolina,South Carolina,Georgia,Florida',
        'northeast': 'Maryland,Delaware,District of Columbia,Pennsylvania,New York,New Jersey,Connecticut,Massachusetts,Vermont,New Hampshire,Rhode Island,Maine'
    }

    def __init__(self):
        self.__agent_data = self.load_json_from_file(self.AGENTS_FILEPATH)
        self.__claim_handler_data = self.load_json_from_file(
            self.CLAIM_HANDLERS_FILEPATH)
        self.__claim_data = self.load_json_from_file(self.CLAIMS_FILEPATH)
        self.__disaster_data = self.load_json_from_file(
            self.DISASTERS_FILEPATH)

    # Helper Methods

    def load_json_from_file(self, filename):
        data = None

        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)

        return data

    def get_agent_data(self):
        return self.__agent_data

    def get_claim_handler_data(self):
        return self.__claim_handler_data

    def get_disaster_data(self):
        return self.__disaster_data

    def get_claim_data(self):
        return self.__claim_data

    # Unit Test Methods

    # region Test Set One

    def get_num_closed_claims(self):
        num_closed_claims = 0
        for claim in self.__claim_data:
            if claim['status'] == "Closed":
                num_closed_claims += 1
            
        return num_closed_claims

    def get_num_claims_for_claim_handler_id(self, claim_handler_id):
        """Calculates the number of claims assigned to a specific claim handler

        Args:
            claim_handler_id (int): id of claim handler

        Returns:
            int: number of claims assigned to claim handler
        """
        num_claims = 0

        for claim in self.__claim_data:
            if claim['claim_handler_assigned_id'] == claim_handler_id:
                num_claims += 1

        return num_claims

    def get_num_disasters_for_state(self, state):
        """Calculates the number of disasters for a specific state

        Args:
            state (string): name of a state in the United States of America,
                            including the District of Columbia

        Returns:
            int: number of disasters for state
        """
        stateDisasters = 0
        for disaster in self.__disaster_data:
            if disaster['state'] == state:
                stateDisasters += 1
        return stateDisasters

    # endregion

    # region Test Set Two

    def get_total_claim_cost_for_disaster(self, disaster_id):
        """Sums the estimated cost of a specific disaster by its claims

        Args:
            disaster_id (int): id of disaster

        Returns:
            float | None: estimate cost of disaster, rounded to the nearest hundredths place
                          returns None if no claims are found
        """
        totalDisasterCost = 0.0
        for claim in self.__claim_data:
            if claim['disaster_id'] == disaster_id:
                totalDisasterCost += claim["estimate_cost"]
        if totalDisasterCost == 0.0:
            return None
        else:
            return totalDisasterCost

    def get_average_claim_cost_for_claim_handler(self, claim_handler_id):
        """Gets the average estimated cost of all claims assigned to a claim handler

        Args:
            claim_handler_id (int): id of claim handler

        Returns:
            float | None : average cost of claims, rounded to the nearest hundredths place
                           or None if no claims are found
        """
        # check if no claims for the id
        if self.get_num_claims_for_claim_handler_id(claim_handler_id) == 0:
            return None
        
        total_claim_cost = 0.0
        num_claims = 0

        for claim in self.__claim_data:
            if claim['claim_handler_assigned_id'] == claim_handler_id:
                total_claim_cost += claim['estimate_cost']
                num_claims += 1
       
        average_cost = round((total_claim_cost / num_claims), 2)
        
        return average_cost

    def get_state_with_most_disasters(self):
        """Returns the name of the state with the most disasters based on disaster data

        If two states have the same number of disasters, then sort by alphabetical (a-z)
        and take the first.

        Example: Say New Jersey and Delaware both have the highest number of disasters at
                 12 disasters each. Then, this method would return "Delaware" since "D"
                 comes before "N" in the alphabet. 

        Returns:
            string: single name of state
        """
        # for each state
            # calculate number of disasters
            # save max value and state for that value
        state_disaster_count = {}

        for disaster in self.__disaster_data:
            state = disaster["state"]
            if state in state_disaster_count:
                state_disaster_count[state] += 1
            else:
                state_disaster_count[state] = 1

        max_disasters = max(state_disaster_count.values())

        # find states that tie for max disasters
        states_max_disasters = [state for state, count in state_disaster_count.items() if count == max_disasters]

        # alphabetically best
        most_disasters_state = sorted(states_max_disasters)[0]

        return most_disasters_state
            
        
        #if multiple states have same value
        #sort alphabetical
        
            
            
            

    def get_state_with_least_disasters(self):
        """Returns the name of the state with the least disasters based on disaster data

        If two states have the same number of disasters, then sort by alphabetical (a-z)
        and take the first.

        Example: Say New Mexico and West Virginia both have the least number of disasters at
                 1 disaster each. Then, this method would return "New Mexico" since "N"
                 comes before "W" in the alphabet. 

        Returns:
            string: single name of state
        """
        state_disaster_count = {}

        for disaster in self.__disaster_data:
            state = disaster["state"]
            if state in state_disaster_count:
                state_disaster_count[state] += 1
            else:
                state_disaster_count[state] = 1

        min_disasters = min(state_disaster_count.values())

        # find states that tie for max disasters
        states_min_disasters = [state for state, count in state_disaster_count.items() if count == min_disasters]

        least_disasters_state = sorted(states_min_disasters)[0]
        
        return least_disasters_state
    
    def get_most_spoken_agent_language_by_state(self, state):
        """Returns the name of the most spoken language by agents (besides English) for a specific state

        Args:
            state (string): name of state

        Returns:
            string: name of language
                    or empty string if state doesn't exist
        """
        language_count = {}
        for agent in self.__agent_data:
            if agent['state'] == state:
                lang = agent['secondary_language']
                if lang in language_count.keys():
                    language_count[lang] += 1
                else:
                    language_count[lang] = 1
        if not language_count:
            return ""
        max_count = max(language_count.values())
    
        most_spoken_languages = [state for state, count in language_count.items() if count == max_count]
        most_spoken_language = most_spoken_languages[0]
        
        
        
        return most_spoken_language

    def get_num_of_open_claims_for_agent_and_severity(self, agent_id, min_severity_rating):
        """Returns the number of open claims for a specific agent and for a minimum severity level and higher

        Note: Severity rating scale for claims is 1 to 10, inclusive.
        
        Args:
            agent_id (int): ID of the agent
            min_severity_rating (int): minimum claim severity rating

        Returns:
            int | None: number of claims that are not closed and have minimum severity rating or greater
                        -1 if severity rating out of bounds
                        None if agent does not exist, or agent has no claims (open or not)
        """
        
        if min_severity_rating < 1 or min_severity_rating > 10:
            return -1
        num_claims = 0
        for claim in self.__claim_data:
            if claim["agent_assigned_id"] is agent_id:
                if (claim['severity_rating'] >= min_severity_rating) and (claim['status'] != "Closed"):
                    num_claims += 1
        if num_claims == 0:
            return None
        else:
            return num_claims

    # endregion

    # region TestSetThree

    def get_num_disasters_declared_after_end_date(self):
        """Gets the number of disasters where it was declared after it ended
    
        Returns:
            int: number of disasters where the declared date is after the end date
        """
        count = 0

        for disaster in self.__disaster_data:

            declared_date = disaster['declared_date']
            end_date = disaster['end_date']

            if declared_date > end_date:
                count += 1

        return count

    def build_map_of_agents_to_total_claim_cost(self):
        """
        Builds a map of agent and their total claim cost

        Args:
            claims_data (list): List of dictionaries representing claim data.

        Hints:
            - An agent with no claims should return 0
            - Invalid agent id should have a value of None
            - You should round your total_claim_cost to the nearest hundredths

        Returns:
            dict: key is agent id, value is total cost of claims associated with the agent
        """
       
        agent_to_total_claim_cost = {}

       
        for agent in self.__agent_data:
            agent_id = agent['id']
            agent_to_total_claim_cost[agent_id] = 0

        
        for claim in self.__claim_data:
            agent_id = claim.get('agent_assigned_id', None)
            cost = claim.get('estimate_cost', 0)

            if agent_id in agent_to_total_claim_cost and (cost is not None):
                agent_to_total_claim_cost[agent_id] += cost
            else:
                agent_to_total_claim_cost[agent_id] = None

        for agent_id, total_cost in agent_to_total_claim_cost.items():
            if total_cost is not None:  
                agent_to_total_claim_cost[agent_id] = round(total_cost, 2)

        return agent_to_total_claim_cost

    def calculate_disaster_claim_density(self, disaster_id):
        """Calculates density of a diaster based on the number of claims and impact radius

        Hints:
            Assume uniform spacing between claims
            Assume disaster impact area is a circle

        Args:
            disaster_id (int): id of diaster

        Returns:
            float: density of claims to disaster area, rounded to the nearest thousandths place
                   None if disaster does not exist
        """
        
        

    # endregion

    # region TestSetFour

    def get_top_three_months_with_highest_num_of_claims_desc(self):
        """Gets the top three months with the highest total claim cost

        Hint:
            Month should be full name like 01 is January and 12 is December
            Year should be full four-digit year
            List should be in descending order

        Returns:
            list: three strings of month and year, descending order of highest claims
        """

        pass

    # endregion
