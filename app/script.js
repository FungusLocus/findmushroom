const SUPABASE_URL = "https://ldsoiaxzcypeqetqrzam.supabase.co"
const SUPABASE_ANON_KEY = "sb_publishable_Iv7DrmXrdqJgoyqd0DC9ZA_Q8FWf2gc"

const db = supabase.createClient(
  SUPABASE_URL,
  SUPABASE_ANON_KEY
);

console.log("Script loaded");
console.log(window.supabase);

proj4.defs("EPSG:3067", "+proj=utm +zone=35 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs");

function getCurrentIsoWeek() {
  const now = new Date();
  const target = new Date(now.valueOf());
  const dayNr = (now.getDay() + 6) % 7;
  target.setDate(target.getDate() - dayNr + 3);
  const firstThursday = new Date(target.getFullYear(), 0, 4);
  const diff = target - firstThursday;
  return 1 + Math.round(diff / (7 * 24 * 60 * 60 * 1000));
}

const CELL_SIZE = 5000;

function cellToLatLngBounds(grid_x, grid_y) {
  const minX = grid_x * CELL_SIZE;
  const minY = grid_y * CELL_SIZE;
  const maxX = minX + CELL_SIZE;
  const maxY = minY + CELL_SIZE;

  const [minLon, minLat] = proj4("EPSG:3067", "EPSG:4326", [minX, minY]);
  const [maxLon, maxLat] = proj4("EPSG:3067", "EPSG:4326", [maxX, maxY]);

  return [[minLat, minLon], [maxLat, maxLon]];}

const map = L.map("map").setView([64.0, 29.0], 6);

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution: "&copy; OpenStreetMap contributors",
  maxZoom: 18,
}).addTo(map);

let predictionLayer = L.layerGroup().addTo(map);

const statusEl = document.getElementById("status");
const selectEl = document.getElementById("species-select");
const buttonEl = document.getElementById("show-predictions-btn");

function probabilityColor(p) {
  const hue = p * 120;
  return `hsl(${hue}, 80%, 45%)`;
}

async function fetchAndRenderPredictions(species) {
  statusEl.textContent = `Loading predictions for ${species}...`;

  const { data, error } = await db
    .from("predictions")
    .select("grid_x, grid_y, probability")
    .eq("species", species)
    .eq("week", getCurrentIsoWeek())
    .gte("probability", 0.2);

  if (error) {
    statusEl.textContent = "Error: " + error.message;
    console.error(error);
    return;
  }
  console.log(data.length);

  predictionLayer.clearLayers();

  predictionLayer.clearLayers();

  data.forEach((row) => {
    const bounds = cellToLatLngBounds(row.grid_x, row.grid_y);
    L.rectangle(bounds, {
      color: probabilityColor(row.probability),
      weight: 0,
      fillColor: probabilityColor(row.probability),
      fillOpacity: 0.6,
    })
      .bindPopup(`Probability: ${(row.probability * 100).toFixed(0)}%`)
      .addTo(predictionLayer);
  });

  statusEl.textContent = `Loaded ${data.length} grid cells for ${species}.`;
}
console.log("buttonEl:", buttonEl);
console.log("selectEl:", selectEl);



buttonEl.addEventListener("click", () => {
  const species = selectEl.value;
  if (!species) {
    statusEl.textContent = "Please select a mushroom first.";
    return;
  }

  const currentWeek = getCurrentIsoWeek();
  const SEASON_START = 20;
  const SEASON_END = 46;

  if (currentWeek < SEASON_START || currentWeek > SEASON_END) {
    statusEl.textContent = `It is not mushroom picking season, come back when the season begins again at week ${SEASON_START}.`;
    return;
  }

  fetchAndRenderPredictions(species);
});

