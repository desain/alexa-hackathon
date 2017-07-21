"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

import random

FOODS_LIST = {
    'pizza': {
        'Amount': {
            '1': {
                'Seconds': 30,
                'AmountType': 'slice of'
            },
            '2': {
                'Seconds': 60,
                'AmountType': 'slices of'
            },
            '3': {
                'Seconds': 90,
                'AmountType': 'slices of'
            },
            '4': {
                'Seconds': 120,
                'AmountType': 'slices of'
            }
        },
        'PowerLevel': 50,
        'DefaultType': 'slices of pizza'
    },
    'brownie': {
        'Seconds': 30,
        'PowerLevel': 100,
        'DefaultType': 'a brownie'
    },
    'brownies': {
        'Amount': {
            '2': {
                'Seconds': 45,
            },
            '3': {
                'Seconds': 60,
            },
            '4': {
                'Seconds': 60,
            }
        },
        'PowerLevel': 100,
        'DefaultType': 'brownies'
    },
    'coffee': {
        'Seconds': 45,
        'PowerLevel': 100,
        'DefaultType': 'a cup of'
    },
    'tea': {
        'Seconds': 45,
        'PowerLevel': 100,
        'DefaultType': 'a cup of'
    },
    'ramen': {
        'Seconds': 180,
        'PowerLevel': 100,
        'DefaultType': 'a bowl of'
    },
    'ramen noodles': {
        'Seconds': 180,
        'PowerLevel': 100,
        'DefaultType': 'a bowl of'
    }
}

skill_id = "amzn1.ask.skill.bfe1f384-0007-438a-b30e-3f14b46196ce"

# ----------------- Helpers for the actual functionality ----------------------

insult_urls = [
    "https://s3.amazonaws.com/hark-audio/252be2a5-273b-4ef4-be71-d18e7b99b0c3.mp3", # bison's penis,
    "https://s3.amazonaws.com/hark-audio/85299a5c-f1f6-45b1-892b-12cfa2a4fa0e.mp3"  # rubber
]

def seconds_to_time(time):
    minutes = time//60
    seconds = time%60
    if minutes == 0:
        if seconds == 1:
            return '1 second'
        else:
            return str(seconds) + ' seconds'
    elif minutes == 1:
        if seconds == 0:
            return 'one minute'
        elif seconds == 1:
            return 'one minute and 1 second'
        else:
            return 'one minute and ' + str(seconds) + ' seconds'
    else:
        if seconds == 0:
            return str(minutes) + ' minutes'
        elif seconds == 1:
            return str(minutes) + ' minutes and 1 second'
        else:
            return str(minutes) + ' minutes and ' + str(seconds) + ' seconds'

# --------------- Helpers that build all of the responses ----------------------

def build_play_directive(url):
    return {
        "type": "AudioPlayer.Play",
        "playBehavior": "REPLACE_ALL",
        "audioItem": {
            "stream": {
                "url": url,
                "token": url[-1024:],
                "offsetInMilliseconds": 0
            }
        }
    }


def build_speechlet_response(should_end_session, **kwargs):
    response = {'shouldEndSession': should_end_session}

    if 'reprompt_text' in kwargs: 
        # Setting reprompt_text to None signifies that we do not want to reprompt
        # the user. If the user does not respond or says something that is not
        # understood, the session will end.
        response['reprompt'] = {'outputSpeech': {'type': 'PlainText','text': kwargs['reprompt_text']}}

    if 'outputSpeech' in kwargs:
        response['outputSpeech'] = {'type': 'PlainText', 'text': kwargs['outputSpeech']}

    if 'directive' in kwargs:
        response['directives'] = [kwargs['directive']]

    return response

def build_simple_speechlet_response(title, output, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'shouldEndSession': should_end_session
    }

def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome response"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Welcome reprompt text"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    speech_output = "End request"
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


# intent['slots'][NAME]['value']

def build_microwave_start_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Microwave Welcome"
    speech_output = "What food are you trying to microwave?"

    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Are you trying to microwave somethihng?" + \
                    "If so, please say a food."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def build_amount_response(food):
    #SESSION ATTRIBUTES
    session_attributes = {'Food': food}
    card_title = "Request Amount"

    speech_output = "How many " + FOODS_LIST[food]['DefaultType'] + \
                    " would you like to heat up?"

    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "I'm sorry, I didn't get that. " + speech_output
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def build_suggestion(speech_output):
    session_attributes = {}
    card_title = 'Microwave Suggestion'

    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    should_end_session = True
    return build_response(session_attributes, build_simple_speechlet_response(
        card_title, speech_output, should_end_session))

def get_insult(intent, session):
    session_attributes = {}
    insult_url = random.choice(insult_urls)
    return build_response(session_attributes, build_speechlet_response(True, directive=build_play_directive(insult_url)))

# --------------- Events ------------------

def log_session_start(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

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
    if intent_name == "RamsayInsultIntent":
        return get_insult(intent, session) 
    elif intent_name == "MicrowaveSuggestionIntent":
        return get_microwave_suggestion(intent, session) 
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")

def get_microwave_suggestion(intent, session):
    slots = intent['slots']
    food = ''
    if slots['Food']['value'] in FOODS_LIST:
        food = slots['Food']['value']
    elif 'Food' in session['attributes']:
        food = session['attributes']['Food']

    outputString = 'To reheat '
    foodData = FOODS_LIST[food]
    if 'value' not in slots['Amount'] or slots['Amount']['value'] is None and 'Seconds' not in foodData:
        return build_amount_response(food)
    else:
        if 'Seconds' in foodData:
            outputString += foodData['DefaultType'] + ' '
        else:
            outputString += str(slots['Amount']['value']) + ' '
        amount = slots['Amount']['value']

    if 'value' in slots['AmountType'] and slots['AmountType']['value'] is not None:
        outputString += slots['AmountType']['value'] + ' '
    elif 'Amount' in foodData and 'AmountType' in foodData['Amount'][amount]:
        outputString += foodData['Amount'][amount]['AmountType'] + ' '

    outputString += food + ', '

    powerLevel = foodData['PowerLevel']
    if powerLevel < 100:
        outputString += 'set your microwave to ' + str(powerLevel) + \
                        ' percent power and '

    if 'Seconds' in foodData:
        outputString += 'microwave it for ' + seconds_to_time(foodData['Seconds']) + '.'
    else:
        if amount == 1:
            outputString += 'microwave it for ' + seconds_to_time(foodData['Amount'][amount]['Seconds']) + '.'
        else:
            outputString += 'microwave them for ' + seconds_to_time(foodData['Amount'][amount]['Seconds']) + '.'

    return build_suggestion(outputString)


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
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        log_session_start({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        response = on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        response = on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        response = on_session_ended(event['request'], event['session'])
    else:
        response = on_session_ended(event['request'], event['session'])

    return response

