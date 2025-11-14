# 📘 My Zootopia (API Version)

This project generates an HTML website showing animal information fetched from the API Ninjas Animals API.

The user enters the name of an animal, the program retrieves matching results from the API, and builds a styled webpage displaying the animals’ characteristics.

This project is an upgraded version of the original “My Zootopia” which used a local JSON file.
It now uses live API data, improved error handling, and a cleaner file structure.

---

## 🚀 Features

- Fetches animal data dynamically from API Ninjas.
- Prompts the user to enter an animal name (e.g., Fox, Snow Leopard).
- Renders each animal as a styled card on an HTML page.
- Handles missing or invalid animals:
  - Shows a custom message if the API returns no results.
  - Shows a custom message if the API request fails.
- Uses environment variables (`.env`) to securely store the API key.
- Fully PEP‑8 compliant (checked with pylint).

---

## 📂 Project Structure

```
MyZootopiaWithAPI/
│
├── animals_web_generator.py   # Main program: user input, rendering HTML
├── data_fetcher.py            # API communication (clean, isolated)
├── animals_template.html      # HTML template with CSS
├── animals.html               # Generated website (output)
│
├── .env                       # Contains API_KEY (ignored by Git)
├── .gitignore                 # Ensures .env is not tracked
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

---

## 🔧 Installation & Setup

### 1. Clone the repository
```bash
git clone <repo-url>
cd <project-folder>
```

### 2. Create and activate a virtual environment (optional but recommended)
```bash
python3 -m venv venv
source venv/bin/activate   # macOS / Linux
venv\Scripts\activate      # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create a `.env` file
Inside the project folder:

```
API_KEY="your_api_key_here"
```

⚠️ The file is already listed in `.gitignore`, keeping your key private.

---

## ▶️ Usage

Run the main script:

```bash
python3 animals_web_generator.py
```

The script will ask:

```
Enter a name of an animal:
```

### Examples:
- Fox  
- Monkey  
- Snow Leopard  
- Tiger  

If results exist → **animals.html** is created and filled with cards.

If the animal does not exist → the HTML page will display:

```
The animal “<name>” doesn't exist.
```

If the API fails → the HTML page will display:

```
Could not fetch data for “<name>”.
```

---

## 📄 Output Example (animals.html)

The generated webpage contains:

- A main header  
- A subheading showing the animal name and number of results  
- A list of cards, each containing:
  - Name  
  - Location  
  - Diet  
  - Type  
  - Habitat  
  - Main prey  
  - Distinctive features  

Styling is controlled entirely in **animals_template.html**.

---

## 🤝 License

This project is for educational use.

---

## 💡 Author

Created by **[margarita-bykadorova](https://github.com/margarita-bykadorova)**  
