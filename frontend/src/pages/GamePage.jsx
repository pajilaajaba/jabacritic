import React, { useEffect, useState} from 'react';
import axios from 'axios';
import api from '../api/axios'
import { useParams } from 'react-router-dom';
import ReviewForm from '../components/ReviewFrom';
import { Link } from 'react-router-dom';

const GamePage = () => {
    const {id} = useParams();
    const [game, setGame] = useState(null);
    const [reviews, setReviews] = useState([]);

    const fetchReviews = () => { //функция для получения отзывов
        api.get(`/reviews/?game=${id}`) 
            .then(response => {
                if (response.data.results) {
                    setReviews(response.data.results);
                } else if (Array.isArray(response.data)) {
                    setReviews(response.data);
                }
            })
            .catch(error => console.error("Ошибка при загрузке отзывов:", error));
    };

    useEffect(()=>{
        api.get(`/games/${id}/`)
        .then(response => setGame(response.data))
        .catch(error => {console.error("ошибка при получении игры"), error});

        fetchReviews();
    }, [id]);
    

    if (!game) {
        return <div> Загрузка подождите...</div>
    }
    const criticReviews = reviews.filter(r => r.is_critic);
    const userReviews = reviews.filter(r => !r.is_critic);
    return (
        <div className="container mx-auto p-4">
        
        {/* ВЕРХНЯЯ ЧАСТЬ */}
        <div className="flex flex-col md:flex-row gap-6 mb-8">
            
            {/* 1. КАРТИНКА (Слева) */}

            <div className="w-full md:w-1/3">
                <img 
                    src={game.image} 
                    className="w-full rounded-lg shadow-lg object-cover" 
                    style={{ maxHeight: '500px' }} // ограничим высоту, чтобы не была гигантской
                    alt = 'Обложки игры нету, скоро появится'
                />
            </div>

            {/* 2. ИНФОРМАЦИЯ (Справа) */}
            <div className="w-full md:w-2/3">
                <h1 className="text-4xl font-bold mb-2 text-gray-900">{game.title}</h1>
                
                <div className="flex items-center gap-4 mb-4">
                    <span className="text-gray-600">{game.release_date}</span>
                    <span className="bg-green-100 text-green-800 px-3 py-1 rounded-full font-bold">
                        Рейтинг: {game.average_rating}
                    </span>
                </div>

                <div className="mb-4">
                    <Link to={`/company/${game.developer.id}`}> {game.developer?.name}  </Link>
                </div>

                <div className="mb-4">
                    <Link to={`/company/${game.publisher.id}`}> {game.publisher?.name}  </Link>
                </div>
                
                {/* ОПИСАНИЕ */}
                <p className="text-gray-700 text-lg leading-relaxed">
                    {game.description}
                </p>

                {/* Кнопка "Оценить" (открывает модалку) */}
                <button className="mt-6 bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700 transition">
                    Написать отзыв
                </button>
            </div>
        </div>

        {/* НИЖНЯЯ ЧАСТЬ (Отзывы)*/}
        <div className="mt-12">
            <h2 className="text-2xl font-bold mb-6 border-b pb-2">Отзывы</h2>

            {/* Сетка из двух колонок для Критиков и Игроков */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                
                {/* Колонка Критиков */}
                  <div>
                     <h3 className="text-xl font-bold text-purple-700 mb-4">Отзывы Критиков</h3>
                     {criticReviews.length > 0 ? criticReviews.map(review => (
                          <div key={review.id} className="bg-purple-50 p-4 rounded mb-4 border-l-4 border-purple-500 shadow-sm">
                              <div className="flex justify-between items-center mb-2">
                                 <span className="font-bold text-purple-900">{review.user.username}</span>
                                  <span className="bg-purple-200 text-purple-800 px-2 py-1 rounded font-bold text-sm">
                                      {review.rating}
                                  </span>
                              </div>
                             <p className="text-gray-700">{review.description}</p>
                        </div>
                    )) : <p className="text-gray-500">Критики пока молчат...</p>}
                </div>

                {/* Колонка Игроков */}
                <div>
                     <h3 className="text-xl font-bold text-blue-700 mb-4">Отзывы Игроков</h3>
                     {userReviews.length > 0 ? userReviews.map(review => (
                         <div key={review.id} className="bg-blue-50 p-4 rounded mb-4 border-l-4 border-blue-500 shadow-sm">
                               <div className="flex justify-between items-center mb-2">
                                 <span className="font-bold text-blue-900">{review.user.username}</span>
                                  <span className="bg-blue-200 text-blue-800 px-2 py-1 rounded font-bold text-sm">
                                      {review.rating}
                                 </span>
                             </div>
                             <p className="text-gray-700">{review.description}</p>
                         </div>
                    )) : <p className="text-gray-500">Отзывов пока нет.</p>}
                </div>

            </div>
        </div>

    </div>
    )
};


export default GamePage;