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
        
        # Matches tab
        matches_frame = ttk.Frame(notebook)
        notebook.add(matches_frame, text="Matches")
        self.create_matches_tab(matches_frame)
        
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
        
        # Load initial history
        self.refresh_history()
    

    
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
            messagebox.showinfo("Success", f"Added {tag}")
            if hasattr(self, 'match_participants_listbox'):
                self.update_match_participants()
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
        
        # Add match history
        if self.race_manager.matches:
            self.history_text.insert(tk.END, "\n=== MATCH HISTORY ===\n\n")
            for match_id, match_data in self.race_manager.matches.items():
                if match_data['status'] == 'completed':
                    match_type = "Match" if match_data.get('is_match', True) else "Scrimmage"
                    self.history_text.insert(tk.END, f"{match_data['name']} ({match_type} - {match_data['league']})\n")
                    
                    # Show tracks played
                    tracks = [race['track'] for race in match_data['races'].values()]
                    self.history_text.insert(tk.END, f"  Tracks: {', '.join(tracks)}\n")
                    
                    # Show individual race results
                    for race_key, race_data in match_data['races'].items():
                        race_num = race_key.split('_')[1]
                        self.history_text.insert(tk.END, f"  Race {race_num} ({race_data['track']}): ")
                        for player, position in race_data['results']:
                            change = race_data['elo_changes'].get(player, 0)
                            self.history_text.insert(tk.END, f"{player}({position}, {change:+.0f}) ")
                        self.history_text.insert(tk.END, "\n")
                    self.history_text.insert(tk.END, "\n")

    def create_matches_tab(self, parent):
        # Create match section
        create_frame = ttk.LabelFrame(parent, text="🏆 Create Match/Scrimmage", padding=15)
        create_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Match name and settings
        name_row = ttk.Frame(create_frame)
        name_row.pack(fill=tk.X, pady=5)
        
        ttk.Label(name_row, text="Name:").pack(side=tk.LEFT)
        self.match_name_entry = ttk.Entry(name_row)
        self.match_name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 10))
        
        ttk.Label(name_row, text="Type:").pack(side=tk.LEFT)
        self.match_type_var = tk.StringVar(value="Match")
        match_type_combo = ttk.Combobox(name_row, textvariable=self.match_type_var,
                                       values=["Match", "Scrimmage"], state="readonly", width=10)
        match_type_combo.pack(side=tk.LEFT, padx=(5, 10))
        
        ttk.Label(name_row, text="League:").pack(side=tk.LEFT)
        self.match_league_var = tk.StringVar(value="Champion")
        match_league_combo = ttk.Combobox(name_row, textvariable=self.match_league_var,
                                         values=["Academy", "Champion", "Master"], 
                                         state="readonly", width=12)
        match_league_combo.pack(side=tk.LEFT, padx=(5, 0))
        match_league_combo.bind("<<ComboboxSelected>>", self.update_match_participants)
        
        # Participants selection
        participants_row = ttk.Frame(create_frame)
        participants_row.pack(fill=tk.X, pady=5)
        
        ttk.Label(participants_row, text="Participants:").pack(anchor=tk.W)
        
        # Search box
        search_frame = ttk.Frame(participants_row)
        search_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.player_search_var = tk.StringVar()
        self.player_search_entry = ttk.Entry(search_frame, textvariable=self.player_search_var)
        self.player_search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        self.player_search_var.trace('w', self.filter_participants)
        
        listbox_frame = ttk.Frame(participants_row)
        listbox_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.match_participants_listbox = tk.Listbox(listbox_frame, selectmode=tk.MULTIPLE, height=6,
                                                    bg='white', fg='black', selectbackground='#0078d4',
                                                    selectforeground='white')
        match_participants_scrollbar = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL, 
                                                    command=self.match_participants_listbox.yview)
        self.match_participants_listbox.configure(yscrollcommand=match_participants_scrollbar.set)
        
        self.match_participants_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        match_participants_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create match button
        create_match_btn = ttk.Button(create_frame, text="🏆 Create Match", command=self.create_match)
        create_match_btn.pack(pady=10)
        
        # Active matches list
        matches_frame = ttk.LabelFrame(parent, text="🏁 Active Matches", padding=10)
        matches_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Matches treeview
        columns = ("Name", "Type", "League", "Progress", "Status")
        self.matches_tree = ttk.Treeview(matches_frame, columns=columns, show="headings", height=8)
        
        for col in columns:
            self.matches_tree.heading(col, text=col)
            self.matches_tree.column(col, width=150)
        
        matches_scrollbar = ttk.Scrollbar(matches_frame, orient=tk.VERTICAL, command=self.matches_tree.yview)
        self.matches_tree.configure(yscrollcommand=matches_scrollbar.set)
        
        self.matches_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        matches_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Buttons for match actions
        match_buttons_frame = ttk.Frame(matches_frame)
        match_buttons_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(match_buttons_frame, text="➕ Add Race", command=self.add_race_to_match).pack(side=tk.LEFT, padx=5)
        ttk.Button(match_buttons_frame, text="❌ Delete", command=self.delete_selected_match).pack(side=tk.LEFT, padx=5)
        ttk.Button(match_buttons_frame, text="🔄 Refresh", command=self.refresh_matches).pack(side=tk.LEFT, padx=5)
        
        self.update_match_participants()
        self.refresh_matches()
    
    def update_match_participants(self, event=None):
        self.filter_participants()
    
    def filter_participants(self, *args):
        selected_league = self.match_league_var.get()
        search_term = self.player_search_var.get().lower()
        
        self.match_participants_listbox.delete(0, tk.END)
        
        players = []
        for tag, data in self.player_manager.players.items():
            player_league = self.player_manager.get_league(data['current_elo'])
            if player_league == selected_league:
                if not search_term or search_term in tag.lower():
                    players.append(tag)
        
        for player in sorted(players):
            self.match_participants_listbox.insert(tk.END, player)
    

    
    def create_match(self):
        match_name = self.match_name_entry.get().strip()
        if not match_name:
            messagebox.showerror("Error", "Please enter a match name")
            return
        
        selected_indices = self.match_participants_listbox.curselection()
        if not selected_indices:
            messagebox.showerror("Error", "Please select participants")
            return
        
        participants = [self.match_participants_listbox.get(i) for i in selected_indices]
        league = self.match_league_var.get()
        is_match = self.match_type_var.get() == "Match"
        
        self.race_manager.create_match(match_name, participants, league, is_match)
        
        # Clear form
        self.match_name_entry.delete(0, tk.END)
        self.match_participants_listbox.selection_clear(0, tk.END)
        self.player_search_var.set("")
        self.player_search_var.set("")
        
        self.refresh_matches()
        messagebox.showinfo("Success", f"{'Match' if is_match else 'Scrimmage'} '{match_name}' created successfully!")
    

    
    def delete_selected_match(self):
        selected = self.matches_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a match to delete")
            return
        
        match_id = self.matches_tree.item(selected[0])['tags'][0]
        match_data = self.race_manager.matches.get(match_id)
        
        if not match_data:
            messagebox.showerror("Error", "Match not found")
            return
        
        match_name = match_data['name']
        race_count = len(match_data['races'])
        confirm = messagebox.askyesno("Confirm Delete", f"Delete match '{match_name}'?\n\nThis will delete {race_count} races and revert all Elo changes.")
        if confirm:
            if self.race_manager.delete_match(match_id):
                self.refresh_matches()
                self.refresh_players()
                messagebox.showinfo("Success", "Match deleted successfully!")
            else:
                messagebox.showerror("Error", "Failed to delete match")
    
    def refresh_matches(self):
        for item in self.matches_tree.get_children():
            self.matches_tree.delete(item)
        
        for match_id, match_data in self.race_manager.matches.items():
            progress = f"{len(match_data['races'])}/{match_data['num_races']}"
            match_type = "Match" if match_data.get('is_match', True) else "Scrimmage"
            
            self.matches_tree.insert("", tk.END, values=(
                match_data['name'],
                match_type,
                match_data['league'],
                progress,
                match_data['status'].title()
            ), tags=(match_id,))
    
    def add_race_to_match(self):
        selected = self.matches_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a match")
            return
        
        match_id = self.matches_tree.item(selected[0])['tags'][0]
        match_data = self.race_manager.matches[match_id]
        
        if match_data['status'] == 'completed':
            messagebox.showinfo("Info", "Match already completed")
            return
        
        self.open_race_dialog(match_id)
    
    def open_race_dialog(self, match_id):
        match_data = self.race_manager.matches[match_id]
        current_race = match_data['current_race']
        
        # Create race dialog
        race_window = tk.Toplevel(self.root)
        race_window.title(f"Add Race {current_race}/{match_data['num_races']} - {match_data['name']}")
        race_window.geometry("500x600")
        race_window.configure(bg='#2b2b2b')
        
        ttk.Label(race_window, text=f"Race {current_race} of {match_data['num_races']}", 
                 font=('Segoe UI', 12, 'bold')).pack(pady=10)
        
        # Track name
        track_frame = ttk.Frame(race_window)
        track_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(track_frame, text="Track Name:").pack(side=tk.LEFT)
        track_entry = ttk.Entry(track_frame)
        track_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        
        # Search for participants
        search_frame = ttk.Frame(race_window)
        search_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(search_frame, text="Search Players:").pack(side=tk.LEFT)
        search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=search_var, width=20)
        search_entry.pack(side=tk.LEFT, padx=(5, 0))
        
        # Race results
        results_frame = ttk.LabelFrame(race_window, text="Race Results", padding=15)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        race_vars = []
        race_dnf_vars = []
        race_dropdowns = []
        
        participants = match_data['participants']
        
        def update_dropdowns():
            search_term = search_var.get().lower()
            if search_term:
                filtered_participants = [p for p in participants if search_term in p.lower()]
            else:
                filtered_participants = participants
            
            values = [""] + sorted(filtered_participants)
            for dropdown in race_dropdowns:
                dropdown['values'] = values
        
        for i in range(len(participants)):
            row_frame = ttk.Frame(results_frame)
            row_frame.pack(fill=tk.X, padx=5, pady=2)
            
            ttk.Label(row_frame, text=f"Position {i+1}:", width=12).pack(side=tk.LEFT)
            
            var = tk.StringVar()
            dropdown = ttk.Combobox(row_frame, textvariable=var, values=[""] + participants, state="readonly")
            dropdown.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
            
            dnf_var = tk.BooleanVar()
            ttk.Checkbutton(row_frame, text="DNF", variable=dnf_var).pack(side=tk.LEFT)
            
            race_vars.append(var)
            race_dnf_vars.append(dnf_var)
            race_dropdowns.append(dropdown)
        
        search_var.trace('w', lambda *args: update_dropdowns())
        
        # Buttons
        btn_frame = ttk.Frame(race_window)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="✅ Add Race", 
                  command=lambda: self.finish_race_dialog(match_id, track_entry, race_vars, race_dnf_vars, race_window)).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="❌ Cancel", 
                  command=race_window.destroy).pack(side=tk.LEFT, padx=5)
    
    def finish_race_dialog(self, match_id, track_entry, race_vars, race_dnf_vars, window):
        track_name = track_entry.get().strip()
        if not track_name:
            messagebox.showerror("Error", "Please enter a track name")
            return
        
        race_results = []
        used_players = set()
        
        for i, var in enumerate(race_vars):
            player = var.get()
            if player:
                if player in used_players:
                    messagebox.showerror("Error", f"Player {player} selected multiple times")
                    return
                used_players.add(player)
                
                position = 'DNF' if race_dnf_vars[i].get() else i + 1
                race_results.append((player, position))
        
        if not race_results:
            messagebox.showerror("Error", "Please assign at least one position")
            return
        
        success = self.race_manager.add_race_to_match(match_id, track_name, race_results)
        if success:
            window.destroy()
            self.refresh_matches()
            self.refresh_players()
            
            match_data = self.race_manager.matches[match_id]
            if match_data['status'] == 'completed':
                messagebox.showinfo("Match Complete!", f"Match '{match_data['name']}' has been completed!")
            else:
                messagebox.showinfo("Success", f"Race added to match. {match_data['current_race']-1}/{match_data['num_races']} races completed.")

def main():
    root = tk.Tk()
    app = EloGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()