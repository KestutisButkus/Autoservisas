# Autoservisas

**Autoservisas** yra Django pagrindu sukurta web aplikacija, skirta automobilių serviso paslaugų valdymui. Šis projektas leidžia valdyti klientų užsakymus, automobilių informaciją, paslaugas ir užsakymų eiles per intuityvią administracinę sąsają.

## Funkcionalumas

- **Klientų ir automobilių registracija:** Galimybė registruoti naujus klientus ir jų automobilius.
- **Užsakymų valdymas:** Sukurti ir valdyti užsakymus, priskirti paslaugas bei stebėti užsakymų būklę.
- **Paslaugų katalogas:** Įtraukti ir redaguoti serviso teikiamas paslaugas.
- **Užsakymų eilių valdymas:** Stebėti paslaugų atlikimo eiles ir jų statusą.
- **Paieškos ir filtravimo funkcionalumas:** Lengvai rasti automobilius ir užsakymus pagal įvairius kriterijus.

## Naudojamos technologijos

- **Python/Django:** Pagrindinė projekto platforma.
- **SQLite:** Duomenų bazės valdymui (galima pakeisti į kitą DBVS, pvz., PostgreSQL).
- **HTML/CSS/JavaScript:** Fronto sąsajos kūrimui.
- **Django Admin:** Įrankis administracinei sąsajai valdyti.
- **TinyMCE arba CKEditor:** Teksto redaktorius aprašymams valdyti.

## Diegimo instrukcija

1. **Klonuokite repozitoriją:**
    ```sh
    git clone https://github.com/vartotojas/autoservisas.git
    ```

2. **Įjunkite virtualią aplinką:**
    ```sh
    python -m venv venv
    source venv/bin/activate  # Linux/MacOS
    venv\Scripts\activate  # Windows
    ```

3. **Įdiekite priklausomybes:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Atlikite migracijas ir paleiskite serverį:**
    ```sh
    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver
    ```

5. **Aplankykite programą naršyklėje:**
    ```plaintext
    http://127.0.0.1:8000/
    ```
