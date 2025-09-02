import json
import math

class PlayerManager:
    def __init__(self, players_file="players.json"):
        self.players_file = players_file
        self.players = self.load_players()
    
    def load_players(self):
        try:
            with open(self.players_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def save_players(self):
        with open(self.players_file, 'w') as f:
            json.dump(self.players, f, indent=2)
    
    def world_rank_to_elo(self, world_rank):
        """Convert world ranking to initial Elo rating using logarithmic scale"""
        # Logarithmic formula: higher ranks get exponentially less Elo
        # This naturally creates the distribution you want without brackets
        max_elo = 4500
        min_elo = 800
        
        # Use log scale where rank 1 = max_elo, higher ranks approach min_elo
        log_rank = math.log(world_rank)
        log_max = math.log(100000)  # Assume ~100k total players for scaling
        
        # Invert the scale so rank 1 gets highest Elo
        elo = max_elo - ((log_rank / log_max) * (max_elo - min_elo))
        
        return max(min_elo, round(elo))
    
    def get_league(self, elo):
        """Determine league based on Elo rating"""
        if elo >= 3000:
            return "Master"
        elif elo >= 1701:
            return "Champion"
        else:
            return "Academy"
    
    def add_player(self, player_tag, world_rank):
        initial_elo = self.world_rank_to_elo(world_rank)
        league = self.get_league(initial_elo)
        self.players[player_tag] = {
            "world_rank": world_rank,
            "initial_elo": initial_elo,
            "current_elo": initial_elo,
            "league": league,
            "races_played": 0
        }
        self.save_players()
        print(f"Added {player_tag}: World Rank #{world_rank} -> {initial_elo} Elo ({league})")
    
    def list_players(self):
        if not self.players:
            print("No players added yet.")
            return
        
        print("\nCurrent Players:")
        print("-" * 70)
        for tag, data in sorted(self.players.items(), key=lambda x: x[1]['current_elo'], reverse=True):
            league = self.get_league(data['current_elo'])
            print(f"{tag:15} | Rank: #{data['world_rank']:6} | Elo: {data['current_elo']:4.0f} | {league}")

def main():
    pm = PlayerManager()
    
    while True:
        print("\n=== Trackmania Elo System ===")
        print("1. Add player")
        print("2. List players")
        print("3. Manage races")
        print("4. Exit")
        
        choice = input("\nChoice: ").strip()
        
        if choice == "1":
            tag = input("Player tag: ").strip()
            try:
                rank = int(input("World rank: ").strip())
                pm.add_player(tag, rank)
            except ValueError:
                print("Invalid rank number!")
        
        elif choice == "2":
            pm.list_players()
        
        elif choice == "3":
            from race_manager import main as race_main
            race_main()
        
        elif choice == "4":
            break
        
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()