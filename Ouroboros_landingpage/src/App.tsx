import { useState, useRef, useEffect } from 'react';
import { Menu, X, Send, Sparkles, Wand2, Zap } from 'lucide-react';
import img85088621 from "figma:asset/b81b4a2f1d6dd33617eaa8d69e28710e079f0b7b.png";
import { ChatInterface } from './components/ChatInterface';
import { ToolsVisualization } from './components/ToolsVisualization';
import { Navigation } from './components/Navigation';
import { DynamicBackground } from './components/DynamicBackground';

export default function App() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [inputValue, setInputValue] = useState('');
  const [messages, setMessages] = useState<Array<{ role: 'user' | 'assistant'; content: string; tools?: string[] }>>([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [totalSavings, setTotalSavings] = useState(0.00);
  const inputRef = useRef<HTMLInputElement>(null);


const calculateDifferential = (inputTokens, outputTokens) => {
  // Competitor (GPT-5) Costs
  const gpt5BaseFee = 0.008;
  const gpt5InputCost = (inputTokens / 1000000) * 1.25;
  const gpt5OutputCost = (outputTokens / 1000000) * 10.00;
  const gpt5Total = gpt5BaseFee + gpt5InputCost + gpt5OutputCost;

  // Your Backend (Gemini 2.5 Flash) Costs
  // Assuming $0.075 In / $0.30 Out per 1M (Flash rates)
  const geminiInputCost = (inputTokens / 1000000) * 0.075; 
  const geminiOutputCost = (outputTokens / 1000000) * 0.30;
  const geminiTotal = geminiInputCost + geminiOutputCost;

  return gpt5Total - geminiTotal; // The Savings
};

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim() || isProcessing) return;

    const userMessage = inputValue.trim();
    setInputValue('');
    const inputTokens = userMessage.split(' ').length * 1.3;
    const outputTokens = 150;
    const querySavings = calculateDifferential(inputTokens, outputTokens);

    // 3. Update State
    setTotalSavings(prev => prev + querySavings);
      
    // UI
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setIsProcessing(true);






try {
  const res = await fetch(`http://localhost:8080/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ 
        message: userMessage,
        session_id: "demo-session-1"
    }),
  });

  const data = await res.json();
  console.log("Is Reflex?", data.is_reflex);

  // Only add savings if Ouroboros used a tool (reflex mode)
  if (data.is_reflex) {
    const inputTokens = userMessage.split(" ").length * 1.3;
    const outputTokens = 150;

    const querySavings = calculateDifferential(inputTokens, outputTokens);

    setTotalSavings(prev => prev + querySavings);
  }

  setMessages(prev => [...prev, { 
    role: 'assistant', 
    content: data.response || data.message,
    tools: data.tools || [] 
  }]);

} catch (error) {
      console.error("Connection failed:", error);
      setMessages(prev => [...prev, { role: 'assistant', content: "error connecting to backend" }]);
    } finally {
      setIsProcessing(false);
    }
  };

  const generateToolsForQuery = (query: string): string[] => {
    const toolSets = {
      data: ['DataParser', 'SchemaValidator', 'DataTransformer'],
      web: ['WebScraper', 'HTMLParser', 'URLExtractor'],
      analysis: ['SentimentAnalyzer', 'StatisticsEngine', 'TrendDetector'],
      image: ['ImageProcessor', 'OCRExtractor', 'VisionAnalyzer'],
      code: ['CodeCompiler', 'SyntaxChecker', 'RefactorEngine'],
      default: ['QueryProcessor', 'ContextAnalyzer', 'ResponseGenerator']
    };

    const lowerQuery = query.toLowerCase();
    if (lowerQuery.includes('data') || lowerQuery.includes('parse')) return toolSets.data;
    if (lowerQuery.includes('web') || lowerQuery.includes('scrape')) return toolSets.web;
    if (lowerQuery.includes('analyz') || lowerQuery.includes('sentiment')) return toolSets.analysis;
    if (lowerQuery.includes('image') || lowerQuery.includes('picture')) return toolSets.image;
    if (lowerQuery.includes('code') || lowerQuery.includes('program')) return toolSets.code;
    return toolSets.default;
  };

  const generateResponse = (query: string, tools: string[]): string => {
    return `I've analyzed your request and created ${tools.length} specialized tools to help: ${tools.join(', ')}. Like the Ouroboros serpent, I'm continuously evolving and building new capabilities to better serve your needs. Each tool I create makes me more capable for future tasks.`;
  };

  const scrollToChat = () => {
    inputRef.current?.scrollIntoView({ behavior: 'smooth', block: 'center' });
    inputRef.current?.focus();
  };

  return (
    <div className="relative min-h-screen overflow-x-hidden">
      {/* Dynamic Animated Background */}
      <DynamicBackground />

      {/* Navigation */}
      <Navigation isMenuOpen={isMenuOpen} setIsMenuOpen={setIsMenuOpen} logo={img85088621} />

      {/* Hero Section */}
      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-32 pb-20">
        <div className="max-w-[650px] mx-auto">
          <h1 className="font-['Bai_Jamjuree:Medium',sans-serif] text-[48px] leading-[70px] tracking-[2.4px] mb-12 animate-fade-in text-white text-left">
            <p className="mb-0">Introducing Ouroboros,</p>
            <p className="mb-0">Unparalleled</p>
            <p className="mb-0">Tool-Assisted Generative</p>
            <p className="mb-0">AI</p>
          </h1>

          {/* --- SAVINGS WIDGET (FIXED & THEMED) --- */}
          {/* Placed inside the main container, aligned to the right of the content column */}
          {totalSavings > 0 && (
            <div className="flex justify-end mb-4 animate-fade-in-down">
              <div className="
                group
                bg-[#13141c]/90 backdrop-blur-md 
                border border-purple-500/20 
                rounded-2xl p-4 pr-6 pl-6
                shadow-[0px_0px_30px_-5px_rgba(168,85,247,0.15)] 
                flex flex-col items-end 
                transition-all duration-300 
                hover:border-purple-500/40 hover:shadow-[0px_0px_30px_-5px_rgba(168,85,247,0.3)]
                transform hover:-translate-y-1
              ">
                
                {/* Header */}
                <div className="flex items-center gap-2 mb-0.7">
                  <span className="relative flex h-2 w-2">
                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                    <span className="relative inline-flex rounded-full h-2 w-2 bg-green-500 shadow-[0_0_10px_rgba(34,197,94,0.6)]"></span>
                  </span>
                  <span className="font-['Bai_Jamjuree',sans-serif] text-[10px] text-purple-200 uppercase tracking-[0.15em] font-bold opacity-80 group-hover:opacity-100 transition-opacity">
                    Ouroboros Efficiency
                  </span>
                </div>

                  {/* Money Amount */}
                  <div className="flex items-center justify-center gap-1.5 mb-0.7 w-full">
                    <span className="font-sans text-3xl text-purple-200/60 font-light">$</span>
                    <span className="font-['Bai_Jamjuree',sans-serif] text-3xl text-white font-medium tracking-tight drop-shadow-sm">
                      {totalSavings.toFixed(2)}
                    </span>
                  </div>

                {/* Subtitle */}
                <div className="font-['Bai_Jamjuree',sans-serif] text-[10px] text-purple-200 uppercase tracking-[0.15em] font-bold opacity-80 group-hover:opacity-100 transition-opacity">
                  saved vs. Standard LLM
                </div>

              </div>
            </div>
          )}



          {/* Main Input */}
          <div className="max-w-2xl mb-8">
            <form onSubmit={handleSubmit} className="relative">
              <div className="bg-[rgba(43,45,48,0.6)] backdrop-blur-xl rounded-[20px] shadow-[0px_4px_4px_0px_rgba(0,0,0,0.25)] border-[5px] border-solid border-[rgba(255,255,255,0.1)] hover:border-[rgba(255,255,255,0.2)] transition-all duration-300">
                <div className="flex items-center gap-4 px-8 py-6">
                  <label htmlFor="main-input" className="font-['Average_Sans:Regular',sans-serif] text-[#dcdee3] tracking-[0.05em] shrink-0">
                    Ask away:
                  </label>
                  <input
                    id="main-input"
                    ref={inputRef}
                    type="text"
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    className="flex-1 bg-transparent text-white outline-none placeholder:text-gray-500"
                    placeholder="What would you like me to build?"
                    disabled={isProcessing}
                  />
                  <button
                    type="submit"
                    disabled={!inputValue.trim() || isProcessing}
                    className="shrink-0 p-2 rounded-full bg-purple-500/20 hover:bg-purple-500/40 disabled:opacity-30 disabled:hover:bg-purple-500/20 transition-all duration-200"
                  >
                    <Send className="w-5 h-5 text-white" />
                  </button>
                </div>
              </div>
            </form>
          </div>

          {/* Feature Pills - Removed */}
        </div>

        {/* Chat Interface */}
        {messages.length > 0 && (
          <ChatInterface 
            messages={messages} 
            isProcessing={isProcessing}
          />
        )}

        {/* Tools Visualization */}
        {messages.some(m => m.tools) && (
          <ToolsVisualization 
            messages={messages.filter(m => m.tools)}
          />
        )}
      </div>

      {/* Floating Info */}
      {messages.length === 0 && (
        <div className="fixed bottom-8 left-1/2 transform -translate-x-1/2 z-20 animate-fade-in-delay-2">
          <div className="bg-black/40 backdrop-blur-md rounded-full px-6 py-3 text-white/80 flex items-center gap-2">
            <div className="w-2 h-2 bg-purple-400 rounded-full animate-pulse" />
            <span className="text-sm">Self-evolving AI • Building tools in real-time</span>
          </div>
        </div>
      )}
    </div>
  );
}