import streamlit as st
import requests
import os
from dotenv import load_dotenv

# --- INITIALIZATION ---

# Load environment variables from a .env file (useful for local development)
load_dotenv()

# Set page configuration. This should be the first Streamlit command.
st.set_page_config(page_title="Business Plan Creator", page_icon="📊", layout="wide")

def initialize_session_state():
    """Initializes all required session state variables in one place to avoid clutter."""
    # --- State and Authentication ---
    if 'page' not in st.session_state:
        st.session_state.page = 0  # 0: Login, 1: Page 1, etc.
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'gemini_api_key' not in st.session_state:
        st.session_state.gemini_api_key = os.getenv("GEMINI_API_KEY", "")

    # --- Form Fields ---
    # This dictionary makes it easy to add or change default values.
    form_fields = {
        "business_name": "", "start_year": "", "business_reason": "", "mission_vision": "",
        "legal_structure": None, "financial_funding": [], "business_sector": None,
        "raw_materials_type": None, "industrial_business_type": None, "services_type": None,
        "durable_goods_type": None, "consumer_goods_type": None, "healthcare_type": None,
        "financial_sector_type": None, "it_sector_type": None, "utilities_type": None,
        "culture_type": None, "primary_countries": "", "product_centralisation": None,
        "characteristics": [], "product_range": None, "end_consumer_characteristics": None,
        "end_consumer_characteristics_2": [], "product_service_description": "", "segment_name": "",
        "segment_demographics": "", "segment_characteristics": "", "customer_count": "",
        "problems_faced": "", "biggest_competitors": "", "competition_intensity": None,
        "price_comparison": None, "market_type": None, "competitive_parameters": [],
        "value_propositions": [], "direct_income": None, "primary_revenue": [],
        "one_time_payments": [], "ongoing_payments": [], "payment_characteristics": [],
        "package_price": None, "price_negotiation": None, "fixed_prices": [],
        "dynamic_prices": [], "distribution_channels": [], "purchasing_power": None,
        "product_related_characteristics": [], "self_service_availability": None,
        "online_communities_presence": None, "development_process_customer_involvement": None,
        "after_sale_purchases": None, "personal_assistance_offered": None,
        "similar_products_switch": None, "general_customer_relation": None,
        "material_resources": [], "intangible_resources": [], "important_activities": [],
        "inhouse_activities": [], "outsourced_activities": [], "company_statements": [],
        "important_strategic_partners": [], "partnership_benefits": [], "other_benefit": "",
        "company_dependency": None, "cost_intensive_components": [], "team_members": "",
        "funding_amount": "", "funding_purpose": ""
    }
    for key, default_value in form_fields.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

# Call the initialization function at the start
initialize_session_state()

# --- AUTHENTICATION & LOGIN PAGE ---

def login_page():
    """Renders the login page and handles authentication."""
    st.title("Login to Business Plan Creator")
    
    # In production, use a secure database or auth service. This is for demonstration.
    VALID_CREDENTIALS = {"admin": "password123"}
    
    username = st.text_input("Username", value="admin")
    password = st.text_input("Password", type="password", value="password123")

    st.session_state.gemini_api_key = st.text_input(
        "Gemini API Key", type="password", value=st.session_state.gemini_api_key,
        help="Required to run the AI agents."
    )

    if st.button("Login"):
        if username in VALID_CREDENTIALS and VALID_CREDENTIALS[username] == password:
            if st.session_state.gemini_api_key:
                st.session_state.authenticated = True
                st.session_state.page = 1
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("A valid Gemini API key is required.")
        else:
            st.error("Invalid username or password.")

# --- FORM PAGES (Simplified for brevity, fill with your questions) ---

def page_one():
    st.header("Part 1: Basic Information and Market Information")
    st.session_state.business_name = st.text_input("Company Name", st.session_state.business_name)
    st.session_state.start_year = st.text_input("Establishment Year", st.session_state.start_year)
    # ... Add all other questions from page 1 ...

def page_two():
    st.header("Part 2: Segmentation and Revenue")
    st.session_state.segment_name = st.text_input("Most Relevant Customer Segment", st.session_state.segment_name)
    # ... Add all other questions from page 2 ...

def page_three():
    st.header("Part 3: Resources, Partners, and Team")
    st.session_state.team_members = st.text_area("Team Members and Competencies", st.session_state.team_members)
    # ... Add all other questions from page 3 ...
    
    # "Generate" button is on the final page
    if st.button("Generate Business Plan"):
        generate_business_plan()

# --- DATA SUBMISSION LOGIC ---

# in app.py

def generate_business_plan():
    """Collects data from session_state and calls the backend API."""
    with st.spinner("🧠 Generating your business plan... This may take a few minutes."):
        try:
            # This is the URL of your deployed backend service on Render
            backend_url = os.getenv("BACKEND_URL")
            if not backend_url:
                st.error("Configuration error: BACKEND_URL is not set.")
                return

            # Collect all form data from session state
            data = {key: st.session_state[key] for key in st.session_state if key not in ['page', 'authenticated']}

            response = requests.post(
                f"{backend_url}/generate_business_plan", # Append the endpoint path
                json=data,
                timeout=300  # 5-minute timeout for potentially long AI responses
            )

            if response.status_code == 200:
                result = response.json()
                business_plan = result.get("business_plan", "Error: No business plan in response.")

                st.markdown("---")
                st.header("Generated Business Plan")
                st.markdown(business_plan, unsafe_allow_html=True)
                st.success("✅ Business Plan ready!")

                st.download_button(
                    label="Download Business Plan", data=business_plan,
                    file_name="business_plan.md", mime="text/markdown"
                )
            else:
                st.error(f"Error from server (Status {response.status_code}): {response.text}")

        except requests.exceptions.RequestException as e:
            st.error(f"Connection Error: Could not connect to the backend service. Please ensure it's running. Details: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

# --- MAIN APP ROUTER ---

if not st.session_state.authenticated:
    login_page()
else:
    st.title("Business Plan Creator")

    # Navigation buttons
    col1, col2 = st.columns([1, 1])
    if st.session_state.page > 1:
        if col1.button("⬅️ Previous Page"):
            st.session_state.page -= 1
            st.rerun()
    if st.session_state.page < 3:
        if col2.button("Next Page ➡️"):
            st.session_state.page += 1
            st.rerun()

    st.markdown("---")

    # Display the correct page based on the current state
    if st.session_state.page == 1:
        page_one()
    elif st.session_state.page == 2:
        page_two()
    elif st.session_state.page == 3:
        page_three()
