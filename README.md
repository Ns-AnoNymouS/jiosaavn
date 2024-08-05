# JioSaavn Telegram Bot

A Python Telegram bot leveraging the Pyrofork library to search and upload songs, albums, playlists, and artists from JioSaavn. This bot utilizes hidden APIs from JioSaavn to provide a seamless music experience on Telegram.

[![GitHub](https://badgen.net/badge/Open%20Source%20%3F/Yes/yellow?icon=github)](https://github.com/Ns-AnoNymouS/jiosaavn)


## Features

- **Search** for songs, albums, playlists, and artists on JioSaavn.
- **Upload** songs directly to Telegram.
- Supports multiple search types (songs, albums, playlists, artists).

## Usage

1. **Start the Bot**: Send the `/start` command.
2. **Search**: Send a query to search for a song, album, playlist, or artist.
3. **Select**: Choose the desired result from the search list.
4. **Upload**: Select the upload option to upload the song to Telegram.

## Commands

- `/start` - Initialize the bot and check its status.
- `/settings` - Configure and manage bot settings.
- `/help` - Get information on how to use the bot.
- `/about` - Learn more about the bot and its features.

## Installation

1. **Clone the Repository**: 
   ```sh
   git clone https://github.com/Ns-AnoNymouS/jiosaavn.git
   ```
2. **Install Dependencies**:
   ```sh
   pip3 install -r requirements.txt
   ```
3. **Run the Bot**:
   ```sh
   python3 -m jiosaavn
   ```

## Running Methods

1. **Deploy to Heroku**:
   Click the button below to deploy to Heroku.

   [![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/Ns-AnoNymouS/jiosaavn/tree/main)
   
2. **Local Setup**:
   - Ensure you have Python and pip installed.
   - Follow the Installation steps above.

## Dependencies

- [Pyrofork](https://pyrofork.mayuri.my.id/main/)
- Custom JioSaavn API

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License.
