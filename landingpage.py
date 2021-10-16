import streamlit as st



st.title("Missinformation Detection")
st.text("")
st.text("")

user_input = st.text_input("Enter the content: ")
type_input = st.selectbox("What type of the content you want us to evaluate?",
            ("Text Content", "URL"))
button_submit = st.button("Submit")
if(button_submit):
    if(type_input == "Text Content"):
        st.text("You have picked Text Content")
    elif(type_input == "URL"):   
        st.text("You have picked URL")
    #Processing data
    #point = 
    #suggested source of information
    point = 90 #sample code
    suggested_art =  ["https://www.washingtonexaminer.com", "facebook.com"]
    st.text("After evaluating, we have the following report for you: ")
    
    st.text("Point: %d" % (int(point)))
    st.text("Suggested reliable article: ")
    for x in suggested_art:
        st.write("[%s](%s)"%(x,x))

    

