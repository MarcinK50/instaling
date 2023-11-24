# instaling
prosty rozwiązywacz [Insta.Ling](https://instaling.pl) w [Selenium](https://www.selenium.dev/) 
# dobra, jak odpalić ten badziew?
to tak, potrzebujesz:
- pythona, najlepiej w wersji 3.11
- firefoxa, program był testowany na wersji 120.0
- geckodriver, można pobrać [stąd](https://github.com/mozilla/geckodriver/releases) (wybrać .zip dla swojego systemu, np. `geckodriver-v0.33.0-win64.zip`)
- dla większej wydajności można pobrać jeszcze mongodb, żeby nie trzeba było wczytywać 20Mb bazy danych słówek z pliku tekstowego, co zużywa całkiem sporo RAMu
# instalacja pythonowych pakietów
w konsoli:
`pip install selenium seleniumwire print_color dotenv pymongo`

teraz wszystkie potrzebne pakiety dla pythona powinny być pobrane
# instalacja geckodriver
plik `geckodriver.exe` z .zip należy przenieść do katalogu, który znajduje się w PATH (zmienne środowiskowe), np. C:\Windows

**po tej czynności można wykonać restart komputera**

# instalacja mongodb
pobrać i uruchomić instalator mongodb [stąd](https://www.mongodb.com/try/download/community-edition)

następnie w cmd uruchamiamy
`mongosh`

i tworzymy bazę danych:
`use instaling`

możemy teraz wyjść z `mongosh`, używając `exit` i zaimportować dane z pliku `remaped_words.json` do kolekcji w mongodb:
`mongoimport --db instaling --collection answers --file remaped_words.json`

teraz wszystko powinno być gotowe do pracy, pozostaje konfiguracja pliku .env

# konfiguracja
kopiujemy plik `.env.example` do pliku `.env` (WAZNE, ZEBY BYL TO PLIK DOKLADNIE `.env`, NIE `.env.txt`, `env.txt`, czy `env`!)

i edytujemy treść zgodnie z swoją konfiguracją
```env
ATLAS_URI=mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.0.2 
DB_NAME=instaling NAZWA BAZY DANYCH
EMAIL=jan123 LOGIN DO INSTALING
PASSWORD=abcde HASLO DO INSTALING
```
przede wszystkim należy zmienić login i hasło do instaling, który został podany przez nauczyciela

kiedy mamy gotowy plik `.env`, możemy uruchomić program

# uruchomienie
w konsoli:
`python main.py`

program powinnien się uruchomić, otwiera się okno firefoxa, skrypt sam loguje się do instaling, zaczyna nową sesję i udziela odpowiedzi

# zglaszanie bledow

jesli znajdziesz jakis blad to zglos go jako issue na karcie wyżej

w przypadku kiedy udalo ci sie jakims cudem zrozumiec co robi ten badziewny kod i poprawic go, tworzac pull requests
