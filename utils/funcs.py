class Utilities:
    mirror_options = {}
    mirror_mode = {}
    
    @staticmethod
    def invert_frame(bone):
        if all([val == 0 for val in [
            bone.rotation_quaternion.x,
            bone.rotation_quaternion.y,
            bone.rotation_quaternion.z,
            bone.location.x,
        ]]):
            return
        
        if "Location" in Utilities.mirror_options:
            match Utilities.mirror_mode:
                case "XV2":        
                    bone.location.x *= -1.0
                case "SZ":
                    bone.location.z *= -1.0
        
        if "Rotation" in Utilities.mirror_options:
            assert bone.rotation_mode == "QUATERNION", f"XV2 rotations must be in Quaternion. Got: {bone.rotation_mode}"
            bone.rotation_quaternion.y *= -1.0
            
            match Utilities.mirror_mode:
                case "XV2":
                    bone.rotation_quaternion.z *= -1.0
                case "SZ":
                    bone.rotation_quaternion.x *= -1.0

    @staticmethod
    def copy_to_other(other, loc, rot, scale):
        for pos in 'xyz':
            if "Location" in Utilities.mirror_options:
                exec(f"other.location.{pos} = loc.{pos}")
            if "Scale" in Utilities.mirror_options:
                exec(f"other.scale.{pos} = scale.{pos}")
        
        if "Rotation" in Utilities.mirror_options:
            for compo in 'wxyz':
                exec(f"other.rotation_quaternion.{compo} = rot.{compo}")

    @staticmethod
    def delete_frame(bone, frame):
        if "Location" in Utilities.mirror_options:
            bone.keyframe_delete(data_path="location", frame=frame)
        if "Scale" in Utilities.mirror_options:
            bone.keyframe_delete(data_path="scale", frame=frame)
        if "Rotation" in Utilities.mirror_options:
            bone.keyframe_delete(data_path="rotation_quaternion", frame=frame)
            bone.keyframe_delete(data_path="rotation_euler", frame=frame)

    @staticmethod
    def insert_frame(bone, frame):
        if "Location" in Utilities.mirror_options:
            bone.keyframe_insert(data_path="location", frame=frame)
        if "Scale" in Utilities.mirror_options:
            bone.keyframe_insert(data_path="scale", frame=frame)
        if "Rotation" in Utilities.mirror_options:
            bone.keyframe_insert(data_path="rotation_quaternion", frame=frame)
            bone.keyframe_insert(data_path="rotation_euler", frame=frame)
