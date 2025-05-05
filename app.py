from flask import Flask, render_template, request, redirect, url_for
from models import get_db, init_db

app = Flask(__name__)

@app.route('/')
def index():
    db = get_db()
    players = db.execute("SELECT * FROM players").fetchall()
    teams = db.execute("SELECT * FROM teams").fetchall()
    return render_template("index.html", players=players, teams=teams)

@app.route('/add_player', methods=["POST"])
def add_player():
    name = request.form['name']
    base_price = request.form['base_price']
    db = get_db()
    db.execute("INSERT INTO players (name, base_price) VALUES (?, ?)", (name, base_price))
    db.commit()
    return redirect(url_for('index'))

@app.route('/add_team', methods=["POST"])
def add_team():
    name = request.form['name']
    db = get_db()
    db.execute("INSERT INTO teams (name) VALUES (?)", (name,))
    db.commit()
    return redirect(url_for('index'))

@app.route('/bid', methods=["POST"])
def bid():
    player_id = request.form['player_id']
    team_id = request.form['team_id']
    amount = int(request.form['amount'])

    db = get_db()
    highest = db.execute("SELECT MAX(amount) as max_bid FROM bids WHERE player_id = ?", (player_id,)).fetchone()
    current_price = db.execute("SELECT base_price FROM players WHERE id = ?", (player_id,)).fetchone()
    if (highest['max_bid'] is None or amount > highest['max_bid']) and amount >= current_price['base_price']:
        db.execute("INSERT INTO bids (player_id, team_id, amount) VALUES (?, ?, ?)", (player_id, team_id, amount))
        db.commit()
    return redirect(url_for('index'))

@app.route('/player/<int:player_id>')
def view_bids(player_id):
    db = get_db()
    player = db.execute("SELECT * FROM players WHERE id = ?", (player_id,)).fetchone()
    bids = db.execute("""
        SELECT bids.amount, teams.name as team_name, bids.timestamp
        FROM bids JOIN teams ON bids.team_id = teams.id
        WHERE bids.player_id = ?
        ORDER BY bids.amount DESC
    """, (player_id,)).fetchall()
    return render_template("bids.html", player=player, bids=bids)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
