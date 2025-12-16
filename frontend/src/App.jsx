import React from 'react';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';

function App() {
  return (
    <BrowserRouter>
      <nav style={{ padding: '10px', background: '#eee', marginBottom: '20px' }}>
        <Link to="/" style={{ marginRight: '15px' }}>Главная</Link>
        <Link to="/login" style={{ marginRight: '15px' }}>Войти</Link>
        <Link to="/register">Зарегистрироваться</Link>
      </nav>


        <Routes>
        <Route path = '/' element = {<HomePage/>}/>
          <Route path = '/login' element = {<LoginPage/>}/>
          <Route path = '/register' element = {<RegisterPage/>}/>
        </Routes>
    </BrowserRouter>
  );
}

export default App;