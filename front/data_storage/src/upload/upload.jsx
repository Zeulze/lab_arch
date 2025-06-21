// src/components/UploadFile.jsx
import React, { useState } from "react";

export default function UploadFile({ token }) {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setMessage("");
  };

  const handleUpload = async () => {
    if (!file) {
      setMessage("Выберите файл для загрузки");
      return;
    }
    setLoading(true);
    setMessage("");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://localhost/file/upload/", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formData,
      });

      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || "Ошибка загрузки");
      }

      const data = await res.json();
      setMessage(`Файл "${data.filename}" успешно загружен!`);
      setFile(null);
    } catch (err) {
      setMessage(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 400, margin: "auto" }}>
      <h3>Загрузка файла</h3>
      <input type="file" onChange={handleFileChange} />
      <button
        onClick={handleUpload}
        disabled={loading}
        style={{ marginTop: 10 }}
      >
        {loading ? "Загрузка..." : "Загрузить"}
      </button>
      {message && <p style={{ marginTop: 10 }}>{message}</p>}
    </div>
  );
}
