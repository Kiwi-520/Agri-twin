function ExplanationBox({ reasons }) {
  return (
    <div className="explanation-box">
      <h3>📋 Why This Decision?</h3>
      <ul>
        {reasons.map((r, i) => (
          <li key={i}>{r}</li>
        ))}
      </ul>
    </div>
  );
}
export default ExplanationBox;
