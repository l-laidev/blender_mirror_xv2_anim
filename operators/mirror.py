import bpy

class MirrorAnim(bpy.types.Operator):
    """Mirror the selected animation."""
    bl_idname = "object.move_x"
    bl_label = "Mirror the selected animation."
    bl_options = {"REGISTER", "UNDO"}
    
    def execute(self, context):
        scene = context.scene
        armature = context.object
        if armature is None or armature.type != "ARMATURE":
            self.report({"ERROR"}, "Please select a valid armature.")
            return {"FINISHED"}
        
        return {"FINISHED"}
