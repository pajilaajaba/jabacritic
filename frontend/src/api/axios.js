import axios from 'axios';

const api = axios.create({
    baseURL:'/api/v1',
    headers: {'Content-Type':'application/json'}
    });

//перехватчик - чтобы добавлять каждый раз в заголовки нашщ токен - чтобы бэк понимал что мы зареганы
api.interceptors.request.use((config) => {
    const token = localStorage.getItem("access_token");
    if (!!token) {
        config.headers.Authorization = `Bearer ${token}`}
    return config
})


//перехватчик ответа - здесь написан чтобы не допустить ошибки 401
//если 
//
api.interceptors.response.use((response) =>{
    return response;
}, (error) => {
    if (error.response && error.response.status == 401){
        console.error('Токен протух, перезагрузите сайт');
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
    }
    return Promise.reject(error);}
);

export default api;