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
    const next = await getNextStep();
    const nextStep = step + 1;

    setStep(nextStep);
    setData(next);

    // irrigation history
    setHistory((prev) => [
      ...prev,
      { step: nextStep, irrigation: next.irrigation_mm },
    ]);

    // explanation logic (human readable)
    const exp = [];

    if (next.soil_moisture < 0.4)
      exp.push("Soil moisture is low → irrigation needed");

    if (next.heat_stress > 0.3)
      exp.push("Heat stress detected → cooling via irrigation");

    if (next.rainfall > 0.05)
      exp.push("Rainfall present → irrigation reduced");

    exp.push(`Fertilizer advice: ${next.fertilizer}`);
    exp.push(next.fertilizer_reason);

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

      {history.length > 0 && (
        <IrrigationChart data={history} />
      )}
    </div>
  );
}

export default Simulation;
