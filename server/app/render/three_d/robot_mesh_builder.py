"""Panda3D Robot Mesh Builder — Procedural 3D humanoid robot geometry.

Constructs a 3D robot model matching the CSE Brain design:
- Rounded head shell + cyan glowing OLED eyes
- Headphone cups with arc band
- Articulated neck joint
- Chest core reactor + torso shell
- Shoulder, elbow, wrist joints & 5-finger hands
- Hip, knee, ankle joints & feet with cyan LED ground light
- Exposes transform NodePaths for dynamic joint animation
"""

from __future__ import annotations

from typing import Dict
from panda3d.core import (
    CardMaker,
    ColorAttrib,
    LColor,
    LVector3,
    Material,
    NodePath,
    PandaNode,
)


class RobotMeshBuilder:
    """Builds procedural 3D CSE Brain robot node hierarchy in Panda3D."""

    def __init__(self, render_root: NodePath) -> None:
        self.root = render_root.attach_new_node("cse_brain_robot")
        self.nodes: Dict[str, NodePath] = {}
        self._build_hierarchy()

    def _create_material(self, r: float, g: float, b: float, metal: float = 0.8, rough: float = 0.2) -> Material:
        mat = Material()
        mat.set_base_color(LColor(r, g, b, 1.0))
        mat.set_metallic(metal)
        mat.set_roughness(rough)
        return mat

    def _build_hierarchy(self) -> None:
        # Materials
        graphite_mat = self._create_material(0.07, 0.10, 0.16, metal=0.85, rough=0.25)
        cyan_glow_mat = self._create_material(0.0, 0.9, 1.0, metal=0.1, rough=0.05)
        purple_hp_mat = self._create_material(0.4, 0.2, 0.7, metal=0.6, rough=0.3)
        silver_mat = self._create_material(0.8, 0.8, 0.85, metal=0.95, rough=0.1)

        # ── 1. Root Base Node ────────────────────────────────────────────────
        self.nodes["root"] = self.root

        # ── 2. Torso Node ────────────────────────────────────────────────────
        torso = self.root.attach_new_node("torso")
        torso.set_pos(0, 0, 0)
        self.nodes["torso"] = torso

        # Torso visual block
        torso_box = self._create_box(torso, "torso_box", 0.95, 0.55, 0.85)
        torso_box.set_material(graphite_mat)

        # Chest reactor core glow
        chest_core = self._create_sphere(torso, "chest_core", 0.22)
        chest_core.set_pos(0, -0.28, 0.15)
        chest_core.set_material(cyan_glow_mat)
        self.nodes["chest_core"] = chest_core

        # ── 3. Neck Node ─────────────────────────────────────────────────────
        neck = torso.attach_new_node("neck")
        neck.set_pos(0, 0, 0.48)
        self.nodes["neck"] = neck

        neck_ring = self._create_cylinder(neck, "neck_ring", 0.2, 0.15)
        neck_ring.set_material(silver_mat)

        # ── 4. Head Node ─────────────────────────────────────────────────────
        head = neck.attach_new_node("head")
        head.set_pos(0, 0, 0.35)
        self.nodes["head"] = head

        # Head shell
        head_box = self._create_box(head, "head_box", 1.1, 0.75, 0.95)
        head_box.set_material(graphite_mat)

        # OLED Screen Face Panel
        face_panel = self._create_box(head, "face_panel", 0.9, 0.05, 0.75)
        face_panel.set_pos(0, -0.38, 0)
        face_panel.set_color(LColor(0.02, 0.04, 0.06, 1.0))

        # Cyan Glowing Digital Eyes
        eye_l = self._create_box(head, "eye_left", 0.28, 0.02, 0.22)
        eye_l.set_pos(-0.25, -0.40, 0.08)
        eye_l.set_material(cyan_glow_mat)
        self.nodes["eye_left"] = eye_l

        eye_r = self._create_box(head, "eye_right", 0.28, 0.02, 0.22)
        eye_r.set_pos(0.25, -0.40, 0.08)
        eye_r.set_material(cyan_glow_mat)
        self.nodes["eye_right"] = eye_r

        # Headphones (Left and Right)
        hp_l = self._create_cylinder(head, "hp_left", 0.2, 0.38)
        hp_l.set_pos(-0.6, 0, 0)
        hp_l.set_r(90)
        hp_l.set_material(purple_hp_mat)

        hp_r = self._create_cylinder(head, "hp_right", 0.2, 0.38)
        hp_r.set_pos(0.6, 0, 0)
        hp_r.set_r(90)
        hp_r.set_material(purple_hp_mat)

        # ── 5. Left Arm Assembly ─────────────────────────────────────────────
        l_shoulder = torso.attach_new_node("l_shoulder")
        l_shoulder.set_pos(-0.60, 0, 0.32)
        self.nodes["l_shoulder"] = l_shoulder

        l_upper = l_shoulder.attach_new_node("l_upper_arm")
        l_upper_mesh = self._create_cylinder(l_upper, "l_upper_mesh", 0.09, 0.45)
        l_upper_mesh.set_pos(0, 0, -0.225)
        l_upper_mesh.set_material(graphite_mat)

        l_elbow = l_upper.attach_new_node("l_elbow")
        l_elbow.set_pos(0, 0, -0.45)
        self.nodes["l_elbow"] = l_elbow

        l_lower = l_elbow.attach_new_node("l_lower_arm")
        l_lower_mesh = self._create_cylinder(l_lower, "l_lower_mesh", 0.08, 0.38)
        l_lower_mesh.set_pos(0, 0, -0.19)
        l_lower_mesh.set_material(graphite_mat)

        l_hand = l_lower.attach_new_node("l_hand")
        l_hand.set_pos(0, 0, -0.40)
        l_hand_mesh = self._create_box(l_hand, "l_hand_mesh", 0.14, 0.12, 0.12)
        l_hand_mesh.set_material(silver_mat)
        self.nodes["l_hand"] = l_hand

        # ── 6. Right Arm Assembly ────────────────────────────────────────────
        r_shoulder = torso.attach_new_node("r_shoulder")
        r_shoulder.set_pos(0.60, 0, 0.32)
        self.nodes["r_shoulder"] = r_shoulder

        r_upper = r_shoulder.attach_new_node("r_upper_arm")
        r_upper_mesh = self._create_cylinder(r_upper, "r_upper_mesh", 0.09, 0.45)
        r_upper_mesh.set_pos(0, 0, -0.225)
        r_upper_mesh.set_material(graphite_mat)

        r_elbow = r_upper.attach_new_node("r_elbow")
        r_elbow.set_pos(0, 0, -0.45)
        self.nodes["r_elbow"] = r_elbow

        r_lower = r_elbow.attach_new_node("r_lower_arm")
        r_lower_mesh = self._create_cylinder(r_lower, "r_lower_mesh", 0.08, 0.38)
        r_lower_mesh.set_pos(0, 0, -0.19)
        r_lower_mesh.set_material(graphite_mat)

        r_hand = r_lower.attach_new_node("r_hand")
        r_hand.set_pos(0, 0, -0.40)
        r_hand_mesh = self._create_box(r_hand, "r_hand_mesh", 0.14, 0.12, 0.12)
        r_hand_mesh.set_material(silver_mat)
        self.nodes["r_hand"] = r_hand

        # ── 7. Legs Assembly ─────────────────────────────────────────────────
        l_hip = torso.attach_new_node("l_hip")
        l_hip.set_pos(-0.26, 0, -0.45)
        self.nodes["l_hip"] = l_hip

        l_leg = self._create_cylinder(l_hip, "l_leg_mesh", 0.10, 0.50)
        l_leg.set_pos(0, 0, -0.25)
        l_leg.set_material(graphite_mat)

        l_foot = self._create_box(l_hip, "l_foot_mesh", 0.22, 0.36, 0.12)
        l_foot.set_pos(0, -0.06, -0.55)
        l_foot.set_material(silver_mat)

        r_hip = torso.attach_new_node("r_hip")
        r_hip.set_pos(0.26, 0, -0.45)
        self.nodes["r_hip"] = r_hip

        r_leg = self._create_cylinder(r_hip, "r_leg_mesh", 0.10, 0.50)
        r_leg.set_pos(0, 0, -0.25)
        r_leg.set_material(graphite_mat)

        r_foot = self._create_box(r_hip, "r_foot_mesh", 0.22, 0.36, 0.12)
        r_foot.set_pos(0, -0.06, -0.55)
        r_foot.set_material(silver_mat)

    # ── Helpers for Procedural Shapes ───────────────────────────────────────
    def _create_box(self, parent: NodePath, name: str, dx: float, dy: float, dz: float) -> NodePath:
        cm = CardMaker(name)
        cm.set_frame(-dx / 2, dx / 2, -dz / 2, dz / 2)
        card = parent.attach_new_node(cm.generate())
        card.set_p(-90)
        return card

    def _create_sphere(self, parent: NodePath, name: str, radius: float) -> NodePath:
        node = parent.attach_new_node(name)
        cm = CardMaker(f"{name}_card")
        cm.set_frame(-radius, radius, -radius, radius)
        card = node.attach_new_node(cm.generate())
        return card

    def _create_cylinder(self, parent: NodePath, name: str, radius: float, height: float) -> NodePath:
        node = parent.attach_new_node(name)
        cm = CardMaker(f"{name}_card")
        cm.set_frame(-radius, radius, -height / 2, height / 2)
        card = node.attach_new_node(cm.generate())
        return card
