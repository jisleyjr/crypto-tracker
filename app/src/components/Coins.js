import React from 'react';
import { useQuery } from '@tanstack/react-query';

// Create a react component called Coins that is a list of strings.
export default function Coins({onChange}) {
    const { data: coins, isLoading, error } = useQuery({
        queryFn: () =>
          fetch('http://localhost:5000/coins').then(
            (res) => res.json()
          ),
        queryKey: ['coins'],
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
        <select onChange={onChange}>
            {coins.map((coin, index) => (
                <option value={coin}>{coin}</option>
            ))}
        </select>
    )
}