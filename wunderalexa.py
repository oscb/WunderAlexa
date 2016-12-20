from __future__ import print_function
import WunderPython
import AlexaUtils
import Constants

wunder = WunderPython.WunderClient.create_client(
    Constants.Keys.CLIENT_ID,
    Constants.Keys.CLIENT_SECRET)


def get_welcome_response():

    session_attributes = {}
    card_title = Constants.Messages.CARD_TITLE_WELCOME
    speech_output = Constants.Messages.SPEECH_WELCOME
    reprompt_text = Constants.Messages.REPROMPT_WELCOME
    should_end_session = False

    speechlet = AlexaUtils.build_speechlet(card_title,
                                           speech_output,
                                           reprompt_text,
                                           should_end_session,
                                           card_type='LinkAccount'
                                           )
    return AlexaUtils.build_response(session_attributes,
                                     speechlet
                                     )


def close_app():
    card_title = Constants.Messages.CARD_TITLE_GOODBYE
    speech_output = Constants.Messages.SPEECH_GOODBYE
    should_end_session = True
    speechlet = AlexaUtils.build_speechlet(card_title,
                                           speech_output,
                                           None,
                                           should_end_session
                                           )
    return AlexaUtils.build_response({},
                                     speechlet
                                     )


def create_task(intent, session):
    """
    Creates a task in a list
    Params:
    - Task
    - List*
    """
    session_attributes = {}
    should_end_session = False

    # Fill values in slots
    task = AlexaUtils.get_slot_value(intent, Constants.Slots.Task)
    wlist = AlexaUtils.get_slot_value(intent, Constants.Slots.List, 'Inbox')
    card_title = Constants.Messages.CARD_TITLE_CREATE_TASK % (task, wlist)

    if task is not None:
        token = AlexaUtils.get_user_token(session)
        if token is not None:
            wunder.build(token)
        else:
            return get_welcome_response()


        try:
            l = wunder.get_list(wlist)
        except Exception as e:
            print(e.message)
            l = None

        if l is None:
            # Return an error
            speech_output = Constants.Messages.SPEECH_MISSING_LIST % wlist + \
                            Constants.Messages.SPEECH_CREATE_TASK_RETRY
            reprompt_text = Constants.Messages.SPEECH_CREATE_TASK_RETRY
            # TODO: Maybe prompt for the name of the list again?

        else:
            # Create a task
            try:
                new_task = l.create_task(task)
                new_task.save()
                speech_output = Constants.Messages.SPEECH_CREATE_TASK % (task, wlist)
            except Exception as e:
                print(e.message)
                speech_output = Constants.Messages.SPEECH_SERVER_ERROR

            reprompt_text = None
            should_end_session = True
    else:
        # TODO: I can store in session that the last time he asked to create a task,
        # so I prompt for the task name and reroute next time!
        speech_output = Constants.Messages.SPEECH_ASK_TASK
        reprompt_text = Constants.Messages.SPEECH_ASK_TASK

    speechlet = AlexaUtils.build_speechlet(card_title,
                                           speech_output,
                                           reprompt_text,
                                           should_end_session
                                           )
    return AlexaUtils.build_response(session_attributes,
                                     speechlet
                                     )


def get_tasks(intent, session):
    """ Gets all tasks for an specific list """
    session_attributes = {}
    should_end_session = False

    # Fill values in slots
    wlist = AlexaUtils.get_slot_value(intent, Constants.Slots.List, 'Inbox')
    card_title = Constants.Messages.CARD_TITLE_GET_TASKS % wlist

    if wlist is not None:

        # Token
        token = AlexaUtils.get_user_token(session)
        if token is not None:
            wunder.build(token)
        else:
            return get_welcome_response()

        try:
            l = wunder.get_list(wlist)
        except Exception as e:
            print(e.message)
            l = None

        if l is None:
            # Return an error
            speech_output = Constants.Messages.SPEECH_MISSING_LIST % wlist + \
                            Constants.Messages.SPEECH_GET_TASKS_RETRY
            reprompt_text = Constants.Messages.SPEECH_GET_TASKS_RETRY
        else:
            # Find all tasks
            try:
                tasks = l.get_tasks()

                if len(tasks) > 0:
                    tasks_titles = ", ".join([t.title for t in tasks])
                    speech_output = Constants.Messages.SPEECH_GET_TASKS % (wlist, tasks_titles)
                else:
                    speech_output = Constants.Messages.SPEECH_GET_TASKS_EMPTY % wlist

            except Exception as e:
                print(e.message)
                speech_output = Constants.Messages.SPEECH_SERVER_ERROR

            reprompt_text = None
            should_end_session = True
    else:
        # TODO: I can store in session that the last time he asked to create a task,
        # so I prompt for the task name and reroute next time!
        speech_output = Constants.Messages.SPEECH_ASK_LIST
        reprompt_text = Constants.Messages.SPEECH_ASK_LIST

    speechlet = AlexaUtils.build_speechlet(card_title,
                                           speech_output,
                                           reprompt_text,
                                           should_end_session
                                           )
    return AlexaUtils.build_response(session_attributes,
                                     speechlet
                                     )

# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """
    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """
    # DO NOT start session here, as it may not be ever called
    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers

    if intent_name == "CreateTask":
        return create_task(intent, session)

    elif intent_name == "GetTasks":
        return get_tasks(intent, session)

    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()

    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return close_app()

    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.
    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    request = event['request']
    session = event['session']
    current_app = session['application']['applicationId']
    req_type = request['type']

    print("event.session.application.applicationId=" + current_app)

    # Validate that the request comes from the Alexa App ID
    if current_app != Constants.Keys.APP_ID:
        raise ValueError("Invalid Application ID")

    # Create a new session
    if session['new']:
        on_session_started({'requestId': request['requestId']}, session)

    # LaunchRequest = When an app is called with no commands
    if req_type == "LaunchRequest":
        return on_launch(request, session)

    # IntentRequest = User said an specific command
    elif req_type == "IntentRequest":
        return on_intent(request, session)

    # SessionEndedRequest = App is closed
    elif req_type == "SessionEndedRequest":
        return on_session_ended(request, session)