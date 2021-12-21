import requests
import json
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, SelectField 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'JazEatz'

class InputForm(FlaskForm):
    let_alex_decide = BooleanField('Let Alex Decide')
    keyword = StringField('Keyword ie.Sushi')
    max_price = SelectField('Min Price', choices=[('0'), ('1'), ('2'), ('3'), ('4')])   
    min_price = SelectField('Min Price', choices=[('0'), ('1'), ('2'), ('3'), ('4')])
    distance = SelectField('Distance', choices=[('1609.344','1 mile'), ('8046.72','5 mile'), ('16093.44','10 mile'), ('32186.88','20 mile')])
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def home():
    let_alex_decide = None
    keyword = None
    min_price = None
    max_price = None
    distance = None
    parse_json = ' '
    form = InputForm()
    if form.validate_on_submit():
        let_alex_decide = form.let_alex_decide.data
        keyword = form.keyword.data 
        min_price = form.min_price.data 
        max_price = form.max_price.data 
        distance = form.distance.data 
                
        url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=39.0168576,-87.7428736&radius="+distance+"&type=restaurant&keyword="+keyword+"&maxprice="+max_price+"&minprice="+min_price+"&rankby=prominence&key=AIzaSyDDKTXC22b3UwBzEoULKfOry0O1f4hbfYE"
        #Add open now

        response = requests.get(url)
        parse_json = json.loads(response.text)

    entrys = parse_json['results']
        
    return render_template('home.html', form=form, entrys=entrys) 

if __name__ == '__main__':
    app.run(debug=True)