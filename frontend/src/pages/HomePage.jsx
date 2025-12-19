import React, { useEffect, useState } from 'react';
import api from '../api/axios';
import { Link } from 'react-router-dom';
import GameCard from '../components/GameCard';

const HomePage = () => {
    const [popularGames, setPopularGames] = useState([]);
    const [newGames, setNewGames] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Загружаем данные параллельно
        const fetchData = async () => {
            try {
                const [popRes, newRes] = await Promise.all([
                    api.get('/games/?ordering=-average_rating'),
                    api.get('/games/?ordering=-release_date')
                ]);

                // Обработка популярных
                const popData = popRes.data.results || popRes.data;
                setPopularGames(popData.slice(0, 4));

                // Обработка новинок
                const newData = newRes.data.results || newRes.data;
                setNewGames(newData.slice(0, 4));
            } catch (error) {
                console.error("Ошибка загрузки главной:", error);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    if (loading) return <div className="text-center mt-20 text-gray-500">Загрузка витрины...</div>;

    return (
        <div className="space-y-16 pb-12">
            
            {/* --- HERO SECTION (Минимализм) --- */}
            <div className="text-center py-20 border-b border-gray-200">
                <h1 className="text-6xl md:text-8xl font-black text-gray-900 tracking-tighter mb-4">
                    Jaba<span className="text-green-600">Critic</span>
                </h1>
                <p className="text-xl md:text-2xl text-gray-500 font-light max-w-2xl mx-auto">
                    Играй. Оценивай. Обсуждай.
                </p>
                
                <div className="mt-8">
                    <Link 
                        to="/catalog" 
                        className="inline-block px-8 py-3 rounded-full bg-gray-900 text-white font-bold hover:bg-gray-700 transition transform hover:-translate-y-1 shadow-lg"
                    >
                        Открыть каталог
                    </Link>
                </div>
            </div>

            {/* --- СЕКЦИЯ 1: ЛУЧШЕЕ --- */}
            <section>
                <div className="flex items-center justify-between mb-8 px-2">
                    <div>
                        <h2 className="text-3xl font-bold text-gray-900">Выбор критиков</h2>
                        <p className="text-gray-500 text-sm mt-1">Игры с самым высоким рейтингом за всё время</p>
                    </div>
                    <Link to="/catalog?ordering=-average_rating" className="text-green-600 font-semibold hover:underline">
                        Смотреть все &rarr;
                    </Link>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
                    {popularGames.map(game => (
                        <GameCard key={game.id} game={game} />
                    ))}
                </div>
            </section>

            {/* --- СЕКЦИЯ 2: НОВИНКИ --- */}
            <section>
                <div className="flex items-center justify-between mb-8 px-2">
                    <div>
                        <h2 className="text-3xl font-bold text-gray-900">Свежие релизы</h2>
                        <p className="text-gray-500 text-sm mt-1">То, во что играют прямо сейчас</p>
                    </div>
                    <Link to="/catalog?ordering=-release_date" className="text-green-600 font-semibold hover:underline">
                        Смотреть все &rarr;
                    </Link>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
                    {newGames.map(game => (
                        <GameCard key={game.id} game={game} />
                    ))}
                </div>
            </section>

        </div>
    );
};

export default HomePage;