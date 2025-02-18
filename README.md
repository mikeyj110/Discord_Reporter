# Discord Reporter

A simple web-based tool that generates CSV reports of messages from a Discord server. The application runs in a Docker container and provides a web UI for selecting a date range and downloading the report.

## Features
- Fetches messages from all text channels in a specified Discord server
- Provides a web UI for selecting the report period
- Generates CSV reports for easy analysis
- Runs in a Docker container for easy deployment

## Prerequisites
- Docker installed on your system
- A Discord bot token with appropriate permissions

## Setup Instructions
### 1. Clone the Repository
```sh
git clone https://github.com/your-username/discord-reporter.git
cd discord-reporter
```

### 2. Configure the Environment Variables
Copy the provided `config.env` file and fill in your bot token and server/guild ID:
```sh
cp config.env.example config.env
```
Edit `config.env` and replace the placeholder values with your actual credentials:
```
DISCORD_TOKEN=your-bot-token-here
DISCORD_GUILD_ID=your-guild-id-here
```

### 3. Build and Run the Docker Container
```sh
docker build -t discord-reporter .
docker run --env-file config.env -p 5000:5000 discord-reporter
```

### 4. Access the Web UI
Open a web browser and go to:
```
http://localhost:5000
```

### 5. Generate and Download Reports
- Select a **Year** and **Month**
- Click **Get Report**
- Download the generated CSV file from the UI

## Notes
- Ensure your bot has **Read Message History** and **View Channels** permissions for all channels.
- Reports are saved inside the `static/` directory within the container.

## License
MIT License.
