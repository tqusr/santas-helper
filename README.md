# Santa's Helper 🎅

A wishlist management tool that helps you keep track of people's gift wishes and find the best prices using Prisjakt's price comparison service.

## Features

- 📝 Store wishlists for multiple people in separate YAML files
- 🔍 Automatically generate Prisjakt search links to find the best prices
- 💻 Command-line interface (CLI) for quick operations
- 🖥️ Graphical user interface (GUI) for easy management
- ⭐ Priority-based wishlist items

## Installation

1. Clone the repository:
```bash
git clone https://github.com/tqusr/santas-helper.git
cd santas-helper
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### GUI Mode

Launch the graphical interface:
```bash
python gui.py
```

The GUI allows you to:
- Add and remove people
- Manage wishlist items with descriptions and priorities
- View all items for each person
- Generate Prisjakt links with clickable URLs
- Open all links in your browser at once

### CLI Mode

Run commands from the terminal:

```bash
# Show help
python cli.py help

# Add a person
python cli.py add-person "John Doe"

# Add an item to their wishlist
python cli.py add-item "John Doe" "Gaming Mouse" "Wireless gaming mouse" 1

# List all people
python cli.py list-people

# View a person's wishlist
python cli.py list-items "John Doe"

# Generate Prisjakt links for all items
python cli.py find-prices "John Doe"

# Remove an item
python cli.py remove-item "John Doe" "Gaming Mouse"

# Remove a person
python cli.py remove-person "John Doe"
```

## Data Storage

Wishlist data is stored in YAML files in the `wishlists/` directory. Each person has their own file named `{person_name}.yaml`.

Example YAML structure:
```yaml
name: John Doe
wishlist:
- name: Gaming Mouse
  description: Wireless gaming mouse
  priority: 1
- name: Keyboard
  description: Mechanical keyboard
  priority: 2
```

## How It Works

When you search for prices, Santa's Helper generates direct Prisjakt search URLs for each wishlist item. Prisjakt (prisjakt.nu) is a Swedish price comparison service that helps find the best deals across multiple retailers.

## Requirements

- Python 3.7+
- pyyaml
- requests
- tkinter (usually included with Python)

## License

MIT License - See LICENSE file for details
