import streamlit as st
import pandas as pd
from precog import predict_risk
from protocols import evaluate_protocol, protocol_cards
from utils import load_image

st.set_page_config(page_title="ChronoLogistics - War Room", layout="wide")

st.title('ChronoLogistics - Dashboard Operativo (War Room)')
st.caption('Una única fuente de verdad — Modo DEMO (simulado)')

tabs = st.tabs([
    "Precog: Monitor de Riesgo Táctico",
    "Chronos: Visión Estratégica 2040",
    "K-Lang: Manual de Batalla Interactivo"
])

# -----------------------------
# TAB 1: Precog
# -----------------------------
with tabs[0]:
    st.header('Precog — Monitor de Riesgo Táctico')
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader('Mapa de Calor de Riesgo')
        img = load_image('assets/map_heatmap.png')
        if img:
            st.image(img, use_column_width=True,
                     caption='Mapa de clústeres — Triángulo del Peligro marcado abajo')
            st.markdown('**Triángulo del Peligro:** Top 3 clústeres críticos: A(40.42, -3.70), B(40.43, -3.71), C(40.41, -3.69)')
        else:
            st.warning('Imagen `map_heatmap.png` no encontrada en assets/')

        st.markdown('---')
        st.subheader('Simulador de Riesgo Interactivo')
        with st.form('sim_form'):
            velocidad_media = st.slider('Velocidad media vehículos (km/h)', 0, 150, 60)
            intensidad_lluvia = st.slider('Intensidad lluvia (mm/h)', 0, 200, 12)
            congestion = st.slider('Congestión (%)', 0, 100, 35)
            temperatura = st.slider('Temperatura ambiente (°C)', -30, 50, 18)
            submitted = st.form_submit_button('Calcular nivel de riesgo')

        inputs = {
            'velocidad_media': velocidad_media,
            'intensidad_lluvia': intensidad_lluvia,
            'congestion': congestion,
            'temperatura': temperatura
        }

        if submitted:
            res = predict_risk(inputs)
            st.metric(label='Nivel de Riesgo en Cascada',
                      value=f"{res['pct']}%",
                      delta=res['level'])
            if res['level'] in ('CRÍTICO', 'ALTO'):
                st.error(f"{res['level']} — Acción requerida inmediata")
            elif res['level'] == 'MEDIO':
                st.warning('MEDIO — Monitorizar y preparar recursos')
            else:
                st.success('BAJO — Operación normal')

    with col2:
        st.subheader('Panel Rápido — Variables en tiempo real')
        st.write('Resumen de entradas actuales:')
        df = pd.DataFrame([inputs])
        st.dataframe(df, use_container_width=True)

        st.markdown('---')
        st.subheader('Simulaciones guardadas')
        if 'sim_history' not in st.session_state:
            st.session_state['sim_history'] = []
        if submitted:
            st.session_state['sim_history'].append(
                {**inputs, **predict_risk(inputs)})
        st.write(pd.DataFrame(st.session_state['sim_history']).tail(5))

# -----------------------------
# TAB 2: Chronos
# -----------------------------
with tabs[1]:
    st.header('Chronos — Visión Estratégica 2040')
    st.markdown('Dirigido a la Junta Directiva e inversores.')

    strategy = st.radio('Seleccionar Estrategia:',
                        ('Fortaleza Verde', 'Búnker Tecnológico'))
    colA, colB = st.columns([1, 2])

    with colA:
        if strategy == 'Fortaleza Verde':
            st.markdown('**Fortaleza Verde** — Resiliencia sostenible.')
            img = load_image('assets/fortaleza_verde.png')
        else:
            st.markdown('**Búnker Tecnológico** — Defensa digital y automatización.')
            img = load_image('assets/bunker_tecnologico.png')

    with colB:
        if img:
            st.image(img, use_column_width=True)
        else:
            st.info('Imagen no encontrada en assets/')

        st.subheader('Defensa argumentada')
        if strategy == 'Fortaleza Verde':
            st.write('Fortaleza Verde reduce la exposición a riesgos climáticos y fomenta aceptación pública.')
        else:
            st.write('Búnker Tecnológico asegura integridad de servicios y defensa contra amenazas digitales.')
        st.markdown('**Recomendación:** combinar resiliencia física + soberanía tecnológica.')

# -----------------------------
# TAB 3: K-Lang
# -----------------------------
with tabs[2]:
    st.header('K-Lang — Manual de Batalla Interactivo')

    protocol_choice = st.selectbox(
        'Selecciona protocolo:', ('VÍSPERA', 'CÓDIGO ROJO', 'RENACIMIENTO'))
    card = protocol_cards[protocol_choice]
    st.markdown(f"**Ficha Técnica — {protocol_choice}**")
    st.write('Disparador:', card['trigger'])
    st.write('Acciones:')
    for i, a in enumerate(card['actions'], start=1):
        st.write(f"{i}. {a}")

    st.subheader('Simulador de Protocolos')
    c1, c2 = st.columns(2)
    with c1:
        viento_kmh = st.slider('Velocidad del Viento (km/h)', 0, 200, 20)
        inundacion_cm = st.slider('Nivel de Inundación (cm)', 0, 500, 10)
    with c2:
        fuego_temp = st.number_input('Temperatura de fuego (°C)', 0, 2000, 25)

    sim_sensors = {
        'viento_kmh': viento_kmh,
        'inundacion_cm': inundacion_cm,
        'fuego_temp': fuego_temp
    }
    active = evaluate_protocol(sim_sensors)

    if active['protocol'] == 'CÓDIGO ROJO':
        st.error(f"PROTOCOLO ACTIVO: {active['protocol']} — {active['reason']}")
    elif active['protocol'] == 'VÍSPERA':
        st.warning(f"PROTOCOLO POTENCIAL: {active['protocol']} — {active['reason']}")
    else:
        st.success(f"Estado: {active['protocol']} — {active['reason']}")

st.sidebar.title('ChronoLogistics — War Room')
st.sidebar.write('Demo técnica. Sustituir módulos simulados por servicios reales.')
