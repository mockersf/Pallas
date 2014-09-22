from wtforms import Form, TextField, validators
from flask import Flask, render_template, flash, request
app = Flask(__name__)
app.secret_key = 'why would I tell you my secret key?'

class TargetSiteForm(Form):
    target = TextField('target', [validators.Length(min=4, max=250)])

@app.route('/', methods=['GET', 'POST'])
def hello():
    form = TargetSiteForm(request.form)
    if request.method == 'POST' and form.validate():
        flash('going to analyse %s' % form.target)
        #return redirect(url_for('login'))
    return render_template('index.html', form=form)

    res = '<html>'
    res += header()
    res += '<div><form>target : <input type="text" name="target"></form>'
    res += '</html>'
    return res