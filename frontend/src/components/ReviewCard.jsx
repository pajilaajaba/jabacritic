
import { Link } from 'react-router-dom';

// type может быть 'game' (по умолчанию) или 'profile'
const ReviewCard = ({ review, type = 'game' }) => {
    
    // определяем цвет границы в зависимости от оценки (зеленый > 70, красный < 50)
    const borderColor = review.rating >= 70 ? 'border-green-500' : (review.rating < 50 ? 'border-red-500' : 'border-blue-500');
    const bgColor = review.rating >= 70 ? 'bg-green-50' : 'bg-gray-50';

    return (
        <div className={`${bgColor} p-4 rounded-lg border-l-4 ${borderColor} shadow-sm hover:shadow-md transition`}>
            <div className="flex justify-between items-center mb-2">
                
                {/*Или имя юзера, или название игры */}
                {type === 'game' ? (
                    // если мы на странице игры -> показываем Имя Юзера (ссылка на профиль)
                    <Link to={`/user/${review.user?.id}`} className="font-bold text-gray-900 hover:text-blue-600">
                        {review.user?.username}
                    </Link>
                ) : (
                    // если мы в профиле -> показываем Название Игры (ссылка на игру)
                    <Link to={`/game/${review.game?.id}`} className="font-bold text-blue-700 hover:underline">
                        {review.game?.title || "Игра удалена"}
                    </Link>
                )}

                {/* ОЦЕНКА */}
                <span className="bg-white px-2 py-1 rounded font-bold text-sm shadow-sm border">
                    {review.rating}/100
                </span>
            </div>
            
            {/* ТЕКСТ */}
            <p className="text-gray-700 whitespace-pre-wrap">
                {review.description}
            </p>
        </div>
    );
};

export default ReviewCard;