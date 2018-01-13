from __future__ import print_function
from bittrex.bittrex import Bittrex, API_V2_0

# -----Constant-----

acronymMap = {"bitcoin":"BTC", "litecoin":"LTC", "verge":"XVG",
"ripple":"XRP", "ethereum":"ETH", "omise go":"OMG",
"siacoin":"SC", "digital note":"XDN", "cardano":"ADA",
"stellar":"XLM", "dogecoin":"DOGE", "q tum":"QTUM",
"z classic":"ZCL", "redd coin":"RDD", "lisk":"LSK",
"status":"SNT", "burst":"BURST", "triggers":"TRIG",
"neo":"NEO", "nexus":"NXS", "ardor":"ARDR",
"black coin":"BLK", "nem":"XEM", "next":"NXT",
"ethereum classic":"ETC", "power ledger":"POWR",
"stratis":"STRAT", "metal":"MTL", "steem":"STEEM",
"ten x":"PAY", "fun fair":"FUN", "unikoin gold":"UKG",
"enigma":"ENG", "ripio credit network":"RCN", "lunyr":"LUN",
"z cash":"ZEC", "bitcoin gold":"BTG", "monero":"XMR",
"dash":"DASH", "bitbean":"BITB", "ubiq":"UBQ",
"waves":"WAVES", "einsteinium":"EMC2", "vertcoin":"VTC",
"ad token":"ADT", "civic":"CVC", "syscoin":"SYS",
"komodo":"KMD", "basic attention token":"BAT",
"edgeless":"EDG", "salt":"SALT", "golem":"GNT",
"e boost":"EBST", "ark":"ARK", "storj":"STORJ",
"hemp coin":"THC", "ad ex":"ADX", "myriad":"XMY",
"lomocoin":"LMC", "co found dot it":"CFI", "first blood":"1ST",
"gnosis":"GNO", "match pool":"GUP",
"music coin":"MUSIC", "block tix":"TIX", "decentraland":"MANA",
"rise":"RISE", "groestlcoin":"GRS", "expanse":"EXP",
"humaniq":"HMQ", "verium reserve":"VRM", "patientory":"PTOY",
"augur":"REP", "viberate":"VIB", "synereo":"AMP",
"sphere":"SPHR", "monetary unit":"MUE", "mona coin":"MONA",
"okay cash":"OK", "counter party":"XCP", "folding coin":"FLDC",
"spread coin":"SPR", "game credits":"GAME", "z coin":"XZC",
"steem dollars":"SBD", "pot coin":"POT", "salus":"SLS",
"geo coin":"GEO", "factom":"FCT", "decent":"DCT",
"cannabis coin":"CANN", "nav coin":"NAV", "feather coin":"FTC",
"internet of people":"IOP", "nubits":"NBT", "wings":"WINGS",
"breakout stake":"BRX", "radium":"RADS", "viacoin":"VIA",
"numeraire":"NMR", "unbreakable coin":"UNB", "pink coin":"PINK",
"elastic":"XEL", "mercury":"MER"}
bittrex = Bittrex(None, None)


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
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
    speech_output = "Welcome to the cryptocurrency checker.  " \
                    "Please say the name of the coin you want to know the " \
                    "price of.  For example, you could say bitcoin."
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please say the name of the coin you want to know the " \
                    "price of.  For example, you could say: bitcoin."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Good luck with your investments!"
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def create_favorite_color_attributes(theCoin):
    return {"theCoin": theCoin}

## Retrieves the current price of the selected cryptocurrency
## in both USD and Satoshis.

def getValueFromSession(intent, session):
    card_title = "Price Retrieval"
    sessionAttributes = {}
    repromptText = None
    try:
        theCoin = intent['slots']['Coin']['value']
    except KeyError:
        theCoin = "";
    if theCoin != "" and theCoin in acronymMap:

        ## Gets the price of bitcoin in usd

        btcPrice = bittrex.get_ticker("USDT-BTC")["result"]["Ask"]

        ## If the coin is not BTC, gets the price of the coin in terms
        ## of BTC for later conversion to dollars

        if theCoin != "bitcoin":
            nestedMaps = bittrex.get_ticker("BTC-" + acronymMap[theCoin])
            askingPrice = nestedMaps["result"]["Ask"]
            dollars = round(askingPrice*btcPrice, 2)
            satoshis = str(askingPrice*(10**8)).split(".")[0]
        else:
            dollars = btcPrice
        dollarValue = str(dollars).split(".")[0]
        centValue = str(dollars).split(".")[1]
        if dollars > 2:
            speech_output = ("The value of " + theCoin + " is: "
                            + dollarValue + " dollars and " + centValue
                            + " cents.  You can ask about a different coin or "
                            + "you can end the session by saying end.")
        elif round(dollars) == 0:
            speech_output = ("The value of " + theCoin + " is "
                            + centValue + " cents or " + satoshis
                            + " Satoshis.  You can ask about a different coin or "
                            + "you can end the session by saying end.")
        else:
            speech_output = ("The value of " + theCoin + " is "
                            + dollarValue + " dollars and " + centValue
                            + " cents or "+ satoshis
                            + " Satoshis.  You can ask about a different coin or "
                            + "you can end the session by saying end.")

            reprompt_text = ("You can ask me the price of a coin by just saying "
                            + " its name.  For example, you could say: bitcoin.")
        should_end_session = False
    else:
        speech_output = ("I have never heard of that coin.  "
                        + "You can say a different coin by saying its name, or"
                        " you can end the session by saying end.")
        reprompt_text = "Please say the name of the coin you want to know the " \
                        "price of.  For example, you could say: bitcoin."
        should_end_session = False
    return build_response(sessionAttributes, build_speechlet_response(
        card_title, speech_output, repromptText, should_end_session))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
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
    if intent_name == "GetCoinPriceIntent":
        return getValueFromSession(intent, session)
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
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
