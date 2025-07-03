
import re
import requests
from bs4 import BeautifulSoup
from .helpers import rand_delay

class EmailFinder:
    def find_email(self, domain, departments):
        if not domain:
            return {}
        
        emails = self._scrape_contacts(domain, departments)

        for dept in departments:
            if dept not in emails or not emails[dept]:
                emails[dept] = [f"{dept}@{domain}"]

        return emails
    
    def _scrape_contacts(self, domain, departments):
        results = {dept: [] for dept in departments}
        urls = [
            f"https://{domain}/contact",
            f"https://{domain}/about",
            f"https://{domain}/careers",
            f"https://{domain}/support"
        ]
        
        for url in urls:
            try:
                rand_delay()
                response = requests.get(url, timeout=5)
                soup = BeautifulSoup(response.text, 'html.parser')
                text = soup.get_text()

                emails_found = re.findall(
                    r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
                    text
                )
                
                for email in emails_found:
                    for dept in departments:
                        if dept in email.split("@")[0].lower():
                            results[dept].append(email)
                            
            except:
                continue

        return results