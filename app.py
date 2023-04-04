import json
import requests
import streamlit as st
st.set_page_config(layout="wide")

st.header('Credit Card Fraud Detection Tool')


###################### Funtions to transform categorical variable #############################################
def type_transaction(content):
    if content == "PAYMENT":
        content = 0
    elif content == "TRANSFER":
        content = 1
    elif content == "CASH_OUT":
        content = 2
    elif content == "DEBIT":
        content = 3
    elif content == "CASH_IN":
        content = 4
    return content


col1, col2 = st.columns(2)

with col1:
    with st.expander("Sender Details"):
        st.image("img/sa.jpg", width=400)
        sender_name = st.text_input(" Sender Name ID")
        ## Transaction information
        type_lebels = ("PAYMENT", "TRANSFER", "CASH_OUT", "DEBIT", "CASH_IN")
        type = st.selectbox(" Type of transaction", type_lebels)
        amount = st.number_input("Amount in $",min_value=0, max_value=110000)
        oldbalanceorg = st.number_input("""Sender Balance Before Transaction was made""",min_value=0, max_value=110000)
        newbalanceOrig = st.number_input("""Sender Balance After Transaction was made""",min_value=0, max_value=110000)

with col2:
    with st.expander("Receiver Details"):
        st.image("img/a.png", width=400)
        receiver_name = st.text_input(" Receiver Name ID")
        oldbalancedest = st.number_input("""Recipient Balance Before Transaction was made""",min_value=0, max_value=110000)
        newbalanceDest = st.number_input("""Recipient Balance After Transaction was made""",min_value=0, max_value=110000)

step = st.slider("Number of Hours it took the Transaction to complete:", min_value = 0, max_value = 744)

## flag 
isflaggedfraud = "Non fraudulent"
if amount >= 200000:
    isflaggedfraud = "Fraudulent transaction"
else:
    isflaggedfraud = "Non fraudulent"


result_button = st.button("Detect Result")
    
    
with st.expander("See explanation"):
    if result_button:

        ## Features
        data = {
            "step": step,
            "type": type_transaction(type),
            "amount": amount,
            "oldbalanceOrg": oldbalanceorg,
            "newbalanceOrig": newbalanceOrig,
            "oldbalanceDest": oldbalancedest,
            "newbalanceDest": newbalanceDest
        }

        ## Transaction detail
        st.write(
            f""" 
            ## **Transaction Details**

            #### **User informantion**:

            Sender Name(ID): {sender_name}\n
            Receiver Name(ID): {receiver_name}

            #### **Transaction information**:

            Number of Hours it took to complete: {step}\n
            Type of Transaction: {type}\n
            Amount Sent: {amount}$\n
            Sender Balance Before Transaction: {oldbalanceorg}$\n
            Sender Balance After Transaction: {newbalanceOrig}$\n
            Recepient Balance Before Transaction: {oldbalancedest}$\n
            Recepient Balance After Transaction: {newbalanceDest}$\n
            System Flag Fraud Status(Transaction amount greater than $200000): {isflaggedfraud}

            """
        )

        st.write("""## **Prediction**""")

        # inference from ml api
        res = requests.post("http://localhost:8000/prediction", json= data)
        json_str = json.dumps(res.json())
        respon = json.loads(json_str)

        if sender_name=='' or receiver_name == '':
            st.write("Error! Please input Transaction ID or Names of Sender and Receiver!")
        else:
            st.write(f"""### The **'{type}'** transaction that took place between {sender_name} and {receiver_name} {respon[0]}.""")



