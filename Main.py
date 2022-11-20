from string import whitespace
import streamlit as st
import re
import numpy as np
from tkinter import VERTICAL
from streamlit_option_menu import option_menu
import time as tm

st.set_page_config(layout="wide")

with open("styles.css") as f:
    st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

heading = "<div class='title'>Page Replacement Algorithms</heading1>"
st.markdown(heading, unsafe_allow_html=True)
A = []
try:
    numbers = st.text_input("Enter Page Reference String below..")

    def collect_numbers(x): return [int(round(float(i)))
                                    for i in re.split("[^0-9.]", x) if i != ""]
    A = collect_numbers(numbers)
    fnum = 0
except ValueError:
    st.error("You have Entered Invalid Page reference string")


if(len(A) > 0):
    c1, c2, x3 = st.columns([4, 5, 7])
    with c1:
        st.markdown("Total number of frames : ")
    with c2:
        fnum = st.selectbox('', [k for k in range(1, len(set(A))+1)])
    def showA(A):
        st = ""
        for k in A:
            st += str(k)+" "
        return st[:-1]

    def showB(A, l):
        st = ""
        for i in range(len(A)):
            if(i == int(l)-1):
                st += "^ "
            else:
                st += "  "
        return st[:-1]

    st.write("Frames : ", fnum)
    st.write("Current String ("+str(len(A))+") :", *A, sep=" ")

line = "<hr class='line'>"
st.markdown(line, unsafe_allow_html=True)


def FIFO(A, n):
    beg = tm.time()
    F = []
    X = ["&emsp;"]*n
    x = 0
    l = 0
    for k in A:
        if(k not in X):
            Y = X.copy()
            Y[x] = k
            F.append(Y)
            x = (x+1) % n
            X = Y.copy()
        else:
            F.append(["&emsp;"]*n)
            l += 1
    F = np.transpose(F)
    end = tm.time()
    return F.tolist(), len(A)-l,end-beg


def LRU(A, n):
    beg = tm.time()
    F = []
    X = ["&emsp;"]*n
    x = l = i = f = 0
    for j in range(len(A)):
        Y = X.copy()
        if(A[j] not in Y):
            if(f >= n):
                K = [A[:j][::-1].index(k) for k in Y]
                Y[Y.index(A[:j][::-1][max(K)])] = A[j]
            else:
                Y[x] = A[j]
                f += 1
                x += 1
            F.append(Y)
        else:
            F.append(["&emsp;"]*n)
            l += 1
        X = Y.copy()
    F = np.transpose(F)
    end = tm.time()
    return F.tolist(), len(A)-l,end-beg


def Optimal(A, n):
    beg = tm.time()
    F = []
    X = ["&emsp;"]*n
    x = l = i = f = 0
    for j in range(len(A)):
        Y = X.copy()
        if(A[j] not in Y):
            if(f >= n):
                K = []
                for k in Y:
                    if(k not in A[j+1:]):
                        Y[Y.index(k)] = A[j]
                        break
                    else:
                        K.append(A[j+1:].index(k))
                else:
                    Y[Y.index(A[j+1:][max(K)])] = A[j]
            else:
                Y[x] = A[j]
                f += 1
                x += 1
            F.append(Y)
        else:
            F.append(["&emsp;"]*n)
            l += 1
        X = Y.copy()
    F = np.transpose(F)
    end = tm.time()
    return F.tolist(), len(A)-l,end-beg


def Ans(A, B, n, pf):
    if(len(A) > 0):
        m = "<div class='Ans'>"
        for x in B:
            m += "<p>"
            m += "".join(["<code>"+str(y)+"</code>&emsp;" for y in x])
            m += "</p>"
        st.markdown(m+"</div>", unsafe_allow_html=True)
        
           


col1, col2 = st.columns([3, 9])
with col1:
    choice = option_menu("", ["FIFO", "LRU(Least Recently Used)",
                         "Optimal", "Compare all"], orientation=VERTICAL)
    if(len(A)>0):
        if choice == "FIFO":
            with col2:
                B, pf,Etime = FIFO(A, fnum)
                UBtime = 0.000010004 * len(A)
                if(len(B)>0 and len(B[0])<=15):
                    Ans(A, B, fnum, pf)
                else:
                    st.write("(To long to Show)")
                Etime,UBtime = "{:.8f} Seconds".format(Etime),"{:.8f} Seconds".format(UBtime)
                
                st.markdown("<h2>Page Faults : "+str(pf) + "</h2><br><h2>Time : "+str(Etime) + "</h2>", unsafe_allow_html=True)
                st.markdown("<h2>Uppper Bound : "+str(UBtime)+"</h2>", unsafe_allow_html=True)

        elif choice == "LRU(Least Recently Used)":
            with col2:
                B, pf,Etime = LRU(A, fnum)
                UBtime = 0.00000045786 * len(A) * len(A)
                if(len(B)>0 and len(B[0])<=15):
                    Ans(A, B, fnum, pf)
                else:
                    st.write("(To long to Show)")
                Etime,UBtime = "{:.8f} Seconds".format(Etime),"{:.8f} Seconds".format(UBtime)
                
                st.markdown("<h2>Page Faults : "+str(pf) + "</h2><br><h2>Time : "+str(Etime) + "</h2>", unsafe_allow_html=True)
                st.markdown("<h2>Uppper Bound : "+str(UBtime)+"</h2>", unsafe_allow_html=True)
        elif choice == "Optimal":
            with col2:
                B, pf,Etime = Optimal(A, fnum)
                UBtime = 0.000000404119 * len(A) * len(A)
                if(len(B)>0 and len(B[0])<=15):
                    Ans(A, B, fnum, pf)
                else:
                    st.write("(To long to Show)")
                Etime,UBtime = "{:.8f} Seconds".format(Etime),"{:.8f} Seconds".format(UBtime)
                
                st.markdown("<h2>Page Faults : "+str(pf) + "</h2><br><h2>Time : "+str(Etime) + "</h2>", unsafe_allow_html=True)
                st.markdown("<h2>Uppper Bound : "+str(UBtime)+"</h2>", unsafe_allow_html=True)
        else:
            with col2:
                D = {"a": "LRU", }
                B, a,Etime1 = LRU(A, fnum)
                B, b,Etime2 = FIFO(A, fnum)
                B, c,Etime3 = Optimal(A, fnum)
                Etime1,Etime2,Etime3 = ["{:.6f}".format(Etime1),"{:.6f}".format(Etime2),"{:.6f}".format(Etime3)]
                X = [[a,Etime1, "LRU"], [b,Etime2, "FIFO"], [c,Etime3, "Optimal"]]
                X.sort(key=lambda y: y[1])
                final = """<table class='Final' align="center">
                <th>Algorithm</th><th>Execution time(s)</th><th>Total Page Fault</th>"""
                for k in X:
                    final += "<tr><td>" + str(k[2])+"</td><td>" + str(k[1])+"</td><td>"+str(k[0])+"</td></tr>"
                final += "</table>"
                st.markdown(final, unsafe_allow_html=True)
