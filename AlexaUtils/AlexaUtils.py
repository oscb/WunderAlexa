def build_speechlet(title, output, reprompt_text=None, should_end_session=False, card_type='Simple'):
    """
    :param title:
    :param output:
    :param reprompt_text:
    :param should_end_session:
    :param card_type:
    :return:
    """
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': card_type,
            'title': title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    """
    Builds an Alexa Response object
    :param session_attributes: Session JSON
    :param speechlet_response: Speechlet JSON
    :return: Response JSON
    """
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


def get_slot_value(intent, slot, default=None):
    """
    Gets a value from an intent slot
    :param intent: Intent JSON object
    :param slot: Name of the Slot
    :param default: Default Value (optional)
    :return: Value contained in the slot, default if any
    """
    if intent is None or intent['slots'] is None:
        return default

    if slot in intent['slots'] and 'value' in intent['slots'][slot]:
        return intent['slots'][slot]['value']
    return default


def get_user_token(session):
    """
    Gets the user AccessToken from the Session
    :param session: Session JSON Object
    :return: AccessToken, None if any
    """
    if 'user' in session and 'accessToken' in session['user']:
        return session['user']['accessToken']
    else:
        return None

