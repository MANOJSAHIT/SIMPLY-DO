from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
import re
from datetime import datetime
from datetime import timedelta

app = Flask(__name__)


app.secret_key = 'manoj1234manu'
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:Manoj@1234@localhost/frt_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)



class set_up:
    def __init__(self):
        @app.route('/')
        @app.route('/login', methods =['GET', 'POST'])
        def login():
            if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
                self.username = request.form['email']
                self.password = request.form['password']
                verify_deatils=user.query.filter_by(user_mail=self.username).all()
                if len(verify_deatils)==0:
                    new_user=user(self.username,self.password)
                    db.session.add(new_user)
                    db.session.commit()
                    return redirect(url_for('main_page'))

                else:
                    for i in verify_deatils:
                        if i.user_password==self.password:
                            return redirect(url_for('main_page'))
                        else:
                            return redirect(url_for('login'))
            return render_template('login.html')

        @app.route('/main_page',methods=['GET','POST'])
        def main_page():
            if request.method == 'POST' and 'event-name' in request.form:
                schedule_name=request.form['event-name']
                schedule_time=request.form['date_time']
                new_schedule=schedules_details(schedule_name,schedule_time,self.username)
                db.session.add(new_schedule)
                db.session.commit()

            elif request.method=='POST':
                but_id=request.get_data()
                get_row=schedules_details.query.get(but_id)
                if get_row.schedules_status:
                    get_row.schedules_status=False
                else:
                    get_row.schedules_status=True
                db.session.commit()
            today = datetime.today()
            t =str(today.strftime("%m/%d/%Y"))
            y = str((today - timedelta(days = 1)).strftime("%m/%d/%Y"))
            to =str((today + timedelta(days = 1)).strftime("%m/%d/%Y"))
            user_yesterday_schedules=schedules_details.query.filter_by(user_mail=self.username).filter(schedules_details.schedules_dt.op('regexp')(y)).all()
            user_today_schedules=schedules_details.query.filter_by(user_mail=self.username).filter(schedules_details.schedules_dt.op('regexp')(t)).all()
            user_tommorow_schedules=schedules_details.query.filter_by(user_mail=self.username).filter(schedules_details.schedules_dt.op('regexp')(to)).all()

            y_event_time={}
            t_event_time={}
            to_event_time={}
            for i in user_yesterday_schedules:
                y_event_time[i.schedules_name]=[str(i.schedules_dt)[-8::1],i.schedules_status,i.schedules_number]
            for i in user_today_schedules:
                t_event_time[i.schedules_name]=[str(i.schedules_dt)[-8::1],i.schedules_status,i.schedules_number]
            for i in user_tommorow_schedules:
                to_event_time[i.schedules_name]=[str(i.schedules_dt)[-8::1],i.schedules_status,i.schedules_number]
            leng=[len(list(y_event_time.keys())),len(list(t_event_time.keys())),len(list(to_event_time.keys()))]
            return render_template('index.html',yet=y_event_time,tet=t_event_time,toet=to_event_time,l=leng)

class user(db.Model):

    __tablename__='user_info'
    user_id=db.Column(db.Integer,primary_key=True,unique=True,autoincrement=True,nullable=False)
    user_mail=db.Column(db.VARCHAR(45),unique=True)
    user_password=db.Column(db.VARCHAR(10))

    def __init__(self,user_mail,user_password):
        self.user_mail=user_mail
        self.user_password=user_password
class schedules_details(db.Model):

    __tablename__='schedules_info'
    schedules_number=db.Column(db.Integer,primary_key=True,nullable=False,unique=True,autoincrement=True)
    schedules_name=db.Column(db.VARCHAR(45),nullable=False)
    schedules_status=db.Column(db.Boolean,nullable=False,default=False)
    schedules_dt=db.Column(db.VARCHAR(20),nullable=False)
    user_mail=db.Column(db.VARCHAR(45),nullable=False)

    def __init__(self,name,dt,mail):
        self.user_mail=mail
        self.schedules_dt=dt
        self.schedules_name=name

if __name__ == '__main__':
    set_up()
    db.create_all()
    app.run(debug=True)
