document.addEventListener("DOMContentLoaded", function() {


    // Function to handle search
    function Search() {
        console.log("search triggered");
        var query = document.getElementById("searchInput").value;
        var filter = document.getElementById("filter-dropdown").value;
        console.log(filter)
        // Append the query to the URL as a parameter
        var url = '/search?search_expression=' + encodeURIComponent(query) + '&folder=' + encodeURIComponent(filter)
        fetch(url, {
            method: "GET",
            headers: {
                "Content-Type": "application/json"
            },
        })
        .then((response) => response.json())
        .then((data) => {
            const searchResults = document.getElementById("searchResults");
            searchResults.innerHTML = ""; // Clear previous results
            data.results.forEach((result) => {
                const listItem = document.createElement("li");
                listItem.textContent = result.name; // Adjust to match your result structure
                listItem.addEventListener("click", () => {
                    window.open(result.url) // Open note when clicked
                });
                searchResults.appendChild(listItem);
            });
            if (data.results.length === 0) {
                searchResults.innerHTML = "<li>No results found</li>";
            }
            document.querySelector('.search-dropdown').style.display = 'block'; // Show dropdown
    })  .catch((error) => {
            console.error("Error:", error);
        });
    }

    // Event listener for the search button click
    var searchButton = document.getElementById("searchButton");
    searchButton.addEventListener("click", Search);

    // Event listener for "Enter" key press
    var searchInput = document.getElementById("searchInput");
    searchInput.addEventListener("keypress", function(event) {
        if (event.key === 'Enter') {
            Search();
        }
    });
});