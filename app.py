from flask import Flask, render_template, request
import random as rnd
import string
import requests
import num2words
import inflect
import json
from collections import OrderedDict
from operator import itemgetter

app = Flask(__name__)

s = rnd.choice(string.ascii_letters) + rnd.choice(string.ascii_letters)

@app.route('/task3/cf/profile/<handle>/')
def cf_si(handle):
    url = f'http://codeforces.com/api/user.status?handle={handle}&from=1&count=100'
    text = requests.get(url).text
    ssilka = json.loads(text)
    page_number = 1
    popitki = ssilka["result"]
    max_page_number = (len(popitki)+24) // 25
    return render_template("cf_single_page.html", popitki=popitki,handle=handle, max_page_number=max_page_number,page_number=page_number)
@app.route('/task3/cf/profile/<handle>/page/<int:page_number>/')
def cf_single(handle, page_number):
    url = f'http://codeforces.com/api/user.status?handle={handle}&from=1&count=100'
    text = requests.get(url).text
    ssilka = json.loads(text)
    popitki = ssilka["result"]

    max_page_number = (len(popitki)+24) // 25
    return render_template("cf_single_page.html", popitki=popitki,handle=handle, max_page_number=max_page_number,page_number=page_number)


@app.route('/task3/cf/top/')
def top():
    handles = sorted(request.args.get("handles").split("|"))
    orderby = request.args.get("orderby", "")
    handict = {}
    url = "https://codeforces.com/api/user.info?handles="
    for nick in handles:
        url = url + nick + ";"
    ssilka = json.loads(requests.get(url).text)
    if (ssilka["status"] == "FAILED"):
        return "User not found"
    else:
        for nicki in ssilka["result"]:
            handle = nicki["handle"]
            rating = nicki["rating"]
            handict[handle] = int(rating)
        if orderby == "rating":
            handict = OrderedDict(sorted(handict.items(), key=itemgetter(1), reverse=True))
    return render_template("cf_top.html", dict=handict)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("error404.html")


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
     <p>city={} category={} ad={}</p><h1>{}</h1><p>{}</p>""".format(city, category, ad, category[1] + city,
                                                                    city[1] + category)
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
    app.run(debug=True)
