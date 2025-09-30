
import streamlit as st
import requests

st.set_page_config(page_title="Business Plan Creator", page_icon="📊")

# Initialize all required session state variables at the start
if 'page' not in st.session_state:
    st.session_state.page = 1
# Initialize session state for form fields if not exists
if 'business_name' not in st.session_state:
    st.session_state.business_name = ""
if 'start_year' not in st.session_state:
    st.session_state.start_year = ""
if 'business_reason' not in st.session_state:
    st.session_state.business_reason = ""
if 'mission_vision' not in st.session_state:
    st.session_state.mission_vision = ""
if 'legal_structure' not in st.session_state:
    st.session_state.legal_structure = None
if 'financial_funding' not in st.session_state:
    st.session_state.financial_funding = []
if 'business_sector' not in st.session_state:
    st.session_state.business_sector = None
if 'raw_materials_type' not in st.session_state:
    st.session_state.raw_materials_type = None
if 'industrial_business_type' not in st.session_state:
    st.session_state.industrial_business_type = None
if 'services_type' not in st.session_state:
    st.session_state.services_type = None
if 'durable_goods_type' not in st.session_state:
    st.session_state.durable_goods_type = None
if 'consumer_goods_type' not in st.session_state:
    st.session_state.consumer_goods_type = None
if 'healthcare_type' not in st.session_state:
    st.session_state.healthcare_type = None
if 'financial_sector_type' not in st.session_state:
    st.session_state.financial_sector_type = None
if 'it_sector_type' not in st.session_state:
    st.session_state.it_sector_type = None
if 'utilities_type' not in st.session_state:
    st.session_state.utilities_type = None
if 'culture_type' not in st.session_state:
    st.session_state.culture_type = None
if 'primary_countries' not in st.session_state:
    st.session_state.primary_countries = ""
if 'product_centralisation' not in st.session_state:
    st.session_state.product_centralisation = None
if 'characteristics' not in st.session_state:
    st.session_state.characteristics = []
if 'product_range' not in st.session_state:
    st.session_state.product_range = None
if 'end_consumer_characteristics' not in st.session_state:
    st.session_state.end_consumer_characteristics = None
if 'end_consumer_characteristics_2' not in st.session_state:
    st.session_state.end_consumer_characteristics_2 = []
if 'product_service_description' not in st.session_state:
    st.session_state.product_service_description = ""
# Page 2 session state initialization
if 'segment_name' not in st.session_state:
    st.session_state.segment_name = ""
if 'segment_demographics' not in st.session_state:
    st.session_state.segment_demographics = ""
if 'segment_characteristics' not in st.session_state:
    st.session_state.segment_characteristics = ""
if 'product_service_description' not in st.session_state:
    st.session_state.product_service_description = ""
if 'customer_count' not in st.session_state:
    st.session_state.customer_count = ""
if 'problems_faced' not in st.session_state:
    st.session_state.problems_faced = ""
if 'biggest_competitors' not in st.session_state:
    st.session_state.biggest_competitors = ""
if 'competition_intensity' not in st.session_state:
    st.session_state.competition_intensity = None
if 'price_comparison' not in st.session_state:
    st.session_state.price_comparison = None
if 'market_type' not in st.session_state:
    st.session_state.market_type = None
if 'competitive_parameters' not in st.session_state:
    st.session_state.competitive_parameters = []
if 'value_propositions' not in st.session_state:
    st.session_state.value_propositions = []
if 'direct_income' not in st.session_state:
    st.session_state.direct_income = None
if 'primary_revenue' not in st.session_state:
    st.session_state.primary_revenue = []
if 'one_time_payments' not in st.session_state:
    st.session_state.one_time_payments = []
if 'ongoing_payments' not in st.session_state:
    st.session_state.ongoing_payments = []
if 'payment_characteristics' not in st.session_state:
    st.session_state.payment_characteristics = []
if 'package_price' not in st.session_state:
    st.session_state.package_price = None
if 'price_negotiation' not in st.session_state:
    st.session_state.price_negotiation = None
if 'fixed_prices' not in st.session_state:
    st.session_state.fixed_prices = []
if 'dynamic_prices' not in st.session_state:
    st.session_state.dynamic_prices = []
if 'distribution_channels' not in st.session_state:
    st.session_state.distribution_channels = []
if 'purchasing_power' not in st.session_state:
    st.session_state.purchasing_power = None
if 'product_related_characteristics' not in st.session_state:
    st.session_state.product_related_characteristics = []
if 'self_service_availability' not in st.session_state:
    st.session_state.self_service_availability = None
if 'online_communities_presence' not in st.session_state:
    st.session_state.online_communities_presence = None
if 'development_process_customer_involvement' not in st.session_state:
    st.session_state.development_process_customer_involvement = None
if 'after_sale_purchases' not in st.session_state:
    st.session_state.after_sale_purchases = None
if 'personal_assistance_offered' not in st.session_state:
    st.session_state.personal_assistance_offered = None
if 'similar_products_switch' not in st.session_state:
    st.session_state.similar_products_switch = None
if 'general_customer_relation' not in st.session_state:
    st.session_state.general_customer_relation = None
# Page 3 session state initialization
if 'material_resources' not in st.session_state:
    st.session_state.material_resources = []
if 'intangible_resources' not in st.session_state:
    st.session_state.intangible_resources = []
if 'important_activities' not in st.session_state:
    st.session_state.important_activities = []
if 'inhouse_activities' not in st.session_state:
    st.session_state.inhouse_activities = []
if 'outsourced_activities' not in st.session_state:
    st.session_state.outsourced_activities = []
if 'company_statements' not in st.session_state:
    st.session_state.company_statements = []
if 'important_strategic_partners' not in st.session_state:
    st.session_state.important_strategic_partners = []
if 'partnership_benefits' not in st.session_state:
    st.session_state.partnership_benefits = []
if 'other_benefit' not in st.session_state:
    st.session_state.other_benefit = None
if 'company_dependency' not in st.session_state:
    st.session_state.company_dependency = None
if 'cost_intensive_components' not in st.session_state:
    st.session_state.cost_intensive_components = []
if 'team_members' not in st.session_state:
    st.session_state.team_members = []
if 'funding_amount' not in st.session_state:
    st.session_state.funding_amount = None
if 'funding_purpose' not in st.session_state:
    st.session_state.funding_purpose = ""

st.title("Business Plan Creator")

col1, col2 = st.columns(2)
with col1:
    if st.session_state.page > 1:  # Only show Previous button if not on first page
        if st.button("Previous Page"):
            st.session_state.page -= 1
            st.rerun()
with col2:
    if st.session_state.page < 3:  # Only show Next button if not on last page
        if st.button("Next Page"):
            st.session_state.page += 1
            st.rerun()

if st.session_state.page == 1:
    st.header("Part 1: Basic information and market information")
    st.write("Initially we would like to ask some basic information about the company.")
    # Text input questions
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

    # Single choice question
    st.session_state.legal_structure = st.radio(
        "What type of business is your company?",
        options=[
            "Sole proprietorship",
            "Private limited company",
            "General partnership",
            "Limited partnership",
            "Public limited company",
            "Association",
            "Branch of another company",
            "Non-profit"
        ],
        index=None if st.session_state.legal_structure is None else [
            "Sole proprietorship",
            "Private limited company",
            "General partnership",
            "Limited partnership",
            "Public limited company",
            "Association",
            "Branch of another company",
            "Non-profit"
        ].index(st.session_state.legal_structure)
    )

    st.session_state.financial_funding = st.multiselect(
        "How is your company currently financed?",
        options=[
            "Own financing",
            "Funding from investors",
            "Bank loan",
            "Revenue from sales",
            "Other"
        ],
        default=st.session_state.financial_funding,
        max_selections=5
    )

    st.session_state.business_sector = st.radio(
        "Which industrial sector does your company operate in?",
        options=[
            "Raw materials (eg mining, steel, trading companies)",
            "Industrial business (e.g. means of production, transport)",
            "Services (e.g. commercial and professional services, tourism)",
            "Durable consumer goods (e.g., furniture, clothing, retail)",
            "Fast-moving consumer goods (e.g., food, beverages, personal products)",
            "Healthcare (e.g., healthcare equipment, pharmaceuticals)",
            "Financial sectors (e.g., banks, insurance)",
            "Information technology",
            "Utilities and energy",
            "Culture and entertainment"
        ],
        index=None if st.session_state.business_sector is None else 0  # Adjust as needed
    )

    # Conditional fields for business sector subtypes (assuming based on selection)
    if st.session_state.business_sector == "Raw materials (eg mining, steel, trading companies)":
        st.session_state.raw_materials_type = st.radio("Specify type:", options=["Mining", "Steel", "Trading", "Other"])
    # Add similar conditionals for other sectors as needed...

    st.session_state.primary_countries = st.text_input(
        "In which countries does your company primarily operate?",
        value=st.session_state.primary_countries
    )

    st.session_state.product_centralisation = st.radio(
        "Is your product/service centralized or decentralized?",
        options=["Centralized", "Decentralized"],
        index=None
    )

    st.session_state.product_range = st.radio(
        "What is the range of your product/service?",
        options=["Narrow", "Medium", "Wide"],
        index=None
    )

    st.session_state.end_consumer_characteristics = st.text_area(
        "What characterizes the end consumer of your product/service?",
        value=st.session_state.end_consumer_characteristics
    )

    st.session_state.end_consumer_characteristics_2 = st.multiselect(
        "What types of end consumers are there?",
        options=["Individuals", "Businesses", "Government", "Other"],
        default=st.session_state.end_consumer_characteristics_2
    )

    st.session_state.product_service_description = st.text_area(
        "Describe your products or services:",
        value=st.session_state.product_service_description
    )

elif st.session_state.page == 2:
    st.header("Part 2: Segmentation and Revenue Information")
    st.session_state.segment_name = st.text_input(
        "Name of the most relevant customer segment:",
        value=st.session_state.segment_name
    )

    st.session_state.segment_demographics = st.text_area(
        "Demographics of the segment:",
        value=st.session_state.segment_demographics
    )

    st.session_state.segment_characteristics = st.text_area(
        "Characteristics of the segment:",
        value=st.session_state.segment_characteristics
    )

    st.session_state.customer_count = st.text_input(
        "Approximate number of customers:",
        value=st.session_state.customer_count
    )

    st.session_state.problems_faced = st.text_area(
        "Problems your company solves for customers:",
        value=st.session_state.problems_faced
    )

    st.session_state.biggest_competitors = st.text_input(
        "Biggest competitors:",
        value=st.session_state.biggest_competitors
    )

    st.session_state.competition_intensity = st.radio(
        "Intensity of competition:",
        options=["Low", "Medium", "High"],
        index=None
    )

    st.session_state.price_comparison = st.radio(
        "Price comparison to competitors:",
        options=["Lower", "Similar", "Higher"],
        index=None
    )

    st.session_state.market_type = st.radio(
        "Market type:",
        options=["Monopoly", "Oligopoly", "Competitive"],
        index=None
    )

    st.session_state.competitive_parameters = st.multiselect(
        "Competitive parameters your company excels in:",
        options=["Quality", "Price", "Innovation", "Service", "Other"],
        default=st.session_state.competitive_parameters
    )

    st.session_state.value_propositions = st.multiselect(
        "Value propositions:",
        options=["Efficiency", "Quality", "Cost", "Innovation", "Other"],
        default=st.session_state.value_propositions
    )

    st.session_state.direct_income = st.radio(
        "Direct income from customers?",
        options=["Yes", "No"],
        index=None
    )

    st.session_state.primary_revenue = st.multiselect(
        "Primary revenue sources:",
        options=["Sales", "Subscriptions", "Ads", "Other"],
        default=st.session_state.primary_revenue
    )

    # Add more fields as per the original code...

elif st.session_state.page == 3:
    st.header("Part 3: Resources, Partners, and Team")
    st.session_state.material_resources = st.multiselect(
        "Material resources:",
        options=["Equipment", "Facilities", "Inventory", "Other"],
        default=st.session_state.material_resources
    )

    st.session_state.intangible_resources = st.multiselect(
        "Intangible resources:",
        options=["Patents", "Brands", "Software", "Other"],
        default=st.session_state.intangible_resources
    )

    st.session_state.important_activities = st.multiselect(
        "Important activities:",
        options=["Production", "Marketing", "R&D", "Other"],
        default=st.session_state.important_activities
    )

    st.session_state.inhouse_activities = st.multiselect(
        "In-house activities:",
        options=["Core operations", "Support functions", "Other"],
        default=st.session_state.inhouse_activities
    )

    st.session_state.outsourced_activities = st.multiselect(
        "Outsourced activities:",
        options=["Logistics", "IT", "Manufacturing", "Other"],
        default=st.session_state.outsourced_activities
    )

    st.session_state.company_statements = st.multiselect(
        "Company statements:",
        options=["Mission", "Vision", "Values", "Other"],
        default=st.session_state.company_statements
    )

    st.session_state.important_strategic_partners = st.multiselect(
        "Important strategic partners:",
        options=["Suppliers", "Distributors", "Allies", "Other"],
        default=st.session_state.important_strategic_partners
    )

    st.session_state.partnership_benefits = st.multiselect(
        "Partnership benefits:",
        options=[
            "Cost reduction (e.g. economies of scale, up-selling, raw material cost reduction, sharing common infrastructure)",
            "Reducing risk",
            "Access to important information (e.g. market knowledge, research and development, legislation)",
            "Outsourcing of activities (e.g. business partners sell/deliver products/services to our customers)",
            "Increases bargaining power",
            "Access to special customer segments",
            "Access to critical resources",
            "Funding/Financing",
            "Other"
        ],
        default=st.session_state.partnership_benefits,
        max_selections=3
    )

    if "Other" in st.session_state.partnership_benefits:
        st.session_state.other_benefit = st.text_input(
            "Please specify the other benefit:",
            value=st.session_state.other_benefit
        )

    st.session_state.company_dependency = st.radio(
        "Company dependency on partners:",
        options=["Not Dependent", "Somewhat Dependent", "Dependent", "Highly Dependent", "Completely Dependent"],
        index=None
    )

    st.session_state.cost_intensive_components = st.multiselect(
        "Most cost-intensive components:",
        options=[
            "Administration, finance and management/control",
            "Building and maintaining customer relationships",
            "Building and maintaining partnerships",
            "Follow-up sales and service activities",
            "Management and employee development",
            "Inbound logistics",
            "Outbound logistics",
            "Marketing Department",
            "Sales Department",
            "Advising and solving clients' unique challenges",
            "Procurement Department",
            "Production Department",
            "R&D (research and development)"
        ],
        default=st.session_state.cost_intensive_components,
        max_selections=3
    )

    st.session_state.team_members = st.text_area(
        "Describe team members, positions, and competencies:",
        value=st.session_state.team_members
    )

    st.session_state.funding_amount = st.text_input(
        "Funding amount (if applying, in DKK):",
        value=st.session_state.funding_amount
    )

    if st.session_state.funding_amount:
        st.session_state.funding_purpose = st.text_area(
            "Funding purpose:",
            value=st.session_state.funding_purpose
        )

if st.session_state.page == 3 and st.button("Generate Business Plan"):
    with st.spinner("🧠 Generating your business plan..."):
        try:
            data = {
                "business_name": st.session_state.business_name,
                "start_year": st.session_state.start_year,
                "business_reason": st.session_state.business_reason,
                "mission_vision": st.session_state.mission_vision,
                "legal_structure": st.session_state.legal_structure,
                "financial_funding": st.session_state.financial_funding,
                "business_sector": st.session_state.business_sector,
                "raw_materials_type": st.session_state.raw_materials_type,
                "industrial_business_type": st.session_state.industrial_business_type,
                "services_type": st.session_state.services_type,
                "durable_goods_type": st.session_state.durable_goods_type,
                "consumer_goods_type": st.session_state.consumer_goods_type,
                "healthcare_type": st.session_state.healthcare_type,
                "financial_sector_type": st.session_state.financial_sector_type,
                "it_sector_type": st.session_state.it_sector_type,
                "utilities_type": st.session_state.utilities_type,
                "culture_type": st.session_state.culture_type,
                "primary_countries": st.session_state.primary_countries,
                "product_centralisation": st.session_state.product_centralisation,
                "product_range": st.session_state.product_range,
                "end_consumer_characteristics": st.session_state.end_consumer_characteristics,
                "end_consumer_characteristics_2": st.session_state.end_consumer_characteristics_2,
                "product_service_description": st.session_state.product_service_description,
                "segment_name": st.session_state.segment_name,
                "segment_demographics": st.session_state.segment_demographics,
                "segment_characteristics": st.session_state.segment_characteristics,
                "customer_count": st.session_state.customer_count,
                "problems_faced": st.session_state.problems_faced,
                "biggest_competitors": st.session_state.biggest_competitors,
                "competition_intensity": st.session_state.competition_intensity,
                "price_comparison": st.session_state.price_comparison,
                "market_type": st.session_state.market_type,
                "competitive_parameters": st.session_state.competitive_parameters,
                "value_propositions": st.session_state.value_propositions,
                "direct_income": st.session_state.direct_income,
                "primary_revenue": st.session_state.primary_revenue,
                "one_time_payments": st.session_state.one_time_payments,
                "ongoing_payments": st.session_state.ongoing_payments,
                "payment_characteristics": st.session_state.payment_characteristics,
                "package_price": st.session_state.package_price,
                "price_negotiation": st.session_state.price_negotiation,
                "fixed_prices": st.session_state.fixed_prices,
                "dynamic_prices": st.session_state.dynamic_prices,
                "distribution_channels": st.session_state.distribution_channels,
                "purchasing_power": st.session_state.purchasing_power,
                "product_related_characteristics": st.session_state.product_related_characteristics,
                "self_service_availability": st.session_state.self_service_availability,
                "online_communities_presence": st.session_state.online_communities_presence,
                "development_process_customer_involvement": st.session_state.development_process_customer_involvement,
                "after_sale_purchases": st.session_state.after_sale_purchases,
                "personal_assistance_offered": st.session_state.personal_assistance_offered,
                "similar_products_switch": st.session_state.similar_products_switch,
                "general_customer_relation": st.session_state.general_customer_relation,
                "material_resources": st.session_state.material_resources,
                "intangible_resources": st.session_state.intangible_resources,
                "important_activities": st.session_state.important_activities,
                "inhouse_activities": st.session_state.inhouse_activities,
                "outsourced_activities": st.session_state.outsourced_activities,
                "company_statements": st.session_state.company_statements,
                "important_strategic_partners": st.session_state.important_strategic_partners,
                "partnership_benefits": st.session_state.partnership_benefits,
                "other_benefit": st.session_state.other_benefit,
                "company_dependency": st.session_state.company_dependency,
                "cost_intensive_components": st.session_state.cost_intensive_components,
                "team_members": st.session_state.team_members,
                "funding_amount": st.session_state.funding_amount,
                "funding_purpose": st.session_state.funding_purpose
            }

            response = requests.post(
                "http://localhost:8000/generate_business_plan",
                json=data
            )

            if response.status_code == 200:
                result = response.json()
                business_plan_markdown = result["business_plan"]

                st.markdown(business_plan_markdown, unsafe_allow_html=True)

                st.success("✅ Business Plan ready!")

                st.download_button(
                    label="Download Business Plan",
                    data=business_plan_markdown,
                    file_name="generated_business_plan.md",
                    mime="text/markdown"
                )
            else:
                st.error(f"Error: {response.text}")
        except Exception as e:
            st.error(f"Error connecting to the server: {str(e)}")

