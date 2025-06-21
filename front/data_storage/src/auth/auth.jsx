import React, { useState } from "react";
import { registerUser, loginUser } from "../api/htmlHttpRequest";

export default function AuthForm({ onLogin }) {
  const [isRegister, setIsRegister] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);

  const toggleMode = () => {
    setError(null);
    setIsRegister(!isRegister);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    try {
      if (isRegister) {
        await registerUser(email, password);
        alert("Регистрация успешна! Теперь войдите.");
        setIsRegister(false);
        setPassword("");
      } else {
        const token = await loginUser(email, password);
        onLogin(token);
      }
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div style={{ maxWidth: 320, margin: "auto" }}>
      <h2>{isRegister ? "Регистрация" : "Вход"}</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="email"
          placeholder="Email"
          required
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          style={{ width: "100%", marginBottom: 8 }}
        />
        <input
          type="password"
          placeholder="Пароль"
          required
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          style={{ width: "100%", marginBottom: 8 }}
        />
        {error && <div style={{ color: "red", marginBottom: 8 }}>{error}</div>}
        <button type="submit" style={{ width: "100%", marginBottom: 8 }}>
          {isRegister ? "Зарегистрироваться" : "Войти"}
        </button>
      </form>
      <button
        onClick={toggleMode}
        style={{
          width: "100%",
          background: "none",
          border: "none",
          color: "blue",
          cursor: "pointer",
        }}
      >
        {isRegister
          ? "Уже есть аккаунт? Войти"
          : "Нет аккаунта? Зарегистрироваться"}
      </button>
    </div>
  );
}
