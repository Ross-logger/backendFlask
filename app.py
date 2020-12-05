from flask import Flask
import random as rnd
import string
import requests

app = Flask(__name__)

s = rnd.choice(string.ascii_letters) + rnd.choice(string.ascii_letters)


@app.route('/')
def menu():
    s = ""
    s += "<ul id=menu>\n"
    s += "<li><a href=/task1/random/>/task1/random/</a></li>\n"
    s += '<li><a href=/task1/i_will_not/>/task1/i_will_not/</a></li>\n'
    s += "</ul>"
    return s


@app.route("/task2/avito/<city>/<category>/<ad>/")
def avito(city, category, ad):
    out = """ <table>
     <h1>debug info</h1>
     <pre>city={} category={} ad={}</pre><h1>{}</h1><pre>{}</pre>""".format(city, category, ad, s, s)
    return out


@app.route("/task2/cf/profile/<username>/")
def cf(username):
    rating = requests.get("https://codeforces.com/api/user.rating?handle=" + username).json()
    if rating["status"] == "OK":
        rating = str(rating["result"][-1]["newRating"])
        out = """<table>
        <tr>
            <th>User</th>
            <th>Rating</th>
        </tr>
        <tr>
            <th>{}</th>
            <th>{}</th>
        </tr>
    </table>
    """.format(username, rating)
    else:
        out = "User not found"
    return out


@app.route('/task1/random/')
def random():
    s = "Haba's mark is " + str(rnd.randint(1, 5))
    return s


@app.route('/task1/i_will_not/')
def iwont():
    s = ""
    s += "<ul id=blackboard>\n"
    for i in range(100):
        s += "<li>I will not waste time</li>\n"
    s += "</ul>"
    return s


@app.route('/haba/')
def hhh():
    s = ["Hello, Haba!",
         "Hello, Arsen!",
         "Hello, Karim!"]

    out = "<pre>{}</pre>".format("\n".join(s))
    return out


if __name__ == '__main__':
    app.run()
