"""
Coded by Sudarshan Havale at 11-03-2019

Snow Builder Operation Menu Functions:
    -Required actions to operate snow builder tool.
    
ToDo: Validations before maya file save.
"""

import maya.cmds as cmds


def get_connections():
    """Get all connection input names in the form of dictionary.
    :return: dictionary of input connections.
    """
    snow_builder_node = cmds.ls(sl=True, type="container")[0]

    if snow_builder_node and cmds.getAttr(
            snow_builder_node + ".containerCategory", asString=True) == "SNOW_BUILDER":

        rename_members(snow_builder_node)

        particle_node = cmds.listConnections(snow_builder_node + ".particleNode",
                                             shapes=True)[0]
        growth_mesh = cmds.listConnections(snow_builder_node + ".growthMesh",
                                           shapes=True)[0]
        snow_mesh = cmds.listConnections(snow_builder_node + ".snowMesh",
                                         shapes=True)[0]
        geo_connector = cmds.listConnections(snow_builder_node + ".geoConnector",
                                             shapes=True)[0]

        return dict(asset_node=snow_builder_node,
                    particle_node=particle_node,
                    growth_mesh=growth_mesh,
                    snow_mesh=snow_mesh,
                    geo_connector=geo_connector)

    else:
        cmds.error("Current selection doesn't have 'Snow Builder' node, "
                   "Please select 'Snow Builder' asset node to proceed")


def rename_members(asset_node=str()):
    """Add container name as prefix to all its members.
    :param asset_node: Container node name
    :return:
    """
    all_members = cmds.container(asset_node, q=True, nodeList=True)

    return [cmds.rename(member, (asset_node + "_" + member))
            for member in all_members if cmds.objExists(member)
            and not member.startswith(asset_node)]


def assign_emitter():
    """Assign selected mesh as an emitter
    :return: Success/Failure message
    """

    current_connections = get_connections()
    new_growth_mesh = cmds.listRelatives(fullPath=True, shapes=True, type="mesh")[0]

    try:
        cmds.connectAttr(new_growth_mesh + ".message",
                         current_connections['asset_node'] + ".growthMesh", force=True)
        cmds.connectAttr(new_growth_mesh + ".message",
                         current_connections['geo_connector'] + ".owner", force=True)
        cmds.connectAttr(new_growth_mesh + ".outMesh",
                         current_connections['geo_connector'] + ".localGeometry",
                         force=True)
        cmds.connectAttr(new_growth_mesh + ".worldMatrix[0]",
                         current_connections['geo_connector'] + ".worldMatrix",
                         force=True)

        # Particles need to be regenerated for new emitter so setting back snow builder to dynamic again.
        back_to_dynamic()

        return "{} has assigned to the new emitter {}".format(
            current_connections['asset_node'], new_growth_mesh)

    except Exception as E:
        return cmds.warning(
            "Error occurred during new emitter assignment...\n{}".format(E))


def bake_output():
    """Duplicates the current snow surface output
    and keep outside the container.

    :return: baked mesh name
    """
    current_connections = get_connections()
    baked_output = cmds.duplicate(
        current_connections["snow_mesh"], returnRootsOnly=True, name="SnowBakedOutput_01")

    return baked_output


def freeze_simulation():
    """Freeze simulation on given frame to stop dynamic behaviour.
    :return: Success message.
    """
    particle_node = get_connections()["particle_node"]
    cmds.select(particle_node, replace=True)
    cmds.setDynStartState()
    cmds.setAttr(particle_node + ".isDynamic", 0)
    message = ("Particle simulation has been frozen for the node {}".format(particle_node))
    return message


def back_to_dynamic():
    """Reset the tool back to dynamic.
    :return: Success message.
    """
    particle_node = get_connections()["particle_node"]
    cmds.select(particle_node, replace=True)
    cmds.clearDynStartState()
    cmds.setAttr(particle_node + ".isDynamic", 1)
    message = ("{} is set back to dynamic again".format(particle_node))
    return message
