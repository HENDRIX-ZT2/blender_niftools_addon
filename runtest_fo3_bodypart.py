"""Automated body part tests for the blender nif scripts."""

# ***** BEGIN LICENSE BLOCK *****
# 
# BSD License
# 
# Copyright (c) 2005-2009, NIF File Format Library and Tools
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. The name of the NIF File Format Library and Tools project may not be
#    used to endorse or promote products derived from this software
#    without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
# NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
# THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# ***** END LICENSE BLOCK *****

from itertools import izip

from nif_test import TestSuite
from PyFFI.Formats.NIF import NifFormat
import Blender
import bpy

class BodyPartTestSuite(TestSuite):
    def run(self):
        # create a mesh
        self.logger.info("creating mesh")
        mesh_data = Blender.Mesh.Primitives.Monkey()
        mesh_numverts = len(mesh_data.verts)
        mesh_obj = self.scene.objects.new(mesh_data, "Monkey")
        # create an armature
        self.logger.info("creating armature")
        arm_data = Blender.Armature.Armature("Scene Root")
        arm_data.drawAxes = True
        arm_data.envelopes = False
        arm_data.vertexGroups = True
        arm_data.drawType = Blender.Armature.STICK
        arm_obj = self.scene.objects.new(arm_data, "Scene Root")
        arm_data.makeEditable()
        bone = Blender.Armature.Editbone()
        arm_data.bones["Bone"] = bone
        arm_data.update()
        # skin the mesh
        self.logger.info("attaching mesh to armature")
        mesh_data.addVertGroup("Bone")
        mesh_data.assignVertsToGroup("Bone", list(range(mesh_numverts)), 1,
                                     Blender.Mesh.AssignModes.REPLACE)
        arm_obj.makeParentDeform([mesh_obj])
        # set body part
        self.logger.info("creating body part vertex group")
        mesh_data.addVertGroup("BP_HEAD")
        mesh_data.assignVertsToGroup("BP_HEAD", list(range(mesh_numverts)), 1,
                                     Blender.Mesh.AssignModes.REPLACE)
        # export
        nif_export = self.test(
            filename = 'test/nif/fo3/_bodypart1.nif',
            config = dict(
                EXPORT_VERSION = 'Fallout 3', EXPORT_SMOOTHOBJECTSEAMS = True,
                EXPORT_FLATTENSKIN = True),
            selection = ['Scene Root'])
        # check body part
        self.logger.info("checking for body parts")
        skininst = nif_export.root_blocks[0].find(
            block_type = NifFormat.BSDismemberSkinInstance)
        if not skininst:
            raise ValueError("no body parts found")
        self.logger.info("checking number of body parts")
        if skininst.numPartitions != 1:
            raise ValueError("bad number of skin partitions")
        self.logger.info("checking body part indices")
        if skininst.partitions[0].bodyPart != NifFormat.BSDismemberBodyPartType.BP_HEAD:
            raise ValueError("bad body part type in skin partition")

suite = BodyPartTestSuite("bodypart")
suite.run()

