import { useEffect, useState } from "react";
import { getNextStep } from "../api/backend";
import MetricCard from "../components/MetricCard";

function Dashboard() {
  const [data, setData] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      const res = await getNextStep();
      setData(res);
    };
    fetchData();
  }, []);

  if (!data) return <p>Loading farm state...</p>;

  return (
    <div className="page">
      <h2>Current Farm State</h2>

      <div className="grid">
        <MetricCard label="Soil Moisture" value={data.soil_moisture.toFixed(2)} unit="" />
        <MetricCard label="Heat Stress" value={data.heat_stress.toFixed(2)} unit="" />
        <MetricCard label="Rainfall" value={data.rainfall.toFixed(2)} unit="mm" />
        <MetricCard label="Crop Stage" value={data.crop_stage.toFixed(2)} unit="" />
      </div>
    </div>
  );
}

export default Dashboard;
