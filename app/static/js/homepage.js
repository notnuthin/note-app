document.addEventListener("DOMContentLoaded", function() {
    var searchButton = document.getElementById("searchButton");

    searchButton.addEventListener("click", function() {
        console.log("button clicked");
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
        .then((data => {
            if (data.result == null){
                alert("Can't find note!")
            } else {
                window.open(data.result)
            }
        }))
        .catch((error) => {
            console.error("Error:", error);
        });
    });
});