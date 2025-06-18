import { useNavigate } from "react-router-dom";

const LogoutButton = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    if (confirm("Are you sure you want to log out?")) {
      localStorage.removeItem("token");  // or localStorage.clear() if needed
      navigate("/login");
    }
  };

  return (
    <button
      onClick={handleLogout}
      className="text-red-600 dark:text-red-400 hover:underline text-sm mt-2"
    >
      Log out
    </button>
  );
};

export default LogoutButton;
