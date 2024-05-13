import logo from './logo.svg';
import './App.css';

import React from 'react';
import './App.css'; // Make sure this points to your actual CSS file
import ImageGallery from './components/ImageGallery'; // Import the ImageGallery component if it's in a separate file

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Tattoo Analysis Gallery</h1>
        <p>Click on an image to analyze it.</p>
      </header>
      <ImageGallery />
    </div>
  );
}

export default App;

