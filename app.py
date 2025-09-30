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

    st.session_state.gemini_api_key = st.text_input(
        "Enter Your Gemini API Key to Proceed", type="password", value=st.session_state.gemini_api_key,
        help="Required to power the AI agents that generate your business plan."
    )

    if st.button("Login"):
        if st.session_state.gemini_api_key:
            # Simple check to see if the key looks plausible (starts with 'AIza')
            # This is not a validation, just a basic UX check.
            if st.session_state.gemini_api_key.startswith("AIza"):
                st.session_state.authenticated = True
                st.session_state.page = 1
                st.success("Login successful!")
                st.rerun()
            else:
                st.warning("That doesn't look like a valid Gemini API key. Please check it and try again.")
        else:
            st.error("A Gemini API key is required to use this application.")

# --- FORM PAGES ---

def page_one():
    st.header("Part 1: Basic Information and Market Information")
    st.write("Initially we would like to ask some basic information about the company.")
    
    st.session_state.business_name = st.text_input(
        "What is the name of your company?",
        placeholder="e.g., EcoFashion",
        value=st.session_state.business_name
    )
    st.session_state.start_year = st.text_input(
        "In what year was your company established?",
        value=st.session_state.start_year
    )
    st.session_state.business_reason = st.text_area(
        "Kindly describe in maximum 500 characters why was your company established!",
        placeholder="e.g., In order to provide IT security services for small firms...",
        value=st.session_state.business_reason
    )
    st.session_state.mission_vision = st.text_area(
        "Please state your company's long-term goal or vision!",
        placeholder="e.g., Our mission is to...",
        value=st.session_state.mission_vision
    )
    st.session_state.legal_structure = st.radio(
        "What type of business is your company?",
        options=["Sole proprietorship", "Private limited company", "General partnership", "Limited partnership", "Public limited company", "Association", "Branch of another company", "Non-profit"],
        index=None if st.session_state.legal_structure is None else ["Sole proprietorship", "Private limited company", "General partnership", "Limited partnership", "Public limited company", "Association", "Branch of another company", "Non-profit"].index(st.session_state.legal_structure)
    )
    st.session_state.financial_funding = st.multiselect(
        "How is your company currently financed?",
        options=["Own financing", "Funding from investors", "Bank loan", "Revenue from sales", "Other"],
        default=st.session_state.financial_funding
    )
    st.session_state.business_sector = st.radio(
        "Which industrial sector does your company operate in?",
        options=["Raw materials (eg mining, steel, trading companies)", "Industrial business (e.g. means of production, transport)", "Services (e.g. commercial and professional services, tourism)", "Durable consumer goods (e.g., furniture, clothing, retail)", "Fast-moving consumer goods (e.g., food, beverages, personal products)", "Healthcare (e.g., healthcare equipment, pharmaceuticals)", "Financial sectors (e.g., banks, insurance)", "Information technology", "Utilities and energy (e.g., water, heat, recycling)", "Culture and leisure (e.g., cultural centre, cinema)"],
        index=None if st.session_state.business_sector is None else ["Raw materials (eg mining, steel, trading companies)", "Industrial business (e.g. means of production, transport)", "Services (e.g. commercial and professional services, tourism)", "Durable consumer goods (e.g., furniture, clothing, retail)", "Fast-moving consumer goods (e.g., food, beverages, personal products)", "Healthcare (e.g., healthcare equipment, pharmaceuticals)", "Financial sectors (e.g., banks, insurance)", "Information technology", "Utilities and energy (e.g., water, heat, recycling)", "Culture and leisure (e.g., cultural centre, cinema)"].index(st.session_state.business_sector)
    )
    # Conditional questions based on business sector
    if st.session_state.business_sector == "Raw materials (eg mining, steel, trading companies)":
        st.session_state.raw_materials_type = st.radio("What type of raw materials business?", options=["Mining", "Textiles and clothing", "Paper and carton", "Chemicals", "Petroleum", "Rubber", "Glass & Ceramics", "Oil", "Steel", "Non-ferrous metals", "Retailers"], index=None if st.session_state.raw_materials_type is None else ["Mining", "Textiles and clothing", "Paper and carton", "Chemicals", "Petroleum", "Rubber", "Glass & Ceramics", "Oil", "Steel", "Non-ferrous metals", "Retailers"].index(st.session_state.raw_materials_type))
    # ... (all other conditional questions from frontend.py)
    
    st.session_state.primary_countries = st.text_area(
        "Please specify which country your company's primary market will be in the short-term (1-2 years).",
        value=st.session_state.primary_countries
    )
    st.session_state.product_centralisation = st.radio(
        "Is product/service development centralized or decentralized?",
        options=["Centralized", "Decentralized"],
        index=None if st.session_state.product_centralisation is None else ["Centralized", "Decentralized"].index(st.session_state.product_centralisation)
    )
    st.session_state.product_range = st.radio(
        "Please specify what characterizes the product range of your company:",
        options=["Single product category", "Multiple related product categories", "Multiple unrelated product categories"],
        index=None if st.session_state.product_range is None else ["Single product category", "Multiple related product categories", "Multiple unrelated product categories"].index(st.session_state.product_range)
    )
    st.session_state.end_consumer_characteristics = st.radio(
        "Please specify what characterizes the groups of end-consumers:",
        options=["One specific customer group", "Several specific customer groups", "Several unspecific customer groups"],
        index=None if st.session_state.end_consumer_characteristics is None else ["One specific customer group", "Several specific customer groups", "Several unspecific customer groups"].index(st.session_state.end_consumer_characteristics)
    )
    st.session_state.end_consumer_characteristics_2 = st.multiselect(
        "Please specify what characterizes the groups of end-consumers:",
        options=["End-consumers are primarily private individuals", "End-consumers are primarily companies", "End-consumers are primarily public institutions", "End-consumers are primarily non-profit organizations"],
        default=st.session_state.end_consumer_characteristics_2
    )
    st.session_state.product_service_description = st.text_area(
        "Please write maximum 500 characters about the products or services that the company offers.",
        placeholder="e.g., The company provides security services...",
        value=st.session_state.product_service_description
    )

def page_two():
    st.header("Part 2: Segmentation and Revenue")
    st.write("In this section we would like to gather information about the products/services the company offers and about your most relevant customer segment.")
    
    st.session_state.segment_name = st.text_input("Name of your most relevant customer segment:", value=st.session_state.segment_name)
    st.session_state.segment_demographics = st.text_area("Demographics of this customer segment:", value=st.session_state.segment_demographics)
    st.session_state.segment_characteristics = st.text_area("Characteristics of this customer segment:", value=st.session_state.segment_characteristics)
    st.session_state.customer_count = st.text_input("How many customers does this segment have?", value=st.session_state.customer_count)
    st.session_state.problems_faced = st.text_area("Please briefly describe the problems or challenges that your company is trying to solve for the customer group:", value=st.session_state.problems_faced)
    st.session_state.biggest_competitors = st.text_area("Please indicate and name the three biggest competitors:", value=st.session_state.biggest_competitors)
    st.session_state.competition_intensity = st.radio("Please indicate the intensity of the competition in the market:", options=["Low", "Medium", "High"], index=None if not st.session_state.competition_intensity else ["Low", "Medium", "High"].index(st.session_state.competition_intensity))
    st.session_state.price_comparison = st.radio("How are the prices of your company's products/services compared to competitors?", options=["Significantly lower", "Similar", "Significantly higher"], index=None if not st.session_state.price_comparison else ["Significantly lower", "Similar", "Significantly higher"].index(st.session_state.price_comparison))
    st.session_state.market_type = st.radio("Is the market best described as a niche market or a mass market?", options=["Niche market", "Mass market"], index=None if not st.session_state.market_type else ["Niche market", "Mass market"].index(st.session_state.market_type))
    # ... (all other questions from frontend.py for page 2)

def page_three():
    st.header("Part 3: Resources, Partners, and Team")
    st.write("We still look at your company from the inside out and would like to gain insight into the key resources for creating and capturing value.")

    st.session_state.material_resources = st.multiselect(
        "Please select the three most important material resources for your company:",
        options=["Liquid funds", "Financial guarantees", "Inventory", "Location", "Logistic infrastructure", "Manufacturing/production facilities", "Own physical stores/shops", "Means of transport", "Technologies"],
        default=st.session_state.material_resources, max_selections=3
    )
    st.session_state.intangible_resources = st.multiselect(
        "Please select the three most important intangible resources:",
        options=["Brand(s)", "Customer relations", "Distribution network", "Knowledge/know-how", "Image and reputation", "Digital technologies", "Intellectual property", "Partnerships", "Human resources"],
        default=st.session_state.intangible_resources, max_selections=3
    )
    # ... (all other questions from frontend.py for page 3)
    
    st.session_state.team_members = st.text_area(
        "Team Members and Competencies",
        value=st.session_state.team_members,
        placeholder="Please describe your team members, their positions, and core competencies..."
    )
    st.session_state.funding_amount = st.text_input(
        "If applying for funding, please specify the amount (in Danish Kroner):",
        placeholder="e.g., 1000000",
        value=st.session_state.funding_amount
    )
    if st.session_state.funding_amount:
        st.session_state.funding_purpose = st.text_area(
            "Please describe how you plan to use the requested funding:",
            value=st.session_state.funding_purpose
        )

    # "Generate" button is on the final page
    if st.button("Generate Business Plan"):
        generate_business_plan()

# --- DATA SUBMISSION LOGIC ---

def generate_business_plan():
    """Collects data from session_state and calls the backend API."""
    with st.spinner("🧠 Generating your business plan... This may take a few minutes."):
        try:
            # This is the URL of your deployed backend service on Render
            # It's best practice to set this as an Environment Variable in Render
            backend_url = os.getenv("BACKEND_URL")
            if not backend_url:
                st.error("Configuration error: BACKEND_URL is not set.")
                return

            # Collect all form data from session state
            data = {key: st.session_state[key] for key in st.session_state if key not in ['page', 'authenticated', 'gemini_api_key']}
            # Also include the API key for the backend to use
            data['gemini_api_key'] = st.session_state.gemini_api_key


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
