from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///items.db'
db = SQLAlchemy(app)


class TodoList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # project = db.Column(db.String(100),nullable=False)
    # phase = db.Column(db.Integer,nullable=False)
    task = db.Column(db.Text, nullable=False)
    owner = db.Column(db.String(100), nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    comments = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(10), nullable=False)
    grouping = db.Column(db.String(100), nullable=True)
    date_recorded = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)

# task
# owner
# due_date
# comments
# status
# grouping
# date_recorded

    def __repr__(self):
        return 'To Do Task #' + str(self.id)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/tasks', methods=['GET', 'POST'])
def tasks():
    if request.method == 'POST':
        todo_task = request.form['task']
        todo_owner = request.form['owner']

        # Have to convert string date to datetime below
        todo_due_date = request.form.get('due_date')
        todo_due_date = datetime.strptime(todo_due_date, '%Y-%m-%d')

        todo_comments = request.form['comments']
        todo_status = request.form['status']
        todo_grouping = request.form['grouping']
        new_task = TodoList(task=todo_task, owner=todo_owner,
                            due_date=todo_due_date, comments=todo_comments, status=todo_status, grouping=todo_grouping)
        db.session.add(new_task)
        db.session.commit()
        return redirect('/tasks')
    else:
        all_tasks = TodoList.query.order_by(TodoList.date_recorded).all()
        return render_template('tasks.html', tasks=all_tasks)


@app.route('/tasks/delete/<int:id>')
def delete(id):
    task = TodoList.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect('/tasks')


@app.route('/tasks/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    task = TodoList.query.get_or_404(id)
    if request.method == 'POST':
        task.task = request.form['task']
        task.owner = request.form['owner']

        # Have to convert string date to datetime below
        todo_due_date = request.form.get('due_date')
        task.due_date = datetime.strptime(todo_due_date, '%Y-%m-%d')

        task.comments = request.form['comments']
        task.status = request.form['status']
        task.grouping = request.form['grouping']
        db.session.commit()
        return redirect("/tasks")
    else:
        return render_template('edit.html', task=task)


if __name__ == "__main__":
    app.run(debug=True)
