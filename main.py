import discord
import shrew
import config_loader

from discord.ext import tasks, commands
from datetime import datetime

class ShrewCog(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.send_new_shrew.start()
    
    @tasks.loop(minutes=1.0)
    async def send_new_shrew(self):
        if self.client.active:
            now = datetime.now()
            if now.hour == 12 and now.minute == 0:
                # Noon Pacific
                new_shrew = shrew.get_new_shrew()

                if new_shrew:
                    channel = self.client.get_channel(config_loader.channel())

                    try:
                        await channel.send(file=discord.File(new_shrew))
                        shrew.mark_shrew_as_used(new_shrew)
                        print("Sent new shrew")
                    except discord.HTTPException as httpErr:
                        print(f"Failed to send message: {httpErr}")
                    except discord.Forbidden as forbiddenErr:
                        print(f"Improper permissions to send message: {forbiddenErr}")
                    except discord.InvalidArgument as invalidErr:
                        print(f"Invalid message argument: {invalidErr}")
                else:
                    print("No more shrews :(")
        else:
            print("Client not active")

class ShrewClient(discord.Client):
    def __init__(self):
        self.active = False
        super().__init__()

    async def on_ready(self):
        print(f"Logged on as {self.user}")
        self.active = True

def main():
    client = ShrewClient()
    cog = ShrewCog(client)

    client.run(config_loader.client_token())

if __name__ == "__main__":
    main()
