import logging
import math
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict, Any
from backend.app.database.database import get_db
from backend.app.database.models import Recall

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["Manufacturer Safety Analytics"])

@router.get("/manufacturers", response_model=List[Dict[str, Any]])
def get_manufacturer_rankings(db: Session = Depends(get_db)):
    """
    Computes dynamic risk profiles and statistics for all automotive manufacturers.
    Calculates weighted safety risk indexes based on severity, tier distributions, and volume.
    """
    try:
        logger.info("Computing manufacturer safety risk profiles...")
        
        # 1. Fetch raw counts grouped by manufacturer and risk level
        results = db.query(
            Recall.manufacturer,
            Recall.risk_label,
            func.count(Recall.id).label("count"),
            func.avg(Recall.defect_severity_score).label("avg_severity")
        ).group_by(
            Recall.manufacturer, 
            Recall.risk_label
        ).all()

        # 2. Structure data per manufacturer
        mfr_data = {}
        for mfr, label, count, avg_sev in results:
            if mfr not in mfr_data:
                mfr_data[mfr] = {
                    "manufacturer": mfr,
                    "total_recalls": 0,
                    "low_risk_count": 0,
                    "medium_risk_count": 0,
                    "high_risk_count": 0,
                    "critical_risk_count": 0,
                    "severity_scores_sum": 0.0,
                }
            
            mfr_data[mfr]["total_recalls"] += count
            mfr_data[mfr]["severity_scores_sum"] += (avg_sev or 0.0) * count
            
            lbl_lower = label.lower()
            if "low" in lbl_lower:
                mfr_data[mfr]["low_risk_count"] += count
            elif "medium" in lbl_lower or "moderate" in lbl_lower:
                mfr_data[mfr]["medium_risk_count"] += count
            elif "high" in lbl_lower:
                mfr_data[mfr]["high_risk_count"] += count
            elif "critical" in lbl_lower:
                mfr_data[mfr]["critical_risk_count"] += count

        # 3. Calculate dynamic safety index and average severity
        rankings = []
        for mfr, profile in mfr_data.items():
            total = profile["total_recalls"]
            if total == 0:
                continue
                
            avg_severity = profile["severity_scores_sum"] / total
            
            # Dynamic Safety Risk Index formula:
            # penalizes High/Critical recalls heavier, and scales logarithmically with volume (number of recalls)
            critical_weight = profile["critical_risk_count"] * 5.0
            high_weight = profile["high_risk_count"] * 3.0
            med_weight = profile["medium_risk_count"] * 1.5
            low_weight = profile["low_risk_count"] * 0.5
            
            severity_factor = (critical_weight + high_weight + med_weight + low_weight) / total
            volume_multiplier = math.log1p(total)  # log(total + 1)
            
            risk_index = float(round(severity_factor * volume_multiplier * 10, 2))
            
            rankings.append({
                "manufacturer": mfr,
                "total_recalls": total,
                "low_risk_count": profile["low_risk_count"],
                "medium_risk_count": profile["medium_risk_count"],
                "high_risk_count": profile["high_risk_count"],
                "critical_risk_count": profile["critical_risk_count"],
                "average_severity_score": float(round(avg_severity, 4)),
                "safety_risk_index": risk_index
            })

        # Sort manufacturers by safety risk index descending (highest risk first)
        rankings = sorted(rankings, key=lambda x: x["safety_risk_index"], reverse=True)
        
        return rankings

    except Exception as e:
        logger.error(f"Error computing manufacturer analytics: {e}")
        return []
