import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import GameCard from '../components/GameCard';
import api from '../api/axios';
import { useParams } from 'react-router-dom';
import ReviewCard from '../components/ReviewCard'; 

const ProfilePage = () => {
    const [profile, setProfile] = useState(null);
    const {id} = useParams();
    
    useEffect(() =>{

        const endpoint = id ? `/users/${id}/` : '/users/me/';

        api.get(endpoint, { baseURL: '/api/auth' })
            .then(resp => {
                setProfile(resp.data);
            })
            .catch(error => console.error('Ошибка при загрузке данных пользователя', error));

    }, [id]);

    if (!profile) {return (<div> загрузка профиля</div>)}

    const dateJoined = new Date(profile.date_joined).getFullYear();
    return (
        <div className="container mx-auto p-4">
            
            <div className="bg-white rounded-xl shadow-md p-6 mb-8 flex flex-col md:flex-row items-center gap-6">
                <div className="w-32 h-32 rounded-full overflow-hidden border-4 border-blue-100 flex-shrink-0">
                    <img 
                        src="https://via.placeholder.com/150" 
                        alt="Avatar" 
                        className="w-full h-full object-cover"
                    />
                </div>

                {/* Инфо */}
                <div className="text-center md:text-left">
                    <h1 className="text-3xl font-bold text-gray-800">
                        {profile.username}
                    </h1>
                    <p className="text-gray-500 mt-1">
                        {profile.email}
                    </p>
                    <div className="mt-3">
                        <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-medium">
                            {profile.is_critic ? ('Критик'): ('Пользователь')}
                        </span>
                        <span className="ml-2 text-gray-400 text-sm">
                            На сайте с {dateJoined}года
                        </span>
                    </div>
                </div>
            </div>

            {/*ИЗБРАННОЕ*/}
            <div className="mb-12">
                <h2 className="text-2xl font-bold mb-6 border-b pb-2 text-gray-800 flex items-center gap-2">
                    ❤️ Любимые игры
                </h2>
                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
                    {profile.favorite_games && profile.favorite_games.length > 0 ? (profile.favorite_games.map(game => <GameCard game={game} key={game.id} />)) 
                    : (<p>Вы пока ничего не лайкнули</p>)}
                </div>
            </div>

            {/*ОТЗЫВЫ*/}
            <div>
                <h2 className="text-2xl font-bold mb-6 border-b pb-2 text-gray-800 flex items-center gap-2">
                    💬 Мои отзывы
                </h2>

                <div className="grid gap-4">
                    {profile.user_reviews && profile.user_reviews.length > 0 ? (
                        profile.user_reviews.map(review => (
                           //компонент - ReviewCard
                            <ReviewCard key={review.id} review={review} type="profile" />
                        ))
                    ) : (
                        <p className="text-gray-500">Отзывов пока нет...</p>
                    )}
                </div>
            </div>
        </div>
    );
};

export default ProfilePage;