import { Canvas, useFrame } from "@react-three/fiber";
import { OrbitControls } from "@react-three/drei";
import { useRef } from "react";

/* ------------------ SOIL ------------------ */
function Soil({ moisture }) {
  // moisture expected in range [0, 1]
  const color =
    moisture < 0.3
      ? "#c2a679" // dry soil
      : moisture < 0.7
      ? "#8d6e63" // optimal moisture
      : "#4fc3f7"; // wet soil

  return (
    <mesh position={[0, -0.5, 0]}>
      <boxGeometry args={[3, 1, 3]} />
      <meshStandardMaterial color={color} />
    </mesh>
  );
}

/* ------------------ CROP ------------------ */
function Crop({ stage }) {
  // stage expected in range [0, 1]
  const ref = useRef();
  const targetHeight = 0.5 + stage * 2.0;

  // Smooth growth animation
  useFrame(() => {
    if (ref.current) {
      ref.current.scale.y += (targetHeight - ref.current.scale.y) * 0.08;
    }
  });

  return (
    <mesh ref={ref} scale={[1, 1, 1]} position={[0, targetHeight / 2, 0]}>
      <cylinderGeometry args={[0.15, 0.15, 1, 16]} />
      <meshStandardMaterial color="#4caf50" />
    </mesh>
  );
}

/* ------------------ DIGITAL TWIN ------------------ */
function DigitalTwin({ soilMoisture, cropStage }) {
  return (
    <div style={{ height: "320px", width: "100%" }}>
      <h3>🌱 Digital Crop Twin</h3>

      <p style={{ fontSize: "14px" }}>
        Soil Moisture: {(soilMoisture * 100).toFixed(1)}% <br />
        Crop Stage: {(cropStage * 100).toFixed(1)}%
      </p>

      <Canvas camera={{ position: [4, 4, 4] }}>
        <ambientLight intensity={0.5} />
        <directionalLight position={[5, 5, 5]} />

        <Soil moisture={soilMoisture} />
        <Crop stage={cropStage} />

        <OrbitControls enableZoom={false} />
      </Canvas>
    </div>
  );
}

export default DigitalTwin;
