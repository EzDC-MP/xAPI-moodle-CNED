"""
Factorized code found in statements creation
"""

import utils
import config
import xapi_resources

#modules for timestamp creation
import pytz
from datetime import datetime

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

def create_simple_agent(csvline):
    """
    Creates a tincan agent solely based on a csvline from the config.mdl_logstore_standard_log file.

    @requires csvline have an 'userid' field.
    @returns a tincan agent actor. None if the userid field does not exists
    @param csvline a dictionary representing a line of the config.mdl_logstore_standard_log csv file
    @see csv.DictReader()
    """
    #Making the actor (this does not depend on the statement type..)
    if not('userid' in csvline):
        return None
    return Agent(mbox = "mailto:"+csvline['userid']+"@"+"moodle-example.com")

def create_timestamp(csvline):
    """
    Creates a datetime object solely based on a csvline from the config.mdl_logstore_standard_log file

    @requires csvline have a 'timecreated' field
    @returns a datetime object. None if the function failed
    @param csvline a dictionary representing a line of the config.mdl_logstore_standard_log csv file
    @see csv.DictReader()
    """
    if not ('timecreated' in csvline):
        return None
    time = int(csvline['timecreated'])
    return datetime.fromtimestamp(time, pytz.timezone('Europe/Paris')).isoformat()

def create_verb(verbstring):
    """
    Creates a Tincan verb object using the verb method, based on the verb dictionnary in xapi_resources

    @requires verbstring in xapi_resources.verb
    @returns a tincan verb object with its corresponding IRI and english languagemap,
    None if the verb is not present in the dictionnary
    @param verbstring a string
    @see xapi_resources.py
    """
    if verbstring in xapi_resources.verb:
        return Verb(id=xapi_resources.verb[verbstring], display=LanguageMap({'en':verbstring}))
    else:
        return None

def get_activity_type(object_name):
    """
    reads off xapi_resources.activity_type dictionary and returns the corresponding IRI of the activity type.

    @param object_name string of an object name.
    @returns the corresponding IRI string in xapi_resources.activity_type
    None if the object_name is not a key in xapi_resources.activity_type
    @see xapi_resources
    """
    if object_name in xapi_resources.activity_type:
        return xapi_resources.activity_type[object_name]
    return None


"""
Below are some functions that are not used at the moment by the script to make statements..
But could be useful for future implementations.. 
As for now, these functions are deprecated
"""

def create_agent(idnumber):
    """
    create a tincan actor using the Agent method from 
    the csv file provided inconfig.mdl_user
    @param id a string representing the id of the user in the csv file
    @returns the corresponding actor (with a name and mbox field). None if the id was not found
    @Note not unused / deprecated.
    """
    csvline = utils.fetch_line(config.mdl_user, "id", idnumber)
    if csvline != None:
        actor = Agent(
            name = csvline['username'],
            mbox = "mailto:"+csvline['email'],
        )
        return actor
    return None

#TODO : this function won't work for now
def create_object(objecttable, objectid, courseid=None):
    """
    create a tincan object using the object method from parameters given. 
    These parameters are fields from a line found in the file pointed at config.mdl_logstore_standard_log
    @params strings corresponding to the object table (mdl_<objecttable>) and its id in this table
    @returns a Tincan 
    @Note deprecated / unused
    """
    
    #build the IRI. Building it from the component and contextinstanceid this way allow for some IRIs to be directly the url of the
    #object on the moodle website.
    IRI = config.moodle_url+objecttable+"_"+objectid

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