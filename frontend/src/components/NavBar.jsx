import React, { useContext, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom'; // useNavigate для поиска
import { AuthContext } from '../context/AuthContext';

const NavBar = () => {
    const { isAuthenticated, logout } = useContext(AuthContext);
    const [search, setSearch] = useState('');
    const navigate = useNavigate();

    const handleSearch = (e) => {
        e.preventDefault();
        navigate(`/catalog?search=${search}`);
        setSearch(''); // Очищаем поле
    };

    return (
        <nav className="bg-gray-900 text-white shadow-lg sticky top-0 z-50">
            <div className="container mx-auto px-4 py-3 flex justify-between items-center">
                
                {/* ЛОГОТИП */}
                <Link to="/" className="flex items-center gap-2 hover:opacity-80 transition">
                    <img src="/public/jaba-logo.avif" className="w-10 h-10" />
                    <div className="flex flex-col leading-tight">
                        <span className="text-xl font-bold tracking-wider">JabaCritic</span>
                        <span className="text-xs text-green-400 uppercase tracking-widest">Games</span>
                    </div>
                </Link>

                {/* ПОИСК */}
                <form onSubmit={handleSearch} className="hidden md:flex flex-grow max-w-md mx-8">
                    <input 
                        type="text" 
                        placeholder="Найти игру..." 
                        className="w-full px-4 py-2 rounded-l-full text-gray-900 focus:outline-none focus:ring-2 focus:ring-green-500"
                        value={search}
                        onChange={(e) => setSearch(e.target.value)}
                    />
                    <button type="submit" className="bg-green-600 px-6 py-2 rounded-r-full hover:bg-green-700 transition">
                        🔍
                    </button>
                </form>

                {/* КНОПКИ */}
                <div className="flex items-center gap-4">
                    <Link to="/catalog" className="text-gray-300 hover:text-white font-medium transition">
                        Каталог
                    </Link>

                    {isAuthenticated ? (
                        <div className="flex items-center gap-4">
                            <Link to="/profile" className="hover:text-green-400 transition">
                                Профиль
                            </Link>
                            <button 
                                onClick={logout} 
                                className="border border-red-500 text-red-500 px-4 py-1 rounded-full hover:bg-red-500 hover:text-white transition text-sm"
                            >
                                Выйти
                            </button>
                        </div>
                    ) : (
                        <div className="flex gap-2">
                            <Link to="/login" className="px-4 py-2 hover:text-green-400 transition">
                                Войти
                            </Link>
                            <Link to="/register" className="bg-green-600 text-white px-4 py-2 rounded-full hover:bg-green-700 transition shadow-lg">
                                Регистрация
                            </Link>
                        </div>
                    )}
                </div>
            </div>
        </nav>
    );
};

export default NavBar;