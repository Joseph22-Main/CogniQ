from analysis.data_analysis import DataAnalyzer

# Sample dummy data
mood_data = [
    {"date": "2025-07-01", "mood": 3},
    {"date": "2025-07-01", "mood": 4},
    {"date": "2025-07-02", "mood": 5},
    {"date": "2025-07-03", "mood": 2}
]

journal_data = [
    {"date": "2025-07-01", "text": "Felt a bit stressed today."},
    {"date": "2025-07-02", "text": "Had a productive day at work."},
    {"date": "2025-07-02", "text": "Reflected on my goals."}
]

# Run analysis
analyzer = DataAnalyzer(mood_data, journal_data)
analyzer.mood_trend()
analyzer.journal_frequency()
analyzer.wellness_score()
