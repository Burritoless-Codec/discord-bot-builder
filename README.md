
# Discord Bot Designer

Welcome to the **Discord Bot Designer**! This GUI application allows users to create and customize their own Discord bots easily. You can define bot commands, set command prefixes, manage intents, and generate Python code for your bot.

## Features

- Add, edit, and delete commands with responses.
- Option to mention the user in responses.
- Save and load configurations in JSON format.
- Generate Python code for your bot based on the defined settings.

## Requirements

- Python 3.6 or higher
- `tkinter` (comes pre-installed with Python)
- `discord.py` library (for running the bot)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Burritoless-Codec/discord-bot-builder.git
   cd discord-bot-builder
   ```

2. Install the necessary library:

   ```bash
   pip install discord.py
   ```

3. Run the application:

   ```bash
   python bot_designer.py
   ```

## Usage

1. **Enter Bot Token**: Provide your Discord bot's token.
2. **Set Command Prefix**: Define the prefix your bot will respond to (e.g., `!` or `?`).
3. **Select Intents**: Choose the intents your bot will use (e.g., message content, guilds).
4. **Define Commands**:
   - **Command Name**: Enter the name of the command.
   - **Response**: Set the response the bot will send when the command is invoked.
   - **Mention User**: Check this option if you want the bot to mention the user in its response.
   - **Command Type**: Choose between "Simple" and "Advanced" (with embedded messages).
5. **Advanced Options**: If "Advanced" is selected, provide an embed title and color.
6. **Manage Commands**: Use the buttons to add, edit, or delete commands.
7. **Save/Load Configuration**: Save your configuration to a JSON file or load a previously saved configuration.
8. **Generate Bot Code**: Click the button to save the generated Python bot code to a `.py` file.

## Example of Generated Code

Here's an example of what the generated bot code might look like:

```python
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command(name='hello', help='Responds with a greeting')
async def hello(ctx):
    await ctx.send(f'{ctx.author.mention}, Hello!')

bot.run('YOUR_BOT_TOKEN')
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [discord.py](https://discordpy.readthedocs.io/en/stable/) for making it easy to interact with the Discord API.
- [Tkinter](https://docs.python.org/3/library/tkinter.html) for providing the GUI toolkit.


