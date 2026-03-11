import api from "@/lib/axios";

export const authService = {
    signUp: async (
        username: string,
        password: string,
        email: string,
        firstName: string,
        lastName: string
    ) => {
        const res = await api.post("/api/v1/auth/signup", {username, password, email, firstName, lastName}, { withCredentials: true });

        return res.data;
    },

    signIn: async (
        email: string,
        password: string,
    ) => {
        const form = new URLSearchParams();
        form.append("username", email);
        form.append("password", password);

        const res = await api.post("/api/v1/auth/signin", form, { headers: { "Content-Type": "application/x-www-form-urlencoded" }, withCredentials: true });

        return res.data;
    },

    signOut: async () => {
        return api.post("/api/v1/auth/signout", {}, { withCredentials: true });
    },

    fetchMe: async () => {
        const res = await api.get("/api/v1/user/me", { withCredentials: true });

        return res.data;
    },

    refresh: async () => {
        const res = await api.post("/api/v1/auth/refresh", {}, { withCredentials: true });

        return res.data;
    }
}