class Keys:
    APP_ID = ''
    TOKEN = ''
    CLIENT_ID = ''
    CLIENT_SECRET = ''

class Slots:
    Task = 'Task'
    List = 'List'


class Messages:

    # Welcome
    CARD_TITLE_WELCOME  = 'Welcome to Wunderlist for Alexa'
    REPROMPT_WELCOME    = 'Start by granting access to your wunderlist, after that you can say: ' \
                          'Create a task for cleaning my car or what are my tasks in my chores list?'
    SPEECH_WELCOME      = CARD_TITLE_WELCOME + '. ' + REPROMPT_WELCOME

    # Create Task
    CARD_TITLE_CREATE_TASK          = 'Create Task %s for List %s'
    SPEECH_CREATE_TASK              = 'I created a task for %s in your list %s'
    SPEECH_CREATE_TASK_RETRY        = 'You can try again saying. Create a task to wash my car in my list chores.'

    # Get Tasks
    CARD_TITLE_GET_TASKS    = 'Get Tasks for List %s'
    SPEECH_GET_TASKS        = 'These are your tasks in your %s list. %s.'
    SPEECH_GET_TASKS_EMPTY  = 'You have no tasks in your %s list.'
    SPEECH_GET_TASKS_RETRY  = 'You can try again saying. What are my tasks in my list chores?'

    # Goodbye
    CARD_TITLE_GOODBYE = 'Wunderlist closed'
    SPEECH_GOODBYE = 'Thank you for using Wunderlist for Alexa. Have a nice day!'

    # Ask Info
    SPEECH_ASK_TASK = 'What task should I create?'
    SPEECH_ASK_LIST = 'Which list?'

    # Errors
    SPEECH_SERVER_ERROR     = 'Sorry, I am having trouble creating tasks in Wunderlist. You can try again later'
    SPEECH_MISSING_LIST     = 'I couldn\'t find the list %s.'


