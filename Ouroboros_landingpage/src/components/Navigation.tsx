import { Menu, X } from 'lucide-react';
import { useState, useEffect } from 'react';

interface NavigationProps {
  isMenuOpen: boolean;
  setIsMenuOpen: (open: boolean) => void;
  logo: string;
}

export function Navigation({ isMenuOpen, setIsMenuOpen, logo }: NavigationProps) {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 20);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <>
      {/* Logo - Centered with navbar */}
      <div className={`fixed top-[5px] left-[18px] z-50 transition-all duration-300 ${scrolled ? 'scale-90' : 'scale-100'}`}>
        <div className="h-[98px] w-[102px]">
          <div className="relative overflow-hidden rounded-[20px] border-[0.5px] border-solid border-white/50 hover:border-white transition-colors duration-200" style={{ height: "100%", width: "100%" }}>
            <img 
              alt="Ouroboros logo" 
              className="absolute h-[283.95%] left-[-19.37%] max-w-none top-[-36.85%] w-[356.78%]" 
              src={logo} 
            />
          </div>
        </div>
      </div>

      {/* Hamburger Menu Button */}
      <button
        onClick={() => setIsMenuOpen(!isMenuOpen)}
        className={`fixed top-8 right-8 z-50 bg-[rgba(0,0,0,0)] box-border flex flex-col gap-[8px] items-center justify-center p-[10px] w-[46px] transition-all duration-300 hover:scale-110 ${scrolled ? 'scale-90' : 'scale-100'}`}
        aria-label="Toggle menu"
      >
        {isMenuOpen ? (
          <X className="w-8 h-8 text-white" />
        ) : (
          <>
            <div className="bg-white h-[2.5px] w-[50px] transition-all duration-300" />
            <div className="bg-white h-[2.5px] w-[50px] transition-all duration-300" />
            <div className="bg-white h-[2.5px] w-[50px] transition-all duration-300" />
          </>
        )}
      </button>

      {/* Slide-out Menu */}
      <div className={`fixed inset-y-0 right-0 w-full sm:w-96 bg-[#1a1a1a]/95 backdrop-blur-xl z-40 transform transition-transform duration-300 ease-in-out ${isMenuOpen ? 'translate-x-0' : 'translate-x-full'}`}>
        <nav className="h-full flex flex-col pt-32 px-8">
          <ul className="space-y-6">
            <li>
              <a 
                href="#about" 
                onClick={() => setIsMenuOpen(false)}
                className="block text-white hover:text-purple-300 transition-colors duration-200 text-xl tracking-wide"
              >
                About Ouroboros
              </a>
            </li>
            <li>
              <a 
                href="#how-it-works" 
                onClick={() => setIsMenuOpen(false)}
                className="block text-white hover:text-purple-300 transition-colors duration-200 text-xl tracking-wide"
              >
                How It Works
              </a>
            </li>
            <li>
              <a 
                href="#capabilities" 
                onClick={() => setIsMenuOpen(false)}
                className="block text-white hover:text-purple-300 transition-colors duration-200 text-xl tracking-wide"
              >
                Capabilities
              </a>
            </li>
            <li>
              <a 
                href="#tools" 
                onClick={() => setIsMenuOpen(false)}
                className="block text-white hover:text-purple-300 transition-colors duration-200 text-xl tracking-wide"
              >
                Tool Library
              </a>
            </li>
            <li>
              <a 
                href="#docs" 
                onClick={() => setIsMenuOpen(false)}
                className="block text-white hover:text-purple-300 transition-colors duration-200 text-xl tracking-wide"
              >
                Documentation
              </a>
            </li>
          </ul>
          
          <div className="mt-auto mb-12">
            <div className="border-t border-white/20 pt-6">
              <p className="text-white/60 text-sm mb-4">
                A self-evolving AI that builds its own tools to become smarter with every task.
              </p>
              <button className="w-full py-3 bg-purple-600 hover:bg-purple-700 text-white rounded-lg transition-colors duration-200">
                Get Started
              </button>
            </div>
          </div>
        </nav>
      </div>

      {/* Overlay */}
      {isMenuOpen && (
        <div 
          className="fixed inset-0 bg-black/50 z-30 backdrop-blur-sm"
          onClick={() => setIsMenuOpen(false)}
        />
      )}
    </>
  );
}