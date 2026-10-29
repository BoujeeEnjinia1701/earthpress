"""Photoreal concept render with Blender (bpy) from a scene exported by scene_export.py.
Usage: python photoreal.py scene.npz out.png [--preview]
Materials come from part names (keywords) and the part's color, so any repo works without edits.
Optional per-repo overrides: a JSON file next to the npz named <stem>.materials.json mapping
part name -> material class (wood, fabric, clear, metal, painted, rubber, screen, paper, film,
plastic, clay)."""
import sys, json, math, colorsys, re
from pathlib import Path
import numpy as np
import bpy
from mathutils import Vector

ARGS = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]   # works under `blender -b -P photoreal.py -- ...` too
sys.argv = [sys.argv[0]] + ARGS
npz_path, out = Path(ARGS[0]), Path(ARGS[1])
preview = "--preview" in sys.argv
EXPO = 0.8
if "--product" in sys.argv: EXPO = 0.5
RES = None
FOCUS = None
HIDE = []
PRODUCT = "--product" in sys.argv
az = el = None
SCENE, GROUND, SUN, LENS, WATER_Z, GROUND_Z = "studio", None, (38.0, None), None, None, None
for a in sys.argv:
    if a.startswith("--scene="): SCENE = a[8:]                    # studio | outdoor (kit 1.9)
    if a.startswith("--ground="): GROUND = a[9:]                  # mud, concrete, roof, sand, soil, grass, workshop
    if a.startswith("--sun="):                                     # elevation[,azimuth] in degrees
        v = a[6:].split(","); SUN = (float(v[0]), float(v[1]) if len(v) > 1 else None)
    if a.startswith("--lens="): LENS = float(a[7:])
    if a.startswith("--ground-z="): GROUND_Z = float(a[11:]) / 1000.0   # ground level in model mm (site models: 0);
    # default is the model's lowest point
    if a.startswith("--water="): WATER_Z = float(a[8:]) / 1000.0   # still water level, mm above the ground level;
    # the outdoor ground relief is about +/-35 mm (mud) away from the product, so -5 to -20 leaves puddles in the
    # hollows and a positive value floods the whole site
    if a.startswith("--az="): az = float(a[5:])
    if a.startswith("--el="): el = float(a[5:])
    if a.startswith("--expo="): EXPO = float(a[7:])
    if a.startswith("--focus="): FOCUS = a[8:].lower().split(",")
    if a.startswith("--hide="): HIDE = a[7:].lower().split(",")
    if a.startswith("--res="): RES = tuple(int(x) for x in a[6:].split("x"))
AZ = math.radians(az if az is not None else -58)
EL = math.radians(el if el is not None else 24)

data = np.load(npz_path)
meta = json.loads(npz_path.with_suffix(".json").read_text())
ovr_path = npz_path.with_name(npz_path.stem + ".materials.json")
overrides = json.loads(ovr_path.read_text()) if ovr_path.exists() else {}

bpy.ops.wm.read_factory_settings(use_empty=True)
scn = bpy.context.scene


def hex_rgb(h):
    h = h.lstrip("#")
    srgb = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in srgb]  # to linear


def classify(name, color, given=None):
    if given:
        return given
    if name in overrides:
        return overrides[name]
    n = name.lower()
    r, g, b = [int(color.lstrip("#")[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    sat = colorsys.rgb_to_hsv(r, g, b)[1]
    rules = [
        (r"person|figure|hand|forearm|arm \(scale\)|scale\)", "clay"),
        (r"label|carton|paper|cardboard", "paper"),
        (r"bench|timber|wood|plywood|table|frame, pine|oak|bamboo", "wood"),
        (r"sack|strap|sleeve|textile|fabric|cloth|canvas|mesh bag|band", "fabric"),
        (r"bottle|glass|window|lens|acrylic|polycarbonate|glazing|cover, clear|clear", "clear"),
        (r"film|foil|membrane", "film"),
        (r"phone|screen|display|tablet", "screen"),
        (r"mat\b|rubber|tyre|tire|grip|foot|feet|gasket|seal", "rubber"),
        (r"alumin|stainless|can\b|copper|brass|galvan|chrome|rod|axle|shaft|bolt", "metal"),
        (r"steel|iron|sheet metal|enclosure", "painted" if sat > 0.25 else "metal"),
    ]
    for pat, cls in rules:
        if re.search(pat, n):
            return cls
    return "plastic"


def principled(mat):
    mat.use_nodes = True
    nt = mat.node_tree
    return nt, nt.nodes["Principled BSDF"]


WEAR = "--no-wear" not in sys.argv


def ground_material(nt, I, cls, base=None):
    """Procedural ground and masonry surfaces for site scenes (kit 1.9)."""
    cols = {"concrete": ((0.3, 0.29, 0.27), (0.55, 0.54, 0.5), 0.85), "roof": ((0.42, 0.39, 0.35), (0.56, 0.52, 0.46), 0.9),
            "mud": ((0.07, 0.055, 0.04), (0.16, 0.12, 0.085), 0.25), "sand": ((0.42, 0.35, 0.24), (0.6, 0.52, 0.38), 0.9),
            "soil": ((0.12, 0.09, 0.06), (0.22, 0.17, 0.11), 0.9), "grass": ((0.07, 0.11, 0.03), (0.16, 0.22, 0.07), 0.8),
            "workshop": ((0.3, 0.3, 0.3), (0.42, 0.42, 0.41), 0.55)}
    lo, hi, rough = cols.get(cls, cols["concrete"])
    tc = nt.nodes.new("ShaderNodeTexCoord")
    n1 = nt.nodes.new("ShaderNodeTexNoise"); n1.inputs["Scale"].default_value = 1.2; n1.inputs["Detail"].default_value = 12
    n2 = nt.nodes.new("ShaderNodeTexNoise"); n2.inputs["Scale"].default_value = 60; n2.inputs["Detail"].default_value = 8
    n3 = nt.nodes.new("ShaderNodeTexNoise"); n3.inputs["Scale"].default_value = 9; n3.inputs["Detail"].default_value = 4
    for n in (n1, n2, n3):
        nt.links.new(tc.outputs["Object"], n.inputs["Vector"])
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].color = lo + (1,); ramp.color_ramp.elements[1].color = hi + (1,)
    mixf = nt.nodes.new("ShaderNodeMath"); mixf.operation = "MULTIPLY_ADD"; mixf.inputs[1].default_value = 0.5
    nt.links.new(n3.outputs["Fac"], mixf.inputs[0]); nt.links.new(n1.outputs["Fac"], mixf.inputs[2])
    nt.links.new(mixf.outputs["Value"], ramp.inputs["Fac"]); nt.links.new(ramp.outputs["Color"], I["Base Color"])
    b = nt.nodes.new("ShaderNodeBump"); b.inputs["Strength"].default_value = 0.5 if cls != "mud" else 0.25
    nt.links.new(n2.outputs["Fac"], b.inputs["Height"]); nt.links.new(b.outputs["Normal"], I["Normal"])
    if cls == "mud":   # wet sheen in the hollows
        rr = nt.nodes.new("ShaderNodeMapRange"); rr.inputs["To Min"].default_value = 0.32; rr.inputs["To Max"].default_value = 0.75
        nt.links.new(n1.outputs["Fac"], rr.inputs["Value"]); nt.links.new(rr.outputs["Result"], I["Roughness"])
    else:
        I["Roughness"].default_value = rough


def make_material(name, color, cls):
    mat = bpy.data.materials.new(name)
    nt, p = principled(mat)
    base = hex_rgb(color) + [1]
    p.inputs["Base Color"].default_value = base
    I = p.inputs
    if cls == "wood":
        tc = nt.nodes.new("ShaderNodeTexCoord"); mp = nt.nodes.new("ShaderNodeMapping")
        mp.inputs["Scale"].default_value = (0.15, 1, 1)
        wave = nt.nodes.new("ShaderNodeTexWave"); wave.wave_type = "BANDS"; wave.bands_direction = "Y"
        wave.inputs["Scale"].default_value = 40; wave.inputs["Distortion"].default_value = 3
        wave.inputs["Detail"].default_value = 4; wave.inputs["Detail Scale"].default_value = 1.5
        ramp = nt.nodes.new("ShaderNodeValToRGB")
        dark = [c * 0.55 for c in base[:3]] + [1]
        ramp.color_ramp.elements[0].color = dark; ramp.color_ramp.elements[1].color = base
        nt.links.new(tc.outputs["Object"], mp.inputs["Vector"]); nt.links.new(mp.outputs["Vector"], wave.inputs["Vector"])
        nt.links.new(wave.outputs["Fac"], ramp.inputs["Fac"]); nt.links.new(ramp.outputs["Color"], I["Base Color"])
        I["Roughness"].default_value = 0.55
    elif cls == "fabric":
        I["Roughness"].default_value = 0.95; I["Sheen Weight"].default_value = 0.6
        noise = nt.nodes.new("ShaderNodeTexNoise"); noise.inputs["Scale"].default_value = 400
        bump = nt.nodes.new("ShaderNodeBump"); bump.inputs["Strength"].default_value = 0.25
        nt.links.new(noise.outputs["Fac"], bump.inputs["Height"]); nt.links.new(bump.outputs["Normal"], I["Normal"])
    elif cls == "clear":
        I["Transmission Weight"].default_value = 1.0; I["Roughness"].default_value = 0.04
        I["IOR"].default_value = 1.57
        tint = [0.6 + 0.4 * c for c in base[:3]] + [1]
        I["Base Color"].default_value = tint
    elif cls == "metal":
        I["Metallic"].default_value = 1.0; I["Roughness"].default_value = 0.28
        I["Anisotropic"].default_value = 0.5
        I["Base Color"].default_value = [max(c, 0.35) for c in base[:3]] + [1]
    elif cls == "painted":
        I["Roughness"].default_value = 0.38; I["Coat Weight"].default_value = 0.35
        I["Coat Roughness"].default_value = 0.15
        if WEAR:   # kit 1.9: faint wear on sharp edges and roughness variation, so paint reads as paint
            geo = nt.nodes.new("ShaderNodeNewGeometry"); cr = nt.nodes.new("ShaderNodeMapRange")
            cr.inputs["From Min"].default_value = 0.52; cr.inputs["From Max"].default_value = 0.6
            mix = nt.nodes.new("ShaderNodeMix"); mix.data_type = "RGBA"
            mix.inputs["A"].default_value = base; mix.inputs["B"].default_value = (0.32, 0.32, 0.33, 1)
            nt.links.new(geo.outputs["Pointiness"], cr.inputs["Value"]); nt.links.new(cr.outputs["Result"], mix.inputs["Factor"])
            nt.links.new(mix.outputs["Result"], I["Base Color"])
    elif cls == "rubber":
        I["Roughness"].default_value = 0.85
    elif cls == "screen":
        I["Roughness"].default_value = 0.08; I["Coat Weight"].default_value = 1.0
        I["Coat Roughness"].default_value = 0.02
    elif cls == "paper":
        I["Roughness"].default_value = 0.75
    elif cls == "film":
        I["Roughness"].default_value = 0.3; I["Transmission Weight"].default_value = 0.6
        I["Alpha"].default_value = 0.85
    elif cls == "emissive":
        I["Base Color"].default_value = (0.02, 0.02, 0.025, 1); I["Roughness"].default_value = 0.1
        I["Emission Color"].default_value = base; I["Emission Strength"].default_value = 2.5
        I["Coat Weight"].default_value = 1.0
    elif cls == "clay":
        I["Base Color"].default_value = (0.33, 0.33, 0.34, 1); I["Roughness"].default_value = 0.6
    elif cls in ("galvanised", "stainless", "aluminium", "cast_metal"):
        I["Metallic"].default_value = 1.0
        rough = {"galvanised": 0.42, "stainless": 0.22, "aluminium": 0.3, "cast_metal": 0.55}[cls]
        vor = nt.nodes.new("ShaderNodeTexVoronoi"); vor.inputs["Scale"].default_value = 60 if cls == "galvanised" else 900
        rr = nt.nodes.new("ShaderNodeMapRange"); rr.inputs["To Min"].default_value = rough * 0.75; rr.inputs["To Max"].default_value = rough * 1.25
        nt.links.new(vor.outputs["Distance"], rr.inputs["Value"]); nt.links.new(rr.outputs["Result"], I["Roughness"])
        if cls == "stainless":
            I["Anisotropic"].default_value = 0.6
        if cls == "cast_metal":
            n2 = nt.nodes.new("ShaderNodeTexNoise"); n2.inputs["Scale"].default_value = 1500
            b2 = nt.nodes.new("ShaderNodeBump"); b2.inputs["Strength"].default_value = 0.15
            nt.links.new(n2.outputs["Fac"], b2.inputs["Height"]); nt.links.new(b2.outputs["Normal"], I["Normal"])
    elif cls in ("hdpe", "plastic_tank", "silver_paint", "matte_black"):
        I["Roughness"].default_value = {"hdpe": 0.55, "plastic_tank": 0.45, "silver_paint": 0.4, "matte_black": 0.85}[cls]
        I["Specular IOR Level"].default_value = 0.4
        if cls == "silver_paint":
            I["Metallic"].default_value = 0.7
        if cls in ("hdpe", "plastic_tank"):
            I["Subsurface Weight"].default_value = 0.05
        n2 = nt.nodes.new("ShaderNodeTexNoise"); n2.inputs["Scale"].default_value = 2500; n2.inputs["Detail"].default_value = 2
        b2 = nt.nodes.new("ShaderNodeBump"); b2.inputs["Strength"].default_value = 0.06
        nt.links.new(n2.outputs["Fac"], b2.inputs["Height"]); nt.links.new(b2.outputs["Normal"], I["Normal"])
    elif cls == "painted_white":
        I["Roughness"].default_value = 0.35; I["Coat Weight"].default_value = 0.2
    elif cls == "mirror":
        I["Metallic"].default_value = 1.0; I["Roughness"].default_value = 0.04
        I["Base Color"].default_value = (0.92, 0.93, 0.94, 1)
    elif cls in ("plywood", "bamboo"):
        tc = nt.nodes.new("ShaderNodeTexCoord"); mp = nt.nodes.new("ShaderNodeMapping")
        mp.inputs["Scale"].default_value = (0.08, 1, 1) if cls == "plywood" else (1, 1, 0.05)
        wave = nt.nodes.new("ShaderNodeTexWave"); wave.wave_type = "BANDS"
        wave.bands_direction = "Y" if cls == "plywood" else "Z"
        wave.inputs["Scale"].default_value = 30 if cls == "plywood" else 4
        wave.inputs["Distortion"].default_value = 6 if cls == "plywood" else 1
        wave.inputs["Detail"].default_value = 5
        ramp = nt.nodes.new("ShaderNodeValToRGB")
        ramp.color_ramp.elements[0].color = [c * 0.7 for c in base[:3]] + [1]; ramp.color_ramp.elements[1].color = base
        nt.links.new(tc.outputs["Object"], mp.inputs["Vector"]); nt.links.new(mp.outputs["Vector"], wave.inputs["Vector"])
        nt.links.new(wave.outputs["Fac"], ramp.inputs["Fac"]); nt.links.new(ramp.outputs["Color"], I["Base Color"])
        I["Roughness"].default_value = 0.6 if cls == "plywood" else 0.35
        if cls == "bamboo":
            I["Coat Weight"].default_value = 0.4
    elif cls in ("coir", "rope"):
        tc = nt.nodes.new("ShaderNodeTexCoord"); mp = nt.nodes.new("ShaderNodeMapping")
        mp.inputs["Scale"].default_value = (1, 1, 0.08)
        n2 = nt.nodes.new("ShaderNodeTexNoise"); n2.inputs["Scale"].default_value = 900 if cls == "coir" else 400
        n2.inputs["Detail"].default_value = 8; n2.inputs["Roughness"].default_value = 0.8
        ramp = nt.nodes.new("ShaderNodeValToRGB")
        ramp.color_ramp.elements[0].color = [c * 0.45 for c in base[:3]] + [1]; ramp.color_ramp.elements[1].color = [min(1, c * 1.3) for c in base[:3]] + [1]
        b2 = nt.nodes.new("ShaderNodeBump"); b2.inputs["Strength"].default_value = 0.9
        nt.links.new(tc.outputs["Object"], mp.inputs["Vector"]); nt.links.new(mp.outputs["Vector"], n2.inputs["Vector"])
        nt.links.new(n2.outputs["Fac"], ramp.inputs["Fac"]); nt.links.new(ramp.outputs["Color"], I["Base Color"])
        nt.links.new(n2.outputs["Fac"], b2.inputs["Height"]); nt.links.new(b2.outputs["Normal"], I["Normal"])
        I["Roughness"].default_value = 0.95; I["Sheen Weight"].default_value = 0.5
    elif cls in ("concrete", "mud", "sand", "soil", "grass"):
        ground_material(nt, I, cls, base)
    elif cls == "water":
        I["Base Color"].default_value = (0.05, 0.06, 0.045, 1); I["Roughness"].default_value = 0.12
        I["Transmission Weight"].default_value = 0.0; I["IOR"].default_value = 1.33; I["Specular IOR Level"].default_value = 0.35
        n2 = nt.nodes.new("ShaderNodeTexNoise"); n2.inputs["Scale"].default_value = 6
        b2 = nt.nodes.new("ShaderNodeBump"); b2.inputs["Strength"].default_value = 0.08
        nt.links.new(n2.outputs["Fac"], b2.inputs["Height"]); nt.links.new(b2.outputs["Normal"], I["Normal"])
    else:  # plastic
        I["Roughness"].default_value = 0.42; I["Specular IOR Level"].default_value = 0.45
    return mat


objs = []
for i, m in enumerate(meta["parts"]):
    if any(m["name"].lower().startswith(h) for h in HIDE):
        continue
    v, f = data[f"v{i}"], data[f"f{i}"]
    me = bpy.data.meshes.new(m["name"])
    me.from_pydata(v.tolist(), [], f.tolist())
    me.update()
    ob = bpy.data.objects.new(m["name"], me)
    scn.collection.objects.link(ob)
    bpy.context.view_layer.objects.active = ob
    ob.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.remove_doubles(threshold=0.00005)
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.mode_set(mode="OBJECT")
    ob.select_set(False)
    me.shade_smooth()
    me.set_sharp_from_angle(angle=math.radians(32))
    cls = classify(m["name"], m["color"], m.get("material"))
    if cls not in ("clear", "film"):
        bev = ob.modifiers.new("bevel", "BEVEL")
        bev.width = 0.0003 if PRODUCT else 0.0012; bev.segments = 3; bev.limit_method = "ANGLE"
        bev.angle_limit = math.radians(40); bev.harden_normals = False
        bev.use_clamp_overlap = True
        ob.modifiers.new("wn", "WEIGHTED_NORMAL").keep_sharp = True
    me.materials.append(make_material(m["name"], m["color"], cls))
    objs.append(ob)
    print(f"{m['name']}: {cls}")

# bounds
pts = [ob.matrix_world @ Vector(c) for ob in objs for c in ob.bound_box]
lo = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
hi = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
ctr = (lo + hi) / 2
size = (hi - lo).length

if SCENE == "outdoor":
    # kit 1.9 site scene: physical sky and sun, a large procedural ground, optional still water
    gname = GROUND or "soil"
    fm = bpy.data.materials.new("ground"); nt, p = principled(fm)
    ground_material(nt, p.inputs, gname)
    relief = {"mud": 0.07, "soil": 0.035, "sand": 0.03, "grass": 0.03}.get(gname, 0.0)
    _po = [o for o in objs if "(site)" not in o.name] or objs
    _pp = [o.matrix_world @ Vector(c) for o in _po for c in o.bound_box]
    psize = (Vector((max(q.x for q in _pp), max(q.y for q in _pp), max(q.z for q in _pp)))
             - Vector((min(q.x for q in _pp), min(q.y for q in _pp), min(q.z for q in _pp)))).length
    near = max(psize * 10, 16.0)   # the relief grid follows the product, not the (possibly huge) site
    pc = Vector((sum(q.x for q in _pp) / len(_pp), sum(q.y for q in _pp) / len(_pp), 0))
    gz = GROUND_Z if GROUND_Z is not None else lo.z
    # far ground: flat plane to the horizon, kept below the deepest hollow of the near ground
    bpy.ops.mesh.primitive_plane_add(size=min(max(size * 60, 200), 1800), location=(pc.x, pc.y, gz - relief * 0.5 - 0.006))
    far = bpy.context.active_object; far.data.materials.append(fm)
    # near ground: a displaced grid, so mud and soil have real relief and still water collects in the hollows
    bpy.ops.mesh.primitive_grid_add(x_subdivisions=220, y_subdivisions=220, size=near, location=(pc.x, pc.y, gz))
    floor = bpy.context.active_object; floor.data.materials.append(fm)
    if relief:
        tex = bpy.data.textures.new("relief", "CLOUDS"); tex.noise_scale = 0.9; tex.noise_depth = 4
        dm = floor.modifiers.new("relief", "DISPLACE"); dm.texture = tex; dm.texture_coords = "GLOBAL"
        dm.strength = relief; dm.mid_level = 0.5
        # keep the ground flat under the product and under each scale figure, so nothing floats or sinks; site
        # context parts ("(site)" in the name) are built to reach below the ground and keep the relief
        def _box(obs):
            q = [o.matrix_world @ Vector(c) for o in obs for c in o.bound_box]
            return (min(v.x for v in q), min(v.y for v in q), max(v.x for v in q), max(v.y for v in q))
        prod = [o for o in objs if "(site)" not in o.name and "(scale)" not in o.name]
        boxes = ([_box(prod)] if prod else []) + [_box([o]) for o in objs if "(scale)" in o.name]
        vg = floor.vertex_groups.new(name="relief")
        for v in floor.data.vertices:
            w = floor.matrix_world @ v.co
            dmin = min((max(b[0] - w.x, 0, w.x - b[2]) ** 2 + max(b[1] - w.y, 0, w.y - b[3]) ** 2) ** 0.5 for b in boxes) if boxes else 9.0
            vg.add([v.index], min(1.0, max(0.0, (dmin - 0.12) / 0.7)), "REPLACE")
        dm.vertex_group = "relief"
        floor.data.shade_smooth()
    if WATER_Z is not None:
        bpy.ops.mesh.primitive_plane_add(size=near * 0.98, location=(pc.x, pc.y, gz + WATER_Z))
        wat = bpy.context.active_object
        wm = make_material("water", "#3E5A5A", "water"); wat.data.materials.append(wm)
    world = bpy.data.worlds.new("sky"); scn.world = world; world.use_nodes = True
    sky = world.node_tree.nodes.new("ShaderNodeTexSky"); sky.sky_type = "MULTIPLE_SCATTERING"
    sun_el = math.radians(SUN[0]); sun_az = math.radians(SUN[1] if SUN[1] is not None else math.degrees(AZ) - 70)
    sky.sun_elevation = sun_el; sky.sun_rotation = sun_az; sky.altitude = 50; sky.air_density = 1.0; sky.aerosol_density = 1.6
    sky.sun_disc = False
    bg = world.node_tree.nodes["Background"]; bg.inputs["Strength"].default_value = 0.06
    world.node_tree.links.new(sky.outputs["Color"], bg.inputs["Color"])
    sun = bpy.data.lights.new("sun", "SUN"); sun.energy = 2.6; sun.angle = math.radians(1.2); sun.color = (1.0, 0.96, 0.9)
    so = bpy.data.objects.new("sun", sun); scn.collection.objects.link(so)
    sd = Vector((math.cos(sun_el) * math.cos(sun_az), math.cos(sun_el) * math.sin(sun_az), math.sin(sun_el)))
    so.rotation_euler = (-sd).to_track_quat("-Z", "Y").to_euler()
    EXPO_SCENE = 1.0
else:
    # studio floor with a curved sweep far behind, so the horizon never shows
    bpy.ops.mesh.primitive_plane_add(size=size * 12, location=(ctr.x, ctr.y, GROUND_Z if GROUND_Z is not None else lo.z))
    floor = bpy.context.active_object
    fm = bpy.data.materials.new("floor"); nt, p = principled(fm)
    p.inputs["Base Color"].default_value = (0.5, 0.49, 0.47, 1); p.inputs["Roughness"].default_value = 0.4
    noise = nt.nodes.new("ShaderNodeTexNoise"); noise.inputs["Scale"].default_value = 30; noise.inputs["Detail"].default_value = 8
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].color = (0.44, 0.43, 0.41, 1); ramp.color_ramp.elements[1].color = (0.54, 0.53, 0.51, 1)
    nt.links.new(noise.outputs["Fac"], ramp.inputs["Fac"]); nt.links.new(ramp.outputs["Color"], p.inputs["Base Color"])
    if PRODUCT:   # seamless white product-studio floor
        ramp.color_ramp.elements[0].color = (0.52, 0.53, 0.55, 1); ramp.color_ramp.elements[1].color = (0.56, 0.57, 0.59, 1)
        p.inputs["Roughness"].default_value = 0.6
    floor.data.materials.append(fm)

    # world: soft neutral studio ambient
    world = bpy.data.worlds.new("studio"); scn.world = world; world.use_nodes = True
    bg = world.node_tree.nodes["Background"]
    bg.inputs["Color"].default_value = (0.78, 0.8, 0.83, 1); bg.inputs["Strength"].default_value = 0.9 if PRODUCT else 0.35

    # lights (three-point softboxes), scaled to the scene
    def area(name, direction_az, direction_el, dist, power, sz, color=(1, 1, 1)):
        a, e = math.radians(direction_az), math.radians(direction_el)
        d = Vector((math.cos(e) * math.cos(a), math.cos(e) * math.sin(a), math.sin(e)))
        L = bpy.data.lights.new(name, "AREA"); L.shape = "DISK"; L.size = sz; L.energy = power; L.color = color
        ob = bpy.data.objects.new(name, L); scn.collection.objects.link(ob)
        ob.location = ctr + d * dist
        ob.rotation_euler = (-d).to_track_quat("-Z", "Y").to_euler()

    D = max(size, 1.0)
    az_deg = math.degrees(AZ)
    area("key", az_deg - 35, 50, D * 1.4, EXPO * 75 * D ** 2, D * 0.9, (1.0, 0.96, 0.9))
    area("fill", az_deg + 70, 25, D * 1.6, EXPO * 22 * D ** 2, D * 1.2, (0.9, 0.95, 1.0))
    area("rim", az_deg + 180, 40, D * 1.5, EXPO * 50 * D ** 2, D * 0.8)
    area("top", 0, 89, D * 1.3, EXPO * 18 * D ** 2, D * 1.5)


# camera
cam_data = bpy.data.cameras.new("cam"); cam_data.lens = LENS or 55
cam = bpy.data.objects.new("cam", cam_data); scn.collection.objects.link(cam); scn.camera = cam
d = Vector((math.cos(EL) * math.cos(AZ), math.cos(EL) * math.sin(AZ), math.sin(EL)))
cam.location = ctr + d * size * 3
cam.rotation_euler = (-d).to_track_quat("-Z", "Y").to_euler()
W, H = RES or ((1280, 960) if preview else (2560, 1920))
scn.render.resolution_x, scn.render.resolution_y = W, H
bpy.context.view_layer.update()
fobjs = [o for o in objs if FOCUS is None or any(o.name.lower().startswith(k) for k in FOCUS)]
if SCENE == "outdoor" and FOCUS is None and any("(site)" not in o.name for o in fobjs):
    # site scenes frame the product and the scale figure; the site context runs out of the picture
    fobjs = [o for o in fobjs if "(site)" not in o.name]
    fpts0 = [ob.matrix_world @ Vector(c) for ob in fobjs for c in ob.bound_box]
    ctr = sum(fpts0, Vector()) / len(fpts0)
    cam.location = ctr + d * size * 3
fpts = [ob.matrix_world @ Vector(c) for ob in fobjs for c in ob.bound_box]
if FOCUS:
    ctr = sum(fpts, Vector()) / len(fpts)
    cam.location = ctr + d * size * 3
    cam_data.lens = 85
coords = [c for p in fpts for c in p]
loc, _ = cam.camera_fit_coords(bpy.context.evaluated_depsgraph_get(), coords)
cam.location = ctr + (Vector(loc) - ctr) * (1.45 if SCENE == "outdoor" else 1.3 if PRODUCT else 1.07)   # site scenes: room for context
cam_data.dof.use_dof = True
cam_data.dof.focus_distance = (cam.location - ctr).length
cam_data.dof.aperture_fstop = 16 if PRODUCT else 11
if SCENE == "outdoor":
    cam_data.dof.aperture_fstop = 8
    cam_data.clip_end = 1000

# render settings
scn.render.engine = "CYCLES"
c = scn.cycles
c.device = "CPU"
if "--gpu" in sys.argv:   # Apple Silicon (Metal) or other GPU when run in the Blender app
    prefs = bpy.context.preferences.addons["cycles"].preferences
    for kind in ("METAL", "OPTIX", "CUDA", "HIP", "ONEAPI"):
        try:
            prefs.compute_device_type = kind; prefs.get_devices()
            if any(d.type == kind for d in prefs.devices):
                for d in prefs.devices: d.use = True
                c.device = "GPU"; print("GPU:", kind); break
        except TypeError:
            continue
c.samples = 48 if preview else (96 if PRODUCT else 192); c.use_adaptive_sampling = True
c.adaptive_threshold = 0.02 if preview else 0.008
c.use_denoising = True; c.denoiser = "OPENIMAGEDENOISE"
c.max_bounces = 8; c.transmission_bounces = 8; c.glossy_bounces = 4
scn.view_settings.view_transform = "AgX"; scn.view_settings.look = "AgX - Medium High Contrast"
if SCENE == "outdoor":
    scn.view_settings.look = "AgX - Medium High Contrast"; scn.view_settings.exposure = -0.2
scn.render.threads_mode = "AUTO"
scn.render.image_settings.file_format = "PNG"
scn.render.filepath = str(out)
bpy.ops.render.render(write_still=True)
print("wrote", out)
