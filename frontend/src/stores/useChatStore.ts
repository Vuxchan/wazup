import { chatService } from "@/services/chatService";
import type { ChatState } from "@/types/store";
import { create } from "zustand";
import { persist } from "zustand/middleware";
import { useAuthStore } from "./useAuthStore";
import { useSocketStore } from "./useSocketStore";
import type { Message } from "@/types/chat";

export const useChatStore = create<ChatState>()(
    persist(
        (set, get) => ({
            conversations: [],
            messages: {},
            activeConversationId: null,
            convoLoading: false,
            messageLoading: false,
            loading: false,
            fakeConversation: null,

            setFakeConversation: (conversation) => {
                set({fakeConversation: conversation, activeConversationId: null});
            },

            setActiveConversation: (id) => {
                set({activeConversationId: id, fakeConversation: null});
            },
            reset: () => {
                set({
                    conversations: [],
                    messages: {},
                    activeConversationId: null,
                    convoLoading: false,
                    messageLoading: false,
                    fakeConversation: null
                })
            },
            fetchConversations: async () => {
                try {
                    set({convoLoading: true});
                    const {conversations} = await chatService.fetchConversations();

                    set({conversations, convoLoading: false});
                } catch (error) {
                    console.error("Error while fetching conversations", error);
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
                    const {messages, cursor, seenBy} = await chatService.fetchMessages(convoId, nextCursor)

                    const processed = messages.map((m: Message) => ({
                        ...m,
                        isOwn: m.senderId === user?.id,
                    }))

                    set((state) => ({conversations: state.conversations.map((c) => c.id === convoId ? {...c, seenBy} : c)}));

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
            },
            sendDirectMessage: async (recipientId, content, imgUrl) => {
                try {
                    const {activeConversationId} = get();
                    await chatService.sendDirectMessage(recipientId, content, imgUrl);

                    set((state) => ({conversations: state.conversations.map((c) => c.id === activeConversationId ? {...c, seenBy: []} : c)}));
                } catch (error) {
                    console.error("Error while sending direct message", error)
                }
            },
            sendGroupMessage: async (conversationId, content, imgUrl) => {
                try {
                    await chatService.sendGroupMessage(conversationId, content, imgUrl);
                    set((state) => ({conversations: state.conversations.map((c) => c.id === get().activeConversationId ? {...c, seenBy: []} : c)}));
                } catch (error) {
                    console.error("Error while sending group message", error)
                }
            },
            addMessage: async (message) => {
                try {
                    const {user} = useAuthStore.getState();
                    const {fetchMessages} = get();

                    message.isOwn = message.senderId === user?.id;

                    const convoId = message.conversationId;

                    let prevItems = get().messages[convoId]?.items ?? [];

                    if (prevItems.length === 0) {
                        await fetchMessages(message.conversationId);
                        prevItems = get().messages[convoId]?.items ?? [];
                    }

                    set((state) => {
                        if (prevItems.some((m) => m.id === message.id)) {
                            return state;
                        }

                        const updatedConversations = [
                            ...state.conversations.filter(convo => convo.id === convoId),
                            ...state.conversations.filter(convo => convo.id !== convoId)
                        ];

                        return {
                            messages: {
                                ...state.messages,
                                [convoId]: {
                                    items: [...prevItems, message],
                                    hasMore: state.messages[convoId].hasMore,
                                    nextCursor: state.messages[convoId].nextCursor ?? undefined
                                }
                            },
                            conversations: updatedConversations
                        }
                    })
                } catch (error) {
                    console.error("Error while adding message", error);
                }
            },
            updateConversation: (conversation) => {
                set((state) => ({
                    conversations: state.conversations.map((c) => c.id === conversation.id ? {...c, ...conversation} : c),
                }))
            },
            markAsSeen: async () => {
                try {
                    const {user} = useAuthStore.getState();
                    const {activeConversationId, conversations} = get();

                    if (!activeConversationId || !user) {
                        return;
                    }

                    const convo = conversations.find((c) => c.id === activeConversationId);

                    if (!convo) {
                        return;
                    }

                    if ((convo.unreadCounts?.[user.id] ?? 0) === 0) {
                        return;
                    }

                    await chatService.markAsSeen(activeConversationId);

                    set((state) => ({
                        conversations: state.conversations.map((c) => (
                            c.id === activeConversationId && c.lastMessage ? {
                                ...c,
                                unreadCounts: {
                                    ...c.unreadCounts,
                                    [user.id]: 0,
                                }
                            }
                            : c
                        ))
                    }))
                } catch (error) {
                    console.error("Error while marking as seen", error);
                }
            },
            addConvo: (convo, setActiveconvoId) => {
                set((state) => {
                    const exist = state.conversations.some((c) => c.id.toString() === convo.id.toString());

                    return {
                        conversations: exist ? state.conversations : [convo, ...state.conversations],
                        activeConversationId: setActiveconvoId ? convo.id : state.activeConversationId,
                        fakeConversation: null
                    }
                })
            },
            createConversation: async (type, name, memberIds) => {
                try {
                    set({loading: true});
                    const conversation = await chatService.createConversation(type, name, memberIds);

                    get().addConvo(conversation, true);

                    useSocketStore.getState().socket?.emit("join_conversation", conversation.id)
                } catch (error) {
                    console.error("Error while creating conversation", error);
                } finally {
                    set({loading: false});
                }
            },
        }),
        {
            name: "chat-storage",
            partialize: (state) => ({conversations: state.conversations})
        }
    )
)