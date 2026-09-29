extends Node

var gold: int = 0
var account_level: int = 1
var selected_hero: String = "Paladin"

var heroes: Dictionary = {
	"Paladin": {
		"level": 1,
		"xp": 0,
		"role": "Tank"
	},
	"Rogue": {
		"level": 1,
		"xp": 0,
		"role": "Melee DPS"
	},
	"Mage": {
		"level": 1,
		"xp": 0,
		"role": "Ranged DPS"
	},
	"Cleric": {
		"level": 1,
		"xp": 0,
		"role": "Healer"
	}
}

var inventory: Array[String] = []


func add_gold(amount: int) -> void:
	gold += amount


func add_xp(hero_name: String, amount: int) -> void:
	if not heroes.has(hero_name):
		return

	var hero: Dictionary = heroes[hero_name]

	var current_xp: int = int(hero.get("xp", 0))
	var current_level: int = int(hero.get("level", 1))

	current_xp += amount

	var required: int = current_level * 100

	while current_xp >= required:
		current_xp -= required
		current_level += 1
		account_level += 1

		required = current_level * 100

	hero["xp"] = current_xp
	hero["level"] = current_level

	heroes[hero_name] = hero


func add_item(item_name: String) -> void:
	inventory.append(item_name)


func save_game() -> void:

	var data: Dictionary = {
		"gold": gold,
		"account_level": account_level,
		"selected_hero": selected_hero,
		"heroes": heroes,
		"inventory": inventory
	}

	var file: FileAccess = FileAccess.open(
		"user://save.json",
		FileAccess.WRITE
	)

	if file:
		file.store_string(JSON.stringify(data))
		file.close()


func load_game() -> void:

	if not FileAccess.file_exists("user://save.json"):
		return

	var file: FileAccess = FileAccess.open(
		"user://save.json",
		FileAccess.READ
	)

	if not file:
		return

	var text: String = file.get_as_text()
	file.close()

	var parsed = JSON.parse_string(text)

	if parsed == null:
		return

	if not parsed is Dictionary:
		return

	var data: Dictionary = parsed

	gold = int(data.get("gold", 0))
	account_level = int(data.get("account_level", 1))
	selected_hero = str(data.get("selected_hero", "Paladin"))

	var saved_heroes = data.get("heroes", null)

	if saved_heroes is Dictionary:
		heroes = saved_heroes

	var saved_inventory = data.get("inventory", null)

	if saved_inventory is Array:
		inventory.clear()

		for item in saved_inventory:
			inventory.append(str(item))


func _ready() -> void:
	load_game()
