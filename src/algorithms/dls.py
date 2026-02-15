"""
Implementation of Depth-Limited Search (DLS).
Iterative approach.
"""


def run_dls(grid_matrix, start_node, target_node, total_rows, total_cols, limit=50):
    nodes_to_visit_stack = [(start_node, 0)]
    parent_tracker = {}
    visited_at_depth = {start_node: 0}

    while nodes_to_visit_stack:
        current_active_node, current_depth = nodes_to_visit_stack.pop()

        if current_active_node == target_node:
            # Draw the path visually BEFORE returning the data
            yield from reconstruct_final_path(parent_tracker, target_node, start_node)
            return parent_tracker

        if current_depth >= limit:
            continue

        if current_active_node != start_node:
            current_active_node.mark_as_explored()

        current_active_node.identify_neighbors(grid_matrix, total_rows, total_cols)

        for neighbor in current_active_node.neighbor_nodes:
            new_depth = current_depth + 1
            if (
                neighbor not in visited_at_depth
                or new_depth < visited_at_depth[neighbor]
            ):
                visited_at_depth[neighbor] = new_depth
                parent_tracker[neighbor] = current_active_node
                neighbor.mark_as_frontier()
                nodes_to_visit_stack.append((neighbor, new_depth))
        yield True
    return None


def reconstruct_final_path(parent_tracker, current_step, start_node):
    while current_step in parent_tracker:
        current_step = parent_tracker[current_step]
        if current_step != start_node:
            current_step.mark_as_path_segment()
        yield True
