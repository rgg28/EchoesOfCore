from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GAME = ROOT / "game"

FILES = {}


def add(path, content):
    FILES[path] = content


# ============================================================
# project.godot
# ============================================================

add("project.godot", r'''[application]

config/name="Echoes of Core"
run/main_scene="res://scenes/Main.tscn"
config/features=PackedStringArray("4.3", "GL Compatibility")

[display]

window/size/viewport_width=1280
window/size/viewport_height=720
window/size/window_width_override=1280
window/size/window_height_override=720
window/stretch/mode="canvas_items"

[rendering]

renderer/rendering_method="gl_compatibility"
renderer/rendering_method.mobile="gl_compatibility"
environment/defaults/default_clear_color=Color(0.06, 0.08, 0.12, 1)

[input]

move_forward={
"deadzone": 0.5,
"events": [Object(InputEventKey,"physical_keycode":87)]
}

move_back={
"deadzone": 0.5,
"events": [Object(InputEventKey,"physical_keycode":83)]
}

move_left={
"deadzone": 0.5,
"events": [Object(InputEventKey,"physical_keycode":65)]
}

move_right={
"deadzone": 0.5,
"events": [Object(InputEventKey,"physical_keycode":68)]
}

ability_1={
"deadzone": 0.5,
"events": [Object(InputEventKey,"physical_keycode":49)]
}

ability_2={
"deadzone": 0.5,
"events": [Object(InputEventKey,"physical_keycode":50)]
}

ability_3={
"deadzone": 0.5,
"events": [Object(InputEventKey,"physical_keycode":51)]
}

ability_4={
"deadzone": 0.5,
"events": [Object(InputEventKey,"physical_keycode":52)]
}

ultimate={
"deadzone": 0.5,
"events": [Object(InputEventKey,"physical_keycode":81)]
}

order_attack={
"deadzone": 0.5,
"events": [Object(InputEventKey,"physical_keycode":90)]
}

order_retreat={
"deadzone": 0.5,
"events": [Object(InputEventKey,"physical_keycode":88)]
}

order_hold={
"deadzone": 0.5,
"events": [Object(InputEventKey,"physical_keycode":67)]
}

[gui]

theme/default_font_multichannel_signed_distance_field=true
''')


# ============================================================
# Main scene
# ============================================================

add("scenes/Main.tscn", r'''[gd_scene load_steps=3 format=3]

[ext_resource path="res://scripts/main.gd" type="Script" id="1"]
[ext_resource path="res://scripts/game_state.gd" type="Script" id="2"]

[node name="EchoesOfCore" type="Node3D"]
script = ExtResource("1")

[node name="GameState" type="Node" parent="."]
script = ExtResource("2")
''')


# ============================================================
# Game state
# ============================================================

add("scripts/game_state.gd", r'''extends Node

var gold: int = 0
var account_level: int = 1
var selected_hero: String = "Paladin"

var heroes := {
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

var inventory: Array = []


func add_gold(amount: int):
    gold += amount


func add_xp(hero_name: String, amount: int):
    if not heroes.has(hero_name):
        return

    heroes[hero_name]["xp"] += amount

    var required := heroes[hero_name]["level"] * 100

    while heroes[hero_name]["xp"] >= required:
        heroes[hero_name]["xp"] -= required
        heroes[hero_name]["level"] += 1
        account_level += 1
        required = heroes[hero_name]["level"] * 100


func add_item(item_name: String):
    inventory.append(item_name)


func save_game():
    var data := {
        "gold": gold,
        "account_level": account_level,
        "selected_hero": selected_hero,
        "heroes": heroes,
        "inventory": inventory
    }

    var file := FileAccess.open("user://save.json", FileAccess.WRITE)

    if file:
        file.store_string(JSON.stringify(data))


func load_game():
    if not FileAccess.file_exists("user://save.json"):
        return

    var file := FileAccess.open("user://save.json", FileAccess.READ)

    if not file:
        return

    var text := file.get_as_text()
    var data = JSON.parse_string(text)

    if typeof(data) != TYPE_DICTIONARY:
        return

    gold = data.get("gold", 0)
    account_level = data.get("account_level", 1)
    selected_hero = data.get("selected_hero", "Paladin")
    heroes = data.get("heroes", heroes)
    inventory = data.get("inventory", [])


func _ready():
    load_game()
''')


# ============================================================
# Hero data
# ============================================================

add("scripts/hero_data.gd", r'''class_name HeroData

static func get_data(hero_name: String) -> Dictionary:

    match hero_name:

        "Paladin":
            return {
                "role": "Tank",
                "color": Color(0.75, 0.82, 1.0),
                "max_hp": 160.0,
                "damage": 12.0,
                "speed": 4.5,
                "abilities": [
                    "Shield Strike",
                    "Holy Guard",
                    "Taunt",
                    "Judgment"
                ],
                "ultimate": "Divine Wall"
            }

        "Rogue":
            return {
                "role": "Melee DPS",
                "color": Color(0.65, 1.0, 0.65),
                "max_hp": 110.0,
                "damage": 20.0,
                "speed": 6.5,
                "abilities": [
                    "Backstab",
                    "Shadow Step",
                    "Poison Blade",
                    "Evasion"
                ],
                "ultimate": "Death From Shadows"
            }

        "Mage":
            return {
                "role": "Ranged DPS",
                "color": Color(0.55, 0.75, 1.0),
                "max_hp": 90.0,
                "damage": 24.0,
                "speed": 4.0,
                "abilities": [
                    "Fireball",
                    "Frost Nova",
                    "Arcane Burst",
                    "Blink"
                ],
                "ultimate": "Meteor"
            }

        "Cleric":
            return {
                "role": "Healer",
                "color": Color(1.0, 0.85, 0.35),
                "max_hp": 100.0,
                "damage": 10.0,
                "speed": 4.0,
                "abilities": [
                    "Holy Bolt",
                    "Heal",
                    "Group Heal",
                    "Purify"
                ],
                "ultimate": "Divine Light"
            }

    return {}
''')


# ============================================================
# Character
# ============================================================

add("scripts/hero.gd", r'''extends CharacterBody3D

var hero_name: String
var role: String
var max_hp: float = 100.0
var hp: float = 100.0
var damage: float = 10.0
var move_speed: float = 5.0

var is_player := false
var ai_order := "follow"

var cooldowns := {
    1: 0.0,
    2: 0.0,
    3: 0.0,
    4: 0.0,
    5: 0.0
}

var target: Node3D = null


func setup(name: String, player_controlled: bool):
    hero_name = name
    is_player = player_controlled

    var data := HeroData.get_data(hero_name)

    role = data["role"]
    max_hp = data["max_hp"]
    hp = max_hp
    damage = data["damage"]
    move_speed = data["speed"]

    var mesh := MeshInstance3D.new()
    var capsule := CapsuleMesh.new()

    capsule.height = 1.8
    capsule.radius = 0.45

    mesh.mesh = capsule

    var material := StandardMaterial3D.new()
    material.albedo_color = data["color"]

    mesh.material_override = material

    add_child(mesh)

    var collision := CollisionShape3D.new()
    var shape := CapsuleShape3D.new()

    shape.height = 1.8
    shape.radius = 0.45

    collision.shape = shape
    add_child(collision)


func _physics_process(delta):

    for key in cooldowns:
        cooldowns[key] = max(0.0, cooldowns[key] - delta)

    if is_player:
        player_control(delta)
    else:
        bot_control(delta)

    move_and_slide()


func player_control(delta):

    var direction := Vector3.ZERO

    if Input.is_action_pressed("move_forward"):
        direction.z -= 1

    if Input.is_action_pressed("move_back"):
        direction.z += 1

    if Input.is_action_pressed("move_left"):
        direction.x -= 1

    if Input.is_action_pressed("move_right"):
        direction.x += 1

    if direction.length() > 0:
        direction = direction.normalized()
        velocity.x = direction.x * move_speed
        velocity.z = direction.z * move_speed
    else:
        velocity.x = move_toward(velocity.x, 0, move_speed * 5 * delta)
        velocity.z = move_toward(velocity.z, 0, move_speed * 5 * delta)

    if Input.is_action_just_pressed("ability_1"):
        use_ability(1)

    if Input.is_action_just_pressed("ability_2"):
        use_ability(2)

    if Input.is_action_just_pressed("ability_3"):
        use_ability(3)

    if Input.is_action_just_pressed("ability_4"):
        use_ability(4)

    if Input.is_action_just_pressed("ultimate"):
        use_ability(5)


func bot_control(delta):

    if ai_order == "hold":
        velocity.x = move_toward(velocity.x, 0, move_speed * 4 * delta)
        velocity.z = move_toward(velocity.z, 0, move_speed * 4 * delta)
        return

    if ai_order == "retreat":
        velocity.x = -global_position.x * 0.8
        velocity.z = -global_position.z * 0.8
        return

    if target and is_instance_valid(target):

        var distance := global_position.distance_to(target.global_position)

        if role == "Healer":

            if target.get("hp") != null and target.hp < target.max_hp * 0.65:
                use_ability(2)
                velocity = Vector3.ZERO
                return

        if distance > 3.0:
            var direction := global_position.direction_to(target.global_position)
            velocity.x = direction.x * move_speed
            velocity.z = direction.z * move_speed
        else:
            velocity = Vector3.ZERO

            if cooldowns[1] <= 0:
                use_ability(1)


func use_ability(index: int):

    if cooldowns[index] > 0:
        return

    cooldowns[index] = 1.5

    if index == 2 and role == "Healer":

        var parent := get_parent()

        for child in parent.get_children():

            if child is CharacterBody3D:
                if child != self and child.has_method("receive_heal"):
                    child.receive_heal(25.0)

        return

    if target and is_instance_valid(target):

        if target.has_method("receive_damage"):
            var multiplier := 1.0

            if index == 5:
                multiplier = 3.0

            target.receive_damage(damage * multiplier)


func receive_damage(amount: float):

    hp -= amount

    if hp <= 0:
        hp = max_hp


func receive_heal(amount: float):

    hp = min(max_hp, hp + amount)
''')


# ============================================================
# Enemy
# ============================================================

add("scripts/enemy.gd", r'''extends CharacterBody3D

var max_hp := 60.0
var hp := 60.0
var damage := 7.0
var target: Node3D = null
var attack_timer := 0.0


func setup(enemy_name: String = "Goblin"):

    if enemy_name == "Goblin":
        max_hp = 60.0
        damage = 7.0

    elif enemy_name == "Wolf":
        max_hp = 45.0
        damage = 10.0

    elif enemy_name == "Skeleton":
        max_hp = 75.0
        damage = 8.0

    elif enemy_name == "Ash Guardian":
        max_hp = 700.0
        damage = 20.0

    hp = max_hp

    var mesh := MeshInstance3D.new()
    var sphere := SphereMesh.new()

    sphere.height = 1.4
    sphere.radius = 0.7

    mesh.mesh = sphere

    var material := StandardMaterial3D.new()
    material.albedo_color = Color(0.75, 0.18, 0.12)

    mesh.material_override = material

    add_child(mesh)

    var collision := CollisionShape3D.new()
    var shape := SphereShape3D.new()

    shape.radius = 0.7
    collision.shape = shape

    add_child(collision)


func _physics_process(delta):

    attack_timer -= delta

    if not target or not is_instance_valid(target):
        return

    var distance := global_position.distance_to(target.global_position)

    if distance > 2.5:

        var direction := global_position.direction_to(target.global_position)

        velocity.x = direction.x * 2.0
        velocity.z = direction.z * 2.0

        move_and_slide()

    else:

        velocity = Vector3.ZERO

        if attack_timer <= 0:
            attack_timer = 1.5

            if target.has_method("receive_damage"):
                target.receive_damage(damage)


func receive_damage(amount: float):

    hp -= amount

    if hp <= 0:
        die()


func die():

    var state = get_node_or_null("/root/EchoesOfCore/GameState")

    if state:
        state.add_gold(10)
        state.add_xp(state.selected_hero, 25)
        state.add_item("Random Loot")

        state.save_game()

    queue_free()
''')


# ============================================================
# Main controller
# ============================================================

add("scripts/main.gd", r'''extends Node3D

var heroes: Array = []
var enemies: Array = []

var player: CharacterBody3D
var boss: CharacterBody3D

var world_root: Node3D

var status_label: Label
var hero_label: Label
var gold_label: Label


func _ready():

    world_root = Node3D.new()
    world_root.name = "World"
    add_child(world_root)

    create_world()
    create_ui()
    create_party()

    spawn_enemy("Goblin", Vector3(5, 0, -5))
    spawn_enemy("Goblin", Vector3(-5, 0, -5))
    spawn_enemy("Wolf", Vector3(7, 0, -8))
    spawn_enemy("Skeleton", Vector3(-7, 0, -8))

    spawn_boss()


func create_world():

    var floor := MeshInstance3D.new()
    var mesh := PlaneMesh.new()

    mesh.size = Vector2(50, 50)
    floor.mesh = mesh

    var material := StandardMaterial3D.new()
    material.albedo_color = Color(0.18, 0.32, 0.20)

    floor.material_override = material

    world_root.add_child(floor)

    var light := DirectionalLight3D.new()

    light.rotation_degrees = Vector3(-55, -30, 0)
    light.light_energy = 1.4

    world_root.add_child(light)

    var environment := WorldEnvironment.new()
    var env := Environment.new()

    env.background_mode = Environment.BG_COLOR
    env.background_color = Color(0.08, 0.12, 0.18)

    env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
    env.ambient_light_color = Color(0.55, 0.60, 0.70)
    env.ambient_light_energy = 0.7

    environment.environment = env

    world_root.add_child(environment)


func create_party():

    var state = get_node_or_null("GameState")

    var selected := "Paladin"

    if state:
        selected = state.selected_hero

    player = create_hero(selected, Vector3(0, 1, 5), true)

    var remaining := []

    for hero_name in ["Paladin", "Rogue", "Mage", "Cleric"]:
        if hero_name != selected:
            remaining.append(hero_name)

    create_hero(remaining[0], Vector3(-3, 1, 7), false)
    create_hero(remaining[1], Vector3(3, 1, 7), false)
    create_hero(remaining[2], Vector3(0, 1, 9), false)


func create_hero(hero_name: String, position: Vector3, controlled: bool):

    var hero := CharacterBody3D.new()
    hero.set_script(load("res://scripts/hero.gd"))

    world_root.add_child(hero)

    hero.global_position = position
    hero.setup(hero_name, controlled)

    heroes.append(hero)

    return hero


func spawn_enemy(enemy_name: String, position: Vector3):

    var enemy := CharacterBody3D.new()
    enemy.set_script(load("res://scripts/enemy.gd"))

    world_root.add_child(enemy)

    enemy.global_position = position
    enemy.setup(enemy_name)

    enemies.append(enemy)

    assign_target(enemy)

    return enemy


func spawn_boss():

    boss = spawn_enemy("Ash Guardian", Vector3(0, 1, -15))

    var boss_mesh = boss.get_node_or_null("MeshInstance3D")

    if boss_mesh:
        boss_mesh.scale = Vector3(2.5, 2.5, 2.5)


func assign_target(enemy):

    if not player:
        return

    enemy.target = player

    for hero in heroes:
        if is_instance_valid(hero):
            hero.target = enemy


func create_ui():

    var canvas := CanvasLayer.new()
    canvas.name = "UI"

    add_child(canvas)

    status_label = Label.new()
    status_label.position = Vector2(30, 25)
    status_label.add_theme_font_size_override("font_size", 24)

    canvas.add_child(status_label)

    hero_label = Label.new()
    hero_label.position = Vector2(30, 65)
    hero_label.add_theme_font_size_override("font_size", 20)

    canvas.add_child(hero_label)

    gold_label = Label.new()
    gold_label.position = Vector2(30, 105)
    gold_label.add_theme_font_size_override("font_size", 20)

    canvas.add_child(gold_label)

    var abilities := Label.new()
    abilities.position = Vector2(420, 640)
    abilities.text = "1 2 3 4  |  Q Ultimate"
    abilities.add_theme_font_size_override("font_size", 24)

    canvas.add_child(abilities)

    var orders := Label.new()
    orders.position = Vector2(30, 650)
    orders.text = "Z Atacar   X Retirada   C Mantener"
    orders.add_theme_font_size_override("font_size", 18)

    canvas.add_child(orders)


func _process(_delta):

    update_ui()
    process_orders()


func update_ui():

    if not player:
        return

    status_label.text = "ECHOES OF CORE"

    hero_label.text = "Héroe: %s   HP: %d / %d" % [
        player.hero_name,
        int(player.hp),
        int(player.max_hp)
    ]

    var state = get_node_or_null("GameState")

    if state:
        gold_label.text = "Oro: %d   Nivel: %d" % [
            state.gold,
            state.account_level
        ]


func process_orders():

    if Input.is_action_just_pressed("order_attack"):
        set_bot_order("attack")

    if Input.is_action_just_pressed("order_retreat"):
        set_bot_order("retreat")

    if Input.is_action_just_pressed("order_hold"):
        set_bot_order("hold")


func set_bot_order(order: String):

    for hero in heroes:

        if hero == player:
            continue

        if is_instance_valid(hero):
            hero.ai_order = order
''')


# ============================================================
# README
# ============================================================

add("README.md", r'''# Echoes of Core

Primera vertical slice jugable del RPG de acción singleplayer.

## Controles

WASD - Movimiento

1 - Habilidad 1

2 - Habilidad 2

3 - Habilidad 3

4 - Habilidad 4

Q - Ultimate

Z - Orden: Atacar

X - Orden: Retirada

C - Orden: Mantener posición

## Estado actual

- Grupo automático de 4 personajes
- Paladín
- Pícaro
- Mago
- Clérigo
- IA básica
- Combate
- Habilidades
- Ultimate
- Enemigos
- Jefe
- Loot básico
- Oro
- XP
- Guardado local

Esta versión es la base sobre la que se construirán las siguientes versiones.
''')


# ============================================================
# Generate
# ============================================================

def main():

    GAME.mkdir(parents=True, exist_ok=True)

    for relative_path, content in FILES.items():

        destination = GAME / relative_path

        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(content, encoding="utf-8")

        print(f"[CREADO] {destination}")

    print()
    print("==========================================")
    print(" ECHOES OF CORE GENERADO CORRECTAMENTE")
    print("==========================================")
    print()
    print(f"Proyecto: {GAME}")
    print(f"Archivos: {len(FILES)}")


if __name__ == "__main__":
    main()
