from typing import Any
from datetime import datetime
import random
from sqlalchemy import update, select
from sqlalchemy.orm import Session
from spm.units.consts import UNIT
from spm.users.models import User
from spm.reffer import service as reffer_service
from .models import (
	CreateProject,
	Project,
	ProjectContract,
	ProjectConstrain,
	ProjectConstrainMetaFunc,
)

constraints:dict[UNIT, ProjectConstrain] = {}

def register_project_constrain_meta(unit:UNIT, form_func:ProjectConstrainMetaFunc):
	global constraints
	constraints[unit] = form_func()

def get_unit_project_constrain(unit:UNIT):
	return constraints[unit]

def get_project(
	project_id: int,
	session: Session
):
	project = session.query(Project).filter(
		Project.id == project_id
	).one()

	return project

def get_contracts(
	project_id: int,
	session: Session
):
	contract = session.query(ProjectContract).filter(
		ProjectContract.project_id == project_id
	).all()

	return contract

def file_object(value: Any):
	return {
		"type": "file",
		"value": value
	}

def get_project_all_properties(
	project_id: int,
	session: Session
) -> dict[str, Any]:
	project = get_project(project_id, session)
	contracts = get_contracts(project_id, session)

	return {
			"id" : project.id,
			"created_at" : project.created_at,

			# IT
			"title" : project.title,
			"commencement_at" : project.commencement_at,
			"operation_at_expected" : project.operation_at_expected,
			"operation_at" : project.operation_at,
			"status" : project.status,
			"zooning_code" : project.zooning_code,

			# Surveying Unit
			"project_type" : project.project_type,
			"location_type" : project.location_type,
			"project_old_name" : project.project_old_name,
			"latitude" : project.latitude,
			"longitude" : project.longitude,
			"location_sattlemen" : project.location_sattlement,
			"city_name" : project.city_name,
			"village_name" : project.village_name,
			"district" : project.district,
			"zip_code" : project.zip_code,

			# Contracts Unit
			"contracts": [
				{
					"id": contract.id,
					"project_id": contract.project_id,
					"created_at": contract.created_at,

					"plan_code": contract.plan_code,
					"plan_title": contract.plan_title,
					"project_code": contract.project_code,

					"contract_period_months": contract.contract_period_months,
					"contract_number": contract.contract_number,
					"contract_coefficient": contract.contract_coefficient,
					"assignment_type": contract.assignment_type,
					"initial_estimate_amount": contract.initial_estimate_amount,
					"contract_amount": contract.contract_amount,
					"contractor": contract.contractor,
					"source_of_financing": contract.source_of_financing,
					"agreement_summary_doc": file_object(contract.agreement_summary_doc),
					"agreement_summary_pdf": file_object(contract.agreement_summary_pdf)
				}
				for contract in contracts
			],

			# Technical Office Unit
			"land_area" : project.land_area,
			"main_building_area" : project.main_building_area,
			"floors_count" : project.floors_count,
			"basement_area" : project.basement_area,
			"basement_rooms_count" : project.basement_rooms_count,
			"ground_floor_area" : project.ground_floor_area,
			"ground_floor_rooms_count" : project.ground_floor_rooms_count,
			"first_floor_area" : project.first_floor_area,
			"first_floor_rooms_count" : project.first_floor_rooms_count,
			"second_floor_area" : project.second_floor_area,
			"second_floor_rooms_count" : project.second_floor_rooms_count,
			"third_floor_area" : project.third_floor_area,
			"third_floor_rooms_count" : project.third_floor_rooms_count,
			"attic_area" : project.attic_area,
			"attic_rooms_count" : project.attic_rooms_count,
			"prayer_room_area" : project.prayer_room_area,
			"prayer_room_floor" : project.prayer_room_floor,
			"restrooms_present" : project.restrooms_present,
			"restroom_fixtures_count" : project.restroom_fixtures_count,
			"caretaker_area" : project.caretaker_area,
			"caretaker_inside_building" : project.caretaker_inside_building,
			"caretaker_and_guard_together" : project.caretaker_and_guard_together,
			"gym_area" : project.gym_area,
			"total_built_area" : project.total_built_area,
			"classes_count" : project.classes_count,
			"admin_rooms_count" : project.admin_rooms_count,
			"auxiliary_rooms_count" : project.auxiliary_rooms_count,
			"labs_count" : project.labs_count,
			"labs_area" : project.labs_area,
			"workshops_count" : project.workshops_count,
			"workshops_area" : project.workshops_area,
			"libraries_count" : project.libraries_count,
			"libraries_area" : project.libraries_area,
			"wall_one_face_area" : project.wall_one_face_area,
			"wall_two_face_area" : project.wall_two_face_area,
			"landscaping_area" : project.landscaping_area,
			"construction_type" : project.construction_type,
			"additional_notes" : project.additional_notes,
			"blueprint_dwg" : file_object(project.blueprint_dwg),
			"blueprint_pdf" : file_object(project.blueprint_pdf),

			# Public Participation Unit
			"landowners_committed_code" : project.landowners_committed_code,
			"land_owner_name" : project.land_owner_name,
			"building_contractor_code" : project.building_contractor_code,
			"founder_name" : project.founder_name,
			"commitment_code" : project.commitment_code,
			"agreement_code" : project.agreement_code,
			"commitment_amount" : project.commitment_amount,
			"memorandum_of_understanding_doc" : file_object(project.memorandum_of_understanding_doc),
			"memorandum_of_understanding_pdf" : file_object(project.memorandum_of_understanding_pdf),

			# Building Supervisor Unit
			"visit_date" : project.visit_date,
			"main_building_physical_progress_percentage" : project.main_building_physical_progress_percentage,
			"main_building_work_stage" : project.main_building_work_stage,
			"toilet_physical_progress_percentage" : project.toilet_physical_progress_percentage,
			"toilet_work_stage" : project.toilet_work_stage,
			"caretaker_physical_progress_percentage" : project.caretaker_physical_progress_percentage,
			"caretaker_work_stage" : project.caretaker_work_stage,
			"wall_construction_physical_progress_percentage" : project.wall_construction_physical_progress_percentage,
			"wall_construction_work_stage" : project.wall_construction_work_stage,
			"landscaping_physical_progress_percentage" : project.landscaping_physical_progress_percentage,
			"landscaping_work_stage" : project.landscaping_work_stage,
			"gym_physical_progress_percentage" : project.gym_physical_progress_percentage,
			"gym_work_stage" : project.gym_work_stage,
			"head_coach_and_guard_physical_progress_percentage" : project.head_coach_and_guard_physical_progress_percentage,
			"head_coach_and_guard_work_stage" : project.head_coach_and_guard_work_stage,
			"total_physical_progress_percentage" : project.total_physical_progress_percentage,
			"project_site_photo" : file_object(project.project_site_photo),

			# Financial performance report
			"charity_expenditure" : project.charity_expenditure,
			"government_expenditure" : project.government_expenditure,
			
			# Public Relations Unit
			"final_project_naming" : project.final_project_naming,
			"opening_ceremony_date" : project.opening_ceremony_date,
			"final_project_photo" : file_object(project.final_project_photo),

			# Accounting unit
			"provisional_delivery_date" : project.provisional_delivery_date,
			"definite_delivery_date" : project.definite_delivery_date
	}

def get_project_properties_by_unit(
	project_id: int,
	unit: UNIT,
	session: Session
):
	properties = get_project_all_properties(project_id, session)
	if unit in (UNIT.SYSTEM_ADMINISTRATOR, UNIT.GENERAL_MANAGER):
		return properties
	
	constraints = get_unit_project_constrain(unit)

	res: dict[str, Any] = {k:v for k,v in properties.items() if k in constraints}

	return res

def create_project(
	user: User,
	model: CreateProject,
	session: Session
):
	random_id = random.randint(1*10**6, (1*10**7)-1) # six digit number
	
	project_object = Project(
		id = random_id,
		created_at = datetime.now(),
		creator = user.id,
		title = model.title,
		commencement_at = model.commencement_at,
		operation_at_expected = model.operation_at_expected,
		operation_at = model.operation_at,
		status = model.status,
	)

	session.add(project_object)

	reffer_service.refferal_user_to(
		user.id, model.reffer_to_surveying,
		random_id, session,
		UNIT.SURVEYING
	)
	reffer_service.refferal_user_to(
		user.id, model.reffer_to_contracts,
		random_id, session,
		UNIT.CONTRACTS
	)
	reffer_service.refferal_user_to(
		user.id, model.reffer_to_technical_assisstant,
		random_id, session,
		UNIT.TECHNICAl_ASSISSTANT
	)
	reffer_service.refferal_user_to(
		user.id, model.reffer_to_public_participation,
		random_id, session,
		UNIT.PUBLIC_PARTICIPATION
	)
	reffer_service.refferal_user_to(
		user.id, model.reffer_to_building_supervisor,
		random_id, session,
		UNIT.BUILDING_SUPERVISOR
	)
	reffer_service.refferal_user_to(
		user.id, model.reffer_to_facilities_supervisor,
		random_id, session,
		UNIT.FACILITIES_SUPERVISOR
	)
	reffer_service.refferal_user_to(
		user.id, model.reffer_to_financial_performance,
		random_id, session,
		UNIT.FINANCIAL_PERFORMANCE
	)
	reffer_service.refferal_user_to(
		user.id, model.reffer_to_general_relations,
		random_id, session,
		UNIT.GENERAL_RELATIONS
	)
	reffer_service.refferal_user_to(
		user.id, model.reffer_to_accounting,
		random_id, session,
		UNIT.ACCOUNTING
	)

	return random_id

def set_project_properties(
	project_id: int,
	properties: dict[str, Any],
	session: Session
):
	if len(properties) == 0:
		return
	
	stmt = (
		update(Project)
		.where(Project.id == project_id)
		.values(**properties)
	)

	session.execute(stmt)