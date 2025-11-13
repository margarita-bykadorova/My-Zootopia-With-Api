import json
import html
from typing import Any, Dict, List

DATA_FILE = "animals_data.json"
TEMPLATE_FILE = "animals_template.html"
OUTPUT_FILE = "animals.html"
PLACEHOLDER = "__REPLACE_ANIMALS_INFO__"


def load_data(file_path: str) -> Any:
    """Loads a JSON file."""
    with open(file_path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def esc(value: Any) -> str | None:
    """HTML-escape a value if it exists."""
    return html.escape(str(value)) if value is not None else None


def prompt_for_skin_type(skin_types: List[str], has_unknown: bool = False) -> str:
    """Prompt the user to choose a skin_type from the displayed list.
    Returns the chosen skin_type label (original casing), or 'Unknown'."""

    print("Available skin types:")
    for st in skin_types:
        print(f" - {st}")
    if has_unknown:
        print(" - Unknown")

    lookup = {st.lower(): st for st in skin_types}
    if has_unknown:
        lookup["unknown"] = "Unknown"

    while True:
        choice_raw = input("\nEnter a skin_type from the list above: ").strip().lower()
        if choice_raw in lookup:
            return lookup[choice_raw]
        print("Not in the list. Please enter exactly one of the shown values.")


def serialize_animal(animal: Dict[str, Any]) -> str:
    """Serialize a single animal into an HTML <li> block with inner list styling classes.
    Returns an HTML string for one card; empty string if the name is missing."""

    name = esc(animal.get("name"))
    locations: List[str] = animal.get("locations", []) or []
    characteristics: Dict[str, Any] = animal.get("characteristics", {}) or {}

    diet = esc(characteristics.get("diet"))
    animal_type = esc(characteristics.get("type"))
    main_prey = esc(characteristics.get("main_prey"))
    distinctive_feature = esc(
        characteristics.get("distinctive_feature")
        or characteristics.get("most_distinctive_feature")
    )
    habitat = esc(characteristics.get("habitat"))

    if not name:
        return ""

    # Indentation helper for readable HTML output
    i = " "

    parts: List[str] = [
        f"<li class='cards__item'>",
        f"{i * 2}<div class='card__title'><strong>{name}</strong></div>",
        f"{i * 2}<div class='card__text'>",
        f"{i * 4}<ul class='animal-info'>",
    ]

    if diet:
        parts.append(f"{i * 6}<li class='animal-info__item'>"
                     f"<strong>Diet:</strong> {diet}</li>")
    if main_prey:
        parts.append(f"{i * 6}<li class='animal-info__item'>"
                     f"<strong>Main prey:</strong> {main_prey}</li>")
    if locations:
        parts.append(f"{i * 6}<li class='animal-info__item'>"
                     f"<strong>Location:</strong> {esc(locations[0])}</li>")
    if habitat:
        parts.append(f"{i * 6}<li class='animal-info__item'>"
                     f"<strong>Habitat:</strong> {habitat}</li>")
    if animal_type:
        parts.append(f"{i * 6}<li class='animal-info__item'>"
                     f"<strong>Type:</strong> {animal_type}</li>")
    if distinctive_feature:
        parts.append(
            f"{i * 6}<li class=\"animal-info__item\">"
            f"<strong>Distinctive feature:</strong> {distinctive_feature}</li>")

    parts.extend([
        f"{i * 4}</ul>",
        f"{i * 2}</div>",
        "</li>",
    ])
    return "\n".join(parts) + "\n"


def collect_skin_types(data) -> list:
    """Collect unique, non-empty skin_type values; keep first-seen order and casing."""

    seen_lowercase = set()
    skin_types = []

    for animal in data:
        characteristics = animal.get("characteristics", {})
        skin_type = characteristics.get("skin_type")
        if not skin_type:
            continue

        skin_type_str = str(skin_type).strip()
        if not skin_type_str:
            continue

        skin_type_lower = skin_type_str.lower()
        if skin_type_lower not in seen_lowercase:
            seen_lowercase.add(skin_type_lower)
            skin_types.append(skin_type_str)

    return skin_types


def filter_by_skin_type(data, chosen_skin: str) -> list:
    """Filter animals by a chosen skin_type (case-insensitive)."""

    filtered_animals = []
    chosen_skin_lower = chosen_skin.strip().lower()

    for animal in data:
        characteristics = animal.get("characteristics", {})
        skin_type = characteristics.get("skin_type")
        if not skin_type:
            continue

        if str(skin_type).strip().lower() == chosen_skin_lower:
            filtered_animals.append(animal)

    return filtered_animals


def collect_unknown_skin_type(data) -> list:
    """Collect animals whose characteristics.skin_type is missing or empty."""

    unknown = []
    for animal in data:
        characteristics = animal.get("characteristics", {})
        skin_type = characteristics.get("skin_type")
        if not skin_type or not str(skin_type).strip():
            unknown.append(animal)
    return unknown


def select_animals_by_choice(data, chosen_label: str, unknown_animals: list) -> list:
    """Select animals based on the chosen label, including 'Unknown'."""
    if chosen_label == "Unknown":
        return unknown_animals
    return filter_by_skin_type(data, chosen_label)


def create_new_html(cards_html: str, chosen_label: str, count: int) -> None:
    """Replace the placeholder and write the output HTML, with h2 subheading."""

    with open(TEMPLATE_FILE, "r", encoding="utf-8") as template:
        tpl = template.read()

    html_out = tpl.replace(PLACEHOLDER, cards_html)
    count_label = "animal" if count == 1 else "animals"
    heading_html = (
        "<h1>My Animal Repository</h1>\n"
        f"<h2 class='subheading'>Skin type: {chosen_label} "
        f"({count} {count_label})</h2>"
    )
    html_out = html_out.replace("<h1>My Animal Repository</h1>", heading_html)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as new:
        new.write(html_out)


def main() -> None:
    """Entry point: prompt for a skin_type, filter animals, render the HTML."""

    data = load_data(DATA_FILE)
    skin_types = collect_skin_types(data)
    unknown_animals = collect_unknown_skin_type(data)

    if not skin_types and not unknown_animals:
        print("No skin types found in data.")
        return

    chosen_label = prompt_for_skin_type(skin_types, has_unknown=bool(unknown_animals))
    filtered = select_animals_by_choice(data, chosen_label, unknown_animals)
    if not filtered:
        print(f"No animals found with skin_type = '{chosen_label}'.")
        return

    cards_html = "".join(serialize_animal(a) for a in filtered)
    create_new_html(cards_html, chosen_label, len(filtered))

    print(f"\nFound {len(filtered)} animals matching the selected criteria.")
    print(f"Generated {OUTPUT_FILE} with skin_type = '{chosen_label}'.")


if __name__ == "__main__":
    main()
