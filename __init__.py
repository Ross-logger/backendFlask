from flask import Flask, render_template, request, redirect, url_for, flash, make_response, session

app = Flask(__name__)

@app.route('/visits-counter/')
def visits():
    if 'visits' in session:
        session['visits'] = session.get('visits') + 1  # чтение и обновление данных сессии
    else:
        session['visits'] = 1  # настройка данных сессии
    return "Total visits: {}".format(session.get('visits'))


@app.route('/delete-visits/')
def delete_visits():
    session.pop('visits', None)  # удаление данных о посещениях
    return 'Visits deleted'

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.run(debug=True)
