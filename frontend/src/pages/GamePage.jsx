import React, { useEffect, useState} from 'react';
import axios from 'axios';
import api from '../api/axios'
import { useParams } from 'react-router-dom';


const GamePage = () => {
    const {id} = useParams();
    const [game, setGame] = useState(null);

    useEffect(()=>{
        api.get(`/games/${id}/`)
        .then(response => setGame(response.data))
        .catch(error => {console.error("ошибка при получении игры"), error});
    }, [id]);
    

    if (!game) {
        return <div> Загрузка подождите...</div>
    }

    return (
        <div>
            <h1 className="text-red-600 text-4xl font-bold">{game.title}</h1>

            {game.image? 
                (<img 
                    src = {game.image}
                    alt = {game.title}
                    style={{ maxWidth: '500px', borderRadius: '10px' }}
                />
            ):(
                 <div style={{ width: '300px', height: '200px', background: '#ccc' }}>Нет фото</div>
            )}

            <h2> Описание игры:{game.description}</h2>
            <h2> Разработчик игры:{game.developer?.name}</h2>
            <h2> Издатель игры:{game.publisher?.name}</h2>
            <h2>Жанры: {(game.genres || []).map(g => g.name).join(', ')}</h2>
            <h2>Средний рейтинг: {game.average_rating}</h2>
        </div>
    )
};


export default GamePage;