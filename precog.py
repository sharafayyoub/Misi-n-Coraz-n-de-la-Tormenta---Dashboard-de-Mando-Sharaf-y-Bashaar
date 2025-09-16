def predict_risk(slider_inputs: dict) -> dict:
    w = {
        'velocidad_media': 0.35,
        'intensidad_lluvia': 0.30,
        'congestion': 0.20,
        'temperatura': 0.15
    }
    vm = min(max(slider_inputs.get('velocidad_media', 0) / 150.0, 0), 1)
    il = min(max(slider_inputs.get('intensidad_lluvia', 0) / 200.0, 0), 1)
    cg = min(max(slider_inputs.get('congestion', 0) / 100.0, 0), 1)
    tp = min(max((slider_inputs.get('temperatura', 0) + 30) / 80.0, 0), 1)

    score = 100 * (
        w['velocidad_media'] * vm +
        w['intensidad_lluvia'] * il +
        w['congestion'] * cg +
        w['temperatura'] * tp
    )
    pct = int(round(score))
    if pct < 30:
        level = 'BAJO'
    elif pct < 60:
        level = 'MEDIO'
    elif pct < 85:
        level = 'ALTO'
    else:
        level = 'CRÍTICO'
    return {'pct': pct, 'level': level}
