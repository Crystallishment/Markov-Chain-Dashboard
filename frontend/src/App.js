import { useState } from "react";

function App() {
  const [result, setResult] = useState(null);
  const [dragging, setDragging] = useState(false);

  const handleDrop = async (e) => {
    e.preventDefault();
    setDragging(false);
    const file = e.dataTransfer.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch("http://localhost:8080/upload", {
      method: "POST",
      body: formData,
    });
    const data = await res.json();
setResult(data);
if (data.message === 'completed') {
  window.location.href = 'http://localhost:8050';
}
  };

  return (
    <div style={{ padding: "50px", textAlign: "center" }}>
      <h1>上传跳转数据</h1>
      <div
        onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
        onDragLeave={() => setDragging(false)}
        onDrop={handleDrop}
        style={{
          border: `2px dashed ${dragging ? "blue" : "gray"}`,
          padding: "50px",
          borderRadius: "10px",
          cursor: "pointer",
        }}
      >
        拖拽 CSV 文件到这里
      </div>
      {result && <pre>{JSON.stringify(result, null, 2)}</pre>}
    </div>
  );
}

export default App;