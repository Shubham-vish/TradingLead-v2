let allTickers = [];

function fetchAndStoreTickers() {
    const elements = document.querySelectorAll('.symbolNameText-RsFlttSS');
    const newTickers = Array.from(elements).map(el => 'NSE:' + el.textContent.trim());

    // Add new tickers to the global array if they are not already present
    newTickers.forEach(ticker => {
        if (!allTickers.includes(ticker)) {
            allTickers.push(ticker);
        }
    });

    return newTickers; // return the array of new tickers fetched in this run
}

fetchAndStoreTickers()
allTickers.join();
