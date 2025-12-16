import React, { useEffect, useState } from 'react';
import axios from 'axios';

const HomePage = () => {
    const [games, setGames] = useState([]);

    useEffect(() => {
        // Делаем запрос
        axios.get('/api/v1/games/')
            .then(response => {
                console.log("Данные от Django:", response.data);
                
                // Проверяем: если пришел массив (список), сохраняем его
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
        <div style={{ padding: '20px' }}>
            <h1>Список игр</h1>
            
            {/* Если игр нет, пишем сообщение. Если есть - рисуем список */}
            {games.length === 0 ? (
                <p>Игр пока нет или идет загрузка...</p>
            ) : (
                <div style={{ display: 'grid', gap: '20px' }}>
                    {games.map(game => (
                        <div key={game.id} style={{ border: '1px solid #ccc', padding: '10px', borderRadius: '8px' }}>
                            <h3>{game.title}</h3>
                            <p>{game.description}</p>
                            <small>Рейтинг: {game.rating || 'Нет'}</small>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default HomePage;