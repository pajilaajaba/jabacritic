import { Link } from 'react-router-dom';

const GameCard = ({game})=>{
    return (
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
                );
}

export default GameCard;