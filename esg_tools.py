def calcular_esg(blend, dados_esg):
    impacto = {"CO2_total": 0, "água_total": 0}
    for oleo, percentual in blend.items():
        impacto["CO2_total"] += dados_esg[oleo]["emissões_CO2"] * percentual / 100
        impacto["água_total"] += dados_esg[oleo]["uso_água"] * percentual / 100
    return impacto