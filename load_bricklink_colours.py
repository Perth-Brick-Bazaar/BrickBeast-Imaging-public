import json

class LegoColorNode:
    def __init__(self, colourID, colourName, hex_code, rgb, hsv, type_):
        self.colourID = colourID
        self.colourName = colourName
        self.hex_code = hex_code
        self.rgb = rgb
        self.hsv_anchor = hsv  # Use these as initial anchors
        self.type = type_
        self.samples = []

    def __repr__(self):
        return f"{self.colourName} (ID: {self.colourID})"

# Load JSON
with open('bricklink_colours.json', 'r') as f:
    palette = json.load(f)

# Initialize color nodes
color_nodes = []
for color_data in palette.values():
    node = LegoColorNode(
        colourID=color_data['colourID'],
        colourName=color_data['colourName'],
        hex_code=color_data['hex'],
        rgb=color_data['rgb'],
        hsv=color_data['hsv'],
        type_=color_data['type']
    )
    color_nodes.append(node)

# Example: Print the first few nodes
for node in color_nodes[:5]:
    print(node)