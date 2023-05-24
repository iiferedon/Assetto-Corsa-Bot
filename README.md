# Assetto-Corsa-Bot
<h3 align="center">Logs join and leave requests in a server via JSON dumping.</h3>

  <p align="center">
    <img src="images/example_discord_bot.png" alt="Logo" >
    <br />
    <a href="https://iiferedon.xyz"><strong>My Website »</strong></a>
    <br />
    <br />
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

Monitor any Assetto Corsa server to check if a player has joined or left the server externally.

<p align="right">(<a href="#top">back to top</a>)</p>



### Built With

* [Discord.py](https://discordpy.readthedocs.io/en/stable/api.html)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

```sh
git clone https://github.com/iiferedon/Assetto-Corsa-Bot.git
cd Assetto-Corsa-Bot/
sudo apt-get update
sudo apt install python3-pip
pip install -r requirements.txt

```

### Installation

1. Create bot
  ```sh
  Fairly obvious just look this up, make sure PRESENCE INTENT, SERVER MEMBERS INTENT, MESSAGE CONTENT INTENT are all checked in the bot section. 
  Create the URL as admin because why not.
  ```
2. edit these
   ```py
    TOKEN = 'BOT_TOKEN' #Bot Token
    GUILD_ID = 1337  # Replace with your Discord server ID
    CHANNEL_ID = 1337 # Replace with your target channel ID
    server_address = "1.3.3.7" #Server Address
    server_port = "1337" #Server Port
   ```
   
<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage
```sh
#Start Script
python3 bot.py
```
<p align="right">(<a href="#top">back to top</a>)</p>




<!-- CONTACT -->
## Contact
Discord - iiferedon#7619 or iiferedon#1337


<p align="right">(<a href="#top">back to top</a>)</p>
