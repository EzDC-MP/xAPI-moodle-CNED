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
#see https://docs.moodle.org/dev/Events_API
event_list = {
   #viewed event (Yes i cc/cv all of this from the website :/)
   r"\core\event\course_viewed" : "viewed",
   r"\mod_resource\event\course_module_viewed" : "viewed",
   r"\mod_forum\event\course_module_viewed" : "viewed",
   r"\mod_forum\event\discussion_viewed" : "viewed", 
   r"\mod_page\event\course_module_viewed" : "viewed",
   r"\mod_chat\event\course_module_viewed" : "viewed",
   r"\mod_scorm\event\course_module_viewed" : "viewed",
   r"\mod_url\event\course_module_viewed" : "viewed",
   r"\mod_folder\event\course_module_viewed" : "viewed",
   r"\mod_forum\event\user_report_viewed" : "viewed",
   r"\mod_book\event\course_module_viewed" : "viewed",
   r"\mod_book\event\chapter_viewed" : "viewed",
   r"\gradereport_overview\event\grade_report_viewed" : "viewed",
   r"\mod_quiz\event\course_module_viewed" : "viewed",
   r"\mod_quiz\event\attempt_viewed" : "viewed",
   r"\mod_lesson\event\course_module_viewed" : "viewed",
   r"\mod_lesson\event\content_page_viewed" : "viewed",
   r"\mod_dialogue\event\course_module_viewed" : "viewed",
   r"\mod_dialogue\event\conversation_viewed" : "viewed",
   r"\core\event\recent_activity_viewed" : "viewed",
   r"\mod_lesson\event\question_viewed" : "viewed",
   r"\mod_scheduler\event\booking_form_viewed" : "viewed",
   r"\mod_workshop\event\course_module_viewed" : "viewed",
   r"\mod_questionnaire\event\course_module_viewed" : "viewed",
   r"\mod_glossary\event\course_module_viewed" : "viewed",
   r"\mod_collaborate\event\course_module_viewed" : "viewed",
   r"\mod_choice\event\course_module_viewed" : "viewed", 
   r"\mod_data\event\course_module_viewed" : "viewed",
   r"\mod_wiki\event\course_module_viewed" : "viewed",
   r"\mod_wiki\event\page_viewed" : "viewed",
   r"\mod_wiki\event\comments_viewed" : "viewed",
   r"\mod_wiki\event\page_history_viewed" : "viewed",
   r"\mod_glossary\event\entry_viewed" : "viewed",
   r"\mod_wiki\event\page_map_viewed" : "viewed",
   r"\mod_assign\event\submission_viewed" : "viewed",
   r"\mod_choicegroup\event\course_module_viewed" : "viewed",
   r"\core\event\badge_viewed" : "viewed",
   r"\mod_collaborate\event\recording_viewed" : "viewed",
   r"\core\event\course_user_report_viewed" : "viewed",
   r"\gradereport_user\event\grade_report_viewed" : "viewed",
   r"\mod_lti\event\course_module_viewed" : "viewed",
   #completed event
   r"\core\event\course_module_completion_updated" : "course_completed"
   #

}