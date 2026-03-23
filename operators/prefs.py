import bpy


class AddonProps(bpy.types.PropertyGroup):
    mirroring_options: bpy.props.EnumProperty(
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
    
    mirroring_mode: bpy.props.EnumProperty(
        name="Preset",
        description="Mirroring mode",
        items=[
            ("XV2", "XV2", "XV2"),
            ("SZ", "SZ", "SparkingZERO"),
        ],
        default="XV2",
    )

    optimize_frame_selection: bpy.props.BoolProperty(
        name="Optimize",
        description="Good for sparsely keyframed animations. Might leave some frames if all frames are keyed.",
        default=True,
    )
