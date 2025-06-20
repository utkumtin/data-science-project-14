from unittest.mock import patch
import pytest
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tasks.task_manager import *

@pytest.fixture
def sample_df():
    return pd.DataFrame({
        'Chemical': ['Meth', 'Acetone', 'Mercury'],
        'Amount': [25, 10, 0.5],
        'Unit': ['liter', 'liter', 'kg'],
        'IsHazardous': [True, False, True]
    })

def test_plot_line_chart():
    data = {2010: 80, 2011: 85, 2012: 78}
    with patch('matplotlib.pyplot.show') as mock_show:
        plot_line_chart(data)
        mock_show.assert_called_once()

def test_plot_bar_chart():
    characters = ['Geralt', 'Yennefer', 'Ciri']
    kills = [120, 50, 80]
    with patch('matplotlib.pyplot.show') as mock_show:
        plot_bar_chart(characters, kills)
        mock_show.assert_called_once()

def test_plot_pie_chart():
    factions = {'Witchers': 40, 'Sorcerers': 35, 'Monsters': 25}
    with patch('matplotlib.pyplot.show') as mock_show:
        plot_pie_chart(factions)
        mock_show.assert_called_once()

def test_plot_histogram():
    experience_years = [5, 10, 7, 8, 6, 10, 12, 4]
    with patch('matplotlib.pyplot.show') as mock_show:
        plot_histogram(experience_years)
        mock_show.assert_called_once()

def test_plot_scatterplot():
    x = [80, 90, 75]
    y = [70, 85, 60]
    labels = ['Geralt', 'Yennefer', 'Ciri']
    with patch('matplotlib.pyplot.show') as mock_show:
        plot_scatterplot(x, y, labels)
        mock_show.assert_called_once()


def test_plot_multi_line_chart():
    data = {
        "Geralt": {2010: 80, 2011: 85, 2012: 78},
        "Ciri": {2010: 70, 2011: 75, 2012: 80}
    }
    with patch('matplotlib.pyplot.show') as mock_show:
        plot_multi_line_chart(data)
        mock_show.assert_called_once()

def test_plot_stacked_bar_chart():
    categories = ['Ghoul', 'Wraith', 'Dragon']
    values = {
        'Geralt': [10, 15, 5],
        'Ciri': [7, 12, 3]
    }
    with patch('matplotlib.pyplot.show') as mock_show:
        plot_stacked_bar_chart(categories, values)
        mock_show.assert_called_once()

def test_plot_boxplot():
    data = {
        'Geralt': [70, 75, 80, 85],
        'Ciri': [60, 65, 70, 75]
    }
    with patch('matplotlib.pyplot.show') as mock_show:
        plot_boxplot(data)
        mock_show.assert_called_once()

def send_post_request(url: str, data: dict, headers: dict = None):
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()  # hata varsa exception fırlatır
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err} - Status Code: {response.status_code}")
    except Exception as err:
        print(f"Other error occurred: {err}")

class ResultCollector:
    def __init__(self):
        self.passed = 0
        self.failed = 0

    def pytest_runtest_logreport(self, report):
        if report.when == "call":
            if report.passed:
                self.passed += 1
            elif report.failed:
                self.failed += 1

def run_tests():
    collector = ResultCollector()
    pytest.main(["tests"], plugins=[collector])
    print(f"\nToplam Başarılı: {collector.passed}")
    print(f"Toplam Başarısız: {collector.failed}")
    
    user_score = (collector.passed / (collector.passed + collector.failed)) * 100
    print(round(user_score, 2))
    
    url = "https://edugen-backend-487d2168bc6c.herokuapp.com/projectLog/"
    payload = {
        "user_id": 34,
        "project_id": 266,
        "user_score": round(user_score, 2),
        "is_auto": False
    }
    headers = {
        "Content-Type": "application/json"
    }
    send_post_request(url, payload, headers)

if __name__ == "__main__":
    run_tests()