import React, { Suspense, lazy } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

const CurrentPositions = lazy(() => import('./components/CurrentPositions'));
const Sales = lazy(() => import('./components/Sales'));

function App() {
  return (
    <Router>
      <Suspense fallback={<h2>Loading...</h2>}>
        <Routes>
          <Route path="/" element={<CurrentPositions />} />
          <Route path="/sales" element={<Sales />} />
        </Routes>
      </Suspense>
    </Router>
  );
}

export default App;
