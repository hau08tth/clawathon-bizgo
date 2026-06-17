import React from "react";

interface Props {
  text: string;
  className?: string;
}

function renderInline(s: string): React.ReactNode[] {
  const parts = s.split(/(\*\*[^*]+\*\*|_[^_]+_)/g);
  return parts.map((p, i) => {
    if (p.startsWith("**") && p.endsWith("**")) return <strong key={i}>{p.slice(2, -2)}</strong>;
    if (p.startsWith("_") && p.endsWith("_")) return <em key={i}>{p.slice(1, -1)}</em>;
    return <span key={i}>{p}</span>;
  });
}

export function MarkdownText({ text, className }: Props) {
  if (!text) return null;
  const lines = text.split("\n");
  const elements: React.ReactNode[] = [];
  let ulBuffer: string[] = [];
  let olBuffer: { n: string; t: string }[] = [];

  const flushUl = (key: string) => {
    if (!ulBuffer.length) return;
    elements.push(
      <ul key={key} className="list-disc pl-4 space-y-0.5 my-1">
        {ulBuffer.map((t, i) => <li key={i}>{renderInline(t)}</li>)}
      </ul>
    );
    ulBuffer = [];
  };
  const flushOl = (key: string) => {
    if (!olBuffer.length) return;
    elements.push(
      <ol key={key} className="list-decimal pl-4 space-y-0.5 my-1">
        {olBuffer.map((t, i) => <li key={i}>{renderInline(t.t)}</li>)}
      </ol>
    );
    olBuffer = [];
  };

  lines.forEach((line, idx) => {
    const ulMatch = line.match(/^[-*]\s+(.*)/);
    const olMatch = line.match(/^(\d+)\.\s+(.*)/);
    if (ulMatch) {
      flushOl(`ol-${idx}`);
      ulBuffer.push(ulMatch[1]);
    } else if (olMatch) {
      flushUl(`ul-${idx}`);
      olBuffer.push({ n: olMatch[1], t: olMatch[2] });
    } else {
      flushUl(`ul-${idx}`);
      flushOl(`ol-${idx}`);
      if (line.trim() === "") {
        elements.push(<div key={`br-${idx}`} className="h-1" />);
      } else {
        elements.push(
          <p key={`p-${idx}`} className="leading-relaxed">
            {renderInline(line)}
          </p>
        );
      }
    }
  });
  flushUl("ul-end");
  flushOl("ol-end");

  return <div className={className}>{elements}</div>;
}
