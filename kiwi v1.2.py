import speech_recognition as sr
import pyttsx3
import openai
import wikipedia

# Set up OpenAI API key
openai.api_key = "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"

# Set up Pyttsx3 module
engine = pyttsx3.init('espeak')
voices = engine.getProperty('voices')
engine.setProperty('voice', 'english+f4')
engine.setProperty('rate', 120)

# Set up speech recognizer and microphone
r = sr.Recognizer()
mic = sr.Microphone()

# Set up conversation variables
USER_NAME = 'user'
BOT_NAME = 'kiwi'
conversation = ''

# Say "exhicuting kiwi" on startup
engine.say("exhicuting kiwi")
engine.runAndWait()

# Define function to get a response from OpenAI
def get_response(prompt):
    response = openai.Completion.create(
        model='text-davinci-003',
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    response_str = response.choices[0].text.replace('\n', '')
    response_str = response_str.split(USER_NAME + ':', 1)[0].split(BOT_NAME + ':', 1)[0]
    return response_str

# Define function to get a summary from Wikipedia
def get_wikipedia_summary(query):
    try:
        summary = wikipedia.summary(query, sentences=2)
    except wikipedia.exceptions.DisambiguationError as e:
        summary = f"Sorry, I found multiple results. Please be more specific."
    except wikipedia.exceptions.PageError as e:
        summary = f"Sorry, I couldn't find anything on Wikipedia for that."
    return summary

# Main loop
while True:
    with mic as source:
        print('\nListening...')
        r.adjust_for_ambient_noise(source, duration=0.2)
        audio = r.listen(source)
    print('No longer listening')

    try:
        user_input = r.recognize_google(audio)
        print(f'{USER_NAME}: {user_input}')  # display user input in terminal
    except sr.UnknownValueError as e:
        continue

    if 'halt' in user_input.lower():
            print('shutting down kiwi')  # shut down bot
            engine.say('shutting down kiwi')
            engine.runAndWait()
            break

    if 'wikipedia' in user_input.lower():
            query = user_input.lower().replace('wikipedia', '')
            summary = get_wikipedia_summary(query)
            response_str = summary
            print(f'{wikipedia}: {response_str}')  # Display Wikipedia response in terminal

    else:
            prompt = f'{USER_NAME}: {user_input}\n{BOT_NAME}: '
            conversation += prompt
            response_str = get_response(conversation)
            conversation += response_str + '\n'
            print(f'{BOT_NAME}: {response_str}')  # Display bot's response in terminal

    engine.say(response_str)
    engine.runAndWait()
