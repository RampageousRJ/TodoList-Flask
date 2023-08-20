from app import app,db
from flask import render_template,redirect,url_for,flash,get_flashed_messages
from forms import *
from models import Task
from datetime import date

@app.route('/',endpoint='home')
def home():
    tasks = Task.query.all()
    return render_template('home.html',tasks=tasks)

@app.route('/add',methods=['GET','POST'],endpoint='add')
def add():
    form = Addtask()
    if form.validate_on_submit():
        print('Submitted:',form.title.data)
        t1=Task(title=form.title.data,date=date.today())
        db.session.add(t1)
        db.session.commit()
        flash('Task added successfully')
        return redirect(url_for('home'))
    return render_template('add.html',form=form)

@app.route('/edit/<int:task_id>',methods=['GET','POST'])
def edit(task_id):
    task = Task.query.get(task_id)
    form = Addtask()
    if task:
        if form.validate_on_submit():
            task.title = form.title.data
            task.date = date.today()
            db.session.commit()
            flash('Task edited successfully')
            return redirect(url_for('home'))
        form.title.data = task.title
        return render_template('edit.html',form=form,task_id=task_id)
    else:
        flash("Task not found")
    return redirect('home')

@app.route('/delete/<int:task_id>',methods=['GET','POST'])
def delete(task_id):
    task = Task.query.get(task_id)
    form = DeleteTask()
    if task:
        if form.validate_on_submit():
            db.session.delete(task)
            db.session.commit()
            flash('Task deleted successfully')
            return redirect(url_for('home'))
        return render_template('delete.html',form=form,task_id=task_id,title=task.title)
    else:
        flash("Task not found")
    return redirect('home')