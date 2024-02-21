import os
import random
import sqlite3

from flask import Flask, flash, render_template, request, session, redirect, Markup
import string


# Check if the application should run locally or in docker, to run locally set is_local to True:
is_local = True

# Set the environment variable based on the mode:
if is_local:
    os.environ['PATH_TO_DATABASE'] = "dictionary.db"
    os.environ['APP_URL'] = "http://localhost:8000"  # Local/Docker  URL
else:
    os.environ['APP_URL'] = "https://urban-spelling-bee.fly.dev"  # Deployed app URL


app = Flask(__name__, static_folder='static')
app.secret_key = 'secret key'
app.config['SESSION_COOKIE_MAX_SIZE'] = 6000

@app.route('/', methods=['GET'])
def index_get():

    # Create the wordlist database
    create_wordlist_table()

    random_seven = session.get('random_seven')  # Retrieve random_seven from the session

    if random_seven is None:
        generate_random_seven()
        random_seven = session['random_seven']

    b1 = random_seven[0]
    b2 = random_seven[1]
    b3 = random_seven[2]
    b4 = random_seven[3]
    b5 = random_seven[4]
    b6 = random_seven[5]
    b7 = random_seven[6]

    # b1 is required to be in the word:

    words_results = []

    conn = sqlite3.connect(os.environ['PATH_TO_DATABASE'])
    c = conn.cursor()

    # append only the words from the database that can be constructed using no letter that is contained in random_rest:
    database_query = c.execute("SELECT word FROM entries")
    for row in database_query:
        try:
            word_letters = set(row[0])
            if word_letters.issubset(set(random_seven)):
                words_results.append(row[0])
        except TypeError:
            print(f"Error processing row: {row}")
    session['words_results'] = words_results

    conn.close()
    your_score = 0
    words = []
    conn = sqlite3.connect(os.environ['PATH_TO_DATABASE'])
    c = conn.cursor()

    c.execute("SELECT word FROM wordlist")
    word_rows = c.fetchall()
    
    for row in word_rows:
        word = get_word_from_wordlist(row[0])
        if word:
            words.append(word)
            your_score += highscore(word)
            if is_pangram(word):
                your_score += 100
    conn.close()

    return render_template('index.html', random_seven=random_seven, words_results=words_results, b1=b1, b2=b2, b3=b3, b4=b4, b5=b5, b6=b6, b7=b7, definition=session.get('definition'), word=session.get('word'), words=words, your_score=your_score)

@app.route('/', methods=['POST'])
def index_post():
    if session.get('random_seven') is None:
        generate_random_seven()
    random_seven = session.get('random_seven')
    term = request.form.get("term")
    session['term'] = term

    words_results = session.get('words_results')
    if len(term) < 4:
        flash(f"Word must be at least 4 letters long 😬", "error")
        return redirect("/")
    if random_seven[0] not in term:
        flash(f"Word must contain center letter ' {random_seven[0]} '☝🏼", "error")
        return redirect("/")
    if term not in words_results:
        flash(f"{term} was not found in the dictionary 🤔", "error")
        return redirect("/")
    if get_word_from_wordlist(term):
        flash(f"The word {term} was already found ✅", "error")
        return redirect("/")
    if is_pangram(term):
        flash(f"Nice! You found a pangram! 🐝", "success")
        insert_word_and_points(term)
        return redirect("/")

    insert_word_and_points(term)
    get_definition(term)
    get_word_from_wordlist(term)

    session['definition'] = get_definition(term)
    definition = session.get('definition')
    session['word'] = get_word_from_wordlist(term)

    # Define Python variables
    wordToShare = session.get('word')
    definitionToShare = session.get('definition')

    # Generate the share button HTML using Python variables
    share_button_html = f'''
    <button id='buttonCopyOrShareWordDef' type='button'>Text</button>
    <script>
      function setupCopyOrShareButton(buttonId, clickHandler) {{
        const button = document.getElementById(buttonId);
        const action = navigator.share ? ' 📤' : '📥';

        button.innerHTML = action;
        button.addEventListener('click', clickHandler);
      }}

      // Copy or share a specific word and its definition:
      function eitherCopyOrShareWordDef() {{
        const wordToShare = "{wordToShare}";
        const definitionToShare = "{definitionToShare}";
        const textToShare = `I found "{wordToShare}" which has the definition "{definitionToShare}".`;

        if (navigator.share) {{
          navigator.share({{
              text: textToShare
          }});
        }} else {{
          navigator.clipboard.writeText(textToShare);
        }}
      }}

      setupCopyOrShareButton('buttonCopyOrShareWordDef', eitherCopyOrShareWordDef);
    </script>
    '''

    # Wrap the success message in Markup to avoid HTML escaping
    success_message = Markup(f"The word {wordToShare} was found 🤘 \n Definition: '{definitionToShare}' {share_button_html}")
    flash(success_message, "success")

    return redirect("/")


def create_wordlist_table():
    conn = sqlite3.connect(os.environ['PATH_TO_DATABASE'])
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS wordlist (word TEXT, score INTEGER);
    ''')

    conn.commit()
    conn.close()

def insert_word_and_points(term):
    conn = sqlite3.connect(os.environ['PATH_TO_DATABASE'])
    c = conn.cursor()

    # Check if the word already exists in the table
    c.execute("SELECT * FROM wordlist WHERE word=?", (term,))
    existing_row = c.fetchone()
    if existing_row:
        print(f"The word '{term}' already exists in the database.")
    else:
        score = highscore(term)
        if is_pangram(term):
            score += 100
        # Insert a word and its points into the table
        c.execute('INSERT INTO wordlist VALUES (?, ?)', (term, score))

    conn.commit()
    conn.close()


def generate_random_seven():
    vowels = ['A', 'E', 'I', 'O', 'U']
    
    # Generate random_seven if it's not already in the session
    alphabet = string.ascii_uppercase

    random_seven = random.sample(alphabet, 7)
    # check if there is at least two vowels in the random_seven:
    if len(set(random_seven).intersection(vowels)) < 2:
        return generate_random_seven()
    print(f"random_seven is {random_seven}")

    # random_rest = list(set(alphabet) - set(random_seven))
    # print(f"random_rest is {random_rest}")
    
    session['random_seven'] = random_seven
    # session['random_rest'] = random_rest


@app.route('/regenerate', methods=['POST'])
def generate():
    generate_random_seven()
    delete_all_words()
    clear_session()
    return redirect("/")


 # get the definition of term from the table entries if term is in words_results:
def get_definition(term):
    print(f"term is {term}")
    # get the definition from the database:
    conn = sqlite3.connect(os.environ['PATH_TO_DATABASE'])
    c = conn.cursor()

    c.execute("SELECT definition FROM entries WHERE word=?", (term,))
    definition = c.fetchone()
    if definition:
        # slice the definition from the tuple:
        definition = definition[0]
    else:
        definition = None
    conn.close()
    print(definition)
    return definition

def get_word_from_wordlist(term):

    print(f"term is {term}")
    conn = sqlite3.connect(os.environ['PATH_TO_DATABASE'])
    c = conn.cursor()

    c.execute("SELECT word FROM wordlist WHERE word=?", (term,))
    word = c.fetchone()
    if word:
        # slice the word from the tuple:
        word = word[0]
    else:
        word = None

    conn.close()
    return word

def delete_all_words():
    conn = sqlite3.connect(os.environ['PATH_TO_DATABASE'])
    c = conn.cursor()

    c.execute("DELETE FROM wordlist")

    conn.commit()
    conn.close()

def clear_session():
    session['random_seven'] = None
    session['term'] = None
    session['definition'] = None
    session['word'] = None


def highscore(word):

    points = 0

    letter_scores = {
            "A": 1, "E": 1, "I": 1, "O": 1, "U": 1, "L": 1, "N": 1, "S": 1, "T": 1, "R": 1,
            "D": 2, "G": 2,
            "B": 3, "C": 3, "M": 3, "P": 3,
            "F": 4, "H": 4, "V": 4, "W": 4, "Y": 4,
            "K": 5,
            "J": 8, "X": 8,
            "Q": 10, "Z": 10
        }

    points = sum(letter_scores.get(letter, 0) for letter in word)

    return points

def is_pangram(term):
    random_seven = session.get('random_seven')
    return all(char in term for char in random_seven)


@app.route('/screencast', methods=['GET'])
def screencast_get():
    return render_template('screencast.html')

