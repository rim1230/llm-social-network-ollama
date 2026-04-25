import argparse
import json
import networkx as nx
import matplotlib.pyplot as plt
import os
from constants_and_utils import *

def draw_network_with_politics(G, personas, save_name, seed=0):
    """
    Draw network with node colors based on political affiliation and labels showing ID and affiliation.
    """
    # Prepare node colors and labels
    node_colors = []
    labels = {}
    for node in G.nodes():
        affiliation = personas[str(node)]['political affiliation']
        if affiliation == 'Democrat':
            node_colors.append('blue')
        elif affiliation == 'Republican':
            node_colors.append('red')
        else:
            node_colors.append('gray')  # Other affiliations
        labels[node] = f"{node}: {affiliation}"

    # Draw the network
    pos = nx.spring_layout(G, seed=seed, k=2*1/np.sqrt(len(G.nodes())))
    nx.draw_networkx(G, pos=pos, with_labels=True, labels=labels, node_color=node_colors, node_size=500, font_size=10, font_weight='bold')
    plt.axis("off")
    axis = plt.gca()
    axis.set_xlim([1.1*x for x in axis.get_xlim()])
    axis.set_ylim([1.1*y for y in axis.get_ylim()])
    plt.tight_layout()

    # Save the plot
    fig_path = os.path.join('./plots', f'{save_name}_politics.png')
    os.makedirs(os.path.dirname(fig_path), exist_ok=True)
    plt.savefig(fig_path)
    plt.close()
    print(f'Saved network plot with politics in {fig_path}')

def main():
    parser = argparse.ArgumentParser(description='Analyze networks with political affiliation visualization.')
    parser.add_argument('--persona_fn', type=str, default='us_50_gpt4o_w_interests.json', help='Persona file name')
    parser.add_argument('--network_fn', type=str, help='Network file prefix')
    parser.add_argument('--num_networks', type=int, default=1, help='Number of networks to analyze')
    args = parser.parse_args()

    # Load personas
    fn = os.path.join(PATH_TO_TEXT_FILES, args.persona_fn)
    with open(fn, 'r') as f:
        personas = json.load(f)

    # Load and draw each network
    for i in range(args.num_networks):
        network_file = os.path.join(PATH_TO_TEXT_FILES, f'{args.network_fn}_{i}.adj')
        if os.path.exists(network_file):
            G = nx.read_adjlist(network_file)
            draw_network_with_politics(G, personas, f'{args.network_fn}_{i}')
        else:
            print(f'Network file {network_file} not found.')

if __name__ == '__main__':
    main()