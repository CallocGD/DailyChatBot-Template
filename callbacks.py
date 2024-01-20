"""
Callbacks
---------
By Calloc

A library for writing bots with Discord.py styled writing and commands
This will eventually replace the Current Template.
"""

from typing import Callable, Generic, TypeVar, Awaitable, Any, get_args, Union, Optional
import inspect
import shlex
import asyncio

SenderT = TypeVar("SenderT")
"""used to make an author variable"""
BotT = TypeVar("BotT")
"""Bot's context carrier..."""


class Command(Generic[BotT, SenderT]):
    """Used for defining a command and it is inspired by discord's Version"""
    def __init__(
        self, ctx: BotT, func: Callable[[BotT, SenderT], Awaitable[None]], name: str = None
    ) -> None:
        self.name = name or func.__name__
        self.sig = inspect.signature(func)
        self.ctx = ctx

        # TODO: ADD BANNED ANNOTATIONS OPTION!
        # get rid of banned parameters...
        annotations = func.__annotations__
        annotations.popitem("ctx")
        annotations.popitem("comment")
        self.annotations: dict[str, Callable[[str], Any]] = annotations
        self.order = list(self.annotations.items())
        self.func = func

    def parse_cmd(self, text: str) -> dict[str, Any]:
        """Converts text into keywords to be loaded into the function chosen
        This will skip undetectable items by default..."""
        params = shlex.split(text)
        missing = list(self.annotations.keys())
        kw = {}
        args = []
        flagged = False
        listed = False
        conv = key = None
        for i in params:
            if i in missing:
                conv = self.annotations[i]
                if conv in [list, tuple]:
                    conv = get_args(self.sig.parameters[i].annotation)[0]
                    listed = True
                    kw[i] = []
                elif conv == Optional:
                    conv = get_args(self.sig.parameters[i].annotation)[0]
                elif conv == Any:
                    conv = str
                key = i
                missing.remove(i)
                flagged = True
            elif listed:
                kw[i].append(conv(i))
            elif flagged:
                if not conv:
                    args.append(i)
                    continue
                # Remove flag after variable has been set...
                kw[key] = conv(i)
                flagged = False
            else:
                args.append(i)

        key = greedy = None
        _previous = None
        if not missing:
            return kw
        # Handle missing arguments
        for a in args:
            if not greedy:
                key = missing.pop(0)
                value = self.annotations[key]
            elif greedy:
                kw[_previous].append(greedy(a))
                continue
            if value == list:  # we have a greedy argument
                conv = get_args(self.sig.parameters[key].annotation)[0]
                greedy = conv
                _previous = key
            else:
                kw[key] = conv(a)
        return kw

    async def invoke(self,author:SenderT, text: str):
        """Attempts to parse and run a given command"""
        keywords = self.parse_cmd(text)
        return await self.func(self.ctx, author, **keywords)





class Context:
    """Bot's Context tools, This can be used for anything beyond gd...

    Parameters
    ----------
    prefixes: `Union[str, list[str]]`: one or more prefixes to use to describe your bot
    """

    def __init__(self, prefixes: Union[list[str], str] = "/") -> None:
        self.prefixes = prefixes
        self.commands: dict[str, Command[Context]] = {}

    def command(
        self, func: Callable[["Context"], Awaitable[None]], name: Optional[str] = None
    ):
        """Used to write clean/organized commands..."""
        assert asyncio.iscoroutinefunction(func), f"{func.__name__} is not asynchronous"
        cmd = Command(self, func, name)
        for p in self.prefixes:
            cmd_name = p + cmd.name
            if cmd_name in self.commands.keys():
                raise RuntimeError(f"{cmd_name} was already written")
            self.commands[p + cmd.name] = cmd
        return func

    def event(
        self, func: Callable[["Context"], Awaitable[None]], name: Optional[str] = None
    ):
        """Used to write a callable event, Events are the same as gd.py"""
        assert asyncio.iscoroutinefunction(func), f"{func.__name__} is not asynchronous"
        event_name = name or func.__name__
        self.__setattr__(event_name, func)
        return func

    async def read_comment(self, author:SenderT, comment:str):
        """Reads all data collected and checks for commands to run..."""
        
        start, end = comment[1].split(" ", 1)
        cmd = self.commands.get(start)
        # Continue if we have nothing...
        if not cmd:
            return
        # otherwise do this...
        try:
            return await cmd.invoke(author, end)
        except Exception as e:
            print(e)
                
    async def main(self) -> None:
        """The main asynchronous function"""
        raise NotImplementedError("main() function wasn't implemented")
    
    def run(self):
        """Runs your bot"""
        raise NotImplementedError("run() wasn't implemented")




# bot = Context("/")
# @bot.command
# async def add(x: int, y: int):
#     print(f"Answer {x + y}")
