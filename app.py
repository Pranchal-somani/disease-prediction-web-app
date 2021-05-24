#Important Modules
from flask import Flask,render_template, url_for ,flash , redirect
#from forms import RegistrationForm, LoginForm
import pickle
from flask import request
import numpy as np
#from keras.layers import Conv2D, MaxPooling2D, Dense, Dropout, Input, Flatten, SeparableConv2D
#from flask_sqlalchemy import SQLAlchemy
#from model_class import DiabetesCheck, CancerCheck

#from tensorflow.keras.models import Sequential
#from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Dropout, Input, Flatten, SeparableConv2D
#from tensorflow.keras.layers import GlobalMaxPooling2D, Activation
#from tensorflow.keras.layers.normalization import BatchNormalization
#from tensorflow.keras.layers.merge import Concatenate
#from tensorflow.keras.models import Model

import os
from flask import send_from_directory

#from this import SQLAlchemy
app=Flask(__name__,template_folder='templates')



# RELATED TO THE SQL DATABASE
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
#db=SQLAlchemy(app)

#from model import User,Post

#//////////////////////////////////////////////////////////

dir_path = os.path.dirname(os.path.realpath(__file__))
# UPLOAD_FOLDER = dir_path + '/uploads'
# STATIC_FOLDER = dir_path + '/static'
UPLOAD_FOLDER = 'uploads'
STATIC_FOLDER = 'static'

#graph = tf.get_default_graph()
#with graph.as_default():;
#FOR THE FIRST MODEL

# call model to predict an image


# home page

#@app.route('/')
#def home():
 #  return render_template('index.html')


# procesing uploaded file and predict it


@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)






#//////////////////////////////////////////////

#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"

#db=SQLAlchemy(app)

#class User(db.Model):
##   username = db.Column(db.String(20), unique=True, nullable=False)
 #   email = db.Column(db.String(120), unique=True, nullable=False)
    #image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
 #   password = db.Column(db.String(60), nullable=False)
    #posts = db.relationship('Post', backref='author', lazy=True)

    #def __repr__(self):
    #   return f"User('{self.username}', '{self.email}', '{self.image_file}')"


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")
 


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/cancer")
def cancer():
    return render_template("cancer.html")


@app.route("/diabetes")
def diabetes():
    #if form.validate_on_submit():
    return render_template("diabetes.html")

@app.route("/heart")
def heart():
    return render_template("heart.html")


@app.route("/kidney")
def kidney():
    #if form.validate_on_submit():
    return render_template("kidney.html")




"""
@app.route("/register", methods=["GET", "POST"])
def register():
    form =RegistrationForm()
    if form.validate_on_submit():
        #flash("Account created for {form.username.data}!".format("success"))
        flash("Account created","success")      
        return redirect(url_for("home"))
    return render_template("register.html", title ="Register",form=form )
@app.route("/login", methods=["POST","GET"])
def login():
    form =LoginForm()
    if form.validate_on_submit():
        #if form.email.data =="sho" and form.password.data=="password":
        flash("You Have Logged in !","success")
        return redirect(url_for("home"))
    #else:
    #   flash("Login Unsuccessful. Please check username and password","danger")
    return render_template("login.html", title ="Login",form=form )
def ValuePredictor1(to_predict_list):
    to_predict = np.array(to_predict_list).reshape(1,30)
    loaded_model = joblib.load("model")
    result = loaded_model.predict(to_predict)
    return result[0]
    
@app.route('/result1',methods = ["GET","POST"])
def result():
    if request.method == 'POST':
        to_predict_list = request.form.to_dict()
        to_predict_list=list(to_predict_list.values())
        to_predict_list = list(map(float, to_predict_list))
        result = ValuePredictor(to_predict_list)
        if int(result)==1:
            prediction='cancer'
        else:
            prediction='Healthy'       
    return(render_template("result.html", prediction=prediction))"""



def ValuePredictor(to_predict_list, size):
    to_predict = np.array(to_predict_list).reshape(1,size)
    if(size==8):#Diabetes
        loaded_model = pickle.load(open('diabetes_final.pkl','rb'))
        result = loaded_model.predict(to_predict)
    elif(size==30):#Cancer
        loaded_model = pickle.load(open('cancer_final.pkl','rb'))
        result = loaded_model.predict(to_predict)
    elif(size==12):#Kidney
        loaded_model = pickle.load(open("kidney.pkl",'rb'))
        result = loaded_model.predict(to_predict)
    elif(size==11):#Heart
        loaded_model = pickle.load(open("heart_final.pkl",'rb'))
        result =loaded_model.predict(to_predict)
    return result[0],size

@app.route('/result',methods = ["POST"])
def result():
    if request.method == 'POST':
        to_predict_list = request.form.to_dict()
        to_predict_list=list(to_predict_list.values())
        print(to_predict_list)
        to_predict_list = list(map(float, to_predict_list))
        if(len(to_predict_list)==30):#Cancer
            Result,size= ValuePredictor(to_predict_list,30)
        elif(len(to_predict_list)==8):#Daiabtes
            Result,size = ValuePredictor(to_predict_list,8)
        elif(len(to_predict_list)==12):
            Result ,size= ValuePredictor(to_predict_list,12)
        elif(len(to_predict_list)==11):
            Result,size = ValuePredictor(to_predict_list,11)
            #if int(result)==1:
            #   prediction ='diabetes'
            #else:
            #   prediction='Healthy' 
       
    if(int(Result)==1 and size==8):
        prediction='Sorry ! you are suffering from Diabetes disease'
    if(int(Result)==1 and size==11):
        prediction='Sorry ! you are suffering from heart disease'
    if(int(Result)==1 and size==12):
        prediction='Sorry ! you are suffering from kidney disease'
    if(int(Result)==1 and size==30):
        prediction='Sorry ! you are suffering from cancer disease'
    
    else:
        prediction='Congrats ! you are Healthy' 
    return(render_template("result.html", prediction=prediction))


if __name__ == "__main__":
    app.run(debug=True)
