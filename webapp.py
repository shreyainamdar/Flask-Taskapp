from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "test.db")}'
db = SQLAlchemy(app)

class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = ToDo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "Error in adding the task."
    else:
        tasks = ToDo.query.order_by(ToDo.date_created).all()
        return render_template('webapp.html', tasks=tasks)
    
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete=ToDo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "there was a problem deleting this task"
    

@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    task_nu=ToDo.query.get_or_404(id)
    if request.method=='POST':
        task_nu.content=request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return " there was a problem while updating the task"
    else:
        return render_template('update.html',task=task_nu)


if __name__ == '__main__':
    app.run(debug=True)
