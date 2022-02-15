# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 18:25:36 2022
Description :- This an app which is used to predict Selling Prices of Used cars, which may belong to
an individual or a Car Dealer. 

@author : Galaxy Roy
"""
from flask import Flask, render_template, request as rq, url_for, redirect
import pickle
import numpy as np

app = Flask(__name__)
model = pickle.load(open('random_forest_regressor_model.pkl', 'rb'))

@app.route('/', methods = ['GET'])
def Home():
    return render_template('main.html')

@app.route('/refresh')
def refresh():
    return redirect('/')

@app.route('/predict', methods = ['POST', 'GET'])

def predict():
    
    Fuel_Type_Diesel = 0
    
    if rq.method == 'POST':
        
        Y = int(rq.form['Year'])
        Year = 2022 - Y
        present_price = float(rq.form['Present_Price'])
        X = float(rq.form['Kms_Driven'])
        kms_driven = np.log(X)
        owner = int(rq.form['Owner'])
        Fuel_Type_Petrol = rq.form['Fuel_Type_Petrol']
        fuel = 'Petrol' if Fuel_Type_Petrol == 'Petrol' else 'Diesel' if Fuel_Type_Petrol == 'Diesel' else 'CNG' 
        
        if Fuel_Type_Petrol == 'Petrol':
            Fuel_Type_Petrol = 1
            Fuel_Type_Diesel = 0
            
        elif Fuel_Type_Petrol == 'Diesel':
            Fuel_Type_Petrol = 0
            Fuel_Type_Diesel = 1
        
        else:
            Fuel_Type_Petrol = 0
            Fuel_Type_Diesel = 0

        Seller_Type_Individual = rq.form['Seller_Type_Individual']
        seller = 'Dealer' if Seller_Type_Individual == "Dealer" else 'Individual'
        
        if Seller_Type_Individual == 'Individual':
            Seller_Type_Individual = 1
            
        else:
            Seller_Type_Individual = 0
            
        Transmission = rq.form['Transmission_Manual']
        trans = 'Automatic' if Transmission == 'Automatic' else 'Manual'
        
        if Transmission == 'Manual':
            Transmission = 1
            
        else:
            Transmission = 0
   
        pred = model.predict([[present_price, kms_driven, owner, Year, Fuel_Type_Diesel, Fuel_Type_Petrol, Seller_Type_Individual, Transmission]])
        opt = round(pred[0], 2)
        
        if opt < 0:
            return render_template('output.html', prediction_text = "Cannot Be Sold", yr = Y, orgp = present_price, kmdrv = X, ownr = owner, fuel = fuel, seller = seller, trans = trans)
        
        else:
            return render_template('output.html', prediction_text = f'Your Car can be sold at a Price Of {opt} lakhs', yr = Y, orgp = present_price, kmdrv = X, ownr = owner, fuel = fuel, seller = seller, trans = trans)
        
    else:
        return render_template('main.html')
    
    
if __name__ == '__main__':    
    app.run(debug = True)