# Import necessary libraries for the GUI application
import tkinter as tk  # Main GUI library for creating windows and widgets
from tkinter import ttk, messagebox  # ttk = themed widgets, messagebox = popup dialogs
from player_manager import PlayerManager  # Our custom class for managing players
from race_manager import RaceManager  # Our custom class for managing races
from datetime import datetime  # For handling dates and times

# Main GUI class that creates and manages the entire application interface
class EloGUI:
    def __init__(self, root):
        # Store reference to the main window
        self.root = root
        
        # Set window properties
        self.root.title("🏁 Trackmania Elo System")  # Window title with emoji
        self.root.geometry("1000x700")  # Window size: width x height in pixels
        self.root.configure(bg='#2b2b2b')  # Dark gray background color (hex color code)
        
        # Configure modern dark theme styling for all GUI elements
        self.style = ttk.Style()  # Create a style object to customize widget appearance
        self.style.theme_use('clam')  # Use 'clam' theme as base (modern looking)
        
        # Configure colors and appearance for different widget types
        # TNotebook = the tab container at the top
        self.style.configure('TNotebook', background='#2b2b2b', borderwidth=0)
        
        # TNotebook.Tab = individual tabs (Players, Add Race, etc.)
        self.style.configure('TNotebook.Tab', background='#404040', foreground='white', 
                           padding=[20, 10], focuscolor='none')
        # .map() changes colors based on state (selected=active tab, active=hover)
        self.style.map('TNotebook.Tab', background=[('selected', '#0078d4'), ('active', '#505050')])
        
        # Style different types of widgets with consistent dark theme
        self.style.configure('TFrame', background='#2b2b2b')  # Container frames
        
        # LabelFrame = frames with titles (like "Add New Player")
        self.style.configure('TLabelFrame', background='#2b2b2b', foreground='white', 
                           borderwidth=1, relief='solid')
        
        # Labels = text that doesn't change (like "Player Tag:")
        self.style.configure('TLabel', background='#2b2b2b', foreground='white', font=('Segoe UI', 10))
        
        # Entry = text input boxes where users type
        self.style.configure('TEntry', fieldbackground='#404040', foreground='white', 
                           borderwidth=1, insertcolor='white')  # insertcolor = cursor color
        
        # Combobox = dropdown menus (white background for readability)
        self.style.configure('TCombobox', fieldbackground='white', foreground='black', 
                           borderwidth=1, arrowcolor='black')
        self.style.map('TCombobox', fieldbackground=[('readonly', 'white')], 
                      foreground=[('readonly', 'black')])
        
        # Buttons = clickable elements
        self.style.configure('TButton', background='#0078d4', foreground='white', 
                           borderwidth=0, focuscolor='none', font=('Segoe UI', 10, 'bold'))
        # Button color changes: active=hover, pressed=clicking
        self.style.map('TButton', background=[('active', '#106ebe'), ('pressed', '#005a9e')])
        
        # Treeview styling (tables that show player data)
        self.style.configure('Treeview', background='#404040', foreground='white', 
                           fieldbackground='#404040', borderwidth=0)
        # Treeview.Heading = column headers (Tag, Elo, etc.)
        self.style.configure('Treeview.Heading', background='#0078d4', foreground='white', 
                           borderwidth=1, relief='solid')
        # Change background when a row is selected
        self.style.map('Treeview', background=[('selected', '#0078d4')])
        
        # Create instances of our custom classes to handle data
        self.player_manager = PlayerManager()  # Handles all player-related operations
        self.race_manager = RaceManager()  # Handles all race-related operations
        
        # Build the GUI interface and load initial data
        self.create_widgets()  # Create all the buttons, tabs, etc.
        self.refresh_players()  # Load and display current player data
    
    def create_widgets(self):
        """Create all the GUI elements (tabs, buttons, text fields, etc.)"""
        
        # Header section at the top of the window
        header_frame = tk.Frame(self.root, bg='#1a1a1a', height=60)  # Dark header bar
        header_frame.pack(fill=tk.X)  # fill=tk.X means stretch horizontally to fill width
        header_frame.pack_propagate(False)  # Don't let contents change the frame size
        
        # Main title label in the header
        title_label = tk.Label(header_frame, text="🏁 TRACKMANIA ELO SYSTEM", 
                              bg='#1a1a1a', fg='#0078d4',  # bg=background, fg=foreground (text color)
                              font=('Segoe UI', 18, 'bold'))  # font: (family, size, style)
        title_label.pack(expand=True)  # expand=True centers the label in available space
        
        # Main notebook widget - creates the tab system (Players, Add Race, etc.)
        notebook = ttk.Notebook(self.root)  # Notebook = container for multiple tabs
        # pack() positions the widget: fill=BOTH means stretch in all directions
        # expand=True means take up all available space, padx/pady add margins
        notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        # Create each tab as a separate frame, then add to notebook
        # Players tab - for viewing and adding players
        players_frame = ttk.Frame(notebook)  # Create a frame to hold tab contents
        notebook.add(players_frame, text="Players")  # Add frame to notebook with tab label
        self.create_players_tab(players_frame)  # Fill the frame with player-related widgets
        
        # Race tab
        race_frame = ttk.Frame(notebook)
        notebook.add(race_frame, text="Add Race")
        self.create_race_tab(race_frame)
        
        # Scheduled races tab
        scheduled_frame = ttk.Frame(notebook)
        notebook.add(scheduled_frame, text="Scheduled Races")
        self.create_scheduled_tab(scheduled_frame)
        
        # History tab
        history_frame = ttk.Frame(notebook)
        notebook.add(history_frame, text="Race History")
        self.create_history_tab(history_frame)
    
    def create_players_tab(self, parent):
        # Add player section
        add_frame = ttk.LabelFrame(parent, text="➕ Add New Player", padding=15)
        add_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(add_frame, text="Player Tag:").grid(row=0, column=0, padx=5, pady=5)
        self.player_tag_entry = ttk.Entry(add_frame)
        self.player_tag_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(add_frame, text="World Rank:").grid(row=0, column=2, padx=5, pady=5)
        self.world_rank_entry = ttk.Entry(add_frame)
        self.world_rank_entry.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Button(add_frame, text="Add Player", command=self.add_player).grid(row=0, column=4, padx=5, pady=5)
        
        # Players list
        list_frame = ttk.LabelFrame(parent, text="📈 Current Standings", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns = ("Tag", "World Rank", "Initial Elo", "Current Elo", "League", "Races")
        self.players_tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        for col in columns:
            self.players_tree.heading(col, text=col)
            self.players_tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.players_tree.yview)
        self.players_tree.configure(yscrollcommand=scrollbar.set)
        
        self.players_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_race_tab(self, parent):
        # Race name and league filter
        top_frame = ttk.LabelFrame(parent, text="🏁 Race Setup", padding=15)
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(top_frame, text="Race Name:").pack(side=tk.LEFT)
        self.race_name_entry = ttk.Entry(top_frame)
        self.race_name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 10))
        
        ttk.Label(top_frame, text="League Filter:").pack(side=tk.LEFT)
        self.league_filter_var = tk.StringVar(value="All")
        self.league_filter = ttk.Combobox(top_frame, textvariable=self.league_filter_var, 
                                         values=["All", "Beginner", "Intermediate", "Advanced"], 
                                         state="readonly", width=12)
        self.league_filter.pack(side=tk.LEFT, padx=(5, 10))
        self.league_filter.bind("<<ComboboxSelected>>", self.update_race_dropdowns)
        
        ttk.Label(top_frame, text="Type:").pack(side=tk.LEFT)
        self.race_type_var = tk.StringVar(value="Match")
        race_type_combo = ttk.Combobox(top_frame, textvariable=self.race_type_var,
                                      values=["Match", "Scrimmage"], state="readonly", width=10)
        race_type_combo.pack(side=tk.LEFT, padx=(5, 0))
        
        # Position dropdowns
        positions_frame = ttk.LabelFrame(parent, text="🏆 Race Results (Select players for each position)", padding=15)
        positions_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.position_vars = []
        self.position_dropdowns = []
        
        for i in range(8):
            row_frame = ttk.Frame(positions_frame)
            row_frame.pack(fill=tk.X, padx=5, pady=2)
            
            label = ttk.Label(row_frame, text=f"Position {i+1}:", width=12)
            label.pack(side=tk.LEFT)
            
            var = tk.StringVar()
            dropdown = ttk.Combobox(row_frame, textvariable=var, state="readonly")
            dropdown.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
            
            # DNF checkbox
            dnf_var = tk.BooleanVar()
            dnf_check = ttk.Checkbutton(row_frame, text="DNF", variable=dnf_var)
            dnf_check.pack(side=tk.LEFT)
            
            self.position_vars.append(var)
            self.position_dropdowns.append(dropdown)
            
            # Store DNF variable for later use
            if not hasattr(self, 'dnf_vars'):
                self.dnf_vars = []
            if len(self.dnf_vars) <= i:
                self.dnf_vars.append(dnf_var)
            else:
                self.dnf_vars[i] = dnf_var
        
        self.update_race_dropdowns()
        
        # Submit race button
        submit_btn = ttk.Button(parent, text="✅ Submit Race", command=self.submit_race)
        submit_btn.pack(pady=15)
    
    def create_history_tab(self, parent):
        # History frame
        history_frame = ttk.LabelFrame(parent, text="📅 Race History", padding=10)
        history_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.history_text = tk.Text(history_frame, wrap=tk.WORD, bg='#404040', fg='white', 
                                   font=('Consolas', 10), borderwidth=0, insertbackground='white')
        history_scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=self.history_text.yview)
        self.history_text.configure(yscrollcommand=history_scrollbar.set)
        
        self.history_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        history_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        refresh_btn = ttk.Button(parent, text="🔄 Refresh History", command=self.refresh_history)
        refresh_btn.pack(side=tk.BOTTOM, pady=10)
    
    def create_scheduled_tab(self, parent):
        # Create scheduled race section
        create_frame = ttk.LabelFrame(parent, text="📅 Schedule New Race", padding=15)
        create_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Race name
        name_row = ttk.Frame(create_frame)
        name_row.pack(fill=tk.X, pady=5)
        ttk.Label(name_row, text="Race Name:").pack(side=tk.LEFT)
        self.scheduled_race_name = ttk.Entry(name_row)
        self.scheduled_race_name.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 10))
        
        # League filter and race type
        ttk.Label(name_row, text="League:").pack(side=tk.LEFT)
        self.scheduled_league_var = tk.StringVar(value="All")
        scheduled_league_filter = ttk.Combobox(name_row, textvariable=self.scheduled_league_var,
                                             values=["All", "Beginner", "Intermediate", "Advanced"],
                                             state="readonly", width=12)
        scheduled_league_filter.pack(side=tk.LEFT, padx=(5, 10))
        scheduled_league_filter.bind("<<ComboboxSelected>>", self.update_scheduled_participants)
        
        ttk.Label(name_row, text="Type:").pack(side=tk.LEFT)
        self.scheduled_race_type_var = tk.StringVar(value="Match")
        race_type_combo = ttk.Combobox(name_row, textvariable=self.scheduled_race_type_var,
                                      values=["Match", "Scrimmage"], state="readonly", width=10)
        race_type_combo.pack(side=tk.LEFT, padx=(5, 0))
        
        # Participants selection
        participants_row = ttk.Frame(create_frame)
        participants_row.pack(fill=tk.X, pady=5)
        
        ttk.Label(participants_row, text="Participants:").pack(anchor=tk.W)
        
        # Listbox for selecting participants
        listbox_frame = ttk.Frame(participants_row)
        listbox_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.participants_listbox = tk.Listbox(listbox_frame, selectmode=tk.MULTIPLE, height=8,
                                              bg='white', fg='black', selectbackground='#0078d4',
                                              selectforeground='white')
        participants_scrollbar = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=self.participants_listbox.yview)
        self.participants_listbox.configure(yscrollcommand=participants_scrollbar.set)
        
        self.participants_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        participants_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create race button
        create_btn = ttk.Button(create_frame, text="📅 Schedule Race", command=self.schedule_race)
        create_btn.pack(pady=10)
        
        # Scheduled races list
        list_frame = ttk.LabelFrame(parent, text="⏳ Pending Races", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scheduled races treeview
        columns = ("Name", "Type", "Participants", "Scheduled Date")
        self.scheduled_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=6)
        
        for col in columns:
            self.scheduled_tree.heading(col, text=col)
            self.scheduled_tree.column(col, width=200)
        
        scheduled_scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.scheduled_tree.yview)
        self.scheduled_tree.configure(yscrollcommand=scheduled_scrollbar.set)
        
        self.scheduled_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scheduled_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Complete race button
        complete_btn = ttk.Button(list_frame, text="✅ Complete Selected Race", command=self.complete_race)
        complete_btn.pack(pady=10)
        
        self.update_scheduled_participants()
        self.refresh_scheduled_races()
    
    def add_player(self):
        tag = self.player_tag_entry.get().strip()
        rank_str = self.world_rank_entry.get().strip()
        
        if not tag or not rank_str:
            messagebox.showerror("Error", "Please fill in both fields")
            return
        
        try:
            rank = int(rank_str)
            self.player_manager.add_player(tag, rank)
            self.player_tag_entry.delete(0, tk.END)
            self.world_rank_entry.delete(0, tk.END)
            self.refresh_players()
            self.refresh_race_dropdowns()
            messagebox.showinfo("Success", f"Added {tag}")
        except ValueError:
            messagebox.showerror("Error", "World rank must be a number")
    
    def refresh_players(self):
        for item in self.players_tree.get_children():
            self.players_tree.delete(item)
        
        for tag, data in sorted(self.player_manager.players.items(), key=lambda x: x[1]['current_elo'], reverse=True):
            league = self.player_manager.get_league(data['current_elo'])
            self.players_tree.insert("", tk.END, values=(
                tag,
                data['world_rank'],
                data['initial_elo'],
                data['current_elo'],
                league,
                data['races_played']
            ))
    
    def update_race_dropdowns(self, event=None):
        selected_league = self.league_filter_var.get()
        
        if selected_league == "All":
            player_names = [""] + list(self.player_manager.players.keys())
        else:
            filtered_players = []
            for tag, data in self.player_manager.players.items():
                player_league = self.player_manager.get_league(data['current_elo'])
                if player_league == selected_league:
                    filtered_players.append(tag)
            player_names = [""] + filtered_players
        
        # Update all dropdown values
        for dropdown in self.position_dropdowns:
            dropdown['values'] = player_names
    
    def refresh_race_dropdowns(self):
        self.update_race_dropdowns()
    
    def submit_race(self):
        race_name = self.race_name_entry.get().strip()
        if not race_name:
            messagebox.showerror("Error", "Please enter a race name")
            return
        
        race_results = []
        used_players = set()
        
        for i, var in enumerate(self.position_vars):
            player = var.get()
            if player:
                if player in used_players:
                    messagebox.showerror("Error", f"Player {player} selected multiple times")
                    return
                used_players.add(player)
                
                # Check if player DNF'd
                position = 'DNF' if self.dnf_vars[i].get() else i + 1
                race_results.append((player, position))
        
        if len(race_results) == 0:
            messagebox.showerror("Error", "Please select at least one player")
            return
        
        is_match = self.race_type_var.get() == "Match"
        self.race_manager.add_race(race_name, race_results, is_match)
        
        # Clear form
        self.race_name_entry.delete(0, tk.END)
        for var in self.position_vars:
            var.set("")
        for dnf_var in self.dnf_vars:
            dnf_var.set(False)
        
        self.refresh_players()
        if hasattr(self, 'scheduled_tree'):
            self.refresh_scheduled_races()
        messagebox.showinfo("Success", f"Race '{race_name}' added successfully!")
    
    def update_scheduled_participants(self, event=None):
        selected_league = self.scheduled_league_var.get()
        
        self.participants_listbox.delete(0, tk.END)
        
        if selected_league == "All":
            players = list(self.player_manager.players.keys())
        else:
            players = []
            for tag, data in self.player_manager.players.items():
                player_league = self.player_manager.get_league(data['current_elo'])
                if player_league == selected_league:
                    players.append(tag)
        
        for player in sorted(players):
            self.participants_listbox.insert(tk.END, player)
    
    def schedule_race(self):
        race_name = self.scheduled_race_name.get().strip()
        if not race_name:
            messagebox.showerror("Error", "Please enter a race name")
            return
        
        selected_indices = self.participants_listbox.curselection()
        if not selected_indices:
            messagebox.showerror("Error", "Please select participants")
            return
        
        participants = [self.participants_listbox.get(i) for i in selected_indices]
        
        is_match = self.scheduled_race_type_var.get() == "Match"
        self.race_manager.create_scheduled_race(race_name, participants, is_match)
        
        # Clear form
        self.scheduled_race_name.delete(0, tk.END)
        self.participants_listbox.selection_clear(0, tk.END)
        
        self.refresh_scheduled_races()
        messagebox.showinfo("Success", f"Race '{race_name}' scheduled successfully!")
    
    def refresh_scheduled_races(self):
        for item in self.scheduled_tree.get_children():
            self.scheduled_tree.delete(item)
        
        for race_id, race_data in self.race_manager.scheduled_races.items():
            participants_str = ", ".join(race_data['participants'][:3])
            if len(race_data['participants']) > 3:
                participants_str += f" (+{len(race_data['participants'])-3} more)"
            
            race_type = "Match" if race_data.get('is_match', True) else "Scrimmage"
            self.scheduled_tree.insert("", tk.END, values=(
                race_data['name'],
                race_type,
                participants_str,
                race_data['scheduled_date'][:10]
            ), tags=(race_id,))
    
    def complete_race(self):
        selected = self.scheduled_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a scheduled race")
            return
        
        # Get race ID from tags
        race_id = self.scheduled_tree.item(selected[0])['tags'][0]
        
        # Open completion dialog
        self.open_completion_dialog(race_id)
    
    def open_completion_dialog(self, race_id):
        scheduled_race = self.race_manager.scheduled_races[race_id]
        
        # Create completion window
        completion_window = tk.Toplevel(self.root)
        completion_window.title(f"Complete Race: {scheduled_race['name']}")
        completion_window.geometry("500x600")
        completion_window.configure(bg='#2b2b2b')
        
        ttk.Label(completion_window, text=f"Race: {scheduled_race['name']}", 
                 font=('Segoe UI', 12, 'bold')).pack(pady=10)
        
        # Position assignments
        positions_frame = ttk.LabelFrame(completion_window, text="Assign Positions", padding=15)
        positions_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.completion_vars = []
        self.completion_dnf_vars = []
        
        participants = scheduled_race['participants']
        for i in range(len(participants)):
            row_frame = ttk.Frame(positions_frame)
            row_frame.pack(fill=tk.X, padx=5, pady=2)
            
            ttk.Label(row_frame, text=f"Position {i+1}:", width=12).pack(side=tk.LEFT)
            
            var = tk.StringVar()
            dropdown = ttk.Combobox(row_frame, textvariable=var, values=[""] + participants, state="readonly")
            dropdown.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
            
            dnf_var = tk.BooleanVar()
            ttk.Checkbutton(row_frame, text="DNF", variable=dnf_var).pack(side=tk.LEFT)
            
            self.completion_vars.append(var)
            self.completion_dnf_vars.append(dnf_var)
        
        # Buttons
        btn_frame = ttk.Frame(completion_window)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="✅ Complete Race", 
                  command=lambda: self.finish_completion(race_id, completion_window)).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="❌ Cancel", 
                  command=completion_window.destroy).pack(side=tk.LEFT, padx=5)
    
    def finish_completion(self, race_id, window):
        race_results = []
        used_players = set()
        
        for i, var in enumerate(self.completion_vars):
            player = var.get()
            if player:
                if player in used_players:
                    messagebox.showerror("Error", f"Player {player} selected multiple times")
                    return
                used_players.add(player)
                
                position = 'DNF' if self.completion_dnf_vars[i].get() else i + 1
                race_results.append((player, position))
        
        if not race_results:
            messagebox.showerror("Error", "Please assign at least one position")
            return
        
        self.race_manager.complete_scheduled_race(race_id, race_results)
        
        window.destroy()
        self.refresh_scheduled_races()
        self.refresh_players()
        messagebox.showinfo("Success", "Race completed successfully!")
    
    def refresh_history(self):
        self.history_text.delete(1.0, tk.END)
        
        if not self.race_manager.races:
            self.history_text.insert(tk.END, "No races recorded yet.")
            return
        
        for race_id, race_data in self.race_manager.races.items():
            self.history_text.insert(tk.END, f"{race_data['name']} ({race_data['date'][:10]})\n")
            for player_tag, position in race_data['results']:
                change = race_data['elo_changes'].get(player_tag, 0)
                self.history_text.insert(tk.END, f"  {position}. {player_tag} ({change:+.0f})\n")
            self.history_text.insert(tk.END, "\n")

def main():
    root = tk.Tk()
    app = EloGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()