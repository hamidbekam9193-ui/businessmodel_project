import os
import traceback
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

from src.main import BusinessPlanFlow, BusinessPlanState

load_dotenv()

app = FastAPI(
    title="Business Plan Generator API",
    description="An API to generate a comprehensive business plan using AI agents.",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Business Plan Generator API is running"}

class BusinessPlanRequest(BaseModel):
    # --- CHANGE START 1: Add the API key field ---
    gemini_api_key: str
    # --- CHANGE END 1 ---

    # ... (all other fields remain the same as the previous fix)
    business_name: str
    start_year: str
    # ... etc. (ensure all Optional fields from the 422 fix are here)
    legal_structure: Optional[str] = ""
    financial_funding: List[str]
    business_sector: Optional[str] = ""
    product_service_description: str
    raw_materials_type: Optional[str] = ""
    industrial_business_type: Optional[str] = ""
    services_type: Optional[str] = ""
    durable_goods_type: Optional[str] = ""
    consumer_goods_type: Optional[str] = ""
    healthcare_type: Optional[str] = ""
    financial_sector_type: Optional[str] = ""
    it_sector_type: Optional[str] = ""
    utilities_type: Optional[str] = ""
    culture_type: Optional[str] = ""
    primary_countries: str
    product_centralisation: Optional[str] = ""
    product_range: Optional[str] = ""
    end_consumer_characteristics: Optional[str] = ""
    end_consumer_characteristics_2: List[str]
    segment_name: str
    segment_demographics: str
    segment_characteristics: str
    customer_count: str
    problems_faced: str
    biggest_competitors: str
    competition_intensity: Optional[str] = ""
    price_comparison: Optional[str] = ""
    market_type: Optional[str] = ""
    competitive_parameters: List[str]
    value_propositions: List[str]
    direct_income: Optional[str] = ""
    primary_revenue: List[str]
    one_time_payments: Optional[List[str]] = []
    ongoing_payments: Optional[List[str]] = []
    payment_characteristics: Optional[List[str]] = []
    package_price: Optional[str] = ""
    price_negotiation: Optional[str] = ""
    fixed_prices: Optional[List[str]] = []
    dynamic_prices: Optional[List[str]] = []
    distribution_channels: List[str]
    purchasing_power: Optional[str] = ""
    product_related_characteristics: List[str]
    self_service_availability: Optional[str] = ""
    online_communities_presence: Optional[str] = ""
    development_process_customer_involvement: Optional[str] = ""
    after_sale_purchases: Optional[str] = ""
    personal_assistance_offered: Optional[str] = ""
    similar_products_switch: Optional[str] = ""
    general_customer_relation: Optional[str] = ""
    material_resources: List[str]
    intangible_resources: List[str]
    important_activities: List[str]
    inhouse_activities: List[str]
    outsourced_activities: Optional[List[str]] = []
    company_statements: Optional[List[str]] = []
    important_strategic_partners: List[str]
    partnership_benefits: List[str]
    other_benefit: Optional[str] = ""
    company_dependency: Optional[str] = ""
    cost_intensive_components: List[str]
    team_members: str
    funding_amount: str
    funding_purpose: str

class BusinessPlanResponse(BaseModel):
    business_plan: str

def collect_business_plan_inputs(request: BusinessPlanRequest) -> dict:
    # This function remains unchanged
    def safe_join(lst):
        return ", ".join(lst) if lst else ""
    inputs = request.model_dump(exclude={'gemini_api_key'})
    for key, value in inputs.items():
        if isinstance(value, list):
            inputs[key] = safe_join(value)
    return inputs

@app.post("/generate_business_plan", response_model=BusinessPlanResponse)
async def generate_business_plan(request: BusinessPlanRequest):
    try:
        # --- CHANGE START 2: Set the environment variable from the request ---
        if not request.gemini_api_key:
            raise HTTPException(status_code=400, detail="GEMINI_API_KEY is required in the request.")
        os.environ['GEMINI_API_KEY'] = request.gemini_api_key
        # --- CHANGE END 2 ---

        print("Received request to generate business plan.")
        inputs = collect_business_plan_inputs(request)
        initial_state = BusinessPlanState(user_inputs=inputs)
        flow = BusinessPlanFlow()
        state_result = await flow.kickoff_async(initial_state.model_dump())

        if isinstance(state_result, BaseModel):
            state_dict = state_result.model_dump()
        elif isinstance(state_result, dict):
            state_dict = state_result
        else:
            raise ValueError("Flow result is not a dict or Pydantic model")

        bp_value = state_dict.get("business_plan")
        if isinstance(bp_value, dict) and "raw" in bp_value:
            state_dict["business_plan"] = bp_value["raw"]
        
        final_state = BusinessPlanState(**state_dict)

        print("Business plan generation complete.")
        return BusinessPlanResponse(business_plan=final_state.business_plan)
    
    except Exception as e:
        print(f"An error occurred: {e}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"An internal error occurred: {str(e)}")
