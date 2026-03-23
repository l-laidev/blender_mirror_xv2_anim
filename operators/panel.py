import bpy
from .mirror import MirrorAnim


class AddonPanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_xv2_mirror_anim"
    bl_label = "Mirror XV2 Animation"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Mirror XV2"
    
    def draw(self, context):
        self.layout.operator(MirrorAnim.bl_idname)
        
        self.layout.prop(context.scene.xv2_mirror_addon_props, "mirroring_options")
        self.layout.prop(context.scene.xv2_mirror_addon_props, "mirroring_mode")
        self.layout.prop(context.scene.xv2_mirror_addon_props, "optimize_frame_selection")
