import axios from 'axios';

const baseURL = `${location.origin}/api/` // eslint-disable-line no-restricted-globals

const axiosInstance = axios.create({
    baseURL: baseURL,
    timeout: 5000,
    headers: {
        'Authorization': localStorage.getItem('accessToken') ? "Bearer " + localStorage.getItem('accessToken') : null,
        'Content-Type': 'application/json',
        'accept': 'application/json'
    }
});


axiosInstance.interceptors.response.use(
    response => response,
    async error => {
        const originalRequest = error.config;

        // Prevent infinite loops
        if (error.response.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;

            if (error.response.data.error.code === "token_not_valid" &&
                error.response.status === 401 &&
                error.response.data.error.message === "Token is invalid or expired") {
                const refreshToken = localStorage.getItem('refreshToken');

                if (refreshToken) {
                    const tokenParts = JSON.parse(atob(refreshToken.split('.')[1]));

                    // exp date in token is expressed in seconds, while now() returns milliseconds:
                    const now = Math.ceil(Date.now() / 1000);

                    if (tokenParts.exp > now) {
                        axiosInstance.defaults.headers['Authorization'] = null
                        originalRequest.headers['Authorization'] = null
                        return await axiosInstance
                            .post('/auth/refresh/', { refreshToken: refreshToken })
                            .then((response) => {

                                localStorage.setItem('accessToken', response.data.accessToken);
                                localStorage.setItem('refreshToken', response.data.refreshToken);

                                axiosInstance.defaults.headers['Authorization'] = "Bearer " + response.data.accessToken;
                                originalRequest.headers['Authorization'] = "Bearer " + response.data.accessToken;

                                return axiosInstance(originalRequest);
                            })
                            .catch(err => {
                                console.log(err)
                            });
                    } else {
                        console.log("Refresh token is expired", tokenParts.exp, now);
                        window.location.href = '/';
                    }
                } else {
                    console.log("Refresh token not available.")
                    window.location.href = '/';
                }
            }

            // specific error handling done elsewhere
            return Promise.reject(error);
        }
    }
);

export default axiosInstance