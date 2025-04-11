import React, { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';
import data from './data.json';
import filterGraph from './filterGraphFunction.js'; // Import the filterGraph function

const ForceDirectedGraph = () => {
  const containerRef = useRef(null);
  const svgRef = useRef(null);
  const [dimensions, setDimensions] = useState({ width: 0, height: 0 });

  // Function to update dimensions
  const updateDimensions = () => {
    if (containerRef.current) {
      const { width, height } = containerRef.current.getBoundingClientRect();
      setDimensions({ width, height });
    }
  };

  // Initial measurement and resize handler
  useEffect(() => {
    updateDimensions();

    const handleResize = () => {
      updateDimensions();
    };

    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  // Graph creation and update
  useEffect(() => {
    if (dimensions.width === 0 || dimensions.height === 0) return;

    const width = dimensions.width;
    const height = dimensions.height;

    // Initial data for nodes
    const nodes = data["nodes"];

    // New links format
    const originalLinks = data["edges"];

    // Define standard sizes for shapes
    const standardSizes = {
      box: { width: 120, height: 60 },
      diamond: { width: 150, height: 70 }
    };

    // Clear any existing SVG content
    d3.select(svgRef.current).selectAll("*").remove();

    // Create an internal representation of links that D3 can use
    const links = originalLinks.map(link => ({
      source: link.from,
      target: link.to,
      color: link.color,
      dashes: link.dashes,
      from: link.from,
      to: link.to
    }));

    // Create the SVG container
    const svg = d3.select(svgRef.current)
      .attr('width', '100%')
      .attr('height', '100%')
      .attr('viewBox', [0, 0, width, height]);

    // Add a background rect to catch click events
    const background = svg.append('rect')
      .attr('width', width)
      .attr('height', height)
      .attr('fill', 'none')
      .attr('pointer-events', 'all');

    // Create a group for the graph that will be transformed during zoom
    const g = svg.append('g');

    // Define zoom behavior
    const zoom = d3.zoom()
      .scaleExtent([0.1, 4]) // Set min/max zoom scale
      .on('zoom', (event) => {
        g.attr('transform', event.transform);
      });

    // Apply zoom behavior to the SVG
    svg.call(zoom);

    // Create links
    const link = g.append('g')
      .attr('class', 'links')
      .selectAll('line')
      .data(links)
      .enter().append('line')
      .attr('stroke-width', 2)
      .attr('stroke', d => d.color.color)
      .style('stroke-dasharray', d => d.dashes ? '5, 5' : '0');

    // Create nodes with shapes and labels
    const node = g.append('g')
      .attr('class', 'nodes')
      .selectAll('g')
      .data(nodes)
      .enter().append('g')
      .attr('class', 'node')
      // Attach data property to track visibility
      .each(function(d) { d.visible = true; })
      .call(d3.drag()
        .on('start', dragstarted)
        .on('drag', dragged)
        .on('end', dragended))
      .on('click', (event, d) => {
        // Check if the node is visible (not faded out)
        if (d.visible) {
          event.stopPropagation(); // Only prevent propagation if visible
          filterGraph(node, link, nodes, links, d);
        } else {
          // If node is hidden, trigger the background click behavior
          resetGraphVisibility();
        }
      });

    // Append shapes and labels with better text fitting
    node.each(function (d) {
      const group = d3.select(this);

      if (d.shape === 'circle') {
        // For circles, use a fixed radius
        const radius = 40;

        // Add circle first
        group.append('circle')
          .attr('r', radius)
          .attr('fill', d.color)
          .lower();

        // Add a hidden text element to test text size
        const testText = group.append('text')
          .text(d.label)
          .attr('visibility', 'hidden');

        // Get bounding box to test size
        const bbox = testText.node().getBBox();
        const textWidth = bbox.width;

        // Remove test text
        testText.remove();

        // Calculate appropriate font size
        const maxFontSize = 14;
        const availableWidth = radius * 1.5;  // 75% of diameter

        // Scale font size based on text length
        let fontSize = Math.min(maxFontSize, Math.max(8, availableWidth / textWidth * maxFontSize));

        // Add the real text with calculated font size
        group.append('text')
          .text(d.label)
          .attr('text-anchor', 'middle')
          .attr('alignment-baseline', 'middle')
          .attr('fill', '#fff')
          .style('font-size', `${fontSize}px`);

        d.collisionRadius = radius;

      } else if (d.shape === 'rect' || d.shape === 'box') {
        // For boxes, use standard size
        const boxWidth = standardSizes.box.width;
        const boxHeight = standardSizes.box.height;

        // Add rectangle first
        group.append('rect')
          .attr('width', boxWidth)
          .attr('height', boxHeight)
          .attr('x', -boxWidth / 2)
          .attr('y', -boxHeight / 2)
          .attr('fill', d.color)
          .lower();

        // Add a hidden text element to test text size
        const testText = group.append('text')
          .text(d.label)
          .attr('visibility', 'hidden');

        // Get bounding box to test size
        const bbox = testText.node().getBBox();
        const textWidth = bbox.width;

        // Remove test text
        testText.remove();

        // Calculate appropriate font size
        const maxFontSize = 14;
        const availableWidth = boxWidth * 0.8;  // 80% of box width

        // Scale font size based on text length
        let fontSize = Math.min(maxFontSize, Math.max(8, availableWidth / textWidth * maxFontSize));

        // Add the real text with calculated font size
        group.append('text')
          .text(d.label)
          .attr('text-anchor', 'middle')
          .attr('alignment-baseline', 'middle')
          .attr('fill', '#fff')
          .style('font-size', `${fontSize}px`);

        d.collisionRadius = Math.sqrt((boxWidth / 2) ** 2 + (boxHeight / 2) ** 2);

      } else if (d.shape === 'diamond') {
        // For diamonds, create a custom horizontal diamond path
        const diamondWidth = standardSizes.diamond.width;
        const diamondHeight = standardSizes.diamond.height;

        // Create a diamond path that is wider than it is tall
        const diamondPath = `M0,${-diamondHeight/2} L${diamondWidth/2},0 L0,${diamondHeight/2} L${-diamondWidth/2},0 Z`;

        // Add diamond shape
        group.append('path')
          .attr('d', diamondPath)
          .attr('fill', d.color)
          .lower();

        // Add a hidden text element to test text size
        const testText = group.append('text')
          .text(d.label)
          .attr('visibility', 'hidden');

        // Get bounding box to test size
        const bbox = testText.node().getBBox();
        const textWidth = bbox.width;

        // Remove test text
        testText.remove();

        // Calculate appropriate font size
        const maxFontSize = 14;
        // Diamond has less usable space due to angles, use 60% of width
        const availableWidth = diamondWidth * 0.6;

        // Scale font size based on text length
        let fontSize = Math.min(maxFontSize, Math.max(8, availableWidth / textWidth * maxFontSize));

        // Add the real text with calculated font size
        group.append('text')
          .text(d.label)
          .attr('text-anchor', 'middle')
          .attr('alignment-baseline', 'middle')
          .attr('fill', '#fff')
          .style('font-size', `${fontSize}px`);

        d.collisionRadius = Math.max(diamondWidth/2, diamondHeight/2);
      }
    });

    // Create a simulation with optimized forces for tighter packing
    const simulation = d3.forceSimulation(nodes)
      .force('link', d3.forceLink(links).id(d => d.id)
        .distance(80))  // Reduced distance for tighter packing
      .force('charge', d3.forceManyBody()
        .strength(-200))  // Reduced repulsion for closer nodes
      .force('center', d3.forceCenter(width / 2, height / 2));

    // Add collision force with slightly smaller padding
    simulation.force('collision', d3.forceCollide()
      .radius(d => d.collisionRadius + 5)  // Reduced padding (from 10 to 5)
      .strength(1));  // Maximum strength to prevent overlap

    // Update positions on each tick
    simulation.on('tick', () => {
      link
        .attr('x1', (d) => d.source.x)
        .attr('y1', (d) => d.source.y)
        .attr('x2', (d) => d.target.x)
        .attr('y2', (d) => d.target.y);

      node.attr('transform', (d) => `translate(${d.x},${d.y})`);
    });

    // Function to reset graph visibility
    function resetGraphVisibility() {
      // Reset all nodes and links to visible
      link.style('opacity', 1);
      node.style('opacity', 1)
        .each(function(d) { d.visible = true; });
    }

    // Add click event to the background rect to reset the graph visibility
    background.on('click', resetGraphVisibility);


    // Drag functions - modified to prevent dragging hidden nodes
    function dragstarted(event, d) {
      // Only allow dragging visible nodes
      if (!d.visible) return;

      if (!event.active) simulation.alphaTarget(0.3).restart();
      d.fx = d.x;
      d.fy = d.y;
    }

    function dragged(event, d) {
      // Only allow dragging visible nodes
      if (!d.visible) return;

      d.fx = event.x;
      d.fy = event.y;
    }

    function dragended(event, d) {
      // Only process for visible nodes
      if (!d.visible) return;

      if (!event.active) simulation.alphaTarget(0);
      d.fx = null;
      d.fy = null;
    }

    // Filter graph to show only the clicked node and its neighbors
  }, [dimensions]);

  return (
    <div
      ref={containerRef}
      style={{
        boxSizing: 'border-box',
        width: '100%',
        height: '100%',
        position: 'absolute',
        top: 0,
        left: 0,
        margin: 0,
        padding: 0,
        overflow: 'hidden'
      }}

    >
      <svg ref={svgRef} style={{ display: 'block', width: '100%', height: '100%' }}></svg>
    </div>
  );
};

export default ForceDirectedGraph;