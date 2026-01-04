function Home() {
  return (
    <div className="page">
      <h1>🌾 Agri-Twin</h1>

      <p>
        <strong>Agri-Twin</strong> is a Reinforcement Learning–driven
        digital twin for intelligent farm management.
      </p>

      <p>
        A PPO-based AI agent continuously observes soil moisture,
        heat stress, rainfall, and crop growth stage, and
        decides <strong>optimal irrigation actions</strong>
        while balancing water efficiency and crop health.
      </p>

      <p>
        Alongside irrigation control, the system provides
        <strong>explainable fertilizer recommendations</strong>
        based on crop stage and stress conditions.
      </p>

      <ul>
        <li>🤖 RL Agent: PPO (continuous control)</li>
        <li>💧 Optimized irrigation decisions</li>
        <li>🌱 Crop growth & stress simulation</li>
        <li>🧪 Fertilization advisory with reasoning</li>
        <li>📊 Real-time visualization & explanations</li>
      </ul>

      <p>
        Use the <strong>Simulation</strong> page to step through
        AI decisions, or the <strong>Dashboard</strong> to
        monitor farm conditions in real time.
      </p>
    </div>
  );
}

export default Home;
