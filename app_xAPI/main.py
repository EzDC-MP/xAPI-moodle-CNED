"""
Python script dedicated to take moodle-generated log csv (ver 3.5)
and create .json files describing xAPI statement following rules dictated at 
https://profiles.adlnet.gov/organization/76fcc051-ef64-4ba4-bfb4-b8035a7d1bf7/profile/e04ed3e2-8927-49c1-a296-2b210d6f269a/version/59c38ed7-428d-44bd-a6c8-bda383a56a92
"""

import xapi_resources
import config
import utils
import uuid
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

def create_agent(idnumber):
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

def get_activity_type(object_name):
    """
    reads off xapi_resources.activity_type dictionary and return the corresponding IRI of the activity type.
    @param an object name, found in the objecttable field in the config.log_file
    """
    if object_name in xapi_resources.activity_type:
        return xapi_resources.activity_type[object_name]
    return None

def get_name(csv_table, id):
    """
    read a csv table with name cvs_table located in config.csv_folder with an id field and name field,
    and returns the name field corresponding to the id field.
    If the csv_table is noexistent, or no name or id is found (Or if the function fail), 
    this function returns None
    @param csv_table the name of the file (without its extension) located in config.csv_folder
    """
    csvline = utils.fetch_line(config.csv_folder+"/"+csv_table+".csv","id",id)
    if csvline != None:
        if 'name' in csvline:
            return csvline['name']
    return None

#TODO : change this function completly to work with only objecttable and id
def create_object(target, objecttable, objectid, courseid, component, contextinstanceid):
    """
    create a tincan object using the object method from parameters given. 
    These parameters are fields from a line found in the file pointed at config.log_file
    @params string corresponding to the field in the csv file
    """
    
    #build the IRI. Building it from the component and contextinstanceid this way allow for some IRIs to be directly the url of the
    #object on the moodle website.
    IRI = config.moodle_url + component.replace("_","/") + "view.php?id=" + contextinstanceid

    if objecttable != None: #The object viewed is not the course itself
        #get the object name in the name table. Object_name is None if the request failed.
        Object_name = get_name(objecttable,objectid)
        Object_activity_type=get_activity_type(objecttable)
    
    if objecttable == None and target == "course":#The object viewed is the course itself.
        #get the object name in the name table. Object_name is None if the request failed.
        Object_name = get_name("course",courseid)
        Object_activity_type=get_activity_type("course")

    #build the object definition
    Object_definition = ActivityDefinition()
    if Object_name != None:
        Object_definition.name({'en':Object_name})
    if Object_activity_type != None:
        Object_definition.type(Object_activity_type)
        
    #build the object
    object = Activity(id=IRI)
    #add definition if needed
    if Object_name != None or Object_activity_type != None: 
        object.definition(Object_definition)

    return object

def create_verb(csvline):
    """
    Make a verb based on a standard logstore csvline. csvline are processed only if the 'action'
    field in the csvline is present in the supported action list.
    @requires csvline with a field of 'edulevel' = 2
    @param csvline a dictionary representing a line of the config.log_file csv file.
    @returns None if failed to create the verb, else return a tincan Verb object.
    @see xapi_resources.action_list
    """
    verb = None
    if 'action' in csvline:
        if csvline['action'] in xapi_resources.action_list:
            action = csvline['action']
            #Each action does not necesseraly correspond directly to an xAPI verb..
            # As such, even after the action is found, various specific test are to be made
            # to know wich xAPI verb to use. For instance the updated action is used both for an update
            # of a forum post, but also for the completion.. 
            if action=='updated':
                if csvline['target']=='course_module_completion':
                #this case correspond to the 'completed' verb
                    verb = Verb(
                        id=xapi_resources.verb["completed"],
                        display=LanguageMap({'en':'completed'})
                    )
            if action=='viewed':
                verb = Verb(
                    id=xapi_resources.verb["viewed"],
                    display=LanguageMap({'en':'viewed'})
                )
    return verb


def log_to_statement(csvline):
    """
    Make a statement solely produced off the config.log_file
    @requires csvline with a field of 'edulevel' = 2
    @param csvline a dictionary representing a line of the config.log_file csv file.
    @see csv.DictReader()
    """
    #Making the verb
    verb=create_verb(csvline)

    #Making the object
    #Building the IRI from the component and contextinstanceid this way allow for some IRIs to be directly the url of the
    #object on the moodle website.
    IRI = config.moodle_url + csvline['component'].replace("_","/") + "view.php?id=" + csvline['contextinstanceid']
    object = Activity(
        id=IRI
    )

    #Making the actor
    actor = Agent(
        mbox = "mailto:"+csvline['userid']+"@"+"moodle-example.com"
    )

    return Statement(actor=actor, verb=verb, object=object)


    

if __name__ == '__main__':
    #Simple tests in main   
    actor = create_agent("102")
    print(actor.name+".."+actor.mbox)
    print(actor)

    import csv
    with open(config.log_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['edulevel']=='2'and row['action']=='updated':
                statement_str=log_to_statement(row).to_json()
                print("writing.."+statement_str)
                utils.newjson("log_out", statement_str)