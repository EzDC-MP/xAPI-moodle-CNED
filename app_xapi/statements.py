"""
Functions dedicated to creating Tincan Statements object.
Theses statements will be generated following theses principles :
- First, we'll try to generate as much of the statement solely from the mdl_logstore_standard_log table.
- IRI of agent object will always be formatted in "<moodle_url><object>_<objectid>" 
(with moodle_url from the config.py file)
- IRI of actor will be the mailbox type and will always be formatted in "mailto:<userid>@<url_of_the_moodle>"

Since every event line is more or less very specific, we have to use various method to parse the data.. 
hence the statements module.
"""
import common
import config
import utils
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
    Make an tincan statement object describing a viewed statement following this statement profile :
    https://profiles.adlnet.gov/organization/76fcc051-ef64-4ba4-bfb4-b8035a7d1bf7/profile/e04ed3e2-8927-49c1-a296-2b210d6f269a/version/59c38ed7-428d-44bd-a6c8-bda383a56a92/templates/fa2726dd-4e03-4633-ac93-025fb2be5641
    
    @requires 'eventname' field in the csvline is a correct key in xapi_resources.event_list
    that points to 'viewed'
    @returns a tincan statement object if at least an actor, object and verb were successfully 
    built from the csvline. Else, returns None.
    @param csvline a correct line from config.mdl_logstore_standard_log
    @see xapi_resources.event_list
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
        return None #we might want to log this kind of errors..

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

def make_module_completed(csvline):
    """
    Make an tincan statement object describing a completed statement following this statement profile :
    https://profiles.adlnet.gov/organization/76fcc051-ef64-4ba4-bfb4-b8035a7d1bf7/profile/e04ed3e2-8927-49c1-a296-2b210d6f269a/version/59c38ed7-428d-44bd-a6c8-bda383a56a92/templates/fa2726dd-4e03-4633-ac93-025fb2be5641
    
    @requires 'eventname' field in the csvline is a correct key in xapi_resources.event_list
    that points to 'course_completed'
    @returns a tincan statement object if at least an actor, object and verb were successfully 
    built from the csvline. Else, returns None.
    @param csvline a correct line from config.mdl_logstore_standard_log
    @see xapi_resources.event_list
    """
    #getting the corrsponding csvline with the completionstate value..
    csvline_modules_completion = utils.fetch_line(config.mdl_course_modules_completion, 'id', csvline['objectid'])
    
    if csvline_modules_completion == None or csvline_modules_completion['completionstate'] == 0:
        return None #failed to find a corresponding line, or the module isn't completed.
    
    #lse, we keep processing the line..

    #making the context
    IRI_parent = config.moodle_url+"course_"+csvline["courseid"]
    context_activities = ContextActivities(
        parent= Activity(id=IRI_parent)
    )
    context = Context(context_activities=context_activities)

    #making the agent..
    agent = common.create_simple_agent(csvline)

    #making the verb..
    verb = common.create_verb("completed")

    #making the object..
    #getting the corresponding line with info on the module itself :
    csvline_course_modules = utils.fetch_line(config.mdl_course_modules, 'id', csvline_modules_completion['coursemoduleid'])
    if csvline_course_modules == None:
        object = None
    else:
        csvline_modules = utils.fetch_line(config.mdl_modules, 'id', csvline_course_modules['module'])
        if csvline_modules == None:
            object = None
        else:
            name = csvline_modules['name']
            ids = csvline_course_modules['instance']
            IRI = config.moodle_url+name+"_"+ids
            object = Activity(id=IRI)
    
    #making the timestamp..
    timestamp = common.create_timestamp(csvline)

    #making the whole statement :
    if object != None or context != None or agent != None or verb != None or timestamp != None:
        statement = Statement(
            actor=agent, 
            verb=verb, 
            object=object,
            context=context,
            timestamp=timestamp
        )
        return statement
    else:
        return None