protocol_cards = {
    'VÍSPERA': {
        'trigger': 'Indicadores de riesgo elevados — (viento 40-89 km/h, inundación 50-149 cm)',
        'actions': [
            'Activar alerta regional',
            'Movilizar equipos de evaluación',
            'Pre-posicionar recursos críticos'
        ]
    },
    'CÓDIGO ROJO': {
        'trigger': 'Amenaza inminente — (viento >=90 km/h, inundación >=150 cm)',
        'actions': [
            'Evacuación selectiva',
            'Corte de rutas no críticas',
            'Activación de centro de mando'
        ]
    },
    'RENACIMIENTO': {
        'trigger': 'Condiciones normalizadas — recuperación',
        'actions': [
            'Evaluación de daños',
            'Plan de recuperación',
            'Comunicación pública'
        ]
    }
}

def evaluate_protocol(sensors: dict) -> dict:
    viento = sensors.get('viento_kmh', 0)
    inund = sensors.get('inundacion_cm', 0)
    fuego = sensors.get('fuego_temp', 0)

    if viento >= 90 or inund >= 150 or fuego >= 850:
        return {'protocol': 'CÓDIGO ROJO', 'reason': 'Condición extrema detectada'}
    if 40 <= viento < 90 or 50 <= inund < 150 or 400 <= fuego < 850:
        return {'protocol': 'VÍSPERA', 'reason': 'Riesgo elevado — vigilar'}
    return {'protocol': 'RENACIMIENTO', 'reason': 'Condiciones normales'}
