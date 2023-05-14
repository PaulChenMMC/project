import pandas as pd
import numpy as np
from scipy.signal import convolve

#Step1

#Step2

#Step3
def calibration(dfA,dfb,sid_select):
    #抓取 sub YX XC
    # 分離csv
    df_filteredB = dfb.loc[dfb['ID'] == sid_select]
    XC = df_filteredB.loc[df_filteredB.index[0], 'xc']
    YC = df_filteredB.loc[df_filteredB.index[0], 'yc']

    # 分離csv
    df_filtered = dfA.loc[dfA['sid'] == sid_select]
    # 為了避免產生SettingWithCopyWarning，要將資料先進行copy再進行操作
    df_filter_copy = df_filtered.copy()
    # 把每一列的標題取出為list，再一一代入進行運算
    for i in list(df_filtered.keys())[2:]:
        # 進行資料XC，YC運算
        if 'x' in i:
            df_filter_copy[i] = df_filtered[i] - XC
        if 'y' in i:
            df_filter_copy[i] = (df_filtered[i] - YC)*-1
    return df_filter_copy

#step4
def trans_select(data_selectPiont):
    if data_selectPiont=="Nose":
        keypiont="1"
    elif data_selectPiont=="LEye":
        keypiont="2"
    elif data_selectPiont=="REye":
        keypiont="3"    
    elif data_selectPiont=="LEar":
        keypiont="4"
    elif data_selectPiont=="REar":
        keypiont="5"
    elif data_selectPiont=="LShouder":
        keypiont="6"
    elif data_selectPiont=="RShouder":
        keypiont="7"
    elif data_selectPiont=="LElbow":
        keypiont="8"
    elif data_selectPiont=="RElbow":
        keypiont="9"
    elif data_selectPiont=="LWrist":
        keypiont="10"
    elif data_selectPiont=="RWrist":
        keypiont="11"
    elif data_selectPiont=="LHip":
        keypiont="12"
    elif data_selectPiont=="RHip":
        keypiont="13"
    elif data_selectPiont=="LKnee":
        keypiont="14"
    elif data_selectPiont=="RKnee":
        keypiont="15"
    elif data_selectPiont=="LAnkle":
        keypiont="16"
    elif data_selectPiont=="RAnkle":
        keypiont="17"
    else:
        keypiont="7"
    return keypiont

def MorletWavelet(fc):
    F_RATIO = 7
    Zalpha2 = 3.3
    
    sigma_f = fc / F_RATIO
    sigma_t = 1 / (2 * np.pi * sigma_f)
    A = 1 / np.sqrt(sigma_t * np.sqrt(np.pi))
    max_t = np.ceil(Zalpha2 * sigma_t)
    
    t = np.arange(-max_t, max_t + 1)
    
    v1 = 1 / (-2 * sigma_t**2)
    v2 = 2j * np.pi * fc
    MW = A * np.exp(t * (t * v1 + v2))
    
    return MW

def tfa_morlet(td, fs, fmin, fmax, fstep):
    TFmap = np.array([])
    for fc in np.arange(fmin, fmax+fstep, fstep):
        MW = MorletWavelet(fc/fs)
        cr = convolve(td, MW, mode='same')
        
        TFmap = np.vstack([TFmap, abs(cr)]) if TFmap.size else abs(cr)
        
    return TFmap

#step5