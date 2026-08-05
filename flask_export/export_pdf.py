# -*- coding: utf-8 -*-

"""
Relatório Executivo em PDF
Portal Wi-Fi TRUE
"""

from io import BytesIO

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

from .export_branding import (

    BRAND,

    ORG,

    PALETA,

    rgb,

    logo_path,

    now_fortaleza,

    br_number

)

MARGEM = 12 * mm

HEADER = 34 * mm


class PDFRelatorio:

    def __init__(

        self,

        titulo,

        usuario,

    ):

        self.buffer = BytesIO()

        self.canvas = canvas.Canvas(

            self.buffer,

            pagesize=landscape(A4)

        )

        self.W, self.H = landscape(A4)

        self.titulo = titulo

        self.usuario = usuario

        self.logo = logo_path()

        self.pagina = 0

        self.data = now_fortaleza()

    # =====================================================

    def cor(self, hex):

        self.canvas.setFillColorRGB(

            *rgb(hex)

        )

    def texto(

        self,

        x,

        y,

        texto,

        tamanho,

        bold=False,

        cor=BRAND["ink"]

    ):

        self.cor(cor)

        self.canvas.setFont(

            "Helvetica-Bold" if bold else "Helvetica",

            tamanho

        )

        self.canvas.drawString(

            x,

            self.H - y,

            str(texto)

        )

    def caixa(

        self,

        x,

        y,

        w,

        h,

        cor

    ):

        self.cor(cor)

        self.canvas.rect(

            x,

            self.H - y - h,

            w,

            h,

            fill=1,

            stroke=0

        )

    # =====================================================

    def cabecalho(self):

        self.caixa(

            0,

            0,

            self.W,

            HEADER,

            BRAND["ink"]

        )

        self.caixa(

            0,

            HEADER,

            self.W,

            2 * mm,

            BRAND["green"]

        )

        self.caixa(

            0,

            HEADER + 2 * mm,

            self.W * .30,

            2 * mm,

            BRAND["yellow"]

        )

        if self.logo:

            try:

                self.canvas.drawImage(

                    self.logo,

                    MARGEM,

                    self.H - 28 * mm,

                    width=22 * mm,

                    height=22 * mm,

                    mask="auto"

                )

            except Exception:

                pass

        self.texto(

            40 * mm,

            12 * mm,

            "PORTAL WI-FI TRUE",

            16,

            True,

            BRAND["white"]

        )

        self.texto(

            40 * mm,

            18 * mm,

            ORG["org_display"],

            9,

            False,

            BRAND["greenSoft"]

        )

        self.texto(

            40 * mm,

            24 * mm,

            self.titulo,

            9,

            False,

            BRAND["greenSoft"]

        )

        self.texto(

            self.W - 90 * mm,

            12 * mm,

            self.data,

            8,

            False,

            BRAND["white"]

        )

        self.texto(

            self.W - 90 * mm,

            18 * mm,

            self.usuario,

            8,

            False,

            BRAND["greenSoft"]

        )

    # =====================================================

    def rodape(self):

        self.texto(

            MARGEM,

            self.H - 8 * mm,

            ORG["footer"],

            7,

            False,

            BRAND["slate"]

        )

        self.texto(

            self.W - 45 * mm,

            self.H - 8 * mm,

            f"Página {self.pagina}",

            7,

            False,

            BRAND["slate"]

        )

    # =====================================================

    def nova_pagina(self):

        if self.pagina:

            self.canvas.showPage()

        self.pagina += 1

        self.cabecalho()

        self.rodape()

        return HEADER + 12 * mm
    # =====================================================
    # DASHBOARD
    # =====================================================

    def dashboard(
        self,
        kpis,
        graficos,
    ):

        y = self.nova_pagina()

        self.texto(
            MARGEM,
            y,
            "Dashboard Executivo",
            12,
            True
        )

        y += 10 * mm

        largura_card = 62 * mm
        altura_card = 22 * mm
        espaco = 6 * mm

        for indice, kpi in enumerate(kpis):

            coluna = indice % 4
            linha = indice // 4

            x = MARGEM + coluna * (largura_card + espaco)
            yy = y + linha * (altura_card + espaco)

            self.caixa(
                x,
                yy,
                largura_card,
                altura_card,
                BRAND["greenSoft"]
            )

            self.texto(
                x + 4 * mm,
                yy + 7 * mm,
                str(kpi["label"]).upper(),
                7,
                True,
                BRAND["slate"]
            )

            self.texto(
                x + 4 * mm,
                yy + 16 * mm,
                kpi["value"],
                16,
                True,
                BRAND["ink"]
            )

        y += 35 * mm

        # ============================================
        # GRÁFICOS
        # ============================================

        for grafico in graficos or []:

            itens = sorted(

                grafico["dados"],

                key=lambda x: x["value"],

                reverse=True

            )[:8]

            if len(itens) < grafico.get(
                "minimo",
                2
            ):

                continue

            if y > self.H - 70 * mm:

                y = self.nova_pagina()

            self.texto(

                MARGEM,

                y,

                grafico["titulo"],

                10,

                True

            )

            y += 8 * mm

            maior = max(

                item["value"]

                for item in itens

            )

            total = sum(

                item["value"]

                for item in itens

            )

            for indice, item in enumerate(itens):

                self.texto(

                    MARGEM,

                    y,

                    item["name"],

                    8

                )

                largura = (

                    item["value"]

                    / maior

                ) * 90 * mm

                self.caixa(

                    85 * mm,

                    y - 2,

                    largura,

                    4 * mm,

                    PALETA[
                        indice % len(PALETA)
                    ]

                )

                percentual = (

                    item["value"]

                    / total

                ) * 100

                self.texto(

                    185 * mm,

                    y,

                    f"{br_number(item['value'])} ({percentual:.1f}%)",

                    8,

                    True

                )

                y += 7 * mm

            y += 8 * mm
    # =====================================================
    # TABELA
    # =====================================================

    def tabela(
        self,
        titulo,
        head,
        body,
    ):

        y = self.nova_pagina()

        self.texto(
            MARGEM,
            y,
            titulo,
            11,
            True
        )

        y += 10 * mm

        largura = (self.W - (2 * MARGEM)) / len(head)

        # Cabeçalho
        for i, coluna in enumerate(head):

            x = MARGEM + i * largura

            self.caixa(
                x,
                y,
                largura,
                8 * mm,
                BRAND["greenDark"]
            )

            self.texto(
                x + 2,
                y + 5,
                coluna,
                8,
                True,
                BRAND["white"]
            )

        y += 8 * mm

        # Dados
        for indice, linha in enumerate(body):

            if y > self.H - 25 * mm:

                y = self.nova_pagina()

            if indice % 2 == 0:

                self.caixa(
                    MARGEM,
                    y,
                    self.W - (2 * MARGEM),
                    7 * mm,
                    BRAND["surface"]
                )

            for coluna, valor in enumerate(linha):

                x = MARGEM + coluna * largura

                self.texto(
                    x + 2,
                    y + 5,
                    valor if valor not in (None, "") else "-",
                    7
                )

            y += 7 * mm

    # =====================================================
    # FINALIZA
    # =====================================================

    def finalizar(self):

        self.canvas.save()

        self.buffer.seek(0)

        return self.buffer


# ==========================================================
# EXPORTAÇÃO
# ==========================================================

def backup_pdf(
    meta,
    kpis,
    head,
    body,
    graficos=None,
    secoes=None,
):

    pdf = PDFRelatorio(

        meta.get(
            "titulo",
            "Relatório Executivo"
        ),

        meta.get(
            "usuario",
            "Administrador"
        )

    )

    pdf.dashboard(

        kpis,

        graficos or []

    )

    pdf.tabela(

        meta.get(
            "titulo",
            "Relatório"
        ),

        head,

        body

    )

    for secao in secoes or []:

        pdf.tabela(

            secao["titulo"],

            secao["head"],

            secao["body"]

        )

    return pdf.finalizar()