# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name": "Xv2 Mirror Anim",
    "author": "hai",
    "description": "Add-on to mirror XV2 animations",
    "blender": (2, 80, 0),
    "version": (1, 1, 2),
    "location": """3D View > Sidebar > Mirror XV2""",
    "warning": "",
    "category": "Animation",
}


import bpy
from .operators import MirrorAnim, AddonPanel, settings


def menu_func(self, context):
    self.layout.operator(MirrorAnim.bl_idname)

def register():
    bpy.utils.register_class(MirrorAnim)
    bpy.utils.register_class(AddonPanel)
    bpy.types.Scene.xv2_mirror_addon_props = settings

def unregister():
    bpy.utils.unregister_class(MirrorAnim)
    bpy.utils.unregister_class(AddonPanel)
    del bpy.types.Scene.xv2_mirror_addon_props


if __name__ == "__main__":
    register()
