from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

#%%

import pandas as pd
df=pd.read_csv("C:\\Users\\Nishaant Harrish\\Downloads\\lungcancer.csv")

df=df.drop(['YELLOW_FINGERS','ALCOHOL CONSUMING','ANXIETY'],axis=1)

k=df.select_dtypes(include=object)
for i in k:
    df[i]=df[i].astype('category')
    df[i]=df[i].cat.codes


x=df.iloc[:,:-1]
y=df.iloc[:,-1]


from sklearn.linear_model import LinearRegression
reg=LinearRegression()
reg.fit(x,y)

#%%
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_submit():
    username = request.form['username']
    password = request.form['password']

    db=mysql.connector.connect(host='localhost',user='root',password='nishaant2003',database='login')
    cur=db.cursor(dictionary=True)
    cur.execute("select * from detail where username='"+username+"' and password='"+password+"'")
    res=cur.fetchone()

    if res is None:
        return render_template('login.html', error='Invalid username or password')
    else:
        return redirect(url_for('input'))
        
#%%
@app.route('/predict',methods=['POST'])
def pred():
    
    gender = int(request.form.get('gender'))
    age = int(request.form.get('age'))
    smoking = int(request.form.get('smoking'))
    peer_pressure=int(request.form.get('peer_pressure'))
    chronic_disease=int(request.form.get('chronic_disease'))
    fatigue=int(request.form.get('fatigue'))
    allergy=int(request.form.get('allergy'))
    wheezing=int(request.form.get('wheezing'))
    coughing=int(request.form.get('coughing'))
    breath=int(request.form.get('breath'))
    swallow=int(request.form.get('swallow'))
    chest=int(request.form.get('chest'))
    
    op = reg.predict([[gender,age,smoking,peer_pressure,chronic_disease,
                       fatigue,allergy,wheezing,coughing,breath,swallow,chest]])
    
    if op <= 1:
        return render_template('output.html',result = 'Lung Cancer : Negative')
    else:
        return render_template('output.html',result = 'Lung Cancer : Positive')
   
#%%
@app.route('/input')
def input():
    return render_template('input.html')

if __name__ == '__main__':
    app.run(host='localhost',port=5000)
