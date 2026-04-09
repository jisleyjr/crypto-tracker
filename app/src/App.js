import React, { Suspense, lazy } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import './App.css';

const CurrentPositions = lazy(() => import('./components/CurrentPositions'));
const Sales = lazy(() => import('./components/Sales'));

function Navigation() {
  const location = useLocation();

  return (
    <nav className="sidebar">
      <div className="nav-header">Crypto Tracker</div>
      <ul className="nav-list">
        <li>
          <Link 
            to="/" 
            className={location.pathname === '/' ? 'nav-link active' : 'nav-link'}
          >
            Positions
          </Link>
        </li>
        <li>
          <Link 
            to="/sales" 
            className={location.pathname === '/sales' ? 'nav-link active' : 'nav-link'}
          >
            Sales
          </Link>
        </li>
      </ul>
    </nav>
  );
}

function App() {
  return (
    <Router>
      <div className="app-container">
        <Navigation />
        <div className="main-content">
          <Suspense fallback={<h2>Loading...</h2>}>
            <Routes>
              <Route path="/" element={<CurrentPositions />} />
              <Route path="/sales" element={<Sales />} />
            </Routes>
          </Suspense>
        </div>
      </div>
    </Router>
  );
}

export default App;
