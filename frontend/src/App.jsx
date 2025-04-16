import "./App.css";
import PDFViewer from "./components/PDFViewer/PDFViewer";

function App() {
  return (
    <div className="app">
      <header className="app-header">
        <h1>PDF Content Viewer</h1>
      </header>
      <main>
        <PDFViewer />
      </main>
    </div>
  );
}

export default App;
