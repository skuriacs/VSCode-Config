#!/usr/bin/env python3
"""
Create visual diagrams to accompany the TileMap vs TileSet documentation.
"""

from reportlab.graphics.shapes import Drawing, Rect, String, Line, Circle
from reportlab.graphics import renderPDF
from reportlab.lib import colors
from reportlab.lib.units import inch

def create_tileset_editor_mockup():
    """Create a mockup of the TileSet editor interface"""
    d = Drawing(600, 400)
    
    # Main window
    d.add(Rect(10, 10, 580, 380, fillColor=colors.lightgrey, strokeColor=colors.black, strokeWidth=2))
    d.add(String(300, 370, "TileSet Editor", fontSize=16, textAnchor="middle", fillColor=colors.black))
    
    # Left panel - Tile Sources
    d.add(Rect(20, 200, 180, 160, fillColor=colors.white, strokeColor=colors.darkgrey))
    d.add(String(110, 345, "Tile Sources", fontSize=12, textAnchor="middle", fillColor=colors.darkblue))
    
    # Source files
    sources = ["grass_tiles.png", "stone_tiles.png", "water_tiles.png"]
    for i, source in enumerate(sources):
        y = 320 - i * 25
        d.add(String(30, y, f"├─ {source}", fontSize=9, fillColor=colors.black))
    
    # Center panel - Texture Preview
    d.add(Rect(220, 200, 200, 160, fillColor=colors.white, strokeColor=colors.darkgrey))
    d.add(String(320, 345, "Texture Preview", fontSize=12, textAnchor="middle", fillColor=colors.darkblue))
    
    # Tile grid
    tile_size = 25
    start_x, start_y = 240, 220
    tile_colors = [colors.lightgreen, colors.lightgrey, colors.lightblue, colors.yellow]
    tile_symbols = ["🌱", "🪨", "💧", "⭐"]
    
    for i in range(4):
        for j in range(2):
            x = start_x + i * (tile_size + 5)
            y = start_y + j * (tile_size + 5)
            color_idx = (i + j) % len(tile_colors)
            d.add(Rect(x, y, tile_size, tile_size, fillColor=tile_colors[color_idx], strokeColor=colors.black))
            # Add tile number
            d.add(String(x + tile_size/2, y + tile_size/2 - 3, str(i + j*4), 
                        fontSize=8, textAnchor="middle", fillColor=colors.black))
    
    # Selected tile highlight
    d.add(Rect(start_x + tile_size + 5, start_y, tile_size, tile_size, 
              fillColor=None, strokeColor=colors.red, strokeWidth=3))
    
    # Right panel - Properties
    d.add(Rect(440, 200, 140, 160, fillColor=colors.white, strokeColor=colors.darkgrey))
    d.add(String(510, 345, "Tile Properties", fontSize=12, textAnchor="middle", fillColor=colors.darkblue))
    
    # Property fields
    properties = ["Tile ID: 1", "Texture Region:", "X: 32  Y: 0", "W: 32  H: 32", "Collision Shape:", "Rectangle"]
    for i, prop in enumerate(properties):
        y = 320 - i * 18
        d.add(String(450, y, prop, fontSize=8, fillColor=colors.black))
    
    # Bottom section - Tools
    d.add(Rect(20, 20, 560, 160, fillColor=colors.white, strokeColor=colors.darkgrey))
    d.add(String(300, 165, "Configuration Tools", fontSize=12, textAnchor="middle", fillColor=colors.darkblue))
    
    # Tool buttons
    tools = ["Add Source", "Remove Source", "Create Animation", "Set Collision", "Custom Data"]
    for i, tool in enumerate(tools):
        x = 40 + i * 110
        d.add(Rect(x, 130, 100, 25, fillColor=colors.lightblue, strokeColor=colors.darkblue))
        d.add(String(x + 50, 140, tool, fontSize=9, textAnchor="middle", fillColor=colors.darkblue))
    
    return d

def create_tilemap_editor_mockup():
    """Create a mockup of the TileMap editor interface"""
    d = Drawing(600, 400)
    
    # Main window
    d.add(Rect(10, 10, 580, 380, fillColor=colors.lightgrey, strokeColor=colors.black, strokeWidth=2))
    d.add(String(300, 370, "TileMap Editor", fontSize=16, textAnchor="middle", fillColor=colors.black))
    
    # Left panel - Tools and Palette
    d.add(Rect(20, 100, 120, 260, fillColor=colors.white, strokeColor=colors.darkgrey))
    d.add(String(80, 345, "Tools & Palette", fontSize=12, textAnchor="middle", fillColor=colors.darkgreen))
    
    # Tool icons
    tools = ["🖌️ Paint", "📏 Line", "⬜ Rect", "🪣 Fill", "✋ Select"]
    for i, tool in enumerate(tools):
        y = 320 - i * 25
        d.add(Rect(30, y-5, 80, 20, fillColor=colors.lightyellow, strokeColor=colors.orange))
        d.add(String(35, y, tool, fontSize=9, fillColor=colors.black))
    
    # Tile palette
    d.add(String(80, 200, "Tile Palette", fontSize=10, textAnchor="middle", fillColor=colors.darkgreen))
    
    tile_size = 20
    start_x, start_y = 35, 120
    tile_colors = [colors.lightgreen, colors.lightgrey, colors.lightblue, colors.yellow]
    
    for i in range(4):
        for j in range(2):
            x = start_x + i * (tile_size + 2)
            y = start_y + j * (tile_size + 2)
            color_idx = (i + j) % len(tile_colors)
            d.add(Rect(x, y, tile_size, tile_size, fillColor=tile_colors[color_idx], strokeColor=colors.black))
    
    # Selected tile highlight
    d.add(Rect(start_x, start_y, tile_size, tile_size, 
              fillColor=None, strokeColor=colors.red, strokeWidth=2))
    
    # Right panel - Level Preview
    d.add(Rect(160, 100, 410, 260, fillColor=colors.white, strokeColor=colors.darkgrey))
    d.add(String(365, 345, "Level Preview", fontSize=12, textAnchor="middle", fillColor=colors.darkgreen))
    
    # Grid with placed tiles
    grid_size = 18
    grid_start_x, grid_start_y = 180, 120
    
    # Create a simple level pattern
    level_pattern = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0],
        [0, 1, 3, 1, 0, 2, 2, 1, 3, 1, 0, 2, 2, 1, 3, 1, 0, 0, 0],
        [0, 1, 1, 1, 0, 2, 2, 1, 1, 1, 0, 2, 2, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
    
    for row_idx, row in enumerate(level_pattern):
        for col_idx, tile_type in enumerate(row):
            if col_idx >= 20:  # Limit grid width
                break
            x = grid_start_x + col_idx * grid_size
            y = grid_start_y + (len(level_pattern) - row_idx - 1) * grid_size
            
            if tile_type == 0:
                continue  # Empty space
            
            color = tile_colors[tile_type % len(tile_colors)]
            d.add(Rect(x, y, grid_size-1, grid_size-1, fillColor=color, strokeColor=colors.black))
    
    # Layers panel
    d.add(String(80, 80, "Layers", fontSize=10, textAnchor="middle", fillColor=colors.darkgreen))
    layers = ["👁️ Background", "👁️ Main", "🔒 Foreground"]
    for i, layer in enumerate(layers):
        y = 60 - i * 15
        d.add(String(30, y, layer, fontSize=8, fillColor=colors.black))
    
    return d

def create_workflow_diagram():
    """Create a workflow comparison diagram"""
    d = Drawing(600, 300)
    
    # Title
    d.add(String(300, 280, "Workflow Comparison", fontSize=16, textAnchor="middle", fillColor=colors.black))
    
    # TileSet workflow (left side)
    ts_x = 50
    d.add(String(ts_x + 75, 250, "TileSet Editor Workflow", fontSize=14, textAnchor="middle", fillColor=colors.darkblue))
    
    ts_steps = [
        "1. Create TileSet Resource",
        "2. Import Source Textures", 
        "3. Configure Tile Regions",
        "4. Set Up Collision Shapes",
        "5. Add Custom Properties",
        "6. Save TileSet Resource"
    ]
    
    for i, step in enumerate(ts_steps):
        y = 220 - i * 35
        # Step box
        d.add(Rect(ts_x, y, 150, 25, fillColor=colors.lightblue, strokeColor=colors.darkblue, strokeWidth=1))
        d.add(String(ts_x + 75, y + 12, step, fontSize=9, textAnchor="middle", fillColor=colors.darkblue))
        
        # Arrow to next step
        if i < len(ts_steps) - 1:
            d.add(Line(ts_x + 75, y, ts_x + 75, y - 10, strokeColor=colors.darkblue, strokeWidth=2))
            # Arrow head
            d.add(Line(ts_x + 70, y - 7, ts_x + 75, y - 10, strokeColor=colors.darkblue, strokeWidth=2))
            d.add(Line(ts_x + 80, y - 7, ts_x + 75, y - 10, strokeColor=colors.darkblue, strokeWidth=2))
    
    # TileMap workflow (right side)
    tm_x = 400
    d.add(String(tm_x + 75, 250, "TileMap Editor Workflow", fontSize=14, textAnchor="middle", fillColor=colors.darkgreen))
    
    tm_steps = [
        "1. Add TileMap Node",
        "2. Assign TileSet Resource",
        "3. Select Painting Tools",
        "4. Choose Tiles from Palette",
        "5. Paint Level Layout",
        "6. Test Gameplay"
    ]
    
    for i, step in enumerate(tm_steps):
        y = 220 - i * 35
        # Step box
        d.add(Rect(tm_x, y, 150, 25, fillColor=colors.lightgreen, strokeColor=colors.darkgreen, strokeWidth=1))
        d.add(String(tm_x + 75, y + 12, step, fontSize=9, textAnchor="middle", fillColor=colors.darkgreen))
        
        # Arrow to next step
        if i < len(tm_steps) - 1:
            d.add(Line(tm_x + 75, y, tm_x + 75, y - 10, strokeColor=colors.darkgreen, strokeWidth=2))
            # Arrow head
            d.add(Line(tm_x + 70, y - 7, tm_x + 75, y - 10, strokeColor=colors.darkgreen, strokeWidth=2))
            d.add(Line(tm_x + 80, y - 7, tm_x + 75, y - 10, strokeColor=colors.darkgreen, strokeWidth=2))
    
    # Connection arrow between workflows
    d.add(Line(220, 150, 380, 150, strokeColor=colors.orange, strokeWidth=3))
    d.add(String(300, 165, "Uses", fontSize=12, textAnchor="middle", fillColor=colors.orange))
    # Arrow head
    d.add(Line(375, 145, 380, 150, strokeColor=colors.orange, strokeWidth=3))
    d.add(Line(375, 155, 380, 150, strokeColor=colors.orange, strokeWidth=3))
    
    return d

def create_architecture_diagram():
    """Create a system architecture diagram"""
    d = Drawing(600, 300)
    
    # Title
    d.add(String(300, 280, "TileSet & TileMap Architecture", fontSize=16, textAnchor="middle", fillColor=colors.black))
    
    # TileSet Resource
    d.add(Rect(50, 200, 200, 60, fillColor=colors.lightblue, strokeColor=colors.darkblue, strokeWidth=2))
    d.add(String(150, 235, "TileSet Resource", fontSize=14, textAnchor="middle", fillColor=colors.darkblue))
    d.add(String(150, 220, "(.tres file)", fontSize=10, textAnchor="middle", fillColor=colors.darkblue))
    d.add(String(150, 210, "Contains tile definitions", fontSize=9, textAnchor="middle", fillColor=colors.darkblue))
    
    # Individual tiles
    tile_data = ["Texture", "Collision", "Properties", "Animation"]
    for i, data in enumerate(tile_data):
        x = 70 + i * 40
        d.add(Rect(x, 160, 35, 30, fillColor=colors.lightcyan, strokeColor=colors.darkblue))
        d.add(String(x + 17, 175, data, fontSize=7, textAnchor="middle", fillColor=colors.darkblue))
        # Connection line
        d.add(Line(x + 17, 190, x + 17, 200, strokeColor=colors.darkblue))
    
    # TileMap Node
    d.add(Rect(350, 200, 200, 60, fillColor=colors.lightgreen, strokeColor=colors.darkgreen, strokeWidth=2))
    d.add(String(450, 235, "TileMap Node", fontSize=14, textAnchor="middle", fillColor=colors.darkgreen))
    d.add(String(450, 220, "(Scene node)", fontSize=10, textAnchor="middle", fillColor=colors.darkgreen))
    d.add(String(450, 210, "Uses TileSet to create levels", fontSize=9, textAnchor="middle", fillColor=colors.darkgreen))
    
    # TileMap components
    map_components = ["Grid", "Layers", "Painting", "Runtime"]
    for i, comp in enumerate(map_components):
        x = 370 + i * 40
        d.add(Rect(x, 160, 35, 30, fillColor=colors.lightgrey, strokeColor=colors.darkgreen))
        d.add(String(x + 17, 175, comp, fontSize=7, textAnchor="middle", fillColor=colors.darkgreen))
        # Connection line
        d.add(Line(x + 17, 190, x + 17, 200, strokeColor=colors.darkgreen))
    
    # Relationship arrow
    d.add(Line(270, 230, 330, 230, strokeColor=colors.purple, strokeWidth=3))
    d.add(String(300, 245, "References", fontSize=10, textAnchor="middle", fillColor=colors.purple))
    # Arrow head
    d.add(Line(325, 225, 330, 230, strokeColor=colors.purple, strokeWidth=3))
    d.add(Line(325, 235, 330, 230, strokeColor=colors.purple, strokeWidth=3))
    
    # Game Scene
    d.add(Rect(200, 80, 200, 40, fillColor=colors.lightyellow, strokeColor=colors.orange, strokeWidth=2))
    d.add(String(300, 105, "Game Scene", fontSize=14, textAnchor="middle", fillColor=colors.orange))
    d.add(String(300, 90, "Contains TileMap nodes", fontSize=10, textAnchor="middle", fillColor=colors.orange))
    
    # Connection from TileMap to Scene
    d.add(Line(450, 200, 450, 140, strokeColor=colors.orange, strokeWidth=2))
    d.add(Line(450, 140, 350, 120, strokeColor=colors.orange, strokeWidth=2))
    # Arrow head
    d.add(Line(355, 115, 350, 120, strokeColor=colors.orange, strokeWidth=2))
    d.add(Line(355, 125, 350, 120, strokeColor=colors.orange, strokeWidth=2))
    
    return d

def main():
    """Generate all visual diagrams"""
    diagrams = [
        ("TileSet_Editor_Mockup", create_tileset_editor_mockup()),
        ("TileMap_Editor_Mockup", create_tilemap_editor_mockup()),
        ("Workflow_Comparison", create_workflow_diagram()),
        ("System_Architecture", create_architecture_diagram())
    ]
    
    for name, drawing in diagrams:
        filename = f"{name}.pdf"
        renderPDF.drawToFile(drawing, filename)
        print(f"Created diagram: {filename}")

if __name__ == "__main__":
    main()