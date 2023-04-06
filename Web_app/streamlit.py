import streamlit as st
import pandas as pd
#import base64
#from sklearn.linear_model import LogisticRegression
#from sklearn.model_selection import train_test_split
#from sklearn.preprocessing import MinMaxScaler
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
#import pickle as pkl
#import shap
import streamlit.components.v1 as components
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
st.subheader("How much yield can your farm generate next season?💸 "
                 "This machine learning app will help you to make a prediction for your next farming methodology!")

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
    f_level = f_level.replace(f_dict)

    pests = ["A","B","C","D"]
    for item in pests:
        if item in p_types:
            pests[pests.index(item)] = 1
        else:
            pests[pests.index(item)] = 0
    
    user_input_dict={'f_level':[f_level], 'pests':[pests], 'region_list':[region_list]} 
     
    return user_input_dict

#user_input=preprocess
user_input_dict=preprocess(region_code, f_level, p_types) 

#predict button
btn_predict = st.sidebar.button("Predict")


