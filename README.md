# Motion Matching in Unity — Mixamo Pipeline

Locomotion system based on **Motion Matching** in Unity 6 (URP), built on the open-source
[MotionMatching](https://github.com/JLPM22/MotionMatching) package by JLPM22.
My work: converting Mixamo mocap into a format the package accepts, building a custom
motion database, tuning the controller and debugging animation artifacts.

> Status: work in progress.

## What I did

**1. FBX → BVH conversion pipeline** — `Tools/fbx2bvh.py`
- Batch conversion of Mixamo FBX clips to BVH via the Blender Python API (headless).
- Matched the package format: rotation order **YXZ**, 3 channels per joint (root also has position).
- Unit scale handling (Mixamo exports in centimeters → `UnitScale 0.01`).

```bash
blender --background --python Tools/fbx2bvh.py
```

**2. Custom motion database** — `Assets/MMAnimations/`
- Locomotion clips: idle, walk, run, walk start, turns, 180° turns.
- Skeleton mapping Mixamo → Mecanim (22 core bones).
- Hips local vectors (forward / up) for correct root orientation.
- Trajectory and pose features (future position/direction, feet, hips).

**3. Debugging and tuning**

| Artifact | Cause | Fix |
|---|---|---|
| Twisted limbs | BVH rotation order XYZ instead of YXZ | Re-exported BVH with YXZ, 3 channels per joint |
| Character lagging behind trajectory | Clamping disabled in controller | Enabled clamping, tuned max distance and adjustment ratios |
| Leaning back / legs forward on turns | Stop clips matched during direction change | Removed stop and in-place turn clips from the database |
| Database not applied at runtime | Prefab override with demo database | Replaced reference in prefab |

## Project structure

```
Assets/
  Character/         Y Bot (Humanoid)
  Animations/        Mixamo FBX clips
  MMAnimations/
    BVH/             converted clips (.txt for the package)
    Data/            AnimationData assets
    YBotData.asset   motion database
Tools/
  fbx2bvh.py         Blender batch converter
```

## Run

1. Unity 6000.x, URP.
2. Open `Assets/Samples/Motion Matching/0.3.2/Examples/Scenes/00_Basic/ExampleSimpleMMController`.
3. Select `Assets/MMAnimations/YBotData` → **Generate Databases**.
4. Play, control with **WASD**.

## Credits

- Motion Matching package: [JLPM22/MotionMatching](https://github.com/JLPM22/MotionMatching).
- Animations and character: [Mixamo](https://www.mixamo.com).
