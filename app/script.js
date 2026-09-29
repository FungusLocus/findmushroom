
const map = L.map("map").setView([60.2, 25.0], 11);

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution: "&copy; OpenStreetMap contributors",
  maxZoom: 18,
}).addTo(map);



const statusEl = document.getElementById("status");
const selectEl = document.getElementById("species-select");
const buttonEl = document.getElementById("show-predictions-btn");

