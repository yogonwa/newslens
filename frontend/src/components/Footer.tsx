import React from 'react';
import { Github, Twitter, Info } from 'lucide-react';

const Footer: React.FC = () => {
  return (
    <footer className="bg-gray-800 text-white pt-12 pb-8 mt-16">
      <div className="container mx-auto px-4">
        <div className="flex flex-wrap justify-between">
          <div className="w-full md:w-1/3 mb-8 md:mb-0">
            <h3 className="text-xl font-bold mb-4">NewsLens</h3>
            <p className="text-gray-300 mb-4">
              Tracking news divergence across different media outlets. See how the same events are covered differently over time.
            </p>
            <div className="flex space-x-4">
              <a href="#" className="text-gray-300 hover:text-white transition-colors">
                <Github size={20} />
              </a>
              <a href="#" className="text-gray-300 hover:text-white transition-colors">
                <Twitter size={20} />
              </a>
              <a href="#" className="text-gray-300 hover:text-white transition-colors">
                <Info size={20} />
              </a>
            </div>
          </div>
          
          <div className="w-full md:w-1/3 mb-8 md:mb-0">
            <h3 className="text-lg font-bold mb-4">Features</h3>
            <ul className="space-y-2">
              <li><a href="#" className="text-gray-300 hover:text-white transition-colors">Media comparison</a></li>
              <li><a href="#" className="text-gray-300 hover:text-white transition-colors">Sentiment analysis</a></li>
              <li><a href="#" className="text-gray-300 hover:text-white transition-colors">Historical archives</a></li>
              <li><a href="#" className="text-gray-300 hover:text-white transition-colors">Timeline playback</a></li>
            </ul>
          </div>
          
          <div className="w-full md:w-1/3">
            <h3 className="text-lg font-bold mb-4">About</h3>
            <ul className="space-y-2">
              <li><a href="#" className="text-gray-300 hover:text-white transition-colors">How it works</a></li>
              <li><a href="#" className="text-gray-300 hover:text-white transition-colors">Media sources</a></li>
              <li><a href="#" className="text-gray-300 hover:text-white transition-colors">Privacy policy</a></li>
              <li><a href="#" className="text-gray-300 hover:text-white transition-colors">Contact us</a></li>
            </ul>
          </div>
        </div>
        
        <div className="border-t border-gray-700 mt-8 pt-8 text-center">
          <p className="text-gray-400 text-sm">
            &copy; {new Date().getFullYear()} NewsLens. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;