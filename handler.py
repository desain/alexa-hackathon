"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

import random

skill_id = "amzn1.ask.skill.bfe1f384-0007-438a-b30e-3f14b46196ce"

# ----------------- Helpers for the actual functionality ----------------------

insult_urls = [
    "https://s3.amazonaws.com/hark-audio/252be2a5-273b-4ef4-be71-d18e7b99b0c3.mp3", # bison's penis,
    "https://s3.amazonaws.com/hark-audio/85299a5c-f1f6-45b1-892b-12cfa2a4fa0e.mp3"  # rubber
]

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
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    return build_response(session_attributes, build_speechlet_response(
            should_end_session,
            outputSpeech="Hi! You can ask me what Gordon Ramsay would think about your food",
            reprompt_test=reprompt_text))


def handle_session_end_request():
    speech_output = "End request"
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


# intent['slots'][NAME]['value']



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
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
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

