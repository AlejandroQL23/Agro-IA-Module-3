import streamlit as st

# Barra lateral
def barra_lateral():
    st.sidebar.header('Menú de visualización y predicciones')
    opcion_principal = st.sidebar.radio('**Haz clic en:**', ['EDA', 'Predicciones'])

    if opcion_principal == 'EDA':
        opcion_eda = st.sidebar.selectbox('Selecciona una opción:',
                                          ['Resumen', 'Dispersión', 'Histograma', 'Correlación'])
        return opcion_principal, opcion_eda
    elif opcion_principal == 'Predicciones':
        return opcion_principal, None

# Main
def main():
    st.set_page_config(
        page_title='Recomendación de acción',
        layout='wide',
        initial_sidebar_state='expanded'
    )

    # Llamar a la barra lateral
    opcion_principal, opcion_elegida = barra_lateral()

    # Contenedor para texto principal
    with st.container():
        st.title('AgroIA: Asistente Inteligente para el cultivo de la papa en Cartago, Costa Rica')
        st.write("""
        **AgroIA** ofrece recomendaciones para el manejo de cultivos, basadas en condiciones climáticas y del suelo. Usando un algoritmo de clasificación multiclase, el sistema sugiere acciones preventivas.
        """)

    # Inputs para predicciones
    if opcion_principal == 'Predicciones':
        with st.container():
            st.subheader('Ingrese los datos')

            # Ingresar datos
            temperatura = st.number_input('Temperatura máxima (°C)', min_value=0, max_value=50)
            humedad_aire = st.number_input('Humedad del aire (%)', min_value=0, max_value=100)
            precipitacion = st.number_input('Precipitación (mm)', min_value=0, max_value=1000)
            ph_suelo = st.number_input('pH del suelo', min_value=0.0, max_value=14.0)
            humedad_suelo = st.number_input('Humedad del suelo (%)', min_value=0, max_value=100)

            # Boton
            if st.button('Obtener Recomendación'):
                recomendacion = obtener_recomendacion(temperatura, humedad_aire, precipitacion, ph_suelo, humedad_suelo)
                st.write(recomendacion)

    # Mostrar gráficos o análisis si es EDA
    elif opcion_principal == 'EDA':
        st.title(f"Gráfico: {opcion_elegida}")
        if opcion_elegida == 'Resumen':
            st.write('El resumen nos da un vistazo rápido de lo que está ocurriendo en tu conjunto de datos, como el valor promedio, el valor más bajo y el valor más alto.')
        # Aquí va el codigo para Resumen
        elif opcion_elegida == "Dispersión":
            st.write('Aquí se puede observar cómo se distribuyen los datos en diferentes rangos o intervalos.')
        # Aquí va el codigo para Dispersión
        elif opcion_elegida == "Histograma":
            st.write('La dispersión nos indica si los datos están cercanos entre sí o si hay una gran variedad de valores.')
        # Aquí va el codigo para Histograma
        elif opcion_elegida == "Correlacion":
            st.write('La correlacion nos muestra como se encuentran relacionadas las variables entre sí')
        # Aquí va el codigo para Correlacion
        else:
            return  None

# Función para generar recomendaciones basadas en los inputs
def obtener_recomendacion(temperatura, humedad_aire, precipitacion, ph_suelo, humedad_suelo):
    recomendacion = "Se recomienda.."
    #colocar prediccion


    return recomendacion


if __name__ == "__main__":
    main()