import React, { useState } from 'react';
import Home from './routes/Home';
import Analysis from './routes/Analysis';
import Clusters from './routes/Clusters';
import Navigation from './components/Navigation';

function App() {
  const [currentPage, setCurrentPage] = useState<'home' | 'analysis' | 'clusters'>('home');

  return (
    <div className="min-h-screen bg-gray-50">
      <Navigation currentPage={currentPage} onNavigate={setCurrentPage} />
      {currentPage === 'home' ? <Home /> : 
       currentPage === 'analysis' ? <Analysis /> : 
       <Clusters />}
    </div>
  );
}

export default App;