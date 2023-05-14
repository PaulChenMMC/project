import streamlit as st
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
import pandas as pd

st.title("Step5-Cluster Visualization")

if 'x1' not in st.session_state:
    st.session_state.x1 = None


if st.session_state.x1 is None:
    fname = "out_cwt.csv"
    df=pd.read_csv(fname)

    dfX = df.drop(df.columns[0:2], axis=1)
    numpyX = dfX.values

    dfY = df[' class']
    numpyY = dfY.values

    tsne = TSNE(perplexity=3, n_components=2, init='pca', n_iter=500)
    x1 = tsne.fit_transform(numpyX, numpyY)
    st.session_state.x1=x1
    st.session_state.numpyY=numpyY
    

plt.figure(figsize=(12,6))
plt.scatter(st.session_state.x1[:, 0], st.session_state.x1[:, 1], c=st.session_state.numpyY, cmap="jet") #we have 5 classes
st.pyplot(plt.gcf())