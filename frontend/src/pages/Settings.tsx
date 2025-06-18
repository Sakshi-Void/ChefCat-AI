const Settings = () => {
  return (
    <div className="p-6 max-w-2xl mx-auto bg-white dark:bg-gray-800 rounded-2xl shadow-md">
      <h2 className="text-2xl font-bold mb-4 text-gray-900 dark:text-white">⚙️ App Settings</h2>
      <p className="text-gray-600 dark:text-gray-300">
        Theme toggle is available in the sidebar. More settings coming soon!
      </p>

      <div className="flex items-center mt-6 space-x-4">
        <span className="text-gray-700 dark:text-gray-300">Preview Mode:</span>
        <button className="bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-white px-4 py-2 rounded hover:bg-gray-300 dark:hover:bg-gray-600">
          Toggle Theme
        </button>
      </div>
    </div>
  );
};

export default Settings;
