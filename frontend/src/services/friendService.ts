import api from "@/lib/axios";

export const friendService = {
    async searchByUsername(username: string) {
        const res = await api.get(`/users/search?username=${username}`);

        return res.data;
    },

    async sendFriendRequest(to: string, requestMessage?: string) {
        const res = await api.post("/friends/requests", {to, requestMessage});
        
        return res.data.message;
    }
}