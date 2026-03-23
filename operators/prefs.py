from bpy.props import EnumProperty


settings = EnumProperty(
    name="Mirror Options",
    description="Enable/Disable what to mirror",
    items=[
        ("Location", "Location", "Mirror X Location"),
        ("Rotation", "Rotation", "Mirror Bone Rotations"),
        ("Scale", "Scale", "Mirror Bone Scaling"),
        ("Optimize", "Optimize", "Good for sparsely keyframed animations. Might leave some frames if all frames are keyed.")
    ],
    default={"Location", "Rotation", "Scale", "Optimize"},
    options={"ENUM_FLAG"},
)
