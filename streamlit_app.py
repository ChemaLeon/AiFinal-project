import streamlit as st
from openai import OpenAI
import json

st.set_page_config(
    page_title="CookSmart",
    page_icon="🍳")

if 'ingredients' not in st.session_state:
    st.session_state["ingredients"] = []


client = OpenAI(
    api_key=st.secrets["api_key"]
)


col1, col2, col3 = st.columns(3)
with col2:

    st.header("CookSmart")
    st.write("Cook Smarter, Not Harder")


system_prompt = """
You are a cooking assistant.

Return ONLY valid JSON in this format:

{
  "recipes": [
    {
      "title": "",
      "ingredients": [],
      "steps": []
    }
  ]
}

Rules:
- Use only given ingredients + basic pantry items such as salt, pepper, water, oil
- Dont use other ingredients, only the ones the person gave.
- Must be valid recipes, not some made up ones. Google them off the internet
- Generate exactly 5 recipes
- Max 10 steps per recipe
- BE VERY VERY DETAILED, BE SURE TO ADD COOKING TIMES, HOW HOT TO COOK AND VERY SPECIFIC THINGS THAT ARE EASY TO FOLLOW.
- add some emojis just for fun
- add additional information such as calories(you can add calories for each ingredient), difficulty(use stars for the difficulty ⭐⭐⭐, 3 out of 5 stars), time(include the overall cook time)
"""



if 'chat' not in st.session_state:
    st.session_state["chat"] = [{'role':'system','content':system_prompt}]

with st.form('hp_form'):
    ingredients = st.text_input("What are the ingredients you have?(Write commas between each induvidual ingredient, atleast 4 ingredients) ")
    cookware = st.text_input("What cookware do you have in your kitches? ")
    otherinfo = st.text_input("Do you have any other information? ")
    submit_button = st.form_submit_button("Submit ingredients")
    user_prompt = f"""
These are the ingredients I have:
{ingredients}
These are the cookware I have:
{cookware}
These are some other information that I gave 
{otherinfo}
What can I cook?
"""

    if submit_button:
        st.write('ingredients taken')
        if 'chat' in st.session_state:
            st.session_state['chat'].append({'role':'user','content':user_prompt})
        if 'ingredients' in st.session_state:
            st.session_state['ingredients'].append(ingredients)


with st.form("get-recipes"):
    st.write("Press to get recipe")
    get_recipe = st.form_submit_button('Get recipe list made with ingredients!')
    if get_recipe:
    
        response = client.chat.completions.create(
            model="gpt-4o",
            response_format= {'type':'json_object'},
            messages=st.session_state['chat'],
        
            )
        data = json.loads(response.choices[0].message.content)  # your JSON string

        for recipe in data["recipes"]:
            st.subheader(recipe["title"])
            
            "**Ingredients:**"
            for ing in recipe["ingredients"]:
                st.write(f"- {ing}")
            
            st.write("**Steps:**")
            for i, step in enumerate(recipe["steps"], 1):
                st.write(f"{i}. {step}")
            
            st.write("---")