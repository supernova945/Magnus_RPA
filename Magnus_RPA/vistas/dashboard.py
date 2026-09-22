import sys
import os
import json
from datetime import datetime

from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QFrame, QLabel)
from PySide6.QtCharts import (QChart, QChartView, QPieSeries, QBarSeries,
                              QBarSet, QBarCategoryAxis, QValueAxis)
from PySide6.QtGui import QPainter, QFont, QColor, QPen
from PySide6.QtCore import Qt

# Constant for ROI calculation (Estimated time a human takes per record in seconds)
# 2 minutes = 120 seconds
MANUAL_TIME_PER_RECORD = 120 

def cargar_resumen():
    """Carga el resumen acumulado de logs/ o devuelve estructura vacía."""
    # Buscar el archivo desde el directorio del proyecto (un nivel arriba de vistas/)
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ruta = os.path.join(base, "logs", "resumen_acumulado.json")
    if os.path.exists(ruta):
        try:
            with open(ruta, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    # Si no existe, devuelve datos vacíos
    return {
        "total":    {"exitosos": 0, "errores": 0, "omitidos": 0, "monto": 0.0},
        "por_metodo": {},
        "por_sociedad": {
            "GT03": {"exitosos": 0, "errores": 0, "omitidos": 0},
            "GT09": {"exitosos": 0, "errores": 0, "omitidos": 0},
            "SV17": {"exitosos": 0, "errores": 0, "omitidos": 0}
        },
        "por_fecha": [],
        "errores_frecuentes": {},
        "ultima_actualizacion": "Sin ejecuciones registradas aún"
    }

# =====================================================================
# CLASE PRINCIPAL DEL DASHBOARD
# =====================================================================
class DemoDashboardFull(QMainWindow):
    def __init__(self):
        super().__init__()
        self.data = cargar_resumen()

        self.setWindowTitle("Dashboard Magnus RPA — Analítica")
        self.resize(1280, 820)
        self.setStyleSheet("background-color: #0D1117; color: white;")

        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(20, 15, 20, 15)
        root.setSpacing(12)

        # Extraer datos base
        total    = self.data.get("total", {})
        exitosos = total.get("exitosos", 0)
        errores  = total.get("errores",  0)
        omitidos = total.get("omitidos", 0)
        monto    = total.get("monto",    0.0)
        total_reg = exitosos + errores + omitidos
        tasa_exito = f"{exitosos / total_reg * 100:.1f}%" if total_reg > 0 else "N/A"
        ult_act = self.data.get("ultima_actualizacion", "—")

        # --- Encabezado: última actualización ---
        lbl_header = QLabel(f"Última actualización: {ult_act}")
        lbl_header.setFont(QFont("72", 8))
        lbl_header.setStyleSheet("color: #3A5080;")
        lbl_header.setAlignment(Qt.AlignRight)
        root.addWidget(lbl_header)

        # ─── FILA 1A: KPIs Financieros ────────────────────────────────
        # Métricas de tiempo
        num_ejec     = total.get("num_ejecuciones", 0)
        dur_total_s  = total.get("duracion_total_s", 0.0)
        dur_prom_s   = dur_total_s / num_ejec if num_ejec > 0 else 0.0
        dur_prom_str = f"{int(dur_prom_s // 60)}m {int(dur_prom_s % 60)}s" if dur_prom_s > 0 else "N/A"
        reg_por_min  = round(exitosos / (dur_total_s / 60), 1) if dur_total_s > 0 else 0.0
        rpm_str      = f"{reg_por_min} reg/min" if reg_por_min > 0 else "N/A"

        # Cálculo de ROI (Tiempo Ahorrado)
        tiempo_humano_s = total_reg * MANUAL_TIME_PER_RECORD
        ahorro_s = tiempo_humano_s - dur_total_s
        horas_ahorradas = max(0, ahorro_s / 3600)
        ahorro_str = f"{horas_ahorradas:.1f} h"

        row_kpi1 = QHBoxLayout()
        row_kpi1.setSpacing(12)
        row_kpi1.addWidget(self._tarjeta("💰 Importe Operado", f"$. {monto:,.2f}", "#161B27", "#1877F2"))
        row_kpi1.addWidget(self._tarjeta("✅ Exitosos",         f"{exitosos:,}",    "#161B27", "#00CC6A"))
        row_kpi1.addWidget(self._tarjeta("⚠️ Omitidos",        f"{omitidos:,}",    "#161B27", "#e3b341"))
        row_kpi1.addWidget(self._tarjeta("❌ Errores",          f"{errores:,}",     "#161B27", "#f85149"))
        root.addLayout(row_kpi1)

        # ─── FILA 1B: KPIs de Rendimiento / ROI ────────────────────
        row_kpi2 = QHBoxLayout()
        row_kpi2.setSpacing(12)
        row_kpi2.addWidget(self._tarjeta("🎯 Tasa de Éxito",   tasa_exito,         "#161B27", "#1877F2"))
        row_kpi2.addWidget(self._tarjeta("⏳ Tiempo Ahorrado", ahorro_str,         "#161B27", "#00CC6A"))
        row_kpi2.addWidget(self._tarjeta("⏱️ Duración Promedio", dur_prom_str,     "#161B27", "#1877F2"))
        row_kpi2.addWidget(self._tarjeta("⚡ Velocidad RPA",    rpm_str,            "#161B27", "#1877F2"))
        root.addLayout(row_kpi2)

        # ─── FILA 2: Pastel estado | Pastel método | Barras sociedad ───
        row_mid = QHBoxLayout()
        row_mid.setSpacing(12)

        # Pastel: Distribución general
        row_mid.addWidget(self._wrap(self._pastel(
            "Distribución de Estados",
            [("Éxito",   exitosos, "#00CC6A"),
             ("Error",   errores,  "#f85149"),
             ("Omitido", omitidos, "#e3b341")],
            explotar="Éxito"
        )))

        # Barras: Análisis de Errores Frecuentes
        row_mid.addWidget(self._wrap(self._barras_errores()))

        # Barras: resultados por sociedad
        ps = self.data.get("por_sociedad", {})
        row_mid.addWidget(self._wrap(self._barras_sociedad(ps)))

        root.addLayout(row_mid)

        # ─── FILA 3: Tendencia de monto por fecha ──────────────────────
        pf = self.data.get("por_fecha", [])
        row_bot = QHBoxLayout()
        row_bot.setSpacing(12)
        row_bot.addWidget(self._wrap(self._tendencia(pf)), stretch=2)
        row_bot.addWidget(self._wrap(self._duracion_por_fecha(pf)), stretch=1)
        root.addLayout(row_bot)

        # Pesos de filas (índices: 0=header, 1=kpi1, 2=kpi2, 3=mid, 4=bot)
        root.setStretch(1, 1)  # KPIs financieros — altura compacta
        root.setStretch(2, 1)  # KPIs rendimiento — altura compacta
        root.setStretch(3, 3)  # Gráficas medias
        root.setStretch(4, 3)  # Gráficas inferiores

    # ─── HELPERS DE UI ────────────────────────────────────────────────

    def _tarjeta(self, titulo, valor, bg, borde):
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {bg};
                border-radius: 8px;
                border-left: 4px solid {borde};
            }}
        """)
        lay = QVBoxLayout(card)
        lay.setContentsMargins(14, 10, 14, 10)

        lt = QLabel(titulo)
        lt.setFont(QFont("72", 10, QFont.Bold))
        lt.setStyleSheet("color: #A8B8D8; border: none;")
        lt.setWordWrap(True)

        lv = QLabel(valor)
        lv.setFont(QFont("72", 16, QFont.Bold))
        lv.setStyleSheet("color: white; border: none;")

        lay.addWidget(lt)
        lay.addWidget(lv)
        return card

    def _wrap(self, chart, altura=None):
        """Envuelve un QChart en un contenedor estilizado."""
        view = QChartView(chart)
        view.setRenderHint(QPainter.Antialiasing)
        view.setStyleSheet("background-color: transparent;")

        frame = QFrame()
        frame.setStyleSheet("background-color: #0d1117; border-radius: 8px;")
        if altura:
            frame.setMinimumHeight(altura)
        lay = QVBoxLayout(frame)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(view)
        return frame

    def _chart_base(self, titulo):
        """Crea un QChart con la línea visual Magnus."""
        c = QChart()
        c.setTitle(titulo)
        c.setAnimationOptions(QChart.SeriesAnimations)
        c.setBackgroundBrush(QColor("#0d1117"))
        c.setBackgroundPen(QPen(Qt.NoPen))
        c.setTitleFont(QFont("72", 11, QFont.Bold))
        c.setTitleBrush(QColor("#1877F2"))
        c.legend().setLabelBrush(QColor("#A8B8D8"))
        c.layout().setContentsMargins(8, 12, 8, 12)
        return c

    def _pastel(self, titulo, datos, explotar=None):
        series = QPieSeries()
        total = sum(max(v, 0) for _, v, _ in datos)
        for etiqueta, valor, color in datos:
            pct = f" ({valor / total * 100:.0f}%)" if total > 0 else ""
            s = series.append(f"{etiqueta}{pct}", max(valor, 0))
            s.setBrush(QColor(color))
            s.setPen(QPen(Qt.NoPen))
            if explotar and explotar in etiqueta and valor > 0:
                s.setExploded(True)
        c = self._chart_base(titulo)
        c.addSeries(series)
        c.legend().setAlignment(Qt.AlignBottom)
        return c

    def _barras_sociedad(self, ps):
        orden_base = ["GT03", "GT09", "SV17"]
        sociedades = [s for s in orden_base if s in ps]
        sociedades.extend(sorted(s for s in ps.keys() if s not in orden_base))
        if not sociedades:
            sociedades = orden_base

        def _set(nombre, clave, color):
            b = QBarSet(nombre)
            b.setColor(QColor(color))
            b.setPen(QPen(Qt.NoPen))
            b.append([ps.get(s, {}).get(clave, 0) for s in sociedades])
            return b

        series = QBarSeries()
        series.append(_set("Exitosos", "exitosos", "#00CC6A"))
        series.append(_set("Errores",  "errores",  "#f85149"))
        series.append(_set("Omitidos", "omitidos", "#e3b341"))

        c = self._chart_base("Resultados por Sociedad")
        c.addSeries(series)
        c.legend().setAlignment(Qt.AlignTop)

        axX = QBarCategoryAxis()
        axX.append(sociedades)
        axX.setLabelsBrush(QColor("#A8B8D8"))
        c.addAxis(axX, Qt.AlignBottom)
        series.attachAxis(axX)

        axY = QValueAxis()
        axY.setLabelsBrush(QColor("#A8B8D8"))
        axY.setGridLinePen(QPen(QColor("#232B3E"), 1))
        c.addAxis(axY, Qt.AlignLeft)
        series.attachAxis(axY)
        return c

    def _barras_errores(self):
        """Muestra los 3 errores más frecuentes encontrados en los logs."""
        errs = self.data.get("errores_frecuentes", {})
        # Ordenar por valor descendente y tomar los 3 primeros
        sorted_errs = sorted(errs.items(), key=lambda x: x[1], reverse=True)[:3]
        
        if not sorted_errs:
            # Crear gráfico vacío para evitar errores
            c = self._chart_base("Top 3 Errores Frecuentes")
            return c

        labels = [e[0] if len(e[0]) < 20 else e[0][:17]+"..." for e in sorted_errs]
        valores = [e[1] for e in sorted_errs]

        set_err = QBarSet("Frecuencia")
        set_err.setColor(QColor("#f85149"))
        set_err.setPen(QPen(Qt.NoPen))
        set_err.append(valores)

        series = QBarSeries()
        series.append(set_err)

        c = self._chart_base("Top 3 Errores Frecuentes")
        c.addSeries(series)
        c.legend().setVisible(False)

        axX = QBarCategoryAxis()
        axX.append(labels)
        axX.setLabelsBrush(QColor("#A8B8D8"))
        c.addAxis(axX, Qt.AlignBottom)
        series.attachAxis(axX)

        axY = QValueAxis()
        axY.setLabelsBrush(QColor("#A8B8D8"))
        axY.setGridLinePen(QPen(QColor("#232B3E"), 1))
        c.addAxis(axY, Qt.AlignLeft)
        series.attachAxis(axY)
        return c

    def _tendencia(self, por_fecha):
        """Gráfica de barras: monto operado por fecha (últimos 15 días)."""
        datos  = por_fecha[-15:]
        fechas = [d.get("fecha", "") for d in datos]
        montos = [round(d.get("monto", 0.0), 2) for d in datos]

        set_m = QBarSet("Monto (Q.)")
        set_m.setColor(QColor("#1877F2"))
        set_m.setPen(QPen(Qt.NoPen))
        set_m.append(montos if montos else [0])

        set_e = QBarSet("Exitosos")
        set_e.setColor(QColor("#00CC6A"))
        set_e.setPen(QPen(Qt.NoPen))
        set_e.append([d.get("exitosos", 0) for d in datos] or [0])

        # Solo monto en la serie principal para no saturar el eje
        series = QBarSeries()
        series.append(set_m)

        c = self._chart_base("Monto Operado por Fecha (últimos 30 días)")
        c.addSeries(series)
        c.legend().setAlignment(Qt.AlignTop)

        axX = QBarCategoryAxis()
        axX.append(fechas if fechas else ["Sin datos"])
        axX.setLabelsBrush(QColor("#A8B8D8"))
        c.addAxis(axX, Qt.AlignBottom)
        series.attachAxis(axX)

        axY = QValueAxis()
        axY.setLabelsBrush(QColor("#A8B8D8"))
        axY.setGridLinePen(QPen(QColor("#232B3E"), 1))
        c.addAxis(axY, Qt.AlignLeft)
        series.attachAxis(axY)
        return c

    def _duracion_por_fecha(self, por_fecha):
        """Gráfica de barras: duración de ejecuciones en minutos por fecha."""
        datos  = por_fecha[-15:]
        fechas = [d.get("fecha", "") for d in datos]
        # Convertir segundos a minutos para mejor legibilidad
        minutos = [round(d.get("duracion_s", 0.0) / 60, 1) for d in datos]

        set_d = QBarSet("Duración (min)")
        set_d.setColor(QColor("#4FA3F7"))
        set_d.setPen(QPen(Qt.NoPen))
        set_d.append(minutos if any(m > 0 for m in minutos) else [0])

        series = QBarSeries()
        series.append(set_d)

        c = self._chart_base("Tiempo de Ejecución por Fecha (min)")
        c.addSeries(series)
        c.legend().setAlignment(Qt.AlignTop)

        axX = QBarCategoryAxis()
        axX.append(fechas if fechas else ["Sin datos"])
        axX.setLabelsBrush(QColor("#A8B8D8"))
        c.addAxis(axX, Qt.AlignBottom)
        series.attachAxis(axX)

        axY = QValueAxis()
        axY.setLabelsBrush(QColor("#A8B8D8"))
        axY.setGridLinePen(QPen(QColor("#232B3E"), 1))
        c.addAxis(axY, Qt.AlignLeft)
        series.attachAxis(axY)
        return c


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = DemoDashboardFull()
    w.show()
    sys.exit(app.exec())
