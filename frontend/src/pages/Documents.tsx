import DocumentsUpload from "../components/DocumentsUpload";

const Documents = () => {
  return (
    <div className="p-4 max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-6 text-gray-800 dark:text-gray-100">
        💾 Upload & Query Documents
      </h1>
      <DocumentsUpload />
    </div>
  );
};

export default Documents;
