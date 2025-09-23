# Netflix Recommendation System (Flask)

This project is a **movie recommendation system** built using **Flask**, **pandas**, **scikit-learn**, and visualization libraries.  
It leverages **content-based filtering** with `CountVectorizer` and `cosine similarity` to suggest movies based on **genre, tags, actors, and view rating**.

---

## Features
- Content-based movie recommendations  
- Search movies by title and filter by language  
- Recommendations ranked by IMDb Score  
- Interactive web interface built with Flask templates  
- View detailed movie pages  

---

## Project Structure
```bash
├── netflix.py # Main Flask app
├── Netflix_recommend.ipynb
├── requirements.txt # Python dependencies
└── NetflixDataset.csv # Dataset file (must be placed in the right path)
```
---

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Usage
1. Clone the repository and navigate into it:
```bash
git clone https://github.com/Cyanishere/Netflix-recommendation-website.git
```

2. Add dataset: Place NetflixDataset.csv in the project’s root folder (or update the path in netflix.py).
3. Run the Flask app:
```bash
python3 netflix.py
```

Application Routes
/ → Homepage with movie/language selection
/about → Displays recommended movies
/moviepage/<name> → Detailed information about the selected movie

## License
This project is for educational purposes. You may modify and use it freely in your projects.
