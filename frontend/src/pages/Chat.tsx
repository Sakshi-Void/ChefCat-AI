import { useEffect, useRef, useState } from "react";
import axiosInstance from "../utils/axiosInstance";
import { ArrowUpCircle } from "lucide-react";
import ChatHistory from "../components/ChatHistory";

interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}

const Chat = () => {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim() || loading) return;

    const userMessage: ChatMessage = { role: "user", content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const res = await axiosInstance.post("/chat/", { message: input });

      const botMessage: ChatMessage = {
        role: "assistant",
        content: (res.data as { response: string }).response,
      };

      setMessages((prev) => [...prev, botMessage]);

      await axiosInstance.post("/history/save", {
        user_id: "guest", 
        user_message: userMessage.content,
        bot_response: botMessage.content,
      });

      const utterance = new SpeechSynthesisUtterance(botMessage.content);
      speechSynthesis.speak(utterance);
    } catch (err) {
      console.error("Chat error:", err);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "⚠️ Failed to get response. Try again." },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="flex h-screen overflow-hidden">
      {/* Sidebar: Chat History */}
      <div className="w-1/3 max-w-xs bg-gray-50 dark:bg-gray-900 border-r border-gray-200 dark:border-gray-700 p-2 overflow-y-auto">
        <ChatHistory onSelect={(msgs) => setMessages(msgs)} />
      </div>

      {/* Main Chat Area */}
      <div className="flex flex-col flex-1">
        <div className="flex-1 overflow-y-auto px-4 py-6 space-y-4">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`max-w-2xl px-4 py-3 rounded-xl whitespace-pre-line shadow-md ${
                msg.role === "user"
                  ? "bg-blue-600 text-white self-end ml-auto"
                  : "bg-gray-200 text-gray-900 dark:bg-gray-700 dark:text-white self-start mr-auto"
              }`}
            >
              {msg.content}
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Box */}
        <div className="bg-white dark:bg-gray-900 p-4 border-t border-gray-300 dark:border-gray-700">
          <div className="flex items-center max-w-3xl mx-auto">
            <input
              type="text"
              placeholder={loading ? "Waiting for reply..." : "Type your message..."}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              disabled={loading}
              className="flex-1 px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-l-lg text-gray-900 dark:text-white dark:bg-gray-800 focus:outline-none disabled:opacity-50"
            />
            <button
              onClick={sendMessage}
              disabled={loading}
              className="bg-purple-600 hover:bg-purple-700 px-4 py-3 rounded-r-lg text-white disabled:opacity-50"
            >
              <ArrowUpCircle className="h-5 w-5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Chat;
