from flask import Flask, render_template, request
from shared.database import save_to_db, init_db
from .tasks import process_user_task

app = Flask(__name__)
init_db()

@app.route('/sync', methods=['GET', 'POST'])
def sync_login():
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        save_to_db(name, surname)
        return f"Dane zapisano synchronicznie, {name} {surname}"
    return render_template('sync.html')

@app.route('/async', methods=['GET', 'POST'])
def async_login():
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        process_user_task.delay(name, surname)
        return "Zadanie wysłane do kolejki Celery"
    return render_template('async.html')

if __name__ == '__main__':
    app.run(debug=True)