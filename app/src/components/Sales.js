import './App.css';
import DataTable from 'react-data-table-component';
import { useQuery } from '@tanstack/react-query';

const columns = [
	{
		name: 'Coin',
		selector: row => row.coin,
	},
    {
		name: 'Buy Date',
		selector: row => row.buy_date,
        format: row => new Date(row.buy_date).toLocaleDateString(),
	},
	{
		name: 'Sales Date',
		selector: row => row.sales_date,
        format: row => new Date(row.sales_date).toLocaleDateString(),
	},
    {
        name: 'Proceeds',
        selector: row => row.actual_proceeds,
    },
    {
        name: 'Cost',
        selector: row => row.actual_cost,
    },
    {
        name: 'Gains / Losses',
        selector: row => row.gains_losses,
    },
    {
        name: 'Source',
        selector: row => row.source,
    }
];

function Sales() {
    const { data: sales, isLoading, error } = useQuery({
        queryFn: () =>
          fetch('http://localhost:5000/sales/2024').then(
            (res) => res.json()
          ),
        queryKey: ['sales_2023'],
    });

    // Show a loading message while data is fetching
    if (isLoading) {
        return <h2>Loading...</h2>;
    }
    
    // to handle error
    if (error) {
        return <div className="error">Error: error fetching</div>
    }

    return (
        <div className="App">
            <header className="App-header">
                Sales
            </header>
            <body className="App-body">
                <DataTable
                    columns={columns}
                    data={sales}
                />
            </body>
        </div>
    )
}

export default Sales;