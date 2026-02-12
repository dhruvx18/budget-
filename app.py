import streamlit as st
import pandas as pd
import os

# Page Config
st.set_page_config(page_title="Budget Tracker", page_icon="💰")

EXCEL_FILE = "budget_data.xlsx"

# --- DATABASE LOGIC ---
def load_data():
    if os.path.exists(EXCEL_FILE):
        return pd.read_excel(EXCEL_FILE)
    else:
        # Create empty dataframe if file doesn't exist
        return pd.DataFrame(columns=["Date", "Amount", "Item Name", "Description", "Mode"])

df = load_data()

st.title("Finance Tracker")

# --- INPUT SECTION ---
with st.form("budget_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    
    with col1:
        date = st.date_input("Date")
        amount = st.number_input("Amount Spent", min_value=0.0, step=1.0)
    
    with col2:
        item_name = st.text_input("Item Name")
        mode = st.selectbox("Mode", ["Cash", "Credit Card", "Debit Card", "UPI", "Net Banking"])
        
    description = st.text_area("Description")
    
    submitted = st.form_submit_button("Save Record Entry")

    if submitted:
        if item_name and amount > 0:
            # Create new row
            new_data = pd.DataFrame([{
                "Date": date,
                "Amount": amount,
                "Item Name": item_name,
                "Description": description,
                "Mode": mode
            }])
            
            # Combine and save
            updated_df = pd.concat([df, new_data], ignore_index=True)
            updated_df.to_excel(EXCEL_FILE, index=False)
            st.success("Record Saved Successfully!")
            st.rerun() # Refresh to show data in the table below
        else:
            st.error("Please provide an Item Name and Amount.")

# --- DISPLAY & DELETE SECTION ---
st.divider()
st.subheader("Recent Entries")

if not df.empty:
    # Display the table
    st.dataframe(df, use_container_width=True)
    
    # Delete Logic
    st.subheader("Delete a Record")
    row_to_delete = st.number_input("Enter Row Index to Delete", min_value=0, max_value=len(df)-1, step=1)
    
    if st.button("Delete Record"):
        df = df.drop(df.index[row_to_delete])
        df.to_excel(EXCEL_FILE, index=False)
        st.warning(f"Record {row_to_delete} deleted.")
        st.rerun()
else:
    st.info("No records found yet. Add your first expense above!")