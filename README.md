# Trackmania Elo System

A comprehensive Elo rating system for Trackmania esports leagues with a modern GUI interface.

## 🏁 Features

- **Player Management**: Add players with world rankings, automatic Elo calculation
- **League System**: Three skill tiers (Beginner, Intermediate, Advanced) based on Elo
- **Race Types**: Matches (competitive) vs Scrimmages (practice) with different Elo impacts
- **Scheduled Races**: Pre-plan races and add results later
- **DNF Handling**: Proper handling of Did Not Finish situations
- **Modern GUI**: Dark theme interface with intuitive navigation

## 📋 Requirements

- Python 3.7+
- tkinter (usually included with Python)
- No additional packages required!

## 🚀 Getting Started

1. **Install Python** (if not already installed)
2. **Clone or download** this project
3. **Run the application**:
   ```bash
   python elo_gui.py
   ```

## 📖 How to Use

### Adding Players
1. Go to the **Players** tab
2. Enter player tag and world ranking
3. Click **Add Player**
4. Initial Elo is automatically calculated from world rank

### Creating Races
**Option 1: Direct Race Entry**
1. Go to **Add Race** tab
2. Enter race name and select type (Match/Scrimmage)
3. Filter by league if needed
4. Select players for each position (1st-8th)
5. Check DNF for players who didn't finish
6. Click **Submit Race**

**Option 2: Scheduled Races**
1. Go to **Scheduled Races** tab
2. Create race with participants ahead of time
3. Later, select the race and add results
4. Useful for tournament planning

### Viewing Results
- **Players tab**: See current standings and Elo changes
- **Race History tab**: View all completed races with Elo changes

## 🎯 Elo System Details

### Initial Elo Calculation
Players start with Elo based on world ranking using a logarithmic formula:
- Rank 1: ~4500 Elo
- Rank 100: ~4000 Elo
- Rank 1000: ~3200 Elo
- Rank 30000+: ~800 Elo (minimum)

### League Tiers
- **Advanced**: 3000-4500 Elo
- **Intermediate**: 1701-3000 Elo  
- **Beginner**: 800-1700 Elo

### Race Types
- **Matches**: K=32, M=1 (full Elo impact for competitive races)
- **Scrimmages**: K=16, M=0 (reduced impact for practice)

### DNF Handling
- All DNF players receive last place position for Elo calculation
- Heavily penalizes DNFs to prevent abuse
- DNF status is tracked and displayed

## 🔧 Technical Details

### File Structure
```
TM Elo/
├── elo_gui.py          # Main GUI application
├── player_manager.py   # Player data management
├── race_manager.py     # Race processing and Elo calculations
├── players.json        # Player database
├── races.json          # Completed races
├── scheduled_races.json # Pending races
└── README.md          # This file
```

### Key Classes

**PlayerManager**: Handles player data, Elo calculations, league assignments
**RaceManager**: Processes race results, manages scheduled races
**EloGUI**: Creates and manages the graphical interface

### Elo Formula
Uses advanced multi-player Elo with position-based scoring:
```
P' = P + K * ((D_o + M)(D - R)/(D - 1) - Σ(expected_scores))
```
Where:
- P = current rating
- K = volatility factor (16 for scrims, 32 for matches)
- M = match importance (0 for scrims, 1 for matches)
- D = total participants
- R = finishing position
- D_o = number of opponents

## 🎨 GUI Features

### Modern Dark Theme
- Professional blue accent color (#0078d4)
- Dark backgrounds for reduced eye strain
- White text on dark backgrounds for readability
- Dropdown menus use white backgrounds for better visibility

### Intuitive Navigation
- Tabbed interface for different functions
- Emojis for visual appeal and quick recognition
- Consistent styling throughout application
- Responsive layout that adapts to content

### User-Friendly Design
- Input validation with helpful error messages
- Confirmation dialogs for important actions
- Auto-clearing forms after successful operations
- Real-time updates of player standings

## 🔍 Code Comments for Learning

The code includes extensive comments explaining:
- **Python concepts**: Classes, functions, data structures
- **GUI programming**: tkinter widgets, event handling, layout management
- **Data management**: JSON files, dictionaries, file I/O
- **Algorithm logic**: Elo calculations, sorting, filtering

Perfect for learning Python GUI development and understanding rating systems!

## 🏆 League Management Tips

1. **Start of Season**: Add all players with current world rankings
2. **Regular Races**: Use "Match" type for official league races
3. **Practice Sessions**: Use "Scrimmage" type to minimize Elo impact
4. **Tournament Planning**: Schedule races in advance, add results later
5. **Monitor DNFs**: Track players who DNF frequently

## 🐛 Troubleshooting

**"No module named 'tkinter'"**: Install tkinter
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install tkinter

# macOS (usually included)
# Windows (usually included)
```

**Players not showing in dropdowns**: Check league filter settings

**Elo changes seem wrong**: Verify race type (Match vs Scrimmage)

## 📈 Future Enhancements

Potential additions:
- Export data to CSV/Excel
- Elo history graphs
- Season management with resets
- Team-based competitions
- Web interface
- Database integration
- Statistics and analytics

## 📄 License

This project is open source. Feel free to modify and distribute!

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Additional statistics
- Better error handling
- Performance optimizations
- UI/UX enhancements
- Documentation improvements

---

**Happy Racing! 🏁**