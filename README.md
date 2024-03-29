<p><a href="https://discord.gg/dz8xBwRa"><img src=https://img.shields.io/badge/Discord_Server-3670a0?style=for-the-badge&logo=discord&logoColor=white></a></p>

# DailyChatBot-Template
A Simple Script To use as a Template for Making Geometry Dash Daily-Chat Bots in a Clean and fun way with Type-hinting for pyright and more...


## Example for making Daily-Chat-Bots
All you have to do is subclass the bot class made. If you understand how to code classes and use the attrs python library this 
will be extremely easy for you to use. Type-hinting has already been provided thanks to `gd.py` by netkit...

You can get really creative with these tools. If you really put your mind to it. The possibilities are endless...

```python
@define(slots=False)
class ExampleBot(Bot):
    """Example Daily Chat Bot, (You can use this as a Template if you really want...)"""
    # NOTE: if you need some globals put them into your attrs class object it's why 
    # I designed it this way...
    my_cache_example_variable:dict = {}
    async def on_comment(self, level: Level, comment: LevelComment):
        # How to get comment's text...
        text = comment.content

        if text.startswith("/echo"):
            echoing = text.strip("/echo")

            test = "@" + comment.author.name + " " + echoing
            # How to reply to a comment 
            # NOTE: I already handled comment-ban-checks in the other class-object...
            await level.comment(test)
```

# How to run your newly made subclassed Bot
## Requirements
1. Get An Email account that hasn't been used to sign-up for a geometry dash account (yet)
2. Sign-up for the account (Preferably over a proxy or vpn if at all possible...)
3. Hold onto the username and password so that the bot can login to the account and start running

## Executing your bot
```python
if __name__ == "__main__":
    # When you've made your own subclass you can use this method to run your bot, 
    # The code will prompt what is needed to be filled out as a bonus...
    ExampleBot(kill_history_on_ban=True, vpn=False).run()
```
Some Premade-settings as shown in this example are here to help you when you run your bot. And I (Calloc) have made it simple but effective to make bots without worrying about the other stuff involved as the other libraries provided take care of everything for you...

## NOTES
- Please Remeber to Use a proxy or VPN Before using the tools I've provided to you, it is very important to have a proxy or VPN because comment-bans are tied to the last IP address used. 
- Using these tools can be seen by the Eldermods as malicious so please use at your own risk! You have been warned! 
- I was inspired by the many hilarious bots I've seen in GD over the many years that I thought it would be nice if I made a library to make it easier than ever to make your own bots that you can deploy with no hassle at all...
- The Bot is designed to shutdown once banned and if you want to resume it you either have to wait out the cooldown or roate to another account if you wish to coninue...

## TODOS
- Make Discordpy Styled Callbacks and Event Wrappers and function-wrappers in the future 


