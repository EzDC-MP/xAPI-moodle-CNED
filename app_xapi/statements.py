"""
this parts create statement when the csv line correspond to a view event.
Theses statements will be generated following theses rules :
First, we'll try to generate as much of the statement solely from the mdl_logstore_standard_log table.
IRI of agent object will always be formatted in "<moodle_url><object>_<objectid>" (with moodle_url being the one from the config.py file)
IRI of actor will be the mailbox type and will always be formatted in "mailto:<userid>@<url_of_the_moodle>"

Since every event line is more or less very specific, we have to use various method to parse the data.. hence the statements module.
"""
import common
import config
from tincan import (
    Statement,
    Agent,
    Verb,
    Activity,
    Context,
    ContextActivities,
    LanguageMap,
    ActivityDefinition,
    StateDocument,
)

def make_viewed(csvline):
    """
    Make an tincan statement object describing a viewed statement following this statement template :
    https://profiles.adlnet.gov/organization/76fcc051-ef64-4ba4-bfb4-b8035a7d1bf7/profile/e04ed3e2-8927-49c1-a296-2b210d6f269a/version/59c38ed7-428d-44bd-a6c8-bda383a56a92/templates/fa2726dd-4e03-4633-ac93-025fb2be5641
    @param csvline a correct line from config.log_file
    @requires 'eventname' field in the csvline is a correct entry in xapi_resources.event_list that points to 'viewed'
    @returns a tincan statement object if at least an actor, object and verb were successfully built from the csvline.
    else, returns None.
    """

    #Making correct IRI and context object
    #check if the objecttable is NULL or not. if it is NULL, then the object is probably the course.
    if csvline['objecttable'] == 'NULL':
        #check if, indeed we are looking at a course object
        if not(csvline['eventname'] == '\core\event\course_viewed'):
            return None #in this case, no statement is created.
        IRI = config.moodle_url+"course_"+csvline["courseid"]
        context = None
    #objecttable is not NULL, we define proper context and IRI for the object.
    else:
        IRI = config.moodle_url+csvline["objecttable"]+"_"+csvline["objectid"]
        IRI_parent = config.moodle_url+"course_"+csvline["courseid"]
        context_activities = ContextActivities(
                parent= Activity(id=IRI_parent)
        )
        context = Context(context_activities=context_activities)
    
    object = Activity(id=IRI)
    actor = common.create_simple_agent(csvline)
    verb = common.create_verb("viewed")
    timestamp = common.create_timestamp(csvline)

    if actor == None or verb == None: #if somehow the actor and verb creation failed, we return None.
        return None#Todo : we might want to log this kind of errors..

    statement=Statement(
        actor=actor, 
        verb=verb, 
        object=object
        )
    if context != None: #add context if it exists.
        statement.context = context
    
    if statement != None: #add timestamp if it exists.
        statement.timestamp = timestamp
    
    return statement

def make_course_completed():
    """
    Make an tincan statement object describing a completed statement following this statement template :
    https://profiles.adlnet.gov/organization/76fcc051-ef64-4ba4-bfb4-b8035a7d1bf7/profile/e04ed3e2-8927-49c1-a296-2b210d6f269a/version/59c38ed7-428d-44bd-a6c8-bda383a56a92/templates/fa2726dd-4e03-4633-ac93-025fb2be5641
    @param csvline a correct line from config.log_file
    @requires 'eventname' field in the csvline is a correct entry in xapi_resources.event_list that points to 'course_completed'
    @returns a tincan statement object if at least an actor, object and verb were successfully built from the csvline.
    else, returns None.
    """
