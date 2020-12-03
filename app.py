from flask import Flask
import random as rnd

app = Flask(__name__)


@app.route('/')
@app.route('/haba/')
def hello_world():
    s = ["Hello, Haba!",
         "Hello, Arsen!",
         "Hello, Karim!"]

    out = "<pre>{}</pre>".format("\n".join(s))
    return out


@app.route('/task1/random/')
def random():
    s = "Haba's mark is " + str(rnd.randint(1, 5))
    return s


@app.route('/task1/i_will_not/')
def iwont():
    s = ""
    for i in range(100):
        s += "<li>I will not waste time</li>\n"
    return s


@app.route('/menu')
def menu():
    s = ""
    s += "<li><a href=/task1/random/>/task1/random/</a></li>\n"
    s += '<li><a href=/task1/i_will_not/>/task1/i_will_not/</a></li>'
    return s


if __name__ == '__main__':
    app.run()
