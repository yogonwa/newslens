import React, { useEffect, useRef } from 'react';
import d3Cloud from 'd3-cloud';

interface Word {
  text: string;
  value: number;
}

interface WordCloudProps {
  words: Word[];
}

const WordCloud: React.FC<WordCloudProps> = ({ words }) => {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!containerRef.current) return;

    const width = containerRef.current.clientWidth;
    const height = containerRef.current.clientHeight;

    // Clear previous content
    containerRef.current.innerHTML = '';

    const layout = d3Cloud()
      .size([width, height])
      .words(words)
      .padding(5)
      .rotate(() => (~~(Math.random() * 2) * 90))
      .fontSize(d => d.value)
      .on('end', draw);

    layout.start();

    function draw(words: d3Cloud.Word[]) {
      const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
      svg.setAttribute('width', width.toString());
      svg.setAttribute('height', height.toString());
      
      const group = document.createElementNS('http://www.w3.org/2000/svg', 'g');
      group.setAttribute('transform', `translate(${width/2},${height/2})`);
      
      words.forEach(word => {
        const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        text.textContent = word.text;
        text.setAttribute('text-anchor', 'middle');
        text.setAttribute('transform', `translate(${word.x},${word.y}) rotate(${word.rotate})`);
        text.setAttribute('font-size', `${word.size}px`);
        text.setAttribute('fill', `hsl(${Math.random() * 360}, 70%, 50%)`);
        group.appendChild(text);
      });
      
      svg.appendChild(group);
      containerRef.current?.appendChild(svg);
    }
  }, [words]);

  return <div ref={containerRef} className="w-full h-full" />;
};

export default WordCloud;