import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Initialize environment
load_dotenv()
RAILWAY_URL = os.getenv('RAILWAY_DB_URL')
engine = create_engine(RAILWAY_URL, connect_args={'options':'-c search_path="SARG_SW"'})

# Initialize select statements
query_string_questionnaire_db = text('select * from questionnaire_db;')
query_string_hs_codes_db = text('select * from hs_codes_db;')

# Initialize insert statement
insert_into_questionnaire_db = text(
    """
    insert into questionnaire_db(
        company_representative_name,
        company_representative_email_id,
        company_name,
        company_state,
        company_city,
        company_legal_structure,
        member_of_industry_body,
        member_of_fieo_entities,
        primary_industry,
        product_hs_code,
        primary_source,
        company_sector,
        ideal_showroom_size_in_sqm,
        mezzanine_floor_required,
        primary_intended_use_of_facility,
        warehousing_need_captive_or_common,
        warehouse_size_if_captive,
        monthly_trade_volumes_cbm_or_mt,
        monthly_trade_volumes_units,
        types_of_goods_for_storage_and_distribution,
        storage_type_bulk_palletized,
        storage_type_ac_ambient,
        storage_type_cc_refrigerated,
        shared_services_requirement,
        common_user_processing_req,
        common_user_processing_req_value_addition_details,
        export_countries,
        priority_gcc_me_cis_countries_for_export,
        distribution_in_uae,
        expected_annual_trade_vol_via_bm_ind_to_uae,
        frequency_of_anticipated_shipments_from_india,
        india_uae_cepa_awareness,
        cepa_leverage_strategy,
        val_added_serv_requirement_for_cepa_at_origin,
        support_with_cepa_compliance_documentation,
        expected_annual_rent_for_showroom_space_aed,
        percetage_as_service_charge_for_maint_and_ops,
        willingness_to_pay_booking_fee,
        benefit_from_dedicated_online_market_place,
        third_party_requirement_for_service_delivery,
        concerns_challenges,
        expected_timline_for_launch,
        dubai_business_license_availability,
        lease_sublease_cosharing_preference,
        long_vs_short_term_lease_arrangement
    )values(
        :company_representative_name,
        :company_representative_email_id,
        :company_name,
        :company_state,
        :company_city,
        :company_legal_structure,
        :member_of_industry_body,
        :member_of_fieo_entities,
        :primary_industry,
        :product_hs_code,
        :primary_source,
        :company_sector,
        :ideal_showroom_size_in_sqm,
        :mezzanine_floor_required,
        :primary_intended_use_of_facility,
        :warehousing_need_captive_or_common,
        :warehouse_size_if_captive,
        :monthly_trade_volumes_cbm_or_mt,
        :monthly_trade_volumes_units,
        :types_of_goods_for_storage_and_distribution,
        :storage_type_bulk_palletized,
        :storage_type_ac_ambient,
        :storage_type_cc_refrigerated,
        :shared_services_requirement,
        :common_user_processing_req,
        :common_user_processing_req_value_addition_details,
        :export_countries,
        :priority_gcc_me_cis_countries_for_export,
        :distribution_in_uae,
        :expected_annual_trade_vol_via_bm_ind_to_uae,
        :frequency_of_anticipated_shipments_from_india,
        :india_uae_cepa_awareness,
        :cepa_leverage_strategy,
        :val_added_serv_requirement_for_cepa_at_origin,
        :support_with_cepa_compliance_documentation,
        :expected_annual_rent_for_showroom_space_aed,
        :percetage_as_service_charge_for_maint_and_ops,
        :willingness_to_pay_booking_fee,
        :benefit_from_dedicated_online_market_place,
        :third_party_requirement_for_service_delivery,
        :concerns_challenges,
        :expected_timline_for_launch,
        :dubai_business_license_availability,
        :lease_sublease_cosharing_preference,
        :long_vs_short_term_lease_arrangement
    )
    """
)

# Function to insert records into questionnaire_db table
def insert_into_questionnaire_db(payload: dict):
    with engine.begin() as conn:
        conn.execute(insert_into_questionnaire_db, payload)

# Function to select data from hs_codes_db table - main table containing hs codes and their descriptions
def select_from_hs_codes_db():
    sql_hs_codes = query_string_hs_codes_db
    with engine.begin() as conn:
        rows = conn.execute(sql_hs_codes).mappings().all() # Converts each row into a JSON type dictionary.
        return [dict(r) for r in rows]

# Function to select data from questionnaire_db table - main table containing all responses
def select_from_questionnaire_db():
    sql_questionnaire = query_string_questionnaire_db
    with engine.begin() as conn:
        data = conn.execute(sql_questionnaire).mappings().all() # Converts each row into a JSON type dictionary.
        return [dict(d) for d in data]