

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
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
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }   

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to ingredient helper. " 
                    
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please tell me the ingredient you need to substitute"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])
          
def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you, have a nice day."
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()

def get_ingredient_from_session(intent, session):
    card_title = suggestIngredient
    session_attributes = {}
    should_end_session = True
    reprompt_text = None
    
    if 'ListOfIngredients' in intent['slots']:
        if intent['slots']['ListOfIngredients']['value'] == "sugar":
            speech_output = "1 cup of sugar can be substituted with 3/4 cup corn syrup."
            return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))
        
        elif intent['slots']['ListOfIngredients']['value'] == "flour":
            speech_output = "1 cup of flour can be substituted with 1 cup of rolled oats."
            return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))
        
        elif intent['slots']['ListOfIngredients']['value'] == "eggs":
            speech_output = "1 egg can be substituted with 3 tablespoons of mayonnaise."
            return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))
        
        elif intent['slots']['ListOfIngredients']['value'] == "rice":
            speech_output = "1 cup of rice can be replaced by 1 cup of cooked barley."
            return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))
        
        elif intent['slots']['ListOfIngredients']['value'] == "butter":
            speech_output = "A cup of butter can be substituted with a cup of margarine."
            return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))
        
        elif intent['slots']['ListOfIngredients']['value'] == "baking soda":
            speech_output = "1 teaspoon of baking soda can be substituted with 4 teaspoons of baking powder."
            return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))
        
            


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "GetIngredientSuggestion":
        return get_ingredient_from_session(intent, session)
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


def lambda_handler(event, context):
    
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])
          
    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])

