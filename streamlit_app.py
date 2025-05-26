# # Import python packages
# import streamlit as st
# import requests
# import pandas as pd
# from snowflake.snowpark.functions import col, when_matched
# from snowflake.snowpark.context import get_active_session

# # Write directly to the app
# st.title(f"Customize Your Smoothie!  :cup_with_straw:")
# st.write(
#     """Choose the fruits you want in your custom smoothie!
#     """
# )

# name_on_order = st.text_input('Name on Smoothie:')
# st.write('The name on your Smoothie will be: ', name_on_order)

# cnx = st.connection("snowflake")
# session = cnx.session()  


# my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
# #st.dataframe(data=my_dataframe, use_container_width=True)
# #st.stop()


# #Convert the snowpark dataframe to a pandas dataframe so we canuse the LOC function 
# pd_df = my_dataframe.to_pandas()
# st.dataframe(pd_df)




# ingredients_list = st.multiselect(
#     'Choose up to 5 ingredients: ',
#     my_dataframe,
#     max_selections=5
# )

# if ingredients_list:
#     ingredients_string = ' '

#     for fruit_chosen in ingredients_list:
#         ingredients_string += fruit_chosen + ' '

#         search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
#         #st.write('The search value for ', fruit_chosen,' is ', search_on)
        
        
#         st.subheader(fruit_chosen + ' Nutrition Information')
#         smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)
#         sf_df = st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)

    
#         # my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
#         #     values ('""" + ingredients_string + """', '""" + name_on_order + """')"""
#     time_to_insert = st.button('Submit Order')
#     if time_to_insert:
#         session.sql(my_insert_stmt).collect()
#         st.success(f'Your Smoothie is ordered! Name on order: {name_on_order} ✅ ')



# Import python packages
import streamlit as st
import requests
import pandas as pd
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f"Customize Your Smoothie!  :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothie!
    """
)

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be: ', name_on_order)

# Snowflake connection
cnx = st.connection("snowflake")
session = cnx.session()

# Get fruit options from Snowflake
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))

# Convert Snowpark DataFrame to Pandas DataFrame
pd_df = my_dataframe.to_pandas()
st.dataframe(pd_df)

# Ingredient selector
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    pd_df['FRUIT_NAME'].tolist(),  # <- use list from Pandas, not Snowpark df
    max_selections = 6
)

if ingredients_list:
    ingredients_string = ' '.join(ingredients_list)  # cleaner join

    for fruit_chosen in ingredients_list:
        # Safely get SEARCH_ON value
        search_row = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON']
        if not search_row.empty and pd.notnull(search_row.iloc[0]):
            search_on = search_row.iloc[0]
            st.subheader(fruit_chosen + ' Nutrition Information')
            smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)
            st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
        else:
            st.warning(f"No search value found for {fruit_chosen}")

    # Build the insert statement
    my_insert_stmt = f"""INSERT INTO smoothies.public.orders(ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{name_on_order}')"""

    # Submit button
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered! Name on order: {name_on_order} ✅ ')
















#new section to display smoothiefroot nutrition

