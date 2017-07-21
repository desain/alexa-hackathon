"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

import random
import time

SPICES = {
    'bitter': ["Ajwain", "Bay Leaf", "Celery", "Clove", "Cumin Seed", "Epazote", "Fenugreek Seeds",
    "Horseradish", "Juniper", "Lavender", "Mace", "Marjoram", "Oregano", "Summer Savory", "Sichuan Peppercorns",
    "Star Anise", "Turmeric", "Thyme"],
    'cooling': ["Anise",  "Fennel", "Sweet Basil"],
    'nutty': ["Ajwain", "Black Cardamom", "Coriander Seed", "Cumin Seed", "Fenugreek Seed",
    "Mustard Seed", "Poppy Seed", "Sesame Seed"],
    'sweet': ["Allspice", "Anise", "Caraway", "Cassia Cinnamon", "Chervil", "Cloves", "Dill Seed",
    "Fennel", "Green cardamom", "Nutmeg", "Poppy Seed", "Sesame Seed", "Star Anise"],
    'spicy': ["Bay Leaf", "Cassia Cinnamon", "Cloves", "Coriander", "Cumin", "Curry Leaf", "Ginger", "Marjoram", "Nutmeg"],
    'hot': ["Black Pepper", "Chiles", "Horseradish", "Mustard", "Wasabi", "White Pepper"],
    'fruity': ["Anise", "Fennel", "Nigella", "Summer Savory", "Star Anise", "Tamarind"]
}

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

# --------------- Side Dish Dummy Data --------------------

vegetable = 'vegetable'
starch = 'starch'
beans = 'beans'
soup = 'soup'
fruit = 'fruit'
caesar_salad = { 'name': 'Caesar salad', 'categories': [vegetable] }
mashed_potatoes = { 'name': 'mashed potatoes', 'categories': [starch] }
asparagus = { 'name': 'asparagus', 'categories': [vegetable] }
spinach = { 'name': 'spinach', 'categories': [vegetable] }
zucchini_and_squash = { 'name': 'zucchini and squash', 'categories': [vegetable] }
veggie_stir_fry = { 'name': 'vegetable stir fry', 'categories': [vegetable] }
green_beans = { 'name': 'green beans', 'categories': [vegetable, beans] }
curry = { 'name': 'curry', 'categories': [vegetable] }
tomato_soup = { 'name': 'tomato soup', 'categories': [vegetable, soup] }
pickled_veggies = { 'name': 'pickled vegetables', 'categories': [vegetable] }
cabbage_salad = { 'name': 'cabbage salad', 'categories': [vegetable] }
fries = { 'name': 'fries', 'categories': [starch] }
hash_browns = { 'name': 'hash browns', 'categories': [starch] }
bread_sticks = { 'name': 'bread sticks', 'categories': [starch] }
garlic_bread = { 'name': 'garlic bread', 'categories': [starch] }
peas_and_carrots = { 'name': 'peas and carrots', 'categories': [vegetable] }
refried_beans = { 'name': 'refried beans', 'categories': [beans] }
berries = { 'name': 'berries', 'categories': [fruit] }

main_to_side = {
    'lasagna': [caesar_salad, asparagus, spinach, zucchini_and_squash, green_beans, cabbage_salad, garlic_bread],
    'steak': [fries, bread_sticks, peas_and_carrots, caesar_salad],
    'salmon': [spinach, pickled_veggies, curry, veggie_stir_fry, zucchini_and_squash, asparagus],
    'tacos': [refried_beans, hash_browns],
    'pizza': [caesar_salad, bread_sticks, garlic_bread, tomato_soup]
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
            outputSpeech="Welcome to the Swiss Kitchen Knife; I know many things.",
            reprompt_test=reprompt_text))


def handle_session_end_request():
    speech_output = "End request"
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
            should_end_session=True,
            outputSpeech=speech_output))


def build_microwave_start_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    speech_output = "What food are you trying to microwave?"

    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Are you trying to microwave somethihng?" + \
                    "If so, please say a food."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
            should_end_session,
            outputSpeech=speech_output,
            reprompt_text=reprompt_text))


def build_amount_response(food):
    #SESSION ATTRIBUTES
    session_attributes = {'Food': food}

    speech_output = "How many " + FOODS_LIST[food]['DefaultType'] + \
                    " would you like to heat up?"

    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "I'm sorry, I didn't get that. " + speech_output
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
            should_end_session,
            outputSpeech=speech_output,
            reprompt_text=reprompt_text))

################ SPICE SUGGESTER CODE ###################

def set_ingredient_in_session(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """

    session_attributes = {}
    should_end_session = False

    if 'Foodone' in intent['slots'] and 'Foodtwo' in intent['slots']:
        ingredient1 = intent['slots']['Foodone']['value']
        ingredient2 = intent['slots']['Foodtwo']['value']
        # session_attributes = create_ingredients_attributes(ingredients, session)
        speech_output = get_output_with_spices([ingredient1, ingredient2])
        reprompt_text = ". You can ask me for spice suggestions by saying, " \
                        "what spices do I use"
    else:
        speech_output = "I'm not sure what your ingredient is. " \
                        "Please try again."
        reprompt_text = "I'm not sure what your ingredient is. " \
                        "You can tell me your ingredients by saying, " \
                        "add dash to my ingredients"
    return build_response(session_attributes, build_speechlet_response(
            should_end_session,
            outputSpeech=speech_output,
            reprompt_text=reprompt_text))

def get_output_with_spices(tastes):
    session_output = ""
    random.seed(time.time())

    for taste in tastes:
         session_output += "Use " + SPICES[taste][random.randint(0, len(SPICES[taste])-1)] + " for a " + taste + " taste, "
    return session_output

################ SPICE SUGGESTER CODE ###################

def build_suggestion(speech_output):
    session_attributes = {}

    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(
            should_end_session,
            outputSpeech=speech_output))

def get_insult(intent, session):
    session_attributes = {}
    insult_url = random.choice(insult_urls)
    return build_response(session_attributes, build_speechlet_response(True, directive=build_play_directive(insult_url)))


def get_ingredient_from_session(intent, session):
    session_attributes = {}
    should_end_session = True
    reprompt_text = None

    if 'ListOfIngredients' in intent['slots']:
        if intent['slots']['ListOfIngredients']['value'] == "sugar":
            speech_output = "1 cup of sugar can be substituted with 3/4 cup corn syrup."
        
        elif intent['slots']['ListOfIngredients']['value'] == "flour":
            speech_output = "1 cup of flour can be substituted with 1 cup of rolled oats."
        
        elif intent['slots']['ListOfIngredients']['value'] == "eggs":
            speech_output = "1 egg can be substituted with 3 tablespoons of mayonnaise."
        
        elif intent['slots']['ListOfIngredients']['value'] == "rice":
            speech_output = "1 cup of rice can be replaced by 1 cup of cooked barley."
        
        elif intent['slots']['ListOfIngredients']['value'] == "butter":
            speech_output = "A cup of butter can be substituted with a cup of margarine."
        
        elif intent['slots']['ListOfIngredients']['value'] == "baking soda":
            speech_output = "1 teaspoon of baking soda can be substituted with 4 teaspoons of baking powder."
        
        elif intent['slots']['ListOfIngredients']['value'] in ("red pepper flakes", "red pepper")
            speech_output = "Red pepper can be substituted with black pepper"

        return build_response({}, build_speechlet_response(
            should_end_session,
            outputSpeech=speech_output))

        
def get_main_dish(intent, session):
    session_attributes = {}

    if session.get('attributes', {}) and "mainDish" in session.get('attributes', {}):
        main_dish = session['attributes']['mainDish']
        speech_output = "You're looking for a side dish for " + main_dish + \
                        ", right?"
    else:
        speech_output = "Okay, let's make something tasty. What is the main dish?"
    
    reprompt_text = "Sorry, I didn't catch that. What is the main dish?"
    should_end_session = False
    
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))
        
        
# Sets the main dish in the session
def set_main_dish(intent, session):
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'MainDish' in intent['slots']:
        main_dish = intent['slots']['MainDish']['value']
        session_attributes = { "mainDish" : main_dish }
        side_dishes = get_side_dishes_for(main_dish)
        session_attributes['sideDishes'] = side_dishes
        speech_output = "I have " + str(len(side_dishes)) + " suggestions for " \
                        + main_dish + \
                        ". Would you like to filter them by a category?"
        reprompt_text = "would you like to filter them by category? You can " \
                        "also hear all the suggestions by saying, all."
    else:
        speech_output = "I didn't catch what the main dish is. " \
                        "Would you say it again?"
        reprompt_text = speech_output
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        
def get_filter_category(intent, session):
    session_attributes = session.get('attributes', {})
    should_end_session = False
    speech_output = "Alright, are you looking for a vegetable, starch, beans, " \
                    "soup, fruit, or something else?"
    reprompt_text = speech_output
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))
        
# Creates a sublist of all the side dishes for the user based on a specified category
def filter_by_category(intent, session):
    session_attributes = session.get('attributes', {})
    should_end_session = False
    if 'MainDish' in intent['slots']:
        main_dish = intent['slots']['MainDish']['value']
        session['attributes']['mainDish'] = main_dish
    if 'Category' in intent['slots']:
        category = intent['slots']['Category']['value']
        session['attributes']['category'] = category
    if "mainDish" in session_attributes:
        main_dish = session['attributes']['mainDish']
        if "sideDishes" not in session_attributes:
            side_dishes = get_side_dishes_for(main_dish)
            if side_dishes == None:
                return build_response(session_attributes, build_speechlet_response(
                    intent['name'], "Sorry, I don't know about that dish.", None, True))
        else:
            side_dishes = session['attributes']['sideDishes']
        session_attributes['sideDishes'] = side_dishes
        if 'Category' in intent['slots']:
            category = intent['slots']['Category']['value']
            session_attributes['category'] = category
            filtered_side_dishes = get_sides_for_category(side_dishes, category)
            if len(filtered_side_dishes) == 0:
                del session_attributes['category']
                speech_output = "Sorry, it looks like there are no " + category \
                                + " side dishes. Try a different category by saying " \
                                "something like, I want a starch on the side."
            else:
                session_attributes['filteredSideDishes'] = filtered_side_dishes
                speech_output = "Okay, I have " + str(len(filtered_side_dishes)) \
                                + " " + category + " suggestions. " \
                                "Would you like to hear them all?"
        else:
            speech_output = "Sorry, I didn't get the category filter. You can say, " \
                            "I want a vegetable side dish."
    else:
        speech_output = "I'm not sure what your main dish is. " \
                        "You can say, the main dish is salmon."
    reprompt_text = speech_output

    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

# Returns the list of dishes associated with the given dish
def get_side_dishes_for(main_dish):
    # Find all side dishes mapped to the main dish
    return main_to_side.get(main_dish, None)

# Returns the sublist of side dishes that are included in the given category
def get_sides_for_category(side_dishes, category):
    filtered_list = []
    for dish in side_dishes:
        if category in dish['categories']:
            filtered_list.append(dish)
    return filtered_list

# Removes the category filter if it exists
def remove_filter(intent, session):
    session_attributes = session.get('attributes', {})
    should_end_session = False

    if "mainDish" in session_attributes:
        main_dish = session['attributes']['mainDish']
        if "sideDishes" not in session_attributes:
            side_dishes = get_side_dishes_for(main_dish)
        else:
            side_dishes = session['attributes']['sideDishes']
        session_attributes['sideDishes'] = side_dishes
        if session_attributes['category']:
            category = session_attributes['category']
            del session_attributes['category']
            speech_output = "Okay, a " + category + " side dish is overrated. "
        else:
            speech_output = ""
        if session_attributes['filteredSideDishes']:
            del session_attributes['filteredSideDishes']
        speech_output += "Would you like to filter by a different category?"
    else:
        speech_output = "I'm not sure what your main dish is. " \
                        "You can say, the main dish is lasagna."
    reprompt_text = speech_output
    session_attributes['madeSuggestion'] = false

    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

def get_suggestion(intent, session):
    session_attributes = session.get('attributes', {})
    session_attributes['madeSuggestion'] = False
    should_end_session = False

    if "mainDish" in session_attributes:
        main_dish = session['attributes']['mainDish']
        if "sideDishes" not in session_attributes:
            side_dishes = get_side_dishes_for(main_dish)
        else:
            side_dishes = session['attributes']['sideDishes']
            
        session_attributes['sideDishes'] = side_dishes
        if "category" in session_attributes and "filteredSideDishes" in session_attributes:
            if len(session_attributes) > 1:
                suggestion = get_random_suggestion(session_attributes['filteredSideDishes'])
                session_attributes['madeSuggestion'] = True
                session_attributes['lastSuggestion'] = suggestion
                category = session_attributes['category']
                speech_output = "Okay, here is one suggestion from the " + category + " category: " \
                                + suggestion['name'] + " goes well with " + main_dish \
                                + ". Does that sound good?"
            else:
                speech_output = "Sorry, I ran out of suggestions."
                should_end_session = True
        else:
            if len(side_dishes) > 1:
                suggestion = get_random_suggestion(side_dishes)
                speech_output = "Here is a suggestion... " + suggestion['name'] + " goes " \
                                "well with " + main_dish + ". Does that sound good?"
            else:
                speech_output = "Sorry, I ran out of suggestions."
                should_end_session = True
    else:
        speech_output = "I'm not sure what your main dish is. " \
                        "You can say, the main dish is tacos."
    reprompt_text = speech_output

    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

# Returns a single side dish from the list of suggestions
# Assumes the list has length >= 1
def get_random_suggestion(suggestions):
    return random.sample(suggestions, 1)[0]

# Recites all suggestions (filtered or not) to the user    
def get_all_suggestions(intent, session):
    session_attributes = session.get('attributes', {})
    session_attributes['madeSuggestion'] = False
    should_end_session = False

    if "mainDish" in session_attributes:
        main_dish = session['attributes']['mainDish']
        if "sideDishes" not in session_attributes:
            side_dishes = get_side_dishes_for(main_dish)
        else:
            side_dishes = session['attributes']['sideDishes']
            
        session_attributes['sideDishes'] = side_dishes
        if "category" in session_attributes and "filteredSideDishes" in session_attributes:
            suggestions = session_attributes['filteredSideDishes']
            speech_output = "Okay, here are all the " + session_attributes['category'] + " suggestions: "
        else:
            suggestions = side_dishes
            speech_output = "Okay, here are all " + str(len(suggestions)) + " suggestions: "
        for side_dish in suggestions:
            speech_output += (side_dish['name'] + ", ")
        speech_output += " and whatever you like. Did something sound good?"
        reprompt_text = "Did something sound good?"
        session_attributes['madeSuggestion'] = True
    else:
        speech_output = "I'm not sure what your main dish is. " \
                        "You can say, the main dish is steak."
        reprompt_text = speech_output

    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

def yes(intent, session):
    session_attributes = session.get('attributes', {})

    if "madeSuggestion" in session_attributes and session_attributes["madeSuggestion"] is True:
        return build_response(session_attributes, build_speechlet_response(
            intent['name'], "Glad I could help!", None, True))
    elif "category" in session_attributes:
        intent['name'] = "GetAllSuggestionsIntent"
        return get_all_suggestions(intent, session)
    elif "mainDish" in session_attributes:
        intent['name'] = "FilterByCategoryIntent"
        return get_filter_category(intent, session)
    else:
        intent['name'] = "SideDishIntent"
        return get_main_dish(intent, session)

def no(intent, session):
    session_attributes = session.get('attributes', {})

    if "madeSuggestion" in session_attributes and session_attributes["madeSuggestion"] is True:
        if "lastSuggestion" in session_attributes:
            remove_last_suggestion(session_attributes)
            session['attributes'] = session_attributes
            intent['name'] = "GetSuggestionIntent"
            return get_suggestion(intent, session)
        elif "category" in session_attributes:
            intent['name'] = "RemoveFilterIntent"
            return remove_filter(intent, session)
        else:
            return build_response(session_attributes, build_speechlet_response(
                intent['name'], "I'm sorry I didn't have better options.", None, True))
    elif "mainDish" in session_attributes:
        intent['name'] = "GetSuggestionIntent"
        return get_suggestion(intent, session)
    else:
        intent['name'] = "SideDishIntent"
        return get_main_dish(intent, session)

# Removes the last suggestion made in the session from all stored lists        
def remove_last_suggestion(session_attributes):
      bad_suggestion = session_attributes['lastSuggestion']
      session_attributes['sideDishes'].remove(bad_suggestion)
      if 'category' in session_attributes:
          session_attributes['filteredSideDishes'].remove(bad_suggestion)
      del session_attributes["lastSuggestion"]
      return
            
            
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
    if intent_name == "GetIngredientSuggestion":
        return get_ingredient_from_session(intent, session)
    elif intent_name == "RamsayInsultIntent":
        return get_insult(intent, session)
    elif intent_name == "MicrowaveSuggestionIntent":
        return get_microwave_suggestion(intent, session)
    elif intent_name == "GetIngredientsIntent":
        return set_ingredient_in_session(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    elif intent_name == "SideDishIntent":
        return get_main_dish(intent, session)
    elif intent_name == "MyMainDishIsIntent":
        return set_main_dish(intent, session)
    elif intent_name == "FilterByCategoryIntent":
        return filter_by_category(intent, session)
    elif intent_name == "RemoveFilterIntent":
        return remove_filter(intent, session)
    elif intent_name == "GetSuggestionIntent":
        return get_suggestion(intent, session)
    elif intent_name == "GetAllSuggestionsIntent":
        return get_all_suggestions(intent, session)
    elif intent_name == "YesIntent":
        return yes(intent, session)
    elif intent_name == "NoIntent":
        return no(intent, session)
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
