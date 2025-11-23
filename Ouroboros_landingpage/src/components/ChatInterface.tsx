import { User, Bot, Loader2 } from 'lucide-react';
import { useEffect, useRef } from 'react';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  tools?: string[];
}

interface ChatInterfaceProps {
  messages: Message[];
  isProcessing: boolean;
}

export function ChatInterface({ messages, isProcessing }: ChatInterfaceProps) {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isProcessing]);

  return (
    <div className="max-w-4xl mx-auto mt-12 space-y-6 animate-fade-in">
      {messages.map((message, index) => (
        <div
          key={index}
          // ADDED "items-center" HERE vvv
          className={`flex gap-4 items-center ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
        >
          {message.role === 'assistant' && (
            <div className="shrink-0 w-10 h-10 rounded-full bg-purple-600/30 flex items-center justify-center border border-purple-400/30">
              <Bot className="w-5 h-5 text-purple-200" />
            </div>
          )}
          
          <div
            className={`max-w-2xl px-6 py-4 rounded-2xl backdrop-blur-sm ${
              message.role === 'user'
                ? 'bg-white/20 text-white'
                : 'bg-black/30 text-white border border-purple-400/20'
            }`}
          >
            <p className="leading-relaxed">{message.content}</p>
            
            {message.tools && message.tools.length > 0 && (
              <div className="mt-4 pt-4 border-t border-white/10">
                <p className="text-sm text-purple-300 mb-2">Tools Generated:</p>
                <div className="flex flex-wrap gap-2">
                  {message.tools.map((tool, toolIndex) => (
                    <span
                      key={toolIndex}
                      className="px-3 py-1 bg-purple-600/30 rounded-full text-xs text-purple-200 border border-purple-400/30"
                    >
                      {tool}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>

          {message.role === 'user' && (
            <div className="shrink-0 w-10 h-10 rounded-full bg-white/20 flex items-center justify-center">
              <User className="w-5 h-5 text-white" />
            </div>
          )}
        </div>
      ))}

      {isProcessing && (
        <div className="flex gap-4 justify-start">
          <div className="shrink-0 w-10 h-10 rounded-full bg-purple-600/30 flex items-center justify-center border border-purple-400/30">
            <Bot className="w-5 h-5 text-purple-200" />
          </div>
          <div className="max-w-2xl px-6 py-4 rounded-2xl backdrop-blur-sm bg-black/30 text-white border border-purple-400/20">
            <div className="flex items-center gap-3">
              <Loader2 className="w-5 h-5 animate-spin text-purple-300" />
              <span className="text-purple-200">Generating tools and analyzing...</span>
            </div>
          </div>
        </div>
      )}

      <div ref={messagesEndRef} />
    </div>
  );
}
