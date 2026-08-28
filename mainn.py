import sqlite3
import streamlit as st
from datetime import date 
import pandas as pd
import matplotlib.pyplot as plt

connect=sqlite3.connect("finance_tracker.db")
cur=connect.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS Income(Date text DEFAULT CURRENT_DATE,Amount integer,Source text, Save_percent integer,Aim text)")
cur.execute("CREATE TABLE IF NOT EXISTS Expense(Date text DEFAULT CURRENT_DATE,Amount integer,Merchant text,Description text)")
cur.execute("CREATE TABLE IF NOT EXISTS Savings(Date text DEFAULT CURRENT_DATE,Amount integer,Source text,savings integer,Total integer)")
connect.commit()


class Finance:
    def validate_entry(self,amount, *text_fields):
        if amount <= 0:
         return "Amount must be greater than 0."
        for field in text_fields:
            if field.strip() == "":
              return "All fields must be filled in. Enter all values again"
        return None 
        
    def i_entry(self):
        st.header('INCOME ENTRY PAGE')
        with st.form(key='sample',clear_on_submit=True):
            i_amount=st.number_input('Enter the amount in rupees: ')
            sources=['relatives','bus_fee_balance','random_find','others']
            i_source=st.selectbox('Source',sources)
            aims=['no idea','fun','book','others','travel']
            i_aim=st.selectbox('Enter your plan on how to spend this money: ',aims)
            percentages=[0,10,20,50,80,100]
            i_save_percent=st.selectbox('Saving_percentage',percentages)
            i_balance=i_amount - i_amount*(i_save_percent/100)
            i_saving=i_amount*(i_save_percent/100)
            i_date=date.today()
            error=self.validate_entry(i_amount,i_source,i_aim)
            submit_button=st.form_submit_button(label='Enter')
            if submit_button:
                if error:
                  st.error(error)
                else:
                  cur.execute("INSERT INTO Income(Date,Amount,Source,Save_percent,Aim,Balance) VALUES(?,?,?,?,?,?)",(i_date,i_amount,i_source,i_save_percent,i_aim,i_balance))
                  cur.execute("INSERT INTO Savings(Date,Amount,Source,savings) VALUES(?,?,?,?)",(i_date,i_amount,i_source,i_saving))
                  connect.commit()
                  st.write(f'entry saved successfully, added {i_balance}rupees')

        if st.button('Back to home'):
            st.session_state.page='home'
            st.rerun()

        if st.button('Income history👇'):
            df=pd.read_sql_query('SELECT*FROM Income',connect)
            st.dataframe(df)
            cur.execute("SELECT SUM(amount) FROM Income")
            total_income = cur.fetchone()[0]
            st.metric("Total Income", f"₹{total_income}")
        if st.button('Show graphically'):
                df=pd.read_sql_query("SELECT Date,sum(Amount) AS Amount from Income GROUP BY Date ORDER BY Date",connect)
                plt.plot(df['Date'],df['Amount'])
                st.pyplot(plt)
        st.image('dollar.jpg',use_container_width=True)
                
            

    def e_entry(self):
        st.header('EXPENSE ENTRY PAGE')
        with st.form(key='sample',clear_on_submit=True):
                e_amount=st.number_input('Enter the amount in rupees: ')
                merchant=['food','travel','fun','clothes','books','others']
                e_merchant=st.selectbox('Where you spent the money',merchant)
                e_description=st.text_input('Add a description: ')
                e_date=date.today()
                error=self.validate_entry(e_amount,e_merchant,e_description)
                submit_button=st.form_submit_button(label='Enter')
                if submit_button:
                    if error:
                        st.error(error)
                    else:
                        cur.execute("INSERT INTO Expense(Date,Amount,Merchant,Description) VALUES(?,?,?,?)",(e_date,e_amount,e_merchant,e_description))
                        connect.commit()
                        st.write('Entry saved successfully')

        if st.button('Back to home'):
             st.session_state.page='home'
             st.rerun()

        if st.button('Expense history'):
            df=pd.read_sql_query('SELECT*FROM Expense',connect)
            st.dataframe(df) 

        if st.button('Show graphically'):
                df=pd.read_sql_query("SELECT Date,sum(Amount) AS Amount from Expense GROUP BY Date ORDER BY Date",connect)
                plt.plot(df['Date'],df['Amount'])
                st.pyplot(plt)

        st.image('dollar.jpg',use_container_width=True)


    def savings(self):
        st.header('SAVINGS')
        df=pd.read_sql_query('SELECT*FROM Savings',connect)
        st.dataframe(df)
        cur.execute("SELECT SUM(savings) FROM savings")
        total_saved = cur.fetchone()[0]
        st.metric("Total Savings", f"₹{total_saved}")
        st.image('dollar.jpg',use_container_width=True)


def home_page():
    st.header("Sidharth's personal Finance Tracker💸")

    col1,col2,col3=st.columns(3)
    st.image('money.jpg',use_container_width=True)

    with col1:
        if st.button('Income',use_container_width=True):
            st.session_state.page='in'
            st.rerun()

    with col2:
        if st.button('Expense',use_container_width=True):
            st.session_state.page='ex'
            st.rerun()

    with col3:
            if st.button('Savings',use_container_width=True):
                st.session_state.page='sa'
                st.rerun()


f=Finance()
if 'page' not in st.session_state:
    st.session_state.page='home'

if st.session_state.page=='home':
    home_page()
elif st.session_state.page=='in':
    f.i_entry()
elif st.session_state.page=='ex':
    f.e_entry()
elif st.session_state.page=='sa':
    f.savings()

          
