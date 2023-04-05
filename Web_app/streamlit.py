import streamlit as st
import pandas as pd
#import base64
#from sklearn.linear_model import LogisticRegression
#from sklearn.model_selection import train_test_split
#from sklearn.preprocessing import MinMaxScaler
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
#import pickle as pkl
#import shap
import streamlit.components.v1 as components

st.set_page_config( 
    page_title="Yield Prediction App",
    page_icon="C:/Users/mahip_cpp2xf3/Datalake-ml-mz/Web_app/crop.PNG" 
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
    st.image("/Users/mahip_cpp2xf3/Datalake-ml-mz/Web app/crop.PNG")

with col2:
    st.write("""As the world population continues to grow, the demand for food increases, making it more important than ever to optimize farming practices and increase crop yields. One way to achieve this is through the use of machine learning algorithms to predict crop yields and gain insights from the data. By leveraging the power of data science, more informed decisions can be made about farming practices, crop yields can be optimized, and ultimately profits can be increased. 
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

