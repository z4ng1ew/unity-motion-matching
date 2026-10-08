import bpy, os

src = os.path.expanduser("~/unity_locomotion/anims")
dst = os.path.expanduser("~/unity_locomotion/bvh")
os.makedirs(dst, exist_ok=True)

files = sorted(f for f in os.listdir(src) if f.endswith(".fbx"))
for f in files:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.fbx(filepath=os.path.join(src, f), ignore_leaf_bones=True)
    arm = next(o for o in bpy.context.scene.objects if o.type == "ARMATURE")
    bpy.context.view_layer.objects.active = arm
    arm.select_set(True)
    act = arm.animation_data.action if arm.animation_data else None
    start, end = (int(act.frame_range[0]), int(act.frame_range[1])) if act else (0, 0)
    bpy.context.scene.render.fps = 30
    out = os.path.join(dst, f.replace(".fbx", ".bvh"))
    bpy.ops.export_anim.bvh(filepath=out, frame_start=start, frame_end=end,
                            rotate_mode='YXZ', root_transform_only=True, global_scale=1.0)
    print("OK:", f, start, end)
