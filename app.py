import streamlit as st
import pickle
import pandas as pd
import numpy as np
from PIL import Image

model = pickle.load(open('model.pkl', 'rb'))


st.set_page_config(
    page_title="Heart-Healthy",
    page_icon="img/heart_logo.jpg",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.title("Welcome to Heart Healthy")
co1, co2 = st.beta_columns([1, 1])
with co1:
    st.subheader("We are a food recommendation engine, whose mission is to provide you with recipes tailored to fit your nutrition needs and preferences.")
    button_temp = """
    <div style="padding:1px">
    <h4 style="color:black;text-align:left">Please complete the form on the left and click on the button below.</h4>
    </div>
    """
    st.markdown(button_temp, unsafe_allow_html=True)
with co2:
    image = Image.open('img/heart_logo.jpg')
    st.image(image, use_column_width=False, width=172)


def predict_age(gender,	age, calories,	difficulty,	food_types):
    input = np.array(
        [[gender,	age, calories,	difficulty,	food_types]]).astype(np.float64)
    prediction = model.predict(input)
    #pred = '{0:.{1}f}'.format(prediction[0][0], 2)
    return int(prediction)


def main():

    gender_choices = {0: "F", 1: "M"}

    def format_func(option):
        return gender_choices[option]

    difficulty_choices = {0: 'Easy', 1: 'Medium', 2: 'Hard'}

    def format_func1(option):
        return difficulty_choices[option]

    food_type_choices = {0: 'Low-Calories', 1: 'Non-veg',
                         2: 'Veg', 3: 'Veg dessert', 4: 'Non-Veg dessert'}

    def format_func2(option):
        return food_type_choices[option]
    with st.sidebar:
        html_temp = """
        <div style="background:#ca1f1b ;padding:10px">
        <h4 style="color:white;text-align:center; padding-bottom : 5px">Let us customize your meal</h2>
        </div>
        """
        st.markdown(html_temp, unsafe_allow_html=True)
        gender = st.selectbox("Select Gender", options=list(
            gender_choices.keys()), format_func=format_func)
        age = st.number_input("Age",  value=50)
        calories = st.number_input("Calories",  value=500)
        difficulty = st.selectbox("Select Difficulty", options=list(
            difficulty_choices.keys()), format_func=format_func1)
        food_types = st.selectbox("Select Food Type", options=list(
            food_type_choices.keys()), format_func=format_func2)

    def return_recipe(data, output, food_types):
        recipes_df = pd.read_csv(data)
        temp_df = recipes_df[(recipes_df['calorie_level'] == output) & (
            recipes_df['food_types'] == food_types)]
        temp_df = temp_df[['name', 'ingredients',
                           'minutes', 'steps', 'total fat (PDV)', 'sugar (PDV)', 'sodium (PDV)',
                           'protein (PDV)', 'saturated fat (PDV)', 'carbohydrates (PDV)']]
        return temp_df.sample(n=1)

    def return_recipe3(data, output, food_types):
        recipes_df = pd.read_csv(data)
        temp_df = recipes_df[(recipes_df['calorie_level'] == output) & (
            recipes_df['food_types'] == food_types)]
        temp_df = temp_df[['name', 'ingredients',
                           'minutes', 'steps', 'total fat (PDV)', 'sugar (PDV)', 'sodium (PDV)',
                           'protein (PDV)', 'saturated fat (PDV)', 'carbohydrates (PDV)']]
        return temp_df.sample(n=3)

    if st.button("Show Me!!"):
        output = predict_age(gender,	age, calories,	difficulty,	food_types)
        if output == 0:
            recipe = return_recipe("recipes.csv", output, food_types)
            st.success('{}'.format(recipe.to_string(
                columns=['name'], header=False, index=False).upper()))
            st.subheader("Nutritional Value")
            st.table(recipe[['total fat (PDV)', 'sugar (PDV)', 'sodium (PDV)',
                             'protein (PDV)', 'saturated fat (PDV)', 'carbohydrates (PDV)']].assign(hack='').set_index('hack'))
            my_expander = st.beta_expander(
                "Click for Ingredients and Steps", expanded=False)
            with my_expander:
                st.subheader("Ingredients")
                st.info('{}'.format(recipe.to_string(
                    columns=['ingredients'], header=False, index=False)))

                recipe_html = (recipe[['steps']].rename(columns={'steps': ''}).assign(hack='').set_index('hack').style
                               .set_properties(**{'background-color': 'black',
                                                  'font-size': '10pt',
                                                  'color': 'lawngreen',
                                                  'border-color': 'white'}))
                st.subheader('Steps')
                st.table(recipe_html)
            # Space out the maps so the first one is 2x the size of the other three
            col1, col2, col3, col4, col5, col6, col7 = st.beta_columns(
                (1, 1, 1, 1, 1, 1, 1))
            original = Image.open('img/star.png')
            col1.write("Leave a rating")
            col1.image(original, use_column_width=True)

            grayscale = Image.open('img/shopping_cart.png').convert('RGB')
            col3.write("Add Recipe ingredients to your shopping list")
            col3.image(grayscale, use_column_width=True)

            star = Image.open('img/bookmark.png').convert('RGB')
            col5.write("Save the recipe for easy future access")
            col5.image(star, use_column_width=True)

            message = Image.open('img/message.png').convert('RGB')
            col7.write("Please leave a comment")
            col7.image(message, use_column_width=True)

            st.subheader("Share")
            with st.beta_expander("Did you cook this recipe?", expanded=True):
                c1, c2 = st.beta_columns([1, 1])
                with c1:
                    st.write("If you are proud of it, share it on Instagram")
                with c2:
                    st.image("img/instagram.jpg", width=60)

            st.subheader("More Recommendations")
            recipes3 = return_recipe3("recipes.csv", output, food_types)
            st.error('{}'.format(recipes3['name'].iloc[0].upper()))
            st.warning('{}'.format(recipes3['name'].iloc[1].upper()))
            st.error('{}'.format(recipes3['name'].iloc[2].upper()))

        elif output == 1:
            return_recipe("recipes.csv", output, food_types)
            st.success('{}'.format(recipe.to_string(
                columns=['name'], header=False, index=False).upper()))
            st.subheader("Nutritional Value")
            st.table(recipe[['total fat (PDV)', 'sugar (PDV)', 'sodium (PDV)',
                             'protein (PDV)', 'saturated fat (PDV)', 'carbohydrates (PDV)']].assign(hack='').set_index('hack'))
            my_expander = st.beta_expander(
                "Click for Ingredients and Steps", expanded=False)
            with my_expander:
                st.subheader("Ingredients")
                st.info('{}'.format(recipe.to_string(
                    columns=['ingredients'], header=False, index=False)))

                recipe_html = (recipe[['steps']].rename(columns={'steps': ''}).assign(hack='').set_index('hack').style
                               .set_properties(**{'background-color': 'black',
                                                  'font-size': '10pt',
                                                  'color': 'lawngreen',
                                                  'border-color': 'white'}))
                st.subheader('Steps')
                st.table(recipe_html)
            # Space out the maps so the first one is 2x the size of the other three
            col1, col2, col3, col4, col5, col6, col7 = st.beta_columns(
                (1, 1, 1, 1, 1, 1, 1))
            original = Image.open('img/star.png')
            col1.write("Leave a rating")
            col1.image(original, use_column_width=True)

            grayscale = Image.open('img/shopping_cart.png').convert('RGB')
            col3.write("Add Recipe ingredients to your shopping list")
            col3.image(grayscale, use_column_width=True)

            star = Image.open('img/bookmark.png').convert('RGB')
            col5.write("Save the recipe for easy future access")
            col5.image(star, use_column_width=True)

            message = Image.open('img/message.png').convert('RGB')
            col7.write("Please leave a comment")
            col7.image(message, use_column_width=True)

            st.subheader("Share")
            with st.beta_expander("Did you cook this recipe?", expanded=True):
                c1, c2 = st.beta_columns([1, 1])
                with c1:
                    st.write("If you are proud of it, share it on Instagram")
                with c2:
                    st.image("img/instagram.jpg", width=60)

            st.subheader("More Recommendations")
            recipes3 = return_recipe3("recipes.csv", output, food_types)
            st.error('{}'.format(recipes3['name'].iloc[0].upper()))
            st.warning('{}'.format(recipes3['name'].iloc[1].upper()))
            st.error('{}'.format(recipes3['name'].iloc[2].upper()))
        elif output == 2:
            
            return_recipe("recipes.csv", output, food_types)
            st.success('{}'.format(recipe.to_string(
                columns=['name'], header=False, index=False).upper()))
            st.subheader("Nutritional Value")
            st.table(recipe[['total fat (PDV)', 'sugar (PDV)', 'sodium (PDV)',
                             'protein (PDV)', 'saturated fat (PDV)', 'carbohydrates (PDV)']].assign(hack='').set_index('hack'))
            my_expander = st.beta_expander(
                "Click for Ingredients and Steps", expanded=False)
            with my_expander:
                st.subheader("Ingredients")
                st.info('{}'.format(recipe.to_string(
                    columns=['ingredients'], header=False, index=False)))

                recipe_html = (recipe[['steps']].rename(columns={'steps': ''}).assign(hack='').set_index('hack').style
                               .set_properties(**{'background-color': 'black',
                                                  'font-size': '10pt',
                                                  'color': 'lawngreen',
                                                  'border-color': 'white'}))
                st.subheader('Steps')
                st.table(recipe_html)
            # Space out the maps so the first one is 2x the size of the other three
            col1, col2, col3, col4, col5, col6, col7 = st.beta_columns(
                (1, 1, 1, 1, 1, 1, 1))
            original = Image.open('img/star.png')
            col1.write("Leave a rating")
            col1.image(original, use_column_width=True)

            grayscale = Image.open('img/shopping_cart.png').convert('RGB')
            col3.write("Add Recipe ingredients to your shopping list")
            col3.image(grayscale, use_column_width=True)

            star = Image.open('img/bookmark.png').convert('RGB')
            col5.write("Save the recipe for easy future access")
            col5.image(star, use_column_width=True)

            message = Image.open('img/message.png').convert('RGB')
            col7.write("Please leave a comment")
            col7.image(message, use_column_width=True)

            st.subheader("Share")
            with st.beta_expander("Did you cook this recipe?", expanded=True):
                c1, c2 = st.beta_columns([1, 1])
                with c1:
                    st.write("If you are proud of it, share it on Instagram")
                with c2:
                    st.image("img/instagram.jpg", width=60)

            st.subheader("More Recommendations")
            recipes3 = return_recipe3("recipes.csv", output, food_types)
            st.error('{}'.format(recipes3['name'].iloc[0].upper()))
            st.warning('{}'.format(recipes3['name'].iloc[1].upper()))
            st.error('{}'.format(recipes3['name'].iloc[2].upper()))


if __name__ == '__main__':
    main()
