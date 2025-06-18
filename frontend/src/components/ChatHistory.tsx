import { useEffect, useState } from "react";
import axiosInstance from "../utils/axiosInstance";

interface HistoryItem {
  id: number;
  user_id: string;
  user_message: string;
  bot_response: string;
  timestamp: string;
}

interface Props {
  onSelect: (messages: { role: "user" | "assistant"; content: string }[]) => void;
}

const ChatHistory = ({ onSelect }: Props) => {
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const res = await axiosInstance.get("/history/all/guest");
        setHistory((res.data as HistoryItem[]).reverse());
      } catch (err) {
        setError("⚠️ Failed to load history.");
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchHistory();
  }, []);

  return (
    <div className="space-y-2">
      <h2 className="text-lg font-semibold text-gray-800 dark:text-white mb-2">
        🕒 Recent Chats
      </h2>

      {loading ? (
        <p className="text-gray-500 dark:text-gray-400">⏳ Loading...</p>
      ) : error ? (
        <p className="text-red-600 dark:text-red-400">{error}</p>
      ) : history.length === 0 ? (
        <p className="text-gray-500 dark:text-gray-400">No history found.</p>
      ) : (
        history.map((entry) => (
          <div
            key={entry.id}
            onClick={() =>
              onSelect([
                { role: "user", content: entry.user_message },
                { role: "assistant", content: entry.bot_response },
              ])
            }
            className="cursor-pointer bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-md p-3 shadow-sm hover:bg-gray-100 dark:hover:bg-gray-700 transition"
          >
            <p className="text-xs text-gray-400 dark:text-gray-500 mb-1">
              {new Date(entry.timestamp).toLocaleString()}
            </p>
            <p className="text-sm text-gray-900 dark:text-white font-medium truncate">
               {entry.user_message}
            </p>
            <p className="text-sm text-gray-700 dark:text-gray-300 line-clamp-2">
              🤖 {entry.bot_response}
            </p>
          </div>
        ))
      )}
    </div>
  );
};

export default ChatHistory;
