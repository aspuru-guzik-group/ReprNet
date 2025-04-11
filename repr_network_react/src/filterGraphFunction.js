export default function filterGraph(node, link, nodes, links, clickedNode) {
  // TODO: depending on the specific use case, write a new filterGraph function.
  // nodes and links are from data.json. node and link are the elements that render the graph.
  // By filtering out, we change the opacity of the hidden nodes and links to 0.05.

  const connectedLinks = links.filter(
    (link) =>
      (link.source.id === clickedNode.id || link.target.id === clickedNode.id)
  );

  const connectedNodes = connectedLinks.reduce((acc, link) => {
    if (!acc.includes(link.source)) acc.push(link.source);
    if (!acc.includes(link.target)) acc.push(link.target);
    return acc;
  }, [clickedNode]);

  // Update visibility flag for each node
  nodes.forEach(node => {
    node.visible = connectedNodes.includes(node);
  });

  // Update the graph dynamically without re-rendering
  link.style('opacity', (d) =>
    connectedLinks.includes(d) ? 1 : 0.05
  );

  node.style('opacity', (d) =>
    connectedNodes.includes(d) ? 1 : 0.05
  );
}