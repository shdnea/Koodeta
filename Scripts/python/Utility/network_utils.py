"""
        @file           network_utils.py

        @author         Syahdan Micoy Nazera
        
        @since          2025-15-01
        @lastupdate     2025-22-01
        
        @brief          Houdini Network Context Utilities
        @dependencies   Python 3.10, hou
        @version        1.0.0
        @todos          Update module to class
                        Add more method
"""

import hou

def create_sticky_box():
    # Get the selected nodes
    selected_nodes = hou.selectedNodes()

    if not selected_nodes:
        hou.ui.displayMessage("No nodes selected.")
    else:
        # Get the parent network (assumes all selected nodes share the same parent)
        parent = selected_nodes[0].parent()

        # Create a network box
        netbox = parent.createNetworkBox()

        # Add nodes to the network box
        for node in selected_nodes:
            netbox.addNode(node)

        # Resize the box to fit contents
        netbox.fitAroundContents()

        # Create a sticky note
        sticky = parent.createStickyNote()
        sticky.setText("Quick Notes:")
        sticky.setColor(hou.Color((1.0, 1.0, 0.6)))  # Light yellow

        # Set the position to inside the network box
        # Use the top-left corner + some padding
        box_pos = netbox.position()
        sticky.setPosition(box_pos + hou.Vector2((2.5, 2.5)))  # Adjust as needed

        # Add the sticky note to the network box
        netbox.addStickyNote(sticky)
