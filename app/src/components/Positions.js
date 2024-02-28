import React from 'react';
import DataTable from 'react-data-table-component';
import { useQuery } from '@tanstack/react-query';

const columns = [
	{
		name: 'Coin',
		selector: row => row.coin,
	},
	{
		name: 'Order Date',
		selector: row => row.order_date,
	},
    {
        name: 'Original Quantity',
        selector: row => row.original_qty,
    },
    {
        name: 'Remaining Quantity',
        selector: row => row.remaining_qty,
    },
    {
        name: 'Price',
        selector: row => row.price,
    },
];

export default function Positions({selectedCoin}) {
    const { data: positions, isLoading, error } = useQuery({
        queryFn: () =>
          fetch('http://localhost:5000/positions/' + selectedCoin).then(
            (res) => res.json()
          ),
        queryKey: ['positions_' + selectedCoin],
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
		<DataTable
			columns={columns}
			data={positions}
		/>
	);
};