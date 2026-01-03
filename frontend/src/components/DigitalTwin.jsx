import { Canvas } from "@react-three/fiber";
import { OrbitControls } from "@react-three/drei";

function Soil({ moisture }) {
  // moisture: 0 → 1
  const color =
    moisture < 0.3
      ? "#c2a679" // dry
      : moisture < 0.7
      ? "#8d6e63" // optimal
      : "#4fc3f7"; // wet

  return (
    <mesh position={[0, -0.5, 0]}>
      <boxGeometry args={[3, 1, 3]} />
      <meshStandardMaterial color={color} />
    </mesh>
  );
}

function Crop({ stage }) {
  // stage: 0 → 1
  const height = 0.5 + stage * 2;

  return (
    <mesh position={[0, height / 2, 0]}>
      <cylinderGeometry args={[0.15, 0.15, height, 16]} />
      <meshStandardMaterial color="#4caf50" />
    </mesh>
  );
}

function DigitalTwin({ soilMoisture, cropStage }) {
  return (
    <div style={{ height: "300px", width: "100%" }}>
      <h3>Digital Crop Twin</h3>

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
