import pandas as pd

class RecomendadorClimatico:
    def __init__(self, archivo_entrada, archivo_salida):
        self.archivo_entrada = archivo_entrada
        self.archivo_salida = archivo_salida
        self.df = None
        self.merged = None

    def cargar_datos(self):
        self.df = pd.read_csv(self.archivo_entrada)

    def transformar_datos(self):
        # Separar por parámetro
        lluvia = self.df[self.df["PARAMETER"] == "PRECTOTCORR"]
        temp_max = self.df[self.df["PARAMETER"] == "T2M_MAX"]
        temp_min = self.df[self.df["PARAMETER"] == "T2M_MIN"]
        humedad = self.df[self.df["PARAMETER"] == "RH2M"]

        meses = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", 
                 "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]

        # Convertir a formato largo
        lluvia_long = lluvia.melt(id_vars=["YEAR"], value_vars=meses, var_name="MONTH", value_name="lluvia_mm")
        temp_max_long = temp_max.melt(id_vars=["YEAR"], value_vars=meses, var_name="MONTH", value_name="temp_max")
        temp_min_long = temp_min.melt(id_vars=["YEAR"], value_vars=meses, var_name="MONTH", value_name="temp_min")
        humedad_long = humedad.melt(id_vars=["YEAR"], value_vars=meses, var_name="MONTH", value_name="humedad")

        # pH del suelo
        ph_cols = [col for col in self.df.columns if "PH_SUELO" in col]
        ph_df = lluvia[["YEAR"] + ph_cols].copy()  # usar fila de lluvia como base
        ph_long = ph_df.melt(id_vars=["YEAR"], var_name="MONTH", value_name="ph_suelo")
        ph_long["MONTH"] = ph_long["MONTH"].str.extract(r'(\w+)_PH_SUELO')

        # Unir todos
        self.merged = lluvia_long.merge(temp_max_long, on=["YEAR", "MONTH"])
        self.merged = self.merged.merge(temp_min_long, on=["YEAR", "MONTH"])
        self.merged = self.merged.merge(humedad_long, on=["YEAR", "MONTH"])
        self.merged = self.merged.merge(ph_long, on=["YEAR", "MONTH"])

    def generar_recomendacion(self, row):
        # Prioridad: riego > fertilización > poda preventiva > ninguna
        if row["lluvia_mm"] < 10 and row["temp_max"] > 30:
            return "riego"
        elif row["ph_suelo"] < 5.5:
            return "fertilización"
        elif row["humedad"] > 90 and row["temp_max"] > 28:
            return "poda preventiva"
        else:
            return "ninguna"

    def aplicar_recomendaciones(self):
        self.merged["Recomendación"] = self.merged.apply(self.generar_recomendacion, axis=1)

    def exportar_resultado(self):
        columnas_finales = ["YEAR", "MONTH", "lluvia_mm", "temp_max", "temp_min", "humedad", "ph_suelo", "Recomendación"]
        self.merged[columnas_finales].to_csv(self.archivo_salida, index=False)

    def procesar(self):
        self.cargar_datos()
        self.transformar_datos()
        self.aplicar_recomendaciones()
        self.exportar_resultado()
        print(f"✅ Archivo generado: {self.archivo_salida}")

# Uso de la clase:
# recomendador = RecomendadorClimatico("df_con_ph.csv", "datos_con_recomendaciones_completo.csv")
# recomendador.procesar()
