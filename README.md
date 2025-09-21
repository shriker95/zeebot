# Zeebot für Twitch

A Bot that has a ai personality and answers your questions in your Twitch Chat. Currently based on MistralAI.

# Setup

* [Register an App on Twitch](https://dev.twitch.tv/docs/authentication/register-app/)
* [Get Mistral Apikey](https://docs.mistral.ai/getting-started/quickstart/#account-setup)
* Setup Service

# INI Template

```
MISTRAL_KEY=""
MISTRAL_MODEL=""
BOT_ID=""
CLIENT_ID=""
CLIENT_SECRET=""
TWITCH_CHANNEL=""
TIMEOUT=
```

# Example systemd unit file

```
[Unit]
Description=zeebot for twitch
After=syslog.target network.target

[Service]
Type=simple
User=twitchbot
WorkingDirectory=/opt/zeebot
ExecStart=/opt/zeebot/bin/python3 /opt/zeebot/bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```
