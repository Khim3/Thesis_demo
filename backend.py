import yaml, re,json
import streamlit as st

with open("./main.css",encoding="utf-8") as f:
    style_file_content = f.read()


def render_dot_to_streamlit(dot_code):
    # Render the DOT code using D3.js and Graphviz in Streamlit
    escaped_dot_code = json.dumps(dot_code)

    html_code = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Graphviz with D3.js (Styled)</title>
        <script src="//d3js.org/d3.v7.min.js"></script>
        <script src="https://unpkg.com/@hpcc-js/wasm@2.20.0/dist/graphviz.umd.js"></script>
        <script src="https://unpkg.com/d3-graphviz@5.6.0/build/d3-graphviz.js"></script>
        <style>
        {style_file_content}
        </style>
    </head>
    <body>


    <div id="graph-container">
        <div id="graph"></div>
    </div>

    <script>
        const scale = 1;

        function attributer(datum, index, nodes) {{
            var selection = d3.select(this);
            if (datum.tag === "svg") {{
                datum.attributes = {{
                    ...datum.attributes,
                    width: '1200',
                    height: '800',
                }};

                const px2pt = 3 / 4;
                const graphWidth = datum.attributes.viewBox.split(' ')[2] / px2pt;
                const graphHeight = datum.attributes.viewBox.split(' ')[3] / px2pt;

                const w = graphWidth / scale;
                const h = graphHeight / scale;
                const x = -(w - graphWidth) / 2;
                const y = -(h - graphHeight) / 2;

                const viewBox = `${{x * px2pt}} ${{y * px2pt}} ${{w * px2pt}} ${{h * px2pt}}`;
                selection.attr('viewBox', viewBox);
                datum.attributes.viewBox = viewBox;
            }}
        }}

        const dot = {escaped_dot_code};

        d3.select("#graph").graphviz()
            .fit(true)
            .attributer(attributer)
            .renderDot(dot);
    </script>

    </body>
    </html>
    """
    return st.components.v1.html(html_code, height=800, scrolling=True)

def clean_dot_code(dot_code: str) -> str:
    # Use regex to remove escaped quotes (e.g., \"Label\" → Label)
    cleaned_dot = re.sub(r'\\"(.*?)\\"', r'\1', dot_code)
    return cleaned_dot
       

        
def extract_clusters_and_relations(dot_code: str) -> str:
    # Extract all subgraphs
    subgraphs = re.findall(r'(subgraph cluster_\d+ \{.*?\})', dot_code, re.DOTALL)

    cleaned_subgraphs = []
    for sg in subgraphs:
        # Extract cluster number
        cluster_match = re.search(r'subgraph\s+(cluster_\d+)', sg)
        cluster_id = cluster_match.group(1) if cluster_match else "cluster_unknown"

        # Extract label
        label_match = re.search(r'label\s*=\s*"([^"]+)"', sg)
        label = label_match.group(1) if label_match else "Unnamed"

        # Extract actor nodes
        actor_nodes = re.findall(r'(actor_\d+_\d+)\s*\[label="[^"]+"\];', sg)
        actor_lines = [re.search(rf'({actor_id}\s*\[label="[^"]+"\];)', sg).group(1) for actor_id in actor_nodes]

        # Compose cleaned subgraph
        subgraph_clean = f'  subgraph {cluster_id} {{ label="{label}";\n    ' + "\n    ".join(actor_lines) + '\n  }'
        cleaned_subgraphs.append(subgraph_clean)

    # Extract all inter-cluster relations
    relations = re.findall(r'(actor_\d+_\d+ -> actor_\d+_\d+ \[label="[^"]+", ltail=cluster_\d+, lhead=cluster_\d+\];)', dot_code)

    # Combine all into final DOT
    output = "digraph G {\n  compound=true;\n  rankdir=TB;\n\n"
    output += "\n\n".join(cleaned_subgraphs)
    output += "\n\n  " + "\n  ".join(relations)
    output += "\n}"
    return output

def convert_clusters_to_nodes(dot_code):
    # Extract all clusters with their number and label
    cluster_headers = re.findall(
        r'subgraph\s+cluster_(\d+)\s*\{[^{}]*?label\s*=\s*"([^"]+)"', dot_code
    )

    # Extract all actors and map them to their cluster
    actor_cluster_map = {}
    for num, label in cluster_headers:
        cluster_block = re.search(
            rf'subgraph\s+cluster_{num}\s*\{{(.*?)\}}', dot_code, re.DOTALL
        )
        if cluster_block:
            actors = re.findall(r'(actor_' + re.escape(num) + r'_\d+)', cluster_block.group(1))
            for actor in actors:
                actor_cluster_map[actor] = f'node_{num}'

    # Create node label map
    cluster_labels = {
        f'node_{num}': label for num, label in cluster_headers
    }

    # Extract inter-cluster actor-to-actor edges
    edges = re.findall(
        r'(actor_\d+_\d+)\s*->\s*(actor_\d+_\d+)\s*\[label="([^"]+)"', 
        dot_code
    )

    # Begin new dot code
    new_dot = ['digraph G {', '    rankdir=LR;']

    # Add new nodes with labels
    for node_id, label in cluster_labels.items():
        new_dot.append(f'    {node_id} [label="{label}"];')

    # Add edges (converted from actors to nodes)
    for src, dst, label in edges:
        src_node = actor_cluster_map.get(src)
        dst_node = actor_cluster_map.get(dst)
        if src_node and dst_node:
            new_dot.append(f'    {src_node} -> {dst_node} [label="{label}"];')

    new_dot.append('}')
    return '\n'.join(new_dot)

def clean_dot_code(dot_code: str) -> str:
    # Clean DOT code by removing escaped double quotes.
    # Use regex to remove escaped quotes (e.g., \"Label\" → Label)
    cleaned_dot = re.sub(r'\\"(.*?)\\"', r'\1', dot_code)
    return cleaned_dot

def beatify_dot_code(dot_code):
    # Add custom styles to the DOT code
    insert_styles = """
    bgcolor="#EDEDED"; 
    node [
        style=filled,
        fillcolor="#FFF3E0",
        color="#FFB74D",  
        fontname="Helvetica",
    ];

    edge [
        fontname="Helvetica",
        color="#1976D2",   
        penwidth=2,
        arrowsize=1.2,
    ];
    """
    style_block = """
        style=filled;
        fillcolor="#E3F2FD";
        color="#90CAF9"; 
        fontname="Helvetica-Bold";
        penwidth=2;
    """
    dot_code = re.sub(r'(rankdir\s*=\s*\w+;)', r'\1' + insert_styles, dot_code)
    dot_code = re.sub(
        r'(subgraph\s+cluster_\d+\s*{)',
        lambda m: f'{m.group(1)}{style_block}',
        dot_code
    )
    return dot_code