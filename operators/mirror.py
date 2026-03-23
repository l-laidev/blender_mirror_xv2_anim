import bpy
from ..utils import Utilities

class MirrorAnim(bpy.types.Operator):
    """Mirror the selected XV2 animation"""
    bl_idname = "animation.mirror_xv2"
    bl_label = "Mirror XV2 Animation"
    bl_options = {"REGISTER", "UNDO"}
    
    def execute(self, context):
        armature = context.object
        if armature is None or armature.type != "ARMATURE":
            self.report({"ERROR"}, "Please select the armature.")
            return {"FINISHED"}
        
        if armature.animation_data is None or armature.animation_data.action is None:
            self.report({"ERROR"}, "Please select an animation.")
            return {"FINISHED"}
        
        Utilities.mirror_options = context.scene.xv2_mirror_addon_props
        old_mode = bpy.context.object.mode
        old_frame = context.scene.frame_current
        bpy.ops.object.mode_set(mode="POSE")
        
        action = armature.animation_data.action
        fcurves = None
        if hasattr(action, "slots"):
            slot = action.slots[0]
            fcurves = action.layers[0].strips[0].channelbag(slot).fcurves
        else:
            fcurves = action.fcurves
        
        bone_path_prefix = """pose.bones[\""""
        bone2keyframes = {}
        # track only those frames which are keyed
        for fc in fcurves:
            bone_name = fc.data_path.replace(bone_path_prefix, "").split("\"]")[0]
            if bone_name not in armature.pose.bones:
                continue
            
            bone2keyframes[bone_name] = list(map(lambda x: int(x.co[0]), fc.keyframe_points))
        
        all_frames = set()
        for frames in bone2keyframes.values():
            all_frames |= set(frames)
        
        if "Optimize" not in Utilities.mirror_options:
            # do not leave out any frames
            all_frames = set(range(min(all_frames), max(all_frames)+1))
            for bone_name in bone2keyframes:
                bone2keyframes[bone_name] = list(all_frames)
        
        LR_pairs = {}
        other_bones = set()
        for bone in armature.pose.bones:
            bone_name_parts = bone.name.split('_')
            
            if len(bone_name_parts) < 2 or bone_name_parts[1] not in ['L', 'R']:
                other_bones.add(bone)
                continue
            
            name_without_LR = '_'.join(bone_name_parts[:1] + bone_name_parts[2:])
            LR_pairs[name_without_LR] = LR_pairs.get(name_without_LR, []) + [bone]
        
        for frame in all_frames:
            context.scene.frame_set(frame)
            
            for bone in other_bones:
                if frame in bone2keyframes.get(bone.name, []):
                    Utilities.invert_frame(bone)
                    Utilities.insert_frame(bone, frame)
            
            for pair in LR_pairs:
                boneA, boneB = LR_pairs[pair]
                
                boneA_loc, boneA_rot, boneA_scale = boneA.location.copy(), boneA.rotation_quaternion.copy(), boneA.scale.copy()
                boneB_loc, boneB_rot, boneB_scale = boneB.location.copy(), boneB.rotation_quaternion.copy(), boneB.scale.copy()
                
                Utilities.delete_frame(boneA, frame)
                Utilities.delete_frame(boneB, frame)
                
                if frame in bone2keyframes.get(boneA.name, []):
                    Utilities.copy_to_other(boneB, boneA_loc, boneA_rot, boneA_scale)
                    Utilities.invert_frame(boneB)
                    Utilities.insert_frame(boneB, frame)
                
                if frame in bone2keyframes.get(boneB.name, []):
                    Utilities.copy_to_other(boneA, boneB_loc, boneB_rot, boneB_scale)
                    Utilities.invert_frame(boneA)
                    Utilities.insert_frame(boneA, frame)
            
        
        context.scene.frame_set(old_frame)
        bpy.ops.object.mode_set(mode=old_mode)
        return {"FINISHED"}
