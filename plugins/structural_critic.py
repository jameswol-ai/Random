import math

class StructuralCritic:
    """
    AI reasoning layer for architectural evaluation.
    Moves system from random scoring → informed critique.
    """

    def analyze(self, design: dict) -> dict:
        cols = design["structure"]["columns"]
        beams = design["structure"]["beams"]
        area = design["area_sqm"]
        cost = design["cost"]

        # ----------------------------
        # Structural Logic
        # ----------------------------
        ratio = beams / max(1, cols)

        if ratio < 1.6:
            structural_note = "Weak beam distribution. Risk of span instability."
            structural_score = 45
        elif 1.6 <= ratio <= 2.6:
            structural_note = "Balanced structural grid. Load paths are coherent."
            structural_score = 85
        else:
            structural_note = "Over-engineered beam density. Material inefficiency likely."
            structural_score = 60

        # ----------------------------
        # Cost Logic
        # ----------------------------
        cost_per_sqm = cost / max(1, area)

        if cost_per_sqm < 1400:
            cost_note = "Economical build, but may sacrifice durability margins."
            cost_score = 70
        elif 1400 <= cost_per_sqm <= 2000:
            cost_note = "Optimal cost envelope for mid-range construction."
            cost_score = 90
        else:
            cost_note = "Premium cost zone. Verify necessity of material intensity."
            cost_score = 55

        # ----------------------------
        # Spatial Logic
        # ----------------------------
        room_count = len(design["rooms"])

        if room_count < 4:
            spatial_note = "Minimal spatial diversity. Program feels compressed."
            spatial_score = 60
        elif 4 <= room_count <= 7:
            spatial_note = "Healthy spatial hierarchy and functional distribution."
            spatial_score = 88
        else:
            spatial_note = "High complexity layout. Risk of circulation inefficiency."
            spatial_score = 75

        # ----------------------------
        # Final Judgment
        # ----------------------------
        overall = int((structural_score + cost_score + spatial_score) / 3)

        return {
            "scores": {
                "structural": structural_score,
                "cost": cost_score,
                "spatial": spatial_score,
                "overall": overall
            },
            "notes": {
                "structural": structural_note,
                "cost": cost_note,
                "spatial": spatial_note
            },
            "verdict": self._verdict(overall)
        }

    def _verdict(self, score: int) -> str:
        if score >= 85:
            return "🟢 HIGHLY VIABLE ARCHITECTURE"
        elif score >= 70:
            return "🟡 ACCEPTABLE WITH OPTIMIZATION POTENTIAL"
        else:
            return "🔴 REQUIRES STRUCTURAL REVISION"