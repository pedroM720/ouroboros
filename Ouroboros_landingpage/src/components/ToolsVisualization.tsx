import { useEffect, useState } from 'react';
import { Wrench, GitBranch, Network } from 'lucide-react';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  tools?: string[];
}

interface ToolsVisualizationProps {
  messages: Message[];
}

export function ToolsVisualization({ messages }: ToolsVisualizationProps) {
  const [allTools, setAllTools] = useState<string[]>([]);

  useEffect(() => {
    const tools = messages
      .flatMap(m => m.tools || [])
      .filter((tool, index, self) => self.indexOf(tool) === index);
    setAllTools(tools);
  }, [messages]);

  if (allTools.length === 0) return null;

  return (
    <div className="max-w-4xl mx-auto mt-16 animate-fade-in-delay">
      <div className="bg-black/20 backdrop-blur-md rounded-3xl border border-purple-400/20 p-8">
        <div className="flex items-center gap-3 mb-6">
          <Network className="w-6 h-6 text-purple-300" />
          <h2 className="text-white text-xl">Tool Ecosystem</h2>
          <span className="ml-auto px-3 py-1 bg-purple-600/30 rounded-full text-sm text-purple-200">
            {allTools.length} {allTools.length === 1 ? 'Tool' : 'Tools'}
          </span>
        </div>

        <div className="relative">
          {/* Ouroboros Circle Visualization */}
          <div className="flex flex-wrap gap-3 mb-6">
            {allTools.map((tool, index) => (
              <div
                key={index}
                className="group relative"
                style={{
                  animation: `fadeInScale 0.5s ease-out ${index * 0.1}s both`
                }}
              >
                <div className="px-4 py-2 bg-gradient-to-r from-purple-600/40 to-purple-500/40 rounded-lg border border-purple-400/30 hover:border-purple-300/50 transition-all duration-300 hover:scale-105 cursor-pointer">
                  <div className="flex items-center gap-2">
                    <Wrench className="w-4 h-4 text-purple-200" />
                    <span className="text-white">{tool}</span>
                  </div>
                </div>
                
                {/* Connection lines effect */}
                {index < allTools.length - 1 && (
                  <div className="absolute top-1/2 -right-1 w-2 h-0.5 bg-gradient-to-r from-purple-400/50 to-transparent" />
                )}
              </div>
            ))}
          </div>

          {/* Self-Evolution Indicator */}
          <div className="flex items-center justify-center gap-2 text-purple-200/60 text-sm">
            <GitBranch className="w-4 h-4" />
            <span>Continuously evolving and building new capabilities</span>
          </div>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-3 gap-4 mt-6">
        <div className="bg-black/20 backdrop-blur-sm rounded-xl border border-white/10 p-4 text-center">
          <div className="text-3xl text-white mb-1">{allTools.length}</div>
          <div className="text-sm text-white/60">Tools Generated</div>
        </div>
        <div className="bg-black/20 backdrop-blur-sm rounded-xl border border-white/10 p-4 text-center">
          <div className="text-3xl text-white mb-1">{messages.filter(m => m.role === 'user').length}</div>
          <div className="text-sm text-white/60">Tasks Completed</div>
        </div>
        <div className="bg-black/20 backdrop-blur-sm rounded-xl border border-white/10 p-4 text-center">
          <div className="text-3xl text-white mb-1">∞</div>
          <div className="text-sm text-white/60">Growth Potential</div>
        </div>
      </div>
    </div>
  );
}
