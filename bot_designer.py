import tkinter as tk
from tkinter import messagebox, filedialog
import json


class BotDesigner:
    def __init__(self, master):
        self.master = master
        self.master.title("Discord Bot Designer")

        # Instructions
        instructions = tk.Label(master, text="Welcome to the Discord Bot Designer!\n"
                                             "Fill in the fields below to create a bot script.\n"
                                             "You can save your configuration and load it later.", wraplength=300)
        instructions.grid(row=0, columnspan=2, padx=10, pady=10)

        # Bot Token
        tk.Label(master, text="Bot Token:").grid(row=1, column=0)
        self.token_entry = tk.Entry(master, width=50)
        self.token_entry.grid(row=1, column=1)

        # Command Prefix
        tk.Label(master, text="Command Prefix:").grid(row=2, column=0)
        self.prefix_entry = tk.Entry(master, width=10)
        self.prefix_entry.grid(row=2, column=1)

        # Intents Selection
        tk.Label(master, text="Select Intents:").grid(row=3, column=0)
        self.intents = {
            'message_content': tk.BooleanVar(value=True),  # Default to True for easy access
            'members': tk.BooleanVar(),
            'guilds': tk.BooleanVar(),
            'reactions': tk.BooleanVar(),
            'typing': tk.BooleanVar()
        }
        for i, (name, var) in enumerate(self.intents.items()):
            tk.Checkbutton(
                master,
                text=name.replace('_', ' ').capitalize(),
                variable=var
            ).grid(row=4+i, column=0, sticky='w')

        # Commands Section
        tk.Label(master, text="Commands:").grid(row=9, column=0)
        self.command_list = []
        self.command_listbox = tk.Listbox(master, width=80, height=10)
        self.command_listbox.grid(row=9, column=1, columnspan=2)

        # Command Input Fields
        tk.Label(master, text="Command Name:").grid(row=10, column=0)
        self.command_name_entry = tk.Entry(master, width=20)
        self.command_name_entry.grid(row=10, column=1)

        tk.Label(master, text="Response:").grid(row=11, column=0)
        self.response_entry = tk.Entry(master, width=50)
        self.response_entry.grid(row=11, column=1)

        # Mention User Option
        self.mention_user_var = tk.BooleanVar()
        tk.Checkbutton(master, text="Mention User", variable=self.mention_user_var).grid(row=12, column=0, sticky='w')

        # Command Type Selection
        self.command_type_var = tk.StringVar(value="Simple")
        tk.Label(master, text="Command Type:").grid(row=12, column=1)
        tk.Radiobutton(
            master,
            text="Simple",
            variable=self.command_type_var,
            value="Simple"
        ).grid(row=13, column=1, sticky='w')
        tk.Radiobutton(
            master,
            text="Advanced",
            variable=self.command_type_var,
            value="Advanced"
        ).grid(row=14, column=1, sticky='w')

        # Advanced Options (initially hidden)
        self.advanced_options_frame = tk.Frame(master)
        self.advanced_options_frame.grid(row=15, column=0, columnspan=3, sticky='w')
        tk.Label(self.advanced_options_frame, text="Embed Title:").grid(row=0, column=0)
        self.embed_title_entry = tk.Entry(self.advanced_options_frame, width=50)
        self.embed_title_entry.grid(row=0, column=1)

        tk.Label(self.advanced_options_frame, text="Embed Color:").grid(row=1, column=0)
        self.embed_color_entry = tk.Entry(self.advanced_options_frame, width=20)
        self.embed_color_entry.grid(row=1, column=1)

        # Buttons for Command Management
        tk.Button(master, text="Add Command", command=self.add_command).grid(row=16, column=0)
        tk.Button(master, text="Edit Command", command=self.edit_command).grid(row=16, column=1)
        tk.Button(master, text="Delete Command", command=self.delete_command).grid(row=16, column=2)

        # Save and Load Buttons
        tk.Button(master, text="Save Configuration", command=self.save_config).grid(row=17, column=0)
        tk.Button(master, text="Load Configuration", command=self.load_config).grid(row=17, column=1)
        tk.Button(master, text="Generate Bot Code", command=self.save_bot_code).grid(row=17, column=2)

        # Status Label
        self.status_label = tk.Label(master, text="", fg="green")
        self.status_label.grid(row=18, columnspan=3)

        self.command_type_var.trace("w", self.update_advanced_options_visibility)

    def update_advanced_options_visibility(self):

        if self.command_type_var.get() == "Advanced":
            self.advanced_options_frame.grid()
        else:
            self.advanced_options_frame.grid_remove()

    def add_command(self):
        command_name = self.command_name_entry.get()
        response = self.response_entry.get()

        if command_name:
            command = {
                'name': command_name,
                'response': response,
                'mention_user': self.mention_user_var.get(),
                'type': self.command_type_var.get(),
                'embed_title': self.embed_title_entry.get() if self.command_type_var.get() == "Advanced" else None,
                'embed_color': self.embed_color_entry.get() if self.command_type_var.get() == "Advanced" else None,
            }
            self.command_list.append(command)
            self.update_command_listbox()
            self.clear_command_inputs()
            self.status_label.config(text=f"Added command: {command_name}")
        else:
            messagebox.showwarning("Input Error", "Command name cannot be empty.")

    def update_command_listbox(self):
        self.command_listbox.delete(0, tk.END)
        for command in self.command_list:
            self.command_listbox.insert(tk.END, command['name'])

    def clear_command_inputs(self):
        self.command_name_entry.delete(0, tk.END)
        self.response_entry.delete(0, tk.END)
        self.mention_user_var.set(False)
        self.embed_title_entry.delete(0, tk.END)
        self.embed_color_entry.delete(0, tk.END)
        self.command_type_var.set("Simple")
        self.update_advanced_options_visibility()

    def edit_command(self):
        selected_index = self.command_listbox.curselection()
        if selected_index:
            command = self.command_list[selected_index[0]]
            self.command_name_entry.delete(0, tk.END)
            self.command_name_entry.insert(0, command['name'])
            self.response_entry.delete(0, tk.END)
            self.response_entry.insert(0, command['response'])
            self.mention_user_var.set(command.get('mention_user', False))
            self.command_type_var.set(command.get('type', "Simple"))
            self.embed_title_entry.delete(0, tk.END)
            self.embed_title_entry.insert(0, command.get('embed_title', ''))
            self.embed_color_entry.delete(0, tk.END)
            self.embed_color_entry.insert(0, command.get('embed_color', ''))
            self.update_advanced_options_visibility()

    def delete_command(self):
        selected_index = self.command_listbox.curselection()
        if selected_index:
            command_name = self.command_list[selected_index[0]]['name']
            del self.command_list[selected_index[0]]
            self.update_command_listbox()
            self.status_label.config(text=f"Deleted command: {command_name}")

    def generate_bot_code(self):
        token = self.token_entry.get()
        prefix = self.prefix_entry.get()
        intents = "intents = discord.Intents.default()\n"
        if self.intents['message_content'].get():
            intents += "intents.message_content = True\n"
        if self.intents['members'].get():
            intents += "intents.members = True\n"
        if self.intents['guilds'].get():
            intents += "intents.guilds = True\n"
        if self.intents['reactions'].get():
            intents += "intents.reactions = True\n"
        if self.intents['typing'].get():
            intents += "intents.typing = True\n"

        bot_code = "import discord\n"
        bot_code += "from discord.ext import commands\n\n"
        bot_code += intents + f"bot = commands.Bot(command_prefix='{prefix}', intents=intents)\n\n"

        for command in self.command_list:
            command_name = command['name']
            command_response = command['response']
            mention_user = command.get('mention_user', False)

            command_code = f"@bot.command(name='{command_name}', help='{command_response}')\n"
            command_code += f"async def {command_name}(ctx):\n"

            if mention_user:
                command_code += f"    await ctx.send(f'{{ctx.author.mention}}, {command_response}')\n"
            else:
                command_code += f"    await ctx.send('{command_response}')\n"

            if command['type'] == "Advanced" and command['embed_title']:
                command_code += \
                    f"    embed = discord.Embed(title='{command['embed_title']}', color={command['embed_color']})\n"
                command_code += f"    embed.description = '{command_response}'\n"
                command_code += f"    await ctx.send(embed=embed)\n"

            bot_code += command_code + "\n"

        bot_code += f"bot.run('{token}')\n"
        return bot_code

    def save_bot_code(self):
        bot_code = self.generate_bot_code()
        if bot_code:
            file_path = filedialog.asksaveasfilename(defaultextension=".py",
                                                     filetypes=[("Python files", "*.py")])
            if file_path:
                with open(file_path, 'w') as f:
                    f.write(bot_code)
                messagebox.showinfo("Success", "Bot code saved successfully!")

    def save_config(self):
        config = {
            'token': self.token_entry.get(),
            'prefix': self.prefix_entry.get(),
            'intents': {key: var.get() for key, var in self.intents.items()},
            'commands': self.command_list
        }
        file_path = filedialog.asksaveasfilename(defaultextension=".json",
                                                 filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'w') as f:
                json.dump(config, f, indent=4)
            messagebox.showinfo("Success", "Configuration saved successfully!")

    def load_config(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'r') as f:
                config = json.load(f)
                self.token_entry.delete(0, tk.END)
                self.token_entry.insert(0, config['token'])
                self.prefix_entry.delete(0, tk.END)
                self.prefix_entry.insert(0, config['prefix'])
                for key, var in self.intents.items():
                    var.set(config['intents'].get(key, False))
                self.command_list = []
                for command in config['commands']:
                    command.setdefault('type', 'Simple')
                    self.command_list.append(command)
                self.update_command_listbox()
                messagebox.showinfo("Success", "Configuration loaded successfully!")


if __name__ == "__main__":
    root = tk.Tk()
    bot_designer = BotDesigner(root)
    root.mainloop()
