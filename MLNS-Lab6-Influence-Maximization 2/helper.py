#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Network Science Analytics
Lab 5: Propagation on Graphs and Influence Maximization
March 20, 2020
"""
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

def stochastic_block_model(sizes, matrix_p):
    
    p = np.asarray(matrix_p)
    # Check if the matrix is symmetric
    if not np.allclose(p, p.T, atol=1e-8):
        raise ValueError("Graph must be undirected!")
    
    cum_sizes = np.cumsum(sizes)

    g = nx.Graph()
    N = np.sum(sizes)
    comm_label = 0
    
    node2comm = {}
    for node in range(N):
        g.add_node(str(node))

        if node < cum_sizes[comm_label]:
            node2comm[str(node)] = comm_label
        else:
            comm_label += 1
            node2comm[str(node)] = comm_label

    for v in range(N):
        for u in range(v+1, N):
            if np.random.rand() < matrix_p[node2comm[str(v)]][node2comm[str(u)]]:
                g.add_edge(str(v), str(u))

    nx.set_node_attributes(G=g, name="community", values=node2comm)

    return g


def visualize_status(graph, iterations, t=-1, node_size=100, colors={0:'b', 1:'r', 2:'g'}):
    '''
    :param graph:
    :list of dictionaries
    :param t:time step
    :param node_list: dictionary keyed by node
    :return:
    '''
    
    values = iterations[t]['status']
    
    pos = nx.spring_layout(graph)
    plt.figure()
    nx.draw_networkx_edges(graph, pos, alpha=0.2)
    nc = nx.draw_networkx_nodes(graph, pos, nodelist=graph.nodes(), node_color='k', node_size=node_size, alpha=0.5)
    for status in colors.keys():
        node_status_list = [node for node in values.keys() if values[node] == status]
        if len(node_status_list) > 0:
            nc = nx.draw_networkx_nodes(graph, pos, nodelist=node_status_list, node_color=colors[status], node_size=node_size)
    plt.axis('off')
    plt.show()
