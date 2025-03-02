import streamlit as st
import pandas as pd
import os
from io import BytesIO




# Set up our App

st.set_page_config(page_title="Data Sweeper app", layout="wide")
st.title("💽 AL Gadani Data Sweeper")
st.write("Transfrom your files between CVS or Excel formats with builtin data cleaning and visualization!")

uploaded_files=st.file_uploader(" Upload files (CVS OR Excel):" ,type=["cvs","xlsx"], accept_multiple_files=True)

if uploaded_files:
   for file in uploaded_files:
      file_ext= os.path.splitext(file.name)[-1].lower()


      if file_ext == ".cvs":
        df= pd.read_csv(file)
      elif file_ext ==".xlsx":
        df=pd.read_excel(file)
      else:st.error("Unsupported file type:{file_ext}")

        # Display Info about the file
      st.write(f"**File Name:** {file.name}")
      st.write(f"**File Siz:** {file.size/1024}")

       #Showw 5 Rows of our df
      st.write("Preview the Head of the Dataframe")
      st.dataframe(df.head())

        #Options for data cleaning 
      st.subheader("Data Cleaning options")
      if st.checkbox(f"Clean Data for {file.name}"):
        col1,col2 =st.columns(2) 

        #Choose specific Columns to keep or Covert
        st.subheader("Seclect Columns to Covert")
        columns=st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns)
        df=df[columns]

        # Create Some Visulizations
        st.subheader("Data Visulization")
      if st.checkbox(f"Show Visulization for {file.name}"):
        st.bar_chart(df.select_dtypes(include='number').iloc[:,:2])



        #Convert the files -> CVS to Excel
        st.subheader("Conversion Option")
        conversion_type =st.radio(f"Convert {file.name} to:",["CSV","Execl"],key=file.name)
        if st.button(f"Convert {file.name}"):
          buffer =BytesIO()
          if conversion_type =="CSV":
           df.to_csv(buffer,index=False)
           file_name=file.name.replace(file_ext, ".csv")
           mime_type="text/csv"
          elif conversion_type =="Excel":
              df.to_excel(buffer,index=False)
              file_name=file.name.replace(file_ext,".xlsx")
              mime_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
              buffer.seek(0)

           #Download Button
          st.download_button (label=f"Download {file.name} as {conversion_type}", data=buffer, file_name=file_name,
          mime=mime_type)
          st.subheader("Developed By Muhammad Essa Gadani")
            
          
            