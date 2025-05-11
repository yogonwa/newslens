import React, { useState, useEffect } from 'react';
import { Calendar, Search, Menu, X } from 'lucide-react';

interface HeaderProps {
  onSearchChange: (query: string) => void;
}

const Header: React.FC<HeaderProps> = ({ onSearchChange }) => {
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 10);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchQuery(e.target.value);
    onSearchChange(e.target.value);
  };

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  return (
    <header
      className={`fixed top-16 left-0 right-0 z-40 transition-all duration-300 ${
        isScrolled ? 'bg-white shadow-md py-2' : 'bg-transparent py-4'
      }`}
    >
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center">
          {/* Subheader removed, contents moved up */}

          <div className="hidden md:flex items-center space-x-6">
            {/* Search bar removed */}
          </div>

          <button className="md:hidden" onClick={toggleMenu}>
            {isMenuOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>

        {/* Mobile menu */}
        {isMenuOpen && (
          <div className="md:hidden mt-4 bg-white rounded-lg shadow-lg p-4 absolute left-4 right-4">
            {/* Search bar removed from mobile menu */}
          </div>
        )}
      </div>
    </header>
  );
};

export default Header;