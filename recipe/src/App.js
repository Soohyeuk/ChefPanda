import { useEffect, useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Saved from "./pages/Saved";
import AddRecipe from "./pages/AddRecipe";
import RecipeDetail from "./pages/RecipeDetail";
import { RecipesProvider } from "./context/RecipesContext";
import SleepWarningModal from "./components/ui/SleepWarningModal";

function App() {
  const [showWarning, setShowWarning] = useState(false);

  useEffect(() => {
    setShowWarning(true);
  }, []);

  return (
    <Router>
      <RecipesProvider>
        <SleepWarningModal
          open={showWarning}
          onClose={() => setShowWarning(false)}
        />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/saved" element={<Saved />} />
          <Route path="/add" element={<AddRecipe />} />
          <Route path="/recipe/:videoId" element={<RecipeDetail />} />
        </Routes>
      </RecipesProvider>
    </Router>
  );
}

export default App;
