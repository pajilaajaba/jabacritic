import { useState, useEffect } from "react";
import api from "../api/axios";
import { useParams } from 'react-router-dom';
import GameCard from "../components/GameCard";

const CompanyPage = () => {
    const [company, setCompany] = useState(null); 
    const [games, setGames] = useState([]);
    const { id } = useParams();

    useEffect(() => {
        // 1. хагрузка компании
        api.get(`/companies/${id}/`)
            .then(response => {
                setCompany(response.data);
            })
            .catch(error => console.error('Ошибка при загрузке компании', error));

        // 2. загрузка игр
        api.get(`/games/?developer=${id}`) 
            .then(response => {
                console.log("Игры разработчика:", response.data);
                if (response.data.results) {
                    setGames(response.data.results);
                } else if (Array.isArray(response.data)) {
                    setGames(response.data);
                }
            })
            .catch(error => {
                console.error("Ошибка при загрузке игр:", error);
            });
            
    }, [id]);

    if (!company) {
        return <div className="p-4 text-center">Загрузка...</div>;
    }

    return (
        <div className="container mx-auto p-4">
            <div className="bg-gray-100 p-6 rounded-lg mb-8 shadow-sm">
                <h1 className="text-3xl font-bold mb-2 text-gray-800">{company.name}</h1>
                <p className="text-gray-600 mb-4">{company.description || "Описание отсутствует"}</p>
                
                <div className="inline-block bg-green-100 text-green-800 px-3 py-1 rounded-full font-bold text-sm">
                    Всего игр: {games.length}
                </div>
            </div>

            {/* Сетка игр */}
            <div>
                <h2 className="text-2xl font-bold text-gray-800 mb-6 border-b pb-2">Игры студии</h2>
                
                {games.length > 0 ? (
                    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
                        {games.map(game => (
                            <GameCard game={game} key={game.id} />
                        ))}
                    </div>
                ) : (
                    <p className="text-gray-500">У этой компании пока нет игр в нашей базе.</p>
                )}
            </div>
        </div>
    );
}

export default CompanyPage;