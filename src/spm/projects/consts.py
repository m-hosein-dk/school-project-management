from enum import Enum

class PROJECT_STATUS(str, Enum):
    IN_DESTRUCTION = "in_construction"
    COMPLETED = "completed"

class PROJECT_TYPE(str, Enum):
    NEW = "new"
    RECONSTRUCTION = "reconstruction"
    COMPLETION = "completion"

class PROJECT_LOCATION_TYPE(str, Enum):
    NEW = "new"
    OLD = "old"

class PROJECT_LOCATION_SETTLEMENT(str, Enum):
    URBAN = "urban"
    RURAL = "rural"

class CONTRACT_ASSIGNMENT_TYPE(str, Enum):
    TENDER = "tender"
    FORMALITIES_WAIVER = "formalities_waiver"
    PRICE_INQUIRY = "price_inquiry"

class CONTRACT_SOURCE_OF_FINANCING(str, Enum):
    PROVINCIAL = "provincial"
    NATIONAL = "national"
    POPULAR = "popular"
    PARTICIPATORY = "participatory"
    OTHER = "other"


class PRAYER_ROOM_FLOOR(str, Enum):
    BASEMENT = "basement"
    GROUND = "ground"
    FIRST = "first"
    SECOND = "second"
    THIRD = "third"
    NOT_PRESENT = "not_present"