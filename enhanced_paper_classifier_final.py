import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import numpy as np
from typing import Dict, List, Optional, Tuple
import json
import os

class EnhancedPaperTreeClassifier:
    def __init__(self):
        """Initialize enhanced paper tree classifier with subcategory support"""
        self.tree_structure = {}
        self.papers = []
        self.node_counter = 0
        self.parent_nodes = {}
        self.category_hierarchy = {}
        
    def add_category(self, category_name: str, parent_category: str = "Root") -> bool:
        if category_name == "Root":
            return False
            
        if parent_category not in self.category_hierarchy:
            self.category_hierarchy[parent_category] = []
        
        if category_name not in self.category_hierarchy[parent_category]:
            self.category_hierarchy[parent_category].append(category_name)
            
        if category_name not in self.tree_structure:
            self.tree_structure[category_name] = []
            
        return True
    
    def add_paper(self, paper_title: str, category_path: str = "Root") -> int:
        self.node_counter += 1
        node_id = self.node_counter
        
        paper_info = {
            'id': node_id,
            'title': paper_title,
            'category_path': category_path
        }
        self.papers.append(paper_info)
        
        if category_path not in self.tree_structure:
            self.tree_structure[category_path] = []
        self.tree_structure[category_path].append(node_id)
        
        self.parent_nodes[node_id] = category_path
        
        return node_id
    
    def get_papers_by_order(self) -> List[str]:
        return [paper['title'] for paper in sorted(self.papers, key=lambda x: x['id'])]
    
    def get_category_tree(self) -> Dict:
        return self.category_hierarchy
    
    def delete_paper_by_id(self, paper_id: int) -> bool:
        paper_to_delete = None
        for paper in self.papers:
            if paper['id'] == paper_id:
                paper_to_delete = paper
                break
        
        if not paper_to_delete:
            print(f"Paper with ID {paper_id} not found")
            return False
        
        self.papers.remove(paper_to_delete)
        
        category_path = paper_to_delete['category_path']
        if category_path in self.tree_structure:
            if paper_id in self.tree_structure[category_path]:
                self.tree_structure[category_path].remove(paper_id)
        
        if paper_id in self.parent_nodes:
            del self.parent_nodes[paper_id]
        
        self._reassign_paper_ids()
        
        print(f"Deleted paper '{paper_to_delete['title']}' (ID: {paper_id})")
        return True
    
    def _reassign_paper_ids(self):
        if not self.papers:
            self.node_counter = 0
            return
        
        sorted_papers = sorted(self.papers, key=lambda x: x['id'])
        
        id_mapping = {}
        for i, paper in enumerate(sorted_papers, 1):
            old_id = paper['id']
            new_id = i
            id_mapping[old_id] = new_id
            paper['id'] = new_id
        
        for category_path, paper_ids in self.tree_structure.items():
            new_paper_ids = []
            for old_id in paper_ids:
                if old_id in id_mapping:
                    new_paper_ids.append(id_mapping[old_id])
            self.tree_structure[category_path] = new_paper_ids
        
        new_parent_nodes = {}
        for old_id, category_path in self.parent_nodes.items():
            if old_id in id_mapping:
                new_parent_nodes[id_mapping[old_id]] = category_path
        self.parent_nodes = new_parent_nodes
        
        self.node_counter = len(self.papers)
    
    def delete_category(self, category_name: str) -> bool:
        if category_name == "Root":
            print("Cannot delete Root category")
            return False
        
        if category_name not in self.tree_structure:
            print(f"Category '{category_name}' not found")
            return False
        
        papers_to_delete = self.tree_structure[category_name].copy()
        
        for paper_id in papers_to_delete:
            self.delete_paper_by_id(paper_id)
        
        del self.tree_structure[category_name]
        
        for parent_cat, subcats in self.category_hierarchy.items():
            if category_name in subcats:
                subcats.remove(category_name)
                break
        
        print(f"Deleted category '{category_name}' and all its papers")
        return True
    
    def get_paper_by_id(self, paper_id: int) -> Optional[Dict]:
        for paper in self.papers:
            if paper['id'] == paper_id:
                return paper
        return None
    
    def visualize_tree(self, save_path: str = None) -> None:
        if not self.papers:
            print("No papers added yet")
            return
            
        num_categories = len([cat for cat in self.tree_structure.keys() if cat != "Root"])
        num_papers = len(self.papers)
        
        base_width = 30
        base_height = 25
        
        if num_categories > 10:
            base_width = 35
        if num_papers > 40:
            base_height = 30
        
        self._create_simple_interactive_visualization(base_width, base_height, save_path)
    
    def _create_simple_interactive_visualization(self, base_width, base_height, save_path):
        """Create simple matplotlib window with mouse drag and wheel zoom"""
        fig, ax = plt.subplots(1, 1, figsize=(16, 12))
        ax.set_xlim(0, base_width)
        ax.set_ylim(0, base_height)
        ax.axis('off')
        
        # Initialize drag state
        ax._drag_start = None
        
        self._draw_complete_tree(ax, base_width, base_height)
        
        # Add title to the figure
        fig.suptitle("Enhanced Paper Classification Tree", 
                     fontsize=14, y=0.95)
        
        # Enable mouse interactions
        def on_scroll(event):
            if event.inaxes != ax:
                return
            
            # Get current limits
            cur_xlim = ax.get_xlim()
            cur_ylim = ax.get_ylim()
            
            # Get event location
            xdata = event.xdata
            ydata = event.ydata
            
            # Zoom factor
            if event.button == 'up':
                scale_factor = 0.9
            else:
                scale_factor = 1.1
            
            # Set new limits
            new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
            new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor
            
            relx = (cur_xlim[1] - xdata) / (cur_xlim[1] - cur_xlim[0])
            rely = (cur_ylim[1] - ydata) / (cur_ylim[1] - cur_ylim[0])
            
            ax.set_xlim([xdata - new_width * (1 - relx), xdata + new_width * relx])
            ax.set_ylim([ydata - new_height * (1 - rely), ydata + new_height * rely])
            
            fig.canvas.draw()
        
        def on_mouse_press(event):
            if event.inaxes != ax:
                return
            ax._drag_start = (event.xdata, event.ydata)
        
        def on_mouse_release(event):
            if event.inaxes != ax:
                return
            ax._drag_start = None
        
        def on_mouse_move(event):
            if event.inaxes != ax or ax._drag_start is None:
                return
            
            dx = event.xdata - ax._drag_start[0]
            dy = event.ydata - ax._drag_start[1]
            
            cur_xlim = ax.get_xlim()
            cur_ylim = ax.get_ylim()
            
            ax.set_xlim(cur_xlim[0] - dx, cur_xlim[1] - dx)
            ax.set_ylim(cur_ylim[0] - dy, cur_ylim[1] - dy)
            
            ax._drag_start = (event.xdata, event.ydata)
            fig.canvas.draw()
        
        def on_key(event):
            if event.key == 'r':
                # Reset view
                ax.set_xlim(0, base_width)
                ax.set_ylim(0, base_height)
                fig.canvas.draw()
            elif event.key == 's' and save_path:
                # Save image
                fig.savefig(save_path, dpi=300, bbox_inches='tight')
                print(f"Image saved to: {save_path}")
        
        # Connect events
        fig.canvas.mpl_connect('scroll_event', on_scroll)
        fig.canvas.mpl_connect('button_press_event', on_mouse_press)
        fig.canvas.mpl_connect('button_release_event', on_mouse_release)
        fig.canvas.mpl_connect('motion_notify_event', on_mouse_move)
        fig.canvas.mpl_connect('key_press_event', on_key)
        
        # Add instructions
        ax.text(base_width/2, base_height + 1, 
                "Mouse: Drag to move | Scroll: Zoom in/out | R: Reset view | S: Save image", 
                ha='center', va='center', fontsize=10, style='italic')
        
        if save_path:
            print(f"Press 'S' to save image to: {save_path}")
        
        print("\n=== Interactive Controls ===")
        print("🖱️  Mouse: Drag to move around the tree")
        print("🔍 Scroll: Zoom in/out with mouse wheel")
        print("🔄 R key: Reset to full view")
        print("💾 S key: Save current view as image")
        print("❌ Close window to return to console")
        
        plt.tight_layout()
        plt.show()
    

    
    def _draw_complete_tree(self, ax, base_width, base_height):
        root_x = base_width / 2
        root_y = base_height - 3
        root_circle = plt.Circle((root_x, root_y), 0.5, fill=True, color='lightblue', edgecolor='black', linewidth=2)
        ax.add_patch(root_circle)
        ax.text(root_x, root_y, "Root", ha='center', va='center', fontsize=12, weight='bold')
        
        self._calculate_category_positions_no_overlap(base_width, base_height, root_x, root_y)
        
        self._draw_categories_no_overlap(ax, root_y, root_x)
        
        ax.text(root_x, root_y + 1.5, "Enhanced Paper Classification Tree with Subcategories", 
                ha='center', va='center', fontsize=16, weight='bold')
        
        legend_elements = [
            plt.Circle((0, 0), 0.1, color='lightblue', label='Root Node'),
            plt.Rectangle((0, 0), 0.2, 0.1, color='lightgreen', label='Main Category (Level 1)'),
            plt.Rectangle((0, 0), 0.2, 0.1, color='lightyellow', label='Subcategory (Level 2)'),
            plt.Rectangle((0, 0), 0.2, 0.1, color='lightgoldenrodyellow', label='Deep Subcategory (Level 3+)'),
            plt.Circle((0, 0), 0.1, color='lightcoral', label='Paper Node')
        ]
        ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(0.98, 0.98))
        
        self._add_paper_references(ax)
    
    def _calculate_category_positions_no_overlap(self, base_width, base_height, root_x, root_y):
        self.category_positions = {}
        
        all_categories = [cat for cat in self.tree_structure.keys() if cat != "Root"]
        
        if not all_categories:
            return
            
        # Group categories by their level (number of colons)
        categories_by_level = {}
        for cat in all_categories:
            level = cat.count(':') + 1
            if level not in categories_by_level:
                categories_by_level[level] = []
            categories_by_level[level].append(cat)
        
        # Position main categories (level 1) with fixed spacing
        if 1 in categories_by_level:
            main_categories = categories_by_level[1]
            if len(main_categories) == 1:
                self.category_positions[main_categories[0]] = {'x': root_x, 'y': root_y - 5, 'level': 1}
            else:
                total_width_needed = len(main_categories) * 5
                start_x = root_x - total_width_needed / 2 + 2.5
                
                for i, cat in enumerate(main_categories):
                    x = start_x + i * 5
                    self.category_positions[cat] = {'x': x, 'y': root_y - 5, 'level': 1}
        
        # Position subcategories (level 2 and higher) with proper spacing
        for level in range(2, max(categories_by_level.keys()) + 1):
            if level not in categories_by_level:
                continue
                
            level_categories = categories_by_level[level]
            
            # Group by parent category
            parent_subcat_map = {}
            for cat in level_categories:
                parent_cat = ':'.join(cat.split(':')[:-1])  # Get parent by removing last part
                if parent_cat not in parent_subcat_map:
                    parent_subcat_map[parent_cat] = []
                parent_subcat_map[parent_cat].append(cat)
            
            for parent_cat, subcats in parent_subcat_map.items():
                if parent_cat not in self.category_positions:
                    continue
                    
                parent_x = self.category_positions[parent_cat]['x']
                parent_y = self.category_positions[parent_cat]['y']
                
                # Calculate spacing based on level (deeper levels get more spacing)
                spacing_multiplier = 3.5 + (level - 2) * 0.5  # Level 2: 3.5, Level 3: 4.0, etc.
                y_offset = 5 + (level - 2) * 2  # Level 2: 5, Level 3: 7, etc.
                
                if len(subcats) == 1:
                    self.category_positions[subcats[0]] = {
                        'x': parent_x, 
                        'y': parent_y - y_offset, 
                        'level': level
                    }
                else:
                    total_width_needed = len(subcats) * spacing_multiplier
                    start_x = parent_x - total_width_needed / 2 + spacing_multiplier / 2
                    
                    for i, subcat in enumerate(subcats):
                        x = start_x + i * spacing_multiplier
                        self.category_positions[subcat] = {
                            'x': x, 
                            'y': parent_y - y_offset, 
                            'level': level
                        }
    
    def _draw_categories_no_overlap(self, ax, root_y, root_x):
        # Draw main categories (level 1)
        for cat_name, papers in self.tree_structure.items():
            if cat_name == "Root":
                if papers:
                    self._draw_root_papers(ax, papers, root_y, root_x)
                continue
                
            if cat_name not in self.category_positions:
                continue
                
            pos = self.category_positions[cat_name]
            
            if pos['level'] == 1:
                cat_rect = FancyBboxPatch(
                    (pos['x'] - 2.0, pos['y'] - 0.5),
                    4.0, 1.0,
                    boxstyle="round,pad=0.1",
                    facecolor='lightgreen',
                    edgecolor='black',
                    linewidth=2
                )
                ax.add_patch(cat_rect)
                ax.text(pos['x'], pos['y'], cat_name, ha='center', va='center', 
                       fontsize=10, weight='bold')
                
                ax.plot([root_x, pos['x']], [root_y - 0.5, pos['y'] + 0.5], 'k-', linewidth=2)
                
                if papers:
                    self._draw_category_papers(ax, papers, pos['x'], pos['y'], pos['y'] - 3)
        
        # Draw subcategories (level 2 and higher)
        for cat_name, papers in self.tree_structure.items():
            if cat_name in self.category_positions and self.category_positions[cat_name]['level'] >= 2:
                pos = self.category_positions[cat_name]
                
                # Determine box size and color based on level
                if pos['level'] == 2:
                    box_width, box_height = 3.0, 0.8
                    face_color = 'lightyellow'
                    line_width = 1.5
                    font_size = 9
                else:
                    # Deeper levels get smaller boxes
                    box_width = max(2.0, 3.0 - (pos['level'] - 2) * 0.3)
                    box_height = max(0.6, 0.8 - (pos['level'] - 2) * 0.1)
                    face_color = 'lightgoldenrodyellow'
                    line_width = 1.0
                    font_size = max(7, 9 - (pos['level'] - 2))
                
                subcat_rect = FancyBboxPatch(
                    (pos['x'] - box_width/2, pos['y'] - box_height/2),
                    box_width, box_height,
                    boxstyle="round,pad=0.1",
                    facecolor=face_color,
                    edgecolor='black',
                    linewidth=line_width
                )
                ax.add_patch(subcat_rect)
                
                # Get the display name (last part of the category path)
                subcat_name = cat_name.split(':')[-1]
                if len(subcat_name) > 25:
                    wrapped_name = self._wrap_text(subcat_name, box_width - 0.5)
                    lines = wrapped_name.split('\n')
                    for i, line in enumerate(lines):
                        line_y = pos['y'] + 0.1 - i * 0.15
                        ax.text(pos['x'], line_y, line, ha='center', va='center', 
                               fontsize=font_size, weight='bold')
                else:
                    ax.text(pos['x'], pos['y'], subcat_name, ha='center', va='center', 
                           fontsize=font_size, weight='bold')
                
                # Draw connection line to parent
                parent_cat = ':'.join(cat_name.split(':')[:-1])  # Get parent by removing last part
                if parent_cat in self.category_positions:
                    parent_y = self.category_positions[parent_cat]['y']
                    parent_x = self.category_positions[parent_cat]['x']
                    ax.plot([parent_x, pos['x']], [parent_y - 0.5, pos['y'] + box_height/2], 'k-', linewidth=line_width)
                
                if papers:
                    self._draw_category_papers(ax, papers, pos['x'], pos['y'], pos['y'] - 3)
    
    def _draw_root_papers(self, ax, papers, root_y, root_x):
        if not papers:
            return
            
        if len(papers) == 1:
            paper_x = root_x
        else:
            total_width_needed = len(papers) * 2
            start_x = root_x - total_width_needed / 2 + 1
            paper_x = start_x
        
        for j, paper_id in enumerate(papers):
            if len(papers) > 1:
                paper_x = root_x - total_width_needed / 2 + 1 + j * 2
            
            paper_y = root_y - 2
            
            paper_circle = plt.Circle((paper_x, paper_y), 0.3, fill=True, 
                                    color='lightcoral', edgecolor='black', linewidth=1.5)
            ax.add_patch(paper_circle)
            
            ax.text(paper_x, paper_y, str(paper_id), ha='center', va='center', 
                   fontsize=10, weight='bold')
            
            ax.plot([root_x, paper_x], [root_y - 0.5, paper_y + 0.3], 'k-', linewidth=1.5)
    
    def _draw_category_papers(self, ax, papers, cat_x, cat_y, target_y):
        if not papers:
            return
            
        if len(papers) == 1:
            paper_x = cat_x
            paper_y = target_y
            
            paper_circle = plt.Circle((paper_x, paper_y), 0.3, fill=True, 
                                    color='lightcoral', edgecolor='black', linewidth=1.5)
            ax.add_patch(paper_circle)
            
            ax.text(paper_x, paper_y, str(papers[0]), ha='center', va='center', 
                   fontsize=10, weight='bold')
            
            ax.plot([cat_x, paper_x], [cat_y - 0.5, paper_y + 0.3], 'k-', linewidth=1.5)
        else:
            total_width_needed = len(papers) * 1.5
            start_x = cat_x - total_width_needed / 2 + 0.75
            
            for j, paper_id in enumerate(papers):
                paper_x = start_x + j * 1.5
                paper_y = target_y
                
                paper_circle = plt.Circle((paper_x, paper_y), 0.3, fill=True, 
                                        color='lightcoral', edgecolor='black', linewidth=1.5)
                ax.add_patch(paper_circle)
                
                ax.text(paper_x, paper_y, str(paper_id), ha='center', va='center', 
                       fontsize=10, weight='bold')
                
                ax.plot([cat_x, paper_x], [cat_y - 0.5, paper_y + 0.3], 'k-', linewidth=1.5)
    
    def _add_paper_references(self, ax) -> None:
        if not self.papers:
            return
            
        sorted_papers = sorted(self.papers, key=lambda x: x['id'])
        
        ref_start_y = 2
        ref_x = 2
        line_height = 0.4
        
        ax.text(15, ref_start_y + 3, "Paper References", ha='center', va='center', 
                fontsize=14, weight='bold', style='italic')
        
        ax.plot([2, 28], [ref_start_y + 2, ref_start_y + 2], 'k-', linewidth=1, alpha=0.3)
        
        for i, paper in enumerate(sorted_papers):
            y_pos = ref_start_y + 1 - i * line_height
            
            ref_text = f"[{paper['id']}] {paper['title']}"
            if paper['category_path'] != "Root":
                ref_text += f" (Category: {paper['category_path']})"
            
            wrapped_text = self._wrap_text(ref_text, max_width=25)
            
            lines = wrapped_text.split('\n')
            for j, line in enumerate(lines):
                line_y = y_pos + j * 0.15
                ax.text(ref_x, line_y, line, ha='left', va='center', 
                       fontsize=9, style='italic')
    
    def _wrap_text(self, text: str, max_width: float) -> str:
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + " " + word if current_line else word
            if len(test_line) * 0.07 > max_width and current_line:
                lines.append(current_line)
                current_line = word
            else:
                current_line = test_line
        
        if current_line:
            lines.append(current_line)
        
        return '\n'.join(lines)
    

    
    def print_papers_list(self) -> None:
        if not self.papers:
            print("No papers added yet")
            return
            
        print("\n=== Papers List (Sorted by ID) ===")
        for paper in sorted(self.papers, key=lambda x: x['id']):
            category_info = f" (Category: {paper['category_path']})" if paper['category_path'] != "Root" else ""
            print(f"{paper['id']:2d}. {paper['title']}{category_info}")
        print()
    
    def print_category_tree(self) -> None:
        print("\n=== Category Hierarchy ===")
        # Rebuild category hierarchy from tree_structure to ensure consistency
        self._rebuild_category_hierarchy()
        self._print_category_recursive("Root", 0)
        print()
    
    def _rebuild_category_hierarchy(self):
        """Rebuild category hierarchy from tree_structure to ensure consistency"""
        self.category_hierarchy = {}
        
        # Add Root category
        self.category_hierarchy["Root"] = []
        
        # First, collect all main categories (those without colons)
        main_categories = []
        for category_path in self.tree_structure.keys():
            if category_path == "Root":
                continue
            if ':' not in category_path:
                main_categories.append(category_path)
                self.category_hierarchy["Root"].append(category_path)
                self.category_hierarchy[category_path] = []
        
        # Then, process all subcategories
        for category_path in self.tree_structure.keys():
            if category_path == "Root" or ':' not in category_path:
                continue
                
            # This is a subcategory
            parent_cat = category_path.split(':')[0]
            if parent_cat in self.category_hierarchy:
                if category_path not in self.category_hierarchy[parent_cat]:
                    self.category_hierarchy[parent_cat].append(category_path)
    
    def _print_category_recursive(self, category: str, level: int):
        indent = "  " * level
        print(f"{indent}├─ {category}")
        
        if category in self.category_hierarchy:
            for subcat in self.category_hierarchy[category]:
                self._print_category_recursive(subcat, level + 1)
    
    def save_state(self, filename: str = "enhanced_paper_tree_state.json") -> None:
        state = {
            'tree_structure': self.tree_structure,
            'papers': self.papers,
            'node_counter': self.node_counter,
            'parent_nodes': self.parent_nodes,
            'category_hierarchy': self.category_hierarchy
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
        print(f"State saved to: {filename}")
    
    def load_state(self, filename: str = "enhanced_paper_tree_state.json") -> None:
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                state = json.load(f)
            self.tree_structure = state['tree_structure']
            self.papers = state['papers']
            self.node_counter = state['node_counter']
            self.parent_nodes = state['parent_nodes']
            # Don't load the potentially corrupted category_hierarchy
            # Instead, rebuild it from tree_structure
            self.category_hierarchy = {}
            print(f"State loaded from {filename}")
            print("Category hierarchy rebuilt from tree structure")
        else:
            print(f"File {filename} does not exist")

    def rename_category(self, old_name: str, new_name: str) -> bool:
        """Rename a category or subcategory with proper cascading updates"""
        if old_name == "Root":
            print("Cannot rename Root category")
            return False
            
        if old_name not in self.tree_structure:
            print(f"Category '{old_name}' not found")
            return False
            
        if new_name in self.tree_structure:
            print(f"Category '{new_name}' already exists")
            return False
            
        # Step 1: Collect all categories that need to be renamed (including nested ones)
        categories_to_rename = []
        categories_to_rename.append(old_name)
        
        # Find all subcategories that start with old_name + ":"
        for cat_name in list(self.tree_structure.keys()):
            if cat_name != old_name and cat_name.startswith(old_name + ":"):
                categories_to_rename.append(cat_name)
        
        # Sort by length (longest first) to ensure we rename from deepest to shallowest
        categories_to_rename.sort(key=len, reverse=True)
        
        # Step 2: Create mapping of old names to new names
        name_mapping = {}
        for old_cat in categories_to_rename:
            if old_cat == old_name:
                # Main category rename
                name_mapping[old_cat] = new_name
            else:
                # Subcategory rename - replace the old main category part
                new_subcat_name = old_cat.replace(old_name + ":", new_name + ":", 1)
                name_mapping[old_cat] = new_subcat_name
        
        # Step 3: Rename all categories in the tree_structure
        for old_cat, new_cat in name_mapping.items():
            if old_cat in self.tree_structure:
                papers = self.tree_structure[old_cat]
                del self.tree_structure[old_cat]
                self.tree_structure[new_cat] = papers
        
        # Step 4: Update all papers' category_path
        for paper in self.papers:
            old_path = paper['category_path']
            if old_path in name_mapping:
                paper['category_path'] = name_mapping[old_path]
        
        # Step 5: Update parent_nodes
        new_parent_nodes = {}
        for paper_id, category_path in self.parent_nodes.items():
            if category_path in name_mapping:
                new_parent_nodes[paper_id] = name_mapping[category_path]
            else:
                new_parent_nodes[paper_id] = category_path
        self.parent_nodes = new_parent_nodes
        
        # Step 6: Rebuild category_hierarchy completely from tree_structure
        self._rebuild_category_hierarchy()
        
        print(f"Renamed category '{old_name}' to '{new_name}'")
        if len(categories_to_rename) > 1:
            print(f"  Also renamed {len(categories_to_rename) - 1} subcategories")
        return True

    def merge_categories(self, source_categories: List[str], target_category: str) -> bool:
        """Merge multiple source categories into a single target category"""
        if not source_categories:
            print("No source categories specified for merging")
            return False
            
        if len(source_categories) < 2:
            print("Need at least 2 source categories to merge")
            return False
            
        if target_category in source_categories:
            print("Target category cannot be one of the source categories")
            return False
            
        # Check if all source categories exist
        for cat in source_categories:
            if cat not in self.tree_structure:
                print(f"Source category '{cat}' not found")
                return False
        
        # Check if target category already exists
        if target_category in self.tree_structure:
            print(f"Target category '{target_category}' already exists")
            return False
        
        # Check if target category name conflicts with existing subcategories
        for existing_cat in self.tree_structure.keys():
            if existing_cat.startswith(target_category + ":") or target_category.startswith(existing_cat + ":"):
                print(f"Target category '{target_category}' conflicts with existing category structure")
                return False
        
        print(f"\n=== Merging Categories ===")
        print(f"Source categories: {', '.join(source_categories)}")
        print(f"Target category: {target_category}")
        
        # Step 1: Create target category
        self.tree_structure[target_category] = []
        
        # Step 2: Collect all papers from source categories
        all_papers = []
        for source_cat in source_categories:
            papers = self.tree_structure[source_cat].copy()
            all_papers.extend(papers)
            print(f"  Moving {len(papers)} papers from '{source_cat}'")
        
        # Step 3: Move all papers to target category
        self.tree_structure[target_category] = all_papers
        
        # Step 4: Update all papers' category_path
        papers_moved = 0
        for paper in self.papers:
            if paper['category_path'] in source_categories:
                paper['category_path'] = target_category
                papers_moved += 1
        
        # Step 5: Update parent_nodes
        for paper_id, category_path in self.parent_nodes.items():
            if category_path in source_categories:
                self.parent_nodes[paper_id] = target_category
        
        # Step 6: Handle subcategories (including nested ones)
        subcategories_to_move = []
        for source_cat in source_categories:
            # Find all subcategories that start with source_cat + ":"
            for cat_name in list(self.tree_structure.keys()):
                if cat_name != source_cat and cat_name.startswith(source_cat + ":"):
                    subcategories_to_move.append(cat_name)
        
        if subcategories_to_move:
            print(f"  Moving {len(subcategories_to_move)} subcategories")
            # Sort by length (longest first) to ensure we process from deepest to shallowest
            subcategories_to_move.sort(key=len, reverse=True)
            
            for subcat in subcategories_to_move:
                # Find which source category this subcategory belongs to
                source_parent = None
                for source_cat in source_categories:
                    if subcat.startswith(source_cat + ":"):
                        source_parent = source_cat
                        break
                
                if source_parent:
                    # Create new subcategory name under target category
                    new_subcat_name = subcat.replace(source_parent + ":", target_category + ":", 1)
                    
                    # Move papers
                    papers = self.tree_structure[subcat].copy()
                    self.tree_structure[new_subcat_name] = papers
                    del self.tree_structure[subcat]
                    
                    # Update paper category paths
                    for paper in self.papers:
                        if paper['category_path'] == subcat:
                            paper['category_path'] = new_subcat_name
                    
                    # Update parent_nodes
                    for paper_id, category_path in self.parent_nodes.items():
                        if category_path == subcat:
                            self.parent_nodes[paper_id] = new_subcat_name
                    
                    print(f"    Moved subcategory '{subcat}' to '{new_subcat_name}'")
        
        # Step 7: Delete source categories
        for source_cat in source_categories:
            del self.tree_structure[source_cat]
            print(f"  Deleted source category '{source_cat}'")
        
        # Step 8: Rebuild category hierarchy
        self._rebuild_category_hierarchy()
        
        print(f"\n✅ Successfully merged {len(source_categories)} categories into '{target_category}'")
        print(f"  Total papers moved: {papers_moved}")
        print(f"  Total subcategories moved: {len(subcategories_to_move)}")
        
        return True

def main():
    classifier = EnhancedPaperTreeClassifier()
    
    print("=== Enhanced Paper Tree Classifier with Subcategories ===")
    print("Type 'help' for help, 'quit' to exit")
    print("Type 'save' to save state, 'load' to load state")
    print("Type 'show' to display tree, 'list' to show papers list")
    print("Type 'categories' to show category hierarchy")
    print("Type 'delete paper ID' to delete paper, 'delete category NAME' to delete category")
    print("Type 'rename OLD_NAME NEW_NAME' to rename category or subcategory")
    print("Type 'merge CAT1,CAT2,... INTO TARGET' to merge multiple categories")
    print()
    
    while True:
        try:
            user_input = input("Enter paper title (or command): ").strip()
            
            if user_input.lower() == 'quit':
                break
            elif user_input.lower() == 'help':
                print("\n=== Help Information ===")
                print("1. Direct input paper title: will add to Root category")
                print("2. Input 'category:paper title': specify main category")
                print("3. Input 'main:sub:paper title': specify subcategory")
                print("4. Input 'show': display tree structure")
                print("5. Input 'list': show papers list")
                print("6. Input 'categories': show category hierarchy")
                print("7. Input 'delete paper ID': delete paper by ID")
                print("8. Input 'delete category NAME': delete category and all its papers")
                print("9. Input 'rename OLD_NAME NEW_NAME': rename category or subcategory")
                print("10. Input 'merge CAT1,CAT2,... INTO TARGET': merge multiple categories")
                print("11. Input 'save': save current state")
                print("12. Input 'load': load previous state")
                print("13. Input 'quit': exit program")
                print()
            elif user_input.lower() == 'show':
                classifier.visualize_tree()
            elif user_input.lower() == 'list':
                classifier.print_papers_list()
            elif user_input.lower() == 'categories':
                classifier.print_category_tree()
            elif user_input.lower().startswith('delete paper '):
                try:
                    paper_id = int(user_input.split('delete paper ')[1])
                    classifier.delete_paper_by_id(paper_id)
                except (ValueError, IndexError):
                    print("Invalid format. Use 'delete paper ID' (e.g., 'delete paper 1')")
            elif user_input.lower().startswith('delete category '):
                try:
                    category_name = user_input.split('delete category ')[1]
                    classifier.delete_category(category_name)
                except IndexError:
                    print("Invalid format. Use 'delete category NAME' (e.g., 'delete category Machine Learning')")
            elif user_input.lower() == 'save':
                classifier.save_state()
            elif user_input.lower() == 'load':
                classifier.load_state()
            elif user_input.lower().startswith('rename '):
                try:
                    parts = user_input.split('rename ')
                    if len(parts) == 2:
                        old_name, new_name = parts[1].strip().split(' ', 1)
                        if old_name and new_name:
                            classifier.rename_category(old_name, new_name)
                        else:
                            print("Invalid format for rename command. Use 'rename OLD_NAME NEW_NAME'")
                    else:
                        print("Invalid format for rename command. Use 'rename OLD_NAME NEW_NAME'")
                except ValueError:
                    print("Invalid format for rename command. Use 'rename OLD_NAME NEW_NAME'")
            elif user_input.lower().startswith('merge '):
                try:
                    # Parse merge command: merge CAT1,CAT2,... INTO TARGET
                    merge_part = user_input[6:].strip()  # Remove 'merge ' prefix
                    if ' INTO ' not in merge_part:
                        print("Invalid format for merge command. Use 'merge CAT1,CAT2,... INTO TARGET'")
                        continue
                    
                    categories_part, target_part = merge_part.split(' INTO ', 1)
                    source_categories = [cat.strip() for cat in categories_part.split(',')]
                    target_category = target_part.strip()
                    
                    if not target_category:
                        print("Target category cannot be empty")
                        continue
                    
                    # Remove empty category names
                    source_categories = [cat for cat in source_categories if cat]
                    
                    if len(source_categories) < 2:
                        print("Need at least 2 source categories to merge")
                        continue
                    
                    classifier.merge_categories(source_categories, target_category)
                    
                except Exception as e:
                    print(f"Error in merge command: {e}")
                    print("Use format: merge CAT1,CAT2,... INTO TARGET")
            elif ':' in user_input:
                parts = user_input.split(':')
                if len(parts) >= 2:
                    if len(parts) == 2:
                        category_name, paper_title = parts[0].strip(), parts[1].strip()
                        if paper_title:
                            classifier.add_category(category_name)
                            node_id = classifier.add_paper(paper_title, category_name)
                            print(f"Added paper '{paper_title}' to category '{category_name}', ID: {node_id}")
                        else:
                            print("Paper title cannot be empty")
                    elif len(parts) == 3:
                        main_cat, sub_cat, paper_title = parts[0].strip(), parts[1].strip(), parts[2].strip()
                        if paper_title:
                            classifier.add_category(main_cat)
                            classifier.add_category(f"{main_cat}:{sub_cat}", main_cat)
                            node_id = classifier.add_paper(paper_title, f"{main_cat}:{sub_cat}")
                            print(f"Added paper '{paper_title}' to subcategory '{main_cat}:{sub_cat}', ID: {node_id}")
                        else:
                            print("Paper title cannot be empty")
                    else:
                        print("Too many category levels. Use format 'main:sub:paper title'")
                else:
                    print("Format error, please use 'category:paper title' or 'main:sub:paper title'")
            elif user_input:
                node_id = classifier.add_paper(user_input)
                print(f"Added paper '{user_input}' to Root category, ID: {node_id}")
            else:
                print("Input cannot be empty")
                
        except KeyboardInterrupt:
            print("\nProgram interrupted")
            break
        except Exception as e:
            print(f"Error occurred: {e}")
    
    print("Program ended")

if __name__ == "__main__":
    main()
