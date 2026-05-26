import os
import logging
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Configure logger
logger = logging.getLogger(__name__)

# Fallback to SQLite for local runs; use PostgreSQL in production/docker
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "sqlite:///./autosentinel.db"
)

# Connect arguments needed only for SQLite
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    DATABASE_URL, 
    connect_args=connect_args
)

SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    from backend.app.database.models import Recall
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables initialized successfully.")

def ingest_initial_data():
    """
    Ingest data from ml_ready_vehicle_recalls.csv into the database if the table is empty.
    Allows dashboard and analytical APIs to serve actual metrics from first boot.
    """
    from backend.app.database.models import Recall
    db = SessionLocal()
    try:
        count = db.query(Recall).count()
        if count > 0:
            logger.info(f"Database already populated with {count} recalls. Ingestion skipped.")
            return

        # Find ML ready dataset CSV
        csv_paths = [
            "/app/data/processed/ml_ready_vehicle_recalls.csv",
            "data/processed/ml_ready_vehicle_recalls.csv",
            "../data/processed/ml_ready_vehicle_recalls.csv"
        ]
        
        csv_file = None
        for path in csv_paths:
            if os.path.exists(path):
                csv_file = path
                break
                
        if not csv_file:
            logger.warning("ML ready safety recalls CSV file not found. Ingestion skipped.")
            return

        logger.info(f"Reading records from {csv_file}...")
        df = pd.read_csv(csv_file, low_memory=False)
        
        # Fill missing values
        df["ai_summary"] = df["ai_summary"].fillna("General vehicle safety recall")
        df["consequence"] = df["consequence"].fillna("No consequence provided")
        df["remedy"] = df["remedy"].fillna("No remedy provided")
        df["defect_severity_score"] = df["defect_severity_score"].fillna(0.0)
        df["recall_risk_score"] = df["recall_risk_score"].fillna(0.0)
        df["vehicle_make"] = df["vehicle_make"].fillna("Unknown")
        df["vehicle_model"] = df["vehicle_model"].fillna("Unknown")

        recalls = []
        for index, row in df.iterrows():
            recall = Recall(
                record_id=str(row.get("record_id", f"rec_{index}")),
                nhtsa_record_id=str(row.get("nhtsa_record_id", f"nhtsa_{index}")),
                manufacturer=str(row.get("manufacturer", "Unknown")),
                component=str(row.get("component", "Other")),
                summary=str(row.get("summary", "")),
                consequence=str(row.get("consequence", "")),
                remedy=str(row.get("remedy", "")),
                model_year=int(row.get("model_year", 2015)),
                risk_label=str(row.get("risk_label", "Low")),
                ai_summary=str(row.get("ai_summary", "")),
                vehicle_make=str(row.get("vehicle_make", "")),
                vehicle_model=str(row.get("vehicle_model", "")),
                defect_severity_score=float(row.get("defect_severity_score", 0.0)),
                recall_risk_score=float(row.get("recall_risk_score", 0.0))
            )
            recalls.append(recall)

        logger.info(f"Bulk inserting {len(recalls)} recalls into database...")
        db.bulk_save_objects(recalls)
        db.commit()
        logger.info("Bulk ingestion completed successfully.")
    except Exception as e:
        db.rollback()
        logger.error(f"Error during bulk data ingestion: {e}")
    finally:
        db.close()
