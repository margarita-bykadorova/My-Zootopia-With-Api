import requests
import html
from typing import Any, Dict, List


TEMPLATE_FILE = "animals_template.html"
OUTPUT_FILE = "animals.html"
PLACEHOLDER = "__REPLACE_ANIMALS_INFO__"
REQUEST_URL = "https://api.api-ninjas.com/v1/animals"
API_KEY = "my_key"
HEADERS = {"X-Api-Key": API_KEY}


def fetch_data(animal: str):
    """Fetch animal data from API. Returns a list or None."""

    try:
        res = requests.get(
            REQUEST_URL,
            headers=HEADERS,
            params={"name": animal},
            timeout=10,
        )
        if not res.ok:
            return None
        try:
            return res.json()
        except ValueError:
            return None
    except requests.RequestException:
        return None


def get_animal_name():
    """Prompt the user to choose an animal name."""

    while True:
        animal = input("Enter a name of an animal: ").strip()
        if not animal:
            print("Please enter a non-empty name.")
        elif not animal.replace(" ", "").isalpha():
            print("Please enter only letters (e.g., Fox, Snow Leopard).")
        else:
            return animal


def esc(value: Any) -> str | None:
    """HTML-escape a value if it exists."""
    return html.escape(str(value)) if value is not None else None


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
            f"{i * 6}<li class='animal-info__item'>"
            f"<strong>Distinctive feature:</strong> {distinctive_feature}</li>")

    parts.extend([
        f"{i * 4}</ul>",
        f"{i * 2}</div>",
        "</li>",
    ])
    return "\n".join(parts) + "\n"


def create_new_html(cards_html: str, animal: str, count: int) -> None:
    """Replace the placeholder and write the output HTML, with h2 subheading."""

    with open(TEMPLATE_FILE, "r", encoding="utf-8") as template:
        tpl = template.read()

    html_out = tpl.replace(PLACEHOLDER, cards_html)
    count_label = "animal" if count == 1 else "animals"
    heading_html = (
        "<h1>My Animal Repository</h1>\n"
        f"<h2 class='subheading'>Animal name: {esc(animal)} "
        f"({count} {count_label})</h2>"
    )
    html_out = html_out.replace("<h1>My Animal Repository</h1>", heading_html)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as new:
        new.write(html_out)


def main() -> None:
    """Entry point: prompt for an animal name, render the HTML."""

    animal = get_animal_name()
    data = fetch_data(animal)

    if data is None:
        cards_html = (
            f"<h2 class='subheading'>"
            f"Could not fetch data for “{esc(animal)}”.</h2>"
        )
        create_new_html(cards_html, animal, 0)
        return

    if not data:
        cards_html = (
            f"<h2 class='subheading empty-message'>"
            f"The animal “{esc(animal)}” doesn't exist.</h2>"
        )
        create_new_html(cards_html, animal, 0)
        return

    cards_html = "".join(serialize_animal(a) for a in data)
    create_new_html(cards_html, animal, len(data))

    print("Website was successfully generated to the file animals.html.")


if __name__ == "__main__":
    main()
