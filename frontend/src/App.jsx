import { useContext } from 'react'; 
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import GamePage from './pages/GamePage';
import CompanyPage from './pages/CompanyPage';
import { AuthContext} from './context/AuthContext';

function App() {
  const {isAuthenticated, logout} = useContext(AuthContext);
  return (
     <BrowserRouter>
      <nav style={{ padding: '15px', background: '#333', color: 'white', marginBottom: '20px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        
        {/* Левая часть */}
        <div>
           <Link to="/" style={{ color: 'white', textDecoration: 'none', fontWeight: 'bold' }}>JabaCritic 🐸</Link>
        </div>

        {/* Правая часть */}
        <div>
            
            {isAuthenticated ? (
                <button onClick={logout} style={{ background: 'red', color: 'white', border: 'none', padding: '5px 10px', borderRadius: '4px', cursor: 'pointer' }}>
                    Выйти
                </button>
            ) : (
                // используем фрагмент <> чтобы не ломать верстку
                <> 
                  <Link to="/login" style={{ marginRight: '15px', color: 'white' }}>Войти</Link>
                  <Link to="/register" style={{ background: 'blue', color: 'white', padding: '5px 10px', borderRadius: '4px', textDecoration: 'none' }}>Зарегистрироваться</Link>
                </>
            )}
        </div>

      </nav>

      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/game/:id" element={<GamePage />} />
        <Route path="/company/:id" element={<CompanyPage/>} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;