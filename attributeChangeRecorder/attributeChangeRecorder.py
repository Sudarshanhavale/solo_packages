"""
Coded by Sudarshan Havale at 28-05-2018

Attribute Change Recorder:
    -Help Recording attribute actions to apply on multiple selections of same types.

Uses:
    -Record: To start recording actions.
    -Stop: To stop recording.
    -Rewind: Wipe out the earlier recorded actions.
    -Apply: Assign recorded actions on selections.

Limitations:
    -Supports set attribute command only.
    -Doesnt work on shader attributes.

To Do:
    -Expansion for other commands actions and include shaders as well.
"""

# Python Imports
import os
import re

# Maya Imports
import maya.cmds as cmds
import maya.mel as mel

# Global variable to store command log
FILE_NAME = os.path.join(cmds.internalVar(userAppDir=True), "commandLog.txt")


def main_ui():
    """Main UI Function
    :return:
    """
    win_name = 'Attribute Change Recorder'

    if cmds.window(win_name, exists=True):
        cmds.deleteUI(win_name, window=True)

    win = cmds.window(win_name, mxb=False)

    cmds.rowLayout(numberOfColumns=4)
    cmds.button(label='Record', command="pm.scriptEditorInfo(hfn= 'commandLog.txt', wh=1)", width=60)
    cmds.button(label='Stop', command="pm.scriptEditorInfo(hfn= 'commandLog.txt', wh=0)", width=60)
    cmds.button(label='Rewind', command="rewind()", width=60)
    cmds.button(label='Play', command="apply_changes()", width=60)

    cmds.showWindow(win)


def rewind():
    """Wipe out the previous records.
    :return: Success message.
    """
    with open(FILE_NAME, "w"):
        return "Rewind Records successful...!"


def apply_changes():
    """Apply recorded changes to the attributes
    of valid selections.

    :return: None
    """
    log_commands = get_log()

    for log_command in log_commands:

        # Unpack recorded commands from log
        process, node_name, attribute_name, value = unpack_command(log_command)
        node_type = cmds.nodeType(node_name)

        # Get valid target nodes from current selection to update recorded attributes.
        target_nodes = get_target_nodes(node_type)
        for target_node in target_nodes:
            mel_command = process + " \"" + target_node + "." \
                          + attribute_name + "\" " + value

            # Execute commands on target nodes.
            mel.eval(mel_command)


def get_target_nodes(node_type=None):
    """Get valid target nodes from the selections.

    :param node_type:
    :return:
    """
    target_nodes = list()
    sel_nodes = cmds.ls(sl=True)

    if node_type == "transform":
        # For the transform node types,
        # current selection might be a valid target node.
        target_nodes = sel_nodes
    else:
        # Look for valid target node of each selection.
        for each_node in sel_nodes:
            get_match = find_node_match(each_node, node_type)

            if get_match:
                target_nodes.append(get_match)
            else:
                # Raise warning for non matching types.
                cmds.warning("Unable to apply change on '{}', "
                             "No matching '{}' found in connections"
                             .format(each_node, node_type))
    return target_nodes


def find_node_match(sel_node=None, node_type=None):
    """Find matching node type from given selection.

    :param sel_node: selected node name.
    :param node_type: node type extracted from logs.
    :return: matching node/shape name else None
    """
    shape_name = cmds.listRelatives(sel_node, shapes=True)[0]
    current_node_type = cmds.nodeType(shape_name)

    if current_node_type == node_type:
        return shape_name
    else:
        # Look for the match type in connections.
        other_conns = cmds.listConnections(shape_name, type=node_type)
        if other_conns:
            return other_conns[0]
        else:
            # If doesnt match then return none type.
            return None


def unpack_command(log_command=None):
    """Unpack given log command for further process.

    :param log_command: string output of get_log() function.
    :return: process, node_name, attribute_name, value
    """
    split_command = re.split(' *" *', log_command)

    process = split_command[0]
    node_name, attribute_name = split_command[1].split(".")
    value = split_command[-1]

    return process, node_name, attribute_name, value


def get_log():
    """Get the filtered setAttr commands from the logs.

    :return: List of all setAttr commands.
    """
    with open(FILE_NAME, "r") as f:
        attr_log = [line for line in f.read().splitlines()
                    if line.startswith("setAttr") and not "|" in line]
    return attr_log


def run():
    """Executor function

    :return: None
    """
    main_ui()


run()
