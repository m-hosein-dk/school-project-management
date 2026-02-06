from typing import Any, Literal
from datetime import date, datetime
from sqlalchemy.orm import Session
from starlette.datastructures import UploadFile
from fastapi import HTTPException, status
from spm.files import service as files_service
from spm.database.service import get_class_by_tablename
from spm.users import service as users_service
from spm.projects.models import Project
from spm.projects import service as projects_service
from spm.units.consts import UNIT
from .models import (
	FormIn,
	Form,
	FormProjectProperty,
	FormProjectPropertyEnum,
	FormProjectPropertyFile,
	FormInsert,
	FormReffer
)

def validate_form(
	form: Form
):
	units_refferal_count:dict[UNIT, int] = {}

	for name, form_input in form.items():
		if isinstance(form_input, FormProjectProperty):
			# check properties
			if form_input.project_property not in Project.__table__.columns:
				raise HTTPException(
					status.HTTP_406_NOT_ACCEPTABLE,
					f"field {form_input.project_property} in form {name} has invalid property name"
				)

		elif isinstance(form_input, FormReffer):
			unit = form_input.unit
			if unit not in units_refferal_count:
				units_refferal_count[unit] = 0
			units_refferal_count[unit] += 1
			if units_refferal_count[unit] > 1:
				raise HTTPException(
					status.HTTP_406_NOT_ACCEPTABLE,
					"for refferals, each unit can only have one refferal field"
				)

		elif isinstance(form_input, FormInsert):
			# check min and maxes
			if form_input.min < 0:
				raise HTTPException(
					status.HTTP_406_NOT_ACCEPTABLE,
					f"field {name} has invalid min value"
				)

			if form_input.max < form_input.min:
				raise HTTPException(
					status.HTTP_406_NOT_ACCEPTABLE,
					f"field {name} has invalid max value"
				)

			# check table existence
			table = get_class_by_tablename(form_input.table_name)
			if not table:
				raise HTTPException(
					status.HTTP_406_NOT_ACCEPTABLE,
					f"field {name} has invalid table name"
				)
			
			# check properties of items
			for item_name, item in form_input.items.items():
				if item.property not in table.__table__.columns:
					raise HTTPException(
						status.HTTP_406_NOT_ACCEPTABLE,
						f"field {item_name} in form {name} has invalid property name"
					)

def do_type_correction(
	data: Any,
	type: str
):
	if type == "integer":
		try:
			return int(data)
		except ValueError:
			raise HTTPException(
				status.HTTP_406_NOT_ACCEPTABLE,
				"wrong type, expected an integer number for {name}"
			)

	elif type == "float":
		try:
			return float(data)
		except ValueError:
			raise HTTPException(
				status.HTTP_406_NOT_ACCEPTABLE,
				"wrong type, expected a floating number for {name}"
			)

	elif type == "date":
		try:
			return date.strptime(data, "%d/%m/%Y")
		except ValueError:
			raise HTTPException(
				status.HTTP_406_NOT_ACCEPTABLE,
				"wrong format, expected a date for {name}"
			)
	
	elif type == "datetime":
		try:
			return datetime.strptime(data, "%Y/%m/%d %H:%M:%S")
		except ValueError:
			raise HTTPException(
				status.HTTP_406_NOT_ACCEPTABLE,
				"wrong format, expected a datetime for {name}"
			)
	
	return data

def parse_form(
	form_in: FormIn,
	form: Form,
	session: Session
) -> FormIn:
	"validates and type-correnct's the form"

	project_id = form_in.project_id
	project = projects_service.get_project(project_id, session)
	if not project:
		raise HTTPException(
			status.HTTP_406_NOT_ACCEPTABLE,
			f"project with id {project_id} does not exist"
		)

	submited_form = form_in.input
	for name, form_input in form.items():
		value = submited_form.get(name, None)

		if isinstance(form_input, FormProjectProperty):
			if not value:
				if not form_input.is_optional:
					raise HTTPException(
						status.HTTP_406_NOT_ACCEPTABLE,
						f"missing required field {name}"
					)
				else:
					continue

			form_input_type = form_input.type

			form_in.input[name] = do_type_correction(
				value,
				form_input_type
			)

		if isinstance(form_input, FormProjectPropertyEnum):
			if not value:
				if not form_input.is_optional:
					raise HTTPException(
						status.HTTP_406_NOT_ACCEPTABLE,
						f"missing required field {name}"
					)
				else:
					continue

			enum_values = form_input.values
			if value not in map(lambda x: x[0], enum_values):
				raise HTTPException(
					status.HTTP_406_NOT_ACCEPTABLE,
					f"field {name} can only accept {enum_values}"
				)

			form_in.input[name] = value

		elif isinstance(form_input, FormReffer):
			if not value:
				raise HTTPException(
					status.HTTP_406_NOT_ACCEPTABLE,
					f"missing required field {name}"
				)

			try:
				user_id = int(value)
			except ValueError:
				raise HTTPException(
					status.HTTP_406_NOT_ACCEPTABLE,
					"wrong type, expected an integer for {name}"
				)

			user = users_service.get_user(user_id, session)
			if not user:
				raise HTTPException(
					status.HTTP_406_NOT_ACCEPTABLE,
					f"user with id {user_id} does not exist"
				)
			if not (user.unit == form_input.unit):
				raise HTTPException(
					status.HTTP_406_NOT_ACCEPTABLE,
					f"user with id {user_id} is not in unit {form_input.unit}"
				)

	return form_in

def get_form_refferals(
	form_in: FormIn,
	form: Form,
) -> list[int]:
	"returns all user ids reffered in the form"
	refferals: list[int] = []

	submited_form = form_in.input
	for name, value in submited_form.items():
		form_input = form.get(name, None)
		if isinstance(form_input, FormReffer):
			refferals.append(value)

	return refferals

def pop_form_files(
	form_in: FormIn,
	form: Form
):
	"removes all insert inputs from the form_in"
	submited_form = form_in.input
	result: list[tuple[FormProjectPropertyFile, UploadFile]] = []
	for name in list(submited_form.keys()):
		form_input = form.get(name, None)
		if isinstance(form_input, FormProjectPropertyFile):
			result.append((form_input, submited_form.pop(name)))
	
	return result

def pop_form_inserts(
	form_in: FormIn,
	form: Form,
):
	"removes all insert inputs from the form_in"
	submited_form = form_in.input
	result: list[tuple[FormInsert, dict]] = []
	for name in list(submited_form.copy().keys()):
		form_input = form.get(name, None)
		if isinstance(form_input, FormInsert):
			result.append((form_input, submited_form.pop(name)))
	
	return result

def validate_file_input(
	uploaded_file: UploadFile,
	allowed_extentions: Literal["*"] | list[str]
):
	if not isinstance(uploaded_file, UploadFile):
		raise HTTPException(
			status.HTTP_406_NOT_ACCEPTABLE,
			"wrong type for file"
		)

	if (not uploaded_file.filename) or (not uploaded_file.size):
		raise HTTPException(
			status.HTTP_406_NOT_ACCEPTABLE,
			"file is not uploaded or there was a problem uploading"
		)

	if not files_service.is_uploadable(
		uploaded_file.size,
		uploaded_file.filename,
		allowed_extentions
	):
		raise HTTPException(
			status.HTTP_406_NOT_ACCEPTABLE,
			f"file is not uploadable. "
			"check files sizes and extentions"
		)