#!/usr/bin/env python3
import json
import math
import sys

pagerank = dict()
embed_data = open(sys.argv[2].strip())
embeddings = json.load(embed_data)

with open(sys.argv[1].strip()) as v:
    lines = v.read().strip().split("\n")
    for line in lines:
        try:
            page, rank = line.split(",")
        except:
            continue
        pagerank[float(page.strip())] = float(rank.strip())

for line in sys.stdin:
    line = line.strip()
    try:
        src_node, dest_nodes = line.split("\t")
        src_node = int(src_node.strip())
        dest_nodes = eval(dest_nodes.strip())
    except:
        continue

    outgoing_edges = len(dest_nodes)
    src_node_pagerank = pagerank[src_node]
    src_node_contribution = src_node_pagerank * (1 / outgoing_edges)

    print(f"{src_node},0")

    for node in dest_nodes:
        if node in pagerank.keys():
            p = embeddings[str(src_node)]
            q = embeddings[str(node)]
            mag_p = math.sqrt(sum(i ** 2 for i in p))
            mag_q = math.sqrt(sum(i ** 2 for i in q))
            sim = sum(x * y for x, y in zip(p, q)) / (mag_p * mag_q)
            print(f"{node},{src_node_contribution * sim}")
        else:
            print(f"{node},0.14")
