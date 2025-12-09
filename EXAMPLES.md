# Santa's Helper - Examples

This file contains practical examples of using Santa's Helper.

## Basic CLI Workflow

### 1. Add People

```bash
python cli.py add-person "Alice"
python cli.py add-person "Bob"
python cli.py add-person "Charlie"
```

### 2. Add Items to Wishlists

```bash
# Alice's wishlist
python cli.py add-item "Alice" "Gaming Laptop" "High-performance gaming laptop" 1
python cli.py add-item "Alice" "Mechanical Keyboard" "RGB mechanical keyboard" 2
python cli.py add-item "Alice" "Gaming Mouse" "Wireless gaming mouse" 2

# Bob's wishlist
python cli.py add-item "Bob" "Smart Watch" "Fitness tracking smartwatch" 1
python cli.py add-item "Bob" "Bluetooth Headphones" "Noise-cancelling headphones" 1

# Charlie's wishlist
python cli.py add-item "Charlie" "Book Set" "Fantasy book series" 3
python cli.py add-item "Charlie" "Coffee Maker" "Automatic espresso machine" 2
```

### 3. View Wishlists

```bash
# List all people
python cli.py list-people

# View specific person's wishlist
python cli.py list-items "Alice"
```

### 4. Generate Price Comparison Links

```bash
python cli.py find-prices "Alice"
```

Output:
```
Prisjakt Links for Alice's Wishlist:
======================================================================

[Priority 1] Gaming Laptop
  Description: High-performance gaming laptop
  Prisjakt: https://www.prisjakt.nu/search?search=Gaming%20Laptop

[Priority 2] Mechanical Keyboard
  Description: RGB mechanical keyboard
  Prisjakt: https://www.prisjakt.nu/search?search=Mechanical%20Keyboard

[Priority 2] Gaming Mouse
  Description: Wireless gaming mouse
  Prisjakt: https://www.prisjakt.nu/search?search=Gaming%20Mouse
```

### 5. Manage Items

```bash
# Remove an item
python cli.py remove-item "Alice" "Gaming Mouse"

# Remove a person's wishlist
python cli.py remove-person "Charlie"
```

## GUI Workflow

1. Launch the GUI:
   ```bash
   python gui.py
   ```

2. In the GUI you can:
   - Click "Add Person" to create a new person
   - Select a person from the list to view their wishlist
   - Click "Add Item" to add items to the selected person's wishlist
   - Click "Find Prices" to open a window with clickable Prisjakt links
   - Click "Open All Links in Browser" to open all items in separate browser tabs

## YAML File Structure

Each person's wishlist is stored in `wishlists/PersonName.yaml`:

```yaml
name: Alice
wishlist:
- name: Gaming Laptop
  description: High-performance gaming laptop
  priority: 1
- name: Mechanical Keyboard
  description: RGB mechanical keyboard
  priority: 2
```

## Tips

1. **Priority Levels**: Use priority 1 for most wanted items, higher numbers for less urgent items
2. **Descriptions**: Add detailed descriptions to help find the exact product
3. **Prisjakt Search**: The generated links search Prisjakt.nu, a Swedish price comparison site
4. **Backup**: The YAML files in `wishlists/` are your data - back them up if needed
5. **Sharing**: You can share YAML files with others or check them into version control

## Advanced Usage

### Batch Operations

Create a script to add multiple items:

```bash
#!/bin/bash
PERSON="Alice"

python cli.py add-item "$PERSON" "Item 1" "Description 1" 1
python cli.py add-item "$PERSON" "Item 2" "Description 2" 2
python cli.py add-item "$PERSON" "Item 3" "Description 3" 3
```

### Viewing All Wishlists

```bash
for person in $(python cli.py list-people | tail -n +2 | sed 's/^  - //'); do
    echo "=== $person ==="
    python cli.py list-items "$person"
    echo
done
```

### Export All Links

```bash
for person in $(python cli.py list-people | tail -n +2 | sed 's/^  - //'); do
    python cli.py find-prices "$person" >> all_prices.txt
    echo -e "\n---\n" >> all_prices.txt
done
```
