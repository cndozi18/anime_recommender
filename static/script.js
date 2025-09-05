const searchBtn = document.getElementById('search-btn');
const animeTitleInput = document.getElementById('anime-title-input');
const resultsContainer = document.getElementById('results-container');

searchBtn.addEventListener('click', getRecommendations);

async function getRecommendations() {
    const animeTitle = animeTitleInput.value;
    
    if (!animeTitle) {
        alert("Please enter an anime title.");
        return; 
    }

    resultsContainer.innerHTML = '<p class="loading">Finding recommendations...</p>';


    try {
    const response = await fetch(`/recommend?title=${encodeURIComponent(animeTitle)}`);
    const data = await response.json();

    displayResults(data);

    } catch (error) {
        console.error("Fetch error:", error);
        resultsContainer.innerHTML = '<p class="error">Could not fetch recommendations. Is the server running?</p>';
    }
    console.log("Received from API:", recommendations);
}

function displayResults(data) {
    resultsContainer.innerHTML = '';

    if (data.error) {
        resultsContainer.innerHTML = `<p class="error">${data.error}</p>`;
    } 
    else if (data.length === 0) {
        resultsContainer.innerHTML = '<p>No recommendations found for this title.</p>';
    } 

    else {
        const listHeader = document.createElement('h2');
        listHeader.textContent = "Here are your recommendations:";
        resultsContainer.appendChild(listHeader);

        data.forEach(animeTitle => {

            const animeElement = document.createElement('p');
            animeElement.classList.add('recommendation-item'); // Add a class for styling
            animeElement.textContent = animeTitle;
            
            resultsContainer.appendChild(animeElement);
        });
    }
}
    
    