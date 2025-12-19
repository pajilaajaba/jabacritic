import React, { useState, useContext } from 'react'; 
import api from '../api/axios'; 
import { AuthContext } from '../context/AuthContext'; // импортируем Контекст
import { Link } from 'react-router-dom';
import toast from 'react-hot-toast';

// используем пропс gameId
const ReviewForm = ({ gameId, onReviewSuccess }) => {
    // Исправлено: Достаем isAuthenticated через хук
    const { isAuthenticated } = useContext(AuthContext);

    const [rating, setRating] = useState(10);
    const [description, setDescription] = useState('');
    const [platform, setPlatform] = useState(1); // по умолчанию PC айди = 1

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await api.post('/reviews/', {
                game: gameId,
                rating: rating,
                description: description,
                platform: platform 
            });
            toast.success("Отзыв успешно опубликован! 🎉");
            if (onReviewSuccess) {onReviewSuccess();}
            setDescription(''); // Очищаем поле после отправки
        } catch (error) {
            console.error('Ошибка при передаче данных', error);
            toast.error("Ошибка! Возможно, вы уже оставляли отзыв.");
        }
    };

    return (
        <div className="bg-white p-6 rounded-lg shadow-md mt-6">
            <h2 className="text-xl font-bold mb-4">Оставить отзыв</h2>
            
            {isAuthenticated ? (
                <form onSubmit={handleSubmit} className="flex flex-col gap-4">
                    
                    {/* 1. Рейтинг */}
                    <div>
                        <label className="block text-sm font-bold mb-1">Оценка (0-100):</label>
                        <input
                            type='number'
                            min='0' max='100'
                            className='p-2 border rounded w-24'
                            value={rating} 
                            onChange={e => setRating(e.target.value)}
                        />
                    </div>

                    {/* 2. Платформа (SELECT) */}
                    <div>
                        <label className="block text-sm font-bold mb-1">Платформа:</label>
                        <select 
                            className='p-2 border rounded w-full bg-white'
                            value={platform}
                            onChange={e => setPlatform(e.target.value)}
                        >
                            <option value="1">PC</option>
                            <option value="2">PlayStation 5</option>
                            <option value="3">PlayStation 4</option>
                            <option value="4">Xbox Series X/S</option>
                            <option value="5">Xbox One</option>
                            <option value="6">Nintendo Switch</option>
                        </select>
                    </div>

                    {/* 3. Текст */}
                    <textarea
                        placeholder='Расскажи о своих впечатлениях...'
                        className='p-2 border rounded h-24'
                        value={description} 
                        onChange={e => setDescription(e.target.value)}
                    />

                    <button type="submit" className="bg-blue-600 text-white p-2 rounded hover:bg-blue-700 font-bold">
                        Опубликовать
                    </button>
                </form>
            ) : (
                <div className="text-center p-4 bg-gray-50 rounded border"> 
                    <p className="mb-2">Только авторизованные пользователи могут писать отзывы.</p>
                    <Link to='/login' className="text-blue-600 underline font-bold">Войти в аккаунт</Link>
                </div>
            )} 
        </div>
    );
};

export default ReviewForm;