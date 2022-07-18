"""
common functions found in making statements
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

def create_agent(idnumber):#NOTE probably deprecated
    """
    create a tincan actor using the Agent method from the csv file provided in
    config.user_file
    @param id a string representing the id of the user in the csv file
    @returns the corresponding actor (with a name and mbox field). None if the id was not found
    @Note not used.
    """
    csvline = utils.fetch_line(config.user_file, "id", idnumber)
    if csvline != None:
        actor = Agent(
            name = csvline['username'],
            mbox = "mailto:"+csvline['email'],
        )
        return actor
    return None

def create_simple_agent(csvline):
    """
    create a tincan agent solely based on a csvline of config.log_file
    @requires csvline have an 'userid' field.
    @param csvline a dictionary representing a line of the config.log_file csv file.
    @see csv.DictReader()
    @returns a tincan agent actor. None if the userid field does not exists.
    """
    #Making the actor (this does not depend on the statement type..)
    if not('userid' in csvline):
        return None
    return Agent(mbox = "mailto:"+csvline['userid']+"@"+"moodle-example.com")

def create_timestamp(csvline):
    """
    create a datetime object solely based on a csvline of config.log_file
    @requires csvline have an 'timecreated' field.
    @param csvline a dictionary representing a line of the config.log_file csv file.
    @see csv.DictReader()
    @returns a datetime object. None if the function failed.
    """
    if not ('timecreated' in csvline):
        return None
    time = int(csvline['timecreated'])
    return datetime.fromtimestamp(time, pytz.timezone('Europe/Paris')).isoformat()

def create_verb(verbstring):
    """
    create a tincan verb using the verb method, based on 
    the verb dictionnary in xapi_resources
    @param verbstring a string
    @requires verbstring is present in xapi_resources.verb
    @returns a tincan verb object with its corresponding IRI and english languagemap. 
    Returns None if the verb is not present in the dictionnary
    @see xapi_resources.py
    """
    if verbstring in xapi_resources.verb:
        return Verb(id=xapi_resources.verb[verbstring], display=LanguageMap({'en':verbstring}))
    else:
        return None

def get_activity_type(object_name):
    """
    reads off xapi_resources.activity_type dictionary and return the corresponding IRI of the activity type.
    @param an object name.
    @Note most of the time, the object_name is found in the objecttable field of the logstore file (for viewed statement for instance)
    But this is not always the case. However the object_name always correspond to an objecttable present in the moodle db.
    """
    if object_name in xapi_resources.activity_type:
        return xapi_resources.activity_type[object_name]
    return None

#TODO : change this function completly to work with only objecttable and id
def create_object(target, objecttable, objectid, courseid, component, contextinstanceid):
    """
    create a tincan object using the object method from parameters given. 
    These parameters are fields from a line found in the file pointed at config.log_file
    @params string corresponding to the field in the csv file
    @deprecated for now
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