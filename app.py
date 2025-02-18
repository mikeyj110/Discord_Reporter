from flask import Flask, request, render_template, redirect, url_for, send_from_directory, jsonify
import threading
import discord
import csv
from datetime import datetime
import os

app = Flask(__name__)

# Ensure the static directory exists
os.makedirs('static', exist_ok=True)

discord_bot_thread = None

# Store session details in memory (for simplicity, could use a database later)
config = {
    'TOKEN': os.getenv('DISCORD_TOKEN', ''),
    'GUILD_ID': int(os.getenv('DISCORD_GUILD_ID', '0')),
    'YEAR': '',
    'MONTH': '',
    'GUILD_NAME': ''
}

# Fetch Guild Info when the container starts
def fetch_guild_info():
    TOKEN = config['TOKEN']
    GUILD_ID = config['GUILD_ID']
    
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)
    
    @client.event
    async def on_ready():
        guild = client.get_guild(GUILD_ID)
        if guild:
            config['GUILD_NAME'] = guild.name
        await client.close()
    
    client.run(TOKEN)

# Run this function at startup
fetch_guild_info()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        config['YEAR'] = int(request.form['year'])
        config['MONTH'] = int(request.form['month'])
        
        global discord_bot_thread
        if discord_bot_thread is None or not discord_bot_thread.is_alive():
            discord_bot_thread = threading.Thread(target=run_discord_bot, daemon=True)
            discord_bot_thread.start()

        return redirect(url_for('index'))

    return render_template('index.html', config=config)

@app.route('/get_guild_info', methods=['GET'])
def get_guild_info():
    return jsonify({'guild_id': config['GUILD_ID'], 'guild_name': config['GUILD_NAME']})

@app.route('/download/<year>/<month>')
def download_file(year, month):
    filename = f"{year}_{month.zfill(2)}_discord_log.csv"
    file_path = os.path.join('static', filename)
    if os.path.exists(file_path):
        return send_from_directory('static', filename, as_attachment=True)
    else:
        return "File not found", 404

def run_discord_bot():
    TOKEN = config['TOKEN']
    GUILD_ID = config['GUILD_ID']
    YEAR = config['YEAR']
    MONTH = config['MONTH']

    client = discord.Client(intents=discord.Intents.default())

    def get_month_range(year: int, month: int):
        start_date = datetime(year, month, 1)
        end_date = datetime(year + 1, 1, 1) if month == 12 else datetime(year, month + 1, 1)
        return start_date, end_date

    @client.event
    async def on_ready():
        print(f'Logged in as {client.user}')
        guild = client.get_guild(GUILD_ID)
        if guild:
            config['GUILD_NAME'] = guild.name

        start_date, end_date = get_month_range(YEAR, MONTH)
        csv_path = f'static/{YEAR}_{MONTH:02d}_discord_log.csv'
        with open(csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Channel', 'Username', 'Timestamp'])
            for channel in guild.text_channels:
                async for message in channel.history(limit=None, after=start_date, before=end_date):
                    writer.writerow([channel.name, message.author.name, message.created_at])
        print(f'Logs saved at {csv_path}.')
        await client.close()

    client.run(TOKEN)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
