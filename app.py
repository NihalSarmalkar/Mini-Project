from flask import Flask, request, render_template
import pickle
import requests
import numpy as np
import json






crop_recommendation_model_path = 'model/MiniProject_RandomForest.pkl'
crop_recommendation_model = pickle.load(
    open(crop_recommendation_model_path, 'rb'))

fertilizer_recommendation_model_path = 'model/MiniProject_RandomForest_fertilizer.pkl'
fertilizer_recommendation_model = pickle.load(
    open(fertilizer_recommendation_model_path, 'rb'))



def weather_fetch(city_name):

    api_key = "42b6b378bf320ec65f4cb1a193c4f4db"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    x = response.json()

    if x["cod"] != "404":
        y = x["main"]

        temperature = round((y["temp"] - 273.15), 2)
        humidity = y["humidity"]
        return temperature, humidity
    else:
        return None


app = Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict_crop')
def predict_crop():
    return render_template('predict_crop_form.html')

@app.route('/predict_fertilizer')
def fertilizer_crop():
    return render_template('predict_fertilizer_form.html')


@ app.route('/crop-predict', methods=['POST'])
def crop_prediction():
    

    if request.method == 'POST':
        N = int(request.form['nitrogen'])
        P = int(request.form['phosphorous'])
        K = int(request.form['pottasium'])
        rainfall = float(request.form['rainfall'])

        # state = request.form.get("stt")
        city = request.form.get("city")

        if weather_fetch(city) != None:
            temperature, humidity = weather_fetch(city)
            data = np.array([[N, P, K, temperature, humidity, rainfall]])
            my_prediction = crop_recommendation_model.predict(data)
            final_prediction = my_prediction[0]

            return render_template('predict_crop_form.html', prediction=final_prediction)

        else:

             return render_template('predict_crop_form.html', prediction="Error Please Try Again !! ")

@ app.route('/fertilizer-predict', methods=['POST'])
def fertilizer_prediction():
    

    if request.method == 'POST':
        N = int(request.form['nitrogen'])
        P = int(request.form['phosphorous'])
        K = int(request.form['pottasium'])
        M = int(request.form['Moisture'])
        TypeSoil = request.form['typeSoil']
        TypeCrop = request.form['typeCrop']

        
        Dict = {"Sandy": 4, "Loamy": 2, "Black": 0,"Red":3,"Clayey":1}
        
        Dict1 = {"Cotton": 1, "Tobacco": 9, "Paddy": 6,"Barley":0,"Wheat":10,"Oil seeds":5, "Grounds Nuts":2, "Maize": 3,"Millets":4, "Pulses": 7, "sugarcane": 8}

        """  
        Sandy - 4
        Loamy - 2
        Black - 0
        Red - 3
        Clayey - 1

        Cotton - 1
        Tobacco - 9
        Paddy - 6
        Barley - 0
        Wheat - 10
        Oil seeds - 5
        Ground Nuts - 2
        Maize - 3
        Millets - 4
        Pulses - 7
        Sugarcane - 8

        """

        



        # state = request.form.get("stt")
        city = request.form.get("city")

        if weather_fetch(city) != None:
            temperature, humidity = weather_fetch(city)
            data = np.array([[temperature, M, N,K,P , Dict[TypeSoil],Dict1[TypeCrop]]])
            my_prediction = fertilizer_recommendation_model.predict(data)
            final_prediction = my_prediction[0]

            return render_template('predict_fertilizer_form.html', prediction=final_prediction)

        else:

             return render_template('predict_fertilizer_form.html', prediction="Error Please Try Again !! ")


            





if __name__ == "__main__":
    app.run(debug=True)