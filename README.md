# Recani: Hybrid Anime Recommender

Recani is a hybrid anime recommender system utilizing a multi-armed bandit algorithm. This project aims to provide personalized anime recommendations by combining content-based filtering and collaborative filtering techniques.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Introduction
Recani is designed to enhance the anime-watching experience by suggesting titles that match the user's preferences. By leveraging both user data and anime content data, the system dynamically adapts to user behavior and improves its recommendations over time.

## Features
- **Hybrid Recommendation**: Combines content-based and collaborative filtering.
- **Multi-Armed Bandit Algorithm**: Uses exploration and exploitation to optimize recommendations.
- **Web Scraping**: Extracts anime data from various sources.
- **Interactive Interface**: Provides an easy-to-use interface for users to get recommendations.

## Installation
To install and run the project locally, follow these steps:

1. **Clone the repository:**
   bash
   git clone https://github.com/manoj-323/recani.git
   cd recani
   

2. **Create a virtual environment:**
   bash
   python -m venv venv
   source venv/bin/activate   # On Windows use venv\Scripts\activate
   

3. **Install dependencies:**
   bash
   pip install -r requirements.txt
   

4. **Install Jupyter Notebook (if not already installed):**
   bash
   pip install notebook
   

## Usage
To start using the recommender system:

1. **Run Jupyter Notebook:**
   bash
   jupyter notebook
   

2. **Open the main notebook:**
   Navigate to `Recani.ipynb` in your Jupyter interface and execute the cells to start the recommendation system.

## Project Structure
- `data/`: Contains datasets used for recommendations.
- `notebooks/`: Jupyter Notebooks with the main code for the project.
- `web_scraping/`: Scripts for extracting anime data from web sources.
- `config/`: Configuration files for the project.
- `requirements.txt`: List of dependencies.
- `README.md`: Project documentation.

## Contributing
We welcome contributions from the community! If you have suggestions, bug reports, or improvements, feel free to submit a pull request or open an issue.

### Steps to Contribute
1. Fork the repository.
2. Create a new branch.
3. Make your changes.
4. Submit a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

