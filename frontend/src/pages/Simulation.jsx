import { useState } from "react";
import { getNextStep } from "../api/backend";

import ActionCard from "../components/ActionCard";
import StepButton from "../components/StepButton";
import IrrigationChart from "../components/IrrigationChart";
import DigitalTwin from "../components/DigitalTwin";
import ExplanationBox from "../components/ExplanationBox";

function Simulation() {
  const [data, setData] = useState(null);
  const [history, setHistory] = useState([]);
  const [step, setStep] = useState(0);
  const [explanations, setExplanations] = useState([]);

  const runSimulation = async () => {
    const next = await getNextStep(); // fetches from backend
    const nextStep = step + 1;

    setStep(nextStep);
    setData(next);

    // Update irrigation history
    setHistory((prev) => [
      ...prev,
      { step: nextStep, irrigation: next.irrigation_mm },
    ]);

    // Build explanations from backend data
    const exp = [];

    // Use irrigation_reason directly from backend
    if (next.irrigation_reason) {
      exp.push(`💧 Irrigation: ${next.irrigation_reason}`);
    }

    // Fertilizer advice
    if (next.fertilizer) {
      exp.push(`🌱 Fertilizer advice: ${next.fertilizer}`);
    }

    if (next.fertilizer_reason) {
      exp.push(next.fertilizer_reason);
    }

    setExplanations(exp);
  };

  return (
    <div className="page">
      <h2>🌾 Decision Simulation (Daily Control)</h2>

      <StepButton onClick={runSimulation} label="Run Next Day" />

      {data && (
        <>
          <ActionCard irrigation={data.irrigation_mm} />

          <ExplanationBox reasons={explanations} />

          <DigitalTwin
            soilMoisture={data.soil_moisture}
            cropStage={data.crop_stage}
          />
        </>
      )}

      {history.length > 0 && <IrrigationChart data={history} />}
    </div>
  );
}

export default Simulation;
