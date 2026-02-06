from typing import Any, Optional, Callable
from datetime import datetime
from pydantic import BaseModel
from sqlalchemy import BigInteger, Enum, DateTime, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from spm.files.models import (
	File
)
from spm.database.core import Base
from spm.users.models import User
from .consts import (
	PROJECT_STATUS,
	PROJECT_TYPE,
	PROJECT_LOCATION_TYPE,
	PROJECT_LOCATION_SETTLEMENT,
	CONTRACT_ASSIGNMENT_TYPE,
	CONTRACT_SOURCE_OF_FINANCING,
	PRAYER_ROOM_FLOOR,
)

class Project(Base):
	__tablename__ = "projects"

	id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
	created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
	creator: Mapped[User] = mapped_column(ForeignKey("users.id"))

	# IT
	title: Mapped[str] = mapped_column(String(100), nullable=False)
	commencement_at: Mapped[datetime] = mapped_column(DateTime)
	operation_at_expected: Mapped[datetime] = mapped_column(DateTime)
	operation_at: Mapped[datetime] = mapped_column(DateTime)
	status: Mapped[PROJECT_STATUS] = mapped_column(Enum(PROJECT_STATUS), nullable=False)
	zooning_code: Mapped[str] = mapped_column(String(50), nullable=True)

	# Surveying Unit
	project_type: Mapped[Optional[PROJECT_TYPE]] = mapped_column(Enum(PROJECT_TYPE), nullable=True)
	location_type: Mapped[Optional[PROJECT_LOCATION_TYPE]] = mapped_column(Enum(PROJECT_LOCATION_TYPE), nullable=True)
	project_old_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
	latitude: Mapped[Optional[float]] = mapped_column(Float(20), nullable=True)
	longitude: Mapped[Optional[float]] = mapped_column(Float(20), nullable=True)
	location_sattlement:Mapped[Optional[PROJECT_LOCATION_SETTLEMENT]] = mapped_column(Enum(PROJECT_LOCATION_SETTLEMENT), nullable=True)
	city_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
	village_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
	district: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
	zip_code: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

	# Technical Office Unit
	land_area: Mapped[Optional[float]] = mapped_column(Float(20), nullable=True)
	main_building_area: Mapped[Optional[float]] = mapped_column(Float(20), nullable=True)
	floors_count: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
	basement_area: Mapped[Optional[float]] = mapped_column(Float(20), nullable=True)
	basement_rooms_count: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
	ground_floor_area: Mapped[Optional[float]] = mapped_column(Float(20), nullable=True)
	ground_floor_rooms_count: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
	first_floor_area: Mapped[Optional[float]] = mapped_column(Float(20), nullable=True)
	first_floor_rooms_count: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
	second_floor_area: Mapped[Optional[float]] = mapped_column(Float(20), nullable=True)
	second_floor_rooms_count: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
	third_floor_area: Mapped[Optional[float]] = mapped_column(Float(20), nullable=True)
	third_floor_rooms_count: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
	attic_area: Mapped[Optional[float]] = mapped_column(Float(20), nullable=True)
	attic_rooms_count: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
	prayer_room_area: Mapped[Optional[float]] = mapped_column(Float(20), nullable=True)
	prayer_room_floor: Mapped[Optional[PRAYER_ROOM_FLOOR]] = mapped_column(Enum(PRAYER_ROOM_FLOOR), nullable=True)
	restrooms_present: Mapped[Optional[bool]] = mapped_column(Boolean, default=False, nullable=True)
	restroom_fixtures_count: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
	caretaker_area: Mapped[Optional[float]] = mapped_column(Float(20), nullable=True)
	caretaker_inside_building: Mapped[Optional[bool]] = mapped_column(Boolean, default=False, nullable=True)
	caretaker_and_guard_together: Mapped[Optional[bool]] = mapped_column(Boolean, default=False, nullable=True)
	gym_area: Mapped[Optional[float]] = mapped_column(Float(20), nullable=True)
	total_built_area: Mapped[Optional[float]] = mapped_column(Float(20), nullable=True)
	classes_count: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
	admin_rooms_count: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
	auxiliary_rooms_count: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
	labs_count: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
	labs_area: Mapped[Optional[float]] = mapped_column(Float(20), nullable=True)
	workshops_count: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
	workshops_area: Mapped[Optional[float]] = mapped_column(Float(20), nullable=True)
	libraries_count: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
	libraries_area: Mapped[Optional[float]] = mapped_column(Float(20), nullable=True)
	wall_one_face_area: Mapped[Optional[float]] = mapped_column(Float(20), nullable=True)
	wall_two_face_area: Mapped[Optional[float]] = mapped_column(Float(20), nullable=True)
	landscaping_area: Mapped[Optional[float]] = mapped_column(Float(20), nullable=True)
	construction_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
	additional_notes: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
	blueprint_dwg: Mapped[Optional[File]] = mapped_column(ForeignKey("files.id"), nullable=True)
	blueprint_pdf: Mapped[Optional[File]] = mapped_column(ForeignKey("files.id"), nullable=True)

	# Public Participation Unit
	landowners_committed_code: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
	land_owner_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
	building_contractor_code: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
	founder_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
	source_of_financing: Mapped[CONTRACT_SOURCE_OF_FINANCING] = mapped_column(Enum(CONTRACT_SOURCE_OF_FINANCING), nullable=True)
	commitment_code: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
	agreement_code: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
	commitment_amount: Mapped[Optional[float]] = mapped_column(Float(20), nullable=True)
	memorandum_of_understanding_doc: Mapped[File] = mapped_column(ForeignKey("files.id"), nullable=True)
	memorandum_of_understanding_pdf: Mapped[File] = mapped_column(ForeignKey("files.id"), nullable=True)

	# Building Supervisor Unit
	visit_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
	main_building_physical_progress_percentage: Mapped[Optional[float]] = mapped_column(Float(5), nullable=True)
	main_building_work_stage: Mapped[Optional[str]] = mapped_column(String(400), nullable=True)
	toilet_physical_progress_percentage: Mapped[Optional[float]] = mapped_column(Float(5), nullable=True)
	toilet_work_stage: Mapped[Optional[str]] = mapped_column(String(400), nullable=True)
	caretaker_physical_progress_percentage: Mapped[Optional[float]] = mapped_column(Float(5), nullable=True)
	caretaker_work_stage: Mapped[Optional[str]] = mapped_column(String(400), nullable=True)
	wall_construction_physical_progress_percentage: Mapped[Optional[float]] = mapped_column(Float(5), nullable=True)
	wall_construction_work_stage: Mapped[Optional[str]] = mapped_column(String(400), nullable=True)
	landscaping_physical_progress_percentage: Mapped[Optional[float]] = mapped_column(Float(5), nullable=True)
	landscaping_work_stage: Mapped[Optional[str]] = mapped_column(String(400), nullable=True)
	gym_physical_progress_percentage: Mapped[Optional[float]] = mapped_column(Float(5), nullable=True)
	gym_work_stage: Mapped[Optional[str]] = mapped_column(String(400), nullable=True)
	head_coach_and_guard_physical_progress_percentage: Mapped[Optional[float]] = mapped_column(Float(5), nullable=True)
	head_coach_and_guard_work_stage: Mapped[Optional[str]] = mapped_column(String(400), nullable=True)
	total_physical_progress_percentage: Mapped[Optional[float]] = mapped_column(Float(5), nullable=True)
	project_site_photo: Mapped[File] = mapped_column(ForeignKey("files.id"), nullable=True)

	# Financial performance report
	charity_expenditure: Mapped[Optional[float]] = mapped_column(Float(20), nullable=True)
	government_expenditure: Mapped[Optional[float]] = mapped_column(Float(20), nullable=True)
	
	# Public Relations Unit
	final_project_naming: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
	opening_ceremony_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
	final_project_photo: Mapped[File] = mapped_column(ForeignKey("files.id"), nullable=True)

	# Accounting unit
	provisional_delivery_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
	definite_delivery_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

class ProjectContract(Base):
	__tablename__ = "projects_contracts"

	id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
	project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)
	created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

	plan_code: Mapped[str] = mapped_column(String(50), nullable=False)
	plan_title: Mapped[str] = mapped_column(String(100), nullable=False)
	project_code: Mapped[str] = mapped_column(String(50), nullable=False)
	
	contract_number: Mapped[str] = mapped_column(String(50), nullable=False)
	contract_create_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
	contract_period_months: Mapped[int] = mapped_column(BigInteger, nullable=False)
	contract_coefficient: Mapped[float] = mapped_column(Float(20), nullable=False)
	assignment_type: Mapped[CONTRACT_ASSIGNMENT_TYPE] = mapped_column(Enum(CONTRACT_ASSIGNMENT_TYPE), nullable=False)
	initial_estimate_amount: Mapped[float] = mapped_column(Float(20), nullable=False)
	contract_amount: Mapped[float] = mapped_column(Float(20), nullable=False)
	contractor: Mapped[str] = mapped_column(String(100), nullable=False)
	source_of_financing: Mapped[CONTRACT_SOURCE_OF_FINANCING] = mapped_column(Enum(CONTRACT_SOURCE_OF_FINANCING), nullable=False)
	agreement_summary_doc: Mapped[File] = mapped_column(ForeignKey("files.id"), nullable=False)
	agreement_summary_pdf: Mapped[File] = mapped_column(ForeignKey("files.id"), nullable=False)

# pydantic modes...
class CreateProject(BaseModel):
	title: str
	commencement_at: datetime
	operation_at_expected: datetime
	operation_at: datetime
	status: PROJECT_STATUS

	reffer_to_surveying: int
	reffer_to_contracts: int
	reffer_to_technical_assisstant: int
	reffer_to_public_participation: int
	reffer_to_building_supervisor: int
	reffer_to_facilities_supervisor: int
	reffer_to_financial_performance: int
	reffer_to_general_relations: int
	reffer_to_accounting:int

type ProjectConstrain = list[str]

type ProjectConstrainMetaFunc = Callable[
	[],
	ProjectConstrain
]