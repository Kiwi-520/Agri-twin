import { useState } from "react";
import { getNextStep } from "../api/backend";
import ActionCard from "../components/ActionCard";
import StepButton from "../components/StepButton";
import IrrigationChart from "../components/IrrigationChart";

function Simulation() {
  const [data, setData] = useState(null);
  const [history, setHistory] = useState([]);
  const [step, setStep] = useState(0);

  const runSimulation = () => {
    const next = getNextStep();
    const nextStep = step + 1;

    setStep(nextStep);
    setData(next);

    setHistory([
      ...history,
      { step: nextStep, irrigation: next.irrigation_mm },
    ]);
  };

  return (
    <div className="page">
      <h2>Decision Simulation</h2>

      <StepButton onClick={runSimulation} />

      {data && <ActionCard irrigation={data.irrigation_mm} />}

      {history.length > 0 && <IrrigationChart data={history} />}
    </div>
  );
}

export default Simulation;
