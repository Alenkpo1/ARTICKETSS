document.addEventListener("DOMContentLoaded", function () {
    fetch('/evento/{{id_evento}}')
        .then(response => response.json())
        .then(data => {
            const dataDisplay = document.getElementById("dataDisplay");

            const nameElement = document.createElement("p");
            nameElement.textContent = "Name: " + data.nombre_evento;

            const ageElement = document.createElement("p");
            ageElement.textContent = "Age: " + data.lugar;

            const cityElement = document.createElement("p");
            cityElement.textContent = "City: " + data.lugar;

            dataDisplay.appendChild(nameElement);
            dataDisplay.appendChild(ageElement);
            dataDisplay.appendChild(cityElement);
        })
        .catch(error => console.error("Error fetching JSON data:", error));
});