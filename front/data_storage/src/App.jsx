import "./App.css";
import AuthForm from "./auth/auth";
import { useState } from "react";
import UploadFile from "./upload/upload";

export const App = () => {
  const [token, setToken] = useState(null);

  if (!token) {
    return <AuthForm onLogin={setToken} />;
  }

  return (
    <div className="App">
      <UploadFile token={token} />
    </div>
  );
};
