# AI Travel Planner

An AI-powered travel planning application that helps users generate budget-friendly travel plans using multiple intelligent agents.

## Features

* Flight recommendations within budget
* Budget hotel suggestions
* Multi-day itinerary generation
* Trip cost optimization
* Multi-agent architecture using Groq LLM

## Tech Stack

* Python
* Groq API
* Streamlit
* OOP-based Agent System

## Project Structure

```text
travel-planner/
│
├── app.py
├── agents.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## Environment Variables

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_api_key_here
```

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/travel-planner.git
```

Move into the project folder:

```bash
cd travel-planner
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

## Example Use Case

* Enter destination city
* Enter total budget
* Enter number of travel days
* Get:

  * flight options
  * hotel recommendations
  * travel itinerary
  * optimized trip budget

## Future Improvements

* Real-time flight APIs
* Hotel booking integration
* Weather forecasting
* Map integration
* Personalized recommendations

## Author

Sakshi Shah
