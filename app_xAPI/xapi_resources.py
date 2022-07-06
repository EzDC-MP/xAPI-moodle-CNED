"""
file with various informations, name and xAPI IRIs used thourought the script.
"""
#dictionary that associate a moodle object (course, book, quizz, lesson..) to an activity type
activity_type = {
    "course" : "http://adlnet.gov/expapi/activities/course",
    "book" : "http://id.tincanapi.com/activitytype/book",
    "quiz" : "http://adlnet.gov/expapi/activities/assessment",
}

#dictionary that associate a verb name to its IRI
#see verbs at 
# https://profiles.adlnet.gov/organization/76fcc051-ef64-4ba4-bfb4-b8035a7d1bf7/profile/e04ed3e2-8927-49c1-a296-2b210d6f269a/version/59c38ed7-428d-44bd-a6c8-bda383a56a92/concepts
verb = {
    "viewed" : "http://id.tincanapi.com/verb/viewed",
    "completed" : "http://adlnet.gov/expapi/verbs/completed",
    "replied" : "http://id.tincanapi.com/verb/replied"
}

#dict representing supported 'event' in the log csv file. That is to say a csvline off the config.log_file that does not
#have a value in the 'event' field present in this file won't be processed. the dict also indicate with which bevahior should be processed the csvline
event_list = {
    'viewed',
    'updated'
    #'answered'
}