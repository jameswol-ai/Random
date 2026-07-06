
def run_structural_review(d):
    alerts = []

    if d["structure"]["columns"] < 16:
        alerts.append("🔴 Structural Warning: Column density too low.")

    if d["cost"] / d["area_sqm"] > 2300:
        alerts.append("🟡 Financial Alert: High material cost intensity.")

    if d["structure"]["beams"] / d["structure"]["columns"] < 1.9:
        alerts.append("🔵 Framing Alert: Beam-to-column ratio inefficient.")

    return alerts or ["🟢 Design structurally valid."]


def calculate_material_takeoffs(d):
    return [
        {"Item": "Concrete", "Qty": f"{d['structure']['columns'] * 2.6:.1f} m³"},
        {"Item": "Steel", "Qty": f"{d['structure']['beams'] * 0.48:.2f} tons"},
        {"Item": "Blocks", "Qty": f"{int(d['area_sqm'] * 42):,} units"},
        {"Item": "Load", "Qty": f"{int(d['structure']['columns'] * 13.2)} kN"}
    ]