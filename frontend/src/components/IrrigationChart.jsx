import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
} from "recharts";

function IrrigationChart({ data }) {
  return (
    <div style={{ width: "100%", height: 300 }}>
      <h3>Irrigation Over Time</h3>

      <ResponsiveContainer>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis
            dataKey="step"
            label={{ value: "Step", position: "insideBottom" }}
          />
          <YAxis
            label={{ value: "mm/day", angle: -90, position: "insideLeft" }}
          />
          <Tooltip />
          <Line
            type="monotone"
            dataKey="irrigation"
            stroke="#2e7d32"
            strokeWidth={2}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

export default IrrigationChart;
