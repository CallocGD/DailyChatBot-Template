from attrs import define
from gd import Client, CommentBanned , MissingAccess , LevelComment, Level



# stdlib...
from abc import abstractmethod
import asyncio
from contextlib import asynccontextmanager
from getpass import getpass
import random
import sys


__version__ = "0.0.1"
__authors__ = ["Calloc"]



# My Library for getting proxy support with gd.py... 
# if you need this script simply copy the module from my github at https://github.com/CallocGD/gdpy-extensions
from gdpy_extensions import ProxyClient

# Bot Made for sevenworks , This Template Was Made by Calloc (ME)

# NOTE: shouldn't be to hard to learn asyncio if you need help dm me  at "calloc." on discord
#  or download VS Code and get pyright extensions... I will be hosting this code template on github...

# Feel free to make pull requests, fork or modify this code it's under an MIT LICENSE for a reason - Calloc


async def comment_delay_sleep():
    """The amount of time to wait before taking more comments in..."""
    return await asyncio.sleep(random.choice(15, 20))



@asynccontextmanager
async def login(vpn:bool = False):
    username = input("GD Username: ")
    password = getpass("GD Password: ")
    proxy_url = input("proxy url (example: socks5://127.0.0.1:5050):") if not vpn else None
    client = ProxyClient(proxy_url=proxy_url) if proxy_url is not None else Client()
    async with client.login(username, password):
        assert client.is_logged_in()
        yield client



@define(slots = False)
class Bot:
    """A DailyChat Bot by Calloc made for easily making 
    dailychat bots..."""
    kill_history_on_ban:bool = True
    """Purges comment history when the bot is banned 
    by an Eldermod thus destorying the evidence..."""
    vpn:bool = False
    """If a Vpn is used, a proxy will not be prompted 
    or required..."""

    
    def login(self):
        """returns an asynchronous context manager along
        with a prompt for logging in that the user needs 
        to fill out..."""
        return login(self.vpn)
    
    async def sleep(self):
        """Used as a smaller sleep incase to prevent 429 
        responses from boomlings..."""
        return await asyncio.sleep(random.uniform(1, 4))

    @abstractmethod
    async def on_comment(self, level:Level, comment:LevelComment):
        """This is a function you need to write for your bot... 
        I've taken care of error-handling when it comes to 
        comment bans - Calloc"""
        pass
    
    async def run_async(self):
        # Globals...
        # NOTE: Don't worry about this function I've taken care of it for you...
        _comment_ids: set[int] = set()
        _new_comment_ids: set[int] = set()

        async with self.login() as client:
            try:
                daily = await client.get_daily(use_client=True) # we enable use_client so we can send comments to the level...
            except MissingAccess:
                print("Error: Daily level is not avalible exiting..")
                sys.exit()

            is_banned = False

            # Loop while we aren't banned...
            while is_banned is False:
                async for comment in daily.get_comments_on_page(count=100):
                    if comment.id not in _comment_ids:
                        try:
                            # Prevents bot from echoing itself... 
                            if comment.author.account_id != client.user.account_id:
                                await self.on_comment(daily, comment)
                            _new_comment_ids.add(comment.id)
                        except CommentBanned:
                            is_banned = True
                            print("Your Bot was banned by an eldermod...")
                            # Exit the comment loop so we can later exit the entire loop...
                            break
                # Reset what was already seen and evaluated...
                _comment_ids = _new_comment_ids
                # Do an emergency exit if we are banned.
                if not is_banned:
                    await comment_delay_sleep()

            if self.kill_history_on_ban:
                print("Purging comment history...")
                print("Comments Purged: 0", end= "\r")
                deleted = 0
                async for comment in client.user.get_comments():
                    await self.sleep()
                    try:
                        await comment.delete()
                        deleted += 1
                        print("Comments Purged: %i" % deleted, end="\r")
                    except:
                        continue
        print("Exiting...")

    def run(self):
        """Starts the Daily-Chat Bot, This bot will exit if it's banned by an eldermod..."""
        asyncio.run(self.run_async())



# TODO: Implement Discord.py Command Wrappers as another external subclass in order to make it easier to parse commands...

@define(slots=False)
class ExampleBot(Bot):
    """Example Daily Chat Bot, (You can use this as a Template if you really want...)"""
    # NOTE: if you need some globals put them into your attrs class object it's why 
    # I designed it this way...
    my_cache:dict = {}
    async def on_comment(self, level: Level, comment: LevelComment):
        # How to get comment's text...
        text = comment.content

        if text.startswith("/echo"):
            echoing = text.strip("/echo")

            test = "@" + comment.author.name + " " + echoing
            # How to reply to a comment 
            # NOTE: I already handled comment-ban-checks in the other class-object...
            await level.comment(test)


if __name__ == "__main__":
    # When you've made your own subclass you can use this method to run your bot, 
    # The code will prompt what is needed to be filled out as a bonus...
    ExampleBot(kill_history_on_ban=True, vpn=False).run()

    # NOTE: If you need proxies, download the proxy list from Sevenwork's github and then use my tool 
    # (https://github.com/CallocGD/Probe) to hunt down unbanned and alive proxies or the harder way which 
    # is using this script with a VPN Running...




