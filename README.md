# WhiteFly - Projekt Rekrutacyjny

Aplikacja full-stack demonstrująca nowoczesną architekturę webową, kolejkowanie zadań oraz konfigurację proxy. Projekt został skonteneryzowany przy użyciu Docker i wdrożony na platformie Render.

Aplikacja jest dostępna pod adresem: [https://whitefly.onrender.com](https://whitefly.onrender.com)

**Disclaimer** Serwer na Render jest usypiany, gdy nie jest wykorzystywany przez pewien okres czasu, dlatego wejście na stronę, gdy serwer jest uśpiony, wymaga trochę więcej czasu (serwer musi się rozbudzić), po rozbudzeniu, interakcja z stroną powinna przebiegać sprawnie



---

## Architektura 

Projekt realizuje architekturę wielowarstwową zgodnie z wymaganiami:

*   **Reverse Proxy:** Nginx (nasłuchuje na porcie 80).
*   **Zadanie 1 (WSGI):** Aplikacja Flask uruchomiona przez Gunicorn.
*   **Zadanie 2 (ASGI):** Aplikacja FastAPI uruchomiona przez Uvicorn.
*   **Kolejka zadań:** Celery z brokerem Redis.
*   **Baza danych:** SQLite3 do trwałego przechowywania rejestracji użytkowników.
*   **Wdrożenie:** Kontener Docker na platformie Render.com.

### Mapowanie Endpointów (Reguły Proxy):
*   `/flask/*` -> Przekierowanie do Flask (Port 5000)
*   `/fastapi/*` -> Przekierowanie do FastAPI (Port 8000)

---

## Realizacja Zadań

### Zadanie 1: Flask & Celery
*   Stworzono formularz rejestracyjny przyjmujący imię i nazwisko.
*   Zaimplementowano worker Celery do obsługi zapisu do bazy danych w tle.
*   **Endpointy:** `/flask/sync` oraz `/flask/async` 

### Zadanie 2: FastAPI
*   Stworzono wydajne API do sprawdzania statusu i operacji asynchronicznych.
*   **Endpointy:** `/fastapi/sync` oraz `/fastapi/async`

### Zadanie 3: Proxy & Wydajność
*   Skonfigurowano Nginx jako Reverse Proxy, łączący obie aplikacje pod jednym adresem IP.
*   Serwer - Render
*   Architektura została przygotowana pod testy obciążeniowe (k6/loader.io).
*   Wynik testu wydajnościowego znajduje się w katalogu testk6

### Zadanie 4: Ochrona przed botami
W celu ograniczenia fałszywych rejestracji znalazłem i proponuję następujące metody:
(Zaimplementowałem je także, znajduje się to w katalogu task4, ale zrobiłem to tylko jako przykład, nie podpinałem tego i nie testowałem na serwerze)

1.  **Metoda Honeypot:** Do formularza dodano pole tekstowe, które jest całkowicie niewidoczne dla użytkownika dzięki stylom CSS. Boty automatycznie skanujące kod HTML zazwyczaj wypełniają wszystkie znalezione pola. Jeśli serwer otrzyma żądanie z wypełnionym polem "pułapką", system natychmiast klasyfikuje je jako atak i odrzuca wniosek przed zapisaniem go w bazie. 
2.  **Rate Limiting (Ograniczanie liczby żądań):** System mierzy czas, jaki upłynął od momentu wyświetlenia formularza do jego wysłania. Ponieważ boty przesyłają dane niemal natychmiast po załadowaniu kodu strony, wprowadzenie minimalnego progu czasowego (np. 2 sekundy) pozwala odsiać nienaturalnie szybkie interakcje, które są niemożliwe do wykonania przez człowieka.
3.  **Weryfikacja Fingerprinting:** Przy każdym załadowaniu formularza generowany jest unikalny identyfikator (token), który jest przypisywany do konkretnej sesji użytkownika i przesyłany w ukrytym polu. Serwer przyjmuje dane tylko wtedy, gdy token z formularza zgadza się z tym zapisanym w sesji, a po udanej rejestracji token jest natychmiast unieważniany. Uniemożliwia to botom wielokrotne uderzanie bezpośrednio w endpoint bez fizycznego wejścia na stronę.

---

