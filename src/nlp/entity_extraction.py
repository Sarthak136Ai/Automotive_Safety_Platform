import spacy


nlp = spacy.load(
    "en_core_web_sm"
)


COMPONENT_TERMS = [
    "ignition switch",
    "wiring",
    "fuel pump",
    "electronic control module",
    "wheel hub",
    "tire",
    "lighting",
    "cooling system",
    "axle",
    "door latch",
    "seat frame",
    "hybrid battery",
    "charger",
    "power steering",
]


FAILURE_TERMS = [
    "overheat",
    "fire",
    "stall",
    "leak",
    "shutdown",
    "fracture",
    "detach",
    "failure",
    "loss of control"
]


def extract_entities(text):

    text = str(text)

    doc = nlp(text)

    detected_components = []

    detected_failures = []

    lower_text = text.lower()

    for component in COMPONENT_TERMS:

        if component in lower_text:
            detected_components.append(
                component
            )

    for failure in FAILURE_TERMS:

        if failure in lower_text:
            detected_failures.append(
                failure
            )

    return {
        "components": list(
            set(detected_components)
        ),
        "failures": list(
            set(detected_failures)
        )
    }