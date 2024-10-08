import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path
from typing import List

"""
Visualises graphs through multiple input methods
"""


class GraphVisualiser:
    def save_graph_from_adjacency_list(
        adj_list: dict, filename: str = "graph_demo"
    ) -> Path:
        """
        Generate and save a graph image from an adjacency list.

        Arguments:
            adj_list (dict): Adjacency list representing the graph.

        Returns:
            Path directory for image
        """
        G = nx.DiGraph(adj_list)
        nx.draw(G, with_labels=True, arrows=True)
        file_path = Path.cwd() / "assets" / f"{filename}.png"
        plt.savefig(file_path, format="PNG")
        plt.close()
        return file_path

    def save_graph_from_adjacency_matrix(
        adj_matrix: List[List[int]], filename: str = "graph_demo"
    ) -> Path:
        """
        Generate and save a graph image from an adjacency matrix.

        Arguments:
            adj_matrix (2D list): Adjacency matrix representing the graph.

        Returns:
            Path directory for image
        """
        G = nx.Graph()
        num_nodes = len(adj_matrix)
        for i in range(num_nodes):
            for j in range(num_nodes):
                if adj_matrix[i][j] != 0:
                    G.add_edge(i, j, weight=adj_matrix[i][j])
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True)
        edge_labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        # Save image
        file_path = Path.cwd() / "assets" / f"{filename}.png"
        plt.savefig(file_path, format="PNG")
        plt.close()
        return file_path
