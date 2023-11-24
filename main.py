from seleniumwire import webdriver  # Import from seleniumwire
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time, json, random, string
from print_color import print
from dotenv import dotenv_values
from pymongo import MongoClient

config = dotenv_values(".env")

### set MOZ_HEADLESS=1 env if you want to headless

EMAIL = config['EMAIL']
PASSWORD = config['PASSWORD']

try:
    mongodb_client = MongoClient(config["ATLAS_URI"])
    database = mongodb_client[config["DB_NAME"]]
    print('Connected to DB!', tag='success', tag_color='green', color='white', format='bold')
except:
    print('Error while connecting to MongoDB', tag='success', tag_color='error', color='white', format='bold')

### args:
### id - id of word to translate
### returns translation
def getWord(id):
    return database['answers'].find_one({}, {id:1})[id]

### returns id of last word
def lastWord(): 
    word_requests = []
    
    for request in driver.requests:
        if 'next_word' in request.url:
            my_json = request.response.body.decode('utf8')
            data = json.loads(my_json)
            word_requests.append(data)

    return word_requests[-1]

wire_options = {
    'disable_encoding': True  # Ask the server not to compress the response
}

driver = webdriver.Firefox(seleniumwire_options=wire_options)
driver.get("https://instaling.pl/teacher.php?page=login")
assert "Insta.Ling" in driver.title

def log_in():
    email_field = driver.find_element(By.ID, 'log_email')
    pass_field = driver.find_element(By.ID, 'log_password')
    login_btn = driver.find_elements(By.CLASS_NAME, 'btn-primary')[1]

    email_field.send_keys(EMAIL)
    pass_field.send_keys(PASSWORD)
    try:
        login_btn.click()
        print('Logged in!', tag='success', tag_color='green', color='white', format='bold')
    except:
        print('Error while logging in', tag='error', tag_color='red', color='white', format='bold')
        driver.close()
        quit()

def start_session():
    driver.find_elements(By.CLASS_NAME, "btn")[0].click() # przycisk "zacznij codzienną sesję"
    time.sleep(1)
    try:
        driver.find_elements(By.ID, "start_session_button")[0].click() # przycisk "zacznij swoją codzienną sesję"
        print('Started new session!', tag='info', tag_color='blue', color='white', format='bold')
    except:
        driver.find_elements(By.ID, "continue_session_button")[0].click() # przycisk "kontynuuj sesję"
        print('Continuing session', tag='info', tag_color='blue', color='white', format='bold')

def answerWord(word):
    ## pytanie
    try:
        answer_input = driver.find_element(By.ID, "answer")
        answer_btn = driver.find_element(By.ID, "check")
        next_btn = driver.find_element(By.ID, "next_word")

        know_new_btn = driver.find_element(By.ID, 'know_new')
        try:
            know_new_btn.click()
            time.sleep(3)
            skip_btn = driver.find_element(By.ID, 'skip')
            time.sleep(3)             ### TODO: use assert instead of time.sleep()???
            skip_btn.click()
            time.sleep(2)
        except:
            print('No need to answer about new word', tag='warn', tag_color='yellow', color='white', format='bold')
        
        try:
            answer_input.send_keys(word)
            answer_btn.click()
        except:
            print("Can't answer question", tag='error', tag_color='red', color='white', format='bold')
        print(f'Answered question: {word}', tag='info', tag_color='blue', color='white', format='bold')
        time.sleep(2)

        result = driver.find_element(By.ID, 'answer_result')
        if result.text == 'Dobrze':
            print('Correct answer!\n', tag='success', tag_color='green', color='white', format='bold')
            next_btn.click()
            print('Next question', tag='info', tag_color='blue', color='white', format='bold')
            return 1
        else:
            print('Bad answer!\n', tag='error', tag_color='red', color='white', format='bold')
            next_btn.click()
            print('Next question', tag='info', tag_color='blue', color='white', format='bold')
            return 0
    except:
        print("Error: can't answer question", tag='error', tag_color='red', color='white', format='bold')
        driver.close()
        quit()

def makeTypo(word):
    char_to_replace = word[random.randint(0, len(word)-1)]
    new_word = word.replace(char_to_replace, ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase)))
    print('Made a typo!', tag='warn', tag_color='yellow', color='white', format='bold')
    return new_word

log_in()
start_session()
time.sleep(3)

correct_answers = 0
typos = 0

while True: ## session loop
    if random.randint(1, 12) == 7: ### 8.33% chance of making a typo:  (1/12)*100% = 0.0833*100% = 8.33% around
        try:
            if answerWord(makeTypo(getWord(lastWord()['id']))) == 1: 
                correct_answers += 1
                typos += 1
        except:
            print('Finished session!', tag='success', tag_color='green', color='white', format='bold')
            print('Stats:', color='white', format='bold')
            print(f'Corrects answers: {correct_answers}', color='green', format='bold')
            print(f'Bad answers: {20-correct_answers}', color='red', format='bold')
            print(f'Mispelling: {typos}', color='yellow', format='bold')
            driver.close()
            quit()
        time.sleep(random.randint(1, 4))
    else:
        try:
            if answerWord(getWord(lastWord()['id'])) == 1: correct_answers += 1
        except:
            print('Finished session!', tag='success', tag_color='green', color='white', format='bold')
            print('Stats:', color='white', format='bold')
            print(f'Corrects answers: {correct_answers}', color='green', format='bold')
            print(f'Bad answers: {20-correct_answers}', color='red', format='bold')
            print(f'Mispelling: {typos}', color='yellow', format='bold')
            driver.close()
            quit()
        time.sleep(random.randint(2, 7))

# Closing file
f.close()
driver.close()