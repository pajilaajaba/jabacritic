import React, { useEffect, useState} from 'react';
import axios from 'axios';
import api from '../api/axios'
import { useParams } from 'react-router-dom';
import ReviewForm from '../components/ReviewForm';
import { Link } from 'react-router-dom';
import ReviewCard from '../components/ReviewCard';
import toast from 'react-hot-toast';

const GamePage = () => {
    const {id} = useParams();
    const [game, setGame] = useState(null);
    const [reviews, setReviews] = useState([]);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [isLike, setIsLike] = useState(false);


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
        .then(response => {
            setGame(response.data);
            setIsLike(response.data.is_favorited); 
        })
        .catch(error => {console.error("ошибка при получении игры"), error});
        fetchReviews();
    }, [id]);

    const handleLike =  (() => {

        const previousState = isLike;
        setIsLike(!isLike);

       api.post(`/games/${id}/like/`)
       .then(resp => {setIsLike(resp.data.status)})
        .catch(err => {
        console.error(err);
        setIsLike(previousState);
        toast.error("Не удалось поставить лайк. Войдите в аккаунт.");
        });
    })
    

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
                <button 
                    onClick={handleLike}
                    className={`mt-6 px-6 py-2 rounded transition border ${
                        isLike 
                        ? "bg-red-50 text-red-600 border-red-200" // Активный лайк
                        : "bg-gray-50 text-gray-500 border-gray-200" // Нет лайка
                    }`}
                >
                    {isLike ? "❤️ В любимых" : "🤍 Добавить в любимые"}
                </button>

                {/* Кнопка "Оценить" (открывает модалку) */}
                <button onClick={() => setIsModalOpen(true)}
                className="mt-6 bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700 transition">
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
                     {criticReviews.length > 0 ? criticReviews.map(review => <ReviewCard key={review.id} review={review} type="game" />
                    ) : <p className="text-gray-500">Критики пока молчат...</p>}
                </div>

                {/* Колонка Игроков */}
                <div>
                     <h3 className="text-xl font-bold text-blue-700 mb-4">Отзывы Игроков</h3>
                     {userReviews.length > 0 ? userReviews.map(review => (
                         <ReviewCard key={review.id} review={review} type="game" />
                    )) : <p className="text-gray-500">Отзывов пока нет.</p>}
                </div>

            </div>
        </div>

    {isModalOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
            {/* Белое окно */}
            <div className="bg-white p-6 rounded-lg shadow-xl w-full max-w-md relative">
                
                {/* Кнопка Закрыть (Крестик) */}
                <button 
                    onClick={() => setIsModalOpen(false)}
                    className="absolute top-2 right-2 text-gray-500 hover:text-red-500 text-2xl"
                >
                    &times;
                </button>

                {/* Форма для отзывов */}
                <ReviewForm 
                    gameId={id} 
                    onReviewSuccess={() => {
                        fetchReviews();      // обновляем список
                        setIsModalOpen(false); // закрываем окно
                    }} 
                />
            </div>
        </div>)}
    </div>
    )
};


export default GamePage;