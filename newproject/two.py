import os
from flask.ext.bootstrap import Bootstrap
from flask.ext.script import Manager
from flask import Flask,render_template,session,redirect,url_for,flash
from flask.ext.moment import Moment
from datetime import datetime
from flask.ext.wtf import Form
from wtforms import StringField,SubmitField
from wtforms.validators import Required
from flask.ext.sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ os.path.join(database,'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


bootstrap = Bootstrap(app)
manager = Manager(app)
moment = Moment(app)
db = SQLALchemy(app)
migrate = Migrate(app,db)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    users = db.relationship('User',backref='role',lazy='dynamic')

    def __repr__(self):
        return '<Role %r>'% self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.column(db.String(64),unique=True,index=True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username




class NameForm(FlaskForm):
    name = StringField('What is your name?',validators=[Required()])
    submit = SubmitField('Submit')



def make_shell_context():
    return dict(app=app,db=db,User=User,role=Role)
manager.add_command('shell',shell(make_context=make_shell_context))
manager.add_command('db',MigrateCommand)



@app.route('/',methods=['GET','POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash(' I love you! ')
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html',form=form,name=session.get('name'))



@app.errorhandler(404)
def page_not_found(e):
    print(e)
    return render_template('404.html'),404



@app.errorhandler(500)
def internal_server_error(e):
    print("e: ", e)
    return render_template('500.html'),500



@app.route('/user/<name>')
def user(name):
    return render_template('user.html',name=name)



















if __name__== '__main__':
    manager.run()


