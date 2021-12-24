import requests
import json
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, SelectField 
import time


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
    res = requests.get('https://ipinfo.io/')
    data = res.json()

    location = data['loc'].split(',')
    lat = float(location[0])
    log = float(location[1])
    lat = str(lat)
    log = str(log)

    let_alex_decide = None
    keyword = None
    min_price = None
    max_price = None
    distance = None
    parse_json = 'n/a'
    form = InputForm()
    if form.validate_on_submit():
        let_alex_decide = form.let_alex_decide.data
        keyword = form.keyword.data 
        min_price = form.min_price.data 
        max_price = form.max_price.data 
        distance = form.distance.data 
                
        url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location="+ lat +"," + log + "&radius="+distance+"&type=restaurant&keyword="+keyword+"&maxprice="+max_price+"&minprice="+min_price+"&rankby=prominence&key=AIzaSyDDKTXC22b3UwBzEoULKfOry0O1f4hbfYE"
        #Add open now

        response = requests.get(url)
        parse_json_o = json.loads(response.text)
        parse_json = parse_json_o['results']
        time.sleep(2)
        for entitys in parse_json:
            ent_photo =  str(entitys['photos']).split("'")
            entitys.update({'res_photo' : ent_photo[9]})
    
    if let_alex_decide == True:
        entrys = [parse_json[0]]
    else:
         entrys = parse_json
    
    return render_template('home.html', form=form, entrys=entrys, lat=lat, log=log) 

if __name__ == '__main__':
    app.run(debug=True)