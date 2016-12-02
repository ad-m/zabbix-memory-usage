import argparse

from pyzabbix import ZabbixAPI

COLOR_LIST = ['4D4D4D', '5DA5DA', 'FAA43A', '60BD68',
              'F17CB0', 'B2912F', 'B276B2', 'DECF3F', 'F15854']

GRAPH_TYPE = {'normal': 0,
              'stacked': 1,
              'pie': 2,
              'exploded': 3}


def get_color(i):
    return COLOR_LIST[i % len(COLOR_LIST)]


def query(args):
    zapi = ZabbixAPI(args.host)
    zapi.login(args.login, args.password)
    if not zapi.host.get(hostids=[args.hostid]):
        print ("Provided host ID is invalid")
    items = zapi.item.get(hostids=[args.hostid],
                          selectItemDiscovery='extend')
    discovered_items = [x for x in items
                        if x['itemDiscovery'] and
                        x['itemDiscovery'].get('parent_itemid') == str(args.itemprototypeid)]
    if not discovered_items:
        print("Unable found items for hostid = {0} ".format(args.hostid) +
              "and parent_itemid = {0}".format(args.itemprototypeid))
        discovery_ids = [x['itemDiscovery']['parent_itemid'] for x in items if x['itemDiscovery']]
        discovered_items = zapi.itemprototype.get(itemids=list(discovery_ids))
        print ("Found only following discovery ID:")
        for ditem in discovered_items:
            print("{id} - {name}".format(id=ditem['itemid'], name=ditem['name']))
        return

    gitems = [{"itemid": item['itemid'], "color": get_color(i)}
              for i, item in enumerate(discovered_items)]

    graph = zapi.graph.get(hostids=[args.hostid], search={'name': args.name})
    if graph:
        print("Going to update graph ID {0}".format(graph[0]['graphid']))
        res = zapi.graph.update(graphid=graph[0]['graphid'],
                                width=args.width,
                                height=args.width,
                                gitems=gitems,
                                graphtype=GRAPH_TYPE[args.graphtype])
        print("Graph update success" if res else "Something fail")
        return
    print("Going to create graph")
    res = zapi.graph.create(name=args.name,
                            width=args.width,
                            height=args.height,
                            gitems=gitems)
    print("Graph create success" if res else "Something fail")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Add grouped graph for LDD items")
    parser.add_argument('host',
                        help='URI of zabbix server eg. http://tacjana.jawne.info.pl/zabbix/')
    parser.add_argument('login', help='username of zabbix server user')
    parser.add_argument('password', help='password for zabbix server user')
    parser.add_argument('--name', help='Name of added graph', default="Memory usage graph")
    parser.add_argument('itemprototypeid', type=int,
                        help="ID of the item prototype from which the items has been created")
    parser.add_argument('hostid', type=int,
                        help="ID of the host for which items the graph has been created")
    parser.add_argument('--height', type=int, default=200,
                        help="--Height of the graph in pixels.")
    parser.add_argument('--width', type=int, default=900,
                        help="--Width of the graph in pixels.")
    parser.add_argument('--graphtype', choices=GRAPH_TYPE.keys(), default='normal',
                        help="Graph's layout type (default: normal)")
    query(parser.parse_args())
