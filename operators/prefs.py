from bpy.props import EnumProperty


settings = EnumProperty(
    name="Mirror Options",
    description="Enable/Disable what to mirror",
    items=[
        ("Location", "Location", "Mirror X Location"),
        ("Rotation", "Rotation", "Mirror Bone Rotations"),
        ("Scale", "Scale", "Mirror Bone Scaling"),
    ],
    default={"Location", "Rotation", "Scale"},
    options={"ENUM_FLAG"},
)
