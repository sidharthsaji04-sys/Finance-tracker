import sqlite3
import streamlit as st
from datetime import date 
import pandas as pd
import matplotlib.pyplot as plt

connect=sqlite3.connect("finance_tracker.db")
cur=connect.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS Income(Date text DEFAULT CURRENT_DATE,Amount integer,Source text)")
cur.execute("CREATE TABLE IF NOT EXISTS Expense(Date text DEFAULT CURRENT_DATE,Amount integer,Merchant text)")
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
            i_date=date.today()
            error=self.validate_entry(i_amount,i_source)
            submit_button=st.form_submit_button(label='Enter')
            if submit_button:
                if error:
                  st.error(error)
                else:
                  cur.execute("INSERT INTO Income(Date,Amount,Source) VALUES(?,?,?,)",(i_date,i_amount,i_source))
                  connect.commit()
                  st.write(f'entry saved successfully, added {i_amount}rupees')

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
                plt.bar(df['Date'],df['Amount'])
                st.pyplot(plt)
        st.image('dollar.jpg',use_container_width=True)
                
            

    def e_entry(self):
        st.header('EXPENSE ENTRY PAGE')
        with st.form(key='sample',clear_on_submit=True):
                e_amount=st.number_input('Enter the amount in rupees: ')
                merchant=['others','food','travel','fun','clothes','books','Internet']
                e_merchant=st.selectbox('Where you spent the money',merchant, help='Select where you had spent this amount')
                e_date=date.today()
                error=self.validate_entry(e_amount,e_merchant)
                submit_button=st.form_submit_button(label='Enter')
                if submit_button:
                    if error:
                        st.error(error)
                    else:
                        cur.execute("INSERT INTO Expense(Date,Amount,Merchant) VALUES(?,?,?)",(e_date,e_amount,e_merchant))
                        connect.commit()
                        st.write('Entry saved successfully')

        if st.button('Back to home'):
             st.session_state.page='home'
             st.rerun()

        if st.button('Expense history'):
            df=pd.read_sql_query('SELECT*FROM Expense',connect)
            st.dataframe(df)

        cur.execute("SELECT sum(Amount) FROM Expense")
        total_expense=cur.fetchone()[0]
        st.metric("Total expense",f"₹{total_expense}")

        if st.button('Show graphically'):
                df=pd.read_sql_query("SELECT Date,sum(Amount) AS Amount from Expense GROUP BY Date ORDER BY Date",connect)
                plt.bar(df['Date'],df['Amount'])
                st.pyplot(plt)

        st.image('dollar.jpg',use_container_width=True)


def home_page():
    st.header("Sidharth's personal Finance Tracker💸")

    col1,col2=st.columns(2)
    st.image('money.jpg',use_container_width=True)

    with col1:
        if st.button('Income',use_container_width=True):
            st.session_state.page='in'
            st.rerun()

    with col2:
        if st.button('Expense',use_container_width=True):
            st.session_state.page='ex'
            st.rerun()


    st.sidebar.title('Money in a nutshell')
    cur.execute("SELECT SUM(amount) FROM Income")
    total_income = cur.fetchone()[0] or 0
    st.sidebar.metric("Total Income", f"₹{total_income}")
    cur.execute("SELECT sum(Amount) FROM Expense")
    total_expense=cur.fetchone()[0] or 0
    st.sidebar.metric("Total expense",f"₹{total_expense}")
    remaining_money=(total_income)-total_expense
    st.sidebar.metric("Remaining money",f"₹{remaining_money}")
    st.sidebar.image('sidebar.jpg',use_container_width=True)



f=Finance()
if 'page' not in st.session_state:
    st.session_state.page='home'

if st.session_state.page=='home':
    home_page()
elif st.session_state.page=='in':
    f.i_entry()
elif st.session_state.page=='ex':
    f.e_entry()


          
