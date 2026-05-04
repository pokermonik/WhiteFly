from flask import Flask, render_template, request, session
from shared.database import save_to_db, init_db
import time
import uuid

app = Flask(__name__)
app.secret_key = 'super_tajny_klucz_rekrutacyjny' # Potrzebne do sesji, oczywiscie w produkcji powinno być bezpieczniejsze i przechowywane w zmiennych środowiskowych
init_db()

@app.route('/sync', methods=['GET', 'POST'])
def sync_login():
    if request.method == 'POST':
        # --- ZABEZPIECZENIE 1: HONEYPOT ---
        if request.form.get('email_confirm'):
            return "Wykryto bota (Honeypot)!", 400

        # --- ZABEZPIECZENIE 2: TIME-LOCK ---
        current_time = time.time()
        load_time = float(request.form.get('load_timestamp', 0))
        if current_time - load_time < 2.0:
            return "Wysłano zbyt szybko!", 400

        # --- ZABEZPIECZENIE 3: DYNAMICZNY TOKEN (CSRF) ---
        # Sprawdzamy czy token z formularza zgadza się z tym w sesji
        user_token = request.form.get('security_token')
        if not user_token or user_token != session.get('form_token'):
            return "Błędny token bezpieczeństwa!", 403

        # Po udanej weryfikacji usuwamy token, by nie został użyty ponownie
        session.pop('form_token', None)
        # główna logika
        name = request.form['name']
        surname = request.form['surname']
        save_to_db(name, surname)
        return f"Dane zapisano bezpiecznie, {name} {surname}"
    
    # Generujemy nowy token przy każdym wejściu na stronę
    token = str(uuid.uuid4())
    session['form_token'] = token
    
    return render_template('sync.html', current_time=time.time(), token=token)