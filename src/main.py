from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from src.worldgen import create_landscape

app = Ursina()
random_generator = random.Random()

window.title = 'rpg_simulator.py'
window.borderless = False
window.exit_button.visible = False
window.fps_counter.enabled = True
# window.show_ursina_splash = True

materials = {
    'sand': color.rgb(230, 208, 112),
    'grass': color.rgb(50, 191, 52),
    'stone': color.rgb(86, 88, 94),
    'snow': color.white,
    'dirt': color.rgb(105, 71, 37)
}


def generate_colors(verts):
    colors = []
    for v in verts:
        if 3 <= v[2] < 5.8:
            if v[2] > 5.5 or v[2] >= 4:
                if v[2] > 5.55:
                    colors.append(materials['grass'])
                else:
                    colors.append(materials['dirt'])
            else:
                colors.append(materials['grass'])
        elif v[2] <= 3:
            colors.append(materials['sand'])
        else:
            if v[2] > 6.2:
                colors.append(materials['snow'])
            else:
                colors.append(materials['stone'])
    return colors


def reset_player_pos():
    player.position = (0, 200, 0)

def jump():
    player.position[1] += 5

def input(key):
    if key == 'y':
        reset_player_pos()
    elif key == 'space':
        jump()


Sky(color=color.gray)

verts, faces = create_landscape()
colors = generate_colors(verts)

ground = Entity(
    model=Mesh(vertices=verts, triangles=faces, colors=colors),
    collider='mesh',
    collision=True,
    scale=20,
)
ground.rotation_x = 270
ground.position = (0, 0, 0)

player = FirstPersonController(y=50)
ray = raycaster.raycast(player.position+Vec3(0, 10, 0), player.down)
if ray.hit:
    player.y = ray.world_point[1]

print(f'v:  {len(verts)}')

app.run()
