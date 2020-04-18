import pymel.core as pm
import maya.cmds as cmds
import maya.mel as mel
import os
import re

# Global variable to store command log
FILE_NAME = os.path.join(pm.internalVar(userAppDir=True), "commandLog.txt")


def main_ui():
    """Main UI Function
    :return:
    """
    win_name = 'Attribute Change Recorder'

    if pm.window(win_name, exists=True):
        pm.deleteUI(win_name, window=True)

    win = pm.window(win_name, mxb=False)

    pm.rowLayout(numberOfColumns=4)
    pm.button(label='Record', command="pm.scriptEditorInfo(hfn= 'commandLog.txt', wh=1)", width=60)
    pm.button(label='Stop', command="pm.scriptEditorInfo(hfn= 'commandLog.txt', wh=0)", width=60)
    pm.button(label='Rewind', command="rewind()", width=60)
    pm.button(label='Play', command="apply_changes()", width=60)

    win.show()


def rewind():
    """Wipe out the previous records.
    :return: Success message.
    """
    with open(FILE_NAME, "w"):
        return "Rewind Records successful...!"


def apply_changes():
    """Apply recorded changes to
    valid attributes from selection.
    :return:
    """
    log_commands = get_log()

    for log_command in log_commands:
        final_command = get_node(log_command)
        target_type = cmds.nodeType(final_command[0])
        target_nodes = get_target_nodes(target_type)
        for each_node in target_nodes:
            mel_command = "setAttr \"" + each_node + "." \
                          + final_command[1] + "\" " + final_command[2]
            mel.eval(mel_command)


def get_target_nodes(target_type=None):
    """Get valid target nodes from selections.
    :param target_type:
    :return:
    """
    target_nodes = list()
    sel_nodes = cmds.ls(sl=True)

    if target_type == "transform":
        target_nodes = sel_nodes
    else:
        for each_node in sel_nodes:
            is_match = valid_node_type(each_node, target_type)
            if is_match != "Invalid":
                target_nodes.append(is_match)
    return target_nodes


def valid_node_type(sel_node=None, target_type=None):
    node_shape = cmds.listRelatives(sel_node, shapes=True)[0]
    node_type = cmds.nodeType(node_shape)

    if node_type == target_type:
        return node_shape
    else:
        other_conns = cmds.listConnections(node_shape, type=target_type)
        if other_conns:
            return other_conns[0]
        else:
            return "Invalid"


def get_node(whole_command=None):
    """
    We can return a dictionary output here. and name is also confusing.
    :param whole_command:
    :return:
    """
    split_command = re.split(' *" *', whole_command)[1:]
    split_attribute = split_command[0].split(".")
    return [split_attribute[0], split_attribute[1], split_command[-1]]


def get_log():
    """Get the recorded setAttr commands from logs.
    :return: List of all setAttr commands.
    """
    with open(FILE_NAME, "r") as f:
        attr_log = [line for line in f.read().splitlines()
                    if line.startswith("setAttr") and not "|" in line]
    return attr_log


main_ui()
