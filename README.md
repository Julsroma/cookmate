# 🍳 CookMate — CS Group Project

A social cooking platform for students built with **Python + Streamlit**.

---

## 📁 Project structure

```
cookmate/
│
├── app.py                  ← Main page: onboarding & dashboard
├── recipes_data.py         ← All recipe data (add your own here!)
├── requirements.txt        ← Libraries to install
│
└── pages/
    ├── 1_Recipe_Finder.py  ← Filter recipes by ingredients & budget
    ├── 2_World_Map.py      ← Interactive world map of cuisines
    ├── 3_Nutrition_Tracker.py ← Log meals + calorie/protein graphs
    └── 4_Meal_Planner.py   ← Weekly plan + smart recommendations
```

---

## 🚀 How to run (step by step)

### 1. Install Python
Download from https://python.org — choose version 3.10 or newer.

### 2. Open the cookmate folder in VS Code
File → Open Folder → select the `cookmate` folder.

### 3. Open the VS Code terminal
Menu bar → Terminal → New Terminal

### 4. Install required libraries
Paste this command and press Enter:
```
pip install -r requirements.txt
```

### 5. Run the app
```
streamlit run app.py
```
A browser window will open automatically at http://localhost:8501

---

## ✏️ How to add more recipes

Open `recipes_data.py` and copy-paste the block below, filling in your details.
Then save the file — the app updates automatically!

```python
{
    "id": 21,                          # Give it a unique number
    "name": "My Recipe",
    "country": "Switzerland",
    "ingredients": ["item1", "item2", "item3"],
    "time_minutes": 20,
    "cost_chf": 4.0,
    "calories": 500,
    "protein": 20,
    "carbs": 60,
    "fat": 15,
    "vegetarian": True,                # True or False
    "vegan": False,
    "gluten_free": False,
    "dairy_free": False,
    "difficulty": "Easy",              # "Easy", "Medium", or "Hard"
    "description": "A short description.",
    "lat": 46.8,                       # Latitude of the country
    "lon": 8.2,                        # Longitude of the country
    "steps": [
        "Step 1...",
        "Step 2...",
    ]
},
```

---

## 🔧 How to change the look

Streamlit themes can be set in `.streamlit/config.toml`:
```toml
[theme]
base = "dark"
primaryColor = "#FF6B6B"
```
Create the `.streamlit/` folder in your project root if it doesn't exist.

---

## 👥 Group: 12.04
