import discord


class DiscordClient(discord.Client):
    def __init__(self, intents=None):
        if intents is None:
            intents = discord.Intents.default()
        super().__init__(intents=intents)
        self.tree = discord.app_commands.CommandTree(self)

    async def sync_commands(self, guild=None, clear=False):
        if isinstance(guild, int):
            guild = discord.Object(guild)
        if clear:
            self.tree.clear_commands(guild=guild)
        await self.tree.sync(guild=guild)
        print('Commands synced')


client = DiscordClient()

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')


@client.tree.command()
@discord.app_commands.default_permissions(manage_guild=True)
async def sync_commands(interaction: discord.Interaction):
    msg = 'Global commands synced. May take up to an hour to take effect.'
    await client.tree.sync()
    await interaction.response.send_message(msg, ephemeral=True)


async def run(token, sync_commands=False):
    async with client:
        await client.login(token)
        if sync_commands:
            await client.sync_commands()
        await client.connect()


if __name__ == '__main__':
    import asyncio
    asyncio.run(run('', sync_commands=True))
