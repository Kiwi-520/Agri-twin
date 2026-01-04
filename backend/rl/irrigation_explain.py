def explain_irrigation(obs, action):
    soil, heat, rain, crop = obs
    reasons = []

    if soil < 0.5:
        reasons.append("Soil low → irrigate more")
    if heat > 0.3:
        reasons.append("Heat stress high → irrigate to cool")
    if rain > 0.05:
        reasons.append("Rain predicted → irrigate less")
    if crop > 0.6:
        reasons.append("Crop nearing maturity → moderate irrigation")

    if not reasons:
        reasons.append("Conditions normal → small irrigation")

    explanation = " + ".join(reasons)
    return f"{explanation} (Applied {action[0]:.2f} mm)"
