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

        socket.on("new_message", ({message, conversation, unreadCounts, sender}) => {
            console.log(message)
            useChatStore.getState().addMessage(message);

            const lastMessage = {
                id: conversation.lastMessage.id,
                content: conversation.lastMessage.content,
                createdAt: conversation.lastMessage.createdAt,
                sender: {
                    id: sender.id,
                    displayName: "",
                    avatarUrl: null
                }
            };

            const updatedConversation = {
                ...conversation,
                lastMessage,
                unreadCounts
            }

            useChatStore.getState().updateConversation(updatedConversation)
        })
    },
    disconnectSocket: () => {
        const socket = get().socket;
        if (socket) {
            socket.disconnect();
            set({socket: null});
        }
    },
}))