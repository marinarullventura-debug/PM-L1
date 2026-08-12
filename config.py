from pathlib import Path

# ============================================================
# GENERAL CONFIGURATION
# ============================================================

INTERNAL_CUSTOMER = "IDIADA Automotive Technology S.A."

QUALITY_EMAIL = "quality.chas@idiada.com"

DEPARTMENTS = [
    "ADAS_AT",
    "BRK_AT",
    "DUR_AT",
    "EE_AT",
    "VD_AT",
    "NVH_AT",
    "CHASSIS_DESIGN_AT"
]

SPECIAL_PM_DEPARTMENTS = { #Poner los nombres en mayúsculas
    "FRANCESC XAVIER MONTANE CLOS": "NVH_AT", 
    "JAVIER ITURBE CARMONA": "NVH_AT"
}

# ============================================================
# PATHS
# (Modificar únicamente estas rutas)
# ============================================================

DEFAULT_EMPLOYEE_FILE = r"J:\IDIADA\ES\HQ\QP01_Quality_Organization\Shared\9. PM Audits\2026\Level_1_PM_Audits\Ch,AS&Dur\lista_empleados_10082026.xlsx"

GLOBAL_HISTORY_FILE = Path(
    r"J:\IDIADA\ES\HQ\QP01_Quality_Organization\Shared\9. PM Audits\2026\Level_1_PM_Audits\Ch,AS&Dur\PM L1 Audit.xlsx"
)

DEPARTMENT_HISTORY = {

    "ADAS_AT": Path(
        r'J:\IDIADA\ES\HQ\KP02A_ADAS\Internal\Quality\1. Quality Internal Audits\2026\2026 PML1 ADAS.xlsx'
    ),

    "BRK_AT": Path(
        r'J:\IDIADA\ES\HQ\KP02C_BRK\BRK\Confi\01_Gen_Man\01 Dept\04_Quality\1. Quality Internal Audits\2026\2026 PML1 BRK.xlsx'
    ),

    "DUR_AT": Path(
        r'J:\IDIADA\ES\HQ\KP02D_Durability\Confidential\KP02D-04_Administration\3_Quality\2.-Quality targets\11.- PM audits\2026\2026 PML1 DUR.xlsx'
    ),

    "EE_AT": Path(
        r'J:\IDIADA\ES\HQ\KP02E_Electronics\Internal\QUALITY\Electronics dept. Systems\1. Audits\1. Quality Internal Audits\2026\2026 PML1 ELN.xlsx'
    ),

    "NVH_AT": Path(
        r'J:\IDIADA\ES\HQ\KP02G_NVH\Internal\0. Quality\1. Quality Internal Audits\2026\2026 PML1 NVH.xlsx'
    ),

    "VD_AT": Path(
        r'J:\IDIADA\ES\HQ\KP02I_Dyn\Internal\0. Quality\1. Quality Internal Audits\2026\2026 PML1 VDYN.xlsx'
    ),

    "CHASSIS_DESIGN_AT": Path(
        r'J:\IDIADA\ES\HQ\KP02K_Chassis_Design\Internal\8. Quality\1. Quality Internal Audits\2026\2026 PML1 CHD.xlsx'
    )

}

# ============================================================
# EMAIL SETTINGS
# ============================================================

DEFAULT_CC = {

    "ADAS_AT": [
        "Paula García Alzuria",
        "David Graells Somoano",
        "Joan Costa Martinez",
        "Jordi Bargallo Rafecas"
    ],

    "BRK_AT": [
        "Juan Pablo Barles Arizon",
        "Oscar Durro Gonzalvez",
        "Jeremie Clement",
        "Fabio Squadrani"
    ],

    "DUR_AT": [
        "Xavier Larroy Puig",
        "Arturo Solsona Guerrero",
        "Anna Marín Saltó"
    ],

    "EE_AT": [
        "Lorena Garcia-Sol Garcia",
        "Judit Delgado Morata"
    ],

    "VD_AT": [
        "Soledad Torreblanca García"
    ],

    "NVH_AT": [
        "Soledad Torreblanca García"
    ],

    "CHASSIS_DESIGN_AT": [
        "Soledad Torreblanca García"
    ]

}

# ============================================================
# SHEET FORMAT
# ============================================================

MONTHS = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]

# ============================================================
# INCIDENT RULES
# ============================================================

RED_RULES = {

    "PO_CONSUMED": True,

    "NO_PM_HOURS": True,

    "NO_HOURS_LAST_3M": True,

    "DELAYED": True

}
