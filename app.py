from flask import Flask, request, render_template
import pickle

app = Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict_crop')
def predict_crop():
    return render_template('predict_crop_form.html')




if __name__ == "__main__":
    app.run(debug=True)