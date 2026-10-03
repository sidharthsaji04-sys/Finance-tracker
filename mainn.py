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
connect.close()


class Finance:
    def validate_entry(self,amount, *text_fields):
        if amount <= 0:
         return "Amount must be greater than 0."
        for field in text_fields:
            if field.strip() == "":
              return "All fields must be filled in. Enter all values again"
        return None 
        
    def i_entry(self):
        connect=sqlite3.connect("finance_tracker.db")
        cur=connect.cursor()
        st.header('INCOME ENTRY PAGE')
        with st.form(key='sample',clear_on_submit=True):
            i_amount=st.number_input('Enter the amount in rupees: ')
            sources=["Other","Salary","Business","Pocket Money","Gifts","Part-time Work","Investment Returns","Refund"]
            i_source=st.selectbox('Income Source',sources,help='From where do you get this amount')
            i_date=date.today()
            error=self.validate_entry(i_amount,i_source)
            submit_button=st.form_submit_button(label='Enter')

            if submit_button:
                if error:
                  st.error(error)
                else:
                  
                  cur.execute("INSERT INTO Income(Date,Amount,Source) VALUES(?,?,?)",(i_date,i_amount,i_source))
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
        connect.close()
        st.image('dollar.jpg',use_container_width=True)
                
            

    def e_entry(self):
        connect=sqlite3.connect("finance_tracker.db")
        cur=connect.cursor()
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
        connect.close()
        st.image('dollar.jpg',use_container_width=True)

class Login:
    def user_login(self):
        st.header("Personal Finance Tracker")
        connect=sqlite3.connect('User_info.db')
        cursor=connect.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS User_data(Login_date text DEFAULT CURRENT_DATE,User_name text,password text)")
        st.subheader('Are you a new user or existing one')
        if 'login_mode' not in st.session_state:
            st.session_state.login_mode = None

        col1,col2=st.columns(2)
        with col1:
                if st.button('Existing user',use_container_width=True):
                    st.session_state.login_mode = 'login'
                    st.rerun()
                
        with col2:
                if st.button('New user',use_container_width=True):
                    st.session_state.login_mode = 'signup'
                    st.rerun()

        if st.session_state.login_mode == 'login':
                st.subheader('Existing user')
                with st.form(key='login form'):
                    name=st.text_input('Enter your name: ',key='login_name',help="This is your user name")
                    password=st.text_input('Enter your password: ',key='login_password',type='password')
                    if st.form_submit_button('Enter'):
                        user=cursor.execute(
                            "SELECT 1 FROM User_data WHERE User_name=? AND password=?",
                            (name.strip(),password)
                        ).fetchone()
                        if user:
                            st.session_state.page='home'
                            st.rerun()
                        else:
                            st.error('Invalid user name or password.')

        elif st.session_state.login_mode == 'signup':
                st.subheader('Welcome to your all in one place for money')
                with st.form(key='signup form'):
                    name=st.text_input('Enter your name: ',key='signup_name',help="This is your user name")
                    password=st.text_input('Enter your new password: ',key='signup_password',type='password')
                    if st.form_submit_button('Enter',key='j'):
                        name=name.strip()
                        if not name or not password:
                            st.error('Enter both a user name and password.')
                        elif cursor.execute("SELECT 1 FROM User_data WHERE User_name=?",(name,)).fetchone():
                            st.error('That user name already exists.')
                        else:
                            cursor.execute(
                                "INSERT INTO User_data(User_name,password) VALUES(?,?)",
                                (name,password)
                            )
                            connect.commit()
                            st.session_state.page='home'
                            st.rerun()

            
    def home_page(self):
        st.header("Personal Finance Tracker")
        st.caption("Made by Sidharth")
        st.caption("Money is not a paper, it's Power")

        col1, col2 = st.columns(2)
        st.image('money.jpg', use_container_width=True)

        with col1:
            if st.button('Income', use_container_width=True):
                st.session_state.page = 'in'
                st.rerun()

        with col2:
            if st.button('Expense', use_container_width=True):
                st.session_state.page = 'ex'
                st.rerun()

        st.sidebar.title('Your finance in a nutshell')
        connect=sqlite3.connect("finance_tracker.db")
        cur=connect.cursor()
        cur.execute("SELECT SUM(amount) FROM Income")
        total_income = cur.fetchone()[0] or 0
        st.sidebar.metric("Total Income", f"Rs{total_income}")
        cur.execute("SELECT sum(Amount) FROM Expense")
        total_expense = cur.fetchone()[0] or 0
        st.sidebar.metric("Total expense", f"Rs{total_expense}")
        remaining_money = total_income - total_expense
        st.sidebar.metric("Remaining money", f"Rs{remaining_money}")
        connect.close()
        st.sidebar.image('sidebar.jpg', use_container_width=True)

f=Finance()
l=Login()

if 'page' not in st.session_state:
    st.session_state.page='login'

if st.session_state.page=='login':
    l.user_login()
elif st.session_state.page=='home':
    l.home_page()
elif st.session_state.page=='in':
    f.i_entry()
elif st.session_state.page=='ex':
    f.e_entry()


          
