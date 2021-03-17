from flask import Flask,request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
db= SQLAlchemy(app)

class Todo(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String, nullable= False)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['GET','POST'])
def index():
    if request.method=='POST':
        task_content = request.form['task']
        new_task = Todo(task=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'Edho prechana'
    else:
        tasks= Todo.query.all()
        return render_template('index.html',tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete =  Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Idha delete panna mudiyadhu'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.task=request.form['task']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'update panna mudiyadhuu'
    else:
        return render_template('update.html',task=task)
if __name__ == '__main__':
    app.run(debug=True)