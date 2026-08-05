# -*- coding: utf-8 -*-

"""
Preparação dos dados para exportação.
Recebe listas de registros já carregadas do banco.
"""

from collections import Counter

from .export_branding import br_number


# ==========================================================
# COLUNAS DOS CADASTROS
# ==========================================================

COLUNAS_CADASTROS = [

    {"header": "ID", "key": "id", "width": 8},

    {"header": "Nome", "key": "nome", "width": 28},

    {"header": "CPF", "key": "cpf", "width": 18},

    {"header": "Telefone", "key": "telefone", "width": 18},

    {"header": "E-mail", "key": "email", "width": 30},

    {"header": "Sexo", "key": "sexo", "width": 12},

    {"header": "Nascimento", "key": "data_nascimento", "width": 16},

    {"header": "CEP", "key": "cep", "width": 12},

    {"header": "Rua", "key": "rua", "width": 28},

    {"header": "Número", "key": "numero", "width": 10},

    {"header": "Bairro", "key": "bairro", "width": 22},

    {"header": "Cidade", "key": "cidade", "width": 22},

    {"header": "Transporte", "key": "meio_transporte", "width": 18},

    {"header": "Dias/Semana", "key": "dias_utilizacao", "width": 15},

    {"header": "Cadastro", "key": "data_cadastro", "width": 22}

]


# ==========================================================
# COLUNAS DOS ACESSOS
# ==========================================================

COLUNAS_ACESSOS = [

    {"header": "ID", "key": "id", "width": 8},

    {"header": "CPF", "key": "cpf", "width": 18},

    {"header": "Nome", "key": "nome", "width": 28},

    {"header": "IP", "key": "ip", "width": 18},

    {"header": "Data/Hora", "key": "data_acesso", "width": 22},

    {"header": "Ônibus", "key": "onibus", "width": 15},

    {"header": "Linha", "key": "linha", "width": 15}

]


# ==========================================================
# NORMALIZAÇÃO
# ==========================================================

def _valor(registro, chave):

    if not isinstance(registro, dict):
        return ""

    for nome in (

        chave,

        chave.lower(),

        chave.upper(),

        chave.capitalize(),

        chave.title()

    ):

        if nome in registro and registro[nome] is not None:

            return registro[nome]

    return ""


def normalizar_cadastro(reg):

    return {

        coluna["key"]: _valor(reg, coluna["key"])

        for coluna in COLUNAS_CADASTROS

    }


def normalizar_acesso(reg):

    return {

        coluna["key"]: _valor(reg, coluna["key"])

        for coluna in COLUNAS_ACESSOS

    }


# ==========================================================
# CONTADORES
# ==========================================================

def _serie(lista, campo, limite=10):

    contador = Counter()

    for registro in lista:

        valor = str(

            registro.get(campo) or ""

        ).strip()

        if valor:

            contador[valor] += 1

    resultado = []

    for nome, total in contador.most_common(limite):

        resultado.append({

            "name": nome,

            "value": total

        })

    return resultado


# ==========================================================
# KPIs
# ==========================================================

def montar_kpis(cadastros, acessos):

    cidades = {

        c.get("cidade")

        for c in cadastros

        if c.get("cidade")

    }

    ceps = [

        c

        for c in cadastros

        if c.get("cep")

    ]

    return [

        {

            "label": "Cadastros",

            "value": br_number(len(cadastros))

        },

        {

            "label": "Acessos",

            "value": br_number(len(acessos))

        },

        {

            "label": "Cidades",

            "value": br_number(len(cidades))

        },

        {

            "label": "Com CEP",

            "value": br_number(len(ceps))

        }

    ]


# ==========================================================
# GRÁFICOS
# ==========================================================

def montar_graficos(cadastros):

    return [

        {

            "titulo": "Cadastros por Cidade",

            "dados": _serie(cadastros, "cidade"),

            "tipos": ["Barras", "Pizza"],

            "unidade": "cadastros",

            "minimo": 2

        },

        {

            "titulo": "Cadastros por Bairro",

            "dados": _serie(cadastros, "bairro"),

            "tipos": ["Barras", "Pizza"],

            "unidade": "cadastros",

            "minimo": 2

        },

        {

            "titulo": "Distribuição por Sexo",

            "dados": _serie(cadastros, "sexo"),

            "tipos": ["Pizza"],

            "unidade": "cadastros",

            "minimo": 2

        },

        {

            "titulo": "Meio de Transporte",

            "dados": _serie(cadastros, "meio_transporte"),

            "tipos": ["Barras", "Pizza"],

            "unidade": "cadastros",

            "minimo": 2

        }

    ]


# ==========================================================
# PREPARAÇÃO
# ==========================================================

def preparar(cadastros_raw, acessos_raw):

    cadastros = [

        normalizar_cadastro(x)

        for x in (cadastros_raw or [])

    ]

    acessos = [

        normalizar_acesso(x)

        for x in (acessos_raw or [])

    ]

    return (

        cadastros,

        acessos,

        montar_kpis(cadastros, acessos),

        montar_graficos(cadastros)

    )