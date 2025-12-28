import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import time

# # # # Teksts

st.write("Hello, let's learn how to build a streamlit app together")
st.title("this is the app title")
st.header("this is the markdown")
st.markdown("## this *is* the header")
st.subheader("this is the subheader")
st.caption("this is the caption")
st.code("x=2021")
st.latex(r''' a+a r^1+a r^2+a r^3 ''')

# # # # Attēli un video vai audio faili.

st.image(r"img\apple.jpg", width=400)
st.video("https://www.youtube.com/watch?v=o6wQ8zAkLxc")

# # # # Ievada lauki

st.checkbox('yes')
st.button('Click')
st.radio('Pick your gender', ['Male', 'Female'])
st.selectbox('Pick your gender', ['Male', 'Female'])
st.multiselect('choose a planet', ['Jupiter', 'Mars', 'Neptune'])
st.select_slider('Pick a mark', ['Bad', 'Good', 'Excellent'])
st.slider('Pick a number', 0, 50)

st.number_input('Pick a number', 0, 10)
st.text_input('Email address')
st.date_input('Travelling date')
st.time_input('School time')
st.text_area('Description')
st.file_uploader('Upload a photo')
st.color_picker('Choose your favorite color')

# # # Progress un statuss

# st.progress(10, text="Wait...")

# with st.spinner('Wait for it...'):
#     time.sleep(10)

# # # # Ziņojumi

st.success("You did it !")
st.error("Error")
st.warning("Warning")
st.info("It's easy to build a streamlit app")
st.exception(RuntimeError("RuntimeError exception"))

# # # Grafiki


chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c'])

st.line_chart(chart_data)

chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=["a", "b", "c"])

st.bar_chart(chart_data)


arr = np.random.normal(1, 1, size=100)
fig, ax = plt.subplots()
ax.hist(arr, bins=20)

st.pyplot(fig)

# # # tabulas

df = pd.DataFrame(
    np.random.randn(10, 5),
    columns=('col %d' % i for i in range(5)))

st.table(df)


df = pd.DataFrame(
    np.random.randn(50, 20),
    columns=('col %d' % i for i in range(20)))

st.dataframe(df)  # Same as st.write(df)

df = pd.DataFrame(np.random.randn(500, 2) /
                  [50, 50] + [37.76, -122.4], columns=['lat', 'lon'])
st.map(df)


# # # Lapas izkārtojums

# add_selectbox = st.sidebar.selectbox(
#     "How would you like to be contacted?",
#     ("Email", "Home phone", "Mobile phone")
# )

# # Using "with" notation

# with st.sidebar:
#     add_radio = st.radio(
#         "Choose a shipping method",
#         ("Standard (5-15 days)", "Express (2-5 days)")
#     )

# # # # Kolonnas

col1, col2, col3 = st.columns(3)

with col1:
    st.header("A cat")
    st.image("https://static.streamlit.io/examples/cat.jpg")

with col2:
    st.header("A dog")
    st.image("https://static.streamlit.io/examples/dog.jpg")

with col3:
    st.header("An owl")
    st.image("https://static.streamlit.io/examples/owl.jpg")

# # cilnes (Tabs)
tab1, tab2, tab3 = st.tabs(["Cat", "Dog", "Owl"])

with tab1:
    st.header("A cat")
    st.image("https://static.streamlit.io/examples/cat.jpg", width=200)

with tab2:
    st.header("A dog")
    st.image("https://static.streamlit.io/examples/dog.jpg", width=200)

with tab3:
    st.header("An owl")
    st.image("https://static.streamlit.io/examples/owl.jpg", width=200)

# # # # # Funkcijas


def display_name(name):
    st.info(f'**Name:** {name}')


name = st.text_input('Please enter your name')

if name:
    display_name(name)


# # # # Pogas

if st.button('Click Me', help='Click this button to perform an action'):
    st.success('You clicked the button!')

if st.button("Congratulations!"):
    st.balloons()


def say_hello():
    st.write('Hello, Streamlit!')


if st.button('Say Hello'):
    say_hello()

# # # # Formas
with st.form('feedback_form'):
    st.header('Feedback form')

    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input('Please enter your name')
        rating = st.slider('Please rate this app', 0, 10, 5)
    with col2:
        dob = st.date_input('Please enter your date of birth')
        recommend = st.radio(
            'Would you recommend this app to others?', ('Yes', 'No'))
    submit_button = st.form_submit_button('Submit')
if submit_button:
    st.write('**Name:**', name, '**Date of birth:**', dob,
             '**Rating:**', rating, '**Would recommend?:**', recommend)


# # # Mainīgie un ievada vērtības

st.title("My Streamlit App")

value1 = st.slider("Select a value", key="value1")
value2 = st.slider("Select a value", key="value2")
pd = pd.DataFrame({
    'values': [value1, value2],
})
st.bar_chart(pd)
