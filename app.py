from flask import Flask, render_template, request, redirect, url_for
import json
import requests
import random


app = Flask(__name__)
value_ = {
    "token": "4UffYATBFJOqTiy9aJDnajwBa5XrSTfy",
    "secret": "put5plsochennadopukpukpukpukpuk1",
    "command": "set",
    "key": "",
    "value": ""
}
data_set = value_

key_ = {
    "token": "4UffYATBFJOqTiy9aJDnajwBa5XrSTfy",
    "secret": "put5plsochennadopukpukpukpukpuk1",
    "command": "get",
    "key": ""
}
data_get = key_

games_info = {}


@app.route("/task4/santa/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        create_form = request.form
        game_name = str(create_form["name_of_game"])
        shifr = str(random.randint(100000000000000000000000000000000000000000, 9000000000000000000000000000000089097809609)) + game_name
        secret = str(random.randint(100000000000000000000000000000000000000000, 9000000000000000000000000000000089097809609))
        link_for_player = "/task4/santa/play/{link}".format(link=shifr)
        organizer = "/task4/santa/toss/{link}/{secret}".format(link=shifr, secret=secret)
        info = {"name": game_name, "code": shifr, "secret":secret, "play": link_for_player,
                "organize":organizer, "active": "True", "players": []}
        data_set["key"] = shifr
        data_set["value"] = json.dumps(info)
        requests.post("https://arsenwisheshappy2021.herokuapp.com/query", data=data_set)
        return render_template("sdelannaya_igra.html", form=create_form, player_link=link_for_player,
                               organizer=organizer)
    else:
        return render_template('student_create.html')


@app.route("/task4/santa/play/<link>", methods=["GET", "POST"])
def play(link):
    if request.method == "GET":
        link_after_post = '/task4/santa/play/{link}'.format(link=link)
        data_get["key"] = link
        r_get = requests.post("https://arsenwisheshappy2021.herokuapp.com/query", data=data_get)
        game_info = json.loads(r_get.text)
        if game_info["active"] == "False":
            error = True
        else:
            error = False
        return render_template("game.html", error_start=error, link_after_post=link_after_post)
    elif request.method == "POST" and request.form["name"].strip() == '':
        link_after_post = '/task4/santa/play/{link}'.format(link=link)
        return render_template("game.html", error_name=True, link_after_post=link_after_post)
    elif request.method == "POST":
        player_form = request.form
        player_name = str(player_form["name"])
        data_get["key"] = link
        r_get = requests.post("https://arsenwisheshappy2021.herokuapp.com/query", data=data_get)
        game_info = json.loads(r_get.text)
        game_info["players"].append(player_name)
        data_set["key"] = link
        data_set["value"] = json.dumps(game_info)
        requests.post("https://arsenwisheshappy2021.herokuapp.com/query", data=data_set)
        return render_template("play_success.html", name=player_name)


@app.route("/task4/santa/toss/<link>/<secret>", methods=["GET", "POST"])
def secreet(link, secret):
    if request.method == "POST":
        data_get["key"] = link
        ret = requests.post("https://arsenwisheshappy2021.herokuapp.com/query", data=data_get)
        game_info = json.loads(ret.text)
        players_list = game_info["players"]
        random.shuffle(players_list)
        pairs = {}
        pairs[players_list[0]] = players_list[-1]
        for i in range(1, len(players_list) // 2):
            pairs[players_list[i]] = players_list[-i - 1]
        game_info["active"] = "False"
        data_set["key"] = link
        data_set["value"] = json.dumps(game_info)
        requests.post("https://arsenwisheshappy2021.herokuapp.com/query", data=data_set)
        list_of_keys = list(pairs.keys())
        return render_template("toss_finished.html", pairs=pairs, list_of_keys=list_of_keys)
    elif request.method == "GET":
        data_get["key"] = link
        ret = requests.post("https://arsenwisheshappy2021.herokuapp.com/query", data=data_get)
        game_info = json.loads(ret.text)
        if game_info["active"] == "False":
            error_f = True
        else:
            error_f = False
        players_list = game_info["players"]
        if len(players_list) == 0 or len(players_list) % 2 == 1:
            error_q = True
        else:
            error_q = False
        link_2 = "/task4/santa/toss/{link}/{secret}".format(link=link, secret=secret)
        return render_template("toss_start.html", error_q=error_q, error_f=error_f, players_list=players_list,
                               link_2=link_2)

if __name__ == '__main__':
    app.run(debug=True)
