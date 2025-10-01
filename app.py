# --- START OF FILE app.py ---

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
    # Fetch API keys from environment first, then allow user input
    if 'gemini_api_key' not in st.session_state:
        st.session_state.gemini_api_key = os.getenv("GEMINI_API_KEY", "")
    if 'groq_api_key' not in st.session_state:
        st.session_state.groq_api_key = os.getenv("GROQ_API_KEY", "")

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
        "Gemini API Key", type="password",
        value=st.session_state.gemini_api_key,
        help="Required for Gemini models. Will default to environment variable if set."
    )
    st.session_state.groq_api_key = st.text_input(
        "Groq API Key", type="password",
        value=st.session_state.groq_api_key,
        help="Required for Groq models. Will default to environment variable if set."
    )

    if st.button("Login"):
        if username in VALID_CREDENTIALS and VALID_CREDENTIALS[username] == password:
            # Authenticate if both keys are provided (or if they are pre-filled from env)
            if st.session_state.gemini_api_key and st.session_state.groq_api_key:
                st.session_state.authenticated = True
                st.session_state.page = 1
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Both Gemini and Groq API keys are required.")
        else:
            st.error("Invalid username or password.")

# --- FORM PAGES (Simplified for brevity, fill with your questions) ---

def page_one():
    st.header("Part 1: Basic Information and Market Information")
    st.session_state.business_name = st.text_input("Company Name", st.session_state.business_name)
    st.session_state.start_year = st.text_input("Establishment Year", st.session_state.start_year)
    # --- Add all other questions from page 1 ---
    # Example for legal_structure:
    st.session_state.legal_structure = st.selectbox(
        "Legal Structure",
        options=[None, "Sole Proprietorship", "Partnership", "Corporation", "LLC"],
        index=0 if st.session_state.legal_structure is None else ([None, "Sole Proprietorship", "Partnership", "Corporation", "LLC"].index(st.session_state.legal_structure) if st.session_state.legal_structure in [None, "Sole Proprietorship", "Partnership", "Corporation", "LLC"] else 0)
    )
    # Example for financial_funding (multi-select)
    financial_options = ["Bootstrapped", "Angel Investment", "Venture Capital", "Bank Loan", "Grants"]
    st.session_state.financial_funding = st.multiselect(
        "Financial Funding",
        options=financial_options,
        default=st.session_state.financial_funding
    )
    # Example for business_sector
    st.session_state.business_sector = st.selectbox(
        "Business Sector",
        options=[None, "Technology", "Retail", "Services", "Manufacturing", "Healthcare", "Finance", "Agriculture", "Education", "Other"],
        index=0 if st.session_state.business_sector is None else ([None, "Technology", "Retail", "Services", "Manufacturing", "Healthcare", "Finance", "Agriculture", "Education", "Other"].index(st.session_state.business_sector) if st.session_state.business_sector in [None, "Technology", "Retail", "Services", "Manufacturing", "Healthcare", "Finance", "Agriculture", "Education", "Other"] else 0)
    )
    st.session_state.business_reason = st.text_area("Reason for Business", st.session_state.business_reason)
    st.session_state.mission_vision = st.text_area("Mission & Vision", st.session_state.mission_vision)
    st.session_state.product_service_description = st.text_area("Product/Service Description", st.session_state.product_service_description)
    st.session_state.primary_countries = st.text_input("Primary Countries of Operation", st.session_state.primary_countries)
    st.session_state.product_centralisation = st.selectbox(
        "Product/Service Centralization",
        options=[None, "Centralized", "Decentralized"],
        index=0 if st.session_state.product_centralisation is None else ([None, "Centralized", "Decentralized"].index(st.session_state.product_centralisation) if st.session_state.product_centralisation in [None, "Centralized", "Decentralized"] else 0)
    )
    st.session_state.product_range = st.selectbox(
        "Product Range",
        options=[None, "Narrow", "Broad"],
        index=0 if st.session_state.product_range is None else ([None, "Narrow", "Broad"].index(st.session_state.product_range) if st.session_state.product_range in [None, "Narrow", "Broad"] else 0)
    )
    st.session_state.end_consumer_characteristics = st.text_area("End Consumer Characteristics (e.g., age, income, lifestyle)", st.session_state.end_consumer_characteristics)
    consumer_characteristics_2_options = ["B2B", "B2C", "Government", "Non-profit"]
    st.session_state.end_consumer_characteristics_2 = st.multiselect(
        "End Consumer Target Group",
        options=consumer_characteristics_2_options,
        default=st.session_state.end_consumer_characteristics_2
    )

def page_two():
    st.header("Part 2: Segmentation, Revenue and Customer Relations")
    st.session_state.segment_name = st.text_input("Most Relevant Customer Segment", st.session_state.segment_name)
    st.session_state.segment_demographics = st.text_area("Segment Demographics", st.session_state.segment_demographics)
    st.session_state.segment_characteristics = st.text_area("Segment Characteristics", st.session_state.segment_characteristics)
    st.session_state.customer_count = st.text_input("Estimated Customer Count", st.session_state.customer_count)
    st.session_state.problems_faced = st.text_area("Customer Problems Solved", st.session_state.problems_faced)
    st.session_state.biggest_competitors = st.text_area("Biggest Competitors", st.session_state.biggest_competitors)
    st.session_state.competition_intensity = st.selectbox(
        "Competition Intensity",
        options=[None, "Low", "Medium", "High"],
        index=0 if st.session_state.competition_intensity is None else ([None, "Low", "Medium", "High"].index(st.session_state.competition_intensity) if st.session_state.competition_intensity in [None, "Low", "Medium", "High"] else 0)
    )
    st.session_state.price_comparison = st.selectbox(
        "Price Comparison to Competitors",
        options=[None, "Lower", "Similar", "Higher"],
        index=0 if st.session_state.price_comparison is None else ([None, "Lower", "Similar", "Higher"].index(st.session_state.price_comparison) if st.session_state.price_comparison in [None, "Lower", "Similar", "Higher"] else 0)
    )
    st.session_state.market_type = st.selectbox(
        "Market Type",
        options=[None, "Niche", "Mass Market", "Diversified"],
        index=0 if st.session_state.market_type is None else ([None, "Niche", "Mass Market", "Diversified"].index(st.session_state.market_type) if st.session_state.market_type in [None, "Niche", "Mass Market", "Diversified"] else 0)
    )
    competitive_params_options = ["Price", "Quality", "Innovation", "Customer Service", "Brand Reputation"]
    st.session_state.competitive_parameters = st.multiselect(
        "Key Competitive Parameters",
        options=competitive_params_options,
        default=st.session_state.competitive_parameters
    )
    value_props_options = ["Cost Reduction", "Performance Improvement", "Customization", "Newness", "Design"]
    st.session_state.value_propositions = st.multiselect(
        "Value Propositions",
        options=value_props_options,
        default=st.session_state.value_propositions
    )
    st.session_state.direct_income = st.selectbox(
        "Primary Income Source",
        options=[None, "Direct Sales", "Subscriptions", "Licensing", "Advertising", "Consulting"],
        index=0 if st.session_state.direct_income is None else ([None, "Direct Sales", "Subscriptions", "Licensing", "Advertising", "Consulting"].index(st.session_state.direct_income) if st.session_state.direct_income in [None, "Direct Sales", "Subscriptions", "Licensing", "Advertising", "Consulting"] else 0)
    )
    revenue_stream_options = ["Asset Sale", "Usage Fee", "Subscription Fees", "Lending/Renting/Leasing", "Licensing", "Brokerage Fees", "Advertising"]
    st.session_state.primary_revenue = st.multiselect(
        "Primary Revenue Streams",
        options=revenue_stream_options,
        default=st.session_state.primary_revenue
    )
    one_time_payment_options = ["Product Purchase", "Consulting Project", "License Fee (one-time)"]
    st.session_state.one_time_payments = st.multiselect(
        "One-Time Payment Characteristics",
        options=one_time_payment_options,
        default=st.session_state.one_time_payments
    )
    ongoing_payment_options = ["Subscription", "Maintenance Fee", "Usage-based Billing"]
    st.session_state.ongoing_payments = st.multiselect(
        "Ongoing Payment Characteristics",
        options=ongoing_payment_options,
        default=st.session_state.ongoing_payments
    )
    payment_char_options = ["Fixed Price", "Dynamic Price (negotiation)", "Usage-based", "Volume-dependent"]
    st.session_state.payment_characteristics = st.multiselect(
        "General Payment Characteristics",
        options=payment_char_options,
        default=st.session_state.payment_characteristics
    )
    st.session_state.package_price = st.selectbox(
        "Pricing Strategy",
        options=[None, "Fixed Package Price", "Tiered Pricing", "Custom Quotes"],
        index=0 if st.session_state.package_price is None else ([None, "Fixed Package Price", "Tiered Pricing", "Custom Quotes"].index(st.session_state.package_price) if st.session_state.package_price in [None, "Fixed Package Price", "Tiered Pricing", "Custom Quotes"] else 0)
    )
    st.session_state.price_negotiation = st.selectbox(
        "Price Negotiation",
        options=[None, "Yes", "No"],
        index=0 if st.session_state.price_negotiation is None else ([None, "Yes", "No"].index(st.session_state.price_negotiation) if st.session_state.price_negotiation in [None, "Yes", "No"] else 0)
    )
    fixed_price_options = ["List Price", "Product Feature Dependent", "Customer Segment Dependent", "Volume Dependent"]
    st.session_state.fixed_prices = st.multiselect(
        "Fixed Price Types",
        options=fixed_price_options,
        default=st.session_state.fixed_prices
    )
    dynamic_price_options = ["Negotiation (with customer)", "Yield Management", "Real-time Market", "Auction"]
    st.session_state.dynamic_prices = st.multiselect(
        "Dynamic Price Types",
        options=dynamic_price_options,
        default=st.session_state.dynamic_prices
    )
    distribution_options = ["Direct Sales", "Online Store", "Retail Partners", "Wholesalers", "Affiliates"]
    st.session_state.distribution_channels = st.multiselect(
        "Distribution Channels",
        options=distribution_options,
        default=st.session_state.distribution_channels
    )
    st.session_state.purchasing_power = st.selectbox(
        "Target Customer Purchasing Power",
        options=[None, "Low", "Medium", "High"],
        index=0 if st.session_state.purchasing_power is None else ([None, "Low", "Medium", "High"].index(st.session_state.purchasing_power) if st.session_state.purchasing_power in [None, "Low", "Medium", "High"] else 0)
    )
    product_char_options = ["New features", "Design changes", "Performance upgrades", "Cost optimization"]
    st.session_state.product_related_characteristics = st.multiselect(
        "Product/Service Related Characteristics",
        options=product_char_options,
        default=st.session_state.product_related_characteristics
    )
    st.session_state.self_service_availability = st.selectbox(
        "Self-Service Availability",
        options=[None, "Yes", "No", "Partial"],
        index=0 if st.session_state.self_service_availability is None else ([None, "Yes", "No", "Partial"].index(st.session_state.self_service_availability) if st.session_state.self_service_availability in [None, "Yes", "No", "Partial"] else 0)
    )
    st.session_state.online_communities_presence = st.selectbox(
        "Online Communities Presence",
        options=[None, "Yes", "No"],
        index=0 if st.session_state.online_communities_presence is None else ([None, "Yes", "No"].index(st.session_state.online_communities_presence) if st.session_state.online_communities_presence in [None, "Yes", "No"] else 0)
    )
    st.session_state.development_process_customer_involvement = st.selectbox(
        "Customer Involvement in Development",
        options=[None, "Yes", "No", "Indirect"],
        index=0 if st.session_state.development_process_customer_involvement is None else ([None, "Yes", "No", "Indirect"].index(st.session_state.development_process_customer_involvement) if st.session_state.development_process_customer_involvement in [None, "Yes", "No", "Indirect"] else 0)
    )
    st.session_state.after_sale_purchases = st.selectbox(
        "After-Sale Purchases/Upsells",
        options=[None, "Yes", "No"],
        index=0 if st.session_state.after_sale_purchases is None else ([None, "Yes", "No"].index(st.session_state.after_sale_purchases) if st.session_state.after_sale_purchases in [None, "Yes", "No"] else 0)
    )
    st.session_state.personal_assistance_offered = st.selectbox(
        "Personal Assistance Offered",
        options=[None, "Yes", "No"],
        index=0 if st.session_state.personal_assistance_offered is None else ([None, "Yes", "No"].index(st.session_state.personal_assistance_offered) if st.session_state.personal_assistance_offered in [None, "Yes", "No"] else 0)
    )
    st.session_state.similar_products_switch = st.selectbox(
        "Ease for Customers to Switch to Similar Products",
        options=[None, "Easy", "Moderate", "Difficult"],
        index=0 if st.session_state.similar_products_switch is None else ([None, "Easy", "Moderate", "Difficult"].index(st.session_state.similar_products_switch) if st.session_state.similar_products_switch in [None, "Easy", "Moderate", "Difficult"] else 0)
    )
    st.session_state.general_customer_relation = st.selectbox(
        "General Customer Relation Type",
        options=[None, "Transactional", "Long-term", "Community-based"],
        index=0 if st.session_state.general_customer_relation is None else ([None, "Transactional", "Long-term", "Community-based"].index(st.session_state.general_customer_relation) if st.session_state.general_customer_relation in [None, "Transactional", "Long-term", "Community-based"] else 0)
    )


def page_three():
    st.header("Part 3: Resources, Partners, and Team")
    st.session_state.team_members = st.text_area("Team Members and Competencies", st.session_state.team_members)
    # --- Add all other questions from page 3 ---
    material_resources_options = ["Physical Assets", "Inventory", "Manufacturing Facilities", "Vehicles"]
    st.session_state.material_resources = st.multiselect(
        "Material Resources",
        options=material_resources_options,
        default=st.session_state.material_resources
    )
    intangible_resources_options = ["Brand", "Patents", "Copyrights", "Software", "Knowledge", "Partnerships"]
    st.session_state.intangible_resources = st.multiselect(
        "Intangible Resources",
        options=intangible_resources_options,
        default=st.session_state.intangible_resources
    )
    important_activities_options = ["Production", "Problem Solving", "Platform/Network Management", "Supply Chain Management", "Marketing", "R&D"]
    st.session_state.important_activities = st.multiselect(
        "Important Activities",
        options=important_activities_options,
        default=st.session_state.important_activities
    )
    inhouse_activities_options = ["Core Product Development", "Customer Support", "Strategic Planning", "Sales"]
    st.session_state.inhouse_activities = st.multiselect(
        "In-house Activities",
        options=inhouse_activities_options,
        default=st.session_state.inhouse_activities
    )
    outsourced_activities_options = ["Manufacturing", "IT Support", "Logistics", "Marketing Campaigns", "HR"]
    st.session_state.outsourced_activities = st.multiselect(
        "Outsourced Activities",
        options=outsourced_activities_options,
        default=st.session_state.outsourced_activities
    )
    company_statements_options = ["Vision Statement", "Mission Statement", "Values Statement", "Unique Selling Proposition"]
    st.session_state.company_statements = st.multiselect(
        "Company Statements",
        options=company_statements_options,
        default=st.session_state.company_statements
    )
    st.session_state.important_strategic_partners = st.text_area("Important Strategic Partners", st.session_state.important_strategic_partners)
    partnership_benefits_options = ["Optimization & Economy", "Reduction of Risk & Uncertainty", "Acquisition of Particular Resources & Activities"]
    st.session_state.partnership_benefits = st.multiselect(
        "Partnership Benefits",
        options=partnership_benefits_options,
        default=st.session_state.partnership_benefits
    )
    st.session_state.other_benefit = st.text_area("Other Partnership Benefits (if any)", st.session_state.other_benefit)
    st.session_state.company_dependency = st.selectbox(
        "Company Dependency on Key Partners",
        options=[None, "Low", "Medium", "High"],
        index=0 if st.session_state.company_dependency is None else ([None, "Low", "Medium", "High"].index(st.session_state.company_dependency) if st.session_state.company_dependency in [None, "Low", "Medium", "High"] else 0)
    )
    cost_intensive_components_options = ["Raw Materials", "Labor", "Technology", "Marketing", "Distribution"]
    st.session_state.cost_intensive_components = st.multiselect(
        "Most Cost-Intensive Components",
        options=cost_intensive_components_options,
        default=st.session_state.cost_intensive_components
    )
    st.session_state.funding_amount = st.text_input("Required Funding Amount", st.session_state.funding_amount)
    st.session_state.funding_purpose = st.text_area("Purpose of Funding", st.session_state.funding_purpose)


    # "Generate" button is on the final page
    if st.button("Generate Business Plan"):
        generate_business_plan()

# --- DATA SUBMISSION LOGIC ---

def generate_business_plan():
    """Collects data from session_state and calls the backend API."""
    with st.spinner("🧠 Generating your business plan... This may take a few minutes."):
        try:
            # Get the backend URL from environment variables.
            backend_url = os.getenv("BACKEND_URL")
            if not backend_url:
                st.error("Configuration error: BACKEND_URL is not set. Please set it in Render environment variables or your local .env file.")
                return

            # Collect all form data from session state
            data = {key: st.session_state[key] for key in st.session_state if key not in ['page', 'authenticated']}
            # Ensure both API keys are passed to the backend
            data['gemini_api_key'] = st.session_state.gemini_api_key
            data['groq_api_key'] = st.session_state.groq_api_key


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
