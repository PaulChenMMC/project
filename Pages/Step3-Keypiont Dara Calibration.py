import streamlit as st
import tkinter as tk
import pandas as pd
from func import calibration
import io

st.title("Step3-Keypiont Dara Calibration")


#選擇多個檔案
multiple_files_selected = st.file_uploader("Select JointData & SubjectBboxData csv file", type="CSV", accept_multiple_files=True, key=None)
#設立空值以利後續判斷
file_A=""
file_B=""
#判斷選擇檔案是否為要校正的檔案
if multiple_files_selected is not None:
    # 取得檔案名稱
    for file in multiple_files_selected:
        if "jointdata.csv" in file.name.lower():
            file_A = file
        elif "subjectbboxdata.csv" in file.name.lower():
            file_B = file

#兩個用來校正的檔案都有選到
if  file_A and file_B :
    #讀取檔案SID ID 有幾種
    dfA = pd.read_csv(file_A)
    dfB = pd.read_csv(file_B)
    options = dfB.iloc[:, 1].unique()
    #產出下拉選單
    sid_select = st.selectbox('請選擇 SID ID', options)
    #執行校正
    if st.button("Data Calibration"):
        df_filter_copy=calibration(dfA,dfB,sid_select)
        csv_file = df_filter_copy.to_csv(index=False)
        st.session_state.df=pd.read_csv(io.StringIO(csv_file))
        # 提供下載按鈕讓使用者下載 CSV 檔案
        st.download_button(
            label="Download Calibration Data",
            data=csv_file,
            file_name=f"Result_{sid_select}_{file_A.name}",
            mime='text/csv'
        )
