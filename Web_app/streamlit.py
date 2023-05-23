# This script will launch a streamlit application using local host that allows user to set farming parameters 
#and gives prediction of farm yield with model explaination.
# The location of model artifacts file needs to be updated based on the directory used to run the script.
# Current script uses 'best_model.sav' file stored in the local machine.


import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
#import base64
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import Ridge
import joblib
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
#import pickle as pkl
#import shap
import streamlit.components.v1 as components

model = joblib.load("Web_app/best_model.sav")


image1 = Image.open('Web_app/crop.PNG')
image2 = Image.open('Web_app/farm_params.png')
st.set_page_config( 
    page_title="Yield Prediction App",
    page_icon=image1 
)
st.set_option('deprecation.showPyplotGlobalUse', False)

######################
#main page layout
######################

st.title("Farm Yield Analytics")
st.subheader("How much yield can your farm generate next season?:ear_of_rice: ")
st.markdown("**This machine learning app will help you make predictions for your next farming methodology!**")

col1, col2 = st.columns([1, 1])

with col1:
    st.image(image1)

with col2:
    st.write("""As the world population continues to grow, the demand for food increases, making it more important than ever to optimize farming practices and increase crop yields. 
    \nUsing machine learning algorithms crop yields can be estimated by leveraging historical data. 
    This will help make more informed decisions about farming practices, optimize crop yield, and ultimately, increase profits. 
""")
    
st.subheader("To predict the farm yield, you need to follow the steps below:")
st.markdown("""
1. Enter/choose the parameters that best describe your farming conditions on the left side bar
2. Press the "Predict" button and wait for the result.
""")

st.subheader("Estimated Yield: ")

######################
#sidebar layout
######################

st.sidebar.title("Farming Conditions")
st.sidebar.image(image2, width=250)
st.sidebar.write("Choose farming parameters")

#input features
region_code =st.sidebar.selectbox('Select region code', ("0","1", "2", "3", "4", "5", "6"))
f_level =st.sidebar.selectbox('Select level of fertilization', ("0", "1", "2", "3", "4", "5"))
water =st.sidebar.slider("Set amount of water supply per hectare",min_value=0.0, max_value=15.0,step=0.1)
p_amount =st.sidebar.slider("Set amount of pesticides use per hectare",min_value=0.0, max_value=10.0,step=0.1)
p_types = st.sidebar.multiselect("Select one or multiple types of pesticides used", ('A', 'B', 'C', 'D'))
p = st.sidebar.slider("Choose X range for analysis plots",min_value=0.0, max_value=20.0,step=0.1)

def preprocess(region_code, f_level, p_types): 
# Pre-processing user input
    region_list = [0,0,0,0,0,0,0]
    region_list[int(region_code)] = 1

    f_dict = {"0":0, "1":1, "2":2, "3":3, "4":4, "5":5} 
    f_level = f_dict[f_level]

    pests = ["A","B","C","D"]
    for item in pests:
        if item in p_types:
            pests[pests.index(item)] = 1
        else:
            pests[pests.index(item)] = 0
    
    input_dict={'f_level':f_level, 'pests':pests, 'region_list':region_list} 
     
    return input_dict

#user_input=preprocess
input_dict=preprocess(region_code, f_level, p_types) 
uv = 72
inputs = np.array([water,uv,f_level,p_amount,input_dict['pests'][0],input_dict['pests'][1],
                   input_dict['pests'][2],input_dict['pests'][3],input_dict['region_list'][0],
                   input_dict['region_list'][1],input_dict['region_list'][2],input_dict['region_list'][3],
                   input_dict['region_list'][4],input_dict['region_list'][5],input_dict['region_list'][6],p_amount**2]).reshape(1,-1)
columns = ['water','uv','fertilizer_usage','pesticides','pesticide_a','pesticide_b','pesticide_c','pesticide_d',
           'region_0','region_1','region_2','region_3','region_4','region_5','region_6','pesticides_2']
test_input = pd.DataFrame(inputs, columns=columns)

#predict button
btn_predict = st.sidebar.button("Predict")

if btn_predict:
    pred = model.predict(test_input)
    result = round(pred[0], 2)
    res = str(result)

    st.write('**:green[The estimated yield per hectare for the given case is]**', res)
else:
    st.write('**:red[Please select the parameters and hit Predict to see the result. ]**')

st.subheader('Model Explaination')

if btn_predict:
    #Plot feature importances
    imp_f = pd.Series(model.best_estimator_._final_estimator.coef_, index=columns)
    #st.write(imp_f)
    imp_f = imp_f.sort_values()
    imp_f.to_frame()
    #colors = ['crimson',] * 12
    #colors[0:8] = 'green'
    #fig = imp_f.plot(kind='barh')
    fig = px.bar(data_frame=imp_f, orientation='h', labels={"index": "Parameters", "value": "Influence"}, text_auto='.3f', color=imp_f.values, color_continuous_scale='balance')
    fig.update_layout(showlegend=False)
    st.write(fig)
    st.write("""The amount of pesticides and fertilization level are bigest influensors in yield prediction. Being in region 5 or 6 also impacts the target varible estimation significantly.
         \nModel rewards higher fertilization level and pesticide amount to achieve better yield per hectare while penalizes too much of pesticide supply and farms being in region 5 or 6.""")
else:
    st.write('**:red[Please select the parameters and hit Predict to see the model explaination. ]**')

st.subheader('Parameter Analysis')        

#st.write("""Below you can analyse the effect of individual parameter on the yield generated.""")
st.write("""The plot below shows the effect of selected parameter on yield, while keeping the other varibles same as what you set in the side panel.""")

param = st.radio('Select the parameter and hit Predict', ["Fertilization level", "Water supply", "Pesticide amount", "Region", "Pesticide Types"],horizontal=True)


if btn_predict and param == "Fertilization level":
    results = []
    inputs = [0,1,2,3,4,5]
    for i in range(6):
        test_input['fertilizer_usage'] = i
        result_i = model.predict(test_input)
        results.append(round(result_i[0],2))
    df = pd.DataFrame(list(zip(inputs, results)), columns =['Fertilization level', 'Yield / hectare'])    
    st.bar_chart(data=df, x='Fertilization level', y='Yield / hectare')
    
if btn_predict and param == "Water supply":
    results = []
    p_range = np.arange(0,p,0.1)
    inputs = list(p_range)
    for i in p_range:
        test_input['water'] = i
        result_i = model.predict(test_input)
        results.append(round(result_i[0],2))
    df = pd.DataFrame(list(zip(inputs, results)), columns =['Water Supply', 'Yield / hectare'])    
    st.line_chart(data=df, x='Water Supply', y='Yield / hectare')

if btn_predict and param == "Pesticide amount":
    results = []
    p_range = np.arange(0,p,0.1)
    inputs = list(p_range)
    for i in p_range:
        test_input['pesticides'] = i
        test_input['pesticides_2'] = i**2
        result_i = model.predict(test_input)
        results.append(round(result_i[0],2))
    df = pd.DataFrame(list(zip(inputs, results)), columns =['Pesticide amount', 'Yield / hectare'])    
    st.line_chart(data=df, x='Pesticide amount', y='Yield / hectare')
    
if btn_predict and param == "Region":
    test_input[["region_0","region_1","region_2","region_3","region_4","region_5","region_6"]] = 0
    results = []
    inputs = [0,1,2,3,4,5,6]
    for i in inputs:
        if i==0:
            test_input['region_0'] = 1
        if i==1:
            test_input['region_1'] = 1
        if i==2:
            test_input['region_2'] = 1
        if i==3:
            test_input['region_3'] = 1
        if i==4:
            test_input['region_4'] = 1
        if i==5:
            test_input['region_5'] = 1
        if i==6:
            test_input['region_6'] = 1
        result_i = model.predict(test_input)
        results.append(round(result_i[0],2))
    df = pd.DataFrame(list(zip(inputs, results)), columns =['Region', 'Yield / hectare'])    
    st.bar_chart(data=df, x='Region', y='Yield / hectare')
    
if btn_predict and param == "Pesticide Types":
    test_input[["pesticide_a","pesticide_b","pesticide_c","pesticide_d"]] = 0
    results = []
    inputs = ['A','B','C','D','AB','AC','AD','BC','BD','CD','ABC','ABD','ACD','BCD','ABCD']
    for i in inputs:
        if 'A' in i:
            test_input['pesticide_a'] = 1
        if 'B' in i:
            test_input['pesticide_b'] = 1
        if 'C' in i:
            test_input['pesticide_c'] = 1
        if 'D' in i:
            test_input['pesticide_d'] = 1
        result_i = model.predict(test_input)
        results.append(round(result_i[0],2))
    df = pd.DataFrame(list(zip(inputs, results)), columns =['Pesticide Types', 'Yield / hectare'])    
    st.bar_chart(data=df, x='Pesticide Types', y='Yield / hectare')
