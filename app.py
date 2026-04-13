"""
CookMate - Main App
Run this file with: streamlit run app.py
"""

import streamlit as st

#    Page configuration (must be first Streamlit call) 
st.set_page_config(
    page_title="CookMate 🍳",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="expanded"
)

#    Initialise session state (stores data across pages) 
if "user_profile" not in st.session_state:
    st.session_state.user_profile = {}
if "nutrition_log" not in st.session_state:
    st.session_state.nutrition_log = []      # list of logged meals
if "meal_plan" not in st.session_state:
    st.session_state.meal_plan = {}          # {day: [recipe_id, ...]}
if "cooking_history" not in st.session_state:
    st.session_state.cooking_history = []    # list of cooked recipe ids
if "onboarding_done" not in st.session_state:
    st.session_state.onboarding_done = False


 
#  ONBOARDING - shown only on first visit
#
if not st.session_state.onboarding_done:

    st.title("🍳 Welcome to CookMate!")
    st.subheader("A smarter way to cook, eat, and enjoy food as a student.")
    st.markdown("---")
    st.markdown("### Let's personalise your experience - it only takes a minute!")

    with st.form("onboarding_form"):

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 👤 Your profile")
            name = st.text_input("Your name", placeholder="e.g. Maria")

            dietary = st.multiselect(
                "Dietary preferences",
                ["None", "Vegetarian", "Vegan", "Gluten-free", "Dairy-free"],
                default=["None"],
                help="Select all that apply"
            )
            allergies = st.multiselect(
                "Allergies or ingredients to avoid",
                ["None", "Nuts", "Shellfish", "Eggs", "Soy", "Pork"],
                default=["None"]
            )

        with col2:
            st.markdown("#### 🎯 Goals & preferences")
            budget = st.slider(
                "Weekly food budget (CHF)",
                min_value=20, max_value=200, value=80, step=5,
                help="We'll only suggest recipes within your budget"
            )
            skill = st.select_slider(
                "Cooking skill level",
                options=["Beginner", "Intermediate", "Advanced"],
                value="Beginner"
            )
            goals = st.multiselect(
                "What matters most to you?",
                ["Eat healthier", "Save money", "Try new cuisines", "Build muscle",
                 "Lose weight", "Cook faster", "Reduce food waste"],
                default=["Eat healthier", "Save money"]
            )

        st.markdown("")
        submitted = st.form_submit_button("🚀 Let's cook!", use_container_width=True)

        if submitted:
            if not name.strip():
                st.warning("Please enter your name!")
            else:
                # Save profile to session state
                st.session_state.user_profile = {
                    "name": name.strip(),
                    "dietary": dietary,
                    "allergies": allergies,
                    "budget": budget,
                    "skill": skill,
                    "goals": goals,
                }
                st.session_state.onboarding_done = True
                st.rerun()



#  DASHBOARD - shown after onboarding

else:
    from recipes_data import RECIPES

    profile = st.session_state.user_profile
    name = profile.get("name", "Student")

    #    Header   
    st.title(f"👋 Hey {name}, welcome to CookMate!")
    st.markdown("Use the **sidebar** to navigate between features.")
    st.markdown("---")

    #    Metrics row   
    col1, col2, col3, col4 = st.columns(4)

    meals_logged = len(st.session_state.nutrition_log)
    total_cal = sum(m.get("calories", 0) for m in st.session_state.nutrition_log)
    total_protein = sum(m.get("protein", 0) for m in st.session_state.nutrition_log)
    budget_per_meal = round(profile.get("budget", 80) / 21, 2)

    with col1:
        st.metric("💰 Weekly budget", f"CHF {profile.get('budget', 80)}")
    with col2:
        st.metric("🍽️ Meals logged", meals_logged)
    with col3:
        st.metric("🔥 Total calories", f"{total_cal} kcal")
    with col4:
        st.metric("💪 Total protein", f"{total_protein} g")

    st.markdown("---")

    #    Quick profile summary 
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("#### 📋 Your profile")
        st.write(f"- **Skill level:** {profile.get('skill', '—')}")
        st.write(f"- **Diet:** {', '.join(profile.get('dietary', [])) or '—'}")
        st.write(f"- **Goals:** {', '.join(profile.get('goals', [])) or '—'}")

    with col_b:
        st.markdown("#### 🧭 What would you like to do?")
        st.page_link("pages/1_Recipe_Finder.py",    label="🍳 Find recipes by ingredients & budget")
        st.page_link("pages/2_World_Map.py",         label="🌍 Explore recipes from around the world")
        st.page_link("pages/3_Nutrition_Tracker.py", label="📊 Track your nutrition")
        st.page_link("pages/4_Meal_Planner.py",      label="📅 Plan your weekly meals")

    st.markdown("---")

    #    Recent cooking history 
    if st.session_state.cooking_history:
        st.markdown("#### 🕒 Recently cooked")
        recent_ids = st.session_state.cooking_history[-5:]
        recent_recipes = [r for r in RECIPES if r["id"] in recent_ids]
        for r in reversed(recent_recipes):
            st.write(f"✅ {r['name']} ({r['country']}) — {r['calories']} kcal, CHF {r['cost_chf']}")
    else:
        st.info("You haven't cooked anything yet! Head to the Recipe Finder to get started.")

    #    Reset button (bottom of page) 
    st.markdown("---")
    if st.button("⚙️ Reset profile & redo onboarding"):
        for key in ["user_profile", "nutrition_log", "meal_plan", "cooking_history", "onboarding_done"]:
            st.session_state[key] = {} if key in ["user_profile", "meal_plan"] else (
                [] if key in ["nutrition_log", "cooking_history"] else False
            )
        st.rerun()
