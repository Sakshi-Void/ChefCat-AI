const Help = () => (
  <div className="p-6 max-w-3xl mx-auto">
    <h1 className="text-2xl font-bold mb-6 text-gray-800 dark:text-gray-100">
      🛟 Help & Usage Guide
    </h1>
    <ul className="list-disc list-inside space-y-3 text-gray-700 dark:text-gray-300 leading-relaxed">
      <li>
        💬 <strong>AI Chat</strong>: Ask questions or get intelligent responses from ChefCat.
      </li>
      <li>
        📁 <strong>Documents</strong>: Upload PDFs and ask context-aware questions.
      </li>
      <li>
        📜 <strong>History</strong>: Browse your previous conversations.
      </li>
      <li>
        ⚙️ <strong>Settings</strong>: Toggle between dark and light themes.
      </li>
    </ul>
  </div>
);

export default Help;
