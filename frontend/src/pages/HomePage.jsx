import React, { useEffect, useState } from 'react';
import api from '../api/axios'
import { Link } from 'react-router-dom';

import GameCard from '../components/GameCard';

const HomePage = () => {
    const [games, setGames] = useState([]);
    useEffect(() => {
        api.get('/games/')
            .then(response => {
                console.log("Данные от Django:", response.data);
                
                // проверяем: если пришел массив (список), сохраняем его
                // DRF обычно возвращает объект { count: 10, results: [...] }
                if (response.data.results) {
                    setGames(response.data.results);
                } else if (Array.isArray(response.data)) {
                    setGames(response.data);
                } else {
                    console.error("Сервер вернул не список, а что-то странное:", response.data);
                }
            })
            .catch(error => {
                console.error("Ошибка при загрузке игр:", error);
            });
    }, []);

     return (
        <div>
            <h1>Каталог игр</h1>
            
            {/* Сетка игр */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: '20px' }}>
                {games.map(game => ( <GameCard game={game} key={game.id} />))}
            </div>
        </div>
    );
};

export default HomePage;