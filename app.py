from flask import Flask
import random as rnd
import string
import requests
import num2words
import inflect
import json

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
    out = """
     <h1>debug info</h1>
     <p>city={} category={} ad={}</p><h1>{}</h1><p>{}</p>""".format(city, category, ad, category[1] + city, city[1] + category)
    return out


@app.route("/task2/cf/profile/<username>/")
def cf(username):
    rating = requests.get("https://codeforces.com/api/user.rating?handle=" + username).json()
    if rating["status"] == "OK":
        rating = str(rating["result"][-1]["newRating"])
        out = """<table id=stats border="1">
        <tr>
            <th>User</th>
            <th>Rating</th>
        </tr>
        <tr>
            <td>{}</td>
            <td>{}</td> 
        </tr>
    </table>""".format(username, rating)
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


@app.route("/task2/num2words/<num>/")
def n(num):
    num = int(num)
    p = inflect.engine()
    h = p.number_to_words(num)
    h = " ".join(h.split("-"))
    h = " ".join(h.split(" and "))
    if 0 <= num <= 999:
        dict = {"status": "OK",
                "number": num,
                "isEven": not bool(num % 2),
                "words": h
                }
    else:
        dict = {
            "status": "FAIL"
        }
    return json.dumps(dict)


if __name__ == '__main__':
    app.run()
