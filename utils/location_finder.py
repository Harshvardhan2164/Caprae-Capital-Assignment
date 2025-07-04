import csv
import random
import pandas as pd

class LocationFinder:
    def __init__(self):
        self.country_groups = {
            "America": ["USA", "Canada", "Brazil", "Mexico", "Argentina"],
            "EMEA": ["UK", "Germany", "France", "UAE", "South Africa", "Nigeria"],
            "APAC": ["China", "India", "Japan", "Australia", "Singapore", "Vietnam"]
        }
        
    def locate(self, industry, country):
        if not industry:
            return []

        region = self._get_region(country)
        countries = self.country_groups.get(region, [])

        companies = []
        for i in range(5):
            country = random.choice(countries)
            companies.append({
                "name": f"{industry} Company {i+1}",
                "country": country,
                "industry": industry
            })
            
        return companies

    def _get_region(self, country):
        for region, countries in self.country_groups.items():
            if country in countries:
                return region

        return "Global"