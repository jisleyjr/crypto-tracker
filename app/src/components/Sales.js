import './App.css';
import AvailableYears from './AvailableYears';
import SalesList from './SalesList';
import { useState } from 'react';

function Sales() {
    const [year, setYear] = useState('2021');

    return (
        <div className="App">
            <header className="App-header">
                <AvailableYears onChange={event => setYear(event.target.value)} />
            </header>
            <main className="App-body">
                <SalesList selectedYear={year} />
            </main>
        </div>
    )
}

export default Sales;