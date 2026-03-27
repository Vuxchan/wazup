import api from "@/lib/axios";

export const friendService = {
    async searchByUsername(username: string) {
        const res = await api.get(`/users/search?username=${username}`);

        return res.data;
    },

    async sendFriendRequest(to: string, requestMessage?: string) {
        const res = await api.post("/friends/requests", {to, requestMessage});
        
        return res.data.message;
    },

    async getAllFriendRequest() {
        try {
            const res = await api.get("/friends/requests");
            const {sent, received} = res.data;
            return {sent, received}
        } catch (error) {
            console.error("Error while getting all friend requests", error);
        }
    },

    async acceptRequest(requestId: string) {
        try {
            const res = await api.post(`/friends/requests/${requestId}/accept`);
            return res.data.requestAcceptedBy;
        } catch (error) {
            console.error("Error while accepting friend request", error);
        }
    },

    async declineRequest(requestId: string) {
        try {
            await api.post(`/friends/requests/${requestId}/decline`);
        } catch (error) {
            console.error("Error while declining friend request", error);
        }
    },

    async getFriendList() {
        const res = await api.get("/friends");
        return res.data;
    }
}