from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from spm.database import service as database_service
from spm.units.consts import UNIT
from spm.users.models import (
	User
)
from spm.files import service as files_service
from spm.projects import service as projects_service
from spm.reffer import service as reffer_service
from .utils import (
	validate_form,
	parse_form,
	pop_form_inserts,
	pop_form_files,
	get_form_refferals,
	validate_file_input
)
from .models import (
	Form,
	FormMetaFunc,
	AllForms,
	ProjectsWithForm,
	FormInsert,
	FormInsetFileItem,
	FormInsertEnumItem,
	FormIn
)

forms:dict[UNIT, Form] = {}

def register_unit_form(unit:UNIT, form_func:FormMetaFunc):
	global forms
	form = form_func()
	validate_form(form)
	forms[unit] = form

def get_unit_form(unit:UNIT):
	return forms[unit]

def forms_hierarchy(user_id: int, session: Session) -> AllForms:
	"returns all forms from all users reffered projects and their units"
	refferals = reffer_service.users_refferals(user_id, session)

	return AllForms(
		forms={
			project_id: {
					unit:get_unit_form(unit) 
					for unit in units
			}
			for project_id, units in refferals.projects.items()
		}
	)

def get_projects_units_with_form(
	user_id:int,
	session: Session
) -> ProjectsWithForm:
	refferals = reffer_service.users_refferals(user_id, session)

	return ProjectsWithForm(
		projects={
			project_id: units
			for project_id, units in refferals.projects.items()
		}
	)

def get_project_units_with_form(
	user_id:int,
	project_id:int,
	session: Session
) -> list[UNIT]:
	refferals = reffer_service.users_refferaled_projects_units(
		user_id,
		project_id,
		session
	)

	return refferals.units

def submit_form(
	user: User,
	form_in: FormIn,
	session: Session
):
	# we can NOT submit a form when we dont have reffer on the project
	if not reffer_service.user_has_refferal_on_project(
		user.id,
		form_in.project_id,
		session
	):
		raise HTTPException(
			status.HTTP_406_NOT_ACCEPTABLE,
			"user does not have refferal on this project."
		)

	# sperating each type
	unit_form = get_unit_form(user.unit)
	# inserts are handelled by their own
	form_inserts = pop_form_inserts(form_in, unit_form)
	form_in = parse_form(form_in, unit_form, session)
	form_files = pop_form_files(form_in, unit_form)

	# uploading files
	file_properties: dict[str, int] = {}
	for item in form_files:
		form_item, uploaded_file = item
		validate_file_input(
			uploaded_file,
			form_item.file_extentions
		)
	
		stored_file = files_service.store_file(
			uploaded_file.filename or "",
			uploaded_file.file.read(),
			form_in.project_id,
			session
		)

		file_properties[form_item.project_property] = stored_file
	form_in.input.update(file_properties)

	# set properties
	projects_service.set_project_properties(
		form_in.project_id,
		form_in.input,
		session
	)

	# dealing with inserts
	submit_form_insert(
		form_inserts,
		form_in,
		session
	)

	# reffers
	reffers = get_form_refferals(form_in, unit_form)
	for reffer in reffers:
		reffer_service.refferal_user_to(
			user.id,
			reffer,
			form_in.project_id,
			session
		)
	reffer_service.remove_refferal_from(
		user.id,
		form_in.project_id,
		session
	)

def submit_form_insert(
	forms: list[tuple[FormInsert, dict]],
	form_in: FormIn,
	session: Session
):
	for form_input, value in forms:
		table = database_service.get_class_by_tablename(form_input.table_name)

		if not table:
			raise HTTPException(
				status.HTTP_500_INTERNAL_SERVER_ERROR,
				f"internal error: could not find table {form_input.table_name}"
			)

		for name, item in form_input.items.items():
			user_input = value[name]

			# uploading file
			if isinstance(item, FormInsetFileItem):
				validate_file_input(
					user_input,
					item.file_extentions
				)

				stored_file = files_service.store_file(
					user_input.filename,
					user_input.file.read(),
					form_in.project_id,
					session
				)

				form_in.input[name] = stored_file

			# handeling enum
			elif isinstance(item, FormInsertEnumItem):
				if not user_input:
					if not item.is_optional:
						raise HTTPException(
							status.HTTP_406_NOT_ACCEPTABLE,
							f"missing required field {name}"
						)
					else:
						continue

				enum_values = item.values
				if user_input not in map(lambda x: x[0], enum_values):
					raise HTTPException(
						status.HTTP_406_NOT_ACCEPTABLE,
						f"{form_input.title} can only accept "
					)

				form_in.input[name] = value

		# rest of type-checkings happened in submit_form()
		obj = table(
			**form_in.input,
			project_id=form_in.project_id,
			created_at=datetime.now()
		)

		session.add(obj)