const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:5000";

export async function resetSimulation() {
  const res = await fetch(`${API_URL}/reset`, {
    method: "POST",
  });
  return await res.json();
}

export async function getNextStep(){
  const res = await fetch(`${API_URL}/step`,{
    method: "POST",
  });
  return await res.json();
}