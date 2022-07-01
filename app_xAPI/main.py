"""
Python script dedicated to take moodle-generated log csv (ver 3.5)
and create .json files describing xAPI statement following rules dictated at 
https://profiles.adlnet.gov/organization/76fcc051-ef64-4ba4-bfb4-b8035a7d1bf7/profile/e04ed3e2-8927-49c1-a296-2b210d6f269a/version/59c38ed7-428d-44bd-a6c8-bda383a56a92
"""
import config
import utils
from tincan import (
    Statement,
    Agent,
    Verb,
    Activity,
    Context,
    LanguageMap,
    ActivityDefinition,
    StateDocument,
)

def createAgent(idnumber):
    """
    create a tincan actor using the Agent method from the csv file provided in
    config.user_file
    @param id a string representing the id of the user in the csv file
    @returns the corresponding actor (with a name and mbox field). None if the id was not found
    """
    csvline = utils.fetch_line(config.user_file, "id", idnumber)
    if csvline != None:
        actor = Agent(
            name = csvline['username'],
            mbox = "mailto:"+csvline['email'],
        )
        return actor
    return None

if __name__ == '__main__':
    actor = createAgent("102")
    print(actor.name+".."+actor.mbox)
    print(actor)