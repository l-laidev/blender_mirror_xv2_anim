def invert_frame(bone, kf):
    if all([val == 0 for val in [
        bone.rotation_quaternion.x,
        bone.rotation_quaternion.y,
        bone.rotation_quaternion.z,
        bone.location.x,
    ]]):
        return
    
    assert bone.rotation_mode == "QUATERNION", f"XV2 rotations must be in Quaternion. Got: {bone.rotation_mode}"
    
    bone.location.x *= -1.0
    bone.rotation_quaternion.y *= -1.0
    bone.rotation_quaternion.z *= -1.0

def copy_to_other(other, loc, rot, scale):
    for pos in 'xyz':
        exec(f"other.location.{pos} = loc.{pos}")
        exec(f"other.scale.{pos} = scale.{pos}")
    
    for compo in 'wxyz':
        exec(f"other.rotation_quaternion.{compo} = rot.{compo}")

def delete_frame(bone, frame):
    bone.keyframe_delete(data_path="location", frame=frame)
    bone.keyframe_delete(data_path="scale", frame=frame)
    bone.keyframe_delete(data_path="rotation_quaternion", frame=frame)
    bone.keyframe_delete(data_path="rotation_euler", frame=frame)

def insert_frame(bone, frame):
    bone.keyframe_insert(data_path="location", frame=frame)
    bone.keyframe_insert(data_path="scale", frame=frame)
    bone.keyframe_insert(data_path="rotation_quaternion", frame=frame)
    bone.keyframe_insert(data_path="rotation_euler", frame=frame)
