const SUPABASE_URL = "https://qyzvutgfjvxbuytdhvdk.supabase.co";
const SUPABASE_ANON_KEY = "sb_publishable_73YbzaOhXM-sw8Y3z0-4Mw_cKymXiqq";

const db = window.supabase.createClient(
  SUPABASE_URL,
  SUPABASE_ANON_KEY
);

console.log("Script loaded");
console.log(window.supabase);


const map = L.map("map").setView([60.2, 25.0], 11);

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution: "&copy; OpenStreetMap contributors",
  maxZoom: 18,
}).addTo(map);


const statusEl = document.getElementById("status");
const selectEl = document.getElementById("species-select");
const buttonEl = document.getElementById("show-predictions-btn");

