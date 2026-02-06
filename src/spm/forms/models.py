from typing import Callable, Literal, Mapping, Any, Type
from pydantic import BaseModel
from spm.units.consts import UNIT

# service models
class FormProjectProperty(BaseModel):
    input_type:str = "project_property"
    title: str
    project_property: str
    type: Literal[
        "string", "text", 
        "integer", "float",
        "date", "datetime",
    ]
    description: str | None = None
    is_optional: bool = False

class FormProjectPropertyEnum(BaseModel):
    input_type:str = "project_property_enum"
    title: str
    project_property: str
    values: list[tuple[int | str, str]] # value and its farsi mapping
    description: str | None = None
    is_optional: bool = False

class FormProjectPropertyFile(BaseModel):
    input_type:str = "project_property_file"
    title: str
    description:str = ""
    project_property:str
    file_extentions: Literal["*"] | list[str] = "*"
    is_optional: bool = False

class FormReffer(BaseModel):
    input_type:str = "reffer"
    unit: UNIT

class FormInsertItem(BaseModel):
    input_type:str = "insert_item"
    title: str
    description:str = ""
    property:str
    type: Literal[
        "string", "text",
        "integer", "float",
        "date", "datetime",
    ]
    is_optional: bool = False

class FormInsetFileItem(BaseModel):
    input_type:str = "insert_file_item"
    title: str
    description:str = ""
    property:str
    file_extentions: Literal["*"] | list[str]
    is_optional: bool = False

class FormInsertEnumItem(BaseModel):
    input_type:str = "insert_enum_item"
    title: str
    description:str = ""
    property:str
    values: list[tuple[int | str, str]] # value and its farsi mapping
    is_optional: bool = False

class FormInsert(BaseModel):
    input_type:str = "insert"
    title: str
    table_name: str
    description:str = ""
    items:dict[str, FormInsertItem | FormInsertEnumItem | FormInsetFileItem]
    is_optional: bool = False

    min:int = 0
    max:int = 1000

type FormInputs = (
    FormProjectProperty | FormReffer | FormProjectPropertyFile | 
    FormProjectPropertyEnum | FormInsert
)

type Form = Mapping[
    str,
    FormInputs
]

type FormMetaFunc = Callable[
    [],
    Form
]

# API models
class AllForms(BaseModel):
    forms: dict[
        int, # project id
        dict[UNIT, Form]
    ]

class ProjectsWithForm(BaseModel):
    projects: dict[
        int,
        list[UNIT]
    ]

class FormIn(BaseModel):
    project_id: int
    input: dict[str, Any]