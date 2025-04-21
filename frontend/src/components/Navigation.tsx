import React from 'react';
import { BarChart3, Grid, Network } from 'lucide-react';

interface NavigationProps {
  currentPage: 'home' | 'analysis' | 'clusters';
  onNavigate: (page: 'home' | 'analysis' | 'clusters') => void;
}

const Navigation: React.FC<NavigationProps> = ({ currentPage, onNavigate }) => {
  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-white shadow-md">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center space-x-8">
            <span className="text-2xl font-bold text-blue-600">NewsLens</span>
            
            <div className="hidden md:flex space-x-4">
              <button
                onClick={() => onNavigate('home')}
                className={`flex items-center px-3 py-2 rounded-md transition-colors ${
                  currentPage === 'home'
                    ? 'bg-blue-100 text-blue-700'
                    : 'text-gray-600 hover:bg-gray-100'
                }`}
              >
                <Grid size={18} className="mr-2" />
                Coverage Grid
              </button>
              
              <button
                onClick={() => onNavigate('analysis')}
                className={`flex items-center px-3 py-2 rounded-md transition-colors ${
                  currentPage === 'analysis'
                    ? 'bg-blue-100 text-blue-700'
                    : 'text-gray-600 hover:bg-gray-100'
                }`}
              >
                <BarChart3 size={18} className="mr-2" />
                Analysis
              </button>

              <button
                onClick={() => onNavigate('clusters')}
                className={`flex items-center px-3 py-2 rounded-md transition-colors ${
                  currentPage === 'clusters'
                    ? 'bg-blue-100 text-blue-700'
                    : 'text-gray-600 hover:bg-gray-100'
                }`}
              >
                <Network size={18} className="mr-2" />
                Topic Clusters
              </button>
            </div>
          </div>
          
          {/* Mobile navigation */}
          <div className="md:hidden flex space-x-2">
            <button
              onClick={() => onNavigate('home')}
              className={`p-2 rounded-md ${
                currentPage === 'home'
                  ? 'bg-blue-100 text-blue-700'
                  : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              <Grid size={20} />
            </button>
            
            <button
              onClick={() => onNavigate('analysis')}
              className={`p-2 rounded-md ${
                currentPage === 'analysis'
                  ? 'bg-blue-100 text-blue-700'
                  : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              <BarChart3 size={20} />
            </button>

            <button
              onClick={() => onNavigate('clusters')}
              className={`p-2 rounded-md ${
                currentPage === 'clusters'
                  ? 'bg-blue-100 text-blue-700'
                  : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              <Network size={20} />
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navigation;