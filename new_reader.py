import os
import re
import json
import time
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter

# 📌 Percorsi dei file
SCREENSHOT_FOLDER = r'C:\Users\marci\Pictures\Screenshots'
GITHUB_PAGES_FOLDER = r'C:\Users\marci\Documents\Marvel_rivals_ocr'
JSON_OUTPUT_PATH = os.path.join(GITHUB_PAGES_FOLDER, 'usernames.json')

def process_screenshot(image_path):
    """ Estrai il testo dallo screenshot usando OCR. """
    image = Image.open(image_path)
    image = image.convert('L')  # Scala di grigi
    image = ImageEnhance.Contrast(image).enhance(2)  # Aumenta contrasto
    image = image.filter(ImageFilter.MedianFilter(3))  # Riduzione rumore
    text = pytesseract.image_to_string(image, lang='eng', config='--psm 6')
    return text

def extract_usernames(raw_text):
    """ Estrai i nomi utente dal testo OCR. """
    pattern = re.compile(r'^(\d{2})\s+([\w\s\-\.,;:\'\"!?]+)$')
    usernames = [match.group(2).strip() for line in raw_text.splitlines() if (match := pattern.match(line))]
    return usernames

def save_to_json(data, file_path):
    """ Salva i dati in formato JSON. """
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"✅ Dati salvati in: {file_path}")

def commit_and_push_changes():
    """ Esegue il commit e il push automatico su GitHub. """
    os.chdir(GITHUB_PAGES_FOLDER)  # Spostati nella cartella GitHub Pages
    
    print("📌 Eseguo `git status` per controllare le modifiche...")
    os.system("git status")

    print("📌 Aggiungo `usernames.json` a Git...")
    os.system("git add usernames.json")

    print("📌 Eseguo il commit...")
    commit_result = os.system('git commit -m "Aggiornamento automatico usernames.json"')

    if commit_result == 0:  # Se il commit ha successo
        print("📌 Eseguo il push su GitHub...")
        push_result = os.system("git push origin main")  # Assicurati che il branch sia corretto
        
        if push_result == 0:
            print("✅ Dati caricati su GitHub con successo!")
        else:
            print("❌ Errore nel push. Controlla le credenziali Git.")
    else:
        print("⚠️ Nessuna modifica da committare.")

def main():
    last_processed = None

    while True:
        # 📌 Trova gli screenshot disponibili
        files = [os.path.join(SCREENSHOT_FOLDER, f) for f in os.listdir(SCREENSHOT_FOLDER)
                 if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        if not files:
            print("📷 Nessuno screenshot trovato. Attendo...")
            time.sleep(5)
            continue

        # 📌 Seleziona l'ultimo screenshot
        latest_file = max(files, key=os.path.getmtime)

        # 🔄 Se non è un nuovo screenshot, stampa comunque i dati esistenti
        if last_processed == latest_file:
            print("🔄 Nessun nuovo screenshot, ma stampo comunque i nomi estratti:")
            with open(JSON_OUTPUT_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print("👥 Nomi utente:", data.get("usernames", []))
        else:
            print("📸 Elaboro nuovo screenshot:", latest_file)
            ocr_text = process_screenshot(latest_file)
            usernames = extract_usernames(ocr_text)

            # 📌 Genera i dati aggiornati
            data = {
                "usernames": usernames, 
                "urls": [f"https://tracker.gg/marvel-rivals/profile/ign/{username}/heroes?mode=competitive&season=2" for username in usernames]
            }

            # 📌 Stampa sempre i nomi trovati
            print("\n👥 Nomi utente estratti:", usernames)

            # 📌 Salva i dati in JSON e caricali su GitHub
            save_to_json(data, JSON_OUTPUT_PATH)
            commit_and_push_changes()

            last_processed = latest_file

        time.sleep(5)

if __name__ == "__main__":
    main()
