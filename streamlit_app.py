# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests


helpful_links = [
    "https://docs.streamlit.io"
]

# Write directly to the app
st.title("My parents new healthy dinner")
st.write(
    f"""Replace the code in this example app with your own code! And if you're new to Streamlit, here are some helpful links:
    :page_with_curl: [Streamlit open source documentation]({helpful_links[0]})    
    """
)

name_of_order = st.text_input("Name of the smoothie:")
st.write("The name of your smoothie will be:", name_of_order)




#session = get_active_session()
cnx= st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up 5 to ingradiants:'    
    ,my_dataframe    
    ,max_selections=5
)

ingredients_string = ''

for fruit_chosen in ingredients_list:
    ingredients_string += fruit_chosen + ' '
    st.subheader(fruit_chosen + ' Nutrition Information')
    smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+fruit_chosen)
    sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

st.write(ingredients_string)

my_insert_stmt = """ insert into smoothies.public.orders(ingredients,NAME_ON_ORDER)
            values ('""" + ingredients_string + """','""" + name_of_order + """' )"""

#st.write(my_insert_stmt)

time_to_insert = st.button ('Submit Order')

if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered!', icon="✅")
    st.stop()


#st.text(smoothiefroot_response.json())




