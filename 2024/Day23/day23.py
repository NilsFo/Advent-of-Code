import time

import networkx as nx
from pyvis.network import Network
from tqdm import tqdm


class Host:

    def __init__(self, id: str):
        super().__init__()
        self.id = id

        self.connections = []

    def add_connection(self, other_connection: str):
        pass


def lan_party_network(host_dict) -> Network:
    all_host_names = list(host_dict.keys())
    all_host_names.sort()

    net = Network(notebook=True)
    for i, host_name in enumerate(all_host_names):
        net.add_node(i, label=host_name, color='blue')

    for i, host_name in enumerate(all_host_names):
        for target_hosts in host_dict[host_name]:
            net.add_edge(i, all_host_names.index(target_hosts))

    return net


def normalize(value, min_value, max_value):
    return (value - min_value) / (max_value - min_value) if max_value > min_value else 0


def cluster_lan_party(host_dict, all_host_names) -> [str]:
    net = lan_party_network(host_dict)
    g = nx.Graph()

    for node in net.nodes:
        g.add_node(node['id'])
    for edge in net.edges:
        g.add_edge(edge['from'], edge['to'])

    clustering_coefficients = nx.clustering(g)
    clustering_coefficients_values = list(clustering_coefficients.values())
    best_coefficient = max(clustering_coefficients_values)

    best_hosts = []
    for i in range(len(all_host_names)):
        current_host = all_host_names[i]
        current_clustering_coefficient = clustering_coefficients[i]

        if current_clustering_coefficient == best_coefficient:
            best_hosts.append(current_host)

    return best_hosts


def main():
    f = open('input.txt')
    input = f.readlines()
    f.close()

    host_dict = {}
    for line in input:
        line = line.strip()
        left, right = line.split('-')

        # the historian's host starts with a 't'.
        # cannot allow that! no need to search for 't' hosts!
        if left not in host_dict:
            host_dict[left] = []
        if right not in host_dict:
            host_dict[right] = []

        host_dict[left].append(right)
        host_dict[right].append(left)

    # sorting all known host names
    all_host_names = list(host_dict.keys())
    all_host_names.sort()

    # sorting child hosts
    for host in host_dict.keys():
        host_dict[host].sort()

    #############################################################################

    print(f'Number of hosts: {len(all_host_names)}')
    print('Rendering...')
    net: Network = lan_party_network(host_dict)
    net.save_graph('input.html')
    print('Done!')

    ############################################################################
    time.sleep(0.5) # for the console to catch up

    all_loops = []
    for i in tqdm(range(len(all_host_names))):
        current_host = all_host_names[i]

        if current_host.startswith('t'):
            loops = hop_host(
                initial_host=current_host,
                hops_remaining=3,
                host_dict=host_dict,
                hosts_history=[],
                current_host=current_host,
            )

            for loop in loops:
                all_loops.append(loop)

                # updating the render
                for host in loop:
                    host_index = all_host_names.index(host)
                    net.get_node(host_index)['color'] = 'green'
    net.save_graph('part_1.html')

    ############################################################################
    time.sleep(0.5) # for the console to catch up

    print(f'Number of Loops: {len(all_loops)}')
    print('Removing duplicates.')
    unique_loops = []
    for i in tqdm(range(len(all_loops))):
        is_duplicate = False
        for j in range(len(unique_loops)):
            if compare_loops(loop_a=all_loops[i], loop_b=unique_loops[j]):
                is_duplicate = True
                break
        if not is_duplicate:
            unique_loops.append(all_loops[i])

    ############################################################################
    time.sleep(0.5) # for the console to catch up

    print('Done!')
    # for i, loop in enumerate(unique_loops):
    #     print(f'Loop #{i + 1}: {print_hosts(loop)}')
    print(f'Number of unique Loops (where the historian could be): {len(unique_loops)}')

    ############################################################################
    # PART 2
    ############################################################################

    best_cluster = cluster_lan_party(host_dict, all_host_names)
    best_cluster.sort()
    best_cluster_formated = ','.join(best_cluster)
    print(f'Best cluster of hosts: {best_cluster_formated}')


def compare_loops(loop_a: [str, str, str], loop_b: [str, str, str]) -> bool:
    loop_a = loop_a.copy()
    loop_b = loop_b.copy()

    loop_a.sort()
    loop_b.sort()

    return loop_a[0] == loop_b[0] and loop_a[1] == loop_b[1] and loop_a[2] == loop_b[2]


def hop_host(initial_host: str,
             hops_remaining: int,
             host_dict: dict,
             hosts_history: [str],
             current_host: str) -> [str]:
    # adding myself to the history
    hosts_history = hosts_history.copy()
    hosts_history.append(current_host)
    hops_remaining -= 1

    #
    loop_hosts = []

    # checking all connected hosts
    other_hosts = host_dict[current_host]

    for other_host in other_hosts:
        if hops_remaining == 0:
            # check if we made a round trip
            if other_host == initial_host:
                loop_hosts.append(hosts_history)
            # else:
            #    return []
        else:
            # not retracing our path
            if other_host not in hosts_history:
                loop_history = hop_host(
                    initial_host=initial_host,
                    hops_remaining=hops_remaining,
                    host_dict=host_dict,
                    hosts_history=hosts_history,
                    current_host=other_host
                )
                if len(loop_history) > 0:
                    for l in loop_history:
                        loop_hosts.append(l)

    # done?
    return loop_hosts


def print_hosts(hosts: [str]):
    return ','.join(hosts)


if __name__ == '__main__':
    main()
