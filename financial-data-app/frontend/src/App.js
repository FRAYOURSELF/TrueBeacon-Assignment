import React, { useEffect, useState } from 'react';
import './App.css';

function App() {
  const [ticksData, setTicksData] = useState([]);
  const [bhavcopyData, setBhavcopyData] = useState([]);
  const [ticksPage, setTicksPage] = useState(1);
  const [bhavcopyPage, setBhavcopyPage] = useState(1);
  const itemsPerPage = 10;

  useEffect(() => {
    // Fetch tick data
    fetch("http://localhost:8000/ticks")
      .then(response => response.json())
      .then(data => setTicksData(data));

    // Fetch bhavcopy data
    fetch("http://localhost:8000/bhavcopy")
      .then(response => response.json())
      .then(data => setBhavcopyData(data));
  }, []);

  const getPaginatedData = (data, page) => {
    const startIndex = (page - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    return data.slice(startIndex, endIndex);
  };

  const placeOrder = async (symbol, price, quantity) => {
    const response = await fetch("http://localhost:8000/place-order", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ symbol, price, quantity })
    });
    const result = await response.json();
    alert(`Order placed: ${result.message}`);
  };

  return (
    <div className="app-container">
      <h1 className="title">Financial Data Dashboard</h1>

      <div className="table-container">
        <h2>Ticks Data</h2>
        <table className="styled-table">
          <thead>
            <tr>
              <th>Symbol</th>
              <th>Timestamp</th>
              <th>Price</th>
              <th>Quantity</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {getPaginatedData(ticksData, ticksPage).map((tick, index) => (
              <tr key={index}>
                <td>{tick.symbol}</td>
                <td>{tick.timestamp}</td>
                <td>{tick.price}</td>
                <td>{tick.quantity}</td>
                <td>
                  <button onClick={() => placeOrder(tick.symbol, tick.price, tick.quantity)}>Place Order</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        <div className="pagination">
          <button
            onClick={() => setTicksPage(t => Math.max(t - 1, 1))}
            className="pagination-button"
          >Previous (Ticks)</button>
          <button
            onClick={() => setTicksPage(t => t + 1)}
            className="pagination-button"
          >Next (Ticks)</button>
        </div>
      </div>

      <div className="table-container">
        <h2>Bhavcopy Data</h2>
        <table className="styled-table">
          <thead>
            <tr>
              <th>Symbol</th>
              <th>Close Price</th>
              <th>Timestamp</th>
            </tr>
          </thead>
          <tbody>
            {getPaginatedData(bhavcopyData, bhavcopyPage).map((bhav, index) => (
              <tr key={index}>
                <td>{bhav.symbol}</td>
                <td>{bhav.close_price}</td>
                <td>{bhav.timestamp}</td>
              </tr>
            ))}
          </tbody>
        </table>
        <div className="pagination">
          <button
            onClick={() => setBhavcopyPage(p => Math.max(p - 1, 1))}
            className="pagination-button"
          >Previous (Bhavcopy)</button>
          <button
            onClick={() => setBhavcopyPage(p => p + 1)}
            className="pagination-button"
          >Next (Bhavcopy)</button>
        </div>
      </div>
    </div>
  );
}

export default App;