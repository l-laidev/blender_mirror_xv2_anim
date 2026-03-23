import bpy

class MirrorAnim(bpy.types.Operator):
    """Mirror the selected animation."""
    bl_idname = "object.move_x"
    bl_label = "Mirror the selected animation."
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
        
        seen = set()
        # swap L/R bones' animation
        for bone_name in filter(lambda x: x.split('_')[1] in ['L', 'R'], bone2keyframes):
            if bone_name in seen:
                continue
            
            bone_name_parts = bone_name.split('_')
            assert bone_name_parts[1] in ['L', 'R'], f'Found invalid bone during L/R swapping: {bone_name}'
            
            bone_name_parts[1] = 'L' if bone_name_parts[1] == 'R' else 'R'
            other_pair_name = '_'.join(bone_name_parts)
            
            seen |= {bone_name, other_pair_name}
            bone1, bone2 = armature.pose.bones[bone_name], armature.pose.bones[other_pair_name]
            
            combined_keyframes = set(list(bone2keyframes.get(bone_name, [])) + list(bone2keyframes.get(other_pair_name, [])))
            
            bone1_kf2locrot = {}
            for kf in bone2keyframes.get(bone_name, []):
                context.scene.frame_set(kf)
                assert bone1.rotation_mode == "QUATERNION", f"XV2 rotations must be in Quaternion. Got: {bone1.rotation_mode}"
                
                bone1_kf2locrot[kf] = (bone1.location.copy(), bone1.rotation_quaternion.copy())
                bone1.keyframe_delete(data_path="location", frame=kf)
                bone1.keyframe_delete(data_path="rotation_quaternion", frame=kf)
                bone1.keyframe_delete(data_path="rotation_euler", frame=kf)
            
            bone2_kf2locrot = {}
            for kf in bone2keyframes.get(other_pair_name, []):
                context.scene.frame_set(kf)
                assert bone2.rotation_mode == "QUATERNION", f"XV2 rotations must be in Quaternion. Got: {bone2.rotation_mode}"
                
                bone2_kf2locrot[kf] = (bone2.location.copy(), bone2.rotation_quaternion.copy())
                bone2.keyframe_delete(data_path="location", frame=kf)
                bone2.keyframe_delete(data_path="rotation_quaternion", frame=kf)
                bone2.keyframe_delete(data_path="rotation_euler", frame=kf)
            
            for kf in bone1_kf2locrot:
                context.scene.frame_set(kf)
                
                loc, rot = bone1_kf2locrot[kf]
                for pos in 'xyz':
                    exec(f"bone2.location.{pos} = loc.{pos}")
                
                for compo in 'wxyz':
                    exec(f"bone2.rotation_quaternion.{compo} = rot.{compo}")
                
                bone2.keyframe_insert(data_path="location", frame=kf)
                bone2.keyframe_insert(data_path="rotation_quaternion", frame=kf)
                bone2.keyframe_insert(data_path="rotation_euler", frame=kf)
            
            for kf in bone2_kf2locrot:
                context.scene.frame_set(kf)
                
                loc, rot = bone2_kf2locrot[kf]
                for pos in 'xyz':
                    exec(f"bone1.location.{pos} = loc.{pos}")
                
                for compo in 'wxyz':
                    exec(f"bone1.rotation_quaternion.{compo} = rot.{compo}")
                
                bone1.keyframe_insert(data_path="location", frame=kf)
                bone1.keyframe_insert(data_path="rotation_quaternion", frame=kf)
                bone1.keyframe_insert(data_path="rotation_euler", frame=kf)
            
        
        # invert location and rotation
        for bone_name in bone2keyframes:
            bone = armature.pose.bones[bone_name]
            
            for kf in bone2keyframes[bone_name]:
                context.scene.frame_set(kf)
                
                # 0 doesn't need to be changed
                if all([val == 0 for val in [
                    bone.rotation_quaternion.x,
                    bone.rotation_quaternion.y,
                    bone.rotation_quaternion.z,
                    bone.location.x,
                ]]):
                    continue
                
                assert bone.rotation_mode == "QUATERNION", f"XV2 rotations must be in Quaternion. Got: {bone.rotation_mode}"
                
                bone.location.x *= -1.0
                bone.rotation_quaternion.y *= -1.0
                bone.rotation_quaternion.z *= -1.0
                
                bone.keyframe_insert(data_path="location", frame=kf)
                bone.keyframe_insert(data_path="rotation_quaternion", frame=kf)
                bone.keyframe_insert(data_path="rotation_euler", frame=kf)
        
        
        context.scene.frame_set(old_frame)
        bpy.ops.object.mode_set(mode=old_mode)
        return {"FINISHED"}
