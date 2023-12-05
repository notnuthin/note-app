document.addEventListener("DOMContentLoaded", function() {
    function handleSearch() {
        console.log("search triggered");
        var query = document.getElementById("searchInput").value;
        // Append the query to the URL as a parameter
        var url = '/search?search_expression=' + encodeURIComponent(query);
        fetch(url, {
            method: "GET",
            headers: {
                "Content-Type": "application/json"
            },
        })
        .then((response) => response.json())
        .then((data) => {
            if (data.result == null) {
                alert("Can't find note!");
            } else {
                window.open(data.result);
            }
        })
        .catch((error) => {
            console.error("Error:", error);
        });
    }
    
    // Event listener for the search button click
    var searchButton = document.getElementById("searchButton");
    searchButton.addEventListener("click", handleSearch);
    
    // Event listener for "Enter" key press
    var searchInput = document.getElementById("searchInput");
    searchInput.addEventListener("keypress", function(event) {
        if (event.key === 'Enter') {
            handleSearch();
        }
    });
});