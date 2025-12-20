"""
File I/O - Load and save scene data in JSON format.

Supports two formats:
1. Planner format (.tapln) - includes x,y positions for editor layout
2. Game format (scenes.json) - standard format without positions
"""

import json


def load_scenes(filepath, include_positions=True):
    """
    Load scenes from a JSON file.

    Args:
        filepath: Path to the JSON file
        include_positions: If True, expects x,y coords (planner format)
                          If False, assigns default positions (game format)

    Returns:
        Dictionary of {scene_id: scene_data}
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    scenes = {}

    # Handle both array format (game) and dict format (planner)
    if isinstance(data, list):
        # Game format: array of scene objects
        for i, scene in enumerate(data):
            scene_id = scene.get("id")
            if not scene_id:
                continue

            scene_data = {
                "id": scene_id,
                "background": scene.get("background", ""),
                "music": scene.get("music", ""),
                "text": scene.get("text", ""),
                "choices": scene.get("choices", []),
            }

            if include_positions:
                scene_data["x"] = scene.get("x", 100 + (i % 5) * 200)
                scene_data["y"] = scene.get("y", 100 + (i // 5) * 150)
            else:
                # Assign grid positions when importing from game format
                scene_data["x"] = 100 + (i % 5) * 200
                scene_data["y"] = 100 + (i // 5) * 150

            scenes[scene_id] = scene_data

    elif isinstance(data, dict):
        # Could be planner format (dict with scene_ids as keys)
        # or a single scene object
        if "id" in data:
            # Single scene object (unlikely but handle it)
            scene_id = data["id"]
            scenes[scene_id] = {
                "id": scene_id,
                "background": data.get("background", ""),
                "music": data.get("music", ""),
                "text": data.get("text", ""),
                "choices": data.get("choices", []),
                "x": data.get("x", 100),
                "y": data.get("y", 100),
            }
        else:
            # Dict format with scene_ids as keys (planner native format)
            for scene_id, scene in data.items():
                scenes[scene_id] = {
                    "id": scene_id,
                    "background": scene.get("background", ""),
                    "music": scene.get("music", ""),
                    "text": scene.get("text", ""),
                    "choices": scene.get("choices", []),
                    "x": scene.get("x", 100),
                    "y": scene.get("y", 100),
                }

    return scenes


def save_scenes(filepath, scenes, include_positions=True):
    """
    Save scenes to a JSON file.

    Args:
        filepath: Path to save to
        scenes: Dictionary of {scene_id: scene_data}
        include_positions: If True, save in planner format with x,y
                          If False, save in game format (array, no positions)
    """
    if include_positions:
        # Planner format: dict with positions
        data = {}
        for scene_id, scene in scenes.items():
            data[scene_id] = {
                "id": scene_id,
                "background": scene.get("background", ""),
                "music": scene.get("music", ""),
                "text": scene.get("text", ""),
                "choices": scene.get("choices", []),
                "x": scene.get("x", 0),
                "y": scene.get("y", 0),
            }
    else:
        # Game format: array without positions
        data = []
        for scene_id, scene in scenes.items():
            data.append({
                "id": scene_id,
                "background": scene.get("background", ""),
                "music": scene.get("music", ""),
                "text": scene.get("text", ""),
                "choices": scene.get("choices", []),
            })

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def scenes_to_graph(scenes):
    """
    Convert scenes dict to a graph representation for analysis.

    Returns:
        Tuple of (nodes, edges) where:
        - nodes is a set of scene_ids
        - edges is a list of (from_id, to_id, label) tuples
    """
    nodes = set(scenes.keys())
    edges = []

    for scene_id, scene in scenes.items():
        for choice in scene.get("choices", []):
            target = choice.get("next_scene")
            label = choice.get("label", "")
            if target:
                edges.append((scene_id, target, label))

    return nodes, edges


def graph_to_scenes(nodes, edges, existing_scenes=None):
    """
    Create scenes from graph representation.

    Args:
        nodes: Set of scene_ids
        edges: List of (from_id, to_id, label) tuples
        existing_scenes: Optional existing scene data to preserve

    Returns:
        Dictionary of {scene_id: scene_data}
    """
    existing = existing_scenes or {}
    scenes = {}

    for node_id in nodes:
        if node_id in existing:
            scenes[node_id] = dict(existing[node_id])
            scenes[node_id]["choices"] = []
        else:
            scenes[node_id] = {
                "id": node_id,
                "background": "",
                "music": "",
                "text": "",
                "choices": [],
                "x": 100,
                "y": 100,
            }

    for from_id, to_id, label in edges:
        if from_id in scenes:
            scenes[from_id]["choices"].append({
                "label": label or "Continue",
                "next_scene": to_id
            })

    return scenes
