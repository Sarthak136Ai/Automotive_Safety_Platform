import pandas as pd


COMPONENT_MAPPING = {
    "service brakes": "Brakes",
    "air bags": "Airbags",
    "electrical system": "Electrical System",
    "fuel system": "Fuel System",
    "steering": "Steering",
    "engine": "Engine",
    "seat belts": "Seat Belts",
    "suspension": "Suspension",
    "power train": "Transmission",
    "battery": "Battery"
}


COLUMN_ALIASES = {

    "manufacturer": [
        "manufacturer",
        "manufacturer_name",
        "manufacturer_text",
        "make",
        "vehicle_manufacturer"
    ],

    "component": [
        "component",
        "component_name",
        "component_category",
        "components",
        "affected_component"
    ],

    "summary": [
        "summary",
        "defect_summary",
        "description"
    ],

    "consequence": [
        "consequence",
        "consequence_summary"
    ],

    "remedy": [
        "remedy",
        "corrective_action"
    ],

    "model_year": [
        "model_year",
        "vehicle_year",
        "vehicle_year_num",
        "year"
    ]
}


def standardize_column_names(df):

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    return df


def map_columns(df):

    mapped_columns = {}

    for standard_name, aliases in COLUMN_ALIASES.items():

        for alias in aliases:

            if alias in df.columns:

                mapped_columns[alias] = standard_name

                break

    df = df.rename(columns=mapped_columns)

    return df


def normalize_manufacturer(name):

    if pd.isna(name):
        return "Unknown"

    name = str(name).strip()

    replacements = {
        "gm": "General Motors",
        "mercedes": "Mercedes-Benz"
    }

    lower_name = name.lower()

    return replacements.get(
        lower_name,
        name
    )


def normalize_component(component):

    if pd.isna(component):
        return "Other"

    component = str(component).lower()

    for key, value in COMPONENT_MAPPING.items():

        if key in component:
            return value

    return "Other"


def validate_required_columns(df):

    required_columns = [
        "manufacturer",
        "component",
        "summary"
    ]

    missing = []

    for column in required_columns:

        if column not in df.columns:
            missing.append(column)

    if missing:

        print("\nAVAILABLE COLUMNS:\n")
        print(df.columns.tolist())

        raise ValueError(
            f"\nMissing required columns: {missing}"
        )


def clean_dataset(df):

    df = standardize_column_names(df)

    df = map_columns(df)

    validate_required_columns(df)

    df = df.drop_duplicates()

    df = df.dropna(
        subset=[
            "manufacturer",
            "component",
            "summary"
        ]
    )

    df["manufacturer"] = (
        df["manufacturer"]
        .apply(normalize_manufacturer)
    )

    df["component"] = (
        df["component"]
        .apply(normalize_component)
    )

    if "consequence" not in df.columns:

        df["consequence"] = (
            "No consequence provided"
        )

    if "remedy" not in df.columns:

        df["remedy"] = (
            "No remedy provided"
        )

    if "model_year" not in df.columns:

        df["model_year"] = 2015

    df["consequence"] = (
        df["consequence"]
        .fillna("No consequence provided")
    )

    df["remedy"] = (
        df["remedy"]
        .fillna("No remedy provided")
    )

    df["model_year"] = pd.to_numeric(
        df["model_year"],
        errors="coerce"
    )

    median_year = (
        df["model_year"]
        .median()
    )

    df["model_year"] = (
        df["model_year"]
        .fillna(median_year)
    )

    return df