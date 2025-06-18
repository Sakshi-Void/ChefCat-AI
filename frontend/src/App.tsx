import { Routes, Route, Navigate, useLocation } from "react-router-dom";
import { useEffect } from "react";

import Sidebar from "./components/Sidebar";
import Chat from "./pages/Chat";
import Documents from "./pages/Documents";
import Settings from "./pages/Settings";
import Help from "./pages/Help";

const App = () => {
  const location = useLocation();

  useEffect(() => {
    document.documentElement.classList.add("transition-colors", "duration-300");
  }, []);

  const showSidebar = ["/chat", "/documents", "/settings", "/help"].includes(location.pathname);

  return (
    <div className="flex h-screen">
      {showSidebar && <Sidebar />}

      <main className="flex-1 bg-gray-50 dark:bg-gray-950 overflow-y-auto">
        <Routes>
          {/* ✅ Direct Routes - No Protection */}
          <Route path="/chat" element={<Chat />} />
          <Route path="/documents" element={<Documents />} />
          <Route path="/settings" element={<Settings />} />
          <Route path="/help" element={<Help />} />

          {/* ✅ Default redirect */}
          <Route path="*" element={<Navigate to="/chat" />} />
        </Routes>
      </main>
    </div>
  );
};

export default App;
