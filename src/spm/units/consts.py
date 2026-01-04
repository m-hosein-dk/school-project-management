from enum import Enum

class UNIT(Enum):
	SYSTEM_ADMINISTRATOR = "system_administrator" # واحد فناوری اطلاعات ( مدیرسیستم)			
	SURVEYING = "surveying" # نقشه کشی
	CONTRACTS = "contracts" # امور قراردادها و اعتبارات
	TECHNICAl_ASSISSTANT = "technical_assisstant" # معاونت فنی
	TECHNICAl_OFFICE = "technical_office" # دفتر فنی
	PUBLIC_PARTICIPATION = "public_participation" # مشارکت مردمی
	BUILDING_SUPERVISOR = "building_supervisor" # واحد سرناظر ابنیه
	BUILDING_SUPERVISION = "building_supervision" # واحد نظارت ابنیه
	FACILITIES_SUPERVISOR = "facilities_supervisor" # واحد سرناظر تاسیسات
	FACILITY_MONITORING = "facility_monitoring" # واحد نظارت تاسیسات
	FINANCIAL_PERFORMANCE = "financial_performance" # گزارش عمکرد مالی

language_mapping = {
	UNIT.SYSTEM_ADMINISTRATOR: {
		"en": "System Administrator",
		"fa": "واحد فناوری اطلاعات ( مدیرسیستم)"
	},

	UNIT.SURVEYING: {
		"en": "Surveying",
		"fa": "نقشه کشی"
	},

	UNIT.CONTRACTS: {
		"en": "Contracts",
		"fa": "امور قراردادها و اعتبارات",
	},

	UNIT.TECHNICAl_ASSISSTANT: {
		"en": "Technical Assisstant",
		"fa": "معاونت فنی"
	},

	UNIT.TECHNICAl_OFFICE: {
		"en": "Technical Office",
		"fa": "دفتر فنی"
	},

	UNIT.PUBLIC_PARTICIPATION: {
		"en": "Public Participation",
		"fa": "واحد مشارکت مردمی"
	},

	UNIT.BUILDING_SUPERVISOR: {
		"en": "Building Supervisor",
		"fa": "واحد سرناظر ابنیه"
	},

	UNIT.BUILDING_SUPERVISION: {
		"en": "Building Supervision",
		"fa": "واحد نظارت ابنیه"
	},

	UNIT.FACILITIES_SUPERVISOR: {
		"en": "Facilities Supervisor",
		"fa": "واحد سرناظر تاسیسات"
	},

	UNIT.FACILITY_MONITORING: {
		"en": "Facility Monitoring",
		"fa": "واحد نظارت تاسیسات"
	},

	UNIT.FINANCIAL_PERFORMANCE: {
		"en": "Financial Performance",
		"fa": "گزارش عمکرد مالی"
	},
}