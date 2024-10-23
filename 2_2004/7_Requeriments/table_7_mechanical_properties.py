"""
DATOS DE LA BASE DE DATOS acero_estructural.db, TABLA EN_10025_2_2004

DATOS CORRESPONDIENTES A

EN 10025-2:2004

HOT ROLLED PRODUCTS OF STRUCTURAL STEELS

PART 2: TECHNICAL DELIVERY CONDITIONS FOR NON-ALLOY STRUCTURAL STEELS

TABLE 7 - MECHANICAL PROPERTIES AT AMBIENT TEMPERATURE FOR FLAT AND LONG PRODUCTS OF STEEL GRADES AND QUALITIES WITH
VALUES FOR THE IMPACT STRENGTH

22/10/2024

__author__ = Pedro Biel

__version__ = 0.0.0

__email__ = pedro.biel@abalsirengineering.com
"""

import pandas as pd
from src.utils.paths import Paths
from src.utils.sqlitepandasdf import SQLitePandasDF


class DatosEN10025_2:
    def __init__(self, acero: str, t: float) -> None:
        """
        Clase que gestiona los datos de la tabla 'EN_10025_2_2004' de la base de datos 'acero_estructural.db'.
        Proporciona valores del límite elástico (R.eH) y resistencia última a tracción (R.m) para acero estructural
        laminado en caliente grados S235 a S500.

        :param acero: Grado del acero: S 235, S 275, S 355, S420, S450, S460
        :param t: Espesor nominal del acero en mm.
        """
        self.acero = acero
        self.t = t

        # Ruta a la base de datos de acero estructural
        self.ruta_datos = f'{Paths.data}\\'
        self.acero_estructural_db = 'acero_estructural.db'
        self.tabla = 'EN_10025_2_2004'

        # Clase para gestionar la conexión a SQLite
        self.sql_pd = SQLitePandasDF

        # Cache para almacenar el DataFrame y evitar múltiples lecturas
        self._df_cache = None

    def _load_dataframe(self) -> pd.DataFrame:
        """
        Carga el DataFrame desde la base de datos SQLite y lo cachea para evitar múltiples accesos.

        :return: DataFrame con los datos de la tabla.
        """
        if self._df_cache is None:  # Solo carga el DataFrame si no está en cache
            sql_pd = self.sql_pd(f'{self.ruta_datos}{self.acero_estructural_db}', self.tabla)
            self._df_cache = sql_pd.sql_to_df()
        return self._df_cache

    def calidades(self) -> list[str]:
        """
        Obtiene la lista de calidades de acero disponibles.

        :return: Lista de calidades de acero (columna 'Calidad').
        """
        df = self._load_dataframe()
        return df['Calidad'].unique().tolist()

    def calidades_simbolo_principal(self) -> list[str]:
        """
        Obtiene la lista de calidades de acero disponibles.

        La denominación de la calidad contiene únicamente el símbolo principal según EN 10027-1:2005, tabla 1. Esto es,
        p.e. de la denominación 'S 235 JR' se obtiene 'S 235'.

        :return: Lista de calidades de acero (columna 'Calidad').
        """
        df = self._load_dataframe()
        return [calidad[:5] for calidad in df['Calidad'].unique().tolist()]

    def _obtener_t_max(self) -> int:
        """
        Determina el valor de t_max basado en el espesor nominal t.

        :return: t_max (16, 40, 63, 80, 100, 125, 150, 200 o 250 mm).
        """

        valores_limite = [3, 16, 40, 63, 80, 100, 125, 150, 200, 250, 400]
        t_max = next(valor for valor in valores_limite if self.t <= valor)

        return t_max

    def limite_elastico(self) -> int:
        """
        Obtiene el valor del límite elástico f.y para un acero y espesor nominal t.

        :return: Valor f.y en N/mm².
        """
        df = self._load_dataframe()
        # print(df)
        t_max = self._obtener_t_max()
        print(f'{t_max = }')
        # return df[(df['Calidad'] == self.acero) & (df['tmax'] == t_max)]['fy'].values[0]
        return df[(df['Calidad'].str.contains(self.acero)) & (df['tmax'] == t_max)]['fy'].values[0]

    def resistencia_ultima_traccion(self) -> int:
        """
        Obtiene el valor de la resistencia última a tracción f.u para un acero y espesor nominal t.

        :return: Valor f.u en N/mm².
        """
        df = self._load_dataframe()
        t_max = self._obtener_t_max()
        # return df[(df['Calidad'] == self.acero) & (df['tmax'] == t_max)]['fu'].values[0]
        return df[(df['Calidad'].str.contains(self.acero)) & (df['tmax'] == t_max)]['fu'].values[0]

if __name__ == '__main__':
    import random

    # Ejemplo de simulación para obtener valores de fy y fu para aceros y espesores aleatorios
    for _ in range(10):
        # acero = random.choice(['S 235 JR', 'S 275 J0', 'S 355 J2', 'S 450 J0'])
        acero = random.choice(['S 235', 'S 275', 'S 355', 'S 450'])
        print(f'{acero = }')
        t = random.randint(1, 300)  # [mm]
        print(f'{t = }')

        # Crear instancia de DatosEN1993_1_1 con valores de acero y t
        datos = DatosEN10025_2(acero, t)

        # Obtener los valores de límite elástico (fy) y resistencia última a tracción (fu)
        fy = datos.limite_elastico()
        fu = datos.resistencia_ultima_traccion()

        # Imprimir resultados
        print(
            f'Acero: {acero}, Espesor: {t} mm, Límite elástico (f.y): {fy} N/mm², Resistencia a tracción (f.u): {fu} N/mm²'
        )
        print('---')
