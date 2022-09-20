from flask import Flask, request, redirect, escape, send_from_directory
import secrets
import random
import sqlite3
import qrcode
from os.path import exists


app = Flask(__name__)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static/favicon.ico')

@app.route('/serviceworker.js', methods=['GET'])
def sw():
    return app.send_static_file('static/serviceworker.js')

def create_short(quantity):
    text = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    random_string = ''
    for _ in range(quantity):
        random_string = random_string + secrets.choice(text)
    return random_string

def qrcode_gen(url):
    img = qrcode.make(url)
    file_name = create_short(4) + ".png"
    if exists(file_name):
        qrcode_gen()
    img.save('static/' + file_name)
    return file_name


@app.route("/")
def index_redirect():
    return redirect("https://tools.omni-tek.org/shorten", code=302)

@app.route("/shorten", methods=['GET', 'POST'])
def index():
    # post method creates a short for a webpage
    if request.method == 'POST':
        # get an unused short
        short = create_short(4)
        con = sqlite3.connect('urls.db')
        cur = con.cursor()
        allfetched = cur.execute("SELECT short_id from urls").fetchall()
        while short in allfetched:
            short = create_short(4)

        # register webpage
        webpage = request.form['webpage']

        cur.execute("INSERT INTO urls VALUES (?,?)", (short, webpage))
        con.commit()
        con.close()
        full_url = 'https://tools.omni-tek.org/shorten/' + short
        with open('shortened.html') as f2:
            content = f2.read()
            content = content.format(url_placeholder = full_url)
            return content

    # get method creates the form
    with open('url_shortener.html') as f:
        return f.read()


@app.route("/shorten/<name>")
def shorten(name):
    con = sqlite3.connect('urls.db')
    cur = con.cursor()
    fetchedone = cur.execute("SELECT URL FROM urls WHERE short_id=?", (name,)).fetchone()
    url2 = fetchedone[0]
    con.close()

    if url2[:8] != "https://":
        url2 = "https://" + url2

    template = '<html><head><meta http-equiv="refresh" content="0; URL=' + url2 + '" /></head><body><p>If you are not redirected immediately, <a href="' + url2 + '">click here</a>.</p></body></html>'

    return template


@app.route("/qrcode", methods=['GET', 'POST'])
def qrcode_func():
    # post method
    if request.method == 'POST':
        # generate qrcode
        url = request.form['url']
        img = qrcode_gen(url)

        with open('qrcode_img.html') as f:
            content2 = f.read()
            content2 = content2.format(placeholder = img)
            return content2

    # get method creates the form
    with open('qrcode.html') as f:
            return f.read()

@app.route("/passgen", methods=['GET', 'POST'])
def passgen():
    # post method
    if request.method == 'POST':
        # generate password
        quantity = int(request.form['quantity'])
        if quantity > 0 and quantity < 101:
            charset = []
            if request.form.get('lowercase') != None:
                charset.extend(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'])
            if request.form.get('uppercase') != None:
                charset.extend(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'])
            if request.form.get('numbers') != None:
                charset.extend(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
            if request.form.get('symbols') != None:
                charset.extend([' ', '!', '"', '#', '$', '%', '&', '\'', '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~'])

            password = ''
            for _ in range(quantity):
                password = password + secrets.choice(charset)

            with open('passgen_result.html') as f:
                content = f.read()
                content = content.format(placeholder = escape(password))
                return content
        else:
            return '<p>You must select a quantity between 1 and 100</p>'

    # get method creates the form
    with open('passgen.html') as f:
            return f.read()

@app.route("/dice", methods=['GET', 'POST'])
def dice():
    # post method
    if request.method == 'POST':
        # generate dice rolls
        lower_limit = int(request.form['lower_limit'])
        upper_limit = int(request.form['upper_limit'])
        die_quantity = int(request.form['die_quantity'])
        html_add = ''

        for _ in range(die_quantity):
            random_number = random.randint(lower_limit, upper_limit)
            html_add = html_add + '<span style="color: white; margin-right: 20px;">' + str(random_number) + '</span>'

        with open('dice_result.html') as f:
            content = f.read()
            content = content.format(placeholder = html_add)
            return content

    # get method creates the form
    with open('dice.html') as f:
        return f.read()

"""

@app.route("/poll", methods=['GET', 'POST'])
def poll():
    # post method
    if request.method == 'POST':
        # generate poll page
        question = request.form['question']
        answer1 = request.form['answer1']
        answer2 = request.form['answer2']
        answer3 = request.form['answer3']
        answer4 = request.form['answer4']
        answer5 = request.form['answer5']

        html_add = '<p>' + question + '</p>' + '''
        <div class="form-check">
            <input class="form-check-input" type="radio" name="flexRadioDefault" id="flexRadioDefault1">
            <label class="form-check-label" for="flexRadioDefault1">
                ''' + answer1 + '''
            </label>
        </div>
        <div class="form-check">
            <input class="form-check-input" type="radio" name="flexRadioDefault" id="flexRadioDefault1">
            <label class="form-check-label" for="flexRadioDefault1">
                ''' + answer2 + '''
            </label>
        </div>
        <div class="form-check">
            <input class="form-check-input" type="radio" name="flexRadioDefault" id="flexRadioDefault1">
            <label class="form-check-label" for="flexRadioDefault1">
                ''' + answer3 + '''
            </label>
        </div>
        <div class="form-check">
            <input class="form-check-input" type="radio" name="flexRadioDefault" id="flexRadioDefault1">
            <label class="form-check-label" for="flexRadioDefault1">
                ''' + answer4 + '''
            </label>
        </div>
        <div class="form-check">
            <input class="form-check-input" type="radio" name="flexRadioDefault" id="flexRadioDefault1">
            <label class="form-check-label" for="flexRadioDefault1">
                ''' + answer5 + '''
            </label>
        </div>
        '''

        with open('poll_generated.html') as f:
            content = f.read()
            content = content.format(placeholder = html_add)
            return content

    # get method creates the form
    with open('poll.html') as f:
        return f.read()

#ip_address = request.remote_addr

"""

if __name__ == "__main__":
    app.run(host='0.0.0.0')