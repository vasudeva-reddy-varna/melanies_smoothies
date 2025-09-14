# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw: ")



Name_on_order = st.text_input("Name on Smoohie")
st.write("Name on your smoothie will be:", Name_on_order)
cnx= st.connection('snowflake')
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop
pd_df = my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()

ingredients_list =  st.multiselect(
                'Choose upto 5 ingredients', 
                my_dataframe,
                max_selections=5
            )

if ingredients_list:
    ingredients_string=''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen+' '
    st.write(ingredients_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, NAME_ON_ORDER)
            values ('""" + ingredients_string + """','""" + Name_on_order + """')"""
time_to_insert=st.button('Submit Order')
if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered '+Name_on_order+'!', icon="✅")

if ingredients_list:
    ingredients_string=''
    for fruit_chosen in ingredients_list:
        st.subheader(fruit_chosen+" nutrition information")
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+fruit_chosen)
        sf_df=st.dataframe(smoothiefroot_response.json(), use_container_width=True)
