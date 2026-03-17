import { chatService } from "@/services/chatService";
import type { ChatState } from "@/types/store";
import { create } from "zustand";
import { persist } from "zustand/middleware";
import { useAuthStore } from "./useAuthStore";
import api from "@/lib/axios";

export const useChatStore = create<ChatState>()(
    persist(
        (set, get) => ({
            conversations: [],
            messages: {},
            activeConversationId: null,
            convoLoading: false,
            messageLoading: false,

            setActiveConversation: (id) => set({activeConversationId: id}),
            reset: () => {
                set({
                    conversations: [],
                    messages: {},
                    activeConversationId: null,
                    convoLoading: false,
                    messageLoading: false,
                })
            },
            fetchConversations: async () => {
                try {
                    set({convoLoading: true});
                    const {conversations} = await chatService.fetchConversations();
                    console.log(conversations)

                    set({conversations, convoLoading: false});
                } catch (error) {
                    console.log("Error while fetching conversations", error);
                    set({convoLoading: false});
                }
            },
            fetchMessages: async (conversationId) => {
                const {activeConversationId, messages} = get();
                const {user} = useAuthStore.getState();

                const convoId = conversationId ?? activeConversationId;

                if (!convoId) return;

                const current = messages?.[convoId];
                const nextCursor = current?.nextCursor === undefined ? "" : current?.nextCursor;

                if (nextCursor === null) return;

                set({messageLoading: true});

                try {
                    const {messages: fetched, cursor} = await chatService.fetchMessages(convoId, nextCursor)

                    const processed = fetched.map((m) => ({
                        ...m,
                        isOwn: m.senderId === user?.id,
                    }))

                    set((state) => {
                        const prev = state.messages[convoId]?.items ?? [];
                        const merged = prev.length > 0 ? [...processed, ...prev] : processed;

                        return {
                            messages: {
                                ...state.messages,
                                [convoId]: {
                                    items: merged,
                                    hasMore: !!cursor,
                                    nextCursor: cursor ?? null
                                }
                            }
                        }
                    })
                } catch (error) {
                    console.error("Error while fetching messages", error);
                } finally {
                    set({messageLoading: false});
                }
            }
        }),
        {
            name: "chat-storage",
            partialize: (state) => ({conversations: state.conversations})
        }
    )
)