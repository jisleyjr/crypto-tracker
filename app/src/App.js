import './App.css';
import Coins from './components/Coins.js';
import Positions from './components/Positions.js';
import { useState } from 'react';

function App() {
  const [coin, setCoin] = useState('ADA');

  return (
    <div className="App">
      <header className="App-header">
        <Coins onChange={event => setCoin(event.target.value)}/>
        <Positions selectedCoin={coin} />
      </header>
    </div>
  );
}

export default App;
