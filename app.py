import streamlit as st
import pandas as pd

st.set_page_config(page_title="Desi Diet Dashboard", layout="wide", page_icon="🍲")
st.title("🍲 Desi Diet & Fitness Dashboard")
st.markdown("Track your daily macros, adjust targets, and manage classic Indian meal items.")

st.sidebar.header("🎯 Your Daily Targets")
target_calories = st.sidebar.number_input("Target Calories (kcal)", min_value=1200, max_value=5000, value=2200, step=50)
target_protein = st.sidebar.slider("Target Protein (g)", min_value=40, max_value=250, value=140)
target_carbs = st.sidebar.slider("Target Carbs (g)", min_value=50, max_value=500, value=220)
target_fats = st.sidebar.slider("Target Fats (g)", min_value=20, max_value=150, value=65)

desi_food_db = {
    "Chicken Dum Biryani (1 plate / ~350g)": {"cal": 550, "protein": 32, "carbs": 65, "fats": 16},
    "Paneer Butter Masala (1 bowl / ~200g)": {"cal": 360, "protein": 14, "carbs": 12, "fats": 28},
    "Cashew Paneer (1 bowl / ~200g)": {"cal": 420, "protein": 15, "carbs": 16, "fats": 34},
    "Chicken Fried Rice (1 plate / ~300g)": {"cal": 480, "protein": 24, "carbs": 55, "fats": 14},
    "Whey Protein Scoop (1 scoop / ~33g)": {"cal": 130, "protein": 25, "carbs": 3, "fats": 2},
    "Roti / Phulka (1 medium / no ghee)": {"cal": 85, "protein": 3, "carbs": 18, "fats": 0.5},
    "Dal Tadka (1 katori / ~150g)": {"cal": 150, "protein": 7, "carbs": 20, "fats": 5},
    "Boiled Egg (Whole - 1 large)": {"cal": 78, "protein": 6, "carbs": 0.6, "fats": 5},
}

if 'logged_meals' not in st.session_state:
    st.session_state.logged_meals = []

st.header("🍽️ Log Your Meals")
col1, col2 = st.columns([2, 1])
with col1:
    selected_food = st.selectbox("Select a food item:", list(desi_food_db.keys()))
with col2:
    servings = st.number_input("Servings / Quantity", min_value=0.5, max_value=10.0, value=1.0, step=0.5)

if st.button("➕ Add to Daily Log", use_container_width=True):
    food_stats = desi_food_db[selected_food]
    st.session_state.logged_meals.append({
        "Food Item": selected_food,
        "Servings": servings,
        "Calories (kcal)": round(food_stats["cal"] * servings),
        "Protein (g)": round(food_stats["protein"] * servings, 1),
        "Carbs (g)": round(food_stats["carbs"] * servings, 1),
        "Fats (g)": round(food_stats["fats"] * servings, 1)
    })
    st.success(f"Added {servings}x {selected_food}!")

st.write("---")
st.header("📊 Daily Progress Tracker")

if st.session_state.logged_meals:
    df_log = pd.DataFrame(st.session_state.logged_meals)
    st.dataframe(df_log, use_container_width=True)
    total_cal = df_log["Calories (kcal)"].sum()
    total_protein = df_log["Protein (g)"].sum()
    total_carbs = df_log["Carbs (g)"].sum()
    total_fats = df_log["Fats (g)"].sum()
    if st.button("🗑️ Clear Log"):
        st.session_state.logged_meals = []
        st.rerun()
else:
    st.info("No food logged yet for today.")
    total_cal, total_protein, total_carbs, total_fats = 0, 0.0, 0.0, 0.0

st.write("---")
m_col1, m_col2, m_col3, m_col4 = st.columns(4)
with m_col1:
    st.metric("Calories", f"{total_cal} / {target_calories} kcal", f"{target_calories - total_cal} left", delta_color="inverse")
with m_col2:
    st.metric("Protein", f"{total_protein}g / {target_protein}g", f"{round(target_protein - total_protein, 1)}g left")
with m_col3:
    st.metric("Carbs", f"{total_carbs}g / {target_carbs}g", f"{round(target_carbs - total_carbs, 1)}g left")
with m_col4:
    st.metric("Fats", f"{total_fats}g / {target_fats}g", f"{round(target_fats - total_fats, 1)}g left")

st.progress(min(float(total_cal) / target_calories, 1.0), text="Calorie Consumed Percentage")
