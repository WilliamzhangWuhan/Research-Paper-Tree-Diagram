# Enhanced Paper Tree Classifier - Final Version

A comprehensive tree-structured paper classification system with subcategory support, paper references, and deletion capabilities.

## 🌟 Features

- 🌳 **Dynamic Tree Structure**: Supports custom parent node names and structures
- 📝 **Automatic ID Management**: Automatically assigns unique IDs for each new paper
- 🎨 **Visualization**: Generates clear tree structure diagrams with paper nodes displayed as circles
- 💾 **State Persistence**: Supports saving and loading classification states
- 🔄 **Flexible Classification**: Supports specifying parent categories or using default categories
- 🗂️ **Subcategory Support**: Create nested categories with unlimited depth
- 📚 **Paper References**: Display complete paper titles below the tree structure
- 🗑️ **Deletion Management**: Delete papers by ID or entire categories
- 🔍 **Category Hierarchy**: View and manage category relationships

## 🚀 Installation

```bash
pip install -r requirements.txt
```

## 📖 Usage

### 1. Run Program

```bash
python enhanced_paper_classifier.py
```

### 2. Basic Operations

#### Add Paper to Root Category
```
Enter paper title (or command): Introduction to Machine Learning
Added paper 'Introduction to Machine Learning' to Root category, ID: 1
```

#### Add Paper to Main Category
```
Enter paper title (or command): Machine Learning:Support Vector Machine Research
Added paper 'Support Vector Machine Research' to category 'Machine Learning', ID: 2
```

#### Add Paper to Subcategory
```
Enter paper title (or command): Machine Learning:Deep Learning:Convolutional Neural Networks
Added paper 'Convolutional Neural Networks' to subcategory 'Machine Learning:Deep Learning', ID: 3
```

#### View Tree Structure
```
Enter paper title (or command): show
```
This will display a visualization of the tree structure with all nodes and paper references below.

#### View Papers List
```
Enter paper title (or command): list
```

#### View Category Hierarchy
```
Enter paper title (or command): categories
```

### 3. Deletion Commands

#### Delete Paper by ID
```
Enter paper title (or command): delete paper 2
Deleted paper 'Support Vector Machine Research' (ID: 2)
```

#### Delete Category and All Its Papers
```
Enter paper title (or command): delete category Machine Learning
Deleted category 'Machine Learning' and all its papers
```

### 4. Available Commands

- `help` - Show help information
- `show` - Display tree structure with paper references
- `list` - Show papers list sorted by ID with category information
- `categories` - Show category hierarchy
- `delete paper ID` - Delete paper by ID (e.g., `delete paper 1`)
- `delete category NAME` - Delete category and all its papers (e.g., `delete category Machine Learning`)
- `save` - Save current state to file
- `load` - Load previous state from file
- `quit` - Exit program

## 🎯 File Structure

- `enhanced_paper_classifier.py` - **Main program file** (final version)
- `final_demo.py` - Complete feature demonstration script
- `requirements.txt` - Python dependencies list
- `README_FINAL.md` - This documentation file

## 🌳 Tree Structure Description

- **Root Node** (blue circle): System starting point
- **Main Category** (green rectangle): Primary classification categories
- **Subcategory** (yellow rectangle): Nested categories under main categories
- **Paper Node** (red circle): Specific paper titles with IDs

## 📊 Example Usage Flow

1. Start program: `python enhanced_paper_classifier.py`
2. Add papers to different categories:
   - `Machine Learning:Deep Learning:Convolutional Neural Networks`
   - `Computer Vision:Object Detection:YOLO Algorithm`
   - `Natural Language Processing:Transformer Models:BERT`
3. Input `show` to view tree structure
4. Input `list` to view papers list
5. Input `categories` to view category hierarchy
6. Delete specific papers: `delete paper 2`
7. Delete categories: `delete category Computer Vision`
8. Input `save` to save current state
9. Continue managing your paper collection...

## 🗑️ Deletion Features

### Paper Deletion
- Delete papers by their unique ID
- Automatically removes from tree structure
- Updates category references
- **IDs are automatically reassigned sequentially starting from 1**
- Maintains relative order of remaining papers

### Category Deletion
- Delete entire categories and all contained papers
- Cascading deletion of subcategories
- Automatic cleanup of empty categories
- Cannot delete Root category

## 🔧 Technical Implementation

- Uses `matplotlib` for graphics drawing and visualization
- Supports dynamic layout adjustment for any number of nodes
- Complete error handling and user input validation
- JSON-based state persistence with UTF-8 support
- Intelligent text wrapping for long paper titles
- Automatic category hierarchy management

## 📱 Demo Scripts

### Quick Demo
```bash
python final_demo.py
```
This demonstrates all features including:
- Adding papers to different category levels
- Creating subcategories
- Deleting papers and categories
- Generating before/after visualizations

## ⚠️ Notes

- Paper title cannot be empty
- Category names and paper titles separated by colon (:)
- Images automatically adjust layout for different numbers of nodes
- State files use JSON format, support English text
- Deletion operations are irreversible (use save/load for backup)
- Root category cannot be deleted

## 🎨 Visual Features

- **Color-coded nodes**: Different colors for different node types
- **Smart layout system**: Prevents overlapping of categories and papers
- **Automatic spacing**: Intelligent distribution of multiple subcategories
- **Dynamic text wrapping**: Long category names automatically wrap to prevent overlap
- **Connection line optimization**: Lines connect precisely to node boundaries without penetration
- **Paper references**: Complete bibliography below the tree
- **Legend**: Easy identification of node types
- **High-resolution output**: 300 DPI images for professional use
- **Layout optimization**: Automatically adjusts for any number of nodes and text lengths

## 🔄 State Management

- Save current state: `save`
- Load previous state: `load`
- Automatic state file creation
- JSON format for easy editing and backup
- Complete preservation of all data structures

This is the final, production-ready version of the Enhanced Paper Tree Classifier with all features implemented and tested.
