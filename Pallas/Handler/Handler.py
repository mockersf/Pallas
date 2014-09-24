from wtforms import Form, TextField, SelectField, validators
from flask import Flask, render_template, flash, request
app = Flask(__name__)
app.secret_key = 'why would I tell you my secret key?'

class TargetSiteForm(Form):
    target = TextField('target', [validators.Length(min=4, max=250)])
    browser = SelectField('browser', choices=[('phantom', 'phantomJS'), ('ff', 'Firefox'), ('chrome', 'Chrome'), ('ie', 'Internet Explorer')])

@app.route('/', methods=['GET', 'POST'])
def hello():
    form = TargetSiteForm(request.form)
    if request.method == 'POST' and form.validate():
        flash('going to analyse %s with %s' % (form.target.data , form.browser.data))
    return render_template('index.html', form=form)
