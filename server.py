from flask import Flask, render_template, jsonify

app = Flask(__name__)

def connect_densely(nodes1, nodes2):
    """ returns the dense connections between nodes1 and nodes2, with
    nodes1 pointing towards nodes2 """
    links = []
    for i in range(len(nodes1)):
        for k in range(len(nodes2)):
            links.append(dict(source=nodes1[i]["id"], 
                              target=nodes2[k]["id"],
                              force=.5))
    return links

def gen_layer(size, number):
    nodes = []
    number = str(number)
    for i in range(size):
        nodes.append(dict(id="layer{}_{}".format(number, i), 
                           group="layer{}".format(number),
                           name="layer{}_{}".format(number, i),
                           value=1))
    return nodes

def dense_nn(sizes=[10, 20]):
    nodes = []
    links = []
    prev_nodes = None
    for number, size in enumerate(sizes):
        cur_nodes = gen_layer(size, number + 1)
        if prev_nodes is not None:
            cur_links = connect_densely(prev_nodes, cur_nodes)
            links += cur_links
        prev_nodes = cur_nodes
        nodes += cur_nodes
    return dict(nodes=nodes, links=links)

def two_layers_dense(layer1_N, layer2_N):
    """ returns graph representing two dense layers """
    nodes1 = gen_layer(30, 1)
    nodes2 = gen_layer(5, 2)
    links = connect_densely(nodes1, nodes2)
    nodes = nodes1 + nodes2
    return dict(nodes=nodes, links=links)

def sample_data():
    """ returns some sample data to test graphing """
    nodes = [dict(id="id{}".format(i), name="name{}".format(i), val=i) for i in range(0, 10)]
    links = [dict(source="id{}".format(i), target="id{}".format(i+1)) for i in range(0, 5)]
    return_data = dict(nodes=nodes, links=links)
    return return_data

@app.route("/data")
def data():
    return_data = dense_nn(sizes=[20, 16, 12, 8, 4, 1, 4, 8, 12, 16, 20])
    return jsonify(return_data)

    """
    {
        "nodes": [
            {
                "id": "id1",
                "name": "name1",
                "val": 1
            },
            {
                "id": "id2",
                "name": "name2",
                "val": 10
            }
        ],
        "links": [
            {
                "source": "id1",
                "target": "id2"
            }
        ]
    }
    """

@app.route("/")
def main():
    return render_template("example.html")

app.run(host='127.0.0.1', port=5000, debug=True)
