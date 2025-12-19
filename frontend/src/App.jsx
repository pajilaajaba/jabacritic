import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

// Импорты страниц
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import GamePage from './pages/GamePage';
import CatalogPage from './pages/CatalogPage';
import ProfilePage from './pages/ProfilePage';
import CompanyPage from './pages/CompanyPage';
import { Toaster } from 'react-hot-toast';

// импорты компонентов
import NavBar from './components/NavBar';
import Footer from './components/Footer';
import { AuthProvider } from './context/AuthContext';

function App() {
  return (
    <BrowserRouter>
      <Toaster
        position="top-center"
        toastOptions={{
          // опции для всех уведомлений
          style: {
            borderRadius: '10px',
            background: '#333',
            color: '#fff',
          },
          // опции конкретно для успеха
          success: {
            iconTheme: {
              primary: '#4ade80',
              secondary: 'black',
            },
          },
        }}
      />
      {/* ГЛАВНЫЙ КОНТЕЙНЕР*/}
      <div className="flex flex-col min-h-screen bg-gray-50 text-gray-900 font-sans">
        
        {/* шапка*/}
        <NavBar />

        {/* основной контент: он будет растягиваться (flex-grow), толкая футер вниз */}
        <main className="flex-grow container mx-auto p-4">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/game/:id" element={<GamePage />} />
            <Route path="/catalog" element={<CatalogPage />} />
            <Route path="/profile" element={<ProfilePage />} />
            <Route path="/user/:id" element={<ProfilePage />} />
            <Route path="/company/:id" element={<CompanyPage />} />
          </Routes>
        </main>

        <Footer />
        
      </div>
    </BrowserRouter>
  );
}

export default App;