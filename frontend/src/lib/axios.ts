import { useAuthStore } from "@/stores/useAuthStore";
import axios from "axios"

const api = axios.create({
    baseURL: import.meta.env.MODE === "development" ? "http://127.0.0.1:8000" : "/api",
    withCredentials: true,
});

api.interceptors.request.use((config) => {
    const {accessToken} = useAuthStore.getState();

    if (accessToken) {
        config.headers.Authorization = `Bearer ${accessToken}`;
    }

    return config;
})

api.interceptors.response.use((res) => res, async (error) => {
    const originalRequest = error.config;

    if (originalRequest.url.includes("/api/v1/auth/signup") || originalRequest.url.includes("/api/v1/auth/signin") || originalRequest.url.includes("/api/v1/auth/refresh")) {
        return Promise.reject(error);
    }

    originalRequest._retryCount = originalRequest._retryCount || 0;

    if (error.response?.status === 403 && originalRequest._retryCount < 4) {
        originalRequest._retryCount += 1;

        try {
            const res = await api.post("/api/v1/auth/refresh", { withCredentials: true });
            const newAccessToken = res.data.access_token;

            useAuthStore.getState().setAccessToken(newAccessToken);

            originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
            return api(originalRequest);
        } catch (refreshError) {
            useAuthStore.getState().clearState();
            return Promise.reject(refreshError);
        }
    }

    return Promise.reject(error);
})

export default api