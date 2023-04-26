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

model = joblib.load("/Users/mahip_cpp2xf3/Datalake-ml-mz/Analytics/best_model.sav")


image1 = Image.open('/Users/mahip_cpp2xf3/Datalake-ml-mz/Web_app/crop.PNG')
image2 = Image.open('/Users/mahip_cpp2xf3/Datalake-ml-mz/Web_app/farm_params.jpg')
st.set_page_config( 
    page_title="Yield Prediction App",
    page_icon=image1 
)
st.set_option('deprecation.showPyplotGlobalUse', False)

######################
#main page layout
######################

st.title("Farm Yield Prediction")
st.subheader("How much yield can your farm generate next season?:ear_of_rice: ")
st.markdown("**This machine learning app will help you to make a prediction for your next farming methodology!**")

col1, col2 = st.columns([1, 1])

with col1:
    st.image(image1, caption='Source: https://graindatasolutions.com/')

with col2:
    st.write("""As the world population continues to grow, the demand for food increases, making it more important than ever to optimize farming practices and increase crop yields. 
    \nUsing machine learning algorithms crop yields can be estimated by leveraging historical data. 
    This will help make more informed decisions about farming practices, optimize crop yield, and ultimately, increase profits. 
""")
    
st.subheader("To predict the farm yield, you need to follow the steps below:")
st.markdown("""
1. Enter/choose the parameters that best descibe your farming conditions on the left side bar;
2. Press the "Predict" button and wait for the result.
""")

st.subheader("Below you could find prediction result: ")

######################
#sidebar layout
######################

st.sidebar.title("Farming Conditions")
st.sidebar.image(image2, width=200)
st.sidebar.write("Please choose farming parameters")

#input features
region_code =st.sidebar.selectbox('Select region code', ("1", "2", "3", "4", "5", "6"))
f_level =st.sidebar.selectbox('Select level of fertilization', ("0", "1", "2", "3", "4", "5"))
water =st.sidebar.slider("Set amount of water supply per hectare",min_value=0.0, max_value=15.0,step=0.1)
p_amount =st.sidebar.slider("Set amount of pesticides use per hectare",min_value=0.0, max_value=10.0,step=0.1)
p_types = st.sidebar.multiselect("Select one or multiple types of pesticides used", ('A', 'B', 'C', 'D'))

def preprocess(region_code, f_level, p_types): 
# Pre-processing user input
    region_list = [0,0,0,0,0,0]
    region_list[int(region_code)-1] = 1

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
                   input_dict['region_list'][4],input_dict['region_list'][5],p_amount**2]).reshape(1,-1)
columns = ['water','uv','fertilizer_usage','pesticides','pesticide_a','pesticide_b','pesticide_c','pesticide_d',
           'region_1','region_2','region_3','region_4','region_5','region_6','pesticides_2']
test_input = pd.DataFrame(inputs, columns=columns)

#predict button
btn_predict = st.sidebar.button("Predict")

if btn_predict:
    pred = model.predict(test_input)
    result = round(pred[0], 2)

    st.write('**:green[The estimated yield per hectare for the given case is]**', result)
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
else:
    st.write('**:red[Please select the parameters and hit Predict to see the model explaination. ]**')

st.write("""The amount of pesticides and fertilization level are bigest influensors in yield prediction. Being in region 5 or 6 also impacts the target varible estimation significantly.
         \nModel rewards higher fertilization level and pesticide amount to achieve better yield per hectare while penalizes too much of pesticide supply and farms being in region 5 or 6.""")

        



