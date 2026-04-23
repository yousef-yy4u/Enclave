export default function Home() {
  return (
    <main
      style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        height: "100vh",
        flexDirection: "column",
        gap: "8px",
      }}
    >
      <h1 style={{ fontSize: "2rem", color: "var(--accent)" }}>Enclave</h1>
      <p style={{ color: "var(--text-secondary)" }}>
        Local-first Enterprise Knowledge Agent
      </p>
    </main>
  );
}
