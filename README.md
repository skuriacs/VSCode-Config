# Godot TileMap vs TileSet Documentation Package

This repository now includes comprehensive documentation explaining the differences between Godot's TileMap and TileSet editors, complete with visual aids and practical examples.

## 📋 Overview

The documentation package consists of:

1. **Main Guide**: `Godot_TileMap_vs_TileSet_Guide.pdf` - A complete 8-page PDF guide
2. **Visual Diagrams**: Four separate PDF diagrams showing editor interfaces and workflows
3. **Source Files**: Markdown source and Python generation scripts

## 📖 Main Documentation

### `Godot_TileMap_vs_TileSet_Guide.pdf`
**Size**: ~14.6 KB | **Pages**: 8

This comprehensive guide includes:

- **Introduction** to both TileSet and TileMap concepts
- **Detailed comparison** of features and use cases
- **Key differences** explained with examples
- **Workflow explanations** for both editors
- **Best practices** and common mistakes to avoid
- **When to use each editor** with practical guidance

### 📊 Visual Diagrams

The package includes four visual PDF diagrams:

1. **`TileSet_Editor_Mockup.pdf`** - Interface mockup showing the TileSet editor layout
2. **`TileMap_Editor_Mockup.pdf`** - Interface mockup showing the TileMap editor layout
3. **`Workflow_Comparison.pdf`** - Side-by-side workflow comparison diagram
4. **`System_Architecture.pdf`** - System architecture showing relationships between components

## 🎯 Key Concepts Explained

### TileSet Editor
- **Purpose**: Create and configure tile resources
- **File Type**: `.tres` resource files
- **Focus**: Individual tile properties, collision shapes, animations
- **Usage**: Setup phase (less frequent)

### TileMap Editor
- **Purpose**: Arrange tiles to create game levels
- **File Type**: Part of scene (`.tscn`) files
- **Focus**: Level design, tile placement, layer management
- **Usage**: Design phase (frequent)

## 🔧 VSCode Integration

This documentation is particularly relevant for developers using this VSCode configuration, as it includes:

- **Godot Tools extension** configured in the profile
- **GDScript formatting and linting** setup
- **Optimized workflow** for Godot development

The VSCode profile (`Sam.code-profile`) includes:
- Godot LSP server configuration (`godotTools.lsp.serverPort: 6005`)
- GDScript formatter setup
- Vim keybindings optimized for game development

## 📂 File Structure

```
VSCode-Config/
├── Sam.code-profile                          # VSCode configuration profile
├── Godot_TileMap_vs_TileSet_Guide.md         # Markdown source
├── Godot_TileMap_vs_TileSet_Guide.pdf        # Main PDF guide (8 pages)
├── TileSet_Editor_Mockup.pdf                 # Visual diagram
├── TileMap_Editor_Mockup.pdf                 # Visual diagram
├── Workflow_Comparison.pdf                   # Visual diagram
├── System_Architecture.pdf                   # Visual diagram
├── create_pdf.py                             # PDF generation script
├── create_diagrams.py                        # Diagram generation script
└── README.md                                 # This file
```

## 🚀 Usage

### For Godot Developers:
1. Read the main guide: `Godot_TileMap_vs_TileSet_Guide.pdf`
2. Reference the visual diagrams when needed
3. Apply the VSCode configuration for optimized Godot development

### For Documentation Updates:
1. Edit the Markdown source: `Godot_TileMap_vs_TileSet_Guide.md`
2. Run the generation script: `python3 create_pdf.py`
3. Update diagrams if needed: `python3 create_diagrams.py`

## 🔄 Generation Scripts

The documentation can be regenerated using the included Python scripts:

- **`create_pdf.py`**: Converts Markdown to styled PDF with proper formatting
- **`create_diagrams.py`**: Generates visual diagrams using ReportLab

### Requirements:
```bash
pip install reportlab markdown
```

## 📌 Quick Reference

| Aspect | TileSet Editor | TileMap Editor |
|--------|----------------|----------------|
| **Purpose** | Define tiles | Arrange tiles |
| **File Type** | `.tres` resources | Scene nodes |
| **Focus** | Tile properties | Level layout |
| **Frequency** | Setup phase | Design phase |

## 🎮 Godot Version Compatibility

This documentation applies to:
- **Godot 4.x** (primary focus)
- **Godot 3.x** (most concepts apply)

The visual examples and interface mockups are based on Godot 4.x editor layouts.

---

*This documentation package was created to help developers understand the distinction between TileSet and TileMap editors in Godot, making 2D game development more efficient and organized.*