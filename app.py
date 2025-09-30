import streamlit as st
import requests
import os
from dotenv import load_dotenv

# --- INITIALIZATION ---

# Load environment variables from a .env file if it exists
load_dotenv()

# Set page configuration
st.set_page_config(page_title="Business Plan Creator", page_icon="📊", layout="wide")

def initialize_session_state():
    """Initializes all required session state variables in one place."""
    # --- State and Authentication ---
    if 'page' not in st.session_state:
        st.session_state.page = 0  # 0: Login, 1: Page 1, etc.
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'gemini_api_key' not in st.session_state:
        st.session_state.gemini_api_key = os.getenv("GEMINI_API_KEY", "")

    # --- Form Fields ---
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

# Call initialization function
initialize_session_state()

# --- AUTHENTICATION & LOGIN PAGE ---

def login_page():
    """Renders the login page and handles authentication."""
    st.title("Login to Business Plan Creator")

    # In production, use a secure database or auth service. This is for demonstration only.
    VALID_CREDENTIALS = {"admin": "password123"}
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # API Key input
    st.session_state.gemini_api_key = st.text_input(
        "Gemini API Key",
        type="password",
        value=st.session_state.gemini_api_key,
        help="This is required to generate the business plan."
    )

    if st.button("Login"):
        if username in VALID_CREDENTIALS and VALID_CREDENTIALS[username] == password:
            if st.session_state.gemini_api_key:
                st.session_state.authenticated = True
                st.session_state.page = 1  # Move to the first form page
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Please provide a valid Gemini API key.")
        else:
            st.error("Invalid username or password.")

# --- FORM PAGES ---

def page_one():
    """Renders the first page of the form."""
    st.header("Part 1: Basic Information and Market Information")
    st.write("Initially we would like to ask some basic information about the company.")
    
    st.session_state.business_name = st.text_input("What is the name of your company?", value=st.session_state.business_name)
    st.session_state.start_year = st.text_input("In what year was your company established?", value=st.session_state.start_year)
    st.session_state.business_reason = st.text_area("Why was your company established? (max 500 chars)", value=st.session_state.business_reason)
    st.session_state.mission_vision = st.text_area("What is your company's long-term goal or vision?", value=st.session_state.mission_vision)

    legal_options = ["Sole proprietorship", "Private limited company", "General partnership", "Limited partnership", "Public limited company", "Association", "Branch of another company", "Non-profit"]
    st.session_state.legal_structure = st.radio(
        "What type of business is your company?",
        options=legal_options,
        index=legal_options.index(st.session_state.legal_structure) if st.session_state.legal_structure in legal_options else None
    )

    st.session_state.financial_funding = st.multiselect(
        "How is your company currently financed?",
        options=["Own financing", "Funding from investors", "Bank loan", "Revenue from sales", "Other"],
        default=st.session_state.financial_funding
    )
    
    sector_options = [
        "Raw materials (eg mining, steel, trading companies)", "Industrial business (e.g. means of production, transport)",
        "Services (e.g. commercial and professional services, tourism)", "Durable consumer goods (e.g., furniture, clothing, retail)",
        "Fast-moving consumer goods (e.g., food, beverages, personal products)", "Healthcare (e.g., healthcare equipment, pharmaceuticals)",
        "Financial sectors (e.g., banks, insurance)", "Information technology", "Utilities and energy", "Culture and entertainment"
    ]
    st.session_state.business_sector = st.radio(
        "Which industrial sector does your company operate in?",
        options=sector_options,
        index=sector_options.index(st.session_state.business_sector) if st.session_state.business_sector in sector_options else None
    )

    if st.session_state.business_sector == sector_options[0]: # Raw materials
        raw_materials_options = ["Mining", "Steel", "Trading", "Other"]
        st.session_state.raw_materials_type = st.radio(
            "Specify type:", options=raw_materials_options,
            index=raw_materials_options.index(st.session_state.raw_materials_type) if st.session_state.raw_materials_type in raw_materials_options else None
        )
    
    # ... Add other conditional sector questions here using the same fixed radio button logic ...

    st.session_state.primary_countries = st.text_input("In which countries does your company primarily operate?", value=st.session_state.primary_countries)
    # ... Continue with other questions for Page 1 ...
    st.session_state.product_service_description = st.text_area("Describe your products or services:", value=st.session_state.product_service_description)

def page_two():
    """Renders the second page of the form."""
    st.header("Part 2: Segmentation and Revenue Information")
    st.session_state.segment_name = st.text_input("Name of the most relevant customer segment:", value=st.session_state.segment_name)
    # ... Add all other questions for Page 2 here ...
    
def page_three():
    """Renders the third page of the form."""
    st.header("Part 3: Resources, Partners, and Team")
    st.session_state.material_resources = st.multiselect("Material resources:", options=["Equipment", "Facilities", "Inventory", "Other"], default=st.session_state.material_resources)
    # ... Add all other questions for Page 3 here ...
    
    # Place the generate button at the end of the last page
    if st.button("Generate Business Plan"):
        generate_business_plan()

# --- DATA SUBMISSION ---

def generate_business_plan():
    """Collects all data and sends it to the backend API."""
    with st.spinner("🧠 Generating your business plan... This may take a few minutes."):
        try:
            # Collect all data from session state into a dictionary
            data = {key: st.session_state[key] for key in st.session_state if key not in ['page', 'authenticated', 'gemini_api_key']}
            
            # Best Practice: Pass the API key in a secure header, not as an environment variable.
            # However, sticking to the original logic, we ensure the backend can access it.
            # The backend should be configured to read this key.
            os.environ["GEMINI_API_KEY"] = st.session_state.gemini_api_key

            # Get backend URL from environment variables for flexibility
            backend_url = os.getenv("BACKEND_URL", "http://localhost:8000/generate_business_plan")
            if "your-app-name.onrender.com" in backend_url:
                st.warning("Please set your BACKEND_URL environment variable.")

            response = requests.post(
                backend_url,
                json=data,
                timeout=300  # 5-minute timeout for long AI generation
            )

            if response.status_code == 200:
                result = response.json()
                business_plan_markdown = result.get("business_plan", "Error: No business plan found in response.")
                
                st.markdown("---")
                st.header("Generated Business Plan")
                st.markdown(business_plan_markdown, unsafe_allow_html=True)
                st.success("✅ Business Plan ready!")

                st.download_button(
                    label="Download Business Plan",
                    data=business_plan_markdown,
                    file_name="generated_business_plan.md",
                    mime="text/markdown"
                )
            else:
                st.error(f"Error from server (Status {response.status_code}): {response.text}")

        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to the server: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

# --- MAIN APP ROUTER ---

if not st.session_state.authenticated:
    login_page()
else:
    st.title("Business Plan Creator")

    # Navigation buttons
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.session_state.page > 1:
            if st.button("⬅️ Previous Page"):
                st.session_state.page -= 1
                st.rerun()
    with col2:
        if st.session_state.page < 3:
            if st.button("Next Page ➡️"):
                st.session_state.page += 1
                st.rerun()
    
    st.markdown("---")

    # Page router
    if st.session_state.page == 1:
        page_one()
    elif st.session_state.page == 2:
        page_two()
    elif st.session_state.page == 3:
        page_three()
