#!/usr/bin/python
import random
import bpy
from bpy.types import Operator  
from bpy.props import FloatVectorProperty, FloatProperty, IntProperty, StringProperty  

bl_info = {
    "name": "UE4NeuronMapper",
    "category": "Object",
}



class UE4NeuronMapper(bpy.types.Operator):
    """UE4 Perception Neuron Rig Mapper"""
    bl_idname = "object.ue4neuronmapper"
    bl_label = "UE4 Neuron Mapper"
    bl_options = {'REGISTER', 'UNDO'}

    target_rig = StringProperty(  
        name="Target Rig",  
        default="HeroTPP",  
        description="target_rig"  
        )

    source_rig = StringProperty(  
        name="Source Rig",  
        default="",  
        description="source_rig"  
        )

    def invoke(self, context, event):
        if bpy.context.scene.objects.active is None:
            print("No armature selected")
            return {'CANCELLED'}
        else:
            self.source_rig = bpy.context.scene.objects.active.name
            wm = context.window_manager
            return wm.invoke_props_dialog(self)
            return {'FINISHED'}

    def execute(self, context):        
            # deselect all objects
            source_armature = bpy.data.objects[self.source_rig]
            source_armature.select = False
            target_armature = bpy.data.objects[self.target_rig]
            bpy.context.scene.objects.active = target_armature
            target_armature.select = True
            print("selected " + str(target_armature))

            bpy.ops.object.mode_set(mode='OBJECT')       
            bpy.ops.object.posemode_toggle()
            bpy.context.object.data.layers[0] = True       
            bpy.context.object.data.layers[2] = True
            bpy.ops.pose.select_all(action='SELECT')            
            bpy.ops.pose.constraints_clear()
            # hide all the control bones, just leave deform bones showing
            bpy.context.object.data.layers[2] = False

            # start mapping bones

            #bpy.context.space_data.context = 'BONE_CONSTRAINT'
            for bone in bpy.data.objects[self.target_rig].data.bones:
                print(bone)
                bone.select = False 

            # root -> hips (copy rotation, z-axis only)

            current_bone = target_armature.pose.bones.get("root")  
            new_constraint = current_bone.constraints.new('COPY_ROTATION')
            new_constraint.target = source_armature
            new_constraint.subtarget = 'Hips'
            new_constraint.use_x = False
            new_constraint.use_y = False         
            

            # pelvis -> hips
            current_bone = target_armature.pose.bones.get("pelvis")        
            new_constraint = current_bone.constraints.new('COPY_LOCATION')
            new_constraint.target = source_armature
            new_constraint.subtarget = 'Hips'
             
            # thigh_l -> damped track to LeftLeg
            current_bone = target_armature.pose.bones.get("thigh_l") 
            new_constraint = current_bone.constraints.new('DAMPED_TRACK')
            new_constraint.target = source_armature
            new_constraint.subtarget = 'LeftLeg'

            # calf_l -> damped track to LeftFoot
            current_bone = target_armature.pose.bones.get("calf_l") 
            new_constraint = current_bone.constraints.new('DAMPED_TRACK')
            new_constraint.target = source_armature
            new_constraint.subtarget = 'LeftFoot'

            # thigh_r -> damped track to RightLeg
            current_bone = target_armature.pose.bones.get("thigh_r") 
            new_constraint = current_bone.constraints.new('DAMPED_TRACK')
            new_constraint.target = source_armature
            new_constraint.subtarget = 'RightLeg'

            # calf_r -> damped track to LeftFoot
            current_bone = target_armature.pose.bones.get("calf_r") 
            new_constraint = current_bone.constraints.new('DAMPED_TRACK')
            new_constraint.target = source_armature
            new_constraint.subtarget = 'RightFoot'


            # spine_01 -> damped track to Spine2
            current_bone = target_armature.pose.bones.get("spine_01") 
            new_constraint = current_bone.constraints.new('DAMPED_TRACK')
            new_constraint.target = source_armature
            new_constraint.subtarget = 'Spine2'

            # spine_02 -> damped track to Spine3
            current_bone = target_armature.pose.bones.get("spine_02") 
            new_constraint = current_bone.constraints.new('DAMPED_TRACK')
            new_constraint.target = source_armature
            new_constraint.subtarget = 'Spine3'

            # spine_03 -> damped track to Neck
            current_bone = target_armature.pose.bones.get("spine_03") 
            new_constraint = current_bone.constraints.new('DAMPED_TRACK')
            new_constraint.target = source_armature
            new_constraint.subtarget = 'Neck'

            # neck_01 -> damped track to head
            current_bone = target_armature.pose.bones.get("neck_01") 
            new_constraint = current_bone.constraints.new('DAMPED_TRACK')
            new_constraint.target = source_armature
            new_constraint.subtarget = 'Head'

            # head -> damped track to head
            current_bone = target_armature.pose.bones.get("head") 
            new_constraint = current_bone.constraints.new('DAMPED_TRACK')
            new_constraint.target = source_armature
            new_constraint.subtarget = 'Head'
            new_constraint.head_tail = 1.0

            # clavicle_l -> damped track to LeftArm
            current_bone = target_armature.pose.bones.get("clavicle_l") 
            new_constraint = current_bone.constraints.new('DAMPED_TRACK')
            new_constraint.target = source_armature
            new_constraint.subtarget = 'LeftArm'

            # clavicle_r -> damped track to RightArm
            current_bone = target_armature.pose.bones.get("clavicle_r") 
            new_constraint = current_bone.constraints.new('DAMPED_TRACK')
            new_constraint.target = source_armature
            new_constraint.subtarget = 'RightArm'

            # upperarm_l -> damped track to LeftArm
            current_bone = target_armature.pose.bones.get("upperarm_l") 
            new_constraint = current_bone.constraints.new('DAMPED_TRACK')
            new_constraint.target = source_armature
            new_constraint.subtarget = 'LeftForeArm'

            # upperarm_r -> damped track to RightArm
            current_bone = target_armature.pose.bones.get("upperarm_r") 
            new_constraint = current_bone.constraints.new('DAMPED_TRACK')
            new_constraint.target = source_armature
            new_constraint.subtarget = 'RightForeArm'

            # lowerarm_l -> damped track to LeftHand
            current_bone = target_armature.pose.bones.get("lowerarm_l") 
            new_constraint = current_bone.constraints.new('DAMPED_TRACK')
            new_constraint.target = source_armature
            new_constraint.subtarget = 'LeftHand'

            # lowerarm_r -> damped track to RightHand
            current_bone = target_armature.pose.bones.get("lowerarm_r") 
            new_constraint = current_bone.constraints.new('DAMPED_TRACK')
            new_constraint.target = source_armature
            new_constraint.subtarget = 'RightHand'

            # hand_l -> copy transforms LeftHand, in local space
            current_bone = target_armature.pose.bones.get("hand_l") 
            new_constraint = current_bone.constraints.new('COPY_TRANSFORMS')
            new_constraint.target = source_armature
            new_constraint.subtarget = 'LeftHand'
            new_constraint.target_space = 'POSE'
            new_constraint.owner_space = 'POSE'

            # hand_r -> copy transforms RightHand, in local space
            current_bone = target_armature.pose.bones.get("hand_r") 
            new_constraint = current_bone.constraints.new('COPY_TRANSFORMS')
            new_constraint.target = source_armature
            new_constraint.subtarget = 'RightHand'
            new_constraint.target_space = 'POSE'
            new_constraint.owner_space = 'POSE'

            # here we have a generic dictionary mapping, the 'fingermap' name should have "_l" or "_r" suffix when addressing the target bone
            # the source mapping will need to have "LeftHand" or "RightHand" prefix

            fingermap = {}
            fingermap['thumb_01'] = 'Thumb1'
            fingermap['thumb_02'] = 'Thumb2'
            fingermap['thumb_03'] = 'Thumb3'
            fingermap['index_01'] = 'Index1'
            fingermap['index_02'] = 'Index2'
            fingermap['index_03'] = 'Index3'
            fingermap['middle_01'] = 'Middle1'
            fingermap['middle_02'] = 'Middle2'
            fingermap['middle_03'] = 'Middle3'
            fingermap['ring_01'] = 'Ring1'
            fingermap['ring_02'] = 'Ring2'
            fingermap['ring_03'] = 'Ring3'
            fingermap['pinky_01'] = 'Pinky1'
            fingermap['pinky_02'] = 'Pinky2'
            fingermap['pinky_03'] = 'Pinky3'

            for finger in fingermap:
                target_finger = finger + "_l"
                source_finger = "LeftHand" + fingermap[finger]
                current_bone = target_armature.pose.bones.get(target_finger) 
                new_constraint = current_bone.constraints.new('COPY_TRANSFORMS')
                new_constraint.target = source_armature
                new_constraint.subtarget = source_finger
                #new_constraint.head_tail = 1.0
                new_constraint.target_space = 'LOCAL'
                new_constraint.owner_space = 'LOCAL'

            for finger in fingermap:
                target_finger = finger + "_r"
                source_finger = "RightHand" + fingermap[finger]
                current_bone = target_armature.pose.bones.get(target_finger) 
                new_constraint = current_bone.constraints.new('COPY_TRANSFORMS')
                new_constraint.target = source_armature
                new_constraint.subtarget = source_finger
                #new_constraint.head_tail = 1.0
                new_constraint.target_space = 'LOCAL'
                new_constraint.owner_space = 'LOCAL'


            

            return {'FINISHED'} 

def register():
    print("+++ UE4NeuronMapperRegister()")
    bpy.utils.register_class(UE4NeuronMapper)
def unregister():
    print("+++ UE4NeuronMapperUnregister()")
    bpy.utils.unregister_class(UE4NeuronMapper)

if __name__ == "__main__":
    register()
