import React, { useEffect, useState } from 'react';
import api from '../api/axios'
import { Link } from 'react-router-dom';

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
                
                {games.map(game => (
                    <div key={game.id} style={{ border: '1px solid grey', borderRadius: '10px', overflow: 'hidden' }}>
                        
                        {/* 1. КАРТИНКА */}
                        {/* Если game.image есть, показываем его. Если нет - цветной квадрат */}
                        {game.image ? (
                            <img 
                                src={game.image} 
                                alt={game.title} 
                                style={{ width: '100%', height: '150px', objectFit: 'cover' }} 
                            />
                        ) : (
                            <div style={{ width: '100%', height: '150px', background: '#ccc' }}>Нет фото</div>
                        )}

                        {/* 2. ТЕКСТ */}
                        <div style={{ padding: '10px' }}>
                            <h3> 
                                <Link to={`/game/${game.id}`}> {game.title} </Link> 
                            </h3>
                            <p>Рейтинг: {game.average_rating || 0}</p>
                        </div>

                    </div>
                ))}
            </div>
        </div>
    );
};

export default HomePage;