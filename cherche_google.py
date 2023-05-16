# %%
import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from itertools import islice
import winsound
import datetime

from domaines import UNIVERSITES_FR, EPST, UNIVERSITES_HORS_FR
from requetes import MCFX, MAITREX, CHERCHEUX, ENSEIGNANTX, PROFESSEURX, ETUDIANTX,  DOCTORANTX

# Domaînes et requêtes sélectionnés:
domaines = UNIVERSITES_FR
requetes = MCFX + MAITREX + CHERCHEUX + ENSEIGNANTX + PROFESSEURX + ETUDIANTX + DOCTORANTX

# Racine pour le nom du fichier excel (racine_YYYY_MM_DD.xls) 
racine = 'res_raw'

# Pour reprendre une recherche après arret (reprise=5 : les recherches commencent au 5e domaine) 
reprise = 1

# %%
def recherche(requetes, domaines, reprise):
    # initialise le tableau de résulats
    results = np.zeros((len(domaines)-reprise+1, len(requetes)))

    driver = webdriver.Chrome(executable_path="./chromedriver.exe") 
    driver.get('https://www.google.com')
    driver.find_element(By.XPATH, '//*[@id="L2AGLb"]').click()

    for i, nom in enumerate(islice(domaines, reprise-1, len(domaines), 1)):

        print(f"### {nom} / {domaines[nom]}")
        for j, req in enumerate(requetes):
            search = driver.find_element(By.NAME, "q")
            search.send_keys(f"{req} site:{domaines[nom]}") 
            search.send_keys(Keys.RETURN)
            try:
                result = driver.find_element(By.XPATH, '//*[@id="result-stats"]')
            except:
                winsound.Beep(440, 500)
                _ = input('Google stoppe la recherche: prouve que tu n\'es pas un.e robot.e, puis presse entrée')
                result = driver.find_element(By.XPATH, '//*[@id="result-stats"]')
            print(f"{req}: {result.text}")
            try:
                results[i,j] = int(result.text.split("Environ")[1].split("résultats")[0].replace(' ','').replace(u'\u202f', ''))
            except:
                results[i,j] = int(result.text.split("résultats")[0].replace(' ','').replace(u'\u202f', ''))
            search = driver.find_element(By.NAME, "q")
            search.clear()
        
        df = pd.DataFrame(results)
        df.columns = [req_.split("\"")[1] for req_ in requetes]
        df.insert(0, 'Nom', [nom_ for nom_ in islice(domaines, reprise-1, len(domaines), 1)])
        df.insert(1, 'Domaine', [domaines[nom_] for nom_ in islice(domaines, reprise-1, len(domaines), 1)])
        df.to_excel(f'{racine}_{str(datetime.date.today())}.xlsx', index=False)

    driver.quit()

if __name__ == "__main__":
    recherche(requetes, domaines, reprise)
     
       
