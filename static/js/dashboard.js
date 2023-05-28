// Function to generate table rows
// function generateTableRows() {
//     let form = document.getElementById("{{ groups }}");
//     let formData = new FormData(form);
//
//     let items = [];
//     for (let value of formData.values()) {
//         items.push(value);
//     }
//
//     let tableBody = document.querySelector("table-body");
//
//     // Clear existing rows
//     tableBody.innerHTML = "";
//
//     // Iterate through each item and create a table row
//     items.forEach(function (item) {
//         let row = document.createElement("tr");
//         let itemCell = document.createElement("td");
//
//         itemCell.textContent = item;
//
//         row.appendChild(itemCell);
//
//         tableBody.appendChild(row);
//     });
// }