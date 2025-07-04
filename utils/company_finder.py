import requests
from bs4 import BeautifulSoup
from .helpers import rand_delay

class CompanyFinder:
    def find(self, company_name):
        api_res = self._api_find(company_name)

        if api_res:
            return api_res
        
        return self._google_find(company_name)
    
    def _api_find(self, name):
        try:
            response = requests.get(
                f"https://autocomplete.clearbit.com/v1/companies/suggest?query={name}",
                timeout=5
            )
            
            if response.status_code == 200 and response.json():
                match = response.json()[0];
                return {
                    "name": match["name"],
                    "domain": match["domain"],
                    "logo": match["logo"],
                    "industry": match.get("industry", "")
                }
        
        except:
            return None
        
    def _google_find(self, name):
        try:
            rand_delay()
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(
                f"https://www.google.com/search?q={name}+company",
                headers=headers
            )
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            domain = ""
            for a in soup.select("a"):
                href = a.get("href", "")
                if "url?q=" in href and "google" not in href:
                    domain = href.split("url?q=")[1].split("&")[0]
                    break
                
            return {
                "name": name,
                "domain": domain,
                "industry": "Unknown"
            }
            
        except:
            return {
                "name": name,
                "domain": "",
                "industry": "Unknown"
            }