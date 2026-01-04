import { useEffect, useState } from "react";
import { getNextStep } from "../api/backend";
import ExplanationBox from "../components/ExplanationBox";

function Explanation() {
  const [data, setData] = useState(null);

  useEffect(() => {
    const fetchExplanation = async () => {
      const res = await getNextStep();
      setData(res);
    };
    fetchExplanation();
  }, []);

  if (!data) return <p>Loading explanation...</p>;

  return (
    <div className="page">
      <h2>Why This Decision?</h2>

      <ExplanationBox
        reasons={[
          `Fertilizer: ${data.fertilizer}`,
          data.fertilizer_reason,
          `Irrigation applied: ${data.irrigation_mm.toFixed(2)} mm`,
        ]}
      />
    </div>
  );
}

export default Explanation;
