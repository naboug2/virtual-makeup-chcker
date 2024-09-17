document.getElementById('ingredient-form').addEventListener('submit', async function(event) {
    event.preventDefault();
    
    const ingredient = document.getElementById('ingredient').value;
    
    // Make a POST request to the backend
    const response = await fetch('http://localhost:5000/analyze', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ ingredients: [ingredient] })
    });
    
    const result = await response.json();
    
    // Display the result
    displayResult(result);
});

function displayResult(result) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '';  // Clear previous results
    
    result.forEach(item => {
        const resultItem = document.createElement('div');
        resultItem.classList.add('result-item');
        
        resultItem.innerHTML = `
            <h3>${item.name}</h3>
            <p><strong>Description:</strong> ${item.description || 'No description available'}</p>
            <p><strong>Safety Rating:</strong> ${item.safety_rating || 'N/A'}</p>
            <p><strong>Use Case:</strong> ${item.use_case || 'N/A'}</p>
            <p><strong>Environmental Impact:</strong> ${item.environmental_impact || 'N/A'}</p>
        `;
        
        resultsDiv.appendChild(resultItem);
    });
}
