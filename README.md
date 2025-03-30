# JioSaavn Telegram Bot

𝘈 𝘗𝘺𝘵𝘩𝘰𝘯 𝘛𝘦𝘭𝘦𝘨𝘳𝘢𝘮 𝘣𝘰𝘵 𝘭𝘦𝘷𝘦𝘳𝘢𝘨𝘪𝘯𝘨 𝘵𝘩𝘦 𝘗𝘺𝘳𝘰𝘧𝘰𝘳𝘬 𝘭𝘪𝘣𝘳𝘢𝘳𝘺 𝘵𝘰 𝘴𝘦𝘢𝘳𝘤𝘩 𝘢𝘯𝘥 𝘶𝘱𝘭𝘰𝘢𝘥 𝘴𝘰𝘯𝘨𝘴, 𝘢𝘭𝘣𝘶𝘮𝘴, 𝘱𝘭𝘢𝘺𝘭𝘪𝘴𝘵𝘴, 𝘢𝘯𝘥 𝘢𝘳𝘵𝘪𝘴𝘵𝘴 𝘧𝘳𝘰𝘮 𝘑𝘪𝘰𝘚𝘢𝘢𝘷𝘯. 𝘛𝘩𝘪𝘴 𝘣𝘰𝘵 𝘶𝘵𝘪𝘭𝘪𝘻𝘦𝘴 𝘩𝘪𝘥𝘥𝘦𝘯 𝘈𝘗𝘐𝘴 𝘧𝘳𝘰𝘮 𝘑𝘪𝘰𝘚𝘢𝘢𝘷𝘯 𝘵𝘰 𝘱𝘳𝘰𝘷𝘪𝘥𝘦 𝘢 𝘴𝘦𝘢𝘮𝘭𝘦𝘴𝘴 𝘮𝘶𝘴𝘪𝘤 𝘦𝘹𝘱𝘦𝘳𝘪𝘦𝘯𝘤𝘦 𝘰𝘯 𝘛𝘦𝘭𝘦𝘨𝘳𝘢𝘮.

[![GitHub](https://badgen.net/badge/Open%20Source%20%3F/Yes/yellow?icon=github)](https://github.com/Ns-AnoNymouS/jiosaavn)

![GitHub contributors](https://img.shields.io/github/contributors/biisal/biisal-file-stream-pro?style=flat&color=green)
![GitHub repo size](https://img.shields.io/github/repo-size/biisal/biisal-file-stream-pro?color=green)
![GitHub](https://img.shields.io/github/license/biisal/biisal-file-stream-pro?color=green)

**Here is our Demo bot -**

[![Click Here](https://img.shields.io/badge/Demo%20Bot-Click%20Here-blue?style=flat&logo=telegram&labelColor=white&link=https://t.me/amcdevsupport)](https://t.me/JiosaavnNsbot)


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


<b>Config Variables :</b>
create a file .env with the following keys
```py
API_ID=12345
API_HASH=esx576f8738x883f3sfzx83
BOT_TOKEN=Your_Bot_Token
PORT=8080
OWNER_ID=your_user_id
DATABASE_URL=mongodb_uri
```

`API_ID` : Goto [my.telegram.org](https://my.telegram.org) to obtain this.

`API_HASH` : Goto [my.telegram.org](https://my.telegram.org) to obtain this.
  
`BOT_TOKEN` : Get the bot token from [@BotFather](https://telegram.dog/BotFather)  

`OWNER_ID` : Your Telegram User ID

`PORT` : The port that you want your webapp to be listened to. Defaults to `8080`

`DATABASE_URL` : MongoDB URI for saving User IDs when they first Start the Bot. We will use that for Broadcasting to them. I will try to add more features related with Database. If you need help to get the URI you can click on logo below!

<a href="https://www.youtube.com/watch?v=HhHzCfrqsoE"><img alt="mongodb" src="./assets/mongo.png" style="border-radius: 50%; height: 100px; width: 100px"></a>

   
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
