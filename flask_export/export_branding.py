# -*- coding: utf-8 -*-

"""
Identidade visual compartilhada pelas exportações
Portal Wi-Fi TRUE - AMT Eusébio
"""

import os
from datetime import datetime
from zoneinfo import ZoneInfo

# ==========================================================
# CORES OFICIAIS
# ==========================================================

BRAND = {

    "green": "#03D199",

    "greenDark": "#047857",

    "greenSoft": "#ECFDF5",

    "yellow": "#FAFF64",

    "blue": "#0891B2",

    "ink": "#0F172A",

    "slate": "#64748B",

    "border": "#E2E8F0",

    "surface": "#F8FAFC",

    "white": "#FFFFFF"

}

# ==========================================================
# PALETA DOS GRÁFICOS
# ==========================================================

PALETA = [

    "#03D199",

    "#22D68B",

    "#C6F55E",

    "#0891B2",

    "#F59E0B",

    "#7C3AED",

    "#EF4444",

    "#0EA5E9"

]

# ==========================================================
# IDENTIFICAÇÃO DO SISTEMA
# ==========================================================

ORG = {

    "system": "Portal Wi-Fi TRUE",

    "org": "AMT Eusébio",

    "org_display": "AMT Eusébio — Autarquia Municipal de Trânsito",

    "subtitle": "Relatório Executivo",

    "footer": (
        "Documento gerado automaticamente pelo Portal Wi-Fi TRUE • "
        "AMT Eusébio • Uso interno"
    )

}

# ==========================================================
# FONTE PADRÃO EXCEL
# ==========================================================

FONT_XLSX = "Calibri"

# ==========================================================
# CAMINHO DA LOGO
# ==========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LOGO_PATH = os.path.join(
    BASE_DIR,
    "assets",
    "amt-logo.png"
)

# ==========================================================
# DATA / HORA
# ==========================================================

FORTALEZA = ZoneInfo("America/Fortaleza")


def now_fortaleza():

    return datetime.now(FORTALEZA).strftime(
        "%d/%m/%Y %H:%M:%S"
    )


def file_stamp():

    return datetime.now(FORTALEZA).strftime(
        "%Y%m%d_%H%M%S"
    )


def logo_path():

    if os.path.exists(LOGO_PATH):
        return LOGO_PATH

    return None


# ==========================================================
# CORES OPENPYXL
# ==========================================================

def argb(cor):

    return "FF" + cor.replace("#", "").upper()


def rgb_hex(cor):

    return cor.replace("#", "").upper()


# ==========================================================
# CORES REPORTLAB
# ==========================================================

def rgb(cor):

    cor = cor.replace("#", "")

    return (

        int(cor[0:2], 16) / 255,

        int(cor[2:4], 16) / 255,

        int(cor[4:6], 16) / 255

    )


# ==========================================================
# FORMATA NÚMEROS
# ==========================================================

def br_number(valor):

    try:

        return "{:,.0f}".format(

            float(valor)

        ).replace(",", ".")

    except Exception:

        return str(valor)