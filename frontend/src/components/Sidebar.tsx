import { Link, useLocation } from "react-router-dom";
import { useEffect, useState } from "react";
import ThemeToggle from "./ui/ThemeToggle";
import LogoutButton from "./ui/LogoutButton"; 
const Sidebar = () => {
  const location = useLocation();
  const [active, setActive] = useState("");

  useEffect(() => {
    setActive(location.pathname);
  }, [location]);

  const navLinks = [
    { name: "🪄 AI Chat", path: "/chat" },
    { name: "💾 Documents", path: "/documents" },
    { name: "⏱ History", path: "/history" },
    { name: "⚙️ Settings", path: "/settings" },
    { name: "❓ Help", path: "/help" },
  ];

  return (
    <aside className="w-56 h-screen flex flex-col justify-between border-r border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 p-4">
      {/* Logo + App name */}
      <div>
        <Link to="/chat" className="flex flex-col items-center mb-6" aria-label="Go to Chat">
          <img
            src="/chefcat-logo.png"
            alt="ChefCat Logo"
            className="w-25 h-25 rounded-full shadow"
          />
          <h1 className="text-lg font-semibold mt-2 text-gray-800 dark:text-gray-100">
            ChefCat AI
          </h1>
        </Link>

        {/* Navigation */}
        <nav className="space-y-1">
          {navLinks.map((link) => (
            <Link
              key={link.name}
              to={link.path}
              className={`block px-3 py-2 rounded-md text-sm font-medium transition ${
                active === link.path
                  ? "bg-indigo-100 dark:bg-indigo-800 text-indigo-700 dark:text-white"
                  : "text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 hover:text-indigo-700 dark:hover:text-white"
              }`}
            >
              {link.name}
            </Link>
          ))}
        </nav>
      </div>

      {/* Bottom controls */}
      <div className="mt-4 flex flex-col items-center space-y-3">
        <ThemeToggle />
        <LogoutButton /> {/* Use your new logout button here */}
      </div>
    </aside>
  );
};

export default Sidebar;
