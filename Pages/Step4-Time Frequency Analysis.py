import streamlit as st
import numpy as np
import pandas as pd
from func import trans_select,tfa_morlet
import matplotlib.pyplot as plt

st.title("Step4-Time Frequency Analysis")
st.subheader("R'nR Elderly Care Series")
#sidebar
data_selectXY = st.sidebar.radio('Direction:', ("x","y"), horizontal=True)
options=["Nose","LEye","REye","LEar","REar","LShouder","RShouder","LElbow","RElbow","LWrist","RWrist","LHip","RHip","LKnee","RKnee","LAnkle","RAankle"]
data_selectPiont = st.sidebar.radio('Keypiont',options, horizontal=True)
st.sidebar.write("Keypoint:", data_selectXY+trans_select( data_selectPiont))

#未選擇上傳資料顯示
empty_element1 = st.empty()
use_data_type= st.radio('Data select', ("Step3 Data","Load keypoint data file"), horizontal=True)
Step3df=None

if use_data_type=="Step3 Data":
    if st.session_state :
        #使用步驟三資料
        empty_element1.text("")
        empty_element3.text("")
        Step3df = st.session_state.df
        Data_Arr = Step3df[data_selectXY+trans_select(data_selectPiont)]
        try:
            # WAVELET
            time_series = np.array(Data_Arr.values)
            ts_length = time_series.shape[0]
            ts = time_series.reshape(ts_length,)
            pts_per_second = 60
            fmin = 0.1
            fmax = 1.5 #社區老人做坐到站每秒極限是2.5次
            fstep = 0.01
            taxis = np.linspace(1, ts_length, ts_length)
            taxis = taxis / pts_per_second  # 把單位改成 sec
            x_max = ts_length/pts_per_second  #畫小波圖的X軸的最大值(秒)

            time_series = Data_Arr
            spec = tfa_morlet(time_series, pts_per_second, fmin, fmax, fstep)
            spec_reverse = np.flip(spec, axis=0)
            plt.figure(figsize=(12, 6))
            plt.imshow(spec_reverse, extent=[0, x_max, fmin, fmax], cmap='jet', aspect='auto')
            plt.xlabel('Time', fontsize=14)
            plt.ylabel('Frequency', fontsize=14)
            plt.title('CWT', fontsize=14)
            plt.grid()
            plt.colorbar()
            st.pyplot(plt)
        except Exception as e:
            st.write('Error!')
else:
    # 上傳檔案選項
    uploaded_file = st.file_uploader("Select keypoint data file", type="CSV")
    if uploaded_file:
        empty_element1.text("")
        empty_element3.text("")
        df = pd.read_csv(uploaded_file)
        Data_Arr = df[data_selectXY+trans_select(data_selectPiont)]
        try:
            # WAVELET
            time_series = np.array(Data_Arr.values)
            ts_length = time_series.shape[0]
            ts = time_series.reshape(ts_length,)
            pts_per_second = 60
            fmin = 0.1
            fmax = 1.5 #社區老人做坐到站每秒極限是2.5次
            fstep = 0.01
            taxis = np.linspace(1, ts_length, ts_length)
            taxis = taxis / pts_per_second  # 把單位改成 sec
            x_max = ts_length/pts_per_second  #畫小波圖的X軸的最大值(秒)

            time_series = Data_Arr
            spec = tfa_morlet(time_series, pts_per_second, fmin, fmax, fstep)
            spec_reverse = np.flip(spec, axis=0)
            plt.figure(figsize=(12, 6))
            plt.imshow(spec_reverse, extent=[0, x_max, fmin, fmax], cmap='jet', aspect='auto')
            plt.xlabel('Time', fontsize=14)
            plt.ylabel('Frequency', fontsize=14)
            plt.title('CWT', fontsize=14)
            plt.grid()
            plt.colorbar()
            st.pyplot(plt)
        except Exception as e:
            st.write('Error!')