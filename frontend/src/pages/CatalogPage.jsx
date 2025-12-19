import { useState, useEffect } from 'react';
import api from '../api/axios';
import GameCard from '../components/GameCard';
import { useSearchParams } from 'react-router-dom';

const CatalogPage = () => {
    const [games, setGames] = useState([]);
    const [genresList, setGenresList] = useState([]);
    const [platformsList, setPlatformsList] = useState([]);
    const [ordering, setOrdering] = useState('-created_at');
    //хук для чтения URL (?search=Witcher)
    const [searchParams] = useSearchParams(); 

    const [filters, setFilters] = useState({
        search: '', // изначально пусто, но useEffect может наполнить далее
        genres: '',
        platforms: '',
        min_year: '',
        max_year: ''
    });

    // загрузка жанров платформ
    useEffect(() => {
        api.get('/genres/').then(resp => { setGenresList(resp.data.results || resp.data) });
        api.get('/platforms/').then(resp => { setPlatformsList(resp.data.results || resp.data) });
    }, []);


    useEffect(() => {
        const urlSearch = searchParams.get('search'); // достаем слово из URL
        
        if (urlSearch) {
            setFilters(prev => ({
                ...prev,
                search: urlSearch
            }));
            fetchGames(urlSearch); 
        } else {
            fetchGames();
        }
    }, [searchParams]);
     
    const fetchGames = (overrideSearch = null) => {
        const params = new URLSearchParams();
        params.append('ordering', ordering);

        // берем search либо из аргумента (свежий из URL), либо из стейта
        const currentSearch = overrideSearch !== null ? overrideSearch : filters.search;

        if (currentSearch) params.append('search', currentSearch);
        
        // остальные фильтры берем из стейта
        if (filters.genres) params.append('genres', filters.genres);
        if (filters.platforms) params.append('platforms', filters.platforms);
        if (filters.min_year) params.append('min_year', filters.min_year);
        if (filters.max_year) params.append('max_year', filters.max_year);

        api.get(`/games/?${params.toString()}`)
            .then(response => {
                if (response.data.results) {
                    setGames(response.data.results);
                } else {
                    setGames(response.data);
                }
            })
            .catch(error => { console.error(error) });
    }

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFilters(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        fetchGames();
    }

    return (
        <div className="container mx-auto p-4 flex flex-col md:flex-row gap-6">     
            {/* ЛЕВАЯ КОЛОНКА */}
            <div className="w-full md:w-1/4 bg-white p-4 rounded shadow-lg h-fit">
                <h2 className="text-xl font-bold mb-4">Фильтры</h2>
                
                <form onSubmit={handleSubmit} className="flex flex-col gap-4">
                    
                    <input 
                        name="search"
                        placeholder="Поиск по названию..."
                        className="p-2 border rounded"
                        value={filters.search} 
                        onChange={handleChange}
                    />
                    
                    {/* Сортировка */}
                    <div className="mb-4">
                        <label className="block text-sm font-bold mb-2 text-gray-700">Сортировка</label>
                        <select 
                            value={ordering} 
                            onChange={e => setOrdering(e.target.value)}
                            className="w-full p-2 border rounded bg-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                        >
                            <option value="-created_at">Сначала новые (добавление)</option>
                            <option value="-release_date">Сначала свежие релизы</option>
                            <option value="-average_rating">Сначала высокий рейтинг</option>
                            <option value="average_rating">Сначала низкий рейтинг</option>
                        </select>
                    </div>

                    {/* остальные фильтры */}
                    <select name="genres" className="p-2 border rounded" onChange={handleChange}>
                        <option value="">Все жанры</option>
                        {genresList.map(g => <option key={g.id} value={g.id}>{g.name}</option>)}
                    </select>

                    <select name="platforms" className="p-2 border rounded" onChange={handleChange}>
                        <option value="">Все платформы</option>
                        {platformsList.map(p => <option key={p.id} value={p.id}>{p.name}</option>)}
                    </select>

                    <div className="flex gap-2 items-center">
                        <input name="min_year" type="number" placeholder="От года" className="p-2 border rounded w-1/2" onChange={handleChange} />
                        <span>-</span>
                        <input name="max_year" type="number" placeholder="До года" className="p-2 border rounded w-1/2" onChange={handleChange} />
                    </div>

                    <button type="submit" className="bg-blue-600 text-white p-2 rounded hover:bg-blue-700 font-bold mt-2">
                        Применить фильтры
                    </button>

                </form>
            </div>

            {/* сам вывод наших игр */}
            <div className="w-full md:w-3/4">
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                    {games.length > 0 ? (
                        games.map(game => <GameCard key={game.id} game={game} />)
                    ) : (
                        <p>Игры не найдены...</p>
                    )}
                </div>
            </div>
        </div>
    );
};

export default CatalogPage;