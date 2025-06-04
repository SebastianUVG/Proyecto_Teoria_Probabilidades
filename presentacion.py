import streamlit as st
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("🎯 Análisis del Problema de Monty Hall")

st.header("📘 Explicación Teórica del Problema de Monty Hall")

st.write("""
Análisis del Problema de Monty Hall

Un concursante debe elegir 1 puerta entre 3 (todas cerradas); el premio consiste en llevarse lo que se encuentra detrás de la puerta elegida. Se sabe con certeza que tras una de ellas hay un premio, y tras las otras dos no hay premio.

Una vez que el concursante haya elegido una puerta y comunicado su elección a los presentes, el presentador, que sabe lo que hay detrás de cada puerta, abrirá una de las otras dos, en la que no habrá premio. A continuación, le da la opción al concursante de cambiar, si lo desea, de puerta.

Pregunta 1. ¿Debe el concursante mantener su elección original o escoger la otra puerta?

Pregunta 2. ¿Existe alguna diferencia en la estrategia si en lugar de 3 se tienen 5 puertas (1 con premio y 4 sin premio)?
""")

st.subheader("Caso con 3 puertas")
st.write("""
- Supón que eliges una puerta (probabilidad de acertar = 1/3).
- El presentador abre una puerta vacía entre las dos restantes.
- Si decides cambiar, la probabilidad de ganar pasa a ser 2/3.
Esto se debe a que si tu elección inicial fue incorrecta (2/3 de las veces), cambiar te lleva a la puerta con premio.
""")

st.latex(r"\text{P(Ganar sin cambiar)} = \frac{1}{3}")
st.latex(r"\text{P(Ganar cambiando)} = \frac{2}{3}")

st.subheader("Caso con 5 puertas")
st.write("""
En este caso, hay más puertas, pero el principio es el mismo.
- P(elegir la puerta ganadora al inicio) = 1/5.
- El presentador abre 1 puerta sin premio.
- Si decides cambiar, ahora eliges entre las 3 restantes (excluyendo la elegida y la abierta).

Supongamos que tu elección inicial fue incorrecta (probabilidad 4/5). Entre las 3 puertas que quedan, una tiene premio, y eliges una aleatoriamente:
""")

st.latex(r"\text{P(Ganar sin cambiar)} = \frac{1}{5} = 0.2")
st.latex(r"\text{P(Ganar cambiando)} = \frac{4}{5} \cdot \frac{1}{3} = \frac{4}{15} \approx 0.2667")

st.markdown("---")
st.header("📂 Carga de Datos de Simulaciones")


# GRAFICAS


@st.cache_data
def cargar_datos():
    datos = {
        "3 puertas - Sin cambiar": pd.read_csv("3nocambio.csv"),
        "3 puertas - Cambiando": pd.read_csv("3cambio.csv"),
        "5 puertas - Sin cambiar": pd.read_csv("5nocambio.csv"),
        "5 puertas - Cambiando": pd.read_csv("5cambio.csv"),
    }
    for k in datos:
        datos[k]["acumulado"] = datos[k]["resultado"].expanding().mean()
    return datos

datos = cargar_datos()
st.success("Archivos CSV cargados correctamente.")
st.header("📈 Resultados Experimentales (Media Acumulada)")

col1, col2 = st.columns([1, 3])
with col1:
    opciones_menu = [
        "3 puertas - Sin cambiar",
        "3 puertas - Cambiando",
        "5 puertas - Sin cambiar",
        "5 puertas - Cambiando",
        "Comparativa 3 puertas",
        "Comparativa 5 puertas"
    ]
    seleccion = st.selectbox("Selecciona el experimento:", opciones_menu)

    max_iter = len(next(iter(datos.values())))
    iteraciones = st.slider("Número de simulaciones a mostrar", 100, max_iter, 10000, step=500)

with col2:
    if seleccion in datos:
        df = datos[seleccion].head(iteraciones)
        media_final = df["resultado"].mean()
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(df["acumulado"], label="Media acumulada")
        ax.axhline(media_final, color='r', linestyle='--', label="Media final")
        ax.text(iteraciones * 0.95, media_final + 0.01, f"{media_final:.4f}", color='red', fontsize=10, ha='right')
        ax.set_title(f"Estrategia: {seleccion}")
        ax.set_xlabel("Simulación")
        ax.set_ylabel("Tasa de Éxito")
        ax.legend()
        st.pyplot(fig)
    
    elif seleccion == "Comparativa 3 puertas":
        df_3_nc = datos["3 puertas - Sin cambiar"].head(iteraciones)
        df_3_c = datos["3 puertas - Cambiando"].head(iteraciones)
        media_nc_3 = df_3_nc["resultado"].mean()
        media_c_3 = df_3_c["resultado"].mean()

        fig1, ax1 = plt.subplots(figsize=(10, 5))
        ax1.plot(df_3_nc["acumulado"], label="Sin cambiar")
        ax1.plot(df_3_c["acumulado"], label="Cambiando")
        ax1.axhline(media_nc_3, color='gray', linestyle='--')
        ax1.axhline(media_c_3, color='red', linestyle='--')
        ax1.text(iteraciones * 0.95, media_nc_3 + 0.01, f"{media_nc_3:.4f}", color='gray', ha='right')
        ax1.text(iteraciones * 0.95, media_c_3 + 0.01, f"{media_c_3:.4f}", color='red', ha='right')
        ax1.set_title("Estrategias con 3 Puertas")
        ax1.set_xlabel("Simulación")
        ax1.set_ylabel("Tasa de Éxito")
        ax1.legend()
        st.pyplot(fig1)
    
    elif seleccion == "Comparativa 5 puertas":
        df_5_nc = datos["5 puertas - Sin cambiar"].head(iteraciones)
        df_5_c = datos["5 puertas - Cambiando"].head(iteraciones)
        media_nc_5 = df_5_nc["resultado"].mean()
        media_c_5 = df_5_c["resultado"].mean()

        fig2, ax2 = plt.subplots(figsize=(10, 5))
        ax2.plot(df_5_nc["acumulado"], label="Sin cambiar")
        ax2.plot(df_5_c["acumulado"], label="Cambiando")
        ax2.axhline(media_nc_5, color='gray', linestyle='--')
        ax2.axhline(media_c_5, color='red', linestyle='--')
        ax2.text(iteraciones * 0.95, media_nc_5 + 0.01, f"{media_nc_5:.4f}", color='gray', ha='right')
        ax2.text(iteraciones * 0.95, media_c_5 + 0.01, f"{media_c_5:.4f}", color='red', ha='right')
        ax2.set_title("Estrategias con 5 Puertas")
        ax2.set_xlabel("Simulación")
        ax2.set_ylabel("Tasa de Éxito")
        ax2.legend()
        st.pyplot(fig2)


def tasa_victoria(df):
    return round(df['resultado'].mean(), 4) 

resultados = pd.DataFrame({
    "Estrategia": ["3 puertas - Sin cambio", "3 puertas - Cambio", "5 puertas - Sin cambio", "5 puertas - Cambio"],
    "Tasa de Victoria": [
        tasa_victoria(datos["3 puertas - Sin cambiar"]),
        tasa_victoria(datos["3 puertas - Cambiando"]),
        tasa_victoria(datos["5 puertas - Sin cambiar"]),
        tasa_victoria(datos["5 puertas - Cambiando"]),
    ]
})  

st.markdown("---")
barras = alt.Chart(resultados).mark_bar().encode(
    x=alt.X('Estrategia', sort=None),
    y='Tasa de Victoria',
    color='Estrategia'
).properties(width=700, height=400)

st.altair_chart(barras)

st.markdown("---")
st.header("📜 Código de Simulación Utilizado")

with st.expander("🔢 Código - 3 puertas (sin cambiar)"):
    st.code("""
puertas = []
puerta_ganadora = []
puerta_abierta = []
victoria_3puertas = []

def puerta_elegida(n):
    if n <= 0.33:
        return 0
    elif 0.33 < n <= 0.66:
        return 1
    else:
        return 2

random.seed(2025)
for i in range(10**5):
    p = random.random()
    puerta_ganadora.append(puerta_elegida(p))
    n = random.random()
    puertas.append(puerta_elegida(n))
    e = random.random()
    while (puerta_elegida(e) == puertas[i]) or puerta_elegida(e) == puerta_ganadora[i]:
        e = random.random()
    puerta_abierta.append(puerta_elegida(e))
    if puertas[i] == puerta_ganadora[i]:
        victoria_3puertas.append(1)
    else:
        victoria_3puertas.append(0)
            
print(statistics.mean(victoria_3puertas))
    """, language='python')

with st.expander("🔢 Código - 3 puertas (cambiando)"):
    st.code("""
puertas2 = []
final_choise = []
puerta_ganadora2 = []
puerta_abierta2 = []
victoria2_3puertas = []
posibilidades = [0, 1, 2]

def puerta_elegida(n):
    if n <= 0.33:
        return 0
    elif 0.33 < n <= 0.66:
        return 1
    else:
        return 2

random.seed(2025)
for i in range(10**5):
    p = random.random()
    puerta_ganadora2.append(puerta_elegida(p))
    n = random.random()
    puertas2.append(puerta_elegida(n))
    e = random.random()
    while (puerta_elegida(e) == puertas2[i]) or puerta_elegida(e) == puerta_ganadora2[i]:
        e = random.random()
    puerta_abierta2.append(puerta_elegida(e))
    puerta1 = puertas2[i]
    puerta2 = puerta_abierta2[i]
    fc = list(set(posibilidades) - set([puerta1, puerta2]))[0]
    final_choise.append(fc)
    if fc == puerta_ganadora2[i]:
        victoria2_3puertas.append(1)
    else:
        victoria2_3puertas.append(0)
            
print(statistics.mean(victoria2_3puertas))
    """, language='python')

with st.expander("🔢 Código - 5 puertas (sin cambiar)"):
    st.code("""
puertas = []
puerta_ganadora = []
puerta_abierta = []
victoria_5puertas = []

def puerta_elegida1(n):
    if n <= 0.2:
        return 0
    elif 0.2 < n <= 0.4:
        return 1
    elif 0.4 < n <= 0.6:
        return 2
    elif 0.6 < n <= 0.8:
        return 3
    else:
        return 4

random.seed(2025)
for i in range(10**5):
    p = random.random()
    puerta_ganadora.append(puerta_elegida1(p))
    n = random.random()
    puertas.append(puerta_elegida1(n))
    e = random.random()
    while (puerta_elegida1(e) == puertas[i]) or puerta_elegida1(e) == puerta_ganadora[i]:
        e = random.random()
    puerta_abierta.append(puerta_elegida1(e))
    if puertas[i] == puerta_ganadora[i]:
        victoria_5puertas.append(1)
    else:
        victoria_5puertas.append(0)
            
print(statistics.mean(victoria_5puertas))
    """, language='python')

with st.expander("🔢 Código - 5 puertas (cambiando)"):
    st.code("""
puertas2 = []
final_choise = []
puerta_ganadora2 = []
puerta_abierta2 = []
victoria2_5puertas = []
posibilidades = [0, 1, 2, 3, 4]

random.seed(2025)
for i in range(10**5):
    p = random.random()
    puerta_ganadora2.append(puerta_elegida1(p))
    n = random.random()
    puertas2.append(puerta_elegida1(n))
    e = random.random()
    while (puerta_elegida1(e) == puertas2[i]) or puerta_elegida1(e) == puerta_ganadora2[i]:
        e = random.random()
    puerta_abierta2.append(puerta_elegida1(e))
    puerta1 = puertas2[i]
    puerta2 = puerta_abierta2[i]
    fc = list(set(posibilidades) - set([puerta1, puerta2]))[0]
    final_choise.append(fc)
    if fc == puerta_ganadora2[i]:
        victoria2_5puertas.append(1)
    else:
        victoria2_5puertas.append(0)

print(statistics.mean(victoria2_5puertas))
    """, language='python')
