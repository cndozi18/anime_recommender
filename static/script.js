const delay = ms => new Promise(res => setTimeout(res, ms));

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

    resultsContainer.innerHTML = '<div class="loader"></div>';


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

async function displayResults(data) {

    resultsContainer.innerHTML = '';

    if (data.error) {
        resultsContainer.innerHTML = `<p class="error">${data.error}</p>`;
        return;
    }
    
    if (data.length === 0) {
        resultsContainer.innerHTML = '<p>No recommendations found for this title.</p>';
        return;
    }

    const listHeader = document.createElement('h2');
    listHeader.textContent = "Here are your recommendations:";
    resultsContainer.appendChild(listHeader);


    for (const animeTitle of data) {

        try {
            const jikanResponse = await fetch(`https://api.jikan.moe/v4/anime?q=${encodeURIComponent(animeTitle)}&limit=1`);
            const jikanData = await jikanResponse.json();
            
            let imageUrl = 'https://via.placeholder.com/225x318.png?text=No+Image';
            if (jikanData.data && jikanData.data.length > 0) {
                imageUrl = jikanData.data[0].images.jpg.image_url;
            }
            

            const animeCard = document.createElement('div');
            animeCard.classList.add('anime-card');
            

            animeCard.innerHTML = `
                <img src="${imageUrl}" alt="${animeTitle} Poster">
                <div class="anime-info">
                    <h3>${animeTitle}</h3>
                </div>
            `;
            
            resultsContainer.appendChild(animeCard);

            await delay(500);

        } catch (error) {
            console.error(`Failed to fetch details for ${animeTitle}:`, error);

            const errorCard = document.createElement('div');
            errorCard.classList.add('anime-card');
            errorCard.innerHTML = `<p>${animeTitle} (Could not load image)</p>`;
            resultsContainer.appendChild(errorCard);
        }
    }
}
    
    