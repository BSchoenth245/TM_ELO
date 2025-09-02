import json
import math
from datetime import datetime
from player_manager import PlayerManager

class RaceManager:
    def __init__(self, races_file="races.json", scheduled_file="scheduled_races.json", matches_file="matches.json"):
        self.races_file = races_file
        self.scheduled_file = scheduled_file
        self.matches_file = matches_file
        self.races = self.load_races()
        self.scheduled_races = self.load_scheduled_races()
        self.matches = self.load_matches()
        self.player_manager = PlayerManager()
    
    def load_races(self):
        try:
            with open(self.races_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def save_races(self):
        with open(self.races_file, 'w') as f:
            json.dump(self.races, f, indent=2)
    
    def load_scheduled_races(self):
        try:
            with open(self.scheduled_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def save_scheduled_races(self):
        with open(self.scheduled_file, 'w') as f:
            json.dump(self.scheduled_races, f, indent=2)
    
    def load_matches(self):
        try:
            with open(self.matches_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def save_matches(self):
        with open(self.matches_file, 'w') as f:
            json.dump(self.matches, f, indent=2)
    
    def update_elo_rating(self, P, K_scrims, K_matches, M_scrims, M_matches, D, R, 
                          opponent_elos, teammate_elos, S=400, is_match=True):
        """
        Update a player's ELO rating based on race/match performance.
        """
        K = K_matches if is_match else K_scrims
        M = M_matches if is_match else M_scrims
        
        D_o = len(opponent_elos)
        D_t = len(teammate_elos)
        
        first_term = (D_o + M) * (D - R) / (D - 1)
        
        opponent_sum = 0
        for O_n in opponent_elos:
            expected_score = 1 / (1 + 10**((O_n - P) / S))
            opponent_sum += expected_score
        
        teammate_sum = 0
        for T_n in teammate_elos:
            expected_score = 1 / (1 + 10**((T_n - P) / S))
            teammate_sum += expected_score
        
        teammate_term = (1 / D_t) * teammate_sum if D_t > 0 else 0
        
        P_prime = P + K * (first_term - opponent_sum - teammate_term)
        return P_prime
    
    def process_race_results(self, race_results, is_match=True):
        """
        Process race results and update player Elos using new formula
        race_results: list of (player_tag, finish_position) tuples, sorted by position
        Position can be 1-8 for normal finishes, or 'DNF' for did not finish
        """
        participants = []
        
        # Count total participants and find last place position
        total_participants = len(race_results)
        
        for player_tag, position in race_results:
            if player_tag not in self.player_manager.players:
                print(f"Warning: {player_tag} not found in player database!")
                continue
            
            # Handle DNF - ALL DNF players get last place position (total_participants)
            if position == 'DNF' or str(position).upper() == 'DNF':
                actual_position = total_participants  # Always last place
            else:
                actual_position = int(position)
            
            participants.append({
                'tag': player_tag,
                'position': actual_position,
                'original_position': position,
                'old_elo': self.player_manager.players[player_tag]['current_elo']
            })
        
        if len(participants) != 8:
            print(f"Warning: Expected 8 racers, got {len(participants)}")
        
        elo_changes = {}
        
        for participant in participants:
            tag = participant['tag']
            position = participant['position']
            current_elo = participant['old_elo']
            
            # Get opponent Elos (all other participants)
            opponent_elos = [p['old_elo'] for p in participants if p['tag'] != tag]
            
            # Calculate new Elo using the provided formula
            new_elo = self.update_elo_rating(
                P=current_elo,
                K_scrims=16,
                K_matches=32,
                M_scrims=0,
                M_matches=1,
                D=len(participants),
                R=position,
                opponent_elos=opponent_elos,
                teammate_elos=[],  # No teammates in individual racing
                is_match=is_match
            )
            
            change = new_elo - current_elo
            elo_changes[tag] = change
        
        # Apply Elo changes
        for participant in participants:
            tag = participant['tag']
            old_elo = participant['old_elo']
            change = elo_changes[tag]
            new_elo = old_elo + change
            
            self.player_manager.players[tag]['current_elo'] = round(new_elo)
            self.player_manager.players[tag]['league'] = self.player_manager.get_league(new_elo)
            self.player_manager.players[tag]['races_played'] += 1
            
            dnf_indicator = " (DNF)" if participant['original_position'] == 'DNF' or str(participant['original_position']).upper() == 'DNF' else ""
            print(f"{tag}: {old_elo} -> {round(new_elo)} ({change:+.1f}){dnf_indicator}")
        
        self.player_manager.save_players()
        return elo_changes
    
    def add_race(self, race_name, race_results, is_match=True):
        """
        Add a race and process results
        race_results: list of (player_tag, finish_position) tuples
        """
        race_id = f"race_{len(self.races) + 1}"
        
        # Sort by finish position
        race_results.sort(key=lambda x: x[1])
        
        elo_changes = self.process_race_results(race_results, is_match)
        
        # Store race data
        self.races[race_id] = {
            "name": race_name,
            "date": datetime.now().isoformat(),
            "results": race_results,
            "elo_changes": elo_changes,
            "is_match": is_match
        }
        
        self.save_races()
        print(f"\nRace '{race_name}' added successfully!")
    
    def create_match(self, match_name, participants, league, is_match=True):
        """
        Create a new match with multiple races (5 for matches, 3 for scrimmages)
        """
        match_id = f"match_{len(self.matches) + 1}"
        num_races = 5 if is_match else 3
        
        self.matches[match_id] = {
            "name": match_name,
            "participants": participants,
            "league": league,
            "is_match": is_match,
            "num_races": num_races,
            "created_date": datetime.now().isoformat(),
            "status": "in_progress",
            "races": {},
            "current_race": 1
        }
        
        self.save_matches()
        print(f"\n{'Match' if is_match else 'Scrimmage'} '{match_name}' created successfully!")
        return match_id
    
    def add_race_to_match(self, match_id, track_name, race_results):
        """
        Add a race result to an ongoing match and update Elo immediately
        """
        if match_id not in self.matches:
            print(f"Match {match_id} not found!")
            return False
        
        match_data = self.matches[match_id]
        current_race = match_data["current_race"]
        
        if current_race > match_data["num_races"]:
            print(f"Match already completed!")
            return False
        
        # Process race results and update Elo immediately
        elo_changes = self.process_race_results(race_results, match_data["is_match"])
        
        race_key = f"race_{current_race}"
        match_data["races"][race_key] = {
            "track": track_name,
            "results": race_results,
            "elo_changes": elo_changes,
            "date": datetime.now().isoformat()
        }
        
        match_data["current_race"] += 1
        
        # Check if match is complete
        if current_race >= match_data["num_races"]:
            match_data["status"] = "completed"
        
        self.save_matches()
        return True
    
    def delete_match(self, match_id):
        """
        Delete a match and revert all Elo changes
        """
        if match_id not in self.matches:
            return False
        
        match_data = self.matches[match_id]
        
        # Revert Elo changes for all races in the match
        for race_key, race_data in match_data['races'].items():
            for player, change in race_data['elo_changes'].items():
                if player in self.player_manager.players:
                    self.player_manager.players[player]['current_elo'] -= change
                    self.player_manager.players[player]['current_elo'] = round(self.player_manager.players[player]['current_elo'])
                    self.player_manager.players[player]['league'] = self.player_manager.get_league(self.player_manager.players[player]['current_elo'])
                    self.player_manager.players[player]['races_played'] -= 1
        
        # Delete the match
        del self.matches[match_id]
        self.save_matches()
        self.player_manager.save_players()
        return True
    
    def delete_race(self, race_id):
        """
        Delete a single race and revert Elo changes
        """
        if race_id not in self.races:
            return False
        
        race_data = self.races[race_id]
        
        # Revert Elo changes
        for player, change in race_data['elo_changes'].items():
            if player in self.player_manager.players:
                self.player_manager.players[player]['current_elo'] -= change
                self.player_manager.players[player]['current_elo'] = round(self.player_manager.players[player]['current_elo'])
                self.player_manager.players[player]['league'] = self.player_manager.get_league(self.player_manager.players[player]['current_elo'])
                self.player_manager.players[player]['races_played'] -= 1
        
        # Delete the race
        del self.races[race_id]
        self.save_races()
        self.player_manager.save_players()
        return True
    

    
    def create_scheduled_race(self, race_name, participants, is_match=True, scheduled_date=None):
        """
        Create a scheduled race with participants but no results yet
        """
        race_id = f"scheduled_{len(self.scheduled_races) + 1}"
        
        self.scheduled_races[race_id] = {
            "name": race_name,
            "participants": participants,
            "is_match": is_match,
            "scheduled_date": scheduled_date or datetime.now().isoformat(),
            "created_date": datetime.now().isoformat(),
            "status": "scheduled"
        }
        
        self.save_scheduled_races()
        print(f"\nScheduled race '{race_name}' created successfully!")
        return race_id
    
    def complete_scheduled_race(self, race_id, race_results, is_match=True):
        """
        Complete a scheduled race by adding results
        """
        if race_id not in self.scheduled_races:
            print(f"Scheduled race {race_id} not found!")
            return
        
        scheduled_race = self.scheduled_races[race_id]
        
        # Process the race results using the scheduled race's match type
        is_match = scheduled_race.get("is_match", True)
        elo_changes = self.process_race_results(race_results, is_match)
        
        # Move to completed races
        completed_race_id = f"race_{len(self.races) + 1}"
        self.races[completed_race_id] = {
            "name": scheduled_race["name"],
            "date": datetime.now().isoformat(),
            "scheduled_date": scheduled_race["scheduled_date"],
            "results": race_results,
            "elo_changes": elo_changes,
            "participants": scheduled_race["participants"],
            "is_match": is_match
        }
        
        # Remove from scheduled races
        del self.scheduled_races[race_id]
        
        self.save_races()
        self.save_scheduled_races()
        print(f"\nScheduled race '{scheduled_race['name']}' completed!")
    
    def list_matches(self):
        if not self.matches:
            print("No matches created.")
            return
        
        print("\nMatches:")
        print("-" * 60)
        for match_id, match_data in self.matches.items():
            status = match_data['status']
            race_progress = f"{len(match_data['races'])}/{match_data['num_races']}"
            print(f"{match_data['name']} (ID: {match_id}) - {status.title()} ({race_progress})")
            print(f"  League: {match_data['league']}")
            print(f"  Participants: {', '.join(match_data['participants'])}")
            if match_data['races']:
                print(f"  Tracks played: {', '.join([race['track'] for race in match_data['races'].values()])}")
            print()
    
    def list_scheduled_races(self):
        if not self.scheduled_races:
            print("No scheduled races.")
            return
        
        print("\nScheduled Races:")
        print("-" * 60)
        for race_id, race_data in self.scheduled_races.items():
            print(f"{race_data['name']} (ID: {race_id})")
            print(f"  Participants: {', '.join(race_data['participants'])}")
            print(f"  Scheduled: {race_data['scheduled_date'][:10]}")
            print()
    
    def list_races(self):
        if not self.races:
            print("No races recorded yet.")
            return
        
        print("\nRace History:")
        print("-" * 60)
        for race_id, race_data in self.races.items():
            print(f"{race_data['name']} ({race_data['date'][:10]})")
            for player_tag, position in race_data['results']:
                change = race_data['elo_changes'].get(player_tag, 0)
                print(f"  {position}. {player_tag} ({change:+.0f})")
            print()

def main():
    rm = RaceManager()
    
    while True:
        print("\n=== Trackmania Race Manager ===")
        print("1. Create match/scrimmage")
        print("2. Add race to match")
        print("3. List matches")
        print("4. Delete match")
        print("5. Schedule race")
        print("6. Complete scheduled race")
        print("7. List scheduled races")
        print("8. View current standings")
        print("9. Exit")
        
        choice = input("\nChoice: ").strip()
        
        if choice == "1":
            match_name = input("Match/Scrimmage name: ").strip()
            match_type = input("Type (match/scrimmage): ").strip().lower()
            is_match = match_type == "match"
            league = input("League (Academy/Champion/Master): ").strip()
            
            print("Enter participants (player_tag), type 'done' when finished:")
            participants = []
            while True:
                entry = input("Player: ").strip()
                if entry.lower() == 'done':
                    break
                if entry in rm.player_manager.players:
                    participants.append(entry)
                else:
                    print(f"Player {entry} not found!")
            
            if participants:
                rm.create_match(match_name, participants, league, is_match)
            else:
                print("No participants added!")
        
        elif choice == "2":
            rm.list_matches()
            match_id = input("Enter match ID: ").strip()
            
            if match_id in rm.matches:
                match_data = rm.matches[match_id]
                if match_data['status'] == 'completed':
                    print("Match already completed!")
                    continue
                
                track_name = input("Track name: ").strip()
                print("Enter race results (player_tag position), type 'done' when finished:")
                
                race_results = []
                while True:
                    entry = input("Player position: ").strip()
                    if entry.lower() == 'done':
                        break
                    
                    try:
                        parts = entry.split()
                        if len(parts) != 2:
                            print("Format: player_tag position (or DNF)")
                            continue
                        
                        player_tag = parts[0]
                        position = parts[1] if parts[1].upper() == 'DNF' else int(parts[1])
                        race_results.append((player_tag, position))
                    except ValueError:
                        print("Invalid format! Use: player_tag position")
                
                if race_results:
                    rm.add_race_to_match(match_id, track_name, race_results)
                else:
                    print("No results entered!")
            else:
                print("Match ID not found!")
        
        elif choice == "3":
            rm.list_matches()
        
        elif choice == "4":
            rm.list_matches()
            match_id = input("Enter match ID to delete: ").strip()
            if match_id in rm.matches:
                confirm = input(f"Delete match '{rm.matches[match_id]['name']}'? (y/N): ").strip().lower()
                if confirm == 'y':
                    if rm.delete_match(match_id):
                        print("Match deleted successfully!")
                    else:
                        print("Failed to delete match!")
            else:
                print("Match ID not found!")
        
        elif choice == "5":
            race_name = input("Race name: ").strip()
            print("Enter participants (player_tag), type 'done' when finished:")
            
            participants = []
            while True:
                entry = input("Player: ").strip()
                if entry.lower() == 'done':
                    break
                if entry in rm.player_manager.players:
                    participants.append(entry)
                else:
                    print(f"Player {entry} not found!")
            
            if participants:
                rm.create_scheduled_race(race_name, participants)
            else:
                print("No participants added!")
        
        elif choice == "6":
            rm.list_scheduled_races()
            race_id = input("Enter race ID to complete: ").strip()
            
            if race_id in rm.scheduled_races:
                print("Enter race results (player_tag position), type 'done' when finished:")
                race_results = []
                while True:
                    entry = input("Player position: ").strip()
                    if entry.lower() == 'done':
                        break
                    
                    try:
                        parts = entry.split()
                        if len(parts) != 2:
                            print("Format: player_tag position (or DNF)")
                            continue
                        
                        player_tag = parts[0]
                        position = parts[1] if parts[1].upper() == 'DNF' else int(parts[1])
                        race_results.append((player_tag, position))
                    except ValueError:
                        print("Invalid format! Use: player_tag position")
                
                if race_results:
                    rm.complete_scheduled_race(race_id, race_results)
                else:
                    print("No results entered!")
            else:
                print("Race ID not found!")
        
        elif choice == "7":
            rm.list_scheduled_races()
        
        elif choice == "8":
            rm.player_manager.list_players()
        
        elif choice == "9":
            break
        
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()