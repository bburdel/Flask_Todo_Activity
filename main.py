from datetime import datetime
import os
import pysnooper

from flask import Flask, render_template, request, redirect, url_for, session
from passlib.hash import pbkdf2_sha256

from model import Task, User

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY').encode()


@app.route('/all')
def all_tasks():
    return render_template('all.jinja2', tasks=Task.select())


@app.route('/create', methods=['GET', 'POST'])
def create_task():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == "POST":
        task = Task(task_name=request.form['task_name'])
        task.save()
        return redirect(url_for('all_tasks'))
    else:
        return render_template('create.jinja2')


@app.route('/login', methods=["GET", "POST"])
# @pysnooper.snoop(depth=2)
def login():
    if request.method == "POST":
        user_lookup = User.select().where(User.user_name == request.form['user_name']).get()

        if user_lookup and pbkdf2_sha256.verify(request.form['user_password'], user_lookup.user_password):
            session['username'] = request.form['user_name']
            return redirect(url_for('all_tasks'))

        return render_template('login.jinja2', error="Incorrect username or password.")
    else:
        return render_template('login.jinja2')


@app.route('/incomplete', methods=['GET', 'POST'])
@pysnooper.snoop(depth=2)
def incomplete_tasks():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        user = User.select().where(User.user_name == session['username']).get()

        Task.update(task_performed=datetime.now(), performed_by=user)\
            .where(Task.id == request.form['task_id'])\
            .execute()

    return render_template('incomplete.jinja2', tasks=Task.select().where(Task.task_performed.is_null()))


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
