export function getNextStep() {
  return {
    soil_moisture: Math.random() * 10,
    heat_stress: 28,
    rainfall: 10,
    crop_stage: "Vegetative",
    crop_height: Math.random() * 10,
    irrigation_mm: 15 + Math.random() * 10,
    explanation: [
      "Soil moisture is moderate",
      "Heat stress is increasing",
      "Rainfall contribution is low",
      "Crop is in a sensitive growth stage",
    ],
  };
}

