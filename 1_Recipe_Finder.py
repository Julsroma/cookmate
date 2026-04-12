"""
Page 1 — Recipe Finder
Lets users search recipes by ingredients they have, budget, and dietary needs.
Also shows personalised recommendations based on their profile.
"""

import streamlit as st
import sys, os

# Make sure we can import from the root folder
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from recipes_data import RECIPES

st.set_page_config(page_title="Recipe Finder", page_icon="🍳", layout="wide")

# ── Guard: redirect to home if onboarding not done ──
if not st.session_state.get("onboarding_done"):
    st.warning("Please complete the onboarding on the Home page first!")
    st.page_link("app.py", label="Go to Home")
    st.stop()

profile = st.session_state.user_profile


# ══════════════════════════════════════════════════════════════════════════════
#  HELPER: Score a recipe for a given user (simple ML-style recommendation)
# ══════════════════════════════════════════════════════════════════════════════
def score_recipe(recipe, profile, cooking_history):
    """
    Returns a numeric score — the higher the score, the better the match.
    This mimics a simple recommendation system.
    """
    score = 0

    # 1. Budget fit
    budget_per_meal = profile.get("budget", 80) / 21
    if recipe["cost_chf"] <= budget_per_meal:
        score += 20
    elif recipe["cost_chf"] <= budget_per_meal * 1.3:
        score += 10

    # 2. Difficulty matches skill
    skill = profile.get("skill", "Beginner")
    if skill == "Beginner" and recipe["difficulty"] == "Easy":
        score += 20
    elif skill == "Intermediate" and recipe["difficulty"] in ["Easy", "Medium"]:
        score += 20
    elif skill == "Advanced":
        score += 20

    # 3. Dietary match
    user_diet = profile.get("dietary", [])
    if "Vegetarian" in user_diet and recipe.get("vegetarian"):
        score += 15
    if "Vegan" in user_diet and recipe.get("vegan"):
        score += 15
    if "Gluten-free" in user_diet and recipe.get("gluten_free"):
        score += 15
    if "Dairy-free" in user_diet and recipe.get("dairy_free"):
        score += 15

    # 4. Variety — recipes not cooked recently score higher
    if recipe["id"] not in cooking_history[-5:]:
        score += 10

    # 5. Health goal bonus
    goals = profile.get("goals", [])
    if "Build muscle" in goals and recipe["protein"] >= 25:
        score += 10
    if "Lose weight" in goals and recipe["calories"] <= 400:
        score += 10
    if "Save money" in goals and recipe["cost_chf"] <= 3.0:
        score += 10

    return score


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE LAYOUT
# ══════════════════════════════════════════════════════════════════════════════
st.title("🍳 Recipe Finder")
st.markdown("Filter recipes by what you have, what fits your budget, and your preferences.")
st.markdown("---")

# ── Sidebar filters ──
with st.sidebar:
    st.header("🔎 Filters")

    # Ingredient search
    ingredient_input = st.text_input(
        "Ingredients you have",
        placeholder="e.g. eggs, pasta, tomatoes",
        help="Separate multiple ingredients with commas"
    )

    max_budget = st.slider(
        "Max cost per meal (CHF)",
        min_value=1.0, max_value=15.0,
        value=float(profile.get("budget", 80)) / 21 * 1.5,
        step=0.5
    )

    max_time = st.slider("Max cooking time (min)", 5, 60, 60, step=5)

    difficulty_filter = st.multiselect(
        "Difficulty",
        ["Easy", "Medium", "Hard"],
        default=["Easy", "Medium"]
    )

    dietary_filter = st.multiselect(
        "Dietary requirements",
        ["Vegetarian", "Vegan", "Gluten-free", "Dairy-free"]
    )

    sort_by = st.selectbox(
        "Sort by",
        ["Best match (recommended)", "Cheapest first", "Fewest calories", "Fastest to cook", "Most protein"]
    )


# ── Filter recipes ──
user_ingredients = [i.strip().lower() for i in ingredient_input.split(",") if i.strip()]

filtered = []
for r in RECIPES:
    # Budget filter
    if r["cost_chf"] > max_budget:
        continue
    # Time filter
    if r["time_minutes"] > max_time:
        continue
    # Difficulty filter
    if difficulty_filter and r["difficulty"] not in difficulty_filter:
        continue
    # Dietary filter
    for d in dietary_filter:
        if d == "Vegetarian" and not r.get("vegetarian"):
            break
        if d == "Vegan" and not r.get("vegan"):
            break
        if d == "Gluten-free" and not r.get("gluten_free"):
            break
        if d == "Dairy-free" and not r.get("dairy_free"):
            break
    else:
        # Ingredient search: recipe must contain at least one searched ingredient
        if user_ingredients:
            recipe_ingredients = [i.lower() for i in r["ingredients"]]
            if not any(ui in " ".join(recipe_ingredients) for ui in user_ingredients):
                continue
        filtered.append(r)

# ── Sort ──
cooking_history = st.session_state.get("cooking_history", [])
if sort_by == "Best match (recommended)":
    filtered.sort(key=lambda r: score_recipe(r, profile, cooking_history), reverse=True)
elif sort_by == "Cheapest first":
    filtered.sort(key=lambda r: r["cost_chf"])
elif sort_by == "Fewest calories":
    filtered.sort(key=lambda r: r["calories"])
elif sort_by == "Fastest to cook":
    filtered.sort(key=lambda r: r["time_minutes"])
elif sort_by == "Most protein":
    filtered.sort(key=lambda r: r["protein"], reverse=True)


# ── Show results ──
st.markdown(f"### {len(filtered)} recipe(s) found")

if not filtered:
    st.info("No recipes match your filters. Try relaxing some criteria!")
else:
    # Show 2 recipes per row
    for i in range(0, len(filtered), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            if i + j >= len(filtered):
                break
            recipe = filtered[i + j]
            with col:
                with st.container(border=True):
                    # Recipe header
                    score = score_recipe(recipe, profile, cooking_history)
                    stars = "⭐" * min(5, max(1, score // 10))

                    st.markdown(f"### {recipe['name']}")
                    st.caption(f"🌍 {recipe['country']} · ⏱ {recipe['time_minutes']} min · 💰 CHF {recipe['cost_chf']} · {stars}")

                    # Badges
                    badges = []
                    if recipe.get("vegetarian"): badges.append("🥦 Vegetarian")
                    if recipe.get("vegan"):       badges.append("🌱 Vegan")
                    if recipe.get("gluten_free"): badges.append("🌾 Gluten-free")
                    if recipe.get("dairy_free"):  badges.append("🥛 Dairy-free")
                    if badges:
                        st.write(" · ".join(badges))

                    st.write(recipe["description"])

                    # Nutrition summary
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Calories", f"{recipe['calories']} kcal")
                    c2.metric("Protein",  f"{recipe['protein']} g")
                    c3.metric("Difficulty", recipe["difficulty"])

                    # Ingredients
                    with st.expander("🛒 Ingredients"):
                        for ing in recipe["ingredients"]:
                            # Highlight if user has it
                            if user_ingredients and any(ui in ing.lower() for ui in user_ingredients):
                                st.write(f"✅ {ing.capitalize()}")
                            else:
                                st.write(f"• {ing.capitalize()}")

                    # Steps
                    with st.expander("👨‍🍳 How to cook"):
                        for k, step in enumerate(recipe["steps"], 1):
                            st.write(f"**{k}.** {step}")

                    # Action buttons
                    c_a, c_b = st.columns(2)
                    with c_a:
                        if st.button(f"✅ Mark as cooked", key=f"cook_{recipe['id']}"):
                            # Add to cooking history
                            st.session_state.cooking_history.append(recipe["id"])
                            # Auto-log nutrition
                            st.session_state.nutrition_log.append({
                                "name": recipe["name"],
                                "calories": recipe["calories"],
                                "protein": recipe["protein"],
                                "carbs": recipe["carbs"],
                                "fat": recipe["fat"],
                                "cost_chf": recipe["cost_chf"],
                            })
                            st.success(f"Logged '{recipe['name']}' to your nutrition tracker!")

                    with c_b:
                        # Add to meal plan
                        day = st.selectbox(
                            "Add to meal plan",
                            ["—", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                            key=f"day_{recipe['id']}"
                        )
                        if day != "—":
                            if day not in st.session_state.meal_plan:
                                st.session_state.meal_plan[day] = []
                            if recipe["id"] not in st.session_state.meal_plan[day]:
                                st.session_state.meal_plan[day].append(recipe["id"])
                                st.success(f"Added to {day}!")
