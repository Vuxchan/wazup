import api from "@/lib/axios";
import type { ConversationResponse } from "@/types/chat";

const pageLimit = 50;

export const chatService = {
    async fetchConversations(): Promise<ConversationResponse> {
        const res = await api.get("/conversations");

        return {conversations: res.data};
    },

    async fetchMessages(id: string, cursor?: string) {
        const res = await api.get(`/conversations/${id}/messages?limit=${pageLimit}&cursor=${cursor}`)

        return {messages: res.data.messages, cursor: res.data.cursor, seenBy: res.data.seenBy};
    },
     
    async sendDirectMessage(recipientId: string, content: string = "", imgUrl?: string) {
        const res = await api.post("/messages/direct", {recipientId, content, imgUrl})

        return res.data;
    },

    async sendGroupMessage(conversationId: string, content: string = "", imgUrl?: string) {
        const res = await api.post("/messages/group", {conversationId, content, imgUrl})

        return res.data;
    },

    async markAsSeen(conversationId: string) {
        return api.patch(`/conversations/${conversationId}/seen`);
    },

    async createConversation(type: "direct" | "group", name: string, memberIds: string[]) {
        const res = await api.post("/conversations", {type, name, memberIds});
        
        return res.data;
    }
}