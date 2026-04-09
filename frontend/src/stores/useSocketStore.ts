import {create} from 'zustand';
import {io, type Socket} from 'socket.io-client';
import { useAuthStore } from './useAuthStore';
import type { SocketState } from '@/types/store';
import { useChatStore } from './useChatStore';

const baseURL = import.meta.env.VITE_SOCKET_URL;

export const useSocketStore = create<SocketState>((set, get) => ({
    socket: null,
    onlineUsers: [],
    connectSocket: () => {
        const accessToken = useAuthStore.getState().accessToken;
        const existingSocket = get().socket;

        if (existingSocket) return;

        const socket: Socket = io(baseURL, {
            auth: {token: accessToken},
            transports: ["websocket"]
        });

        set({socket});

        socket.on("connect", () => {
            console.log("socket connected")
        });

        socket.on("online_users", (userIds) => {
            set({onlineUsers: userIds});
        });

        socket.on("new_message", ({conversation, message}) => {
            useChatStore.getState().addMessage(message);
            const {conversations} = useChatStore.getState();

            const oldConversation = conversations.filter((c) => c.id === conversation.id)[0];
            const unreadCounts = { ...oldConversation.unreadCounts };
            oldConversation.participants.forEach(p => {
                if (p.id === conversation.lastMessage.sender.id) {
                    unreadCounts[p.id] = 0;
                } else {
                    const currentCount = unreadCounts[p.id] || 0;
                    unreadCounts[p.id] = currentCount + 1;
                }
            });

            const updatedConversation = {
                ...conversation,
                unreadCounts,
            }

            if (useChatStore.getState().activeConversationId === message.conversationId) {
                useChatStore.getState().markAsSeen(); 
            }

            useChatStore.getState().updateConversation(updatedConversation)
        });

        socket.on("read_message", ({conversation}) => {
            const {conversations} = useChatStore.getState();
            const oldConversation = conversations.filter((c) => c.id === conversation.id)[0];
            const seenBy = [
                ...oldConversation.seenBy,
                ...conversation.seenBy 
            ];

            const updated = {
                ...conversation,
                seenBy
            }

            useChatStore.getState().updateConversation(updated);
        });

        socket.on("new_direct", (conversation) => {
            useChatStore.getState().addConvo(conversation, false);
            socket.emit("join_conversation", conversation.id);
        })

        socket.on("new_group", (conversation) => {
            useChatStore.getState().addConvo(conversation, false);
            socket.emit("join_conversation", conversation.id);
        });
    },
    disconnectSocket: () => {
        const socket = get().socket;
        if (socket) {
            socket.disconnect();
            set({socket: null});
        }
    },
}))