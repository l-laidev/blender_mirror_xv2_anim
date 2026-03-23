import bpy
from ..utils import invert_frame, copy_to_other, insert_frame, delete_frame

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
        
        old_mode = bpy.context.object.mode
        old_frame = context.scene.frame_current
        bpy.ops.object.mode_set(mode="POSE")
        
        action = armature.animation_data.action
        slot = action.slots[0]
        fcurves = action.layers[0].strips[0].channelbag(slot).fcurves
        
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
        
        LR_pairs = {}
        other_bones = set()
        for bone in armature.pose.bones:
            bone_name_parts = bone.name.split('_')
            
            if bone_name_parts[1] not in ['L', 'R']:
                other_bones.add(bone)
                continue
            
            name_without_LR = '_'.join(bone_name_parts[:1] + bone_name_parts[2:])
            LR_pairs[name_without_LR] = LR_pairs.get(name_without_LR, []) + [bone]
        
        for frame in all_frames:
            context.scene.frame_set(frame)
            
            for bone in other_bones:
                if frame in bone2keyframes.get(bone.name, []):
                    invert_frame(bone, frame)
                    insert_frame(bone, frame)
            
            for pair in LR_pairs:
                boneA, boneB = LR_pairs[pair]
                
                boneA_loc, boneA_rot, boneA_scale = boneA.location.copy(), boneA.rotation_quaternion.copy(), boneA.scale.copy()
                boneB_loc, boneB_rot, boneB_scale = boneB.location.copy(), boneB.rotation_quaternion.copy(), boneB.scale.copy()
                
                delete_frame(boneA, frame)
                delete_frame(boneB, frame)
                
                if frame in bone2keyframes.get(boneA.name, []):
                    copy_to_other(boneB, boneA_loc, boneA_rot, boneA_scale)
                    invert_frame(boneB, frame)
                    insert_frame(boneB, frame)
                
                if frame in bone2keyframes.get(boneB.name, []):
                    copy_to_other(boneA, boneB_loc, boneB_rot, boneB_scale)
                    invert_frame(boneA, frame)
                    insert_frame(boneA, frame)
            
        
        context.scene.frame_set(old_frame)
        bpy.ops.object.mode_set(mode=old_mode)
        return {"FINISHED"}
