from __init__ import app as app
from flask import Flask, render_template, redirect, url_for
import pyfiles
from pyfiles import helloworld,dbmod
from flask_wtf import Form
from wtforms import TextField, IntegerField, validators, SubmitField
from flask import request

class Form(Form):
    zip = IntegerField('zip')
    submit = SubmitField('Submit')


@app.route('/home', methods=['GET','POST'])
def hello_world():
    form = Form()
    package = helloworld.collectTableData()
    if request.method == 'POST':
        zip = request.form.to_dict()
        zip = zip['zipinput']
        return redirect(url_for('my_zip',zip=zip)) #my_zip(form.zip)
    return render_template('somedata.html',package=package)
    
@app.route('/myzip/<zip>',methods=['GET', 'POST'])
def my_zip(zip):
    #pack = dbmod.getPCVectorFromDB()
    zip = int(float(zip))
    pack = dbmod.getZIPData(zip)
    legend = 'Some Data'
    labels = pack[0]
    values = pack[1]
    rank = dbmod.getZIPRank(zip)
    rank = round(rank[1]*100)
    return render_template('chart.html',values=values, labels=labels, legend=legend, rank=rank)

@app.route('/')
def landingpage():
    return render_template('base.html')

@app.route('/insights')
def insights():
    return render_template('insights.html')

@app.route('/myzip')
def myzip():
    return render_template('myzip.html')

@app.route('/about')
def about():
    return render_template('about.html')
