import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd


SCOPE=["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"]
@st.cache_resource
def init_connection():
	credentials=Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=SCOPE)
	client=gspread.authorize(credentials)
	return client

CLIENT=init_connection()
SHEET=CLIENT.open("users").sheet1
st.title("somebody's unisex boutique")
tab1,tab2=st.tabs(["login","register"])
with tab1:
	with st.form("login"):
		username=st.text_input("enter username").strip().lower()
		password=st.text_input("enter password").strip()
		users=SHEET.get_all_records()
		if st.form_submit_button("login"):
			if username.lower()=="admin" and password=="blue":
				st.success("admin's view")
				df=pd.DataFrame(users)
				st.dataframe(df)
			else:
				found=False
				for user in users:
					if str(user["username"])==username and str(user["password"])==password:
						found=True
						st.success(f"welcome,{username}")
						break
				if not found:
					st.error("invalid username or password")
with tab2:				
	with st.form("register"):
		users=SHEET.get_all_records()
		username100=st.text_input("enter a username")
		password100=st.text_input("enter password")
		name100=st.text_input("enter your name")
		email100=st.text_input("enter your email")
		if st.form_submit_button("register"):
			SHEET.append_row([username100,password100,name100,email100])

			st.success("registeration complete")	






