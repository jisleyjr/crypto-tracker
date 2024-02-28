import './App.css';
import Coins from './Coins.js';
import Positions from './Positions.js';
import { useState } from 'react';

function CurrentPositions() {
  const [coin, setCoin] = useState('ADA');

  return (
    <div className="App">
      <header className="App-header">
        <Coins onChange={event => setCoin(event.target.value)}/>
      </header>
      <body className="App-body">
        <Positions selectedCoin={coin} />
      </body>
    </div>
  );
}

export default CurrentPositions;